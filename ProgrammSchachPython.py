import pygame as pg
import os
import sys

pg.init()
BREITE = 800
HOEHE = 800
FELDBREITE = BREITE // 8
FELDHOEHE = HOEHE // 8
FPS = 40

WHITE = pg.Color("white")
BLACK = pg.Color("grey")
GREEN = pg.Color("darkgreen")

STANDARDFIGUREN = [('r', 'br'), ('n', 'bn'), ('b', 'bb'), ('q', 'bq'), ('k', 'bk'), ('p', 'bp'),
                   ('R', 'wr'), ('N', 'wn'), ('B', 'wb'), ('Q', 'wq'), ('K', 'wk'), ('P', 'wp')]

screen = pg.display.set_mode((BREITE, HOEHE))


def mache_zug(von, nach):
    figur = stellung[von[1]][von[0]]
    if figur == "-":
        return
    stellung[von[1]][von[0]] = "-"
    stellung[nach[1]][nach[0]] = figur
    return 'b' if am_zug == 'w' else 'w'


def feld_zu_koordinaten(linie, reihe):
    return linie * FELDBREITE, reihe * FELDHOEHE


def koordinaten_zu_feld(koordinate_x, koordinate_y):
    return koordinate_x // FELDBREITE, koordinate_y // FELDHOEHE


def lade_figuren():
    bilder = {}
    for figur, dateiname in STANDARDFIGUREN:
        bilder[figur] = pg.transform.smoothscale(
            pg.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figuren', dateiname + '.png')),
            (FELDBREITE, FELDHOEHE))
    return bilder


def ist_gegnerische_figur(figur):
    return (figur.islower() and am_zug == 'w') or (figur.isupper() and am_zug == 'b')


def ist_eigene_figur(figur):
    return (figur.islower() and am_zug == 'b') or (figur.isupper() and am_zug == 'w')


# TODO Prüfe, ob entstehende Stellung legal ist -
# (eigener König kann danach nicht "geschlagen" werden - d.h. im Schach oder Könige nebeneinander)
def legale_zielfelder(von_feld):
    if von_feld == ():
        return []
    startlinie, startreihe = von_feld
    figur = stellung[startreihe][startlinie]
    if not ist_eigene_figur(figur):
        return []
    gerade_richtungen = ((-1, 0), (0, -1), (1, 0), (0, 1))  # oben, links, unten, rechts
    schraege_richtungen = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # linksoben, rechtsoben, rechtsunten, linksunten
    springer_richtungen = ((-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1))
    alle_richtungen = gerade_richtungen + schraege_richtungen
    if figur.upper() == "N":
        return felder_in_richtung(startlinie, startreihe, 1, springer_richtungen)
    if figur.upper() == "B":
        return felder_in_richtung(startlinie, startreihe, 7, schraege_richtungen)
    if figur.upper() == "R":
        return felder_in_richtung(startlinie, startreihe, 7, gerade_richtungen)
    if figur.upper() == "Q":
        return felder_in_richtung(startlinie, startreihe, 7, alle_richtungen)
    # TODO Rochade
    if figur.upper() == "K":
        return felder_in_richtung(startlinie, startreihe, 1, alle_richtungen)
    zielfelder = []
    # TODO Schöner machen, en-passant, Bauernumwandlung
    if figur == "P":
        if stellung[startreihe - 1][startlinie] == "-":
            zielfelder.append((startlinie, startreihe - 1))
            if startreihe == 6 and stellung[startreihe - 2][startlinie] == "-":
                zielfelder.append((startlinie, startreihe - 2))
        if ist_gegnerische_figur(stellung[startreihe - 1][startlinie - 1]):
            zielfelder.append((startlinie - 1, startreihe - 1))
        if ist_gegnerische_figur(stellung[startreihe - 1][startlinie + 1]):
            zielfelder.append((startlinie + 1, startreihe - 1))
    if figur == "p":
        if stellung[startreihe + 1][startlinie] == "-":
            zielfelder.append((startlinie, startreihe + 1))
            if startreihe == 1 and stellung[startreihe + 2][startlinie] == "-":
                zielfelder.append((startlinie, startreihe + 2))
        if ist_gegnerische_figur(stellung[startreihe + 1][startlinie - 1]):
            zielfelder.append((startlinie - 1, startreihe + 1))
        if ist_gegnerische_figur(stellung[startreihe + 1][startlinie + 1]):
            zielfelder.append((startlinie + 1, startreihe + 1))
    return zielfelder


def felder_in_richtung(startlinie, startreihe, maximale_entfernung, richtungen):
    zielfelder = []

    for richtung in richtungen:
        for i in range(1, maximale_entfernung + 1):
            end_reihe = startreihe + richtung[0] * i
            end_linie = startlinie + richtung[1] * i
            if 0 <= end_reihe <= 7 and 0 <= end_linie <= 7:  # nur innerhalb des Bretts
                zielfeldfigur = stellung[end_reihe][end_linie]
                if ist_eigene_figur(zielfeldfigur):
                    break
                zielfelder.append((end_linie, end_reihe))
                if ist_gegnerische_figur(zielfeldfigur):
                    break
            else:
                break
    return zielfelder


def schraege_felder(startlinie, startreihe, maximale_entfernung):
    zielfelder = []
    richtungen = ((-1, 0), (0, -1), (1, 0), (0, 1))  # oben, links, unten, rechts
    for richtung in richtungen:
        for i in range(1, 8):
            end_reihe = startreihe + richtung[0] * i
            end_linie = startlinie + richtung[1] * i
            if 0 <= end_reihe <= 7 and 0 <= end_linie <= 7:  # nur innerhalb des Bretts
                zielfeldfigur = stellung[end_reihe][end_linie]
                if ist_eigene_figur(zielfeldfigur):
                    break
                zielfelder.append((end_linie, end_reihe))
                if ist_gegnerische_figur(zielfeldfigur):
                    break
            else:
                break
    return zielfelder


def springer_felder(startlinie, startreihe):
    pass


def bauern_felder(startlinie, startreihe):
    pass


def erstelle_ausgangsstellung():
    return [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-"],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"]
    ]


def zeichne_stellung(markierte_felder=None):
    """ Zeichne Stellung. Markierte Felder werden grün hinterlegt"""
    if markierte_felder is None:
        markierte_felder = []
    for reihe in range(len(stellung)):
        for linie in range(len(stellung[0])):
            color = (WHITE, BLACK)[(linie + reihe) % 2]
            if (linie, reihe) in markierte_felder:
                color = GREEN
            koordinate_x, koordinate_y = feld_zu_koordinaten(linie, reihe)
            pg.draw.rect(screen, color, [koordinate_x, koordinate_y, FELDBREITE, FELDHOEHE])
            if stellung[reihe][linie] != '-':
                screen.blit(bilder_der_figuren[stellung[reihe][linie]], (koordinate_x, koordinate_y))
    pg.display.flip()


# Hier geht das Hauptprogramm los

# Die Bilder der Figuren werden für die spätere Anzeige aus Dateien geladen und in einer Liste gespeichert.
bilder_der_figuren = lade_figuren()

# Die aktuelle Stellung auf dem Brett
# stellung[0][0] ist oben links, d.h. a8
# stellung[7][7] ist unten rechts, d.h. h1
# stellung[2][4] - e6 (von oben links 2 runter, 4 rechts)
stellung = erstelle_ausgangsstellung()
zeichne_stellung()
# Nächste Stellung brauchen wir, wenn wir überprüfen wollen, ob nach einem Zug der Spieler im Schach stehen würde
naechste_stellung = [[]]

am_zug = 'w'
clock = pg.time.Clock()
pg.display.set_caption('Philipps Schachprogramm')
startfeld = ()
# ab hier beginnt die Schleife, in der das eigentliche Spiel läuft
while True:
    clock.tick(FPS)
    for ereignis in pg.event.get():
        event = ereignis.type
        if event == pg.MOUSEBUTTONDOWN or event == pg.MOUSEBUTTONUP:
            maus_feld = koordinaten_zu_feld(*pg.mouse.get_pos())
            if startfeld == () or maus_feld not in legale_zielfelder(startfeld):
                dorthinkannmanziehen = legale_zielfelder(maus_feld)
                if dorthinkannmanziehen:
                    startfeld = maus_feld
                zeichne_stellung(dorthinkannmanziehen)
            if maus_feld in legale_zielfelder(startfeld):
                am_zug = mache_zug(startfeld, maus_feld)
                startfeld = ()
                dorthinkannmanziehen = []
                zeichne_stellung()
        if event == pg.QUIT:
            pg.quit()
            sys.exit()
