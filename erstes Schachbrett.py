#pygame ab Version 2.0 wird benötigt
#Installation im Terminal mit 
#   --> pip install pygame (windows) 
#   --> pip3 install pygame (mac)
#   --> sudo apt-get install python3-pygame (Linux Debian/Ubuntu/Mint)

import pygame as pg

# in den folgenden Zeilen werden Startwerte wie zum Beispiel die Breite und
# Höhe des Spielfeldes festgelegt
pg.init()
BREITE, HÖHE = 500,500
FPS = 40
screen = pg.display.set_mode((BREITE, HÖHE))

weitermachen = True
clock = pg.time.Clock()

# ab hier beginnt die Schleife, in der das eigentliche Spiel läuft
while weitermachen:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
  # ab hier wird mit 40 FPS das Bild im Hintergrund gezeichnet (also sozusagen vorbereitet)
  # achtung! das Zeichnen des Bildes bedeutet noch nicht, dass es auch sichtbar ist
  

  # Die folgende Anweisung füllt den Bilschirm mit einer Farbe
  # Farben können in Python zum Beispiel als Mischung aus den Basifarben Rot, Grün und Blau angegeben werden
  # (0,0,0) steht beispielsweise für die Mischung aus keinem Rot (da 0) und keinem Grün und keinem Blau, was
  # zusammen überraschenderweise die Farbe Schwarz ergibt
  screen.fill((0,0,0))


  # ... und der folgende Befehl zeichnet ein Rechteck
  # Der Befehl ist dabei wie folgt aufgebaut:
  # pg.draw.rect(Bilschirm_auf_dem_gezeichnet_wird , (Farbwerte Rot, Grün, Blau), [x-Koordinate obere linke Ecke, y-Koordinate obere linke Ecke, Rechteckbreite, Rechteckhöhe])



  # mit hilfe einer Schleife kann man natürlich auch mehrere Rechtecke in Folge zeichnen ...
  for x in range(8):
        pg.draw.rect(screen, (250,250,250), [x*64, 0, 55, 55])
        pg.draw.rect(screen, (250,0,0), [x*64, 64, 55, 55])
        pg.draw.rect(screen, (250,0,0), [x*64, 128, 55, 55])
        pg.draw.rect(screen, (250,0,0), [x*64, 192, 55, 55])
        pg.draw.rect(screen, (250,0,0), [x*64, 256, 55, 55])
        pg.draw.rect(screen, (250,0,0), [x*64, 320, 55, 55])
        pg.draw.rect(screen, (250,0,0), [x*64, 384, 55, 55])
        pg.draw.rect(screen, (250,0,0), [x*64, 448, 55, 55])

  # hier wird das im Hintergrund gezeichnete Bild sichtbar gemacht
  pg.display.flip()

pg.quit()