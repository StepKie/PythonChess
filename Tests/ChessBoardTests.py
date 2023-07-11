import pytest

from ChessBoard import ChessBoard, Square, Move
from ChessPiece import *
from GameManager import GameManager


@pytest.fixture
def chessboard():
    return ChessBoard()


def test_legal_moves_from(chessboard):
    b1 = next(sq for sq in chessboard.squares if str(sq) == "b1")
    legal_moves_for_nb1 = chessboard.legal_moves_from(b1)
    assert len(legal_moves_for_nb1) == 2


def test_legal_moves(chessboard):
    legal_moves_from_starting_position = chessboard.legal_moves()
    assert len(legal_moves_from_starting_position) == 20


def test_is_check(chessboard):
    game_manager = GameManager(chessboard)

    game_manager.make_move("e2", "e4")
    game_manager.make_move("d7", "d5")
    assert not chessboard.is_check()

    game_manager.make_move("f1", "b5")
    assert chessboard.is_check()


def test_is_mate(chessboard):
    game_manager = GameManager(chessboard)

    game_manager.make_move("f2", "f3"),
    game_manager.make_move("e7", "e6"),
    game_manager.make_move("g2", "g4"),
    game_manager.make_move("d8", "h4")

    assert chessboard.is_mate()
