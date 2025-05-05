from Models.koszyk import Koszyk

def wyswietl_koszyk():
    """Wyświetla koszyk klienta"""
    klient_id = int(input("Podaj ID klienta: "))
    Koszyk.wyswietl_koszyk(klient_id)

if __name__ == "__main__":
    wyswietl_koszyk()
