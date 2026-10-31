"""Exact weighted-generator checks and floating common-dilation diagnostics."""
import json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.linalg import expm
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
sm=s.Matrix([[0,1],[0,0]])
kron=s.kronecker_product
count=0
for lam,a in [(12,8),(2,18),(20,0)]:
 r=s.Rational(lam+a,2)
 jumps=[s.sqrt(lam)*kron(sm,I,I),s.sqrt(a)*kron(sm.H,I,I),s.sqrt(lam)*kron(I,sm,I),s.sqrt(a)*kron(I,sm.H,I)]
 def gs(O):
  return sum((L.H*O*L-(L.H*L*O+O*L.H*L)/2 for L in jumps),s.zeros(8))
 for eps in [s.Rational(0),s.Rational(1,37)]:
  K=kron(X,I,Z)/3+kron(I,X,X)/5+eps*kron(I,I,Z)
  J=gs(K)+r*K
  assert J==r*eps*kron(I,I,Z);count+=1
  for x,y in [(s.Rational(3,5),s.Rational(4,5)),(s.Rational(-2,3),s.Rational(-1,2)),(0,s.Rational(6,5))]:
   z=x+s.I*y;V=s.eye(8)+2*y*K/r
   lhs=gs(V)+s.I*s.conjugate(z)*K*V-s.I*V*z*K
   rhs=2*y*J/r+4*y*y*K*K/r
   assert (lhs-rhs).applyfunc(s.simplify)==s.zeros(8);count+=1
   # Exact positivity via principal-minor LDL decomposition (strict positive case).
   for M in [V-s.eye(8)/2,3*s.eye(8)/2-V]:
    _,D=M.LDLdecomposition(hermitian=True)
    assert all(v>0 for v in D.diagonal());count+=1
# Common initialized-field dilation cross overlaps, including outside interaction.
x=np.array(X,complex);y=np.array(Y,complex);z=np.array(Z,complex);eye=np.eye(2);smn=np.array(sm,complex)
def cross_super(Ha,Hb,Ls):
 d=len(Ha); eye=np.eye(d)
 M=np.kron(eye,1j*Ha)-np.kron((1j*Hb).T,eye)
 for L in Ls:
  D=L.conj().T@L
  M+=np.kron(L.T,L.conj().T)-.5*np.kron(eye,D)-.5*np.kron(D.T,eye)
 return M
rows=[]
for lam,a in [(2400.,0.),(1600.,800.),(24.,2376.)]:
 r=(lam+a)/2;c=1.;tau=.1;R=20.
 Ls=[np.sqrt(lam)*np.kron(smn,eye),np.sqrt(a)*np.kron(smn.conj().T,eye)]
 segments=[(.1,np.kron(x,z),0),(.05,.7*np.kron(x,x),None),(.1,np.kron(x,y),1)]
 branches=[((0,0),1.),((0,1),-1.),((1,0),-1.),((1,1),1.)]
 gram=np.zeros((4,4),complex)
 diag_defect=0.
 for aa,ca in branches:
  for bb,cb in branches:
   v=np.eye(4,dtype=complex).reshape(-1,order='F')
   for t,K,idx in reversed(segments):
    ka=1 if idx is None else aa[idx];kb=1 if idx is None else bb[idx]
    v=expm(t*cross_super(ka*K,kb*K,Ls))@v
   O=v.reshape((4,4),order='F');gram+=ca*cb*O
   if aa==bb:diag_defect=max(diag_defect,float(np.linalg.norm(O-np.eye(4),2)))
 herm=float(np.linalg.norm(gram-gram.conj().T,2));ev=np.linalg.eigvalsh((gram+gram.conj().T)/2)
 amplitude=float(np.sqrt(max(0.,ev[-1])))
 eta=float(np.exp(4*c*R/r+4*R*R*c*c*tau/r)/(R-1))
 assert herm<1e-9 and ev[0]>-1e-9 and diag_defect<1e-9 and amplitude<=eta**2+1e-9
 rows.append({'lambda':lam,'injection':a,'r':r,'selected_locations':[0,2],'outside_middle_on':True,'source_reused':True,'amplitude_operator_norm':amplitude,'proved_upper':eta**2,'gram_min_eigenvalue':float(ev[0]),'gram_hermiticity_defect':herm,'same_branch_isometry_defect':diag_defect})
out={'exact_checks':count,'common_dilation_checks':rows,'scope':'Exact rational operator identities/weight positivity. Floating cross-dilation matrix-exponential diagnostics are not rigorous numerical certificates or a proof of the theorem.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
