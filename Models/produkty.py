import sqlite3
from database import get_db_connection

class Produkt:
    def __init__(self, kategoria, marka, model, producent, cena, ilosc, rodzaj=None, ilosc_strun=None, rodzaj_przetwornikow=None, ilosc_bebnow=None, rodzaj_naciagow=None):
        self.kategoria = kategoria
        self.marka = marka
        self.model = model
        self.producent = producent
        self.cena = cena
        self.ilosc = ilosc
        self.rodzaj = rodzaj
        self.ilosc_strun = ilosc_strun
        self.rodzaj_przetwornikow = rodzaj_przetwornikow
        self.ilosc_bebnow = ilosc_bebnow
        self.rodzaj_naciagow = rodzaj_naciagow

    def dodaj_do_bazy(self):
        """Dodaje produkt do bazy danych"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO produkty (kategoria, marka, model, producent, cena, ilosc, rodzaj, ilosc_strun, rodzaj_przetwornikow, ilosc_bebnow, rodzaj_naciagow)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (self.kategoria, self.marka, self.model, self.producent, self.cena, self.ilosc, self.rodzaj, self.ilosc_strun, self.rodzaj_przetwornikow, self.ilosc_bebnow, self.rodzaj_naciagow))

        conn.commit()
        conn.close()
        print(f" Produkt {self.marka} {self.model} ({self.kategoria}) został dodany do bazy.")
    @staticmethod
    def usun_produkt(produkt_id):
        """Usuwa produkt z bazy danych, jeśli nie znajduje się w żadnym koszyku"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Sprawdzenie, czy produkt istnieje w bazie
        cursor.execute("SELECT * FROM produkty WHERE id = ?", (produkt_id,))
        produkt = cursor.fetchone()

        if produkt is None:
            print(f" Produkt o ID {produkt_id} nie istnieje w bazie.")
            conn.close()
            return

        # Sprawdzamy, czy produkt znajduje się w koszyku któregokolwiek klienta
        cursor.execute("SELECT * FROM koszyk WHERE produkt_id = ?", (produkt_id,))
        koszyk_pozycje = cursor.fetchall()

        if koszyk_pozycje:
            print(f"️ Nie można usunąć produktu ID {produkt_id}, ponieważ znajduje się w koszykach klientów.")
            conn.close()
            return

        # Usunięcie produktu
        cursor.execute("DELETE FROM produkty WHERE id = ?", (produkt_id,))
        conn.commit()
        conn.close()
        print(f" Produkt ID {produkt_id} został usunięty z bazy.")

    @staticmethod
    def modyfikuj_produkt(produkt_id):
        """Modyfikuje istniejący produkt w bazie danych"""
        conn = get_db_connection()
        cursor = conn.cursor()

        # Pobranie danych produktu do edycji
        cursor.execute("SELECT * FROM produkty WHERE id = ?", (produkt_id,))
        produkt = cursor.fetchone()

        if produkt is None:
            print(f" Produkt o ID {produkt_id} nie istnieje w bazie.")
            conn.close()
            return

        print(f"\n Edycja produktu ID {produkt_id}: {produkt['marka']} {produkt['model']}")

        # Pobieramy nowe wartości (jeśli użytkownik naciska Enter, zostaje stara wartość)
        nowa_marka = input(f"Nowa marka [{produkt['marka']}]: ").strip() or produkt['marka']
        nowy_model = input(f"Nowy model [{produkt['model']}]: ").strip() or produkt['model']
        nowy_producent = input(f"Nowy producent [{produkt['producent']}]: ").strip() or produkt['producent']

        while True:
            nowa_cena = input(f"Nowa cena [{produkt['cena']} zł]: ").strip()
            if not nowa_cena:
                nowa_cena = produkt['cena']
                break
            if nowa_cena.replace(".", "", 1).isdigit():
                nowa_cena = float(nowa_cena)
                break
            print(" Cena musi być liczbą!")

        while True:
            nowa_ilosc = input(f"Nowa ilość [{produkt['ilosc']} szt.]: ").strip()
            if not nowa_ilosc:
                nowa_ilosc = produkt['ilosc']
                break
            if nowa_ilosc.isdigit():
                nowa_ilosc = int(nowa_ilosc)
                break
            print(" Ilość musi być liczbą!")

        # Jeśli produkt to gitara
        if produkt["kategoria"] == "gitara":
            nowy_rodzaj = input(f"Nowy rodzaj ({produkt['rodzaj']}) [elektryczna/akustyczna/basowa]: ").strip() or \
                          produkt['rodzaj']
            nowa_ilosc_strun = input(f"Nowa ilość strun [{produkt['ilosc_strun']}]: ").strip() or produkt['ilosc_strun']
            nowy_przetwornik = input(
                f"Nowy rodzaj przetworników [{produkt['rodzaj_przetwornikow']}] [single-coil/humbucker/P90]: ").strip() or \
                               produkt['rodzaj_przetwornikow']

            # Aktualizacja w bazie
            cursor.execute('''
                   UPDATE produkty SET marka=?, model=?, producent=?, cena=?, ilosc=?, rodzaj=?, ilosc_strun=?, rodzaj_przetwornikow=?
                   WHERE id=?
               ''', (nowa_marka, nowy_model, nowy_producent, nowa_cena, nowa_ilosc, nowy_rodzaj, nowa_ilosc_strun,
                     nowy_przetwornik, produkt_id))

        # Jeśli produkt to perkusja
        elif produkt["kategoria"] == "perkusja":
            nowa_ilosc_bebnow = input(f"Nowa ilość bębnów [{produkt['ilosc_bebnow']}]: ").strip() or produkt[
                'ilosc_bebnow']
            nowy_naciag = input(
                f"Nowy rodzaj naciągów [{produkt['rodzaj_naciagow']}] [powlekane/niewpowlekane]: ").strip() or produkt[
                              'rodzaj_naciagow']

            # Aktualizacja w bazie
            cursor.execute('''
                   UPDATE produkty SET marka=?, model=?, producent=?, cena=?, ilosc=?, ilosc_bebnow=?, rodzaj_naciagow=?
                   WHERE id=?
               ''', (
            nowa_marka, nowy_model, nowy_producent, nowa_cena, nowa_ilosc, nowa_ilosc_bebnow, nowy_naciag, produkt_id))

        conn.commit()
        conn.close()
        print(f" Produkt ID {produkt_id} został zaktualizowany.")
