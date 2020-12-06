
# import additional classes
from sudokuBoardClass import SudokuBoard
from buttonClass import Button

# import pygame library for GUI
import sys, pygame as pg

"""
Class that displays the game GUI and does minor SUDUKO rule checks
"""
class PygameGUI():
    """initialize pygame"""
    def __init__(self):
        # initialize pygame
        pg.init()

        # initialize game window
        self.window_width = 495
        self.window_height = 600
        self.window = pg.display.set_mode((self.window_width, self.window_height))
        self.running = True

        # initialize colors as RGB for repl.it
        self.white = [255,255,255]
        self.black = [0,0,0]
        self.grey = [128,128,128]
        self.orange = [255, 165, 0]
        self.lime = [0, 255, 0]
        self.springgreen = [0, 255, 127]
        self.lightblue = [173,216,230]
        self.magenta = [255, 0, 255]
        self.darkmagenta = [139,0,139]
        self.lavender = [230,230,250]
        self.tomato = [255,99,71]
        self.plum = [221,160,221]
        self.paleturquoise = [175,238,238]
        self.coral = [255,127,80]

        # initialize game grid
        self.board = None
        self.new_board()
        self.grid_size = 405
        self.thick_border = 3
        self.cell_size = int(self.grid_size/9)
        self.grid_offset = (self.window_width - self.grid_size)/2
        self.grid_position = (self.grid_offset, self.grid_offset)
        self.thick_border_color = self.lightblue
        self.thin_border_color = self.grey
        self.cell_selected_color = self.orange
        self.cell_locked_color = self.lavender
        self.cell_wrong_color = self.tomato
        self.cell_correct_color = self.springgreen

        # initialize buttons
        self.off_button_color = self.lightblue
        self.on_button_color = self.darkmagenta
        self.off_button_hover = self.paleturquoise
        self.on_button_hover = self.plum
        self.playing_buttons = []
        self.play_again = []

        # initialize font
        self.font = pg.font.SysFont("arial", int(self.cell_size/2))
        self.default_font_color = self.black
        self.hint_font_color = self.lime
        self.solved_font_color = self.magenta
        self.button_off_font_color = self.black
        self.button_on_font_color = self.white

        # initialize state flags
        self.cells_locked = []
        self.cell_selected = None
        self.mouse_position = None
        self.game_state = "playing"
        self.complete = False
        self.win = False
        self.cell_changed = False
        self.incorrect_cells = []
        self.correct_cells = []
        self.solved_cells = []
        self.hint_cell = None

        # initialize game win
        self.win_circle_color = self.coral

        self.load()


    """
    Functions to manage game as it is running
    """

    """runs the GUI until quit"""
    def run(self):
        while self.running:
            if self.game_state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_display()
        pg.quit()
        sys.exit()

    """event listener during playing state"""
    def playing_events(self):
        # listening for quit event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            # listening for left click event
            if event.type == pg.MOUSEBUTTONDOWN:

                # find cell selected
                cell_selected = self.mouse_in_cell()
                if cell_selected:
                    self.cell_selected = cell_selected
                else:
                    self.cell_selected = None

                    # check if a play button is clicked
                    for button in self.playing_buttons:
                        if button.hover and self.win == False:
                            button.click()

                    # check if play again is clicked
                    for button in self.play_again:
                        if button.hover and self.win == True:
                            button.click()
                            self.playing_buttons[2].toggle = False

                    # remove hint cell when hint untoggled
                    if self.playing_buttons[1].toggle == False:
                        self.hint_cell = False

            # User types an input
            if event.type == pg.KEYDOWN:

                # only allow input in non locked cells
                if self.cell_selected != None and self.cell_selected not in self.cells_locked:

                    # allow inputs 1 to 9
                    if self.is_integer(event.unicode) and int(event.unicode) != 0:

                        # set player board cell value to input
                        self.board.player_board[self.cell_selected[0]][self.cell_selected[1]] = int(event.unicode)

                        # check if the cell is correct or not
                        self.check_cells()

                        self.remove_solved_cells()

                        # check if board complete is now true
                        self.board_complete()

                        # toggle hint button off when change is made
                        self.playing_buttons[1].toggle = False
                        self.hint_cell = None

                        # flag that a cell has changed
                        self.cell_changed = True

                    # allow user to clear input
                    elif event.key == pg.K_DELETE or event.key == pg.K_BACKSPACE:

                        # set player board cell value to None
                        self.complete = False
                        self.board.player_board[self.cell_selected[0]][self.cell_selected[1]] = None

                        # call cell check to remove from incorrect array if in array
                        self.check_cells()

                        self.remove_solved_cells()

                        # toggle hint button off when change is made
                        self.playing_buttons[1].toggle = False
                        self.hint_cell = None

                        # flag that a cell has changed
                        self.cell_changed = True

    """updating function during playing state"""
    def playing_update(self):
        # get the current mouse position
        self.mouse_position = pg.mouse.get_pos()

        # check if mouse is hovering over button
        if self.win == False:
            for button in self.playing_buttons:
                button.update(self.mouse_position)
        else:
            for button in self.play_again:
                button.update(self.mouse_position)


    """
    Functions to display the board as game is running
    """

    """generate a display window for game"""
    def playing_display(self):
        # set background to white
        self.window.fill(self.white)

        if self.win == False:
            # display each button in button array
            for play_button in self.playing_buttons:
                play_button.draw(self.window)
        else:
            for button in self.play_again:
                button.draw(self.window)

        # display locked cell over grid
        self.display_locked_cells()

        # display incorrect cells
        self.display_wrong_cells()

        # display grid over shaded cells
        self.display_grid()

        # display title over grid
        self.display_title()

        # display selected cell over locked cell
        if self.win == False:
            if self.cell_selected:
                self.draw_selected()

        # display numbers over selected cell
        self.display_numbers()

        # display win
        if self.incorrect_cells == [] and self.complete == True and self.playing_buttons[2].toggle == True:
            self.display_win()

        # update the display
        pg.display.update()

    """draw the grid on display screen"""
    def display_grid(self):
        # set grid position, size, and outer border
        pg.draw.rect(self.window, self.thick_border_color, (self.grid_position[0], self.grid_position[1], self.window_width -
                                            (self.window_width - self.grid_size), self.window_height -
                                            (self.window_height - self.grid_size)), self.thick_border)

        # draw each cell
        for i in range(9):

            # make inner lines thin
            if i % 3 != 0:

                # inner columns
                pg.draw.line(self.window, self.thin_border_color, (self.grid_position[0] + (i * self.cell_size), self.grid_position[1]),
                                (self.grid_position[0] + (i * self.cell_size), self.grid_position[1] + self.grid_size))

                # inner rows
                pg.draw.line(self.window, self.thin_border_color, (self.grid_position[0], self.grid_position[1] + (i * self.cell_size)),
                                 (self.grid_position[1] + self.grid_size, self.grid_position[1] + (i * self.cell_size)))

            # make sub-grid lines thick
            else:
                # sub-grid columns
                pg.draw.line(self.window, self.thick_border_color, (self.grid_position[0] + (i * self.cell_size), self.grid_position[1]),
                             (self.grid_position[0] + (i * self.cell_size), self.grid_position[1] + self.grid_size), self.thick_border)

                # sub-grid rows
                pg.draw.line(self.window, self.thick_border_color, (self.grid_position[0], self.grid_position[1] + (i * self.cell_size)),
                             (self.grid_position[1] + self.grid_size, self.grid_position[1] + (i * self.cell_size)), self.thick_border)

    """display window title text"""
    def display_title(self):
        # initialize font
        font = pg.font.SysFont("arial", 35, bold=1)
        text = font.render("SUDOKU", False, self.black)

        # determine text size
        text_width, text_height = text.get_size()

        # center the text on the circle
        x_cordinate = int((self.window_width - text_width) / 2)
        y_cordinate = int((self.grid_offset - text_height) / 2)

        # display text on screen
        self.window.blit(text, (x_cordinate, y_cordinate))

    """highlight the select cell"""
    def draw_selected(self):
        # Only allow non locked cells to be selected.
        if self.cell_selected not in self.cells_locked:
            pg.draw.rect(self.window, self.cell_selected_color, ((self.cell_selected[1] * self.cell_size) + self.grid_position[0],
                                                                (self.cell_selected[0] * self.cell_size) + self.grid_position[0],
                                                                self.cell_size, self.cell_size), 3)

    """determine if mouse click is on grid"""
    def mouse_in_cell(self):
        # if the game has been won
        if self.win == True:
            return False

        # if the mouse is higher than or to the left of the grid
        if self.mouse_position[0] < self.grid_position[1] or self.mouse_position[1] < self.grid_position[1]:
            return False

        # if the mouse is lower than or to the right of the grid
        if self.mouse_position[0] > self.grid_position[0] + self.grid_size \
            or self.mouse_position[1] > self.grid_position[1] + self.grid_size:
            return False

        # if we've made it here, we've clicked on the grid.
        # get index of column and row clicked
        row_clicked = int((self.mouse_position[1] - self.grid_position[0]) // self.cell_size)
        column_clicked = int((self.mouse_position[0] - self.grid_position[1])//self.cell_size)

        # return cell index clicked
        return ([row_clicked, column_clicked])

    """create button objects"""
    def create_buttons(self):
        # append button objects to the playing buttons array
        self.playing_buttons.append(Button(88, 40, self.grid_offset + 96, 520,
                                           self.off_button_color, self.off_button_color,
                                           self.off_button_hover, self.off_button_hover,
                                           self.button_off_font_color, self.button_off_font_color, "Reset",
                                           self.reset_board))

        self.playing_buttons.append(Button(88, 40, self.grid_offset + 35, 465,
                                           self.off_button_color, self.off_button_color,
                                           self.off_button_hover, self.off_button_hover,
                                           self.button_off_font_color, self.button_off_font_color, "Hint",
                                           self.display_hint))

        self.playing_buttons.append(Button(88, 40, self.grid_offset + 158, 465,
                                           self.off_button_color, self.on_button_color,
                                           self.off_button_hover, self.on_button_hover,
                                           self.button_off_font_color, self.button_on_font_color, "Check",
                                           self.check_cells))

        self.playing_buttons.append(Button(88, 40, self.grid_offset + 281, 465,
                                           self.off_button_color, self.off_button_color,
                                           self.off_button_hover, self.off_button_hover,
                                           self.button_off_font_color, self.button_off_font_color, "Solve",
                                           self.solve_board))

        self.playing_buttons.append(Button(88, 40, self.grid_offset + 221, 520,
                                           self.off_button_color, self.off_button_color,
                                           self.off_button_hover, self.off_button_hover,
                                           self.button_off_font_color, self.button_off_font_color, "New",
                                           self.new_board))

        self.play_again.append(Button(88, 40, self.grid_offset + 158, 465,
                                      self.off_button_color, self.off_button_color,
                                      self.off_button_hover, self.off_button_hover,
                                      self.button_off_font_color, self.button_off_font_color, "New",
                                      self.new_board))

    """display text on screen"""
    def display_digit(self, digit, position, font_color):
        font = self.font.render(digit, False, font_color)
        font_height = font.get_height()
        font_width = font.get_width()

        # center the font position in the cell
        position[0] += (self.cell_size - font_width)/2
        position[1] += (self.cell_size - font_height)/2
        self.window.blit(font, position)

    """display numbers on screen"""
    def display_numbers(self):
        # iterate through the generated suduko board.
        for i in range(9):
            for j in range(9):

                # use player board so we can see new numbers input
                number = self.board.player_board[i][j]

                # hint derives form solved board
                hint = self.board.solved_board[i][j]

                # skip None from player board, display hint from solved board, display solved in blue
                if number != None or [i,j] == self.hint_cell:

                    # determine cell the number will be displayed in
                        # first index pegs to a column, second index pegs to a row
                    cell_position = [(j * self.cell_size) + self.grid_position[0],
                                     (i * self.cell_size) + self.grid_position[1]]

                    if [i,j] == self.hint_cell:
                        if number != None:
                            self.display_digit(str(number), cell_position, self.default_font_color)
                        self.display_digit(str(hint), cell_position, self.hint_font_color)
                    elif [i,j] in self.solved_cells:
                        self.display_digit(str(number), cell_position, self.solved_font_color)
                    else:
                        self.display_digit(str(number), cell_position, self.default_font_color)

    """shade locked cells"""
    def display_locked_cells(self):
        for cell in self.cells_locked:

            # shade locked cells containing provided hints
            pg.draw.rect(self.window, self.cell_locked_color, ((cell[1] * self.cell_size) + self.grid_position[0],
                                                               (cell[0] * self.cell_size) + self.grid_position[1],
                                                               self.cell_size, self.cell_size))

    """check if user keyboard input is integer"""
    def is_integer(self, input):
        # if there is an error converting our input string to integer, return false
        try:
            int(input)
            return True
        except:
            return False

    """helper function for creating buttons"""
    def load(self):
        self.create_buttons()
        self.flag_locked_cells()

    """add locked cells to locked cells array"""
    def flag_locked_cells(self):
        # iterate original board
        for i in range(9):
            for j in range(9):
                number = self.board.fresh_board[i][j]

                # lock cells containing provided hints
                if number != None:
                    self.cells_locked.append([i,j])

    """when user requests, display hint"""
    def display_hint(self):
        # iterate array to determine the hint cell to be shown
        for i in range(9):
            for j in range(9):
                if self.board.player_board[i][j] == None or [i,j] in self.incorrect_cells:
                    self.hint_cell = [i,j]
                    return

    """
    this button solves the board
        * Please note that the puzzle solving logic is in "sudokuBoardClass.py"
            in order to avoid duplicate code, this function is simply checking 
            against a copy of the solved puzzle.
    """
    def solve_board(self):
        # reset toggle on buttons
        self.playing_buttons[1].toggle = False
        self.playing_buttons[2].toggle = False

        # iterate array
        for i in range(9):
            for j in range(9):

                #skip locked cells, correct cells, solved cells
                if [i,j] not in self.cells_locked \
                        and [i,j] not in self.solved_cells\
                        and self.board.player_board[i][j] != self.board.solved_board[i][j]:

                    # input correct values
                    self.board.player_board[i][j] = self.board.solved_board[i][j]

                    # add cell to solved cells array
                    self.solved_cells.append([i, j])

                    # remove incorrect cells from array
                    if [i,j] in self.incorrect_cells:
                        self.incorrect_cells.remove([i,j])

                    # add correct cells to array
                    if [i, j] not in self.correct_cells and [i,j] not in self.cells_locked:
                        self.correct_cells.append([i, j])


        # check that board is complete
        self.board_complete()

    """if cell is deleted or changed remove cell from solved"""
    def remove_solved_cells(self):
        if self.cell_selected in self.solved_cells:
            self.solved_cells.remove(self.cell_selected)

    """erase all user input"""
    def reset_board(self):
        # re-initialize playing states
        self.cell_selected = None
        self.complete = False
        self.win = False
        self.cell_changed = False
        self.incorrect_cells = []
        self.correct_cells = []
        self.solved_cells = []
        self.hint_cell = None

        # re-initialize button toggles
        for button in self.playing_buttons:
            button.toggle = False

        # iterate unlocked cells and set them to None
        for i in range(9):
           for j in range(9):
               if [i,j] not in self.cells_locked:
                   self.board.player_board[i][j] = None

    """generate a unique and valid board with a single solution"""
    def new_board(self):
        # initialize new game
        self.cells_locked = []
        self.cell_selected = None
        self.mouse_position = None
        self.game_state = "playing"
        self.complete = False
        self.win = False
        self.cell_changed = False
        self.incorrect_cells = []
        self.correct_cells = []
        self.solved_cells = []
        self.hint_cell = None

        # generate new board
        self.board = SudokuBoard()
        self.board.fill_board()
        self.board.save_solved_board()
        self.board.remove_clues()
        self.board.save_fresh_board()

        # initialize locked cells
        self.flag_locked_cells()

        # print new board to console
        self.board.print_sudoku()



    """
     Functions to verify user solutions
    """

    """check if the board is complete"""
    def board_complete(self):
        # iterate board to ensure no cells contain None
        for i in range(9):
            for j in range(9):
                if self.board.player_board[i][j] == None:

                    #set complete flag to false
                    self.complete = False
                    return False

        # set complete flag to true
        self.complete = True
        return True

    """on each user input, highlight all user input cells breaking sudoku rule set"""
    def check_cells(self):
        # reset hint toggle
        self.playing_buttons[1].toggle = False

        # iterate entire grid:
        for row in range(9):
            for column in range(9):

                # don't evaluate or change locked cells
                if [row, column] not in self.cells_locked:

                    #  If cell is not none, check if incorrect.
                    if self.board.player_board[row][column] != None:

                        # check if input is incorrect
                        if self.check_row(row,column) == False or \
                                self.check_column(row,column) == False or \
                                self.check_sub_grid(row,column) == False:

                            # if cell not in incorrect array, add it
                            if [row,column] not in self.incorrect_cells:
                                self.incorrect_cells.append([row, column])

                            # if cell in correct array, remove it
                            if [row,column] in self.correct_cells:
                                self.correct_cells.remove([row, column])

                        # if new input is correct
                        else:
                            # if cell in incorrect array, remove it
                            if [row, column] in self.incorrect_cells:
                                self.incorrect_cells.remove([row, column])

                            # if cell not in correct array, add it
                            if [row, column] not in self.correct_cells:
                                self.correct_cells.append([row, column])

                    # If cell is now None, remove from incorrect array and correct array.
                    else:
                        if [row, column] in self.incorrect_cells:
                            self.incorrect_cells.remove([row, column])

                        if [row, column] in self.correct_cells:
                            self.correct_cells.remove([row, column])

    """determines if player placement is valid within row"""
    def check_row(self, row, column):
        # iterate the columns in the row, skip current column
        for col in range(9):

            # skip the current cell column
            if col != column:

                # if player input exists in row, return false
                if self.board.player_board[row][col] == self.board.player_board[row][column]:
                    return False
        return True

    """determines if player placement is valid within column"""
    def check_column(self, row, column):
        # iterate the rows in the column, skip current row
        for r in range(9):

            # skip the current cell row
            if r != row:

                # if player input value exists in column, return false
                if self.board.player_board[r][column] == self.board.player_board[row][column]:
                    return False
        return True

    """determines if player placement is valid within subgrid"""
    def check_sub_grid(self, row, column):
        # determine the particular sub-grid on the sudoku board
        sub_grid_row = (row // 3) * 3
        sub_grid_col = (column // 3) * 3

        # check if num is in current sub grid
        for r in range(3):
            for col in range(3):

                # skip input cell
                if (sub_grid_row + r) != row and (sub_grid_col + col) != column:

                    # if player input exists in sub-grid return false
                    if self.board.player_board[sub_grid_row + r][sub_grid_col + col] == self.board.player_board[row][column]:
                        return False
        return True

    """shade incorrect cells cells"""
    def display_wrong_cells(self):
        # only display incorrect cells if the check button is toggled on
        if self.playing_buttons[2].toggle == True:
            for cell in self.incorrect_cells:

                # shade incorrect cells
                pg.draw.rect(self.window, self.cell_wrong_color, ((cell[1] * self.cell_size) + self.grid_position[0],
                                                                    (cell[0] * self.cell_size) + self.grid_position[1],
                                                                    self.cell_size, self.cell_size))

            for cell in self.correct_cells:

                # shade correct cells only
                if self.complete == False or self.incorrect_cells != []:
                    pg.draw.rect(self.window, self.cell_correct_color, ((cell[1] * self.cell_size) + self.grid_position[0],
                                                                    (cell[0] * self.cell_size) + self.grid_position[1],
                                                                    self.cell_size, self.cell_size))

    """display win if board is complete and correct"""
    def display_win(self):
        self.win = True

        # display win circle
        pg.draw.circle(self.window, self.win_circle_color, (int((self.grid_size/2) + int(self.grid_offset)),
                                            int((self.grid_size/2) + int(self.grid_offset))),int(self.window_width/4))

        # initialize font
        font = pg.font.SysFont("arial", 35, bold=1)
        text = font.render("You Win!", False, "white")

        # determine text size
        text_width, text_height = text.get_size()

        # center the text on the circle
        x_cordinate = int((self.grid_size + (2 * self.grid_offset) - text_width)/2)
        y_cordinate = int((self.grid_size + (2 * self.grid_offset) - text_height)/2)

        # display text on screen
        self.window.blit(text, (x_cordinate, y_cordinate))