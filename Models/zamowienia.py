from database import get_db_connection
from Models.faktura import Faktura

class Zamowienia:

    @staticmethod
    def zloz_zamowienie(konto_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM klienci WHERE konto_id = ?", (int(konto_id),))
        klient_row = cursor.fetchone()
        if klient_row is None:
            print("Nie znaleziono klienta powiązanego z tym kontem.")
            conn.close()
            return

        klient_id = klient_row["id"]

        cursor.execute("SELECT produkt_id, ilosc, cena FROM koszyk WHERE klient_id = ?", (klient_id,))
        koszyk = cursor.fetchall()
        if not koszyk:
            print("Koszyk jest pusty.")
            conn.close()
            return


        for item in koszyk:
            cursor.execute("SELECT ilosc FROM produkty WHERE id = ?", (item["produkt_id"],))
            produkt = cursor.fetchone()
            if not produkt or produkt["ilosc"] < item["ilosc"]:
                print(f"Brak wystarczającej ilości produktu ID {item['produkt_id']}.")
                conn.close()
                return

        suma = sum(item["ilosc"] * item["cena"] for item in koszyk)

        dostawa = input("Wybierz sposób dostawy (kurier/odbiór osobisty): ").strip().lower()
        if dostawa not in ["kurier", "odbiór osobisty"]:
            print("Nieprawidłowy sposób dostawy.")
            conn.close()
            return

        cursor.execute('''
            INSERT INTO zamowienia (klient_id, suma, dostawa)
            VALUES (?, ?, ?)
        ''', (klient_id, suma, dostawa))
        zamowienie_id = cursor.lastrowid

        for item in koszyk:
            cursor.execute('''
                INSERT INTO zamowione_produkty (zamowienie_id, produkt_id, ilosc, cena)
                VALUES (?, ?, ?, ?)
            ''', (zamowienie_id, item["produkt_id"], item["ilosc"], item["cena"]))

            cursor.execute(
                "UPDATE produkty SET ilosc = ilosc - ? WHERE id = ?",
                (item["ilosc"], item["produkt_id"])
            )

        try:
            vat = 0.23
            suma_netto = suma / (1 + vat)
            suma_brutto = suma
            cursor.execute('''
                INSERT INTO faktury (zamowienie_id, klient_id, suma_netto, vat, suma_brutto)
                VALUES (?, ?, ?, ?, ?)
            ''', (zamowienie_id, klient_id, round(suma_netto, 2), vat, round(suma_brutto, 2)))

            # Pobierz dane produktów do faktury
            cursor.execute('''
                SELECT p.marka, p.model, zp.ilosc, zp.cena
                FROM zamowione_produkty zp
                JOIN produkty p ON zp.produkt_id = p.id
                WHERE zp.zamowienie_id = ?
            ''', (zamowienie_id,))
            produkty = cursor.fetchall()
            produkty_list = [dict(p) for p in produkty]

            Faktura.generuj_plik(
                zamowienie_id=zamowienie_id,
                klient_id=klient_id,
                suma_netto=round(suma_netto, 2),
                vat=vat,
                suma_brutto=round(suma_brutto, 2),
                produkty=produkty_list,
                dostawa=dostawa
            )

            print("Faktura została wygenerowana.")
        except Exception as e:
            print(f"Błąd przy generowaniu faktury: {e}")

        cursor.execute("DELETE FROM koszyk WHERE klient_id = ?", (klient_id,))

        conn.commit()
        conn.close()

        print("Zamówienie złożone pomyślnie.")

    @staticmethod
    def wyswietl_zamowienia_klienta(klient_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, suma, dostawa, data_zamowienia
            FROM zamowienia
            WHERE klient_id = ?
            ORDER BY data_zamowienia DESC
        """, (klient_id,))
        zamowienia = cursor.fetchall()

        if zamowienia:
            print("Twoje zamówienia:")
            for z in zamowienia:
                print(f"ID: {z['id']}, Suma: {z['suma']} zł, Dostawa: {z['dostawa']}, Data: {z['data_zamowienia']}")
        else:
            print("Brak zamówień dla tego klienta.")

        conn.close()

    @staticmethod
    def anuluj_zamowienie(konto_id):
        try:
            zamowienie_id = int(input("Podaj ID zamówienia do anulowania: "))
        except ValueError:
            print("Nieprawidłowy numer zamówienia.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()


        cursor.execute("SELECT id FROM klienci WHERE konto_id = ?", (konto_id,))
        klient = cursor.fetchone()
        if not klient:
            print("Nie znaleziono klienta.")
            conn.close()
            return

        klient_id = klient["id"]


        cursor.execute("SELECT id FROM zamowienia WHERE id = ? AND klient_id = ?", (zamowienie_id, klient_id))
        zamowienie = cursor.fetchone()
        if not zamowienie:
            print("Nie znaleziono zamówienia powiązanego z tym kontem.")
            conn.close()
            return


        cursor.execute("SELECT produkt_id, ilosc FROM zamowione_produkty WHERE zamowienie_id = ?", (zamowienie_id,))
        produkty = cursor.fetchall()
        for produkt in produkty:
            cursor.execute("UPDATE produkty SET ilosc = ilosc + ? WHERE id = ?",
                           (produkt["ilosc"], produkt["produkt_id"]))


        cursor.execute("DELETE FROM faktury WHERE zamowienie_id = ?", (zamowienie_id,))
        cursor.execute("DELETE FROM zamowione_produkty WHERE zamowienie_id = ?", (zamowienie_id,))
        cursor.execute("DELETE FROM zamowienia WHERE id = ?", (zamowienie_id,))

        conn.commit()
        conn.close()
        print("Zamówienie zostało anulowane.")

    @staticmethod
    def generuj_raport_sprzedazy(data_od=None, data_do=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = '''
                SELECT z.id, z.data_zamowienia, z.suma, z.dostawa, COUNT(zp.id) as liczba_produktow
                FROM zamowienia z
                LEFT JOIN zamowione_produkty zp ON z.id = zp.zamowienie_id
            '''
        params = []

        if data_od and data_do:
            query += " WHERE DATE(z.data_zamowienia) BETWEEN ? AND ?"
            params = [data_od, data_do]
        elif data_od:
            query += " WHERE DATE(z.data_zamowienia) >= ?"
            params = [data_od]
        elif data_do:
            query += " WHERE DATE(z.data_zamowienia) <= ?"
            params = [data_do]

        query += " GROUP BY z.id ORDER BY z.data_zamowienia DESC"

        cursor.execute(query, params)
        zamowienia = cursor.fetchall()

        print("\n=== RAPORT SPRZEDAŻY ===")
        if zamowienia:
            for z in zamowienia:
                print(
                    f"Zamówienie ID: {z['id']} | Data: {z['data_zamowienia']} | Suma: {z['suma']} zł | Dostawa: {z['dostawa']} | Liczba produktów: {z['liczba_produktow']}")
        else:
            print("Brak danych do wyświetlenia w wybranym zakresie.")

        conn.close()