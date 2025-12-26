from ChessBoard import Move, Square, ChessBoard, FILE_NAMES
from ChessPiece import PieceType, Color, WHITE, BLACK, KING, PAWN, ChessPiece


def create_move(board, start_square: Square, end_square: Square) -> Move:
    """Factory function to create appropriate move type based on board state.
    
    Handles special moves like en passant without polluting main game logic.
    
    Args:
        board: ChessBoard instance
        start_square: Starting square
        end_square: Target square
        
    Returns:
        Appropriate Move subclass (EnPassantMove, CastlingMove, or regular Move)
    """
    piece = start_square.piece
    
    # Check for en passant
    if piece.piece_type == PAWN and \
       end_square.piece is None and \
       start_square.file != end_square.file:
        # Diagonal pawn move to empty square = en passant
        captured_pawn_square = board.get_square(end_square.file, start_square.rank)
        return EnPassantMove(start_square, end_square, captured_pawn_square)
    
    # Regular move (castling would be handled here too when implemented)
    return Move(start_square, end_square)


def get_en_passant_square(board, pawn_file: int, pawn_rank: int, direction: int):
    """Check if en passant is available and return the target square.
    
    Args:
        board: ChessBoard instance
        pawn_file: File of the pawn attempting en passant
        pawn_rank: Rank of the pawn attempting en passant
        direction: Direction the pawn moves (1 for black, -1 for white)
        
    Returns:
        Target square for en passant capture, or None if not available
    """
    if not board.last_move or board.last_move.piece.piece_type != PAWN:
        return None
    
    # Check if last move was a two-square pawn advance
    rank_diff = abs(board.last_move.end_square.rank - board.last_move.start_square.rank)
    if rank_diff != 2:
        return None
    
    # Check if opponent's pawn is beside our pawn
    if abs(board.last_move.end_square.file - pawn_file) == 1 and \
       board.last_move.end_square.rank == pawn_rank:
        return board.get_square(board.last_move.end_square.file, pawn_rank + direction)
    
    return None


class CastlingMove(Move):
    def __init__(self, board: ChessBoard, type: ChessPiece):
        king_end_file = "g" if type.piece_type is KING else "c"
        rook_start_file = "h" if type.piece_type is KING else "a"
        rook_end_file = "f" if type.piece_type is KING else "d"
        rank = 1 if type.color is WHITE else 8

        self.move_king = Move(board.square(f"e{rank}"), board.square(f"{king_end_file}{rank}"))
        self.move_rook = Move(board.square(f"{rook_start_file}{rank}"), board.square(f"{rook_end_file}{rank}"))

    def execute(self):
        self.move_king.execute()
        self.move_rook.execute()

    def undo(self):
        self.move_king.undo()
        self.move_rook.undo()

    def __repr__(self) -> str:
        return super().__repr__() + repr(self.rook_start_square) + repr(self.rook_end_square)

    def __str__(self) -> str:
        return "0-0" if FILE_NAMES[self.move_king.end_square.file] == "g" else "0-0-0"


class EnPassantMove(Move):
    """Represents an en passant capture move.
    
    En passant allows a pawn to capture an opponent's pawn that just moved
    two squares forward from its starting position, as if it had only moved one square.
    """
    
    def __init__(self, start_square: Square, end_square: Square, captured_pawn_square: Square):
        super().__init__(start_square, end_square)
        self.captured_pawn_square = captured_pawn_square
        self.captured_pawn = captured_pawn_square.piece
    
    def execute(self):
        """Execute the en passant move, removing the captured pawn from its square."""
        self.start_square.piece = None
        self.end_square.piece = self.piece
        self.captured_pawn_square.piece = None
    
    def undo(self):
        """Undo the en passant move, restoring the captured pawn."""
        self.end_square.piece = None
        self.start_square.piece = self.piece
        self.captured_pawn_square.piece = self.captured_pawn
    
    def __str__(self) -> str:
        return f"{str(self.start_square)}x{str(self.end_square)} e.p."

