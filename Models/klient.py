import sqlite3
from database import get_db_connection

class Klient:
    def __init__(self, imie, nazwisko, email, adres, id=None):
        self.id = id
        self.imie = imie
        self.nazwisko = nazwisko
        self.email = email
        self.adres = adres

    @staticmethod
    def is_valid_email(email):
        """Sprawdza, czy e-mail zawiera '@' oraz '.' """
        return "@" in email and "." in email

    @staticmethod
    def is_valid_name(name):
        """Sprawdza, czy imię i nazwisko składają się tylko z liter"""
        return name.isalpha() and len(name) > 1

    def dodaj_do_bazy(self):
        """Dodaje klienta do bazy danych"""
        if not Klient.is_valid_email(self.email):
            raise ValueError(f"Nieprawidłowy format e-maila: {self.email}")
        if not Klient.is_valid_name(self.imie):
            raise ValueError(f"Nieprawidłowe imię: {self.imie}")
        if not Klient.is_valid_name(self.nazwisko):
            raise ValueError(f"Nieprawidłowe nazwisko: {self.nazwisko}")
        if len(self.adres.strip()) < 5:
            raise ValueError(f"Nieprawidłowy adres zamieszkania: {self.adres}")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO klienci (imie, nazwisko, email, adres) VALUES (?, ?, ?, ?)",
                           (self.imie, self.nazwisko, self.email, self.adres))
            conn.commit()
            print(f"Klient {self.imie} {self.nazwisko} został dodany do bazy.")
        except sqlite3.IntegrityError:
            print(f"Błąd: Klient z e-mailem {self.email} już istnieje w bazie.")
        except sqlite3.Error as e:
            print(f"Błąd bazy danych: {e}")
        finally:
            conn.close()

    @staticmethod
    def usun_klienta(klient_id):
        """Usuwa klienta z bazy danych na podstawie ID"""
        if not isinstance(klient_id, int) or klient_id <= 0:
            raise ValueError(f"Nieprawidłowe ID klienta: {klient_id}")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Sprawdzamy, czy klient istnieje
            cursor.execute("SELECT * FROM klienci WHERE id=?", (klient_id,))
            klient = cursor.fetchone()

            if klient is None:
                print(f"Błąd: Klient o ID {klient_id} nie istnieje w bazie.")
                return

            # Usuwamy klienta
            cursor.execute("DELETE FROM klienci WHERE id=?", (klient_id,))
            conn.commit()
            print(f"Klient o ID {klient_id} został usunięty z bazy.")
        except sqlite3.Error as e:
            print(f"Błąd bazy danych: {e}")
        finally:
            conn.close()