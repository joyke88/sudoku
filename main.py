"""
Programming Method:
  1. Backtracking is used to produce a valid Sudoku board with a single solution.
  2. As there is only one valid solution, the user input is compared to the generated board to determine if the win condition is met.
  3. Python is utilized for the game logic.
  4. Pygame is utilized for the game GUI.

Sudoku Rules:
  1. Every puzzle is randomly generated with exactly one correct solution and exactly 27 free clues.
  2. Each of the 9 sub-grids must contain the digits 1-9.
  3. Each number can only appear once in a row, column or sub-grid.

How to play:
  1. Expand the play window for the best experience.
  2. Select any cell by left clicking on it.
  3. Input digits with the number keys on your keyboard.
  4. Remove inputs with the delete key or backspace key.
  5. Toggle "Check" on when you have completed the game to see if you win.

Game features:
  1. "Solve" with automatically solve any blank or incorrect cells. Solved cells will be displayed in pink.
  2. "New" will generate a new random valid puzzle.
  3. "Hint" will give you a single additional clue. It will display the correct value for the first cell being blank or marked as breaking the Sudoku rule set.
  4. "Check" will display invalid duplicate's in a sub-grid, column, or row as red. If the cell is a valid input, it will be displayed as green.
  5. "Reset" will clear the puzzle to the beginning state.
"""

from pygameGuiClass import PygameGUI

if __name__ == "__main__":
    game = PygameGUI()
    game.run()

main()