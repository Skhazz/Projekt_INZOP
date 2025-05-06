import sqlite3

DATABASE_NAME = "sklep_muzyczny.db"

def get_db_connection():
    """Nawiązanie połączenia z bazą danych"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Umożliwia odwoływanie się do kolumn po nazwach
    return conn

def initialize_database():
    """Tworzenie tabel, jeśli baza nie istnieje"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS klienci (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        konto_id INTEGER NOT NULL,
        imie TEXT NOT NULL,
        nazwisko TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        adres TEXT NOT NULL,
        FOREIGN KEY(konto_id) REFERENCES konta(id)
    );

    CREATE TABLE IF NOT EXISTS konta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE NOT NULL,
        haslo TEXT NOT NULL,
        email TEXT NOT NULL,
        adres_dostawy TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS produkty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kategoria TEXT NOT NULL CHECK(kategoria IN ('gitara', 'perkusja')),
        marka TEXT NOT NULL,
        model TEXT NOT NULL,
        producent TEXT NOT NULL,
        cena REAL NOT NULL CHECK(cena >= 0),
        ilosc INTEGER NOT NULL CHECK(ilosc >= 0),
        rodzaj TEXT CHECK(rodzaj IN ('elektryczna', 'akustyczna', 'basowa')),
        ilosc_strun INTEGER CHECK(ilosc_strun BETWEEN 4 AND 12),
        rodzaj_przetwornikow TEXT CHECK(rodzaj_przetwornikow IN ('single-coil', 'humbucker', 'P90')),
        ilosc_bebnow INTEGER CHECK(ilosc_bebnow >= 1),
        rodzaj_naciagow TEXT CHECK(rodzaj_naciagow IN ('powlekane', 'niewpowlekane'))
    );

    CREATE TABLE IF NOT EXISTS zamowienia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        klient_id INTEGER,
        data_zamowienia TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        suma REAL NOT NULL,
        dostawa TEXT NOT NULL CHECK(dostawa IN ('kurier', 'odbiór osobisty')),
        FOREIGN KEY(klient_id) REFERENCES klienci(id)
    );

    CREATE TABLE IF NOT EXISTS zamowione_produkty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zamowienie_id INTEGER NOT NULL,
        produkt_id INTEGER NOT NULL,
        ilosc INTEGER NOT NULL,
        cena REAL NOT NULL,
        FOREIGN KEY(zamowienie_id) REFERENCES zamowienia(id),
        FOREIGN KEY(produkt_id) REFERENCES produkty(id)
    );

    CREATE TABLE IF NOT EXISTS pozycje_zamowienia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zamowienie_id INTEGER,
        produkt_id INTEGER,
        ilosc INTEGER NOT NULL,
        FOREIGN KEY(zamowienie_id) REFERENCES zamowienia(id),
        FOREIGN KEY(produkt_id) REFERENCES produkty(id)
    );

    CREATE TABLE IF NOT EXISTS faktury (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zamowienie_id INTEGER NOT NULL,
        klient_id INTEGER,
        data_faktury TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        suma_netto REAL NOT NULL,
        vat REAL NOT NULL,
        suma_brutto REAL NOT NULL,
        FOREIGN KEY(zamowienie_id) REFERENCES zamowienia(id),
        FOREIGN KEY(klient_id) REFERENCES klienci(id)
    );

    CREATE TABLE IF NOT EXISTS koszyk (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        klient_id INTEGER NOT NULL,
        produkt_id INTEGER NOT NULL,
        ilosc INTEGER NOT NULL CHECK(ilosc >= 1),
        cena REAL NOT NULL,
        FOREIGN KEY(klient_id) REFERENCES klienci(id),
        FOREIGN KEY(produkt_id) REFERENCES produkty(id)
    );
    ''')


    cursor.execute("SELECT id FROM konta WHERE login = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute('''
            INSERT INTO konta (login, haslo, email, adres_dostawy)
            VALUES ('admin', 'admin', 'admin@example.com', 'Panel administratora')
        ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
