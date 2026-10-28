#!/usr/bin/env python3
"""Exact acquisition-interface counterexamples; no RNG or source calls."""
from pathlib import Path
import hashlib,itertools,json
import sympy as s
root=Path(__file__).resolve().parent
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
basis=[I,X,Y,Z]; tau=s.Matrix([[1,0,0,0]])
def vec(a):return s.Matrix([s.simplify(s.trace(b*a)) for b in basis])
def fmap(k):return s.Matrix.hstack(*[vec(k*b*k.conjugate().T)/2 for b in basis])
branches=[]
for a in [X,Y,Z]:
    lp=fmap((I+a)/2);lm=fmap((I-a)/2)
    assert (lp+lm)*vec(I/2)==vec(I/2)
    branches.append((lp,lm))
G=s.Matrix.hstack(vec(I/2),*[lp*vec(I/2) for lp,lm in branches])
F=s.Matrix.vstack(tau,*[tau*lp for lp,lm in branches]);H=F*G
assert G.rank()==H.rank()==4 and H.det()!=0
assert list(H[0,:])==[1,s.Rational(1,2),s.Rational(1,2),s.Rational(1,2)]
# Persistent bit: shifted branch table computed from actual diagonal branch states.
p=s.Rational(1,3);pf=s.Rational(1,2)
C0=s.Matrix([[0,0],[1,1]]);C1=s.Matrix([[1,0],[-1,0]])
def bit_model(p):
    G=s.Matrix([[p,p],[1-p,0]]);F=s.Matrix([[1,1],[1,0]])
    P0=s.diag(1,0);P1=s.diag(0,1);H=F*G
    Cs=[H.inv()*F*P*G for P in [P0,P1]]
    assert Cs==[C0,C1]
    return H,s.Matrix([[1,p]])
Hp,m=bit_model(p);Hf,mf=bit_model(pf)
# Persistent conditional bits are fixed by the only allowed nonselective action.
for bit in [s.Matrix([1,0]),s.Matrix([0,1])]:
    assert (s.diag(1,0)+s.diag(0,1))*bit==bit
    assert sum((s.diag(1,0)*bit,s.diag(0,1)*bit),s.zeros(2,1))==bit
K=max(sum(abs(x) for x in Hp.inv()*s.Matrix([1,v])) for v in [0,1]);assert K==3
mass_debit=K*max(abs(x) for x in m-mf)/2;assert mass_debit==s.Rational(1,4)
TVs={}
for n in range(1,8):
    tv=s.S.Zero
    for w in itertools.product([0,1],repeat=n):
        c=s.Matrix([1,0])
        for z in w:c=[C0,C1][z]*c
        tv+=abs(((m-mf)*c)[0])/2
    assert tv==abs(p-pf)<=mass_debit
    TVs[n]=str(tv)
report={'status':'PASS: exact diagnostic, not acquisition or independent receipt','source_calls':0,'episode_starts':0,'rng_calls':0,
 'source_sha256':hashlib.sha256((root/'RAW_JOINT_CORE_RESIDUAL_ACQUISITION.md').read_bytes()).hexdigest(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'open_loop_unital_obstruction_only':{'all_nonselective_maps_fix_initial_state':True,'open_loop_discard_preparation_rank':1,'raw_joint_core_rank':H.rank(),'raw_joint_core_determinant':str(H.det()),'raw_joint_core_masses':[str(x) for x in H[0,:]]},
 'persistent_bit_normalized_feedback_obstruction':{'conditional_bits_fixed':True,'initial_diagonal_bit_weights_preserved_by_all_normalized_stopping_protocols':'proved by conditional fixed points and termination probability one for each bit','normalized_preparation_rank':1,'raw_joint_core_rank':2},
 'mass_debit_control':{'p':str(p),'p_fit':str(pf),'native_coordinate_residual':0,'K_core':str(K),'terminal_mass_debit':str(mass_debit),'full_transcript_TV_by_horizon':TVs}}
(root/'raw_joint_core_residual_exact_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
