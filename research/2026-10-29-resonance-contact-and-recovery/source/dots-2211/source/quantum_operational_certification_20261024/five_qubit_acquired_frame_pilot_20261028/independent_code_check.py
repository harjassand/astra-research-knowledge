#!/usr/bin/env python3
"""Independent stabilizer/Kraus construction and complete PTM checks; no source draws."""
from pathlib import Path
import importlib.util,itertools,json,hashlib
import sympy as s
import numpy as np
D=Path(__file__).parent
sp=importlib.util.spec_from_file_location('code',D/'code_and_channels.py');a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);ps=[I,X,Y,Z]
def kr(xs):
 r=s.ones(1,1)
 for x in xs:r=s.kronecker_product(r,x)
 return r
strings=['XZZXI','IXZZX','XIXZZ','ZXIXZ'];lookup=dict(zip('IXYZ',ps));gs=[kr([lookup[c] for c in w]) for w in strings]
Proj=s.eye(32)
for g in gs:Proj=Proj*(s.eye(32)+g)/2
assert Proj*Proj==Proj and s.trace(Proj)==2
v0=4*Proj[:,0];v1=kr([X]*5)*v0;V=v0.row_join(v1);assert V.H*V==I
E=[s.eye(32)]+[kr([ps[j] if k==site else I for k in range(5)]) for site in range(5) for j in [1,2,3]]
# Exact rational Knill-Laflamme and recovery-TP identities.
EV=[e*V for e in E]
for i,j in itertools.product(range(16),repeat=2):assert EV[i].H*EV[j]==(I if i==j else s.zeros(2))
Rec=[v.H for v in EV];assert sum((r.H*r for r in Rec),s.zeros(32))==s.eye(32)
Vauthor,Rauthor=a.exact_encoder_recovery();assert V==Vauthor and Rec==Rauthor
# Recover the polynomial coefficients from syndrome conjugation, not weight assumption.
wordcoeff=[]
for coset in a.COS:
 for word,sign in coset:
  pp=kr([ps[x] for x in word]);corr=sum((e.H*pp*e for e in E),s.zeros(32));weight=sum(x!=0 for x in word)
  assert corr==(16-4*weight)*pp;wordcoeff.append(weight)
Pn=[np.array(x,complex) for x in ps];Vn=np.array(V,complex);Rn=[np.array(r,complex) for r in Rec]
def direct(Ks):
 globalKs=[np.array([[1]],complex)]
 for local in Ks:globalKs=[np.kron(g,np.array(l,complex)) for g in globalKs for l in local]
 Ls=[r@g@Vn for r in Rn for g in globalKs]
 T=np.array([[sum(np.trace(Pn[i]@l@Pn[j]@l.conj().T).real/2 for l in Ls) for j in range(4)] for i in range(4)])
 return T,float(np.linalg.norm(sum(l.conj().T@l for l in Ls)-np.eye(2)))
src=a.generator_sources();cases=[]
for mode in ['identity','ideal_residual','unremoved_frames']:
 if mode=='identity':Ks=[[I] for _ in range(5)]
 elif mode=='ideal_residual':Ks=[[(r['frame_V'].H*k).applyfunc(s.cancel) for k in r['Ks']] for r in src]
 else:Ks=[r['Ks'] for r in src]
 local=[a.exact_ptm(k) for k in Ks];poly=a.logical_ptm(local);dense,tp=direct(Ks);err=float(np.max(abs(dense-np.array(poly,float))));assert err<1e-12 and tp<1e-12
 failures=a.holdout_failure_probabilities(poly);assert s.cancel(sum(failures)/6)==s.Rational(2,3)*a.infidelity(poly)
 cases.append({'mode':mode,'complete_PTM_max_difference':err,'logical_TP_residual':tp,'entanglement_infidelity':float(a.infidelity(poly)),'six_state_mean_failure':float(sum(failures)/6)})
out={'status':'PASS_INDEPENDENT_STANDARD_CODE_AND_COMPLETE_PTM','exact_Knill_Laflamme_pairs':256,'exact_recovery_TP':True,'exact_syndrome_Pauli_coefficients':len(wordcoeff),'complete_Kraus_PTM_cases':cases,'source_draws':0,'scope':'Exact standard code identities and floating direct-Kraus validation of exact Pauli polynomial, not hardware or acquired holdout','sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [Path(__file__),D/'code_and_channels.py']}}
(D/'independent_code_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
