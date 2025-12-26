from ChessBoard import ChessBoard, Move, Square
from ChessPiece import WHITE, BLACK
from typing import Optional


class GameManager:
    """Manages chess game flow including turns, move execution, and move history.
    
    Handles move validation, turn switching, and takeback functionality.
    """
    
    def __init__(self, chessboard: ChessBoard):
        self.chessboard = chessboard
        self.moves = []

    def switch_turn(self) -> None:
        self.chessboard.current_player = BLACK if self.chessboard.current_player == WHITE else WHITE

    def make_move(self, start: str, end: str) -> Move:
        start_square = self.chessboard.square(start)
        end_square = self.chessboard.square(end)
        return self.exec_move(start_square, end_square)

    # Hm. learning to use @singledispatch, @overload. None of these were particularly better than this on first try
    def exec_move(self, start_square: Square, end_square: Square) -> Move:
        move = Move(start_square, end_square)
        legal_moves = self.chessboard.legal_moves_from(start_square)
        if move.end_square not in [m.end_square for m in legal_moves]:
            raise ValueError(f"{move} is not a legal move")
        move.execute()
        self.moves.append(move)
        self.switch_turn()
        return move

    def take_back(self) -> Optional[Move]:
        if self.moves:
            last_move = self.moves.pop()
            last_move.undo()
            self.switch_turn()
            return last_move
        return None
