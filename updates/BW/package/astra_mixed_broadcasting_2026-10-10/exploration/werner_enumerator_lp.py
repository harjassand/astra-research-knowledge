import math
import numpy as np
from scipy.optimize import linprog

def bc(n,k): return math.comb(n,k) if 0<=k<=n else 0
def kraw(n,j,i,q): return sum((-1)**a*(q-1)**(j-a)*bc(i,a)*bc(n-i,j-a) for a in range(j+1))
def solve(n,d=3,K=2):
    # A_i = sum |tr(P E)|^2/K^2 over weight-i unitary errors.
    M=np.array([[K/d**n*kraw(n,j,i,d*d) for i in range(n+1)] for j in range(n+1)])
    U=np.array([[K*K/d**l*bc(n-i,l-i) if i<=l else 0 for i in range(n+1)] for l in range(n+1)])
    S=np.array([[2**(-n)*kraw(n,j,l,2) for l in range(n+1)] for j in range(n+1)])@U
    c=np.array([K*K/d**n*(-.5)**(n-i) for i in range(n+1)])
    eq=np.array([[1]+[0]*n,[1]*(n+1)],float)
    res=linprog(c,A_ub=np.r_[np.eye(n+1)-M,-S],b_ub=np.zeros(2*(n+1)), A_eq=eq,b_eq=[1,d**n/K], bounds=[(0,None)]*(n+1), method='highs')
    if res.success:
        return {'n':n,'q':res.fun,'A':res.x.tolist(),'sector':(S@res.x).tolist()}
    return str(res.message)
if __name__=='__main__':
 for n in range(1,16): print(solve(n))
