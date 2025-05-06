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

        # Sprawdź dostępność wszystkich produktów
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

            # Zmniejsz ilość w magazynie
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

            Faktura.generuj_plik(
                zamowienie_id=zamowienie_id,
                klient_id=klient_id,
                suma_netto=round(suma_netto, 2),
                vat=vat,
                suma_brutto=round(suma_brutto, 2)
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
    def anuluj_zamowienie(zamowienie_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Pobierz produkty z zamówienia
        cursor.execute("""
            SELECT produkt_id, ilosc
            FROM zamowione_produkty
            WHERE zamowienie_id = ?
        """, (zamowienie_id,))
        produkty = cursor.fetchall()

        # Przywróć ilości do magazynu
        for item in produkty:
            produkt_id = item["produkt_id"]
            ilosc = item["ilosc"]
            cursor.execute("""
                UPDATE produkty
                SET ilosc = ilosc + ?
                WHERE id = ?
            """, (ilosc, produkt_id))

        # Usuń powiązane rekordy
        cursor.execute("DELETE FROM zamowione_produkty WHERE zamowienie_id = ?", (zamowienie_id,))
        cursor.execute("DELETE FROM faktury WHERE zamowienie_id = ?", (zamowienie_id,))
        cursor.execute("DELETE FROM zamowienia WHERE id = ?", (zamowienie_id,))

        conn.commit()
        conn.close()

        print(f"Zamówienie ID {zamowienie_id} zostało anulowane, a ilości produktów przywrócone.")

    @staticmethod
    def generuj_raport_sprzedazy(data_od=None, data_do=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT z.id, z.data_zamowienia, z.suma, k.imie || ' ' || k.nazwisko AS klient
            FROM zamowienia z
            JOIN klienci k ON z.klient_id = k.id
            WHERE 1=1
        """
        params = []

        if data_od:
            query += " AND z.data_zamowienia >= ?"
            params.append(data_od)
        if data_do:
            query += " AND z.data_zamowienia <= ?"
            params.append(data_do)

        cursor.execute(query, params)
        wyniki = cursor.fetchall()

        if not wyniki:
            print("Brak zamówień w podanym zakresie.")
        else:
            print("\n--- Raport sprzedaży ---")
            for z in wyniki:
                print(
                    f"Zamówienie #{z['id']} | Data: {z['data_zamowienia']} | Suma: {z['suma']} zł | Klient: {z['klient']}")
            print(f"\nŁącznie: {sum(z['suma'] for z in wyniki)} zł")

        conn.close()
