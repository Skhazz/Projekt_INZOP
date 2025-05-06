from database import get_db_connection

class Koszyk:

    @staticmethod
    def dodaj_do_koszyka(klient_id, produkt_id, ilosc):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Pobierz cenę produktu
        cursor.execute("SELECT cena FROM produkty WHERE id = ?", (produkt_id,))
        produkt = cursor.fetchone()
        if not produkt:
            print("Nie znaleziono produktu o podanym ID.")
            conn.close()
            return

        cena = produkt["cena"] * ilosc

        # Dodaj do koszyka
        cursor.execute("""
            INSERT INTO koszyk (klient_id, produkt_id, ilosc, cena)
            VALUES (?, ?, ?, ?)
        """, (klient_id, produkt_id, ilosc, cena))

        conn.commit()
        conn.close()
        print("Produkt dodany do koszyka.")

    @staticmethod
    def usun_z_koszyka(klient_id, produkt_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM koszyk WHERE klient_id = ? AND produkt_id = ?", (klient_id, produkt_id))
        conn.commit()
        conn.close()
        print("Produkt usunięty z koszyka.")

    @staticmethod
    def wyswietl_koszyk(klient_id):
        """Wyświetla koszyk klienta"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
        SELECT k.produkt_id, (p.marka || ' ' || p.model) AS nazwa, k.ilosc, k.cena
        FROM koszyk k
        JOIN produkty p ON k.produkt_id = p.id
        WHERE k.klient_id = ?
        ''', (klient_id,))
        produkty = cursor.fetchall()

        if produkty:
            print(f"\n Koszyk klienta ID {klient_id}:")
            suma_koszyka = 0
            for produkt in produkty:
                suma_koszyka += produkt['cena']
                print(f"    ID: {produkt['produkt_id']} | {produkt['nazwa']} - {produkt['ilosc']} szt., Łączna cena: {produkt['cena']} zł")
            print(f"\n Suma do zapłaty: {suma_koszyka} zł")
        else:
            print(f" Koszyk klienta ID {klient_id} jest pusty.")

        conn.close()
