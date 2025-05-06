from database import get_db_connection

class Koszyk:

    @staticmethod
    def dodaj_do_koszyka(klient_id, produkt_id, ilosc):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Sprawdź, czy produkt istnieje i ma wystarczającą ilość
        cursor.execute("SELECT ilosc, cena FROM produkty WHERE id = ?", (produkt_id,))
        produkt = cursor.fetchone()

        if not produkt:
            print("Nie znaleziono produktu o podanym ID.")
            conn.close()
            return

        if produkt["ilosc"] < ilosc:
            print("Brak wystarczającej ilości produktu na stanie.")
            conn.close()
            return

        cena = produkt["cena"]

        # Sprawdź, czy produkt jest już w koszyku
        cursor.execute("SELECT id, ilosc FROM koszyk WHERE klient_id = ? AND produkt_id = ?", (klient_id, produkt_id))
        istnieje = cursor.fetchone()

        if istnieje:
            nowa_ilosc = istnieje["ilosc"] + ilosc
            cursor.execute("UPDATE koszyk SET ilosc = ?, cena = ? WHERE id = ?", (nowa_ilosc, cena, istnieje["id"]))
        else:
            cursor.execute("INSERT INTO koszyk (klient_id, produkt_id, ilosc, cena) VALUES (?, ?, ?, ?)",
                           (klient_id, produkt_id, ilosc, cena))

        conn.commit()
        conn.close()
        print("Produkt dodany do koszyka.")

    @staticmethod
    def wyswietl_koszyk(klient_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT k.ilosc, k.cena, p.marka, p.model
            FROM koszyk k
            JOIN produkty p ON k.produkt_id = p.id
            WHERE k.klient_id = ?
        ''', (klient_id,))
        produkty = cursor.fetchall()

        if not produkty:
            print("Koszyk jest pusty.")
        else:
            print("\n--- Zawartość koszyka ---")
            for p in produkty:
                print(f"{p['marka']} {p['model']} | Ilość: {p['ilosc']} | Cena za sztukę: {p['cena']} zł")

        conn.close()
