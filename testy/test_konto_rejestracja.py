import pytest
import sqlite3
from database import initialize_database, get_db_connection
from Models.konta import Konto

@pytest.fixture(scope="function")
def clear_test_login():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM konta WHERE login = 'nowy_test'")
    conn.commit()
    conn.close()


def test_rejestracja_poprawna(clear_test_login):
    konto = Konto('nowy_test', 'haslo123', 'nowy@example.com', 'ul. Testowa 1')
    konto.utworz_konto()

    # Sprawdź, czy konto zostało dodane
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM konta WHERE login = ?", ('nowy_test',))
    wynik = cursor.fetchone()
    conn.close()

    assert wynik is not None, "Konto nie zostało dodane do bazy danych."
    assert wynik['email'] == 'nowy@example.com', "Adres email nie został poprawnie zapisany."

def test_rejestracja_duplikat(clear_test_login):
    konto1 = Konto('nowy_test', 'haslo123', 'nowy@example.com', 'ul. Testowa 1')
    konto1.utworz_konto()
    konto2 = Konto('nowy_test', 'innehaslo', 'inny@example.com', 'ul. Inna 2')
    konto2.utworz_konto()  # powinien wypisać komunikat, ale nie rzuca wyjątku

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as liczba FROM konta WHERE login = ?", ('nowy_test',))
    liczba = cursor.fetchone()['liczba']
    conn.close()

    assert liczba == 1, "Duplikat loginu został dodany, a nie powinien."
