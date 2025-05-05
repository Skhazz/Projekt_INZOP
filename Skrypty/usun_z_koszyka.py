from Models.koszyk import Koszyk

def usun_z_koszyka(konto_id):
    """Usuwa produkt z koszyka klienta po ID konta"""
    try:
        produkt_id = int(input("Podaj ID produktu do usunięcia: "))
        Koszyk.usun_z_koszyka(konto_id, produkt_id)
    except ValueError:
        print(" ID produktu musi być liczbą całkowitą!")

if __name__ == "__main__":
    print("Ten skrypt powinien być wywoływany z parametrem konto_id z panelu klienta.")
