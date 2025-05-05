from Models.konta import Konto

def rejestracja():
    """Tworzy nowe konto klienta"""
    print("\n*** Rejestracja nowego konta ***")
    login = input("Podaj login: ").strip()
    haslo = input("Podaj hasło: ").strip()
    email = input("Podaj email: ").strip()
    adres_dostawy = input("Podaj adres dostawy: ").strip()

    try:
        konto = Konto(login, haslo, email, adres_dostawy)
        konto.utworz_konto()
    except ValueError as e:
        print(f"Błąd: {e}")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    rejestracja()
