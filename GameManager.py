from operator import contains

from ChessBoard import ChessBoard, Move
from ChessPiece import WHITE, BLACK


# Currently, this class is hardly used, since most logic is in the ChessBoard. This may change as new functionality
# is added
class GameManager:
    def __init__(self, chessboard: ChessBoard):
        self.chessboard = chessboard
        self.moves = []

    def switch_turn(self):
        self.chessboard.current_player = BLACK if self.chessboard.current_player == WHITE else WHITE

    def make_move(self, start: str, end: str):
        start_square = self.chessboard.square(start)
        end_square = self.chessboard.square(end)
        return self.exec_move(start_square, end_square)

    # Hm. learning to use @singledispatch, @overload. None of these were particularly better than this on first try
    def exec_move(self, start_square, end_square):
        move = Move(start_square, end_square)
        if not str(move.end_square) in [str(x.end_square) for x in self.chessboard.legal_moves_from(start_square)]:
            raise ValueError(f"{move} is not a legal move")
        move.execute()
        self.moves.append(move)
        self.switch_turn()
        return move

    def take_back(self):
        if self.moves:
            last_move = self.moves.pop()
            last_move.undo()
            self.switch_turn()
            return last_move
        return None
