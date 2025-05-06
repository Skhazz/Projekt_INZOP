from Models.konta import Konto
from Models.klient import Klient
from database import get_db_connection

def rejestracja():
    """Tworzy nowe konto klienta i odpowiadający rekord klienta"""
    print("\n*** Rejestracja nowego konta ***")
    login = input("Podaj login: ").strip()
    haslo = input("Podaj hasło: ").strip()
    email = input("Podaj email: ").strip()
    adres_dostawy = input("Podaj adres dostawy: ").strip()

    try:
        konto = Konto(login, haslo, email, adres_dostawy)
        konto.utworz_konto()

        # po rejestracji konta, pobierz jego ID
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM konta WHERE login = ?", (login,))
        konto_row = cursor.fetchone()
        conn.close()

        if konto_row:
            konto_id = konto_row["id"]

            print("\nPodaj dane osobowe do utworzenia konta klienta:")
            imie = input("Imię: ").strip()
            nazwisko = input("Nazwisko: ").strip()

            # użyj e-maila i adresu z konta
            email_os = email
            adres = adres_dostawy

            try:
                Klient.dodaj_z_konto_id(konto_id, imie, nazwisko, email_os, adres)
                print("Konto klienta zostało utworzone.")
            except Exception as e:
                print(f"Błąd przy tworzeniu klienta: {e}")
        else:
            print("Nie udało się pobrać ID nowego konta.")

    except ValueError as e:
        print(f"Błąd: {e}")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    rejestracja()
