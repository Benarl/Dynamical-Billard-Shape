import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from geometry.geometry import billard
import numpy as np
import time
from decimal import Decimal

class App:
    def __init__(self, master):
        # Create a container
        self.frame = tkinter.Frame(master)
        self.slider = tkinter.Scale(self.frame, from_=0, to=1600, 
                               orient="horizontal",length =700, 
                               command=self.updateValue)
        self.slider.pack()
        # Create 2 buttons
        self.button_left = tkinter.Button(self.frame,text="< Decrease Slope",
                                        command=self.decrease)
        self.button_left.pack(side="left")
        self.button_right = tkinter.Button(self.frame,text="Increase Slope >",
                                        command=self.increase)
        self.button_right.pack(side="left")

        fig = Figure(figsize=(8,8))
        self.ax = fig.add_subplot(111)
        # Create billard
        self.b=billard([[0,0], [0,1], [1,1]], position=[0,0], slope=[1,1])
        # self.b=billard([[0,0], [0,1], [1,1], [1,0]], position=[0,0], slope=[1,1])
        self.b.n_bounce(10)
        xs, ys = zip(*(self.b.corners+[self.b.corners[0]]))
        self.box, = self.ax.plot(xs, ys, c="k")
        x, y = zip(*self.b.bounces)
        self.line, = self.ax.plot(x,y, c="g")

        self.canvas = FigureCanvasTkAgg(fig,master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', expand=1)
        self.frame.pack()

        self.i = 0

    def updateValue(self, event):
        sg = self.slider.get()/1000
        t = 1+round(np.tan(sg)*1000)/1000
        self.b.reset_slope([1, t])
        self.b.n_bounce(10)
        x, y = zip(*self.b.bounces)
        self.line.set_data(x, y)
        self.canvas.draw()
        
    def decrease(self):
        self.i -= 0.0001
        self.change_shape()

    def increase(self):
        self.i += 0.0001
        self.change_shape()


    def change_shape(self):
        self.b=billard([[0,0], [self.i,1], [1+self.i,1], [1,0]], position=[0,0], slope=[1,1])
        self.b.reset_slope(self.b.slopes[-1])
        self.b.n_bounce(100)
        x, y = zip(*self.b.bounces)
        self.line.set_data(x, y)
        x, y = zip(*(self.b.corners+[self.b.corners[0]]))
        self.box.set_data(x, y)
        a = max(self.i+1,1)-min(self.i, 0)
        self.box.axes.set_xlim(min(self.i, 0),max(self.i+1,1))
        self.line.axes.set_xlim(min(self.i, 0),max(self.i+1,1))
        self.canvas.draw()


root = tkinter.Tk()
app = App(root)
root.mainloop()