"""
Rules of SUDOKO:
    1.) Place a number of 1 to 9 in each cell
    2.) Ensure there are no duplicate digits in a row, in a column, or in a sub grid.
    3.) Complete every the puzzle without breaking the rule in step 2.

Game instructions:
    1.) Use the mouse to select a free cell
    2.) Use the number keys to input a digit
    3.) Use the delete or backspace keys to remove an input

Game features:
    1.) Automatically generates a random and valid suduko game
        a.) Each puzzle generated has exaclty 1 solution to ensure validity
        b.) Each puzzle generated has exactly 27 free hints given

    2.) The game includes an automatic solver.
        a.) Please note that the logic for solving the puzzle is in "sudokuBoardClass.py"
        b.) "pygameGuiClass.py" simply refers to a copy of the solved puzzle in order to avoid duplicate code.
        c.) For ease of grading, the solved board is printed to console, with the user input values marked red.

    3.) The game ensures validity of the users solution and displays "you win" upon clicking "check" with a complete puzzle.

    4.) The game enforces SUDOKU rules, which can be visually verified in real time with the "check button".

    5.) The game can provide a single hint at a time if stuck by clicking "hint"
        a.) The hint shows the correct value of the first cell breaking SUDOKU rules or equaling None

    6.) At any time you can randomly generate a new valid board by clicking "new"
"""

# References:
    # Backtracking: Back to Back SWE --> https://www.youtube.com/watch?v=JzONv5kaPJM
    # Rules on creating a valid board: https://www.sudokuwiki.org/Sudoku_Creation_and_Grading.pdf
    # Referenced pygame docs: https://www.pygame.org/docs/
    # Referenced A Plus Coding tutorials to help with pygame: https://www.youtube.com/watch?v=r_cmJBgrq5k&t=752s

from pygameGuiClass import PygameGUI

if __name__ == "__main__":
    game = PygameGUI()
    game.run()

main()