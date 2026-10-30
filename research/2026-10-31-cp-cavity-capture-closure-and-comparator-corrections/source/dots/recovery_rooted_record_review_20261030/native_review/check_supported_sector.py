import numpy as np,json
rng=np.random.default_rng(431)
def pos(n):
 A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));return A.conj().T@A+np.eye(n)
def root(A,p):
 d,U=np.linalg.eigh(A);return (U*d**p)@U.conj().T
worst=0.;noncomm=0.
for _ in range(100):
 F=np.zeros((6,6),complex);F[:2,:2]=pos(2);F[2:,2:]=pos(4)
 R=np.diag([0,0,1,1,1,1]);P=np.diag([0,0,1,0,1,0]);H=P
 G=np.eye(6)+.3*F
 C=np.linalg.norm(root(G,-.5)@H@root(G,.5),2)
 D=1j*(H@G-G@H)
 for sign in [-1,1]:
  mineig=np.linalg.eigvalsh(2*C*R@G-sign*D)[0];worst=min(worst,mineig);assert mineig>-1e-10
 noncomm=max(noncomm,np.linalg.norm(P@F-F@P))
print(json.dumps({'samples':100,'minimum_supported_bound_eigenvalue':worst,'nonzero_P_F_commutator_max':noncomm},indent=2))
