from Models.zamowienia import Zamowienia
from database import get_db_connection

def anuluj_zamowienie(konto_id):
    """Anuluje zamówienie należące do zalogowanego klienta"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM klienci WHERE konto_id = ?", (konto_id,))
        row = cursor.fetchone()

        if not row:
            print("Nie znaleziono klienta powiązanego z tym kontem.")
            return

        klient_id = row["id"]
        zamowienie_id = input("Podaj ID zamówienia do anulowania: ").strip()

        if not zamowienie_id.isdigit():
            print("ID zamówienia musi być liczbą całkowitą!")
            return

        zamowienie_id = int(zamowienie_id)

        # Sprawdź, czy zamówienie należy do klienta
        cursor.execute("SELECT id FROM zamowienia WHERE id = ? AND klient_id = ?", (zamowienie_id, klient_id))
        if cursor.fetchone():
            Zamowienia.anuluj_zamowienie(zamowienie_id)
        else:
            print("To zamówienie nie należy do Ciebie lub nie istnieje.")

        conn.close()

    except Exception as e:
        print(f"Błąd: {e}")

if __name__ == "__main__":
    print("Ten skrypt powinien być wywoływany z parametrem konto_id z panelu klienta.")
