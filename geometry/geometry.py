from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from decimal import Decimal

EPSILON = Decimal('1E-10')
MAX_ITER = 10000

SHAPE = {"Carre" : [[0,0], [0,1], [1,1], [1,0]],
        "Rectangle" : [[0,0], [0,1], [2,1], [2,0]],
        "Triangle Rectangle" : [[0,0], [0,1], [1,1]],
        "Carre 45" : [[0,0.5], [0.5,1], [1,0.5], [0.5,0]]} 

def reflect(k1,k2):
    try:
        reflected = (k1*k2*k2+2*k2-k1)/(1+2*k1*k2-k2*k2)
        return [1, reflected]
    except ZeroDivisionError:
        return [0,1]
def f2d(f:float):
    return Decimal(str(f))

def l2d(l:list):
    for i in range(len(l)):
        l[i] = f2d(l[i])
    return l

class line:
    def __init__(self, slope:list, p1:list, p2:list=None):
        slope = l2d(slope)
        self.p1 = l2d(p1)
        if slope[0] == 0:
            self.c = Decimal("0")
            self.a = Decimal("1")
        else:
            self.a = f2d(slope[1])/f2d(slope[0])
            self.c =  Decimal("1")
        self.b = self.c*self.p1[1]-self.p1[0]*self.a
        if p2:
            self.p2 = l2d(p2)
            self.mode = "finite"
        else:
            self.mode = "semi"

    @classmethod
    def from_points(cls, p1:list, p2:list):
        p1 = l2d(p1)
        p2 = l2d(p2)
        slope = [p2[0]-p1[0], p2[1]-p1[1]]
        return cls(slope,p1,p2)

    def equation(self, p):
        return self.c*p[1]-self.a*p[0]-self.b
    
    def isin(self, p):
        cond_equation = abs(self.equation(p)) < EPSILON
        if self.mode == "finite":
            cond_x = (self.p1[0]-p[0])*(self.p2[0]-p[0]) <= EPSILON
            cond_y = (self.p1[1]-p[1])*(self.p2[1]-p[1]) <= EPSILON
            return cond_equation and cond_x and cond_y
        elif self.mode == "semi":
            cond_x = abs(self.p1[0] - p[0]) >= EPSILON
            cond_y = abs(self.p1[1] - p[1]) >= EPSILON
            return cond_equation and (cond_x or cond_y)
    
    def intersect(self, line):
        p=[0,0]
        if self.c * line.c > 0:
            if self.a != line.a:
                p[0] = (line.b - self.b)/(self.a-line.a)
                p[1] = self.a*p[0]+self.b
            else:
                return None
        elif self.c == 1:
            p[0] = -line.b*line.a
            p[1] = self.b-(self.a/line.a)*line.b
        elif line.c == 1:
            p[0] = -self.b*self.a
            p[1] = line.b-(line.a/self.a)*self.b
        else:
            return None   
        if self.isin(p) and line.isin(p):
            return p
        
    def print(self):
        print(self.a, self.b, self.c)
        

class billard:
    def __init__(self, corners, position=[0,0],slope=[1,1]):
        self.position = l2d(position)
        self.slope = l2d(slope)
        self.path = line(self.slope, self.position)
        self.corners = [l2d(corner) for corner in corners]
        self.line = []
        self.bounce_line = None
        self.bounces = [position]
        self.slopes = [slope]
        self.interval = [Decimal('0')]
        for i in range(len(self.corners)):
            self.line.append(line.from_points(self.corners[i%len(self.corners)], self.corners[(i+1)%len(self.corners)]))
    
    def reset_slope(self, slope):
        self.slope = l2d(slope)
        self.position = self.bounces[0]
        self.bounces = [self.position]
        self.slopes = [self.slope]
        self.interval = [Decimal('0')]
        self.path = line(self.slope, self.position)

    def on_corner(self):
        for c in self.corners:
            if abs(c[0]-self.position[0]) <= EPSILON and abs(c[1]-self.position[1]) <= EPSILON:
                return True
        return False

    def bounce(self):
        for l in self.line:
            intersection = self.path.intersect(l)
            if intersection:
                self.bounce_line=l
                break
        if not intersection:
            pass
        self.position = intersection
        if self.on_corner():
            pass
        else:
            if self.bounce_line.a == 0:
                self.slope = [-self.slope[0], self.slope[1]]
            elif self.bounce_line.c == 0:
                self.slope = [self.slope[0], -self.slope[1]]
            elif self.slope[0] == 0:
                self.slope[1] = (self.bounce_line.a **2 - 1)/2*self.bounce_line.a 
                self.slope[0] = Decimal("1")
            else:
                normal = -1/self.bounce_line.a 
                incident = self.slope[1]/self.slope[0]
                self.slope = reflect(incident, normal)
        self.path = line(self.slope, self.position)
        self.bounces.append(self.position)
        self.slopes.append(self.slope)
        self.interval.append(((self.bounces[-1][1]-self.bounces[-2][1])**2 + \
                              (self.bounces[-1][0]-self.bounces[-2][0])**2)**(Decimal("0.5"))+ \
                                  self.interval[-1])
    
    def n_bounce(self, n:int=50):
        for _ in range(n):
            self.bounce()