from Models.produkty import Produkt

def dodaj_produkt():
    print("\nDodawanie nowego produktu:")
    kategoria = input("Podaj kategorię (gitara/perkusja): ").strip()

    if kategoria not in ["gitara", "perkusja"]:
        print("Niepoprawna kategoria.")
        return

    marka = input("Podaj markę: ").strip()
    model = input("Podaj model: ").strip()
    producent = input("Podaj producenta: ").strip()
    cena = float(input("Podaj cenę: "))
    ilosc = int(input("Podaj ilość na stanie: "))

    produkt = None

    if kategoria == "gitara":
        rodzaj = input("Podaj rodzaj gitary (elektryczna/akustyczna/basowa): ").strip()
        ilosc_strun = int(input("Podaj ilość strun (4-12): "))
        rodzaj_przetwornikow = input("Podaj rodzaj przetworników (single-coil/humbucker/P90): ").strip()

        produkt = Produkt(
            kategoria=kategoria,
            marka=marka,
            model=model,
            producent=producent,
            cena=cena,
            ilosc=ilosc,
            rodzaj=rodzaj,
            ilosc_strun=ilosc_strun,
            rodzaj_przetwornikow=rodzaj_przetwornikow,
            ilosc_bebnow=None,
            rodzaj_naciagow=None
        )

    elif kategoria == "perkusja":
        ilosc_bebnow = int(input("Podaj ilość bębnów: "))
        rodzaj_naciagow = input("Podaj rodzaj naciągów (powlekane/niewpowlekane): ").strip()

        produkt = Produkt(
            kategoria=kategoria,
            marka=marka,
            model=model,
            producent=producent,
            cena=cena,
            ilosc=ilosc,
            rodzaj=None,
            ilosc_strun=None,
            rodzaj_przetwornikow=None,
            ilosc_bebnow=ilosc_bebnow,
            rodzaj_naciagow=rodzaj_naciagow
        )

    if produkt:
        produkt.dodaj_do_bazy()
