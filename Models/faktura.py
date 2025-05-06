import os
from datetime import datetime

class Faktura:
    @staticmethod
    def generuj_plik(zamowienie_id, klient_id, suma_netto, vat, suma_brutto, sciezka="."):
        """
        Generuje plik .txt z danymi faktury.
        """
        nazwa_pliku = os.path.join(sciezka, f"faktura_{zamowienie_id}.txt")
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(nazwa_pliku, "w", encoding="utf-8") as f:
            f.write("=== FAKTURA ===\n")
            f.write(f"Data wystawienia: {data}\n")
            f.write(f"Numer zamówienia: {zamowienie_id}\n")
            f.write(f"ID klienta: {klient_id}\n")
            f.write(f"Suma netto: {round(suma_netto, 2)} zł\n")
            f.write(f"VAT: {int(vat * 100)}%\n")
            f.write(f"Suma brutto: {round(suma_brutto, 2)} zł\n")

        print(f"Faktura zapisana jako: {nazwa_pliku}")
