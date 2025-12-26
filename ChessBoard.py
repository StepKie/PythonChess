"""Chess board representation and game logic.

This module contains the core chess engine including:
- Square and Move classes for representing board positions and moves
- ChessBoard class for managing game state and move generation
- Legal move calculation with check/checkmate/stalemate detection
- FEN position parsing for board setup
"""
from typing import List

from ChessPiece import *


FILE_NAMES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANK_NAMES = ["8", "7", "6", "5", "4", "3", "2", "1"]
SQUARE_NAMES = [f + r for r in RANK_NAMES for f in FILE_NAMES]
TARGET_SQUARE_STATES = [EMPTY_SQUARE, SAME_COLOR, OPPOSITE_COLOR] = range(1, 4)
# noinspection SpellCheckingInspection
FEN_INITIAL_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# Pawn starting ranks
WHITE_PAWN_START_RANK = 6
BLACK_PAWN_START_RANK = 1

# Promotion ranks
WHITE_PROMOTION_RANK = 0  # 8th rank (index 0)
BLACK_PROMOTION_RANK = 7  # 1st rank (index 7)

# Movement directions
STRAIGHT_DIRECTIONS = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
DIAGONAL_DIRECTIONS = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # up-left, up-right, down-right, down-left
KNIGHT_DIRECTIONS = ((-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1))
ALL_DIRECTIONS = STRAIGHT_DIRECTIONS + DIAGONAL_DIRECTIONS


class Square:
    """Represents a square on the chess board.
    
    Attributes:
        file: Column index (0=a, ..., 7=h)
        rank: Row index (0=8, ..., 7=1)
        piece: ChessPiece on this square, or None if empty
    """

    def __init__(self, file: int, rank: int, piece: Optional[ChessPiece] = None):
        self.file = file  # 0=a, ..., 7=h
        self.rank = rank  # 0=8, ..., 7=1
        self.piece = piece

    def __str__(self) -> str:
        return FILE_NAMES[self.file] + RANK_NAMES[self.rank]

    def __repr__(self) -> str:
        return f"Square({str(self)})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Square):
            return False
        return self.file == other.file and self.rank == other.rank
    
    def __hash__(self) -> int:
        return hash((self.file, self.rank))

    def status(self, color: Color):
        if self.piece is None:
            return EMPTY_SQUARE
        return SAME_COLOR if (color == self.piece.color) else OPPOSITE_COLOR


class Move:
    """Represents a chess move from one square to another.
    
    Handles move execution, undo, and pawn promotion.
    """
    
    def __init__(self, start_square: Square, end_square: Square):
        self.start_square = start_square
        self.end_square = end_square
        self.piece = self.start_square.piece
        self.captured_piece = self.end_square.piece
        # Track castling rights for future castling implementation
        self.removed_castling_rights = self.affected_castling_rights()


    def execute(self):
        """Execute the move, handling pawn promotion automatically."""
        # Check for pawn promotion
        if self.piece.piece_type == PAWN:
            if self.piece.color == WHITE and self.end_square.rank == WHITE_PROMOTION_RANK:
                final_piece = ChessPiece(QUEEN, WHITE)
            elif self.piece.color == BLACK and self.end_square.rank == BLACK_PROMOTION_RANK:
                final_piece = ChessPiece(QUEEN, BLACK)
            else:
                final_piece = self.piece
        else:
            final_piece = self.piece

        self.start_square.piece = None
        self.end_square.piece = final_piece
        self.removed_castling_rights = self.affected_castling_rights()

    def undo(self):
        self.end_square.piece = self.captured_piece
        self.start_square.piece = self.piece

    def __repr__(self) -> str:
        return repr(self.start_square) + repr(self.end_square)
    
    def __str__(self) -> str:
        """Return move in algebraic notation (e.g., 'e2e4')."""
        return str(self.start_square) + str(self.end_square)
    
    def __eq__(self, other) -> bool:
        """Compare moves based on start and end squares."""
        if not isinstance(other, Move):
            return False
        return (self.start_square == other.start_square and 
                self.end_square == other.end_square)
    
    def __hash__(self) -> int:
        """Hash based on start and end squares."""
        return hash((self.start_square, self.end_square))

    def affected_castling_rights(self):
        affected_rights = {
            (KING, WHITE): "KQ",
            (KING, BLACK): "kq",
            (ROOK, WHITE, "a1"): "Q",
            (ROOK, BLACK, "a8"): "q",
            (ROOK, WHITE, "h1"): "K",
            (ROOK, BLACK, "h8"): "k"
        }

        return affected_rights.get((self.piece, self.piece.color, str(self.start_square)), "")


def parse_fen_position(fen: str) -> List[Square]:
    """Parse FEN position string into list of squares.
    
    Args:
        fen: FEN string (only position part is used)
        
    Returns:
        List of 64 Square objects representing the board
    """
    fen_parts = fen.split("/")[:8]  # Split and truncate before the first space
    squares = []
    for rank_index, fen_rank in enumerate(fen_parts):
        file_index = 0
        for char in fen_rank:
            if char.isdigit():  # add as many empty squares as indicated by number
                num_empty_squares = int(char)
                squares.extend([Square(file_index + i, rank_index, piece=None) for i in range(num_empty_squares)])
                file_index += num_empty_squares
            else:
                piece = ChessPiece.from_symbol(char)
                squares.append(Square(file_index, rank_index, piece))
                file_index += 1
    return squares


def create_position(fen: str):
    """Create position from FEN string (deprecated, use parse_fen_position)."""
    return parse_fen_position(fen)


class ChessBoard:
    """Represents a chess board with pieces and game state.
    
    Manages board state, move generation, and game rules like check and checkmate.
    """
    
    def __init__(self):
        self.squares = create_position(FEN_INITIAL_POSITION)
        self.current_player = WHITE
        self.moves = []
    
    @property
    def opponent_color(self) -> Color:
        """Get the opponent's color."""
        return BLACK if self.current_player == WHITE else WHITE
    
    def copy(self):
        """Create a deep copy of the board."""
        import copy
        return copy.deepcopy(self)

    def get_square(self, file: int, rank: int):
        return self.squares[rank * 8 + file]
    
    def is_within_bounds(self, file: int, rank: int) -> bool:
        """Check if file and rank are within board boundaries."""
        return 0 <= file <= 7 and 0 <= rank <= 7

    def square(self, notation: str):
        """Get square from algebraic notation (e.g., 'e4').
        
        Raises:
            ValueError: If notation is invalid or out of bounds
        """
        if len(notation) != 2:
            raise ValueError(f"Invalid notation '{notation}': must be exactly 2 characters (e.g., 'e4')")
        
        file_char, rank_char = notation[0], notation[1]
        
        if file_char not in FILE_NAMES:
            raise ValueError(f"Invalid file '{file_char}': must be a-h")
        if rank_char not in RANK_NAMES:
            raise ValueError(f"Invalid rank '{rank_char}': must be 1-8")
        
        return self.get_square(FILE_NAMES.index(file_char), RANK_NAMES.index(rank_char))

    def get_attacked_squares(self) -> List[Square]:
        """Get all squares attacked by the opponent's pieces."""
        attacked = []
        for square in self.squares:
            if square.status(self.current_player) == OPPOSITE_COLOR:
                attacked.extend(self.all_target_squares(square))
        return attacked

    def is_check(self):
        """Check if the current player's king is under attack."""
        return any(
            attacked_square.piece.piece_type == KING
            for attacked_square in self.get_attacked_squares()
            if attacked_square.piece is not None
        )

    def is_mate(self):
        """Check if the current player is in checkmate."""
        return self.is_check() and not self.legal_moves()
    
    def is_stalemate(self):
        """Check if the current player is in stalemate (no legal moves but not in check)."""
        return not self.is_check() and not self.legal_moves()
    
    def is_game_over(self):
        """Check if the game is over (checkmate or stalemate)."""
        return not self.legal_moves()
    
    def to_fen(self) -> str:
        """Export current board position to FEN notation.
        
        Returns basic position part only (doesn't include move counters or castling rights yet).
        """
        fen_parts = []
        for rank in range(8):
            empty_count = 0
            rank_str = ""
            for file in range(8):
                square = self.get_square(file, rank)
                if square.piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        rank_str += str(empty_count)
                        empty_count = 0
                    rank_str += square.piece.symbol()
            if empty_count > 0:
                rank_str += str(empty_count)
            fen_parts.append(rank_str)
        
        position = "/".join(fen_parts)
        active_color = "w" if self.current_player else "b"
        return f"{position} {active_color} - - 0 1"
    
    def has_insufficient_material(self) -> bool:
        """Check if the position has insufficient material for checkmate.
        
        Returns True for:
        - King vs King
        - King and Bishop vs King
        - King and Knight vs King
        - King and Bishop vs King and Bishop (same color bishops)
        """
        pieces = [sq.piece for sq in self.squares if sq.piece is not None]
        
        # Count pieces by type and color
        white_pieces = [p for p in pieces if p.color == WHITE]
        black_pieces = [p for p in pieces if p.color == BLACK]
        
        # King vs King
        if len(pieces) == 2:
            return True
        
        # King and minor piece vs King
        if len(pieces) == 3:
            minor_pieces = [p for p in pieces if p.piece_type in (KNIGHT, BISHOP)]
            return len(minor_pieces) == 1
        
        # King and Bishop vs King and Bishop (same color squares)
        if len(pieces) == 4:
            bishops = [sq for sq in self.squares if sq.piece and sq.piece.piece_type == BISHOP]
            if len(bishops) == 2:
                # Bishops on same color squares (sum of coordinates is even or odd)
                return (bishops[0].file + bishops[0].rank) % 2 == (bishops[1].file + bishops[1].rank) % 2
        
        return False

    def legal_moves_from(self, from_square):
        """Get all legal moves from a given square."""
        legal_moves = []
        if from_square.status(self.current_player) == SAME_COLOR:
            for target_square in self.all_target_squares(from_square):
                candidate_move = Move(from_square, target_square)
                if self.is_legal(candidate_move):
                    legal_moves.append(candidate_move)
        return legal_moves

    def is_legal(self, move: Move) -> bool:
        """Check if a move is legal by executing it, checking for check, then undoing it."""
        # TODO: Add special castling validation when castling is implemented
        move.execute()
        is_valid = not self.is_check()
        move.undo()
        return is_valid

    def legal_moves(self):
        """Get all legal moves for the current player."""
        return [move for square in self.squares for move in self.legal_moves_from(square)]

    def all_target_squares(self, from_square: Square):
        moved_piece = from_square.piece
        if moved_piece is None:
            return []
        piece_type = moved_piece.piece_type
        movements = {
            KNIGHT: (1, KNIGHT_DIRECTIONS),
            BISHOP: (7, DIAGONAL_DIRECTIONS),
            ROOK: (7, STRAIGHT_DIRECTIONS),
            QUEEN: (7, ALL_DIRECTIONS),
            KING: (1, ALL_DIRECTIONS)
        }
        # TODO castling
        return self.fields_in_direction(from_square, *movements[piece_type]) if piece_type != PAWN else \
            self.pawn_squares(from_square)

    def pawn_squares(self, from_square):
        target_squares = []
        # TODO en-passant
        from_file = from_square.file
        from_rank = from_square.rank
        piece_color = from_square.piece.color

        direction_row = 1 if piece_color == BLACK else -1
        starting_row = BLACK_PAWN_START_RANK if piece_color == BLACK else WHITE_PAWN_START_RANK
        one_square_forward = self.get_square(from_file, from_rank + direction_row)
        two_squares_forward = self.get_square(from_file, from_rank + 2 * direction_row)
        left_diagonal = self.get_square(from_file - 1, from_rank + direction_row)
        right_diagonal = self.get_square(from_file + 1, from_rank + direction_row)
        if one_square_forward.status(piece_color) == EMPTY_SQUARE:
            target_squares.append(one_square_forward)
            if from_rank == starting_row and two_squares_forward.status(piece_color) == EMPTY_SQUARE:
                target_squares.append(two_squares_forward)
        if from_file > 0 and left_diagonal.status(piece_color) == OPPOSITE_COLOR:
            target_squares.append(left_diagonal)
        if from_file < 7 and right_diagonal.status(piece_color) == OPPOSITE_COLOR:
            target_squares.append(right_diagonal)
        return target_squares

    def fields_in_direction(self, start_square: Square, max_distance, directions):
        target_squares = []
        from_color = start_square.piece.color
        for direction in directions:
            for i in range(1, max_distance + 1):
                end_file = start_square.file + direction[1] * i
                end_rank = start_square.rank + direction[0] * i
                if not self.is_within_bounds(end_file, end_rank):
                    break
                target_square = self.get_square(end_file, end_rank)
                target_square_status = target_square.status(from_color)
                if target_square_status == SAME_COLOR:
                    break
                target_squares.append(target_square)
                if target_square_status == OPPOSITE_COLOR:
                    break
        return target_squares