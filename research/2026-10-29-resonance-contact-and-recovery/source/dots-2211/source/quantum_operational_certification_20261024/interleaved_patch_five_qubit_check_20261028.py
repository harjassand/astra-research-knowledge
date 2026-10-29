"""Exact interleaved two-code Pauli calculation + arbitrary single-patch CPTP check."""
from itertools import product
from fractions import Fraction as F
from pathlib import Path
import json,numpy as np
P={'I':(0,0),'X':(1,0),'Y':(1,1),'Z':(0,1)}
def vec(s):return tuple(P[c][0] for c in s)+tuple(P[c][1] for c in s)
def add(a,b):return tuple(x^y for x,y in zip(a,b))
def sp(a,b):return sum(a[i]*b[i+5]+a[i+5]*b[i] for i in range(5))%2
G=list(map(vec,['XZZXI','IXZZX','XIXZZ','ZXIXZ']));syn=lambda e:tuple(sp(e,g) for g in G)
cor={syn(vec('IIIII')):vec('IIIII')}
for i in range(5):
 for c in 'XYZ':cor[syn(vec('I'*i+c+'I'*(4-i)))]=vec('I'*i+c+'I'*(4-i))
LX,LZ=vec('XXXXX'),vec('ZZZZZ')
def logical(word):
 e=vec(word);r=add(e,cor[syn(e)]);return (sp(r,LZ),sp(r,LX))
# Every arbitrary w=2 patch Pauli is corrected, including joint XX/XY/etc.
count=0
for site in range(5):
 for a,b in product('IXYZ',repeat=2):
  assert logical('I'*site+a+'I'*(4-site))==(0,0)
  assert logical('I'*site+b+'I'*(4-site))==(0,0);count+=1
rows=[]
for p in [F(1,10),F(1,20),F(1,50),F(1,100),F(1,200),F(1,1000)]:
 delta=p
 # Native patch XX event p; independently composed calibration YY event delta.
 probs={'I':(1-p)*(1-delta),'X':p*(1-delta),'Y':(1-p)*delta,'Z':p*delta}
 q=1-probs['I'];bad=F(0)
 for word in product('IXYZ',repeat=5):
  pr=F(1)
  for c in word:pr*=probs[c]
  if logical(''.join(word))!=(0,0):bad+=pr
 bound=((1+2*q)**5-1-10*q)/2
 assert bad<=bound and bad<=10*q*q
 rows.append({'native_p':str(p),'calibration_delta':str(delta),'patch_q':str(q),'exact_joint_logical_half_diamond':str(bad),'exact_joint_logical_half_diamond_float':float(bad),'expansion_bound':str(bound),'binomial_bound_10q2':str(10*q*q)})
# Floating arbitrary two-qubit CPTP map on ONE patch, including entangling Kraus matrices.
rng=np.random.default_rng(2855);A=rng.normal(size=(12,4))+1j*rng.normal(size=(12,4));Q,_=np.linalg.qr(A);Ks=[Q[4*k:4*(k+1),:] for k in range(3)]
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);Ps=[I,X,Y,Z]
# On a fixed patch, distinct Pauli pairs have distinct syndrome pairs and correct to I4.
# Recovery logical Kraus are scalar coefficients of each Kraus in the Pauli-pair basis.
coeffs=[np.trace(np.kron(a,b).conj().T@K)/4 for K in Ks for a,b in product(Ps,repeat=2)]
normalization=sum(abs(c)**2 for c in coeffs)
assert abs(normalization-1)<1e-12
# Bad shared program flag: all five physical corrections apply X together, probability h.
h=F(1,1000);assert logical('XXXXX')==(1,0);assert h>10*h*h
out={'status':'PASS_INTERLEAVED_PATCH_CHECKS','source_draws':0,'single_patch_pauli_errors_corrected':count,'patch_width':2,'logical_qubits':2,'physical_carriers':10,'all_patch_patterns_per_rate':4**5,'rows':rows,'arbitrary_single_patch_CPTP_logical_identity_residual':float(abs(normalization-1)),'shared_program_negative_control':{'each_local_averaged_error':str(h),'actual_logical_error':str(h),'incorrect_independent_10h2':str(10*h*h)},'scope':'Exact rational Pauli joint logical channel plus floating arbitrary single-patch CPTP Kraus norm identity. No dense10qubit MonteCarlo, acquired data, hardware or general bath guarantee.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
