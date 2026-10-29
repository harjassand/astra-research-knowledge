"""The fixed C1 bounded norm weight used by the continuum receiver."""
import numpy as np


def phi(v):
    x=np.asarray(v)**2
    h=(x-4)*(25-x)
    return 1+np.where((x>=4)&(x<=25),4*h*h/194481,0)
