import math
import numpy as np

def g(w):
    if w<1e-6: return 1-w*w/3
    return (w/math.sinh(w))**2

p=math.sqrt(6-math.sqrt(20));r=math.sqrt(8);s=math.sqrt(6+math.sqrt(20))
xs=np.array([p,r,s]);
A=np.stack([xs**2,2*xs**4,-np.ones(3)],axis=1)
b=-np.array([x**3*g(x) for x in xs])
lam,mu,eta=np.linalg.solve(A,b)
def F(w): return w**3*g(w)+lam*w*w+2*mu*w**4-eta
print('endpoints',p,r,s)
print('multipliers',lam,mu,eta)
for w in [.01,.1,.5,1.,1.5,2.,2.7,2.9,3.,3.5,4.,5.,10.,20.]:print(w,F(w))
grid=np.geomspace(1e-6,100,200001)
sign=np.array([F(float(w)) for w in grid])
roots=[]
for i in range(len(grid)-1):
    if sign[i]*sign[i+1]<0: roots.append((grid[i],grid[i+1]))
print('grid sign brackets',roots)
