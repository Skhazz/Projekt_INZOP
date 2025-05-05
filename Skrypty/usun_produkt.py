from Models.produkty import Produkt


def usun_produkt():
    """Usuwa produkt z bazy po ID"""
    produkt_id = input("Podaj ID produktu do usunięcia: ").strip()

    if not produkt_id.isdigit():
        print(" ID produktu musi być liczbą całkowitą!")
        return

    Produkt.usun_produkt(int(produkt_id))


if __name__ == "__main__":
    usun_produkt()
