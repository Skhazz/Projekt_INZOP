from Models.zamowienia import Zamowienia

def raport_sprzedazy():
    """Generuje raport sprzedaży z opcją wyboru zakresu dat"""
    print("\n Generowanie raportu sprzedaży")
    print("Podaj zakres dat (format: YYYY-MM-DD) lub zostaw puste, aby zobaczyć całość")

    data_od = input("Od (YYYY-MM-DD): ").strip()
    data_do = input("Do (YYYY-MM-DD): ").strip()


    if data_od and len(data_od) != 10:
        print(" Niepoprawny format daty! Powinien być YYYY-MM-DD")
        return
    if data_do and len(data_do) != 10:
        print(" Niepoprawny format daty! Powinien być YYYY-MM-DD")
        return

    Zamowienia.generuj_raport_sprzedazy(data_od or None, data_do or None)

if __name__ == "__main__":
    raport_sprzedazy()
