"""Chess board rendering using pygame.

Handles visual display of the chess board including:
- Board square colors and checkerboard pattern
- Piece image loading and scaling
- Move highlighting
- Coordinate conversion between chess notation and screen pixels
"""
import pygame as pg
import os
from typing import Dict, List, Tuple

WHITE = pg.Color("white")
BLACK = pg.Color("grey")
GREEN = pg.Color("darkgreen")

DEFAULT_FIELD_DIMENSION = 100
CHECKERBOARD_PATTERN = 2

PIECE_SYMBOL_TO_FILENAME = [('r', 'br'), ('n', 'bn'), ('b', 'bb'), ('q', 'bq'), ('k', 'bk'), ('p', 'bp'),
                            ('R', 'wr'), ('N', 'wn'), ('B', 'wb'), ('Q', 'wq'), ('K', 'wk'), ('P', 'wp')]


class BoardRenderer:
    """Handles rendering the chess board and pieces using pygame.
    
    Manages the visual display including board squares, piece images,
    and highlighted moves.
    """
    
    def __init__(self, chessboard, field_dimension: int = DEFAULT_FIELD_DIMENSION):
        self.chessboard = chessboard
        self.field_dimension = field_dimension
        board_dimension = field_dimension * 8
        self.screen = pg.display.set_mode((board_dimension, board_dimension))
        self.images = self.load_images()

    def draw_board(self, highlighted_moves: List = []) -> None:
        for square in self.chessboard.squares:
            color = BLACK if (square.file + square.rank) % CHECKERBOARD_PATTERN else WHITE
            if square in [move.end_square for move in highlighted_moves]:
                color = GREEN
            coordinate_x, coordinate_y = self.field_to_coordinates(square.file, square.rank)
            pg.draw.rect(self.screen, color, [coordinate_x, coordinate_y, self.field_dimension, self.field_dimension])
            if square.piece is not None:
                self.screen.blit(self.images[square.piece.symbol()], (coordinate_x, coordinate_y))
        pg.display.flip()

    def field_to_coordinates(self, file: int, rank: int) -> Tuple[int, int]:
        return file * self.field_dimension, rank * self.field_dimension

    def coordinates_to_field(self, coordinate_x: int, coordinate_y: int) -> Tuple[int, int]:
        return coordinate_x // self.field_dimension, coordinate_y // self.field_dimension

    def load_images(self) -> Dict[str, pg.Surface]:
        images = {}
        for piece, filename in PIECE_SYMBOL_TO_FILENAME:
            image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Figuren', filename + '.png')
            images[piece] = pg.transform.smoothscale(pg.image.load(image_path),
                                                     (self.field_dimension, self.field_dimension))
        return images
