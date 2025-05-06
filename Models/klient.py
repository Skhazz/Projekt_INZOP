from database import get_db_connection
import re

class Klient:
    def __init__(self, imie, nazwisko, email, adres):
        self.imie = imie
        self.nazwisko = nazwisko
        self.email = email
        self.adres = adres

    def dodaj_do_bazy(self):
        if not Klient.is_valid_email(self.email):
            raise ValueError(f"Nieprawidłowy format e-maila: {self.email}")
        if not Klient.is_valid_name(self.imie):
            raise ValueError(f"Nieprawidłowe imię: {self.imie}")
        if not Klient.is_valid_name(self.nazwisko):
            raise ValueError(f"Nieprawidłowe nazwisko: {self.nazwisko}")
        if len(self.adres.strip()) < 5:
            raise ValueError(f"Nieprawidłowy adres zamieszkania: {self.adres}")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO klienci (imie, nazwisko, email, adres, konto_id) VALUES (?, ?, ?, ?, NULL)",
            (self.imie, self.nazwisko, self.email, self.adres)
        )
        conn.commit()
        conn.close()
        print(f"Klient {self.imie} {self.nazwisko} został dodany do bazy.")

    @staticmethod
    def dodaj_z_konto_id(konto_id, imie, nazwisko, email, adres):
        if not Klient.is_valid_email(email):
            raise ValueError(f"Nieprawidłowy format e-maila: {email}")
        if not Klient.is_valid_name(imie):
            raise ValueError(f"Nieprawidłowe imię: {imie}")
        if not Klient.is_valid_name(nazwisko):
            raise ValueError(f"Nieprawidłowe nazwisko: {nazwisko}")
        if len(adres.strip()) < 5:
            raise ValueError(f"Nieprawidłowy adres zamieszkania: {adres}")

        conn = get_db_connection()
        cursor = conn.cursor()

        # WALIDACJA: czy email już istnieje?
        cursor.execute("SELECT id FROM klienci WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            raise ValueError("Klient z tym adresem e-mail już istnieje.")

        cursor.execute(
            "INSERT INTO klienci (konto_id, imie, nazwisko, email, adres) VALUES (?, ?, ?, ?, ?)",
            (konto_id, imie, nazwisko, email, adres)
        )
        conn.commit()
        conn.close()
        print(f"Klient {imie} {nazwisko} został dodany do bazy z kontem ID {konto_id}.")

    @staticmethod
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    @staticmethod
    def is_valid_name(name):
        return len(name.strip()) >= 2 and name.isalpha()
