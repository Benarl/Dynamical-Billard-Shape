from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from decimal import Decimal
import numpy as np

def triangle(x):
    return 2*abs(x-int(x+0.5-1*(x<0)))

class billard_square:
    def __init__(self, angle, position):
        self.angle =angle
        self.position=position
        self.N = 1000
        self.c=1
        self.interval=range(self.N)

    def x(self, t):
        return triangle(self.c*(t)*np.cos(self.angle)+self.position[0])

    def y(self, t):
        return triangle(self.c*(t)*np.sin(self.angle)+self.position[1])

    def trajectory(self, T=5):
        trajectory=[[self.x((i)*T/self.N) for i in self.interval], [self.y((i+self.position[1])*T/self.N) for i in self.interval]]
        return trajectory


