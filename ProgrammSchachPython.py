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
    global am_zug, letzter_zug
    figur = figur_auf(*von)
    zielfeldfigur = figur_auf(*nach)
    if figur == "-":
        return
    stellung[von[1]][von[0]] = "-"
    stellung[nach[1]][nach[0]] = figur
    letzter_zug = von, nach, zielfeldfigur
    am_zug = 'b' if am_zug == 'w' else 'w'


def nimm_zurueck():
    global am_zug
    von, nach, geschlagene_figur = letzter_zug
    stellung[von[1]][von[0]] = stellung[nach[1]][nach[0]]
    stellung[nach[1]][nach[0]] = geschlagene_figur
    am_zug = 'b' if am_zug == 'w' else 'w'


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


def figur_auf(linie, reihe):
    if not (0 <= linie <= 7 and 0 <= reihe <= 7):
        return "x"
    return stellung[reihe][linie]


def ist_gegnerische_figur(figur):
    return (figur.islower() and am_zug == 'w') or (figur.isupper() and am_zug == 'b')


def ist_eigene_figur(figur):
    return (figur.islower() and am_zug == 'b') or (figur.isupper() and am_zug == 'w')


def ist_schach():
    for reihe in range(len(stellung)):
        for linie in range(len(stellung[reihe])):
            if ist_eigene_figur(figur_auf(linie, reihe)):
                for zielfeld in alle_zielfelder((linie, reihe)):
                    zielfeldfigur = figur_auf(*zielfeld)
                    if ist_gegnerische_figur(zielfeldfigur) and zielfeldfigur.upper() == "K":
                        print("SCHACH!")
                        return True
    return False


def legale_zielfelder(von_feld):
    zielfelder = alle_zielfelder(von_feld)
    # Entferne Felder wenn man in der resultierenden Stellung im Schach stünde
    for zielfeld in zielfelder:
        mache_zug(von_feld, zielfeld)
        if ist_schach():
            zielfelder.remove(zielfeld)
        nimm_zurueck()
    return zielfelder


# TODO Prüfe, ob entstehende Stellung legal ist -
# (eigener König kann danach nicht "geschlagen" werden - d.h. im Schach oder Könige nebeneinander)
def alle_zielfelder(von_feld):
    if von_feld == ():
        return []
    startlinie, startreihe = von_feld
    figur = figur_auf(startlinie, startreihe)
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
    # TODO en-passant, Bauernumwandlung
    if figur.upper() == "P":
        richtung_reihe = (-1, 1)[figur.islower()]
        ausgangsreihe = (6, 1)[figur.islower()]
        reihe_ein_feld_vor = startreihe + richtung_reihe
        reihe_zwei_felder_vor = startreihe + 2 * richtung_reihe
        if figur_auf(startlinie, startreihe + richtung_reihe) == "-":
            zielfelder.append((startlinie, reihe_ein_feld_vor))
            if startreihe == ausgangsreihe and figur_auf(startlinie, reihe_zwei_felder_vor) == "-":
                zielfelder.append((startlinie, reihe_zwei_felder_vor))
        if ist_gegnerische_figur(figur_auf(startlinie - 1,  reihe_ein_feld_vor)):
            zielfelder.append((startlinie - 1, reihe_ein_feld_vor))
        if ist_gegnerische_figur(figur_auf(startlinie + 1,  reihe_ein_feld_vor)):
            zielfelder.append((startlinie + 1, reihe_ein_feld_vor))
    return zielfelder



def felder_in_richtung(startlinie, startreihe, maximale_entfernung, richtungen):
    zielfelder = []
    for richtung in richtungen:
        for i in range(1, maximale_entfernung + 1):
            end_reihe = startreihe + richtung[0] * i
            end_linie = startlinie + richtung[1] * i
            if 0 <= end_reihe <= 7 and 0 <= end_linie <= 7:  # nur innerhalb des Bretts
                zielfeldfigur = figur_auf(end_linie, end_reihe)
                if ist_eigene_figur(zielfeldfigur):
                    break
                zielfelder.append((end_linie, end_reihe))
                if ist_gegnerische_figur(zielfeldfigur):
                    break
            else:
                break
    return zielfelder


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
            if figur_auf(linie, reihe) != '-':
                screen.blit(bilder_der_figuren[figur_auf(linie, reihe)], (koordinate_x, koordinate_y))
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

am_zug = 'w'

# von, nach, was wurde geschlagen
letzter_zug = ((), (), "-")

clock = pg.time.Clock()
pg.display.set_caption('Philipps Schachprogramm')
startfeld = ()
# ab hier beginnt die Schleife, in der das eigentliche Spiel läuft
while True:
    clock.tick(FPS)
    for ereignis in pg.event.get():
        ereignis_typ = ereignis.type
        if ereignis_typ == pg.MOUSEBUTTONDOWN or ereignis_typ == pg.MOUSEBUTTONUP:
            maus_feld = koordinaten_zu_feld(*pg.mouse.get_pos())
            if startfeld == () or maus_feld not in legale_zielfelder(startfeld):
                dorthinkannmanziehen = legale_zielfelder(maus_feld)
                if dorthinkannmanziehen:
                    startfeld = maus_feld
                zeichne_stellung(dorthinkannmanziehen)
            if maus_feld in legale_zielfelder(startfeld):
                mache_zug(startfeld, maus_feld)
                startfeld = ()
                dorthinkannmanziehen = []
                zeichne_stellung()
        elif ereignis_typ == pg.KEYDOWN and ereignis.key == pg.K_z:
            print("Zurück")
            nimm_zurueck()
            zeichne_stellung()
        if ereignis_typ == pg.QUIT:
            pg.quit()
            sys.exit()
