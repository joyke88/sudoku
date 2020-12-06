# pygame library for GUI
import pygame as pg

"""
Allow button objects to be created
"""
class Button:
    def __init__(self, width, height, x_cordinate, y_cordinate, off_color, on_color, off_hover, on_hover,
                 off_text_color, on_text_color, text = None, function = None):
        # initialize button class
        self.image = pg.Surface((width, height))
        self.btn_position = (x_cordinate, y_cordinate)
        self.rectangle = self.image.get_rect()
        self.rectangle.topleft = self.btn_position
        self.width = width
        self.height = height
        self.text = text
        self.off_color = off_color
        self.on_color = on_color
        self.off_text_color =  off_text_color
        self.on_text_color = on_text_color
        self.off_hover = off_hover
        self.on_hover = on_hover
        self.function = function
        self.hover = False
        self.button_text_color = "black"
        self.win_button_text_color = "white"
        self.toggle = False

    """update button color based on hover status"""
    def update(self, mouse_position):
        if self.rectangle.collidepoint(mouse_position):
            self.hover = True
        else:
            self.hover = False

    """display button"""
    def draw(self, window):

        # determine hover color
        if self.hover:
            if self.toggle:
                self.image.fill(self.on_hover)
            else:
                self.image.fill(self.off_hover)

        # determine base color depending on toggle status
        else:
            if self.toggle:
                self.image.fill(self.on_color)
            else:
                self.image.fill(self.off_color)

        # display text
        if self.text:
            self.display_text(self.text)

        # display button on screen
        window.blit(self.image, self.btn_position)

    """click functionality"""
    def click(self):

        # alternate the button toggle on each click
        if self.toggle:
            self.toggle = False
        else:
            self.toggle = True


        self.function()

    """display button text"""
    def display_text(self, text):
        # initialize font
        font = pg.font.SysFont("arial", 15, bold=1)

        # determine font color on toggle
        if self.toggle:
            text = font.render(text, False, self.on_text_color)
        else:
            text = font.render(text, False, self.off_text_color)

        # determine text size
        text_width, text_height = text.get_size()

        # center the text on the button
        x_cordinate = int((self.width - text_width)/2)
        y_cordinate = int((self.height - text_height)/2)

        # display text on screen
        self.image.blit(text, (x_cordinate, y_cordinate))

