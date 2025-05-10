import os
import sys
import pytest

# Umożliwia importowanie modułów z głównego katalogu projektu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from Models.konta import Konto
from Models.koszyk import Koszyk
from Models.zamowienia import Zamowienia
from database import get_db_connection, initialize_database

def test_proces_konta(monkeypatch):
    initialize_database()

    login = "testuser"
    haslo = "1234"
    email = "test@example.com"
    adres = "Testowa 123"

    # Rejestracja konta
    konto = Konto(login, haslo, email, adres)
    konto.utworz_konto()

    # Logowanie
    konto_id = Konto.zaloguj(login, haslo)
    assert konto_id is not None

    # Dodanie klienta bezpośrednio do bazy (z uwzględnieniem konto_id)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO klienci (imie, nazwisko, email, adres, konto_id)
        VALUES (?, ?, ?, ?, ?)
    ''', ("Test", "Uzytkownik", email, adres, konto_id))
    conn.commit()

    # Pobierz ID klienta
    cursor.execute("SELECT id FROM klienci WHERE konto_id = ?", (konto_id,))
    klient_id = cursor.fetchone()["id"]

    # Dodanie produktu testowego
    cursor.execute('''
        INSERT INTO produkty (kategoria, marka, model, producent, cena, ilosc, rodzaj, ilosc_strun, rodzaj_przetwornikow, ilosc_bebnow, rodzaj_naciagow)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ("gitara", "Yamaha", "Pacifica", "Yamaha", 999.99, 10, "elektryczna", 6, "humbucker", None, None))
    produkt_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Dodanie do koszyka
    Koszyk.dodaj_do_koszyka(klient_id, produkt_id, 1)

    # Monkeypatch na wybór dostawy
    monkeypatch.setattr("builtins.input", lambda _: "kurier")

    # Złożenie zamówienia
    Zamowienia.zloz_zamowienie(konto_id)

    # Usunięcie konta (i tym samym klienta)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM klienci WHERE id = ?", (klient_id,))
    cursor.execute("DELETE FROM konta WHERE id = ?", (konto_id,))
    conn.commit()
    conn.close()

    # Sprawdzenie, że konto już nie istnieje
    assert Konto.zaloguj(login, haslo) is None