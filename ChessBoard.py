from ChessPiece import *

FILE_NAMES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANK_NAMES = ["8", "7", "6", "5", "4", "3", "2", "1"]
SQUARE_NAMES = [f + r for r in RANK_NAMES for f in FILE_NAMES]
TARGET_SQUARE_STATES = [EMPTY_SQUARE, SAME_COLOR, OPPOSITE_COLOR] = range(1, 4)
# noinspection SpellCheckingInspection
FEN_INITIAL_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Square:

    def __init__(self, file: int, rank: int, piece: Optional[ChessPiece] = None):
        self.file = file  # 0=a, ..., 7=h
        self.rank = rank  # 0=8, ..., 7=1
        self.piece = piece

    def __str__(self) -> str:
        return FILE_NAMES[self.file] + RANK_NAMES[self.rank]

    def __repr__(self) -> str:
        return FILE_NAMES[self.file] + RANK_NAMES[self.rank]

    def status(self, color: Color):
        if self.piece is None:
            return EMPTY_SQUARE
        return SAME_COLOR if (color == self.piece.color) else OPPOSITE_COLOR


class Move:
    def __init__(self, start_square: Square, end_square):
        self.start_square = start_square
        self.end_square = end_square
        self.piece = self.start_square.piece
        self.captured_piece = self.end_square.piece

    def execute(self):
        if self.piece == ChessPiece(PAWN, WHITE) and self.end_square.rank == 0:
            final_piece = ChessPiece(QUEEN, WHITE)
        elif self.piece == ChessPiece(PAWN, BLACK) and self.end_square.rank == 7:
            final_piece = ChessPiece(QUEEN, BLACK)
        else:
            final_piece = self.piece

        self.start_square.piece = None
        self.end_square.piece = final_piece

    def undo(self):
        self.end_square.piece = self.captured_piece
        self.start_square.piece = self.piece

    def __repr__(self) -> str:
        return repr(self.start_square) + repr(self.end_square)


def create_position(fen: str):
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


class ChessBoard:
    def __init__(self):
        self.squares = create_position(FEN_INITIAL_POSITION)
        self.current_player = WHITE
        self.moves = []

    def get_square(self, file: int, rank: int):
        return self.squares[rank * 8 + file]

    def square(self, notation: str):
        return self.get_square(FILE_NAMES.index(notation[0]), RANK_NAMES.index(notation[1]))

    def is_check(self):
        for opponent_occupied_square in filter(lambda sq: sq.status(self.current_player) == OPPOSITE_COLOR,
                                               self.squares):
            for attacked_square in self.all_target_squares(opponent_occupied_square):
                if (piece := attacked_square.piece) is not None and piece.piece_type == KING:
                    return True
        return False

    def is_mate(self):
        return self.is_check() and not self.legal_moves()

    def legal_moves_from(self, from_square):
        legal_moves = []
        if from_square.status(self.current_player) == SAME_COLOR:
            for target_square in self.all_target_squares(from_square):
                candidate_move = Move(from_square, target_square)
                candidate_move.execute()
                # only add moves where the player does not end up in check
                if not self.is_check():
                    legal_moves.append(candidate_move)
                candidate_move.undo()
        return legal_moves

    def legal_moves(self):
        # list comprehension instead would be the following, readability debatable
        # return [move for square in self.squares for move in self.legal_moves_from(square)]
        legal_moves = []
        for square in self.squares:
            legal_moves += self.legal_moves_from(square)
        return legal_moves

    def all_target_squares(self, from_square: Square):
        moved_piece = from_square.piece
        if moved_piece is None:
            return []

        piece_type = moved_piece.piece_type
        piece_color = moved_piece.color

        straight_directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        diagonal_directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # up-left, up-right, down-right, down-left
        knight_directions = ((-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1))
        all_directions = straight_directions + diagonal_directions
        if piece_type == KNIGHT:
            return self.fields_in_direction(from_square, 1, knight_directions)
        if piece_type == BISHOP:
            return self.fields_in_direction(from_square, 7, diagonal_directions)
        if piece_type == ROOK:
            return self.fields_in_direction(from_square, 7, straight_directions)
        if piece_type == QUEEN:
            return self.fields_in_direction(from_square, 7, all_directions)
        # TODO castling
        if piece_type == KING:
            return self.fields_in_direction(from_square, 1, all_directions)
        target_squares = []
        # TODO en-passant
        from_file = from_square.file
        from_rank = from_square.rank
        if piece_type == PAWN:
            direction_row = (-1, 1)[piece_color == BLACK]
            starting_row = (6, 1)[piece_color == BLACK]
            rank_one_step = from_rank + direction_row
            rank_two_steps = from_rank + 2 * direction_row
            if self.get_square(from_file, rank_one_step).status(piece_color) == EMPTY_SQUARE:
                target_squares.append(self.get_square(from_file, rank_one_step))
                if from_rank == starting_row and self.get_square(from_file, rank_two_steps).status(
                        piece_color) == EMPTY_SQUARE:
                    target_squares.append(self.get_square(from_file, rank_two_steps))
            if from_file > 0 and self.get_square(from_file - 1, rank_one_step).status(piece_color) == OPPOSITE_COLOR:
                target_squares.append(self.get_square(from_file - 1, rank_one_step))
            if self.get_square(from_file + 1, rank_one_step).status(piece_color) == OPPOSITE_COLOR:
                target_squares.append(self.get_square(from_file + 1, rank_one_step))
        return target_squares

    def fields_in_direction(self, start_square: Square, max_distance, directions):
        target_squares = []
        from_color = start_square.piece.color
        for direction in directions:
            for i in range(1, max_distance + 1):
                end_file = start_square.file + direction[1] * i
                end_rank = start_square.rank + direction[0] * i
                if 0 <= end_rank <= 7 and 0 <= end_file <= 7:  # only within board bounds
                    target_square = self.get_square(end_file, end_rank)
                    target_square_status = target_square.status(from_color)
                    if target_square_status == SAME_COLOR:
                        break
                    target_squares.append(target_square)
                    if target_square_status == OPPOSITE_COLOR:
                        break
                else:
                    break
        return target_squares
