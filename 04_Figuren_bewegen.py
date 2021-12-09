import pygame as pg
import os

# Hier steht nun eine ganze Menge mehr Quellcode als in den vorherigen Beispielen. Der Inhalt ist nicht immer neu oder wichtig, bietet
# aber als Beispiel viel Interessantes zum nachgucken und nachvollziehen. Der spannende Part für das Bewegen der Figuren ist primär
# das Codieren der Stellung auf dem Schachbrett und das Auslesen von Mausbewegungen. Beides findet man im unteren Teil des Programms.
# Nun aber zum Programm ...



# Zuerst werden ein paar nützliche Hilfsfunktionen angelegt ...
def zeichneBrett(brett, farbe1 = '#DFBF93', farbe2 = '#C5844E'): # <-- mit einem Gleichheitszeichen hinter einem Parameter gibt man einen Standardwert
    for (spalte, zeile), feld in brett.items():                  #     vor, der verwendet wird, falls beim Aufruf kein passender Wert mitgegeben wurde.
        if feld == True:                                         #     Hier sind das die Standardfarben Hellbraun und Dunkelbraun.
            farbe = farbe1
        else:
            farbe = farbe2
        pg.draw.rect(screen, farbe, (spalte*FELDBREITE, zeile*FELDHOEHE, FELDBREITE, FELDHOEHE))

def ladeFiguren(figurenliste):
  bilder = {}
  for figur, dateiname in figurenliste:
    bilder[figur] = pg.transform.smoothscale(pg.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figuren', dateiname + '.png')),(FELDBREITE,FELDHOEHE))
  return bilder

def zeichneFiguren(stellung, figurenbilder):
  for spalte in range(len(stellung)):
    for zeile in range(len(stellung[0])):
      if (stellung[spalte][zeile] != 'leer'):
        screen.blit(figurenbilder[stellung[spalte][zeile]], feldZuKoordinaten(spalte, zeile))

def feldZuKoordinaten(spalte, zeile):
    return spalte*FELDBREITE, zeile*FELDHOEHE

def koordinatenZuFeld(x, y):
    return x//FELDBREITE, y//FELDHOEHE


# Nun folgt die übliche Initialisierung (Festlegung der Startwerte)
pg.init()
BREITE = 600
HOEHE = 600
FELDER_PRO_ZEILE = 8
FELDER_PRO_SPALTE = 8
FELDBREITE = BREITE // FELDER_PRO_ZEILE
FELDHOEHE = HOEHE // FELDER_PRO_SPALTE
FPS = 40
screen = pg.display.set_mode((BREITE, HOEHE))
pg.display.set_caption('Chess Deluxe')
weitermachen = True
clock = pg.time.Clock()

# Anschließend werden ein paar Konstanten festgelegt, die die spätere Arbeit erleichtern sollen.
# Die Konstante BRETT enthält ein Wörterbuch (sozusagen eine Zuordnung von einem Wert zu einem anderen --> Wörterbücher werden mit { } markiert)
# , das jedem Schachfeld (spalte, zeile) einen Wahrheitswert (true oder false) zuordnet. Dabei wird allen hellen Feldern true und allen dunklen
# Feldern false zugeordnet. Dies kann hilfreich sein, damit man nicht bei jedem neuen Zeichnen des Schachbrettes erneut bestimmen muss, welche
# Felder dunkel und welche hell sind.
BRETT = {(spalte, zeile): (spalte + zeile) % 2 == 0 for spalte in range(FELDER_PRO_ZEILE) for zeile in range(FELDER_PRO_SPALTE)}

# Die Konstante STANDARDFIGUREN ist eine Liste, die paarweise den Namen einer Figur in Kurzform (z.B. P für den weißen Bauern) und den Dateinamen
# der passenden Grafik enthält. Damit erleichtert man sich später das Laden der Grafiken für die Figuren.
STANDARDFIGUREN = [('r','br'), ('n','bn'), ('b','bb'), ('q','bq'), ('k','bk'), ('p','bp'),
                   ('R','wr'), ('N','wn'), ('B','wb'), ('Q','wq'), ('K','wk'), ('P','wp')]

# Die Bilder der Figuren werden für die spätere Anzeige aus Dateien geladen und in einer Liste gespeichert.
bilder_der_figuren = ladeFiguren(STANDARDFIGUREN)





# Nun wird die aktuelle Stellung der Figuren festgelegt. Dazu bietet sich eine Liste an, die zu jedem der 8x8 Felder entweder den Wert
# 'leer' oder die Kurzform der Figur speichert, die sich auf dem Feld befindet. Zuerst erstellt man sich dazu ein leeres 8x8-Brett ...
stellung = []
for spalte in range(FELDER_PRO_SPALTE):
  fertige_spalte = []
  for zeile in range(FELDER_PRO_ZEILE):
    fertige_spalte.append('leer')
  stellung.append(fertige_spalte)
# ... dann werden einige leere Felder mit Figuren besetzt. Zuerst setzen wir einen weißen König auf das Feld (1,1).
stellung[1][1] = 'K'
# ... und einen schwarzen Bauern auf das Feld (1,3)
stellung[1][3] = 'p'
# ... und einen weißen Bauern auf das Feld (4,7)
stellung[4][7] = 'r'



# Der Spielablauf beginnt wie üblich.
while weitermachen:
  clock.tick(FPS)

  # Hier können wir nun endlich die Mausbewegung abfragen!
  # Dazu nutzen wir einfach die folgende Schleife, die auch in eurem ursprünglichen Schachbrett-Programm enthalten war.
  # Der Befehl pg.event.get() ruft alle Ereignisse (also zum Beispiel Tastendruck, Maustaste gedrückt, ...) ab, die vor
  # kurzer Zeit stattgefunden haben. Aber Vorsicht: wenn der Befehl einmal benutzt wurde, dann sind die eingetretenen
  # Ereignisse alle von ihrer Ablage entfernt. Mann muss sich sich also am besten irgendwo merken, wenn man sie einmal
  # abruft, damit man sie einzeln durchgehen und abarbeiten kann. Hier werden die übergebenen Ereignisse aus der Ablage
  # in der Variable "ereignis" gespeichert. In dieser Schleife kann man dann zum Beispiel prüfen, ob eines der Ereignisse
  # ein Mausklick war.
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
      # Das geht zum Beispiel so:
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      print('Die Maus wurde geklickt.')
      # Die Position der Maus kann man wie folgt abfragen:
      print(pg.mouse.get_pos())


  # Damit auch etwas zu sehen ist, werden hier das Spielfeld und die Figuren gezeichnet
  # (nichts Neues, Vorgehen genau wie in den vorherigen Kapiteln)
  screen.fill((0,0,0))
  zeichneBrett(BRETT)
  zeichneFiguren(stellung, bilder_der_figuren)
  pg.display.flip()

pg.quit()