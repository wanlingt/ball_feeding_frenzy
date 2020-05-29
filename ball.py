import tkinter as tk
import random

CANVAS_WIDTH = 600      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 600     # Height of drawing canvas in pixels
COLOURS = ["azure", "blanched almond", "peach puff", "navajo white", "lemon chiffon", "lavender",
          "lavender blush", "misty rose", "dark slate gray", "pale turquoise", "sea green", "indian red",
          "salmon", "light salmon", "coral1", "light pink", "CadetBlue1", "PaleVioletRed1", "SteelBlue1",
           "dark sea green", "darkslateblue"]

class Ball:
    def __init__(self, canvas, colour_id, size):
        # self.canvas = canvas
        x0_choice = [0, CANVAS_WIDTH - size - 1]
        y0 = random.uniform(0, CANVAS_HEIGHT - size)
        x0 = random.choice(x0_choice)
        self.shape = canvas.create_oval(x0, y0, x0 + size, y0 + size, fill = COLOURS[colour_id],
                                        outline = COLOURS[colour_id])
        self.dx = random.randrange(1, 5)
        self.dy = 0

    def move(self, canvas):
        canvas.move(self.shape, self.dx, self.dy)
        if hit_left_wall(canvas, self.shape) or hit_right_wall(canvas, self.shape):
            self.dx *= -1
        if hit_top_wall(canvas, self.shape) or hit_bottom_wall(canvas, self.shape):
            self.dy *= -1


def hit_left_wall(canvas, shape):
    return get_left_x(canvas, shape) <= 0

def hit_top_wall(canvas, shape):
    return get_top_y(canvas, shape) <= 0

def hit_right_wall(canvas, shape):
    return get_right_x(canvas, shape) >= CANVAS_WIDTH

def hit_bottom_wall(canvas, shape):
    return get_bottom_y(canvas, shape) >= CANVAS_HEIGHT


######## These helper methods use "lists" ###########

def get_left_x(canvas, shape):
    return canvas.coords(shape)[0]

def get_top_y(canvas, shape):
    return canvas.coords(shape)[1]

def get_right_x(canvas, shape):
    return canvas.coords(shape)[2]

def get_bottom_y(canvas, shape):
    return canvas.coords(shape)[3]
