import random

from Gui.draw_train import DrawTrain
import tkinter as tk
from threading import Lock
from Models.Train import Train
from Models.InterSection import Intersection

if __name__ == "__main__":

    window = tk.Tk()
    train_length = 250
    colors = ['red', 'green', 'yellow', 'blue']
    trains = []
    intersections = []

    for i in range(4):
        color = colors.pop(random.randint(0, len(colors) - 1))
        trains.append(Train(i, color=color, train_length=train_length, front=0))
        intersections.append(Intersection(i, Lock(), -1))
    draw_train = DrawTrain(window, train_length, trains, intersections)
    window.mainloop()
    # window.after(10, yazdir)
