"""
File: finalproject.py
----------------
Final Project
Adapted from the game Feeding Frenzy
Hit smaller shapes to grow in size, the game ends when you hit a larger shape
"""

import tkinter as tk
import time
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from ball import Ball
import sys
import os


CANVAS_WIDTH = 600 # Width of drawing canvas in pixels
CANVAS_HEIGHT = 600 # Height of drawing canvas in pixels
BALL_SIZE = 50
SIZE_FACTOR = 1.1 # Size that the main ball should increase by every time it hits a smaller ball
NO_OF_SMALLER_BALLS = 8
NO_OF_LARGER_BALLS = 8
COLOURS = ["azure", "blanched almond", "peach puff", "navajo white", "lemon chiffon", "lavender",
          "lavender blush", "misty rose", "dark slate gray", "pale turquoise", "sea green", "indian red",
          "salmon", "light salmon", "coral1", "light pink", "CadetBlue1", "PaleVioletRed1", "SteelBlue1",
           "dark sea green", "darkslateblue"]


def main():
    # Create canvas
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, "Ball Feeding Frenzy", "black")

    # Starter message
    display_label(canvas, "Starting in \n 3", 1)
    display_label(canvas, "Starting in \n 2", 1)
    display_label(canvas, "Starting in \n 1", 1)

    # Create main ball
    main_ball = canvas.create_oval(0, 0, BALL_SIZE, BALL_SIZE, fill="DeepPink3", outline = "old lace", width = 2)

    # Create other balls in game
    smaller_balls = []
    larger_balls = []

    for i in range(NO_OF_SMALLER_BALLS):
        # number of smaller balls
        colour_id = random.randint(0, len(COLOURS) - 1)
        size = random.randint(5, BALL_SIZE)
        smaller_balls.append(Ball(canvas, colour_id, size))

    for i in range(NO_OF_LARGER_BALLS):
        # number of larger balls
        colour_id = random.randint(0, len(COLOURS) - 1)
        size = random.randint(BALL_SIZE, 2 * BALL_SIZE)
        larger_balls.append(Ball(canvas, colour_id, size))

    ball_sizes = smaller_balls + larger_balls
    all_shapes = canvas.find_overlapping(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
    number_of_original_shapes = len(all_shapes)

    # Link the shape ID to the balls created using a dictionary
    keys = []
    for shape in all_shapes:
        if shape != 1:
            keys.append(shape)
    shape_dict = dict(zip(keys, ball_sizes))

    large_shapes_hit = []

    scoreboard = create_scoreboard(canvas)

    while True:
        mouse_x = canvas.winfo_pointerx()
        mouse_y = canvas.winfo_pointery()
        canvas.moveto(main_ball, mouse_x, mouse_y)

        other_balls = list(shape_dict.values())
        # Get number of shapes hit
        shapes_hit = (number_of_original_shapes) - len(other_balls) - 1
        shapes_left = number_of_original_shapes - shapes_hit
        
        for ball in other_balls:
            ball.move(canvas)

        # Actions that occur when the main shape comes into contact with other shapes
        hit_shape(canvas, main_ball, other_balls, shape_dict, shapes_hit, large_shapes_hit)

        # Update the scoreboard
        update_scores(canvas, shapes_hit, scoreboard)
        end_game_message(canvas, shapes_left, shapes_hit, large_shapes_hit, other_balls)


        # redraw canvas
        canvas.update()
        # pause
        time.sleep(1 / 50.) # Time to hold each frame; reducing this time reduces the ball"s speed

    canvas.mainloop()

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

def restart_button(canvas, display_time):
    restart_btn = tk.Button(canvas, text = "Restart", command = restart_program(), bg = "white")
    restart_btn.place(x = CANVAS_WIDTH / 2, y = CANVAS_HEIGHT / 2, anchor = CENTER)
    time.sleep(display_time)
    canvas.update()
    restart_btn.place_forget()
    canvas.update()

def display_label(canvas, message, display_time):
    """
    Function to display introductory messages on screen before the start of the game
    """
    widget = tk.Label(canvas, text=message, fg="pink", bg="black",
                      font=("arial", 20, "bold"))
    widget.place(relx=0.5, rely=0.5, anchor="center")
    canvas.update()
    time.sleep(display_time)
    widget.place_forget()
    canvas.update()

def create_scoreboard(canvas):
    scoreboard = canvas.create_text(10, 10, text = "Score: 0", fill = "pink", anchor = tk.NW,
                                    font = ("arial", "15", "bold"))
    return scoreboard

def update_scores(canvas, shapes_hit, scoreboard):
    canvas.itemconfig(scoreboard, text = "Score: " + str(shapes_hit))

def end_game_message(canvas, shapes_left, shapes_hit, large_shapes_hit, other_shapes):
    """Displays different end game messages depending on whether all shapes were hit"""

    # Not all shapes were hit
    if len(large_shapes_hit) == 1:
        for shape in other_shapes:
            canvas.delete(shape)
        black_screen = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill="black", width=0)
        end_game_text = canvas.create_text(CANVAS_WIDTH / 2,
                                           CANVAS_HEIGHT / 2,
                                           fill="pink",
                                           text="GAME OVER \n You hit " + str(shapes_hit) + " shapes",
                                           justify=tk.CENTER)
        return True
    # All shapes were hit
    elif shapes_left == 1:
        end_screen = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill="black", width=0)
        end_screen_text = canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2,
                                             text = "Congrats! You've cleared all the shapes. \n "
                                                    "Total shapes hit = " + str(shapes_hit), fill = "pink"
                                             , justify = tk.CENTER)
        return True

def hit_shape(canvas, main_shape, other_shapes_list, shape_dict, shapes_hit, large_shapes_hit):
    """
    Defines what happens to the main shape when it comes into contact with other shapes of different sizes
    Touching a:
    Smaller shape will cause the main shape to increase in size
    Larger shape will end the game
    """
    # get coordinates of main shape
    main_shape_coords = canvas.coords(main_shape)
    x1 = main_shape_coords[0]
    y1 = main_shape_coords[1]
    x2 = main_shape_coords[2]
    y2 = main_shape_coords[3]
    overlapping_shapes_list = canvas.find_overlapping(x1, y1, x2, y2)

    # delete object if it is smaller than the main shape
    for shape in overlapping_shapes_list:
        if shape != main_shape:
            if area(canvas, main_shape) >= area(canvas, shape):
                # Remove shape that was hit
                canvas.delete(shape)
                del shape_dict[shape]

                # Increase size of main shape
                increase_size(canvas, main_shape)
                # canvas.itemconfig(main_shape, fill="pink", outline = "DeepPink3", width = 2)

            else:
                large_shapes_hit.append(shape)
                break

    return

def increase_size(canvas, shape):
    """Increase size of the shape by the size factor"""
    x1, y1, x2, y2 = canvas.coords(shape)
    x1 *= SIZE_FACTOR
    y1 *= SIZE_FACTOR
    x2 *= SIZE_FACTOR
    y2 *= SIZE_FACTOR
    return canvas.coords(shape, x1, y1, x2, y2)

def area(canvas, shape):
    """
    Find area of a shape
    """
    shape_coords = canvas.coords(shape)
    x1 = shape_coords[0]
    y1 = shape_coords[1]
    x2 = shape_coords[2]
    y2 = shape_coords[3]
    shape_area = (x2 - x1) * (y2 - y1)
    return shape_area


######## DO NOT MODIFY ANY CODE BELOW THIS LINE ###########

# This function is provided to you and should not be modified.
# It creates a window that contains a drawing canvas that you
# will use to make your drawings.
def make_canvas(width, height, title, background):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tk.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tk.Canvas(top, width=width + 1, height=height + 1, background = background)
    canvas.pack()
    return canvas


if __name__ == "__main__":
    main()