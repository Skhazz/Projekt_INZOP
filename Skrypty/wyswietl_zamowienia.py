from Models.zamowienia import Zamowienia
from database import get_db_connection

def wyswietl_zamowienia_klienta(konto_id):
    """Wyświetla zamówienia klienta po przekształceniu konto_id na klient_id"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM klienci WHERE konto_id = ?", (konto_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            print("Nie znaleziono klienta powiązanego z tym kontem.")
            return

        klient_id = row["id"]
        Zamowienia.wyswietl_zamowienia_klienta(klient_id)

    except Exception as e:
        print(f"Błąd: {e}")

if __name__ == "__main__":
    print("Ten skrypt powinien być wywoływany z parametrem konto_id z panelu klienta.")
