import sys

import pygame as pg

from BoardRenderer import BoardRenderer
from ChessBoard import ChessBoard
from GameManager import GameManager


def handle_events():
    global start_square
    for event in pg.event.get():
        # 1. Regular mouse clicks
        if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
            mouse_pos = pg.mouse.get_pos()
            mouse_field = renderer.coordinates_to_field(*mouse_pos)
            mouse_square = chessboard.get_square(*mouse_field)
            # 1a. no start_square set -> highlight fields
            if not start_square and event.type == pg.MOUSEBUTTONDOWN:
                if highlighted_fields := chessboard.legal_moves_from(mouse_square):
                    start_square = mouse_square
                    renderer.draw_board(highlighted_fields)
            # 1b. start_square set and mouse square is valid chess move -> move
            elif event.type == pg.MOUSEBUTTONUP and start_square:
                if mouse_square in [move.end_square for move in chessboard.legal_moves_from(start_square)]:
                    game_manager.exec_move(start_square, mouse_square)
                    start_square = None
                    renderer.draw_board()
            # 1c. clicked on start_square again -> reset
            elif event.type == pg.MOUSEBUTTONDOWN and mouse_square == start_square:
                start_square = None
                renderer.draw_board()
        # 2. Ctrl+Z -> Takeback
        elif event.type == pg.KEYDOWN and event.key == pg.K_z:
            game_manager.take_back()
            renderer.draw_board()
        # 3. Escape -> Quit
        elif event.type == pg.QUIT:
            pg.quit()
            sys.exit()


FPS = 40

# Initialize Pygame
pg.init()
pg.display.set_caption('Philipps Schachprogramm')

# Create game objects
chessboard = ChessBoard()
renderer = BoardRenderer(chessboard)
game_manager = GameManager(chessboard)
start_square = ()

renderer.draw_board()

# Game loop
clock = pg.time.Clock()

while True:
    clock.tick(FPS)
    handle_events()
