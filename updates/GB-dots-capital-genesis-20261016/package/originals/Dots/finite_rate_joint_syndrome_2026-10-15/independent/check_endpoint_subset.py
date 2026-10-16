import numpy as np
from scipy.linalg import expm
from functools import reduce
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Y=np.array([[0,-1j],[1j,0]]); Z=np.diag([1,-1]).astype(complex)
ps={'I':I,'X':X,'Y':Y,'Z':Z}
def P(s):return reduce(np.kron,[ps[c] for c in s])
def ad(A):return np.kron(A.conj(),A)
def lind(H,checks,gammas):
 d=len(H);E=np.eye(d);return -1j*(np.kron(E,H)-np.kron(H.T,E))+sum(g*(ad(z)-np.eye(d*d)) for z,g in zip(checks,gammas))
def vec(x):return x.reshape(-1,order='F')
def B(j,g,t):
 d=np.sqrt(g*g+4*j*j);return .5*(np.exp(-g*t)*(np.cosh(d*t)+g/d*np.sinh(d*t))-1)
checks=[P('ZII'),P('IZI')];E=np.eye(8)
H0=.7*P('IIX')+.4*P('ZIZ')+.3*P('IZY')+.15*P('ZZX')
W1=.3*P('XIX')+.2*P('YIZ')+.17*P('XZI')
W2=.21*P('IXZ')+.13*P('ZYY')-.19*P('IYX')
W1/=np.linalg.norm(W1,2);W2/=np.linalg.norm(W2,2)
assert np.linalg.norm(W1@W2-W2@W1)>.1
for i,W in enumerate([W1,W2]):
 for j,z in enumerate(checks):assert np.linalg.norm(W@z-(-1 if i==j else 1)*z@W)<1e-11
count=0;ratio=0.
for gammas in [[.3,.7],[1.2,.2]]:
 for js in [[.05,.09],[.2,.15],[.5,.7]]:
  L=lind(H0+js[0]*W1+js[1]*W2,checks,gammas)
  for t in [.02,.2,1.,3.]:
   channel=expm(t*L)
   for s in range(4):
    signs=[1-2*(s>>1),1-2*(s&1)]
    Pi=reduce(np.matmul,[(E+sign*z)/2 for sign,z in zip(signs,checks)])
    inds=np.where(np.diag(Pi).real>.5)[0]
    for subset in [[0],[1],[0,1]]:
     F=reduce(np.matmul,[(E-signs[i]*checks[i])/2 for i in subset])
     effect=(channel.conj().T@vec(F)).reshape((8,8),order='F');effect=(effect+effect.conj().T)/2
     block=effect[np.ix_(inds,inds)];maximum=np.linalg.eigvalsh(block).max()
     bound=np.prod([min(1,B(js[i],gammas[i],t)) for i in subset])
     assert maximum<=bound+3e-12,(gammas,js,t,s,subset,maximum,bound)
     ratio=max(ratio,maximum/bound);count+=1
# Invalid-incidence example: a single coupling flips both selected checks.
g=.7;j=.2;t=.01;zs=[P('ZI'),P('IZ')];ch=expm(t*lind(j*P('XX'),zs,[g,g]));r=np.zeros((4,4));r[0,0]=1
prob=(ch@vec(r)).reshape((4,4),order='F')[3,3].real;invalid=B(j,g,t)**2
assert prob>1000*invalid
print(f'PASS {count} exact endpoint-effect tests; maximum observed effect/bound={ratio:.8f}.')
print('Effects maximized over arbitrary initial bath states in each starting parity sector.')
print(f'Invalid-incidence counterexample: joint flip={prob:.10g}, false product bound={invalid:.10g}.')
print('Shared bath operators are noncommuting. No chronological support/lifetime conclusion.')
