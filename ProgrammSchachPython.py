import pygame as pg
import os
# in den folgenden Zeilen werden Startwerte wie zum Beispiel die Breite und
# Höhe des Spielfeldes festgelegt
pg.init()
BREITE = 800
HOEHE = 800
FELDBREITE = BREITE // 8
FELDHOEHE = HOEHE // 8

WHITE = (240,240,240)
BLACK = (100,115,15)

# Die Konstante STANDARDFIGUREN ist eine Liste, die paarweise den Namen einer Figur in Kurzform (z.B. P für den weißen Bauern) und den Dateinamen
# der passenden Grafik enthält. Damit erleichtert man sich später das Laden der Grafiken für die Figuren.
STANDARDFIGUREN = [('r','br'), ('n','bn'), ('b','bb'), ('q','bq'), ('k','bk'), ('p','bp'),
                   ('R','wr'), ('N','wn'), ('B','wb'), ('Q','wq'), ('K','wk'), ('P','wp')]

FPS = 40 
screen = pg.display.set_mode((BREITE, HOEHE))


weitermachen = True
clock = pg.time.Clock()


def MacheZug(von, nach):
  return 0

def feldZuKoordinaten(spalte, zeile):
    return spalte*FELDBREITE, zeile*FELDHOEHE

def koordinatenZuFeld(x, y):
    return x//FELDBREITE, y//FELDHOEHE

def ladeFiguren(figurenliste):
  bilder = {}
  for figur, dateiname in figurenliste:
    bilder[figur] = pg.transform.smoothscale(pg.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figuren', dateiname + '.png')),(FELDBREITE,FELDHOEHE))
  return bilder
# Die Bilder der Figuren werden für die spätere Anzeige aus Dateien geladen und in einer Liste gespeichert.
bilder_der_figuren = ladeFiguren(STANDARDFIGUREN)


def BaueBrettAuf():
  stellung = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
  ]
  return stellung

def ZeichneStellung(stellung):
  for zeile in range(len(stellung)):
    for spalte in range(len(stellung[0])):
      color =  (WHITE, BLACK)[(spalte + zeile) % 2]
      pg.draw.rect(screen, color, [spalte * 100, zeile * 100, 100, 100])
      if (stellung[zeile][spalte] != '-'):
        screen.blit(bilder_der_figuren[stellung[zeile][spalte]], feldZuKoordinaten(spalte, zeile))

  pg.display.flip()


ausgangsstellung = BaueBrettAuf()
ZeichneStellung(ausgangsstellung)

# ab hier beginnt die Schleife, in der das eigentliche Spiel läuft
while weitermachen:
  clock.tick(FPS)
  
  for ereignis in pg.event.get():
    if ereignis.type == pg.MOUSEBUTTONDOWN:
        print('Die Maus wurde geklickt.')
        print(pg.mouse.get_pos())
    if ereignis.type == pg.QUIT:
      weitermachen = False

pg.quit()

