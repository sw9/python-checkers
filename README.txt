Group members:
Shichao Wang

Brief Description of Project Goals/Features:

For the final project, I made a checkers app that does move validation. For example, it will not allow you to move your piece into an already occupied square. It enforces the rule that if a jump is available, you have to take it. It detects when it's possible to make double jumps. It detects when to king a checkers piece. It also detects victory and defeat conditions. For example, you lose when no moves are available at all. You win when all of your opponents' pieces have been taken off the field

My checkers app includes a built in timer. This timer can be setup with a base period of time plus a bonus for each move made. Whomever runs out of time first loses. Some other features include the ability to ask for a draw. Just click the offer draw button, and the other player can agree to the draw during his/her turn.

Finally, it's possible to save the game to a JSON file and continue playing at a later date.

Instructions to run:
python3 checkers.py

Requirements Met:
  Custom class:
My custom class is in the checkersBackend.py file; it's the Piece class. This class represents the checkers pieces. The magic methods that I implemented were __ne__, __eq__, and __hash__. This allows me to create a map using variations of the Piece class as keys to their correponding icons.

  Three Modules:
    1 -> datetime module for the timer function
    2 -> json module for importing and exporting the game board, player names, time on the clock, and so on
    3 -> tkinter module for the gui

   Custom Decorator or Generator function:
   I have a custom decorator function called boundsCheck in the checkersBackend.py file. This decorator checks the output of other functions for positions that are outside of the boundaries of the 8x8 checkers board and removes these positions.
