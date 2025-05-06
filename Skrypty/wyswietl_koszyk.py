from Models.koszyk import Koszyk
from database import get_db_connection

def wyswietl_koszyk(konto_id):
    """Wyświetla koszyk klienta po ID konta (zalogowanego)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM klienci WHERE konto_id = ?", (konto_id,))
        wynik = cursor.fetchone()
        conn.close()

        if wynik is None:
            print("Nie znaleziono klienta powiązanego z tym kontem.")
            return

        klient_id = wynik["id"]
        Koszyk.wyswietl_koszyk(klient_id)

    except Exception as e:
        print(f" Błąd podczas wyświetlania koszyka: {e}")
