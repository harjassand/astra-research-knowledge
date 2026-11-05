import numpy as np
from scipy.optimize import minimize
I=np.eye(2);P=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def pauli3(x):
 a=np.array([[1.]])
 for z in x:a=np.kron(a,I if z<0 else P[z])
 return a
S0=[pauli3([a,-1,-1]) for a in range(3)]
M0=[pauli3([-1,a,-1]) for a in range(3)]
E0=[pauli3([-1,-1,a]) for a in range(3)]
PS=(np.eye(8)+sum(S0[a]@E0[a] for a in range(3)))/2
PM=(np.eye(8)+sum(M0[a]@E0[a] for a in range(3)))/2
B=[S0[2],M0[2],(S0[0]@M0[1]-S0[1]@M0[0])/np.sqrt(2)]
def matrix(t,f):
 U=(np.cos(f)*np.eye(8)-1j*np.sin(f)*PM)@(np.cos(t)*np.eye(8)+1j*np.sin(t)*PS)
 return np.real(np.array([[np.trace(A@U@C@U.conj().T)/8 for C in B]for A in B]))
if __name__=='__main__':
 for t,f in [(.2,.3),(.4,.6),(.7,.2)]:print(t,f,matrix(t,f))
