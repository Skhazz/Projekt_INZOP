import sqlite3
from database import get_db_connection

class Zamowienia:
    @staticmethod
    def zloz_zamowienie(klient_id):
        """Tworzy zamówienie na podstawie produktów w koszyku klienta"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Pobieramy produkty z koszyka klienta
        cursor.execute('''
        SELECT k.produkt_id, p.marka, p.model, k.ilosc, k.cena, p.ilosc AS dostepna_ilosc
        FROM koszyk k
        JOIN produkty p ON k.produkt_id = p.id
        WHERE k.klient_id = ?
        ''', (klient_id,))
        produkty_w_koszyku = cursor.fetchall()

        if not produkty_w_koszyku:
            print(" Koszyk jest pusty, nie można złożyć zamówienia.")
            conn.close()
            return

        # Obliczamy sumę zamówienia
        suma_zamowienia = sum(produkt['cena'] for produkt in produkty_w_koszyku)

        # Klient wybiera sposób dostawy
        dostawa = None
        while dostawa not in ["kurier", "odbiór osobisty"]:
            dostawa = input("Wybierz sposób dostawy (kurier/odbiór osobisty): ").strip().lower()
            if dostawa not in ["kurier", "odbiór osobisty"]:
                print(" Nieprawidłowa opcja. Wybierz 'kurier' lub 'odbiór osobisty'.")

        # Wyświetlamy podsumowanie zamówienia
        print(f"\n Podsumowanie zamówienia klienta ID {klient_id}:")
        for produkt in produkty_w_koszyku:
            print(f"    {produkt['marka']} {produkt['model']} - {produkt['ilosc']} szt., Cena: {produkt['cena']} zł")

        print(f"\n Łączna wartość zamówienia: {suma_zamowienia} zł")
        print(f" Sposób dostawy: {dostawa}")

        # Potwierdzenie zamówienia
        potwierdzenie = input("Czy chcesz złożyć zamówienie? (tak/nie): ").strip().lower()
        if potwierdzenie != "tak":
            print(" Zamówienie anulowane.")
            conn.close()
            return

        # Tworzymy nowe zamówienie w bazie
        cursor.execute("INSERT INTO zamowienia (klient_id, suma, dostawa) VALUES (?, ?, ?)",
                       (klient_id, suma_zamowienia, dostawa))
        zamowienie_id = cursor.lastrowid  # Pobieramy ID nowego zamówienia

        # Dodajemy produkty do `zamowione_produkty` i aktualizujemy stan magazynowy
        for produkt in produkty_w_koszyku:
            produkt_id = produkt["produkt_id"]
            ilosc_zamowiona = produkt["ilosc"]
            cena = produkt["cena"]
            dostepna_ilosc = produkt["dostepna_ilosc"]

            if ilosc_zamowiona > dostepna_ilosc:
                print(f" Nie można zamówić {ilosc_zamowiona} szt. {produkt['marka']} {produkt['model']}, bo na stanie jest tylko {dostepna_ilosc} szt.")
                conn.close()
                return

            cursor.execute("INSERT INTO zamowione_produkty (zamowienie_id, produkt_id, ilosc, cena) VALUES (?, ?, ?, ?)",
                           (zamowienie_id, produkt_id, ilosc_zamowiona, cena))
            cursor.execute("UPDATE produkty SET ilosc = ilosc - ? WHERE id = ?", (ilosc_zamowiona, produkt_id))

        # Opróżniamy koszyk po złożeniu zamówienia
        cursor.execute("DELETE FROM koszyk WHERE klient_id = ?", (klient_id,))
        conn.commit()
        conn.close()
        Zamowienia.generuj_fakture(zamowienie_id)

        print(f" Zamówienie ID {zamowienie_id} zostało złożone!  Dostawa: {dostawa}")

    @staticmethod
    def wyswietl_zamowienia_klienta(klient_id):
        """Wyświetla zamówienia klienta z produktami"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Pobieramy zamówienia klienta
        cursor.execute('''
           SELECT id, data_zamowienia, suma, dostawa FROM zamowienia WHERE klient_id = ?
           ''', (klient_id,))
        zamowienia = cursor.fetchall()

        if not zamowienia:
            print(f" Klient ID {klient_id} nie ma żadnych zamówień.")
            conn.close()
            return

        print(f"\n Zamówienia klienta ID {klient_id}:")
        for zamowienie in zamowienia:
            zamowienie_id = zamowienie["id"]
            print(f"\n Zamówienie ID: {zamowienie_id} | Data: {zamowienie['data_zamowienia']}")
            print(f" Dostawa: {zamowienie['dostawa']} |  Suma: {zamowienie['suma']} zł")

            # Pobieramy produkty w danym zamówieniu
            cursor.execute('''
               SELECT p.marka, p.model, zp.ilosc, zp.cena
               FROM zamowione_produkty zp
               JOIN produkty p ON zp.produkt_id = p.id
               WHERE zp.zamowienie_id = ?
               ''', (zamowienie_id,))
            produkty = cursor.fetchall()

            for produkt in produkty:
                print(
                    f"   {produkt['marka']} {produkt['model']} - {produkt['ilosc']} szt., Cena: {produkt['cena']} zł")

        conn.close()

    @staticmethod
    def generuj_raport_sprzedazy(data_od=None, data_do=None):
        """Generuje raport sprzedaży dla podanego zakresu dat"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Filtrujemy po dacie, jeśli podano zakres
        warunek_daty = ""
        parametry = []
        if data_od and data_do:
            warunek_daty = "WHERE z.data_zamowienia BETWEEN ? AND ?"
            parametry = [data_od, data_do]
        elif data_od:
            warunek_daty = "WHERE z.data_zamowienia >= ?"
            parametry = [data_od]
        elif data_do:
            warunek_daty = "WHERE z.data_zamowienia <= ?"
            parametry = [data_do]

        # Pobieramy łączną liczbę zamówień i sprzedaż netto/brutto
        cursor.execute(f'''
            SELECT COUNT(z.id) AS liczba_zamowien, 
                   SUM(f.suma_netto) AS suma_netto, 
                   SUM(f.suma_brutto) AS suma_brutto
            FROM zamowienia z
            JOIN faktury f ON z.id = f.zamowienie_id
            {warunek_daty}
            ''', parametry)
        raport = cursor.fetchone()

        liczba_zamowien = raport["liczba_zamowien"] or 0
        suma_netto = raport["suma_netto"] or 0
        suma_brutto = raport["suma_brutto"] or 0
        vat = suma_brutto - suma_netto  # Obliczamy VAT

        print("\n RAPORT SPRZEDAŻY ")
        if data_od and data_do:
            print(f"🗓 Zakres: {data_od} - {data_do}")
        elif data_od:
            print(f"🗓 Od: {data_od}")
        elif data_do:
            print(f"🗓 Do: {data_do}")

        print(f" Liczba zamówień: {liczba_zamowien}")
        print(f" Suma netto: {suma_netto:.2f} zł")
        print(f" VAT 23%: {vat:.2f} zł")
        print(f" Suma brutto: {suma_brutto:.2f} zł")

        # Pobieramy najczęściej kupowane produkty
        cursor.execute(f'''
            SELECT p.marka, p.model, SUM(zp.ilosc) AS sprzedane_sztuki
            FROM zamowione_produkty zp
            JOIN produkty p ON zp.produkt_id = p.id
            JOIN zamowienia z ON zp.zamowienie_id = z.id
            {warunek_daty}
            GROUP BY p.id
            ORDER BY sprzedane_sztuki DESC
            LIMIT 5
            ''', parametry)
        bestsellery = cursor.fetchall()

        print("\n Najczęściej kupowane produkty:")
        for produkt in bestsellery:
            print(f"    {produkt['marka']} {produkt['model']} - {produkt['sprzedane_sztuki']} szt.")

        conn.close()

    @staticmethod
    def anuluj_zamowienie(zamowienie_id):
        """Anuluje zamówienie, zwraca produkty na stan i usuwa powiązane wpisy"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Sprawdzamy, czy zamówienie istnieje
        cursor.execute("SELECT * FROM zamowienia WHERE id = ?", (zamowienie_id,))
        zamowienie = cursor.fetchone()

        if not zamowienie:
            print(f" Zamówienie ID {zamowienie_id} nie istnieje.")
            conn.close()
            return

        # Pobieramy produkty zamówione w tym zamówieniu
        cursor.execute("SELECT produkt_id, ilosc FROM zamowione_produkty WHERE zamowienie_id = ?", (zamowienie_id,))
        produkty = cursor.fetchall()

        if not produkty:
            print(f"️ Zamówienie ID {zamowienie_id} nie zawiera produktów.")
            conn.close()
            return

        # Zwracamy produkty na stan magazynowy
        for produkt in produkty:
            produkt_id = produkt["produkt_id"]
            ilosc_zwrocona = produkt["ilosc"]
            cursor.execute("UPDATE produkty SET ilosc = ilosc + ? WHERE id = ?", (ilosc_zwrocona, produkt_id))

        # Usuwamy produkty z tabeli `zamowione_produkty`
        cursor.execute("DELETE FROM zamowione_produkty WHERE zamowienie_id = ?", (zamowienie_id,))

        # Usuwamy fakturę powiązaną z zamówieniem
        cursor.execute("DELETE FROM faktury WHERE zamowienie_id = ?", (zamowienie_id,))

        # Usuwamy zamówienie
        cursor.execute("DELETE FROM zamowienia WHERE id = ?", (zamowienie_id,))

        conn.commit()
        conn.close()
        print(f" Zamówienie ID {zamowienie_id} zostało anulowane, produkty zwrócone na magazyn.")

    @staticmethod
    def generuj_fakture(zamowienie_id):
        """Generuje fakturę dla danego zamówienia, zapisuje ją w bazie i do pliku"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Pobieramy dane zamówienia
        cursor.execute('''
            SELECT z.klient_id, z.data_zamowienia, z.suma, z.dostawa, k.imie, k.nazwisko, k.adres
            FROM zamowienia z
            JOIN klienci k ON z.klient_id = k.id
            WHERE z.id = ?
            ''', (zamowienie_id,))
        zamowienie = cursor.fetchone()

        if not zamowienie:
            print(f" Zamówienie ID {zamowienie_id} nie istnieje.")
            conn.close()
            return

        # Pobieramy produkty z zamówienia
        cursor.execute('''
            SELECT p.marka, p.model, zp.ilosc, zp.cena
            FROM zamowione_produkty zp
            JOIN produkty p ON zp.produkt_id = p.id
            WHERE zp.zamowienie_id = ?
            ''', (zamowienie_id,))
        produkty = cursor.fetchall()

        # Obliczamy VAT 23%
        suma_netto = zamowienie["suma"]
        vat = round(suma_netto * 0.23, 2)
        suma_brutto = round(suma_netto + vat, 2)

        # Zapisujemy fakturę do bazy
        cursor.execute('''
            INSERT INTO faktury (zamowienie_id, klient_id, suma_netto, vat, suma_brutto)
            VALUES (?, ?, ?, ?, ?)
            ''', (zamowienie_id, zamowienie["klient_id"], suma_netto, vat, suma_brutto))
        faktura_id = cursor.lastrowid
        conn.commit()

        conn.close()

        # Tworzymy zawartość faktury
        faktura_content = f"""
            ==============================
                    FAKTURA VAT
            ==============================
            Numer faktury: {faktura_id}
            Numer zamówienia: {zamowienie_id}
            Data: {zamowienie["data_zamowienia"]}

            Klient: {zamowienie["imie"]} {zamowienie["nazwisko"]}
            Adres: {zamowienie["adres"]}

            ------------------------------
            Produkty:
            ------------------------------
            """
        for produkt in produkty:
            faktura_content += f"   {produkt['marka']} {produkt['model']} - {produkt['ilosc']} szt., Cena: {produkt['cena']} zł\n"

        faktura_content += f"""
            ------------------------------
             Dostawa: {zamowienie["dostawa"]}
             Suma netto: {suma_netto} zł
             VAT 23%: {vat} zł
             Suma brutto: {suma_brutto} zł
            ------------------------------

            Dziękujemy za zakupy w naszym sklepie!
            """

        # Zapisujemy fakturę do pliku
        filename = f"faktura_{faktura_id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(faktura_content)

        # Wyświetlamy fakturę
        print(faktura_content)
        print(f" Faktura zapisana jako {filename}")

