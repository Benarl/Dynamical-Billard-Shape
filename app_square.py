import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from geometry.geometry import billard, SHAPE
from geometry.square import billard_square
import numpy as np

class App:
    def __init__(self, master):
        # Create a container
        self.frame = tkinter.Frame(master)
        self.slider = tkinter.Scale(self.frame, from_=0, to=1600, 
                               orient="horizontal",length =700, 
                               command=self.updateValue)
        self.slider.pack()
        
        self.slider_proj = tkinter.Scale(self.frame, from_=0, to=1600, 
                               orient="horizontal",length =700, 
                               command=self.change_projection)


        self.slider_phi_x = tkinter.Scale(self.frame, from_=0, to=1600, 
                               orient="horizontal",length =700, 
                               command=self.change_phi_x)

        self.slider_phi_y = tkinter.Scale(self.frame, from_=0, to=1600, 
                               orient="horizontal",length =700, 
                               command=self.change_phi_y)

        self.slider_proj.pack()
        self.slider_phi_x.pack()
        self.slider_phi_y.pack()
        self.prog_angle = 0
        
        # create buttons

        fig, self.ax = plt.subplots(ncols=1, figsize=(5,5))

        # Create billard
        self.b=billard_square(angle=0, position=[0,0])
        xs, ys = zip(*([[0,0], [0,1], [1,1], [1,0], [0,0]]))
        self.box, = self.ax.plot(xs, ys, c="k")
        self.ax.axis("off")
        x, y = self.b.trajectory()

        self.line, = self.ax.plot(x,y, c="k", lw=2)

        self.canvas = FigureCanvasTkAgg(fig,master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', expand=1)
        self.frame.pack()

        self.i = 0

    def update_plot(self):
        
        x, y = self.b.trajectory()
        self.line.set_data(x, y)

        self.canvas.draw()

    def updateValue(self, event):
        # angle = (self.slider.get()*np.pi/2)/1600
        # c,s=np.cos(angle), np.sin(angle)
        angle = 3*self.slider.get()/1600
        self.b.angle=angle
        # self.b.reset_slope([1,angle])
        # self.b.loop()
        self.update_plot()

    def change_projection(self, event):
        self.prog_angle = (self.slider_proj.get())/800
        self.b.c=max(0.001,abs(self.prog_angle))
        self.update_plot()

    def change_phi_x(self, event):
        self.phi_x = (self.slider_phi_x.get())/1600
        self.b.position[0] = self.phi_x
        self.update_plot()

    def change_phi_y(self, event):
        self.phi_y = (self.slider_phi_y.get())/1600
        self.b.position[1] = self.phi_y
        self.update_plot()




root = tkinter.Tk()
app = App(root)
root.mainloop()