from database import get_db_connection

def wyswietl_produkty():
    """Wyświetla listę dostępnych produktów w sklepie"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        print("\n Produkty dostępne w sklepie:")
        cursor.execute("SELECT * FROM produkty")
        produkty = cursor.fetchall()

        if produkty:
            for produkt in produkty:
                if produkt["kategoria"] == "gitara":
                    print(f" ID: {produkt['id']} | {produkt['marka']} {produkt['model']} ({produkt['rodzaj']}) - {produkt['ilosc_strun']} strun, {produkt['rodzaj_przetwornikow']}, Cena: {produkt['cena']} zł, Ilość: {produkt['ilosc']} szt.")
                elif produkt["kategoria"] == "perkusja":
                    print(f" ID: {produkt['id']} | {produkt['marka']} {produkt['model']} - {produkt['ilosc_bebnow']} bębnów, {produkt['rodzaj_naciagow']}, Cena: {produkt['cena']} zł, Ilość: {produkt['ilosc']} szt.")
        else:
            print("⚠Brak produktów w bazie.")

    except Exception as e:
        print(f" Błąd podczas pobierania danych: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    wyswietl_produkty()
