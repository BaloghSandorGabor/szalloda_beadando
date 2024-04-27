import os

def clear_terminal():
    # Ellenőrizd az operációs rendszert
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix-alapú rendszerek (Linux, macOS)
        os.system('clear')

clear_terminal()

from datetime import datetime

# Absztrakt Szoba osztály
class Szoba:
    def __init__(self, ar, szobaszam, szoba_tipus):
        self.ar = ar
        self.szobaszam = szobaszam
        self.szoba_tipus = szoba_tipus
        self.foglalt = False
        self.foglalt_kezdo_datum = None
        self.foglalt_vegso_datum = None

    def foglalas_letrehozasa(self, kezdo_datum, vegso_datum):
        # Ellenőrizzük, hogy a dátumok érvényesek-e
        if not self.ellenorzi_datumokat(kezdo_datum, vegso_datum):
            return False

        # Ellenőrizzük, hogy a szoba elérhető-e az adott időszakban
        if self.foglalt and (self.foglalt_kezdo_datum <= vegso_datum and self.foglalt_vegso_datum >= kezdo_datum):
            print(f"Nem lehet lefoglalni a szobát {self.szobaszam}, mert az már foglalt az adott időszakban.")
            return False

        # Ha a foglalás létrejött, állítsuk be a szoba foglalt állapotát
        self.foglalt = True
        self.foglalt_kezdo_datum = kezdo_datum
        self.foglalt_vegso_datum = vegso_datum
        print(f"A {self.szobaszam} szoba sikeresen lefoglalva, {kezdo_datum} és {vegso_datum} között.")
        return True

    def foglalas_lemondasa(self, kezdo_datum, vegso_datum):
        # Ellenőrizzük, hogy a lemondás dátumai megegyeznek-e a foglalás dátumaival
        if (self.foglalt and self.foglalt_kezdo_datum == kezdo_datum and self.foglalt_vegso_datum == vegso_datum):
            self.foglalt = False
            self.foglalt_kezdo_datum = None
            self.foglalt_vegso_datum = None
            print(f"A szoba {self.szobaszam} sikeresen lemondva.")
            return True
        else:
            print(f"Nem lehet lemondani a foglalást, mert a dátumok nem egyeznek a meglévő foglalás dátumaival.")
            return False

    def ellenorzi_datumokat(self, kezdo_datum, vegso_datum):
        try:
            datetime.strptime(kezdo_datum, "%Y-%m-%d")
            datetime.strptime(vegso_datum, "%Y-%m-%d")
            return True
        except ValueError:
            print("A megadott dátumok formátuma helytelen. Kérjük, írja be a dátumokat az alábbi formátumban: YYYY-MM-DD")
            return False

# EgyágyasSzoba osztály (Szoba osztályból származtatva)
class EgyagyasSzoba(Szoba):
    def __init__(self, ar="10.000,- Ft/fő/éj", szobaszam="101", szoba_tipus="Egyágyas szoba"):
        super().__init__(ar, szobaszam, szoba_tipus)

# KétágyasSzoba osztály (Szoba osztályból származtatva)
class KetagyasSzoba(Szoba):
    def __init__(self, ar="15.000,- Ft/fő/éj", szobaszam="102", szoba_tipus="Kétágyas szoba"):
        super().__init__(ar, szobaszam, szoba_tipus)

# Foglalás osztály
class Foglalas:
    def __init__(self, foglalas_id, vendeg_neve, kezdo_datum, vegso_datum, szoba):
        self.foglalas_id = foglalas_id
        self.vendeg_neve = vendeg_neve
        self.kezdo_datum = kezdo_datum
        self.vegso_datum = vegso_datum
        self.szoba = szoba

    def __str__(self):
        return f"Foglalás ID: {self.foglalas_id}, Vendég neve: {self.vendeg_neve}, Kezdő dátum: {self.kezdo_datum}, Végső dátum: {self.vegso_datum}, Szoba szám: {self.szoba.szobaszam}"

    def lemondas(self):
        # Ellenőrizd, hogy a foglalás adatai megfelelnek-e
        return self.szoba.foglalas_lemondasa(self.kezdo_datum, self.vegso_datum)

# Szálloda osztály
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def add_foglalas(self, foglalas):
        self.foglalasok.append(foglalas)

    def listaz_foglalasok(self):
        foglalas_lista = ""
        for foglalas in self.foglalasok:
            foglalas_lista += str(foglalas) + "\n"
        return foglalas_lista

    def listaz_lehetséges_lemondhato_foglalasok(self):
        lemondhato_foglalasok = []
        for foglalas in self.foglalasok:
            if foglalas.szoba.foglalt and foglalas.szoba.foglalt_kezdo_datum == foglalas.kezdo_datum and foglalas.szoba.foglalt_vegso_datum == foglalas.vegso_datum:
                lemondhato_foglalasok.append(foglalas)
        return lemondhato_foglalasok

# Szálloda felhasználói felület
class SzallodaUI:
    def __init__(self, szalloda):
        self.szalloda = szalloda

    def futas(self):
        print("\nÜdvözlöm a szálloda foglalási rendszerében.")
        print("Kérem, válasszon az alábbi menüpontok közül:")
        while True:
            print("\n1. Foglalás létrehozása")
            print("2. Foglalás lemondása")
            print("3. Foglalások listázása")
            print("4. Kilépés")

            try:
                valasztas = int(input("\nVálasszon egy műveletet: "))

                if valasztas == 1:
                    self.foglalas_letrehozasa()
                elif valasztas == 2:
                    self.foglalas_lemondasa()
                elif valasztas == 3:
                    self.foglalasok_listazasa()
                elif valasztas == 4:
                    print("\nKilépés...")
                    break
                else:
                    print("\nÉrvénytelen választás. Kérjük, válasszon 1-4 között.")
            except ValueError:
                print("\nKérjük, számot adjon meg a választáshoz.")

    def foglalas_letrehozasa(self):
        vendeg_neve = input("\nAdja meg a vendég nevét: ")

        # Aktuális dátum lekérése
        aktualis_datum = datetime.now().date()

        # Kezdő dátum bekérése és ellenőrzése
        while True:
            kezdo_datum = input("Adja meg a kezdő dátumot (YYYY-MM-DD): ")
            try:
                kezdo_datum = datetime.strptime(kezdo_datum, "%Y-%m-%d").date()
                # Ellenőrizzük, hogy a kezdő dátum nem korábbi-e, mint az aktuális dátum
                if kezdo_datum >= aktualis_datum:
                    kezdo_datum = kezdo_datum.strftime("%Y-%m-%d")
                    break  # Ha helyes dátum és nem korábbi, kilépünk a ciklusból
                else:
                    print("A kezdő dátum nem lehet korábbi, mint az aktuális dátum.")
            except ValueError:
                print("Nem megfelelő dátum formátum. Kérjük, adja meg a dátumot az alábbi formátumban: YYYY-MM-DD.")

        # Végső dátum bekérése és ellenőrzése
        while True:
            vegso_datum = input("Adja meg a végső dátumot (YYYY-MM-DD): ")
            try:
                vegso_datum = datetime.strptime(vegso_datum, "%Y-%m-%d").date()
                # Ellenőrizzük, hogy a végső dátum nem korábbi-e, mint a kezdő dátum
                if vegso_datum >= aktualis_datum:
                    vegso_datum = vegso_datum.strftime("%Y-%m-%d")
                    break  # Ha helyes dátum és nem korábbi, kilépünk a ciklusból
                else:
                    print("A végső dátum nem lehet korábbi, mint a kezdő dátum.")
            except ValueError:
                print("Nem megfelelő dátum formátum. Kérjük, adja meg a dátumot az alábbi formátumban: YYYY-MM-DD.")

        # Listázás a szabad szobákról
        print("\nSzabad szobák:")
        szabad_szobak = [szoba for szoba in self.szalloda.szobak if not szoba.foglalt]
        for szoba in szabad_szobak:
            print(f"Szoba szám: {szoba.szobaszam}, Szoba típus: {szoba.szoba_tipus}, Ár: {szoba.ar}")

        # Szoba kiválasztása
        while True:
            try:
                szoba_szam = int(input("\nAdja meg a foglalni kívánt szoba számát: "))
                kivalsztott_szoba = None
                for szoba in self.szalloda.szobak:
                    if szoba.szobaszam == szoba_szam:
                        kivalsztott_szoba = szoba
                        break
                if kivalsztott_szoba is not None and kivalsztott_szoba.foglalas_letrehozasa(kezdo_datum, vegso_datum):
                    foglalas_id = len(self.szalloda.foglalasok) + 1
                    foglalas = Foglalas(foglalas_id, vendeg_neve, kezdo_datum, vegso_datum, kivalsztott_szoba)
                    self.szalloda.add_foglalas(foglalas)
                    print(f"\nA foglalás létrejött. Foglalás ID: {foglalas_id}")
                    break
                else:
                    print("\nNem sikerült létrehozni a foglalást. Próbálja újra.")
                    break
            except ValueError:
                print("\nHibás bemenet. Kérjük, próbálja újra.")

    def foglalas_lemondasa(self):
        print("\nLemondható foglalások:")
        lemondhato_foglalasok = self.szalloda.listaz_lehetséges_lemondhato_foglalasok()

        # Ellenőrizze, hogy vannak-e lemondható foglalások
        if not lemondhato_foglalasok:
            print("Nincs lemondható foglalás.")
            return  # Visszatérés a menübe

        # Ha vannak lemondható foglalások, listázza ki őket
        for foglalas in lemondhato_foglalasok:
            print(f"{foglalas}")

        try:
            foglalas_id = int(input("\nAdja meg a foglalás ID-jét a lemondáshoz: "))

            # Foglalás keresése az adott foglalás ID alapján
            foglalas = next((f for f in self.szalloda.foglalasok if f.foglalas_id == foglalas_id), None)

            if foglalas:
                if foglalas.lemondas():
                    self.szalloda.foglalasok.remove(foglalas)
                    print("\nFoglalás sikeresen lemondva!")
                else:
                    print("\nNem lehet lemondani a foglalást.")
            else:
                print("\nA megadott foglalás ID nem található.")
        except ValueError:
            print("\nKérjük, számot adjon meg a foglalás ID-jéhez.")

    def foglalasok_listazasa(self):
        print("\nFoglalások listája:")
        print(self.szalloda.listaz_foglalasok())

if __name__ == "__main__":
    szalloda = Szalloda("Példa Szálloda")
    #Példa szobák hozzáadása a szállodához
    szalloda.add_szoba(EgyagyasSzoba("10.000,- Ft/fő/éj", 101))
    szalloda.add_szoba(KetagyasSzoba("15.000,- Ft/fő/éj", 102))
    szalloda.add_szoba(KetagyasSzoba("15.000,- Ft/fő/éj", 103))

    # Példa foglalások hozzáadása a szállodához
    foglalas1 = Foglalas(1, "Lapos Elemér", "2024-05-01", "2024-05-05", szalloda.szobak[0])
    foglalas2 = Foglalas(2, "Akna Antal", "2024-06-01", "2024-06-05", szalloda.szobak[1])
    foglalas3 = Foglalas(3, "Teszt Géza", "2024-07-01", "2024-07-05", szalloda.szobak[2])
    foglalas4 = Foglalas(4, "Vad Virág", "2024-08-01", "2024-08-05", szalloda.szobak[0])
    foglalas5 = Foglalas(5, "Kék Jácint", "2024-09-01", "2024-09-05", szalloda.szobak[1])

    # Foglalások hozzáadása a szállodához
    szalloda.add_foglalas(foglalas1)
    szalloda.add_foglalas(foglalas2)
    szalloda.add_foglalas(foglalas3)
    szalloda.add_foglalas(foglalas4)
    szalloda.add_foglalas(foglalas5)

    szalloda_ui = SzallodaUI(szalloda)
    szalloda_ui.futas()