from Models.klient import Klient

def usun_klienta():
    """Usuwa klienta na podstawie ID z obsługą błędów"""
    try:
        klient_id = int(input("Podaj ID klienta do usunięcia: "))
        Klient.usun_klienta(klient_id)  # Teraz usuwamy po ID
    except ValueError as e:
        print(f"Błąd: {e}")
    except Exception as e:
        print(f" Nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    usun_klienta()
