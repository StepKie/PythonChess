import pygame as pg
# ein neues Paket mit dem Namen os wird geladen, um das Arbeiten mit Dateipfaden zu vereinfachen
import os


# ... Startwerte
pg.init()
BREITE, HÖHE = 800,800
screen = pg.display.set_mode((BREITE, HÖHE))
weitermachen = True

# Bilschirm in einer Farbe einfärben (nur damit die Bilder der schwarzen Figuren gegen die Hintergrundfarbe besser sichtbar sind)
screen.fill((220,170,70))


# Um eine Datei zu laden, muss man zuerst einmal wissen, über welchen Pfad die Datei erreichbar ist.
# Ein Pfad ist eine Wegbeschreibung, wie man von einem Laufwerk wie zum Beispiel H: zu einer bestimmten Datei kommt.
# Den Pfad, unter dem die aktuell verwendete Python-Datei liegt, kann man sich immer mit dem Befehl __file__ ausgeben lassen.
# Testen könnte man das zum Beispiel so:
print(__file__)

# Leider wird dieser Pfad nicht für alle Betriebsysteme immer identisch angegeben. Um eine einheitliche
# Darstellung zu erhalten, kann man den folgenden Befehl aus dem os-Paket (OS = Operating System) verwenden.
print(os.path.abspath(__file__))

# Um eine Grafik zu laden, benötigen wir nicht den Pfad der aktuellen Python-Datei sondern den Pfad des Ordners, in dem
# die Datei liegt (denn da liegt ja vermutlich auch der Ordner mit den Bildern der Schachfiguren). Den Pfad des übergeordneten
# Ordners erhalten wir mir folgendem Befehl:
print(os.path.dirname(os.path.abspath(__file__)))

# Nun müssen wir diesem Pfad bloß noch den Namen des Unterodner hinzufügen, in dem unsere Bilder liegen und den Namen
# der Bilddatei anhängen. Auch dazu wird ein Befehl des os-Paketes verwendet (join), den man so formulieren kann:
print(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figuren', 'bk.png'))

# Um einmal ein vollständiges Beispiel anzugeben: mit den folgenden beiden Zeieln kann man das Bild des 
# schwarzen Königs laden (erste Zeile) und an der position (100, 100) im Pygame-Fenster anzeigen (zweite Zeile)
# Damit die Befehle funktionieren, muss natürlich auch ein Ordner namens Figuren im selben Ordner wie diese Datei
# liegen und er muss ein Bild mit dem Namen bk.png enthalten.
bild = pg.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figuren', 'bk.png'))
screen.blit(bild, (100, 100))

# Da Grafiken nach dem Laden oft noch nicht die richtige Größe besitzen, ist es meist hilfreich, die Grafiken
# mit dem folgenden Befehl (smoothscale) auf die passende Größe zu skalieren. In den Klammern wird neben dem
# zu skallierenden Bild die gewünschte Breite und Höhe angegeben.
bild = pg.transform.smoothscale(bild, (BREITE // 8, HÖHE // 8))
screen.blit(bild, (300, 100))





# Nun zu Demonstrationszwecken noch ein paar Zeilen damit das Bild sichtbar wird und sich das pygame-Fenster
# nicht sofort wieder schließt (nichts neues hier)
pg.display.flip()
while weitermachen:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
pg.quit()