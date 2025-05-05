import os

DATABASE_NAME = "sklep_muzyczny.db"


def nuke_database():
    """Usuwa plik bazy danych SQLite po potwierdzeniu."""
    potwierdzenie = input("Czy na pewno chcesz usunąć bazę danych? (tak/nie): ").strip().lower()

    if potwierdzenie != "tak":
        print("Operacja anulowana.")
        return

    try:
        if os.path.exists(DATABASE_NAME):
            os.remove(DATABASE_NAME)
            print(f"Baza danych '{DATABASE_NAME}' została usunięta!")
        else:
            print(f"⚠Baza danych '{DATABASE_NAME}' nie istnieje.")
    except Exception as e:
        print(f"Błąd podczas usuwania bazy danych: {e}")


if __name__ == "__main__":
    nuke_database()
