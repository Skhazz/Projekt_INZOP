from Models.produkty import Produkt

def modyfikuj_produkt():
    """Modyfikuje produkt w bazie po ID"""
    produkt_id = input("Podaj ID produktu do edycji: ").strip()

    if not produkt_id.isdigit():
        print(" ID produktu musi być liczbą całkowitą!")
        return

    Produkt.modyfikuj_produkt(int(produkt_id))

if __name__ == "__main__":
    modyfikuj_produkt()
