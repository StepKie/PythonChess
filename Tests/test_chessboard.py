"""Test suite for chess board functionality and game manager"""
import pytest

from ChessBoard import ChessBoard
from GameManager import GameManager


@pytest.fixture
def chessboard():
    return ChessBoard()


@pytest.fixture
def game_manager(chessboard):
    return GameManager(chessboard)


def test_legal_moves_from(chessboard):
    """Knight on b1 has 2 legal moves"""
    b1 = next(sq for sq in chessboard.squares if str(sq) == "b1")
    legal_moves_for_nb1 = chessboard.legal_moves_from(b1)
    assert len(legal_moves_for_nb1) == 2


def test_legal_moves(chessboard):
    """Initial position has 20 legal moves"""
    legal_moves_from_starting_position = chessboard.legal_moves()
    assert len(legal_moves_from_starting_position) == 20


def test_is_check(chessboard, game_manager):
    """Check detection works correctly"""
    game_manager.make_move("e2", "e4")
    game_manager.make_move("d7", "d5")
    assert not chessboard.is_check()

    game_manager.make_move("f1", "b5")
    assert chessboard.is_check()


def test_raises_on_illegal_move(chessboard):
    """Illegal moves raise ValueError"""
    with pytest.raises(ValueError):
        game_manager = GameManager(chessboard)
        game_manager.make_move("e2", "e5")


def test_is_mate(chessboard, game_manager):
    """Checkmate detection works correctly (fool's mate)"""
    game_manager.make_move("f2", "f3"),
    game_manager.make_move("e7", "e6"),
    game_manager.make_move("g2", "g4"),
    game_manager.make_move("d8", "h4")

    assert chessboard.is_mate()


def test_takeback(chessboard, game_manager):
    """Takeback works correctly"""
    game_manager.make_move("e2", "e4")
    game_manager.make_move("d7", "d5")
    game_manager.make_move("f1", "b5")
    
    last_move = game_manager.take_back()
    assert last_move is not None, "Should have returned a move"
    assert not chessboard.is_check(), "Should not be in check after takeback"


def test_stalemate(chessboard):
    """Stalemate detection works correctly"""
    # Set up stalemate position: White Kf6, Rg7, Black Kh8, black to move
    from ChessBoard import create_position, BLACK
    
    # FEN: 7k (black king on h8) / 6R1 (white rook on g7) / 5K2 (white king on f6)
    chessboard.squares = create_position("7k/6R1/5K2/8/8/8/8/8 w - - 0 1")
    chessboard.current_player = BLACK  # Black to move
    
    assert not chessboard.is_check(), "Should not be in check"
    assert chessboard.is_stalemate(), "Should be stalemate"
    assert chessboard.is_game_over(), "Should be game over"
