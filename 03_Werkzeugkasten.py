import pygame as pg
import os

# Hier soll ein Werkzeugkasten mit nützlichen Funktionen für den späteren Gebrauch entstehen
# Zum Testen der Werkzeuge geben wir zuerst ein paar Werte vor, die auch im Schachprogramm festgelegt sind
# bzw. die wir zum Testen der Funktionen verwenden wollen
BREITE, HÖHE = 500, 500
dateipfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figuren', 'bk.png')

# nützlich für die spätere Arbeit ist zum Beispiel eine Funktion, die uns die x- und y-Koordinaten unseres
# pygame-Fensters auf die zugehörigen Feldnummern des zu den Koordinaten gehörenden Schachfeldes umrechnet.
# Das geht wie folgt. Tipp: die Operation // steht für das ganzzahlige Teilen ohne Rest
def koordinatenZuFeld(x, y):
    return x//(BREITE//8), y//(HÖHE//8)


# Und jetzt du: Vervollständige die folgende Funktion, die Felder die Nummer eines Feldes erhält und daraus
# die x- und y-Koordinaten der Mitte des Feldes berechnet. Tipp: hilfreicht ist dabei die Funktion round() ,
# die eine Zahl ganzzahlig rundet.
def felderZuKoordinaten(spalte, zeile):
    return 'Hier muss deine Funktion hin'


# Tipp: Da Bilder (z.B. für die Spielfiguren) immer anhand ihrer oberen linken Ecke platziert werden, ist es
#       nützlich, nicht nur die Koordinaten der Mitte eines Schachfeldes zu kennen, sondern auch berechnen
#       zu können, an welchen Koordinaten die linke obere Ecke eines Bildes liegen muss, damit das Bild in
#       der Mitte eines Schachfeldes platziert ist. Das hängt natürlich auch von der Größe des Bildes ab ...

# ... schau dir dazu einmal an, welche Werte die folgenden Befehle zu den Beispielbild ausgeben
bildgroessen = pg.image.load(dateipfad).get_rect()
print(bildgroessen)
print(bildgroessen.center[0])
print(bildgroessen.center[1])
print(bildgroessen.width)
print(bildgroessen.height)

# und nun bist du wieder an der Reihe. Schreibe eine Funktion, die die korrekten Koordinaten für ein
# Bild berechnet
def koordinatenZuBildkoordinaten(x, y, bild):
    return 'Hier muss deine Funktion hin'


# Zum testen der Befehle:
print(koordinatenZuFeld(50,50))

# print(felderZuKoordinaten(0,0))

# x, y = felderZuKoordinaten(1,2)
# print(koordinatenZuBildkoordinaten(x, y, pg.image.load(dateipfad)))