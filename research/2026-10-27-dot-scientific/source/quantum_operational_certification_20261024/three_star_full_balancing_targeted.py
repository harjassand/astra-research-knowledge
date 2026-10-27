import numpy as np
from scipy.optimize import differential_evolution, minimize

def f(G):
 v=np.linalg.eigvalsh(G);v=v[v>1e-15];return np.dot(v,np.log(v))
def value(p,x,c):
 d=p/3;R=np.diag(np.r_[p,x/3]);R[0,1:]=R[1:,0]=c/np.sqrt(3)
 z=sum(f(np.array([[d,c[i]],[c[i],x[i]]])) for i in range(3))+f(R)-np.log(3)
 for i,j in [(0,1),(0,2),(1,2)]:z-=2*f(np.array([[d,c[i]/np.sqrt(6),c[j]/np.sqrt(6)],[c[i]/np.sqrt(6),x[i]/3,0],[c[j]/np.sqrt(6),0,x[j]/3]]))
 return z
def gap(z):
 p=z[0];w=np.array([z[1],(1-z[1])*z[2],(1-z[1])*(1-z[2])]);r=np.array(z[3:]);x=(1-p)*w;c=np.sqrt(p*x*r/3)
 return value(p,x,c)-value(p,np.ones(3)*(1-p)/3,np.ones(3)*sum(c)/3)
if __name__=='__main__':
 bounds=[(.01,.99),(.001,.999),(.001,.999)]+[(0,1)]*3
 res=differential_evolution(gap,bounds,popsize=8,maxiter=150,tol=1e-8,seed=981,polish=True)
 print(res.fun,res.x,flush=True);np.savez('three_star_full_balancing_targeted.npz',z=res.x,gap=res.fun)
