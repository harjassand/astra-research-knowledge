"""Independent structure checks for backward-control refinement, not a numerical proof."""
import json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.linalg import expm
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);kron=s.kronecker_product
checks=0
for r in [s.Rational(3),s.Rational(10)]:
 for om in [s.Rational(0),s.Rational(2),s.Rational(100)]:
  K=kron(X,X)/3;H=kron(I,om*Z)
  B=2*kron(X,r*X-2*om*Y)/(3*(r*r+4*om*om))
  assert (-r*B+s.I*(H*B-B*H)+2*K).applyfunc(s.simplify)==s.zeros(4);checks+=1
  for z in [s.Rational(3,5)+s.I*s.Rational(4,5),1-s.I/3]:
   y=s.im(z);V=s.eye(4)+y*B
   lhs=-r*y*B+s.I*(H*V-V*H)+s.I*s.conjugate(z)*K*V-s.I*V*z*K
   rhs=s.I*y*s.conjugate(z)*K*B-s.I*y*z*B*K
   assert (lhs-rhs).applyfunc(s.simplify)==s.zeros(4);checks+=1
# Noncommuting source-coefficient eigenoperator example.
r=s.Rational(12);K=(kron(X,X)+kron(Y,Y)+kron(Z,Z))/7
Ls=[s.sqrt(r/4)*kron(p,I) for p in [X,Y,Z]]
gk=sum((L.H*K*L-(L.H*L*K+K*L.H*L)/2 for L in Ls),s.zeros(4))
assert gk==-r*K;checks+=1
assert max(abs(v) for v in K.eigenvals())==s.Rational(3,7);checks+=1
# Finite-horizon common dilation, with a retained measurement record mid-location.
x=np.array(X,complex);y=np.array(Y,complex);z=np.array(Z,complex);eye=np.eye(2);sm=np.array([[0,1],[0,0]],complex)
P=[np.kron(eye,np.diag([1,0])),np.kron(eye,np.diag([0,1]))]
def cross(Ha,Hb,Ls):
 M=np.kron(np.eye(4),1j*Ha)-np.kron((1j*Hb).T,np.eye(4))
 for L in Ls:
  D=L.conj().T@L;M+=np.kron(L.T,L.conj().T)-.5*np.kron(np.eye(4),D)-.5*np.kron(D.T,np.eye(4))
 return M
meas=sum(np.kron(p.T,p.conj().T) for p in P)
rows=[]
for omega in [0.,20.,2000.,10000.]:
 r=1200.;c=1.;tau=.1;R=20.;Ls=[np.sqrt(1600)*np.kron(sm,eye),np.sqrt(800)*np.kron(sm.conj().T,eye)]
 events=[('flow',.05,np.kron(x,z),0,np.kron(eye,omega*y)),('instrument',),('flow',.05,np.kron(x,z),0,np.kron(eye,omega*y)),('flow',.05,.7*np.kron(x,x),None,np.kron(eye,.3*omega*z)),('flow',.1,np.kron(x,y),1,np.kron(eye,omega*x))]
 branches=[((0,0),1.),((0,1),-1.),((1,0),-1.),((1,1),1.)]
 G=np.zeros((4,4),complex);diag=0.
 for aa,ca in branches:
  for bb,cb in branches:
   v=np.eye(4,dtype=complex).reshape(-1,order='F')
   for event in reversed(events):
    if event[0]=='instrument':v=meas@v;continue
    _,t,K,idx,H=event;ka=1 if idx is None else aa[idx];kb=1 if idx is None else bb[idx]
    v=expm(t*cross(H+ka*K,H+kb*K,Ls))@v
   O=v.reshape((4,4),order='F');G+=ca*cb*O
   if aa==bb:diag=max(diag,float(np.linalg.norm(O-np.eye(4),2)))
 ev=np.linalg.eigvalsh((G+G.conj().T)/2);amp=float(np.sqrt(max(0,ev[-1])))
 eta=float(np.sqrt(1+2*R*c/r)*np.exp(4*R*R*c*c*tau/r)/(R-1))
 assert ev[0]>-1e-8 and diag<1e-8 and amp<=eta**2+1e-8
 rows.append({'omega':omega,'common_dilation_fault_amplitude':amp,'uniform_proved_bound':eta**2,'same_branch_isometry_defect':diag,'mid_location_instrument':True,'record_retained_in_common_dilation':True,'source_reused':True,'outside_interaction_on':True})
out={'exact_identity_checks':checks,'floating_full_history_diagnostics':rows,'scope':'Exact stationary backward-weight/eigenoperator identities; floating finite-horizon full common-dilation tests with local measurement. Not a rigorous numerical certificate, experimental evidence or proof of finite-horizon theorem.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
