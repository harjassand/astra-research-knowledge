"""Floating-point corroboration of backward/time-window and Young-split formulas."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
p=Path(__file__).parent
h=.8; kappa=1.6; lam=3.; v=.22
I=np.eye(2,dtype=complex); H=np.diag([0.,h]); L=np.array([[0,np.sqrt(2*h)],[0,0]],complex); V=v*np.array([[0,1],[1,0]],complex)
C2=h*v*v; rho=np.array([[.7,.2j],[-.2j,.3]],complex)
def S(q):
 D=L.conj().T@L; K=np.sqrt(lam)*V
 return -1j*(np.kron(I,K)-np.kron(K.T,I))+lam*((1+q)*np.kron(L.conj(),L)-.5*(np.kron(I,D)+np.kron(D.T,I)))
# Noncounted exposure before and after a counted window, q above basic stationary threshold.
segments=[(0.,.7,0.),(.7,1.2,.8),(1.2,1.6,0.)]
# Backward solution on each interval with right endpoint A.
boundaries=[None]*4; boundaries[3]=0.
for k in range(2,-1,-1):
 l,r,q=segments[k]; B=lam*(kappa/2-2*h*q); d=r-l
 boundaries[k]=np.exp(-B*d)*boundaries[k+1]+(2*lam*q*(-np.expm1(-B*d))/B if B else 2*lam*q*d)
def at(k,t):
 l,r,q=segments[k]; B=lam*(kappa/2-2*h*q); d=r-t
 return np.exp(-B*d)*boundaries[k+1]+(2*lam*q*(-np.expm1(-B*d))/B if B else 2*lam*q*d)
R=sum(quad(lambda t:2*at(k,t)*C2/kappa,l,r)[0] for k,(l,r,q) in enumerate(segments))
x=rho.reshape(-1,order='F')
for l,r,q in segments: x=expm((r-l)*S(q))@x
actual=np.trace(x.reshape(2,2,order='F')).real
bound=(1+boundaries[0]*np.trace(H@rho).real)*np.exp(R)
# Pointwise residual is bounded by r(t)*W(t), using explicit derivative.
res=[]
for k,(l,r,q) in enumerate(segments):
 for t in np.linspace(l,r,9):
  a=at(k,t); aprime=lam*((kappa/2-2*h*q)*a-2*q); W=I+a*H
  D=L.conj().T@L; K=np.sqrt(lam)*V
  adj=1j*(K@W-W@K)+lam*((1+q)*L.conj().T@W@L-.5*(D@W+W@D))
  residue=aprime*H+adj-(2*a*C2/kappa)*W
  res.append(np.linalg.eigvalsh((residue+residue.conj().T)/2).max())
# Optimized split extends admissible q from .5 to 1 in this TLS normalization.
sharpen=[]
for q in [.1,.49,.7,.95]:
 g=kappa-2*h*q; a=4*q/g; r=8*q*C2/g**2; W=I+a*H
 D=L.conj().T@L; K=np.sqrt(lam)*V
 adj=1j*(K@W-W@K)+lam*((1+q)*L.conj().T@W@L-.5*(D@W+W@D))
 actual2=np.trace((expm(.6*S(q))@rho.reshape(-1,order='F')).reshape(2,2,order='F')).real
 bound2=(1+a*np.trace(H@rho).real)*np.exp(.6*r)
 sharpen.append(dict(q=q,mgf=actual2,bound=bound2,residual_max_eigenvalue=float(np.linalg.eigvalsh(adj-r*W).max())))
out={'backward':{'segments':segments,'a_boundaries':boundaries,'R':R,'mgf':actual,'bound':bound,'max_residual_eigenvalue':max(res),'all_postwindow_a_zero':boundaries[2]==boundaries[3]==0.},'optimized_split':sharpen,'limitations':'Numerical floating-point checks, not exact arithmetic or interval certificates.'}
assert actual<=bound+1e-10; assert max(res)<1e-10
assert all(z['mgf']<=z['bound']+1e-10 and z['residual_max_eigenvalue']<1e-10 for z in sharpen)
(p/'check_backward.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
