"""Game flow management for chess games.

Handles turn management, move execution with validation,
move history, and takeback functionality.
"""
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
        from SpecialMoves import create_move
        
        # Validate piece ownership and get legal moves
        legal_moves = self.chessboard.legal_moves_from(start_square)
        
        # Create the appropriate move type (handles special moves like en passant)
        move = create_move(self.chessboard, start_square, end_square)
        
        # Check if this specific move is legal
        if move not in legal_moves:
            piece_name = start_square.piece.name() if start_square.piece else "empty square"
            legal_destinations = ", ".join(str(m.end_square) for m in legal_moves) if legal_moves else "none"
            raise ValueError(
                f"Illegal move: {piece_name} on {start_square} cannot move to {end_square}. "
                f"Legal moves: {legal_destinations}"
            )
        
        move.execute()
        self.chessboard.last_move = move
        self.moves.append(move)
        self.switch_turn()
        return move

    def take_back(self) -> Optional[Move]:
        if self.moves:
            last_move = self.moves.pop()
            last_move.undo()
            # Update last_move on board
            self.chessboard.last_move = self.moves[-1] if self.moves else None
            self.switch_turn()
            return last_move
        return None
