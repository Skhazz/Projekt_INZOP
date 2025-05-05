import sys  #Patryk Sliwowski, Filip Sołowiej, Jacek Wargol
from database import initialize_database
from Skrypty.dodaj_klienta import dodaj_klienta
from Skrypty.wyswietl_baze import wyswietl_baze
from Skrypty.usun_klienta import usun_klienta
from Skrypty.nuke_database import nuke_database
from Skrypty.dodaj_produkt import dodaj_produkt
from Skrypty.dodaj_do_koszyka import dodaj_do_koszyka
from Skrypty.wyswietl_koszyk import wyswietl_koszyk
from Skrypty.wyswietl_produkty import wyswietl_produkty
from Skrypty.usun_z_koszyka import usun_z_koszyka
from Skrypty.usun_produkt import usun_produkt
from Skrypty.modyfikuj_produkt import modyfikuj_produkt
from Skrypty.zloz_zamowienie import zloz_zamowienie
from Skrypty.anuluj_zamowienie import anuluj_zamowienie
from Skrypty.wyswietl_zamowienia import wyswietl_zamowienia_klienta
from Skrypty.raport_sprzedazy import raport_sprzedazy


initialize_database()


def panel_administratora():
    """Menu dla administratora"""
    opcje_admin = {
        "1": ("Raport Sprzedaży", raport_sprzedazy),
        "2": ("Dodaj klienta", dodaj_klienta),
        "3": ("Usuń klienta", usun_klienta),
        "4": ("Dodaj produkt", dodaj_produkt),
        "5": ("Usuń produkt", usun_produkt),
        "6": ("Modyfikuj Produkt", modyfikuj_produkt),
        "7": ("Wyświetl bazę danych", wyswietl_baze),
        "8": ("Wyświetl produkty", wyswietl_produkty),
        "9": ("Usuń bazę danych (nuke)", nuke_database),
        "10": ("Powrót do głównego menu", None)
    }

    while True:
        print("\n PANEL ADMINISTRATORA:")
        for numer, (opis, _) in opcje_admin.items():
            print(f"{numer}. {opis}")

        wybor = input("Wybierz opcję: ").strip()

        if wybor in opcje_admin:
            opis, funkcja = opcje_admin[wybor]

            if funkcja is None:  # Jeśli użytkownik wybrał powrót
                print(" Powrót do głównego menu.")
                return  # Zamiast `break`, używamy `return`, żeby wrócić do głównego menu

            print(f"\n Wybrano: {opis} (wpisz 'anuluj', aby wrócić do menu)\n")

            potwierdzenie = input("Naciśnij Enter, aby kontynuować lub wpisz 'anuluj': ").strip().lower()
            if potwierdzenie == "anuluj":
                print(" Powrót do menu administratora.")
                continue

            funkcja()  # Uruchamiamy wybraną funkcję
        else:
            print(" Nieprawidłowy wybór, spróbuj ponownie.")

def panel_klienta():
    """Menu dla klienta"""
    opcje_klient = {
        "1": ("Wyświetl produkty", wyswietl_produkty),
        "2": ("Dodaj do koszyka", dodaj_do_koszyka),
        "3": ("Wyświetl koszyk", wyswietl_koszyk),
        "4": ("Usuń z koszyka", usun_z_koszyka),
        "5": ("Złóż zamowienie", zloz_zamowienie),
        "6": ("Wyświetl złożnone zamówienia", wyswietl_zamowienia_klienta),
        "7": ("Anuluj zamówienie", anuluj_zamowienie),
        "8": ("Powrót do głównego menu", None)
    }

    while True:
        print("\n PANEL KLIENTA:")
        for numer, (opis, _) in opcje_klient.items():
            print(f"{numer}. {opis}")

        wybor = input("Wybierz opcję: ").strip()

        if wybor in opcje_klient:
            opis, funkcja = opcje_klient[wybor]

            if funkcja is None:  # Jeśli użytkownik wybrał powrót
                print(" Powrót do głównego menu.")
                return  # Wracamy do głównego menu

            print(f"\n Wybrano: {opis} (wpisz 'anuluj', aby wrócić do menu)\n")

            potwierdzenie = input("Naciśnij Enter, aby kontynuować lub wpisz 'anuluj': ").strip().lower()
            if potwierdzenie == "anuluj":
                print(" Powrót do menu klienta.")
                continue

            funkcja()  # Uruchamiamy wybraną funkcję
        else:
            print(" Nieprawidłowy wybór, spróbuj ponownie.")

def menu_glowne():
    """Główne menu wyboru panelu"""
    opcje_glowne = {
        "1": ("Panel administratora", panel_administratora),
        "2": ("Panel klienta", panel_klienta),
        "3": ("Wyjdź do terminala", exit),
        "4": ("Wyłącz program", lambda: sys.exit("Program zamknięty."))
    }

    while True:
        print("\n GŁÓWNE MENU:")
        for numer, (opis, _) in opcje_glowne.items():
            print(f"{numer}. {opis}")

        wybor = input("Wybierz opcję: ").strip()

        if wybor in opcje_glowne:
            opis, funkcja = opcje_glowne[wybor]
            if funkcja is not None:  # Sprawdzamy, czy funkcja istnieje
                funkcja()
        else:
            print(" Nieprawidłowy wybór, spróbuj ponownie.")


if __name__ == "__main__":
    menu_glowne()
