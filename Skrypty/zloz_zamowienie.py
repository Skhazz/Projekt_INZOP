from Models.zamowienia import Zamowienia

def zloz_zamowienie():
    """Tworzy zamówienie na podstawie koszyka klienta"""
    klient_id = input("Podaj ID klienta: ").strip()

    if not klient_id.isdigit():
        print(" ID klienta musi być liczbą całkowitą!")
        return

    Zamowienia.zloz_zamowienie(int(klient_id))

if __name__ == "__main__":
    zloz_zamowienie()
