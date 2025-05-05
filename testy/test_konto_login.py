import pytest
import sqlite3
from database import initialize_database, get_db_connection
from Models.konta import Konto

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    initialize_database()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Wyczyść i dodaj konto testowe
    cursor.execute("DELETE FROM konta WHERE login = 'test_user'")
    cursor.execute('''
        INSERT INTO konta (login, haslo, email, adres_dostawy)
        VALUES (?, ?, ?, ?)''',
        ('test_user', 'test_pass', 'test@example.com', 'Testowa 123'))
    conn.commit()
    conn.close()


def test_poprawne_logowanie():
    konto_id = Konto.zaloguj('test_user', 'test_pass')
    assert konto_id is not None, "Logowanie nie powiodło się mimo poprawnych danych."

def test_nieprawidlowe_haslo():
    konto_id = Konto.zaloguj('test_user', 'zle_haslo')
    assert konto_id is None, "Logowanie powinno się nie udać z błędnym hasłem."

def test_nieprawidlowy_login():
    konto_id = Konto.zaloguj('nie_istnieje', 'test_pass')
    assert konto_id is None, "Logowanie powinno się nie udać z błędnym loginem."
