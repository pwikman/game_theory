import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm 

def polynomial(x):
    return 0.8*norm.cdf(7*(x-0.5))+0.05 +0.1*x

def polynomial_2(x):
    return 0.8*norm.cdf(7*(x-0.674))+0.05 +0.1*x

d = np.arange(0,1,0.01)


vec_p = np.vectorize(polynomial)(d)
vec_p2 = np.vectorize(polynomial_2)(d)
vec_45 = np. vectorize(lambda x: x)(d)

fig, ax = plt.subplots()

ax.plot(d,vec_p, 'k')
ax.plot(d,vec_p2, 'k--')
ax.plot(d,vec_45, 'k', linewidth=0.5)
plt.savefig('index.png')