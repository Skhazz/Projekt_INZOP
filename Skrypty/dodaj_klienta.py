from Models.klient import Klient

def dodaj_klienta():
    """Dodaje klienta z obsługą błędów"""
    imie = input("Podaj imię: ")
    nazwisko = input("Podaj nazwisko: ")
    email = input("Podaj email: ")
    adres = input("Podaj adres zamieszkania: ")

    try:
        klient = Klient(imie, nazwisko, email, adres)
        klient.dodaj_do_bazy()
    except ValueError as e:
        print(f"Błąd: {e}")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    dodaj_klienta()
