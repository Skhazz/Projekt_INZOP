from Skrypty.dodaj_do_koszyka import dodaj_do_koszyka
from Skrypty.usun_z_koszyka import usun_z_koszyka
from Skrypty.wyswietl_koszyk import wyswietl_koszyk
from Skrypty.wyswietl_produkty import wyswietl_produkty
from Skrypty.zloz_zamowienie import zloz_zamowienie
from Skrypty.wyswietl_zamowienia import wyswietl_zamowienia_klienta
from Skrypty.anuluj_zamowienie import anuluj_zamowienie
from Skrypty.rejestracja import rejestracja
from Skrypty.raport_sprzedazy import raport_sprzedazy
from Skrypty.nuke_database import nuke_database
from Skrypty.dodaj_produkt import dodaj_produkt
from Skrypty.modyfikuj_produkt import modyfikuj_produkt
from Skrypty.usun_produkt import usun_produkt
from database import get_db_connection
from database import initialize_database
initialize_database()


def panel_klienta(konto_id):
    while True:
        print("\n--- Panel klienta ---")
        opcje = {
            "1": ("Dodaj produkt do koszyka", lambda: dodaj_do_koszyka(konto_id)),
            "2": ("Usuń produkt z koszyka", lambda: usun_z_koszyka(konto_id)),
            "3": ("Wyświetl koszyk", lambda: wyswietl_koszyk(konto_id)),
            "4": ("Wyświetl dostępne produkty", wyswietl_produkty),
            "5": ("Złóż zamowienie", lambda: zloz_zamowienie(konto_id)),
            "6": ("Wyświetl złożone zamówienia", lambda: wyswietl_zamowienia_klienta(konto_id)),
            "7": ("Anuluj zamówienie", lambda: anuluj_zamowienie(konto_id)),
            "8": ("Wyloguj się", None)
        }

        for klucz, (opis, _) in opcje.items():
            print(f"{klucz}. {opis}")

        wybor = input("\nWybierz opcję: ").strip()

        if wybor == "8":
            print("Wylogowano.")
            break
        elif wybor in opcje:
            _, funkcja = opcje[wybor]
            if funkcja:
                funkcja()
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

def zmien_haslo_admina():
    login = "admin"
    aktualne = input("Podaj obecne hasło: ").strip()
    nowe = input("Podaj nowe hasło: ").strip()
    potwierdz = input("Potwierdź nowe hasło: ").strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT haslo FROM konta WHERE login = ?", (login,))
    row = cursor.fetchone()

    if not row or row["haslo"] != aktualne:
        print("Błędne obecne hasło.")
        conn.close()
        return

    if nowe != potwierdz:
        print("Hasła nie są zgodne.")
        conn.close()
        return

    cursor.execute("UPDATE konta SET haslo = ? WHERE login = ?", (nowe, login))
    conn.commit()
    conn.close()

    print("Hasło administratora zostało zmienione.")

def panel_admina():
    while True:
        print("\n--- Panel administratora ---")
        opcje = {
            "1": ("Wyświetl produkty", wyswietl_produkty),
            "2": ("Dodaj produkt", dodaj_produkt),
            "3": ("Modyfikuj produkt", modyfikuj_produkt),
            "4": ("Usuń produkt", usun_produkt),
            "5": ("Wygeneruj raport sprzedaży", raport_sprzedazy),
            "6": ("Usuń całą bazę (NIEODWRACALNE)", nuke_database),
            "7": ("Powrót do menu głównego", None),
            "8": ("Zmień hasło administratora", zmien_haslo_admina)
        }

        for klucz, (opis, _) in opcje.items():
            print(f"{klucz}. {opis}")

        wybor = input("\nWybierz opcję: ").strip()

        if wybor == "7":
            break
        elif wybor in opcje:
            _, funkcja = opcje[wybor]
            if funkcja:
                funkcja()
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

def logowanie_klienta():
    print("\n--- Logowanie klienta ---")
    login = input("Login: ").strip()
    haslo = input("Hasło: ").strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM konta WHERE login = ? AND haslo = ?", (login, haslo))
    row = cursor.fetchone()
    conn.close()

    if row:
        konto_id = row["id"]
        print(f"Zalogowano pomyślnie jako {login}.")
        panel_klienta(konto_id)
    else:
        print("Błędny login lub hasło.")

def logowanie_admina():
    print("\n--- Logowanie administratora ---")
    login = input("Login: ").strip()
    haslo = input("Hasło: ").strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM konta WHERE login = ? AND haslo = ?", (login, haslo))
    row = cursor.fetchone()
    conn.close()

    if row and login == "admin":
        print("Zalogowano jako administrator.")
        panel_admina()
    else:
        print("Błędne dane administratora. Dostęp zabroniony.")

def menu_glowne():
    while True:
        print("\n--- MENU GŁÓWNE ---")
        opcje = {
            "1": ("Panel administratora", logowanie_admina),
            "2": ("Panel klienta", logowanie_klienta),
            "3": ("Rejestracja nowego konta", rejestracja),
            "4": ("Wyjście", None)
        }

        for klucz, (opis, _) in opcje.items():
            print(f"{klucz}. {opis}")

        wybor = input("\nWybierz opcję: ").strip()

        if wybor == "4":
            print("Zamykam program.")
            break
        elif wybor in opcje:
            _, funkcja = opcje[wybor]
            if funkcja:
                funkcja()
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    menu_glowne()
