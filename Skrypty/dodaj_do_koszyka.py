from Models.koszyk import Koszyk

def dodaj_do_koszyka():
    """Dodaje produkt do koszyka klienta"""
    try:
        klient_id = input("Podaj ID klienta: ").strip()
        if not klient_id.isdigit():
            raise ValueError(" ID klienta musi być liczbą całkowitą!")

        produkt_id = input("Podaj ID produktu: ").strip()
        if not produkt_id.isdigit():
            raise ValueError(" ID produktu musi być liczbą całkowitą!")

        ilosc = input("Podaj ilość: ").strip()
        if not ilosc.isdigit():
            raise ValueError(" Ilość musi być liczbą całkowitą!")

        # Konwersja na int po walidacji
        klient_id = int(klient_id)
        produkt_id = int(produkt_id)
        ilosc = int(ilosc)
        Koszyk.dodaj_do_koszyka(klient_id, produkt_id, ilosc)

    except ValueError as e:
        print(f" Błąd: {e}")
    except Exception as e:
        print(f" Nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    dodaj_do_koszyka()
