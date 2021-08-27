from geometry.geometry import billard
# Rectangle ratio controls is equivalent to the slope ratio
# e=5
# f=6
# b=billard([[0,0], [0,e], [f,e], [f,0]], position=[0,0], slope=[1,1])

# 90 rotated square get very similar properties with trajectory from square
# The increasing integer sequences generate a curve related to the ratio :
# 1, 3, 2, 5/3, 3/2, 7/5, 4/3, 9/7, 5/4, 11/9, 6/5, 13/11, 7/6, 15/13
# which is a(n) = b(n+2)/b(n)
# b(n) = 1, 3, 2, 5, 3, 7, 4, 9, 5, 11, 6, 13, 7, 15 ... =  n if n odd, n/2 if n even

# b=billard([[-1,0], [0,1], [1,0], [0,-1]], position=[0,0.1], slope=[14,1])



b=billard([[-1,0], [0,1], [1,0], [0,-1]], position=[0,0.1], slope=[14,1])



b.n_bounce(500)

b.plot()