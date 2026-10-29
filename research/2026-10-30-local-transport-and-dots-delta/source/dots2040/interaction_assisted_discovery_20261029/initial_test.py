import sympy as s, itertools
from scipy.linalg import expm
import numpy as np
r=s.symbols('r')
K=s.Matrix([[-3,1,2],[1,-4,3],[2,3,-5]])
S=s.Matrix([[1,0,0],[0,1+r,-r],[0,0,1]])
Kr=s.simplify(S.inv()*K*S)
def full(k):
 Q=s.zeros(4);Q[0,0]=-1;Q[0,1]=1;Q[1,0]=1
 Q[1:4,1:4]=k-s.diag(1,0,0)
 return Q
def excl(Q,k):
 n=Q.rows; states=list(itertools.combinations(range(n),k));I={z:i for i,z in enumerate(states)};L=s.zeros(len(states))
 for a,z in enumerate(states):
  for i in z:
   for j in range(n):
    if j in z:continue
    w=tuple(sorted(set(z)-{i}|{j}));L[a,I[w]]+=Q[i,j]
  L[a,a]=-sum(L.row(a))
 return states,s.simplify(L)
states,L=excl(full(Kr),2);_,L0=excl(full(K),2)
b=s.Matrix([int(0 in z) for z in states]);a=s.zeros(1,6);a[0,0]=1
print('STATES',states);print('Lr',L)
for power in range(1,8):
 d=s.factor((a*(L**power-L0**power)*b)[0]);print('derivative',power,d)
 if d!=0:break
for rr in [s.Rational(1,10),s.Rational(1,2),s.Rational(4,5)]:
 lr=np.array(L.subs(r,rr)).astype(float);l0=np.array(L0).astype(float)
 for t in [.1,.5,1,2]:
  p1=float(np.array(a).astype(float)@expm(t*lr)@np.array(b).astype(float));p0=float(np.array(a).astype(float)@expm(t*l0)@np.array(b).astype(float))
  print('boundary occupancy',rr,t,p0,p1,p1-p0)
print('r vs 1-r')
for power in range(1,8):
 d=s.factor((a*(L**power-(L.subs(r,1-r))**power)*b)[0]);print('derivative',power,d)
 if d!=0:break
