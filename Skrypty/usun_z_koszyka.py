from Models.koszyk import Koszyk

def usun_z_koszyka():
    """Usuwa produkt z koszyka klienta"""
    klient_id = int(input("Podaj ID klienta: "))
    produkt_id = int(input("Podaj ID produktu do usunięcia: "))

    Koszyk.usun_z_koszyka(klient_id, produkt_id)

if __name__ == "__main__":
    usun_z_koszyka()