from __future__ import annotations
import dataclasses
from typing import cast, Optional

PieceType = int
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = range(1, 7)
PIECE_SYMBOLS = [None, "p", "n", "b", "r", "q", "k"]
PIECE_NAMES = [None, "pawn", "knight", "bishop", "rook", "queen", "king"]

UNICODE_PIECE_SYMBOLS = {
    "R": "♖", "r": "♜",
    "N": "♘", "n": "♞",
    "B": "♗", "b": "♝",
    "Q": "♕", "q": "♛",
    "K": "♔", "k": "♚",
    "P": "♙", "p": "♟",
}

Color = bool
COLORS = [WHITE, BLACK] = [True, False]
COLOR_NAMES = ["black", "white"]


@dataclasses.dataclass
class ChessPiece:
    """A piece with type and color."""
    piece_type: PieceType
    color: Color

    def symbol(self) -> str:
        symbol = PIECE_SYMBOLS[self.piece_type]
        return symbol.upper() if self.color == WHITE else symbol

    def name(self) -> str:
        return cast(str, PIECE_NAMES[self.piece_type])

    def unicode_symbol(self, invert_color: bool = False) -> str:
        symbol = self.symbol().swapcase() if invert_color else self.symbol()
        return UNICODE_PIECE_SYMBOLS[symbol]

    def __hash__(self) -> int:
        return self.piece_type + (-1 if self.color else 5)

    def __repr__(self) -> str:
        return f"Piece.from_symbol({self.symbol()!r})"

    def __str__(self) -> str:
        return self.symbol()

    @classmethod
    def from_symbol(cls, symbol: str) -> Optional[ChessPiece]:
        return None if symbol.lower() not in PIECE_SYMBOLS \
            else cls(PIECE_SYMBOLS.index(symbol.lower()), symbol.isupper())
