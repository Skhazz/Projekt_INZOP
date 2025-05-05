from Models.produkty import Produkt

def dodaj_produkt():
    """Dodaje produkt do bazy danych"""
    kategoria = input("Podaj kategorię (gitara/perkusja): ").strip().lower()
    if kategoria not in ["gitara", "perkusja"]:
        print("Nieprawidłowa kategoria!")
        return

    marka = input("Podaj markę: ")
    model = input("Podaj model: ")
    producent = input("Podaj producenta: ")
    cena = float(input("Podaj cenę: "))
    ilosc = int(input("Podaj ilość na stanie: "))

    if kategoria == "gitara":
        rodzaj = input("Podaj rodzaj gitary (elektryczna/akustyczna/basowa): ").strip().lower()
        if rodzaj not in ["elektryczna", "akustyczna", "basowa"]:
            print("Nieprawidłowy rodzaj gitary!")
            return
        ilosc_strun = int(input("Podaj ilość strun (4-12): "))
        rodzaj_przetwornikow = input("Podaj rodzaj przetworników (single-coil/humbucker/P90): ").strip().lower()
        produkt = Produkt(kategoria, marka, model, producent, cena, ilosc, rodzaj, ilosc_strun, rodzaj_przetwornikow)
    else:
        ilosc_bebnow = int(input("Podaj ilość bębnów: "))
        rodzaj_naciagow = input("Podaj rodzaj naciągów (powlekane/niewpowlekane): ").strip().lower()
        produkt = Produkt(kategoria, marka, model, producent, cena, ilosc, None, None, None, ilosc_bebnow, rodzaj_naciagow)

    produkt.dodaj_do_bazy()

if __name__ == "__main__":
    dodaj_produkt()
