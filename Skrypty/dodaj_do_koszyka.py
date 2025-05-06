from Models.koszyk import Koszyk
from database import get_db_connection

def dodaj_do_koszyka(konto_id):
    """Dodaje produkt do koszyka na podstawie ID konta (przetwarza klient_id)"""
    try:
        produkt_id = input("Podaj ID produktu: ").strip()
        if not produkt_id.isdigit():
            raise ValueError(" ID produktu musi być liczbą całkowitą!")

        ilosc = input("Podaj ilość: ").strip()
        if not ilosc.isdigit():
            raise ValueError(" Ilość musi być liczbą całkowitą!")

        produkt_id = int(produkt_id)
        ilosc = int(ilosc)

        # Pobierz klient_id z konto_id
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM klienci WHERE konto_id = ?", (konto_id,))
        wynik = cursor.fetchone()
        conn.close()

        if wynik is None:
            print(" Nie znaleziono klienta powiązanego z tym kontem.")
            return

        klient_id = wynik["id"]
        Koszyk.dodaj_do_koszyka(klient_id, produkt_id, ilosc)

    except ValueError as e:
        print(f" Błąd: {e}")
    except Exception as e:
        print(f" Nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    print("Ten skrypt powinien być wywoływany z parametrem konto_id z panelu klienta.")
