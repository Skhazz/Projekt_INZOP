from Models.koszyk import Koszyk

def dodaj_do_koszyka(konto_id):
    """Dodaje produkt do koszyka klienta (po zalogowaniu)"""
    try:
        produkt_id = input("Podaj ID produktu: ").strip()
        if not produkt_id.isdigit():
            raise ValueError(" ID produktu musi być liczbą całkowitą!")

        ilosc = input("Podaj ilość: ").strip()
        if not ilosc.isdigit():
            raise ValueError(" Ilość musi być liczbą całkowitą!")

        produkt_id = int(produkt_id)
        ilosc = int(ilosc)

        Koszyk.dodaj_do_koszyka(konto_id, produkt_id, ilosc)

    except ValueError as e:
        print(f" Błąd: {e}")
    except Exception as e:
        print(f" Nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    print("Ten skrypt powinien być wywoływany z parametrem konto_id z panelu klienta.")
