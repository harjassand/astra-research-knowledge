"""Exact symbolic reset obstructions and independent numerical kernel diagnostic.
Conventions H_hop=-(t/2)sum(XX+YY), D=gamma sum(Z rho Z-rho), d=4 gamma.
"""
import itertools
import sympy as s
import numpy as np
from scipy.linalg import expm

# Four states form two independent 10<->01 choices, fixed particle number two.
states = [(1,0,1,0),(0,1,1,0),(1,0,0,1),(0,1,0,1)]
d,r,a = s.symbols('d r a', positive=True)
ham=lambda x,y:sum(u!=v for u,v in zip(x,y))
Q=s.Matrix([[s.Rational(ham(x,y),2)*d for y in states] for x in states])
c=s.Matrix([1,-1,-1,1]); ones=s.ones(4)
assert (c.T*ones)[0] == 0
assert c.T*Q*c == s.zeros(1)
Qres=Q-r*(s.ones(4,4)-s.eye(4))
assert (c.T*Qres*c)[0] == 4*r
print('Reset-rate matrix Q/d:'); print(Q/d)
print('c^T Q c = 0; c^T (Q-r[1-I]) c = 4r > 0, incompatible with dephasing CP.')
C=s.Matrix([[a**(ham(x,y)//2) for y in states] for x in states])
assert (C*c - (1-a)**2*c).applyfunc(s.expand) == s.zeros(4,1)
print('Finite-time coherence matrix eigenvector c has eigenvalue (1-a)^2; m-pair extension is (1-a)^m.')

# Exact alternating-renewal waiting law for a resonant damped dimer.
z=s.symbols('z',positive=True); h=s.symbols('h',positive=True)
k=2*h*h/(z+d)
f=s.factor(k/(z+k))
assert f == 2*h*h/(z*z+d*z+2*h*h)
print('Unique classical alternating-renewal waiting transform:',f)
print('For h=d=1: f(time)=4/sqrt(7) exp(-time/2) sin(sqrt(7) time/2), not nonnegative.')

# Optional full four-site periodic chain diagnostic, no frozen spectators.
# Vectorization is by ordered configuration pair (ket,bra).
bs=list(itertools.combinations(range(4),2)); masks=[sum(1<<i for i in x) for x in bs]
N=len(masks); ix={v:i for i,v in enumerate(masks)}
H=np.zeros((N,N)); t=U=dec=1.
for v in masks:
 i=ix[v]; spin=[1-2*((v>>j)&1) for j in range(4)]
 H[i,i]=U*sum(spin[j]*spin[(j+1)%4] for j in range(4))
 for j in range(4):
  k=(j+1)%4
  if ((v>>j)&1)!=((v>>k)&1): H[ix[v^(1<<j)^(1<<k)],i]-=t
L=np.zeros((N*N,N*N),complex)
for x in range(N):
 for y in range(N):
  row=x*N+y
  L[row,row]-=dec*(masks[x]^masks[y]).bit_count()/2
  for z0 in range(N):
   L[row,z0*N+y]+=-1j*H[x,z0]
   L[row,x*N+z0]+=1j*H[z0,y]
p=np.array([i*N+i for i in range(N)]); q=np.array([j for j in range(N*N) if j not in set(p)])
A=L[np.ix_(p,q)]; B=L[np.ix_(q,p)]; M=L[np.ix_(q,q)]
assert np.allclose(L[np.ix_(p,p)],0)
print('Full four-site periodic chain, U=t=d=1, unprojected diagonal excursion kernel:')
for tau in [0,.25,.5,.75,1,1.5,2]:
 K=A@expm(tau*M)@B
 off=K.real.copy(); np.fill_diagonal(off,np.inf)
 i,j=np.unravel_index(np.argmin(off),off.shape)
 print('tau=',tau,'minimum offdiagonal K=',off[i,j], 'states=',format(masks[i],'04b'),format(masks[j],'04b'),'imag residual=',np.max(abs(K.imag)))

# Rigorous rational negative-entry certificate at tau=1/2.
# Integer real/imaginary data above are converted exactly; no float dynamics used.
toexact=lambda Z:s.Matrix([[s.Integer(round(z.real))+s.I*s.Integer(round(z.imag)) for z in row] for row in Z])
Ms=toexact(M); As=toexact(A); Bs=toexact(B)
i=ix[int('1001',2)]; j=ix[int('1010',2)]
left=As[i,:]; v=Bs[:,j]; S=(left*v)[0]; tau=s.Rational(1,2)
Nterms=50
for ell in range(1,Nterms+1):
 v=(Ms*v).applyfunc(s.expand)
 S += s.expand((left*v)[0])*tau**ell/s.factorial(ell)
S=s.simplify(S)
absupper=lambda z:abs(s.re(z))+abs(s.im(z))
Mnorm=max(sum(absupper(Ms[i,j]) for j in range(Ms.cols)) for i in range(Ms.rows))
Anorm=sum(absupper(z) for z in left)
Bnorm=max(absupper(z) for z in Bs[:,j])
x=tau*Mnorm
# exp(x) <= 3^ceil(x), so tail is an explicitly rational upper bound.
err=Anorm*Bnorm*3**s.ceiling(x)*x**(Nterms+1)/s.factorial(Nterms+1)
assert s.im(S)==0
assert S+err < -s.Rational(1111,1000)
assert S-err > -s.Rational(1112,1000)
print('RIGOROUS certificate: -1.112 < K_(1001,1010)(1/2) < -1.111 at U=t=d=1.')
print('50th-order rational Taylor polynomial=',s.N(S,18),'remainder bound=',s.N(err,6),'M norm bound=',Mnorm)
