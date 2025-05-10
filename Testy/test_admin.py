import os
import sys
import pytest

# Umożliwia importowanie modułów z głównego katalogu projektu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from database import get_db_connection, initialize_database
import Models.konta as konta_mod
from Models.produkty import Produkt
from Skrypty.raport_sprzedazy import raport_sprzedazy
from Skrypty.wyswietl_produkty import wyswietl_produkty


def test_panel_admina(monkeypatch, capsys):
    initialize_database()

    # Logowanie jako admin
    konto_id = konta_mod.Konto.zaloguj("admin", "admin")
    assert konto_id is not None
    print("Zalogowano jako admin.")

    # Dodanie dwóch produktów
    produkt1 = Produkt("gitara", "Fender", "Stratocaster", "Fender", 2500, 5, "elektryczna", 6, "single-coil", None, None)
    produkt2 = Produkt("perkusja", "Pearl", "Roadshow", "Pearl", 3000, 3, None, None, None, 5, "powlekane")

    produkt1.dodaj_do_bazy()
    produkt2.dodaj_do_bazy()

    # Pobierz ID produktu do modyfikacji i usunięcia
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM produkty WHERE marka = 'Fender'")
    produkt1_id = cursor.fetchone()["id"]

    # Monkeypatch do modyfikacji produktu
    input_map = {
        f"Nowa marka [Fender]: ": "Fender",
        f"Nowy model [Stratocaster]: ": "Telecaster",
        f"Nowy producent [Fender]: ": "Fender",
        f"Nowa cena [2500 zł]: ": "2600",
        f"Nowa ilość [5 szt.]: ": "10"
    }
    monkeypatch.setattr("builtins.input", lambda prompt: input_map.get(prompt, ""))

    Produkt.modyfikuj_produkt(produkt1_id)

    # Wyświetlenie produktów
    wyswietl_produkty()
    output = capsys.readouterr().out
    assert "Fender" in output
    assert "Pearl" in output

    # Usunięcie produktu
    Produkt.usun_produkt(produkt1_id)

    # Generowanie raportu sprzedaży
    monkeypatch.setattr("builtins.input", lambda _: "")
    raport_sprzedazy()
    output = capsys.readouterr().out
    assert "RAPORT SPRZEDAŻY" in output

    # Bezpośrednia zmiana hasła admina w bazie danych
    nowe_haslo = "nowehaslo"
    cursor.execute("UPDATE konta SET haslo = ? WHERE login = ?", (nowe_haslo, "admin"))
    conn.commit()

    # Ponowne logowanie z nowym hasłem
    konto_id2 = konta_mod.Konto.zaloguj("admin", "nowehaslo")
    assert konto_id2 == konto_id
    print("Hasło admina zmienione pomyślnie.")

    # Przywracanie domyślnego hasła (żeby test był powtarzalny)
    cursor.execute("UPDATE konta SET haslo = ? WHERE login = ?", ("admin", "admin"))
    conn.commit()
    conn.close()

    print("Hasło przywrócone. Test zakończony sukcesem.")
