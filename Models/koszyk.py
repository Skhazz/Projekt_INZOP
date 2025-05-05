import sqlite3
from database import get_db_connection

class Koszyk:
    @staticmethod
    def dodaj_do_koszyka(klient_id, produkt_id, ilosc):
        """Dodaje produkt do koszyka klienta lub zwiększa ilość i sumuje cenę"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Pobranie dostępnej ilości produktu
        cursor.execute("SELECT ilosc, cena FROM produkty WHERE id = ?", (produkt_id,))
        produkt = cursor.fetchone()

        if produkt is None:
            print(f" Produkt o ID {produkt_id} nie istnieje!")
            conn.close()
            return

        dostepna_ilosc = produkt["ilosc"]
        cena_jednostkowa = produkt["cena"]

        # Pobranie obecnej ilości produktu w koszyku danego klienta
        cursor.execute("SELECT ilosc, cena FROM koszyk WHERE klient_id = ? AND produkt_id = ?", (klient_id, produkt_id))
        koszyk_pozycja = cursor.fetchone()

        if koszyk_pozycja:
            # Produkt już w koszyku → sprawdzamy, czy można dodać więcej
            nowa_ilosc = koszyk_pozycja["ilosc"] + ilosc

            if nowa_ilosc > dostepna_ilosc:
                print(
                    f" Nie możesz dodać więcej niż {dostepna_ilosc} szt. tego produktu! (W twoim koszyku: {koszyk_pozycja['ilosc']} szt.)")
            else:
                # Aktualizujemy ilość i sumujemy cenę w koszyku
                nowa_cena = koszyk_pozycja["cena"] + (ilosc * cena_jednostkowa)
                cursor.execute("UPDATE koszyk SET ilosc = ?, cena = ? WHERE klient_id = ? AND produkt_id = ?",
                               (nowa_ilosc, nowa_cena, klient_id, produkt_id))
                conn.commit()
                print(
                    f" Zaktualizowano ilość produktu ID {produkt_id} w koszyku klienta ID {klient_id} → Teraz: {nowa_ilosc} szt., Łączna cena: {nowa_cena} zł")

        else:
            # Produkt nie jest jeszcze w koszyku → dodajemy nowy wpis
            if ilosc > dostepna_ilosc:
                print(f" Nie możesz dodać więcej niż {dostepna_ilosc} szt. tego produktu!")
            else:
                cena_laczna = ilosc * cena_jednostkowa
                cursor.execute("INSERT INTO koszyk (klient_id, produkt_id, ilosc, cena) VALUES (?, ?, ?, ?)",
                               (klient_id, produkt_id, ilosc, cena_laczna))
                conn.commit()
                print(
                    f" Produkt ID {produkt_id} dodany do koszyka klienta ID {klient_id}. Łączna cena: {cena_laczna} zł.")

    @staticmethod
    def usun_z_koszyka(klient_id, produkt_id, ilosc=None):
        """Usuwa określoną ilość produktu z koszyka klienta lub całość"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Sprawdzenie, czy produkt istnieje w koszyku
        cursor.execute("SELECT ilosc, cena FROM koszyk WHERE klient_id = ? AND produkt_id = ?", (klient_id, produkt_id))
        pozycja = cursor.fetchone()

        if pozycja is None:
            print(f"️ Produkt ID {produkt_id} nie znajduje się w koszyku klienta ID {klient_id}.")
            conn.close()
            return

        obecna_ilosc = pozycja["ilosc"]
        cena_jednostkowa = pozycja["cena"] / obecna_ilosc  # Obliczenie ceny jednej sztuki

        # Jeśli użytkownik nie podał ilości, pytamy ponownie
        while ilosc is None or not str(ilosc).isdigit():
            ilosc = input(" Podaj ilość do usunięcia lub wciśnij Enter, aby anulować: ").strip()
            if ilosc == "":
                print(" Anulowano usuwanie, wracamy do menu.")
                conn.close()
                return
            if not ilosc.isdigit():
                print(" Ilość musi być liczbą całkowitą!")
                continue
            ilosc = int(ilosc)

        # Sprawdzamy, czy użytkownik chce usunąć więcej niż ma w koszyku
        if ilosc >= obecna_ilosc:
            # Usuń cały produkt z koszyka
            cursor.execute("DELETE FROM koszyk WHERE klient_id = ? AND produkt_id = ?", (klient_id, produkt_id))
            conn.commit()
            print(f" Usunięto cały produkt ID {produkt_id} z koszyka klienta ID {klient_id}.")
        else:
            # Odejmujemy tylko część sztuk i aktualizujemy cenę
            nowa_ilosc = obecna_ilosc - ilosc
            nowa_cena = nowa_ilosc * cena_jednostkowa
            cursor.execute("UPDATE koszyk SET ilosc = ?, cena = ? WHERE klient_id = ? AND produkt_id = ?",
                           (nowa_ilosc, nowa_cena, klient_id, produkt_id))
            conn.commit()
            print(
                f" Zaktualizowano ilość produktu ID {produkt_id} w koszyku klienta ID {klient_id} → Pozostało: {nowa_ilosc} szt., Łączna cena: {nowa_cena} zł")

    @staticmethod
    def wyswietl_koszyk(klient_id):
        """Wyświetla koszyk klienta"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
        SELECT k.produkt_id, p.marka, p.model, k.ilosc, k.cena
        FROM koszyk k
        JOIN produkty p ON k.produkt_id = p.id
        WHERE k.klient_id = ?
        ''', (klient_id,))
        produkty = cursor.fetchall()

        if produkty:
            print(f"\n Koszyk klienta ID {klient_id}:")
            suma_koszyka = 0  # Zmienna do sumowania całkowitej wartości koszyka
            for produkt in produkty:
                suma_koszyka += produkt['cena']  # Sumujemy ceny wszystkich produktów
                print(
                    f"    ID: {produkt['produkt_id']} | {produkt['marka']} {produkt['model']} - {produkt['ilosc']} szt., Łączna cena: {produkt['cena']} zł")
            print(f"\n Suma do zapłaty: {suma_koszyka} zł")
        else:
            print(f" Koszyk klienta ID {klient_id} jest pusty.")

        conn.close()