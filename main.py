"""
Sudoku Rules:
    1.) Every puzzle is randomly generated with exactly one correct solution and exactly 27 free clues.
    2.) Each of the 9 sub-grids must contain the digits 1-9.
    3.) Each number can only appear once in a row, column or sub-grid.

How to play:
    1.) Select any cell by left clicking on it.
    2.) Input digits with the number keys on your keyboard.
    3.) Remove inputs with the delete key or backspace key.
    4.) Toggle "Check" on when you have completed the game to see if you win.

Game features:
    1.) "Solve" with automatically solve any blank or incorrect cells. Solved cells will be displayed in pink.
        a.) Please note that the logic for solving the puzzle is in "sudokuBoardClass.py"
        b.) "pygameGuiClass.py" simply refers to a copy of the solved puzzle in order to avoid duplicate code.
        c.) For ease of grading, the solved board is printed to console, with the user input values marked red.
    2.)"New" will generate a new random valid puzzle.
    3.) "Hint" will give you a single additional clue. It will display the correct value for the first cell being blank or marked as breaking the Sudoku rule set.
    4.) "Check" will display invalid duplicate's in a sub-grid, column, or row as red. If the cell is a valid input, it will be displayed as green.
    5.) "Reset" will clear the puzzle to the beginning state.
"""

from pygameGuiClass import PygameGUI

if __name__ == "__main__":
    game = PygameGUI()
    game.run()

main()