
# import colors class to enable colors to console
from consoleColorsClass import ConsoleColors

# import random library to create random sudoku board
import random

"""
Generates random, valid, single solution SUDOKU puzzles and solves them.
"""
class SudokuBoard():
    """save player board, solved board, and fresh board states."""
    def __init__(self):
        self.player_board = self.__create_board()
        self.solved_board = []
        self.fresh_board = []
        self.solutions = 0

    """initialize the n * n board"""
    def __create_board(self):
        board = []
        for i in range(9):
            board.append([None] * 9)

        return board

    """initial generation of a random board"""
    def fill_board(self):
        # get the next empty cell to guess
        row, column = self.next_cell()

        choices = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # check if the puzzle has been completed
        if row == None:
            return True

        # make a random choice for current cell
        random.shuffle(choices)
        for choice in choices:

            # check if it is a legal choice
            if self.is_legal(row, column, choice):
                self.player_board[row][column] = choice

                # continue filling board with recursive call.
                if self.fill_board():
                    return True

            # if there were no legal moves in this cell, set it to none (back tracking)
            self.player_board[row][column] = None

        return

    """check if there are any un-filled cells"""
    def next_cell(self):
        # iterate rows
        for i in range(9):

            # iterate columns
            for j in range(9):

                # check values of cells
                if self.player_board[i][j] == None:
                    return i, j

        # if entire board is filled, returned none for i and j
        return None, None

    """checks the legality of each guess"""
    def is_legal(self, row, col, num):
        # check if num is in current row
        for i in range(9):
            if self.player_board[row][i] == num:
                return False

        # check if num is in current column
        for i in range(9):
            if self.player_board[i][col] == num:
                return False

        # determine the "sub grid" row and column on a 3 by 3 grid of sub grids
        sub_grid_row = (row // 3) * 3
        sub_grid_col = (col // 3) * 3

        # check if num is in current sub grid
        for i in range(3):
            for j in range(3):
                # check the value of each cell within the sub grid
                if self.player_board[sub_grid_row + i][sub_grid_col + j] == num:
                    return False
        return True

    """save a copy of the full board as solved board for reference to later"""
    def save_solved_board(self):

        # create empty rows
        for i in range(9):
            self.solved_board.append([])

            # insert column values into each row
            for j in range(9):
                self.solved_board[i].append(self.player_board[i][j])

        return

    """remove 54 clues for valid sudoku board"""
    def remove_clues(self):
        # initialize count
        removed = 0

        # Remove 54 random clues, leaving 27 on the board
        while removed < 54:

            # choose a random cell to remove
            row, column = random.randint(0,8), random.randint(0,8)

            # backup removed cell in case it needs to be re-inserted
            saved_clue = self.player_board[row][column]
            self.player_board[row][column] = None

            # initialize solutions to 0, and check amount of solutions at current step
            self.solutions = 0
            self.find_solutions()

            # if number of solutions = 1, continue. If not re-insert clue and try again.
            if self.solutions == 1:
                removed += 1
            else:
                self.player_board[row][column] = saved_clue

        return

    """solving a given board"""
    def find_solutions(self):

        # get the next empty cell to guess
        row, column = self.next_cell()

        # if row or column returned with a true value, the puzzle is complete.
        if row == None:
            return True

        # make a choice in the current cell
        for choice in range(1,10):

            # check if it is a legal choice
            if self.is_legal(row, column, choice):
                self.player_board[row][column] = choice

                # check if the puzzle was solved
                if self.find_solutions():
                    self.solutions += 1
                    break

        # back track to erase the solutions just discovered.
        self.player_board[row][column] = None

        return

    """save a fresh copy of the playable board"""
    def save_fresh_board(self):

        # create empty rows
        for i in range(9):
            self.fresh_board.append([])

            # insert column values into each row
            for j in range(9):
                self.fresh_board[i].append(self.player_board[i][j])

        return


    """check if puzzle is solved"""
    def check_if_solved(self):
        # iterate rows and columns checking solution against player attempt
        for i in range(9):
            for j in range(9):
                if self.solved_board[i][j] != self.player_board[i][j]:
                    return False

        return True

    """print sudoku board to console for testing purposes"""
    def print_sudoku(self):
        print(f'\n{ConsoleColors.YELLOW}---- INSTRUCTIONS ----{ConsoleColors.RESET}')
        print(f'  - Input a number 1 to 9 using the keyboard')
        print(f'  - Remove an input using backspace or delete keys')
        print(f'\n{ConsoleColors.YELLOW}---- SOLVED BOARD ----{ConsoleColors.RESET}')
        print(f'  - User input in {ConsoleColors.RED} RED {ConsoleColors.RESET}')
        print(f'  - Locked cells in {ConsoleColors.BOLD}WHITE{ConsoleColors.RESET}')

        # iterate printed rows
        for i in range(19):

            # minor row borders
            if i in [2,4,8,10,14,16]:
                print('+   ' * 9 + '+')
            # major row borders
            elif i in [0,6,12,18]:
                print('+---' * 9 + '+')
            else:

                # iterate printed columns
                for j in range(37):

                    # column borders
                    if j in [0,12,24,36]:
                        print('|', end = '')

                    # columns for number input
                    elif j in [2,6,10,14,18,22,26,30,34]:

                        # if the user must input the number, color it red
                        if self.fresh_board[int(i/2)][int(j/4)] == None:
                            print(f'{ConsoleColors.RED}{self.solved_board[int(i/2)][int(j/4)]}{ConsoleColors.RESET}', end = '')

                        # if the cell is locked, color it white
                        else:
                            print(f'{self.solved_board[int(i/2)][int(j/4)]}', end = '')

                    # digit buffer
                    else:
                        print(' ', end = '')
                print()

    """display board for testing"""
    def __repr__(self):
        return str(f'Player Board: \n{self.player_board}\n\n'
                   f'Solved Board: \n{self.solved_board}\n\n'
                   f'Fresh Board: \n{self.fresh_board}\n\n')
