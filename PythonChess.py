import sys

import pygame as pg

from BoardRenderer import BoardRenderer
from ChessBoard import ChessBoard
from GameManager import GameManager


class ChessGame:
    def __init__(self):
        # Initialize Pygame
        pg.init()
        pg.display.set_caption('SK Python Chess')
        
        # Create game objects
        self.chessboard = ChessBoard()
        self.renderer = BoardRenderer(self.chessboard)
        self.game_manager = GameManager(self.chessboard)
        self.start_square = None
        self.clock = pg.time.Clock()
        self.fps = 40

    def handle_events(self):
        for event in pg.event.get():
            # 1. Regular mouse clicks
            if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                mouse_field = self.renderer.coordinates_to_field(*mouse_pos)
                mouse_square = self.chessboard.get_square(*mouse_field)
                # 1a. no start_square set -> highlight fields
                if not self.start_square and event.type == pg.MOUSEBUTTONDOWN:
                    if highlighted_fields := self.chessboard.legal_moves_from(mouse_square):
                        self.start_square = mouse_square
                        self.renderer.draw_board(highlighted_fields)
                # 1b. start_square set and mouse square is valid chess move -> move
                elif event.type == pg.MOUSEBUTTONUP and self.start_square:
                    if mouse_square in [move.end_square for move in self.chessboard.legal_moves_from(self.start_square)]:
                        self.game_manager.exec_move(self.start_square, mouse_square)
                        self.start_square = None
                        self.renderer.draw_board()
                # 1c. clicked on start_square again -> reset
                elif event.type == pg.MOUSEBUTTONDOWN and mouse_square == self.start_square:
                    self.start_square = None
                    self.renderer.draw_board()
            # 2. Ctrl+Z -> Takeback
            elif event.type == pg.KEYDOWN and event.key == pg.K_z:
                self.game_manager.take_back()
                self.renderer.draw_board()
            # 3. Escape -> Quit
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run(self):
        self.renderer.draw_board()
        
        # Game loop
        while True:
            self.clock.tick(self.fps)
            self.handle_events()


if __name__ == "__main__":
    game = ChessGame()
    game.run()
