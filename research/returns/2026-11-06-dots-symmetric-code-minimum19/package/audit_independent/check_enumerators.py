import sys,numpy as np,sympy as s
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from audit_lift import cg
from sympy.physics.wigner import wigner_6j
rng=np.random.default_rng(314)
for n in range(1,7):
 D=n+1;j=n/2;sj=s.Rational(n,2);K=2
 Q=np.linalg.qr(rng.normal(size=(D,K))+1j*rng.normal(size=(D,K)))[0];P=Q@Q.conj().T;a=[];b=[]
 for k in range(D):
  aa=bb=0
  for q in range(-k,k+1):
   T=np.array([[np.sqrt((2*k+1)/D)*cg(j,k,j,m-j,q,mp-j)for m in range(D)]for mp in range(D)])
   aa+=abs(np.trace(P@T))**2;bb+=np.trace(P@T.conj().T@P@T).real
  a.append(D/K**2*aa);b.append(D/K*bb)
 M=np.array([[(2*k+1)*(-1)**(n+k+l)*float(wigner_6j(sj,sj,k,sj,sj,l))for l in range(D)]for k in range(D)])
 PP=np.kron(P,P);w=[]
 for l in range(D):
  V=np.array([[cg(j,j,l,i-j,k-j,m)for m in range(-l,l+1)]for i in range(D)for k in range(D)])
  w.append(np.trace(V.T@PP@V).real)
 errM=max(abs(np.array(b)-K*M@a));errw=max(abs(np.array(w)-(K*K/D)*M@(np.array([(-1)**l for l in range(D)])*a)))
 assert errM<1e-10 and errw<1e-10
 print(n,'M identity',errM,'pair weights',errw,'sum a',sum(a),flush=True)
