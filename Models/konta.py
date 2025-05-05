import sqlite3
from database import get_db_connection

class Konto:
    def __init__(self, login, haslo, email, adres_dostawy, id=None):
        self.id = id
        self.login = login
        self.haslo = haslo
        self.email = email
        self.adres_dostawy = adres_dostawy

    def utworz_konto(self):
        if len(self.login) < 3:
            raise ValueError("Login musi mieć co najmniej 3 znaki")
        if len(self.haslo) < 3:
            raise ValueError("Hasło musi mieć co najmniej 3 znaki")
        if "@" not in self.email or "." not in self.email:
            raise ValueError("Nieprawidłowy format e-maila")
        if len(self.adres_dostawy.strip()) < 5:
            raise ValueError("Nieprawidłowy adres dostawy")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO konta (login, haslo, email, adres_dostawy)
                VALUES (?, ?, ?, ?)
            ''', (self.login, self.haslo, self.email, self.adres_dostawy))
            conn.commit()
            print(f"Konto '{self.login}' zostało utworzone.")
        except sqlite3.IntegrityError:
            print(f"Login '{self.login}' już istnieje.")
        finally:
            conn.close()

    @staticmethod
    def zaloguj(login, haslo):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM konta WHERE login = ? AND haslo = ?
        ''', (login, haslo))
        konto = cursor.fetchone()
        conn.close()
        if konto:
            print(f"Zalogowano jako {login}.")
            return konto["id"]
        else:
            print("Nieprawidłowy login lub hasło.")
            return None
