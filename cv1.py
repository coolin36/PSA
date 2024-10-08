#!/usr/bin/env python3
print("2024 MUSIC")

def prva_funkcia():
    a = 1+4
    return a

b = prva_funkcia()
print(b)

def funkcia_pozdrav(meno):
    #return "Ahoj " + meno + ", ako sa mas?"
    return "Ahoj {1} {0} {0} {1}, ako sa mas?".format(meno, "---")

print(funkcia_pozdrav("Roland"))

meno = input("Zadajte meno na pozdravenie: ")
print(funkcia_pozdrav(meno))

class PrvaTrieda():
    def __init__(self):
        self._meno = "Roland"
        self._priezvisko = "Zemanovic"
    
    def pozdrav(self):
        print("Ahoj {} {}. ".format(self._meno, self._priezvisko))

pozdravovac = PrvaTrieda()
pozdravovac.pozdrav

if __name__ == "__main__":
    pozdravovac = PrvaTrieda()
    pozdravovac.pozdrav