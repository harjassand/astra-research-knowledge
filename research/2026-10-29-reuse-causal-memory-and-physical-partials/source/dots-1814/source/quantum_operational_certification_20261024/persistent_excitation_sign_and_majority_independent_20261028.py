#!/usr/bin/env python3
"""Independent algebra checks for acquired gaps and genuine majority extraction."""
import itertools,json
import numpy as np
from scipy.linalg import expm
from fractions import Fraction as F
from pathlib import Path
import sympy as S
P=[np.eye(2,dtype=complex),np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.]).astype(complex)]
def kron(xs):
 r=np.ones((1,1),complex)
 for x in xs:r=np.kron(r,x)
 return r
def op(x):return float(np.linalg.norm(x,2))
def sign(x):
 vals,vec=np.linalg.eigh(x);return vec@np.diag(np.where(vals>=0,1.,-1.))@vec.conj().T
maxr={'two_gap_sign':0.,'one_gap_sign':0.,'direct_gap_sign':0.,'majority_identity':0.,'full_gauge_receiver':0.};signcases=[]
for d in [2,4,8]:
 z=np.diag([1.]*(d//2)+[-1.]*(d//2));base=np.array([[np.sin((i+1)*(j+2)) for j in range(d)] for i in range(d)]);H=(base+base.T)/2
 V=expm(.31j*H);B=V@z@V.conj().T
 for gscale in [.02,.13,.6]:
  R0=np.diag([gscale*(1+.11*i) for i in range(d)])
  # Noncommuting within-sign gauge blocks, commuting exactly with z.
  within=H.copy();within[:d//2,d//2:]=0;within[d//2:,:d//2]=0
  L=expm(.23j*within);R=V@L@R0@L.conj().T@V.conj().T;Delta=B@R;g=np.linalg.eigvalsh(R).min()
  E0=H+.17j*(np.triu(H,1)-np.triu(H,1).T);E0/=op(E0)
  for ratio in [.02,.15,.4,.8]:
   C=Delta+ratio*g*E0;e=op(C-Delta);h=np.min(np.abs(np.linalg.eigvalsh(C)));SS=sign(C);error=op(SS-B)
   maxr['two_gap_sign']=max(maxr['two_gap_sign'],error-2*e/(g+h))
   maxr['one_gap_sign']=max(maxr['one_gap_sign'],error-2*e/(2*g-e))
   if h>e:maxr['direct_gap_sign']=max(maxr['direct_gap_sign'],error-2*e/(2*h-e))
   signcases.append({'dimension':d,'true_gap':g,'error_radius':e,'observed_gap':h,'actual_sign_error':error})
# Repetition permutation with all coherent one-bit syndrome sectors.
U=np.zeros((8,8),complex);errs=[0,4,2,1]
for l,g in itertools.product(range(2),range(4)):U[(7*l)^errs[g],4*l+g]=1
BX=U@np.kron(P[1],np.eye(4))@U.conj().T;BZ=U@np.kron(P[3],np.eye(4))@U.conj().T
XXX=kron([P[1]]*3);Zs=[kron([P[3] if k==i else P[0] for k in range(3)]) for i in range(3)]
majority=(sum(Zs)-Zs[0]@Zs[1]@Zs[2])/2
assert np.array_equal(BX,XXX) and np.array_equal(BZ,majority)
assert np.array_equal(BX@BZ+BZ@BX,np.zeros((8,8)))
# Exactly rational stereographic Jacobi approximation to the XXX eigenspaces.
r=F(41,99);c=(1-r*r)/(1+r*r);s=2*r/(1+r*r);g=F(1,8)
Q=S.eye(8)
for a in range(4):
 b=7-a;Q[a,a]=S.Rational(c.numerator,c.denominator);Q[b,b]=Q[a,a];Q[b,a]=S.Rational(s.numerator,s.denominator);Q[a,b]=-Q[b,a]
SX=Q*S.diag(*([1]*4+[-1]*4))*Q.T
assert Q.T*Q==S.eye(8) and SX*SX==S.eye(8) and SX==SX.T
BXexact=S.Matrix(BX.real.astype(int));diff=SX-BXexact
exact_error2=F(str((diff*diff)[0,0]));assert diff*diff==S.Rational(exact_error2.numerator,exact_error2.denominator)*S.eye(8)
h=2*g*c*s;e=g*abs(c*c-s*s);bound=2*e/(g+h);direct=2*e/(2*h-e)
assert exact_error2<=bound*bound and exact_error2<=direct*direct and h>e
SXfloat=np.array(SX,float).astype(complex)
# Actual mixed-ancilla three-controlled-reflection circuit; retains whole R reference.
phi=np.zeros((4,4),complex);v=np.array([1,0,0,1])/np.sqrt(2);phi=np.outer(v,v)
Bell_RA=np.zeros((32,32),complex)
for a,b in itertools.product(range(2),repeat=2):
 ea=np.zeros((2,2));ea[a,b]=1;Bell_RA+=np.kron(np.kron(ea,np.eye(8)),ea)/2
source=np.kron(np.eye(2),np.kron(U,np.eye(2)))
def gauge_bell_operator(sx,sz):
 CZ=np.kron((np.eye(8)+sz)/2,P[0])+np.kron((np.eye(8)-sz)/2,P[1])
 CX=np.kron(np.eye(8),np.diag([1.,0.]))+np.kron(sx,np.diag([0.,1.]))
 W=CZ@CX@CZ;full=np.kron(np.eye(2),W)@source;T=np.zeros((4,4),complex)
 for a,b in itertools.product(range(4),repeat=2):
  gh=np.zeros((4,4),complex);gh[a,b]=1
  inp=np.kron(np.kron(phi,gh),P[0]/2)
  Fg=np.trace(Bell_RA@full@inp@full.conj().T);T[b,a]=Fg
 return T
T_exact=gauge_bell_operator(BX,BZ);assert op(T_exact-np.eye(4))<1e-12
T_rational=gauge_bell_operator(SXfloat,BZ);worst=1-np.linalg.eigvalsh(T_rational).min();certificate=1.5*float(exact_error2)
maxr['full_gauge_receiver']=max(maxr['full_gauge_receiver'],worst-certificate)
# A noncommuting perturbed signed pair, then the actual physical sign receiver.
fixtureH=np.array([[np.sin((a+2)*(b+3)) for b in range(8)] for a in range(8)]);fixtureH=(fixtureH+fixtureH.T)/2;fixtureH/=op(fixtureH)
sx=sign(BX/8+.0007*fixtureH);sz=sign(BZ/8+.0005*fixtureH)
T_pert=gauge_bell_operator(sx,sz);worst_pert=1-np.linalg.eigvalsh(T_pert).min();cert_pert=3*(op(sz-BZ)**2+op(sx-BX)**2/2)
maxr['full_gauge_receiver']=max(maxr['full_gauge_receiver'],worst_pert-cert_pert)
# Explicit ordinary one-copy Pauli Born laws for the full-support training gauge.
unsigned=np.zeros((8,8),complex);signed={1:np.zeros((8,8),complex),3:np.zeros((8,8),complex)};born_total=0.;born_events=0
for j,sgn in itertools.product([1,3],[-1,1]):
 rhoin=np.kron((P[0]+sgn*P[j])/2,np.eye(4)/4);out=U@rhoin@U.conj().T
 for axes in itertools.product([1,2,3],repeat=3):
  for bits in itertools.product([-1,1],repeat=3):
   pis=[(P[0]+b*P[a])/2 for a,b in zip(axes,bits)];prob=np.trace(out@kron(pis)).real/(4*27)
   assert prob>=-1e-14
   shadow=kron([3*pi-P[0] for pi in pis]);unsigned+=prob*shadow;signed[j]+=2*sgn*prob*shadow
   born_total+=prob;born_events+=1
assert abs(born_total-1)<1e-12 and op(unsigned-np.eye(8)/8)<1e-12
assert op(signed[1]-BX/8)<1e-12 and op(signed[3]-BZ/8)<1e-12
# Pure/coherent/mixed future gauge states, not restricted to the calibration state.
gauge_states=[np.diag([1.,0,0,0]),np.ones((4,4))/4,np.diag([.4,.3,.2,.1])]
Vg=expm(.31j*np.array([[0,1,0,.2],[1,0,.3,0],[0,.3,0,.7],[.2,0,.7,0]]));gauge_states.append(Vg@np.diag([.52,.28,.15,.05])@Vg.conj().T)
future_losses=[]
for gh in gauge_states:
 assert abs(np.trace(gh)-1)<1e-12 and np.linalg.eigvalsh(gh).min()>-1e-12
 assert abs(np.trace(T_exact@gh)-1)<1e-12
 loss=1-np.trace(T_rational@gh).real;assert loss<=certificate+1e-12
 future_losses.append(loss)
# Retain a maximally entangled gauge-memory purifier and the complete logical reference.
vecGM=np.eye(4).reshape(-1)/2;rhoGM=np.outer(vecGM,vecGM)
inp=np.kron(np.kron(phi,rhoGM),P[0]/2).reshape(2,2,4,4,2,2,2,4,4,2)
inp=inp.transpose(0,1,2,4,3,5,6,7,9,8).reshape(128,128)
CZ=np.kron((np.eye(8)+BZ)/2,P[0])+np.kron((np.eye(8)-BZ)/2,P[1])
CX=np.kron(np.eye(8),np.diag([1.,0.]))+np.kron(BX,np.diag([0.,1.]))
allW=np.kron(np.eye(2),np.kron(CZ@CX@CZ,np.eye(4)))@np.kron(np.eye(2),np.kron(U,np.eye(8)))
rhoout=allW@inp@allW.conj().T
# dims R,P,A,M; sum physical P on bra and ket.
rr=rhoout.reshape(2,8,2,4,2,8,2,4);outRAM=np.trace(rr,axis1=1,axis2=5).reshape(16,16)
expectedRAM=np.kron(phi,np.eye(4)/4);purified_residual=op(outRAM-expectedRAM);assert purified_residual<1e-12
assert max(maxr.values())<2e-11,maxr
result={'status':'PASS acquired-gap/sign/majority algebra','source_draws':0,'rng_draws':0,'sign_perturbation_fixtures':len(signcases),'exact_majority_and_XXX_identities':True,'exact_rational_sign_physicality':True,'exact_rational_sign_error_squared':str(exact_error2),'exact_rational_two_gap_bound':str(bound),'exact_rational_direct_gap_bound':str(direct),'exact_sign_full_gauge_Bell_operator_residual':op(T_exact-np.eye(4)),'rational_sign_worst_gauge_loss':worst,'rational_sign_colored_upper':certificate,'perturbed_pair_worst_gauge_loss':worst_pert,'perturbed_pair_colored_upper':cert_pert,'ordinary_Pauli_Born_events':born_events,'ordinary_total_probability':born_total,'unsigned_shadow_identity_residual':op(unsigned-np.eye(8)/8),'signed_shadow_identity_residuals':[op(signed[1]-BX/8),op(signed[3]-BZ/8)],'future_pure_mixed_gauge_fixtures':len(gauge_states),'future_gauge_losses':future_losses,'full_reference_entangled_memory_product_residual':purified_residual,'maximum_positive_residuals':maxr,'sign_fixtures':signcases}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='sign_fixtures'},indent=2))
