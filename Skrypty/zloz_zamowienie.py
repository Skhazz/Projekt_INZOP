from Models.zamowienia import Zamowienia

def zloz_zamowienie(konto_id):
    """Tworzy zamówienie na podstawie koszyka klienta po ID konta"""
    Zamowienia.zloz_zamowienie(konto_id)

if __name__ == "__main__":
    print("Ten skrypt powinien być wywoływany z parametrem konto_id z panelu klienta.")
