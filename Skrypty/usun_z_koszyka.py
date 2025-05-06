from Models.koszyk import Koszyk
from database import get_db_connection

def usun_z_koszyka(konto_id):
    """Usuwa produkt z koszyka klienta po ID konta (przekonwertowanego na klienta)"""
    try:
        # Pobierz klient_id na podstawie konto_id
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM klienci WHERE konto_id = ?", (konto_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            print("Nie znaleziono klienta powiązanego z tym kontem.")
            return

        klient_id = row["id"]

        produkt_id = int(input("Podaj ID produktu do usunięcia: "))
        Koszyk.usun_z_koszyka(klient_id, produkt_id)

    except ValueError:
        print("ID produktu musi być liczbą całkowitą!")
    except Exception as e:
        print(f"Błąd: {e}")

if __name__ == "__main__":
    print("Ten skrypt powinien być wywoływany z parametrem konto_id z panelu klienta.")
