from Models.zamowienia import Zamowienia

def anuluj_zamowienie():
    """Anuluje zamówienie po podaniu jego ID"""
    zamowienie_id = input("Podaj ID zamówienia do anulowania: ").strip()

    if not zamowienie_id.isdigit():
        print(" ID zamówienia musi być liczbą całkowitą!")
        return

    Zamowienia.anuluj_zamowienie(int(zamowienie_id))

if __name__ == "__main__":
    print("Ten skrypt można wywołać z menu klienta — użytkownik musi znać ID zamówienia do anulowania.")
