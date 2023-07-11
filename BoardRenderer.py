import pygame as pg
import os

WHITE = pg.Color("white")
BLACK = pg.Color("grey")
GREEN = pg.Color("darkgreen")

DEFAULT_FIELD_DIMENSION = 100

PIECE_SYMBOL_TO_FILENAME = [('r', 'br'), ('n', 'bn'), ('b', 'bb'), ('q', 'bq'), ('k', 'bk'), ('p', 'bp'),
                            ('R', 'wr'), ('N', 'wn'), ('B', 'wb'), ('Q', 'wq'), ('K', 'wk'), ('P', 'wp')]


class BoardRenderer:
    def __init__(self, chessboard, field_dimension=DEFAULT_FIELD_DIMENSION):
        self.chessboard = chessboard
        self.field_dimension = field_dimension
        board_dimension = field_dimension * 8
        self.screen = pg.display.set_mode((board_dimension, board_dimension))
        self.images = self.load_images()

    def draw_board(self, highlighted_moves=[]):
        for square in self.chessboard.squares:
            color = BLACK if (square.file + square.rank) % 2 else WHITE
            if square in [move.end_square for move in highlighted_moves]:
                color = GREEN
            koordinate_x, koordinate_y = self.field_to_coordinates(square.file, square.rank)
            pg.draw.rect(self.screen, color, [koordinate_x, koordinate_y, self.field_dimension, self.field_dimension])
            if square.piece is not None:
                self.screen.blit(self.images[square.piece.symbol()], (koordinate_x, koordinate_y))
        pg.display.flip()

    def field_to_coordinates(self, file, rank):
        return file * self.field_dimension, rank * self.field_dimension

    def coordinates_to_field(self, coordinate_x, coordinate_y):
        return coordinate_x // self.field_dimension, coordinate_y // self.field_dimension

    def load_images(self):
        images = {}
        for piece, filename in PIECE_SYMBOL_TO_FILENAME:
            image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figuren', filename + '.png')
            images[piece] = pg.transform.smoothscale(pg.image.load(image_path),
                                                     (self.field_dimension, self.field_dimension))
        return images
