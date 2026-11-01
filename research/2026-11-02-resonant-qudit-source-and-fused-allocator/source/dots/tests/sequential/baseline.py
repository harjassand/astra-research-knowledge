import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla, json
from pathlib import Path
D=11;eye=sp.eye(D,format='csc');tr=np.zeros(D*D);tr[np.arange(D)*(D+1)]=1

def edge(t,s):return sp.csc_matrix(([1.],([t],[s])),shape=(D,D))
def gain(L):return sp.kron(L.conjugate(),L,format='csc')
def diss(L):
 A=L.conj().T@L
 return gain(L)-.5*(sp.kron(eye,A,format='csc')+sp.kron(A.T,eye,format='csc'))
H=sp.csc_matrix((D,D));dec=[]
for j in (0,1):
 E=sum(edge(3+4*j+b,1+4*j+b) for b in (0,1));H+=E+E.T
 dec.append(sum(edge((5 if j==0 else 9)+b,3+4*j+b) for b in (0,1)))
prep=[(edge(1,0)+s*edge(2,0))/np.sqrt(2) for s in (1,-1)]
read=[(edge(0,9)+s*edge(0,10))/np.sqrt(2) for s in (1,-1)]
base=-1j*(sp.kron(eye,H)-sp.kron(H.T,eye))
for J in dec+read:base+=diss(J)
results=[]
for p in (0.,.001):
 for r in (.001,.01,.05,.1):
  L=base+r*((1-p)*diss(prep[0])+p*diss(prep[1]));A=L.tolil();A[0,:]=tr;b=np.zeros(D*D,complex);b[0]=1
  rho=sla.spsolve(A.tocsc(),b);Jc=gain(read[0]);Jw=gain(read[1]);K=L-Jc-Jw
  rw=sla.spsolve(K,-Jw@rho);mu=float(tr@rw.real)
  dv=sla.spsolve(K.conj().T,-tr.astype(complex));rhs=mu*tr-Jw.conj().T@dv;A=L.conj().T.tolil();A[0,:]=rho.conjugate();rhs[0]=0;hv=sla.spsolve(A.tocsc(),rhs)
  ev=[np.linalg.eigvalsh(v.reshape((D,D),order='F')) for v in (hv,hv+dv)]
  results.append(dict(r=r,p=p,wrong=mu,flux=float(tr@((Jc+Jw)@rho).real),predicted_flux=r/(1+5.5*r),positive_range=float(max(e.max() for e in ev)-min(e.min() for e in ev))))
Path(__file__).with_name('baseline.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
