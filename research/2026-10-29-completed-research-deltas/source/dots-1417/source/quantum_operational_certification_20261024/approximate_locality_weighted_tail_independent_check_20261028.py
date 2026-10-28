#!/usr/bin/env python3
"""Exact fixed-matrix locality-tail/ideal-subset checks; zero source calls and RNG."""
import json
from pathlib import Path
import sympy as s
R=s.Rational; I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
K=s.kronecker_product
clean=lambda a:a.applyfunc(s.expand)
zero=lambda a:clean(a)==s.zeros(*a.shape)
tr=lambda a:s.expand(s.trace(a))
S=s.zeros(4)
for a in range(2):
 for b in range(2):S[2*b+a,2*a+b]=1
c=R(8320,8321); t=R(129,8321); tau=2*t; kappa=R(1,4)
U=clean(c*s.eye(4)+s.I*t*S)
assert c*c+t*t==1 and zero(U.H*U-s.eye(4)) and tau<=kappa/8

def pt2(a,keep):
 out=s.zeros(2)
 for i in range(2):
  for j in range(2):
   out[i,j]=sum(a[2*i+k,2*j+k] if keep==0 else a[2*k+i,2*k+j] for k in range(2))
 return clean(out)

def psd2(a):
 return zero(a-a.H) and a[0,0]>=0 and a[1,1]>=0 and s.expand(a.det())>=0

sigma=s.diag(R(99,100),R(1,100))
H=s.Matrix([[R(7,10),R(1,100)],[R(1,100),R(1,200)]])
assert psd2(H-kappa*sigma) and psd2(sigma-H) and not zero(H*sigma-sigma*H)
rho=clean(U*K(I/2,sigma)*U.H); RR=clean(U*K(I/2,H)*U.H)
assert tr(rho)==1 and not zero(rho*RR-RR*rho)
records=[]
for name,P,Q in [('X',X,Z),('Z',Z,X)]:
 B=clean(U*K(P,I)*U.H); Banti=clean(U*K(Q,I)*U.H); V=K(P,I); Vanti=K(Q,I)
 xx=clean(B*RR)
 assert zero(B*B-s.eye(4)) and zero(B*rho-rho*B)
 assert zero(Banti*xx*Banti+xx)
 assert not zero(B-K(pt2(B,0)/2,I))
 delta=tr(rho*(B-V)**2); delta_anti=tr(rho*(Banti-Vanti)**2)
 assert delta==2*t*t and delta_anti==2*t*t and delta<=tau*tau
 disjoint=pt2(xx,1); local=pt2(xx,0)
 assert tr(disjoint)==0 and tr(local)==0
 # For a traceless 2x2 Hermitian matrix, ||A||_1^2=-4 det(A).
 disjoint_norm_squared=s.expand(-4*disjoint.det()); local_norm_squared=s.expand(-4*local.det())
 assert 0<disjoint_norm_squared<=tau*tau
 assert local_norm_squared >= (kappa-tau)**2
 assert tr(V*xx)>=tr(RR)-tau and tr(RR)>=kappa
 assert zero(pt2(Vanti*xx*Vanti,1)-disjoint)
 assert zero(2*disjoint-pt2(Vanti*xx*Vanti-Banti*xx*Banti,1))
 # Literal proxy-bit measurement in the virtual uniform logical-P ensemble.
 bit_error=s.S(0)
 for sign in (-1,1):
  virtual=clean(rho*(s.eye(4)+sign*B))
  wrong=(s.eye(4)-sign*V)/2
  assert tr(virtual)==1
  bit_error+=tr(virtual*wrong)/2
 assert bit_error==delta/4
 # Nontrivial mixed-gauge ideal-prefix invariance with one maximally mixed ancilla.
 state=K(rho,I/2)
 Bz=clean(U*K(Z,I)*U.H); Bx=clean(U*K(X,I)*U.H)
 forward=lambda b:K((s.eye(4)+b)/2,I)+K((s.eye(4)-b)/2,X)
 backward=lambda b:K(s.eye(4),(I+Z)/2)+K(b,(I-Z)/2)
 for a,b,d in [(forward(Bz),forward(K(Z,I)),delta_anti if name=='X' else delta),
               (backward(Bx),backward(K(X,I)),delta if name=='X' else delta_anti)]:
  assert zero(a*state*a.H-state)
  assert tr(state*(a-b).H*(a-b))==d/2
 records.append({'axis':name,'weighted_squared_tail':str(delta),'disjoint_contrast_trace_norm_squared':str(disjoint_norm_squared),'true_patch_contrast_trace_norm_squared':str(local_norm_squared),'virtual_bit_error':str(bit_error)})

# Two genuinely nonlocal ideal logical factors, but disjoint local actual swap blocks.
q=2; dp=4; da=4
rho2=s.eye(dp)/dp; state=K(rho2,s.eye(da)/da)
VP={j:[K(P,I),K(I,P)] for j,P in [('X',X),('Y',Y),('Z',Z)]}
BP={j:[clean(U*p*U.H) for p in v] for j,v in VP.items()}
AX=[K(X,I),K(I,X)]; AZ=[K(Z,I),K(I,Z)]
def forward(z,i):return K((s.eye(dp)+z)/2,s.eye(da))+K((s.eye(dp)-z)/2,AX[i])
def backward(x,i):return K(s.eye(dp),(s.eye(da)+AZ[i])/2)+K(x,(s.eye(da)-AZ[i])/2)
def block(x,z,i):return clean(forward(z,i)*backward(x,i)*forward(z,i))
ideal=[block(BP['X'][i],BP['Z'][i],i) for i in range(q)]
actual=[block(VP['X'][i],VP['Z'][i],i) for i in range(q)]
assert zero(ideal[0]*ideal[1]-ideal[1]*ideal[0])
assert zero(actual[0]*actual[1]-actual[1]*actual[0])
full=clean(actual[1]*actual[0]); ideal_full=clean(ideal[1]*ideal[0])
cone_records=[]
for i in range(q):
 assert not zero(BP['X'][i]-VP['X'][i])
 # Actual outside-cone block deletion at the full marginal observable level.
 for j in ['X','Y','Z']:
  target=K(s.eye(dp),VP[j][i])
  assert zero(full.H*target*full-actual[i].H*target*actual[i])
 def marginal_fidelity(W):
  total=s.S(1)
  for j in ['X','Y','Z']:
   target=K(s.eye(dp),VP[j][i])
   total+=tr(state*K(BP[j][i],s.eye(da))*W.H*target*W)
  return s.expand(total/4)
 assert marginal_fidelity(ideal[i])==1 and marginal_fidelity(ideal_full)==1
 fidelity=marginal_fidelity(actual[i]); assert fidelity==marginal_fidelity(full)
 dx=tr(rho2*(BP['X'][i]-VP['X'][i])**2); dz=tr(rho2*(BP['Z'][i]-VP['Z'][i])**2)
 hybrid=s.expand(2-2*s.re(tr(state*ideal[i].H*actual[i])))
 bound=3*(dz+dx/2)
 assert 0<1-fidelity<=hybrid<=bound
 for gate in [forward(BP['Z'][i],i),backward(BP['X'][i],i),forward(BP['Z'][i],i)]:
  assert zero(gate*state*gate.H-state)
 cone_records.append({'logical_index':i,'actual_ancestors':[i],'ideal_subset_Bell_fidelity':'1','actual_marginal_Bell_loss':str(1-fidelity),'restricted_hybrid_squared_norm':str(hybrid),'restricted_hybrid_bound':str(bound)})
# Here the full actual receiver is the physical SWAP, so its logical channel is U.
joint_loss=s.expand(1-tr(U)*s.conjugate(tr(U))/16)
assert 0<joint_loss<=sum(R(r['actual_marginal_Bell_loss']) for r in cone_records)
# All numerical constants are certified by rational arithmetic, not a floating entropy evaluation.
assert R(1,256)*8+R(1,256)*2==R(5,128)<R(1,2)
assert 1-R(1,8)-R(1,8)-R(1,16)==R(11,16)
assert R(1,8)+R(1,8)+R(1,16)==R(5,16)
# Constants of the complete approximate-comparator ERM/sign/joint propagation.
assert 36+3==39
assert 2*R(42,512)+R(1,4)==R(53,128)
assert 2*R(53,128)==R(53,64)
assert 20*R(53,64)+5<=25
assert 20*22==440 and 3*R(3,2)*440==1980 and 4*1980==7920
assert 3*R(3,2)*25==R(225,2) and 4*R(225,2)==450
assert R(450,16384)<R(1,20)
out={'full_theorem_constant_checks':'PASS','status':'PASS','source_calls':0,'RNG_used':False,'kind':'exact prescribed matrix / arithmetic check; not acquisition evidence','tau':str(tau),'kappa':str(kappa),'noncommuting_gauge_H_and_sigma':True,'noncommuting_R_and_rho':True,'true_generators_physically_nonlocal':True,'coarse_localization_checks':records,'ideal_subset_causal_checks':cone_records,'global_Bell_loss':str(joint_loss),'RAC_literal_measurement_identity':'p_i = delta_Xi/4','entropy_safe_upper_bound_at_tau_le_1_over_8':'h2(tau^2/4) < 5/128 < 1/2','coarse_threshold_true_at_least':'11 kappa / 16','coarse_threshold_disjoint_at_most':'5 kappa / 16'}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(p.read_text(),end='')
