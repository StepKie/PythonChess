from ChessBoard import Move, Square, ChessBoard, FILE_NAMES
from ChessPiece import PieceType, Color, WHITE, KING, ChessPiece


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

