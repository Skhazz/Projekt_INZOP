from Models.zamowienia import Zamowienia

def wyswietl_zamowienia_klienta():
    """Wyświetla zamówienia danego klienta"""
    klient_id = input("Podaj ID klienta: ").strip()

    if not klient_id.isdigit():
        print(" ID klienta musi być liczbą całkowitą!")
        return

    Zamowienia.wyswietl_zamowienia_klienta(int(klient_id))

if __name__ == "__main__":
    wyswietl_zamowienia_klienta()
