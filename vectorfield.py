import matplotlib.pyplot as plt
import numpy as np
import egtsimplex

#define function of x=[x0,x1,x2] and t to plot dynamics on simplex
def f(x,t):
    A=np.array([[0,1,-1],[-1,0,1],[1,-1,0]])
    phi=(x.dot(A.dot(x)))
    x0dot=x[0]*(A.dot(x)[0]-phi)
    x1dot=x[1]*(A.dot(x)[1]-phi)
    x2dot=x[2]*(A.dot(x)[2]-phi)
    return [x0dot,x1dot,x2dot]


#initialize simplex_dynamics object with function
dynamics=egtsimplex.simplex_dynamics(f)

#plot the simplex dynamics
fig,ax=plt.subplots()
dynamics.plot_simplex(ax)
plt.show()