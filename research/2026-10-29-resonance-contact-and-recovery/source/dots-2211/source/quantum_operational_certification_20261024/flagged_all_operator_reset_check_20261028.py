"""Exact dyadic matrix checks of the all-operator noiseless reset identity.
Complex128 is used only for dyadic values; comparisons are exact array equality,
not tolerances. Matrix sizes32, all summands/products exactly representable.
"""
from itertools import product
from pathlib import Path
import json
import numpy as np
I=np.eye(2,dtype=complex)
P={'I':I,'X':np.array([[0,1],[1,0]],complex),'Z':np.diag([1,-1]).astype(complex),'Y':np.array([[0,-1j],[1j,0]])}
def mat(w):
 a=np.ones((1,1),complex)
 for c in w:a=np.kron(a,P[c])
 return a
G=list(map(mat,['XZZXI','IXZZX','XIXZZ','ZXIXZ']));ID=np.eye(32,dtype=complex)
words=['IIIII']+['I'*q+p+'I'*(4-q) for q in range(5) for p in 'XYZ']
E={}
for w in words:
 e=mat(w);s=tuple(int(np.array_equal(e@g,-g@e)) for g in G);E[s]=e
assert len(E)==16
projectors={};K={};first_hit_checks=0
for s in product((0,1),repeat=4):
 pi=ID.copy()
 for bit,g in zip(s,G):pi=pi@((ID+(-1)**bit*g)/2)
 assert np.array_equal(pi@pi,pi)
 assert np.trace(pi)==2
 projectors[s]=pi;K[s]=E[s]@pi
 if any(s):
  k=s.index(1);j=ID.copy()
  for h in range(k+1):j=j@((ID+(-1 if h==k else 1)*G[h])/2)
  assert np.array_equal(pi@j,pi)
  assert np.array_equal(E[s]@pi@j,K[s]);first_hit_checks+=1
zero=(0,0,0,0);pi0=projectors[zero]
assert np.array_equal(sum(k.conj().T@k for k in K.values()),ID)
for k in K.values():assert np.array_equal(pi0@k,k)
assert np.array_equal(K[zero],pi0)
# Composition Kraus K_s K_t is zero except s=0, where it equals K_t.
for s,ks in K.items():
 for t,kt in K.items():assert np.array_equal(ks@kt,kt if s==zero else np.zeros_like(kt))
out={'status':'PASS_EXACT_DYADIC_ALL_OPERATOR_KRAUS_IDENTITY','syndrome_sectors':16,'rank_each':2,'first_hit_nonzero_branches':first_hit_checks,'composition_kraus_pairs':256,'trace_preserving':True,'range_codespace':True,'idempotent_as_full_superoperator':True,'reference_extension':'Kraus identity implies equality after tensoring arbitrary reference','scope':'Noiseless syndrome projector instrument and physical Pauli correction; flag cancellation supplied by governing Clifford commutation proof, not re-simulated here.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
