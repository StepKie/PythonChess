#pygame ab Version 2.0 wird benötigt
#Installation im Terminal mit 
#   --> pip install pygame (windows) 
#   --> pip3 install pygame (mac)
#   --> sudo apt-get install python3-pygame (Linux Debian/Ubuntu/Mint)

import pygame as pg
import os
# in den folgenden Zeilen werden Startwerte wie zum Beispiel die Breite und
# Höhe des Spielfeldes festgelegt
pg.init()
BREITE, HÖHE = 800,800
FPS = 40 
screen = pg.display.set_mode((BREITE, HÖHE))


weitermachen = True
clock = pg.time.Clock()

def LadeFigur(figurkuerzel):
  return pg.transform.smoothscale(pg.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figuren', figurkuerzel)), (BREITE // 8, HÖHE // 8))

bk = LadeFigur('bk.png')
bq = LadeFigur('bq.png')
bb = LadeFigur('bb.png')
br = LadeFigur('br.png')
bn = LadeFigur('bn.png')
bp = LadeFigur('bp.png')


wk = LadeFigur('wk.png')
wq = LadeFigur('wq.png')
wb = LadeFigur('wb.png')
wr = LadeFigur('wr.png')
wn = LadeFigur('wn.png')
wp = LadeFigur('wp.png')

  # ab hier wird mit 40 FPS das Bild im Hintergrund gezeichnet (also sozusagen vorbereitet)
  # achtung! das Zeichnen des Bildes bedeutet noch nicht, dass es auch sichtbar ist
  

  # Die folgende Anweisung füllt den Bilschirm mit einer Farbe
  # Farben können in Python zum Beispiel als Mischung aus den Basifarben Rot, Grün und Blau angegeben werden
  # (0,0,0) steht beispielsweise für die Mischung aus keinem Rot (da 0) und keinem Grün und keinem Blau, was
  # zusammen überraschenderweise die Farbe Schwarz ergibt
#screen.fill((100,15,15))


  # ... und der folgende Befehl zeichnet ein Rechteck
  # Der Befehl ist dabei wie folgt aufgebaut:
  # pg.draw.rect(Bilschirm_auf_dem_gezeichnet_wird , (Farbwerte Rot, Grün, Blau), [x-Koordinate obere linke Ecke, y-Koordinate obere linke Ecke, Rechteckbreite, Rechteckhöhe])

WHITE = (240,240,240)
BLACK = (100,115,15)

  # mit hilfe einer Schleife kann man natürlich auch mehrere Rechtecke in Folge zeichnen ...
  

for x in range(8):
  for y in range(8):
    color =  (WHITE, BLACK)[(x +y) % 2]
    pg.draw.rect(screen, color, [x * 100, y * 100, 100, 100])      
  
  screen.blit(bk, (400,0))
  screen.blit(bq, (300,0))
  screen.blit(bb, (200,0))
  screen.blit(bb, (500,0))
  screen.blit(bn, (600,0))
  screen.blit(bn, (100,0))
  screen.blit(br, (0,0))
  screen.blit(br, (700,0))
  for x in range (8):
    screen.blit(bp, (x*100, 100))

  screen.blit(wk, (400,700))
  screen.blit(wq, (300,700))
  screen.blit(wb, (200,700))
  screen.blit(wb, (500,700))
  screen.blit(wn, (600,700))
  screen.blit(wn, (100,700))
  screen.blit(wr, (0,700))
  screen.blit(wr, (700,700))
  for x in range (8):
    screen.blit(wp, (x*100, 600))




  pg.display.flip()

# ab hier beginnt die Schleife, in der das eigentliche Spiel läuft
while weitermachen:
  clock.tick(FPS)
  
  for ereignis in pg.event.get():
    if ereignis.type == pg.MOUSEBUTTONDOWN:
        print('Die Maus wurde geklickt.')
        # Die Position der Maus kann man wie folgt abfragen:
        print(pg.mouse.get_pos())
    if ereignis.type == pg.QUIT:
      weitermachen = False

pg.quit()

