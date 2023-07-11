# About

This is a minimal chess program for a school assignment created in collaboration with a 13-year-old student.
Hence, for comprehension purposes, most variables etc. are in German.

## Some TODOs as proposed by ChatGPT

Refactor the main game loop:

Extract the main game loop into a separate function, such as run_game(), and call it from the bottom of the script.
Move the event handling code into its own function, such as handle_events(), to handle different types of events.
Split the event handling code based on event types (e.g., mouse events, key events, quit event) and delegate to appropriate functions for each event type.
This will make your code more modular and easier to understand.
Use a chessboard class:

Create a Chessboard class that represents the game board and encapsulates the logic related to the board.
Move functions like feld_zu_koordinaten(), koordinaten_zu_feld(), and zeichne_stellung() into methods of the Chessboard class.
This will encapsulate the board-related functionality and improve code organization.
Use a Piece class:

Create a Piece class to represent chess pieces.
Move functions like figur_auf(), ist_gegnerische_figur(), and ist_eigene_figur() into methods of the Piece class.
This will encapsulate piece-related functionality and make the code more object-oriented.
Use a Move class:

Instead of storing moves as tuples (von, nach, figur, zielfeldfigur), create a Move class to represent moves.
The Move class can have attributes like start_pos, end_pos, piece, captured_piece, etc.
This will make the code more readable and allow for easier manipulation of moves.
Refactor the move generation code:

Move the move generation logic into a separate function, such as generate_moves(), that takes a position and returns a list of legal moves.
Consider implementing move generation for each piece type separately using methods in the Piece class.
This will improve code organization and make it easier to extend and modify move generation logic.
Implement a BoardRenderer class:

Create a BoardRenderer class responsible for rendering the chessboard and pieces on the screen.
Move the code related to loading the images of the pieces and drawing the board into methods of the BoardRenderer class.
This will separate the rendering concerns from the game logic and make the code more modular.
Implement an UndoManager class:

Create an UndoManager class to manage the undo functionality.
Move the code related to undoing moves into methods of the UndoManager class.
This will encapsulate the undo logic and make it easier to manage and track moves.
