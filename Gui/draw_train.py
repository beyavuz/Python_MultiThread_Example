import random
import tkinter
import tkinter as tk
from threading import Thread, Lock

from Models.Train import Train
from Models.Crossing import Crossing
from Models.InterSection import Intersection
from Deadlock.train_deadlock import move_train_deadlock
from Misc.train_hierc import move_train_hierarchy



class DrawTrain:
    def __init__(self, window, train_length, trains, intersections):
        self.window = window
        self.train_length = train_length
        self.window.geometry("800x800")
        self.window.resizable(False, False)
        self.canvas_anim_id = None
        self.intersections = []
        self.create_intersections()
        self.obje_trains = []
        self.create_variables()
        self.panel = tkinter.PanedWindow(orient='horizontal')
        self.panel.configure(bg="white")
        self.btn_deadlock = tkinter.Button(self.panel, text="Deadlock",
                                           command=lambda: self.train_move(self.obje_trains, self.intersections,
                                                                           move_train_deadlock))
        self.btn_hierc = tkinter.Button(self.panel, text="Solve with Hierarchy",
                                        command=lambda: self.train_move(self.obje_trains, self.intersections,
                                                                        move_train_hierarchy))
        self.btn_arbitrator = tkinter.Button(self.panel, text="Solve with Arbitrator",
                                             command=lambda: self.delete_all())
        self.btn_deadlock.grid(row=0, column=0)
        self.btn_hierc.grid(row=0, column=1, padx=20)
        self.btn_arbitrator.grid(row=0, column=2)
        self.panel.pack(fill=tkinter.BOTH)

        self.canvas = tk.Canvas(self.window, width=800, height=800)
        # self.tracks = []
        self.threads = []
        self.trains = []
        self.__initiate_tracks()
        self.__initate_trains(trains)
        self.__start_ui()

    def create_variables(self):
        colors = ['red', 'green', 'yellow', 'blue']
        self.obje_trains = []
        self.intersections = []
        for i in range(4):
            color = colors.pop(random.randint(0, len(colors) - 1))
            self.obje_trains.append(Train(i, color=color, train_length=self.train_length, front=0))
            self.intersections.append(Intersection(i, Lock(), -1))

    def __start_ui(self):
        self.window.title("Deadlock")
        self.__draw_elements()

    def create_intersections(self):
        for i in range(4):
            self.intersections.append(Intersection(i, Lock(), -1))

    def __initiate_tracks(self):
        self.track1 = (10, 300, 790, 300)
        self.track2 = (10, 440, 790, 440)
        self.track3 = (330, 10, 330, 790)
        self.track4 = (470, 10, 470, 790)
        self.tracks = [self.track1, self.track2, self.track3, self.track4]

    def __initate_trains(self, trains):
        self.train1 = {"id": trains[0].uid, "start_position": (10 - self.train_length, 300, 10, 300),
                       "color": trains[0].color}
        self.train2 = {"id": trains[1].uid, "start_position": (790 + self.train_length, 440, 790, 440),
                       "color": trains[1].color}
        self.train3 = {"id": trains[2].uid, "start_position": (470, 10 - self.train_length, 470, 10),
                       "color": trains[2].color}
        self.train4 = {"id": trains[3].uid, "start_position": (330, 790 + self.train_length, 330, 790),
                       "color": trains[3].color}
        self.trains = [self.train1, self.train2, self.train3, self.train4]
        for train in self.trains:
            print(f"Train id:{train['id']} , color:{train['color']}")

    def __draw_elements(self):

        for track in self.tracks:
            self.canvas.create_line(*track, fill="white")
        for train in self.trains:
            train['object'] = self.canvas.create_line(*train.get('start_position'), fill=train.get('color'), width=8,
                                                      tags=f"train_{train.get('id')}")
        # self.son_tren = self.canvas.create_line(self.trains[0].get('start_position'), fill='red', width=8, tags="son_tren")
        self.boxes = []
        self.boxes.append(self.canvas.create_rectangle(350, 320, 360, 330, fill="white"))  # intersection0
        self.boxes.append(self.canvas.create_rectangle(450, 320, 440, 330, fill="white"))  # intersection1
        self.boxes.append(self.canvas.create_rectangle(450, 420, 440, 410, fill="white"))  # intersection2
        self.boxes.append(self.canvas.create_rectangle(350, 420, 360, 410, fill="white"))  # intersection3
        self.canvas.pack()
        # self.canvas.pack(fill=tk.BOTH, expand=True)

    def update_trains_animations(self, trains, intersections):
        if self.canvas.coords("train_0")[2] < 790:
            self.canvas.move(self.trains[0].get('object'), trains[0].front - self.canvas.coords("train_0")[2], 0)
        if self.canvas.coords("train_1")[2] > 0:
            self.canvas.move(self.trains[1].get('object'), 790 - self.canvas.coords("train_1")[2] - trains[1].front, 0)
        if self.canvas.coords("train_2")[3] < 790:
            self.canvas.move(self.trains[2].get('object'), 0, trains[2].front - self.canvas.coords("train_2")[3])
        if self.canvas.coords("train_3")[3] > 0:
            self.canvas.move(self.trains[3].get('object'), 0, 790 - trains[3].front - self.canvas.coords("train_3")[3])
        for i in range(4):
            if intersections[i].locked_by < 0:
                self.canvas.itemconfig(self.boxes[intersections[i].uid], fill='white')
            else:
                self.canvas.itemconfig(self.boxes[intersections[i].uid],
                                       fill=self.trains[intersections[i].locked_by]['color'])
        print("nden cok hızlı")
        self.canvas_anim_id = self.canvas.after(1, self.update_trains_animations, trains, intersections)

    def __reset_ui(self, trains, intersections, function):
        if self.canvas_anim_id is not None:
            self.canvas.after_cancel(self.canvas_anim_id)
        self.create_intersections()
        self.create_variables()
        self.canvas.delete('all')
        print("Gene varmı:::", self.canvas.find_all())
        self.__draw_elements()
        self.threads = [Thread(target=function,
                               args=(
                                   trains[0], 780, [Crossing(320, intersections[0]), Crossing(460, intersections[1])])),
                        Thread(target=function,
                               args=(
                                   trains[1], 780, [Crossing(310, intersections[2]), Crossing(450, intersections[3])])),
                        Thread(target=function,
                               args=(
                                   trains[2], 780, [Crossing(290, intersections[1]), Crossing(430, intersections[2])])),
                        Thread(target=function,
                               args=(
                                   trains[3], 780, [Crossing(340, intersections[3]), Crossing(480, intersections[0])]))]

    def train_move(self, trains, intersections, function):
        self.__reset_ui(trains, intersections, function)
        for thread in self.threads:
            thread.start()
            print("Threadler yeniden başladı...")
        self.update_trains_animations(trains, intersections)

    def delete_all(self):
        self.canvas.delete('all')
