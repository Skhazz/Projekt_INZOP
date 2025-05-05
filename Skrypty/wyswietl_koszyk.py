from Models.koszyk import Koszyk

def wyswietl_koszyk(konto_id):
    """Wyświetla koszyk klienta po ID konta (zalogowanego)"""
    Koszyk.wyswietl_koszyk(konto_id)

if __name__ == "__main__":
    print("Ten skrypt powinien być wywoływany z parametrem konto_id z panelu klienta.")
