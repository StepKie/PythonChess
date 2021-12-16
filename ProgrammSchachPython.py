import pygame as pg
import os

pg.init()
BREITE = 800
HOEHE = 800
FELDBREITE = BREITE // 8
FELDHOEHE = HOEHE // 8

WHITE = (240, 240, 240)
BLACK = (100, 115, 15)

STANDARDFIGUREN = [('r', 'br'), ('n', 'bn'), ('b', 'bb'), ('q', 'bq'), ('k', 'bk'), ('p', 'bp'),
                   ('R', 'wr'), ('N', 'wn'), ('B', 'wb'), ('Q', 'wq'), ('K', 'wk'), ('P', 'wp')]

FPS = 40
screen = pg.display.set_mode((BREITE, HOEHE))

# Die aktuelle Stellung auf dem Brett
# stellung[0][0] ist oben links, d.h. a8
# stellung[7][7] ist unten rechts, d.h. h1
# stellung[2][4] - e6 (von oben links 2 runter, 4 rechts)
stellung = [[]]


def mache_zug(von, nach):
    figur = stellung[von[1]][von[0]]
    stellung[von[1]][von[0]] = "-"
    stellung[nach[1]][nach[0]] = figur
    zeichne_stellung()


def feld_zu_koordinaten(spalte, zeile):
    return spalte * FELDBREITE, zeile * FELDHOEHE


def koordinaten_zu_feld(x, y):
    return x // FELDBREITE, y // FELDHOEHE


def lade_figuren():
    bilder = {}
    for figur, dateiname in STANDARDFIGUREN:
        bilder[figur] = pg.transform.smoothscale(
            pg.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figuren', dateiname + '.png')),
            (FELDBREITE, FELDHOEHE))
    return bilder


def erstelle_ausgangsstellung():
    grundstellung = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"]
    ]
    return grundstellung


def zeichne_stellung():
    for zeile in range(len(stellung)):
        for spalte in range(len(stellung[0])):
            color = (WHITE, BLACK)[(spalte + zeile) % 2]
            (x, y) = feld_zu_koordinaten(spalte, zeile)
            pg.draw.rect(screen, color, [x, y, FELDBREITE, FELDHOEHE])
            if stellung[zeile][spalte] != '-':
                screen.blit(bilder_der_figuren[stellung[zeile][spalte]], (x, y))
    pg.display.flip()


# Hier geht das Hauptprogramm los

# Die Bilder der Figuren werden für die spätere Anzeige aus Dateien geladen und in einer Liste gespeichert.
bilder_der_figuren = lade_figuren()
stellung = erstelle_ausgangsstellung()

zeichne_stellung()

weitermachen = True
clock = pg.time.Clock()
pg.display.set_caption('Philipps Schachprogramm')

# ab hier beginnt die Schleife, in der das eigentliche Spiel läuft
while weitermachen:
    clock.tick(FPS)

    for ereignis in pg.event.get():
        if ereignis.type == pg.MOUSEBUTTONDOWN:
            print('Die Maus wurde geklickt.')
            koordinate_von = pg.mouse.get_pos()
            print(koordinate_von)
        if ereignis.type == pg.MOUSEBUTTONUP:
            print('Die Maus wurde losgelassen.')
            koordinate_nach = pg.mouse.get_pos()
            print(koordinate_nach)
            mache_zug(koordinaten_zu_feld(*koordinate_von), koordinaten_zu_feld(*koordinate_nach))

        if ereignis.type == pg.QUIT:
            weitermachen = False

pg.quit()
