import numpy as np
exec(open('mixed_reset_purity_probe.py').read().split('best=-1e9')[0])
def f(X):
 e=np.linalg.eigvalsh((X+X.conj().T)/2);e=e[e>1e-12];return sum(e*np.log(e))
def dd(X,n):return f(X)+f(ptr(X,n))-2*f(N(X,n))-np.trace(X).real*np.log(3)
rng=np.random.default_rng(852);omega=np.eye(3).reshape(-1);V=np.vstack([np.eye(3),np.zeros((3,3))]);ov=V.T.reshape(-1)
for j in range(18):
 G=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));A=G@G.conj().T+.1*np.eye(3);delta=10**rng.uniform(-1,1);gamma=10**rng.uniform(-1,1);d=10**rng.uniform(-1,1)
 Y=np.block([[A+gamma**2/delta*np.eye(3),gamma*np.eye(3)],[gamma*np.eye(3),delta*np.eye(3)]])
 L=np.hstack([np.eye(3),-gamma/delta*np.eye(3)]);kap=delta**2/(delta**2+gamma**2);K=np.sqrt(kap)*L
 X=d*np.outer(ov,ov)+np.kron(np.eye(3),Y);seed=d*np.outer(omega,omega)+np.kron(np.eye(3),A);T=np.kron(np.eye(3),K)
 assert np.linalg.norm(T@X@T.conj().T-kap*seed)<1e-9
 assert dd(X,6)>=kap*dd(seed,3)-1e-7
 for s in[.1,1,3]:
  cs=s+gamma**2*s/(delta*(delta+s));C=np.linalg.inv(V.conj().T@np.linalg.inv(Y+s*np.eye(6))@V)
  assert np.linalg.norm(C-A-cs*np.eye(3))<1e-9
print('PASS18 actual complex common-clock sources, exact accepted maps and finite entropy payment')
