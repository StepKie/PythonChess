# PythonChess

Minimal chess program with a pygame GUI. Originally a ninth-grade school assignment, extended with additional features.

## Project Structure

- `PythonChess.py` - Main entry point (pygame GUI app)
- `ChessBoard.py` - Core board logic, move generation, FEN support
- `ChessPiece.py` - Piece data structures
- `GameManager.py` - Game flow and move execution
- `SpecialMoves.py` - En passant, castling, promotion
- `BoardRenderer.py` - Pygame-based visual rendering
- `Tests/` - pytest test suite
- `Figuren/` - Chess piece PNG images

## Tech Stack

- Python 3.11+
- pygame for GUI
- pytest for tests
- Type hints and dataclasses throughout

## Commands

```bash
# Run the app
python PythonChess.py

# Run tests
pytest Tests/

# Run tests with verbose output
pytest Tests/ -v
```

## Conventions

- Standard Python naming: snake_case for functions/variables, PascalCase for classes
- Type hints used throughout
- One module per logical concern (board, pieces, rendering, game management, special moves)
- Tests in `Tests/` directory using pytest fixtures
- Default branch is `master`
