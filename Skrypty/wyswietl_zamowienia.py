from Models.zamowienia import Zamowienia

def wyswietl_zamowienia_klienta(konto_id):
    """Wyświetla zamówienia danego klienta po ID konta"""
    Zamowienia.wyswietl_zamowienia_klienta(konto_id)

if __name__ == "__main__":
    print("Ten skrypt powinien być wywoływany z parametrem konto_id z panelu klienta.")
