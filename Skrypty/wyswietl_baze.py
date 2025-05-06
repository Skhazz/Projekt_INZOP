from database import get_db_connection

def wyswietl_baze():
    """Wyświetla całą zawartość bazy danych"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        print("\n*** ZAWARTOŚĆ BAZY DANYCH ***\n")


        print(" Klienci:")
        cursor.execute("SELECT * FROM klienci")
        klienci = cursor.fetchall()
        if klienci:
            for klient in klienci:
                print(dict(klient))
        else:
            print("Brak klientów w bazie.")


        print("\n Produkty w sklepie:")
        cursor.execute("SELECT * FROM produkty")
        produkty = cursor.fetchall()

        if produkty:
            for produkt in produkty:
                if produkt["kategoria"] == "gitara":
                    print(
                        f"{produkt['marka']} {produkt['model']} ({produkt['rodzaj']}) - {produkt['ilosc_strun']} strun, {produkt['rodzaj_przetwornikow']}, Cena: {produkt['cena']} zł, Ilość: {produkt['ilosc']} szt.")
                elif produkt["kategoria"] == "perkusja":
                    print(
                        f"{produkt['marka']} {produkt['model']} - {produkt['ilosc_bebnow']} bębnów, {produkt['rodzaj_naciagow']}, Cena: {produkt['cena']} zł, Ilość: {produkt['ilosc']} szt.")
        else:
            print("Brak produktów w bazie.")


        print("\n Zamówienia:")
        cursor.execute("SELECT * FROM zamowienia")
        zamowienia = cursor.fetchall()
        if zamowienia:
            for zamowienie in zamowienia:
                print(dict(zamowienie))
        else:
            print("Brak zamówień w bazie.")


        print("\n Pozycje zamówień:")
        cursor.execute("SELECT * FROM pozycje_zamowienia")
        pozycje = cursor.fetchall()
        if pozycje:
            for pozycja in pozycje:
                print(dict(pozycja))
        else:
            print("Brak pozycji zamówień w bazie.")

        print("\n Koszyki klientów:")
        cursor.execute('''
                SELECT k.klient_id, p.marka, p.model, p.cena, k.ilosc
                FROM koszyk k
                JOIN produkty p ON k.produkt_id = p.id
                ORDER BY k.klient_id
                ''')
        koszyk = cursor.fetchall()
        if koszyk:
            aktualny_klient = None
            for item in koszyk:
                klient_id = item["klient_id"]
                if klient_id != aktualny_klient:
                    print(f"\n Koszyk klienta ID {klient_id}:")
                    aktualny_klient = klient_id
                print(f" {item['marka']} {item['model']} - {item['ilosc']} szt., Cena: {item['cena']} zł")
        else:
            print("Brak produktów w koszykach klientów.")

    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    wyswietl_baze()
