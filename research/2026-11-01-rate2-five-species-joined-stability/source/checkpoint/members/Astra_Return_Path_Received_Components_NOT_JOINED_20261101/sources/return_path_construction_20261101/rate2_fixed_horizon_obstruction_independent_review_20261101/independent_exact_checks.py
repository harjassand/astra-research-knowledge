#!/usr/bin/env python3
"""Exact support for the ordinary fixed-horizon rate-2 transfer review."""
import hashlib,json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
A,B,C,D,E,K,N=s.symbols('A B C D E K N', nonnegative=True)
x=(A,B,C,D,E)
cs={'0':(0,0,0,0,0),'A':(1,0,0,0,0),'2A':(2,0,0,0,0),
    'AB':(1,1,0,0,0),'AC':(1,0,1,0,0),'AD':(1,0,0,1,0),
    'AE':(1,0,0,0,1),'CD':(0,0,1,1,0)}
rs=[('0','A',1),('A','0',1),('2A','AC',1),('AC','2A',1),
    ('2A','AD',1),('AD','2A',1),('2A','AE',1),('AE','2A',1),
    ('AE','CD',1),('CD','AE',2),('CD','AB',1),('AB','CD',1)]
def prop(src,k):
    return k*s.prod(s.prod(v-j for j in range(y)) for v,y in zip(x,cs[src]))
def v(src,dst): return s.Matrix(cs[dst])-s.Matrix(cs[src])
F=s.zeros(5,1)
qbad=0
for src,dst,k in rs:
    p=prop(src,k); F+=p*v(src,dst)
    if cs[src][0] and (src,dst)!=('AB','CD'): qbad+=p
F=F.applyfunc(s.expand); qbad=s.expand(qbad)
LA=1-A-3*A*(A-1)+A*(C+D)+3*C*D-A*B
qb=A+3*A*(A-1)+A*(C+D+2*E)
upper=1+3*K*K-(N/s.Integer(2)-K)*A
# These are nonnegative on the stopped count region; A(A-1)>=0 for integer A.
drift_certificate=3*(K*K-C*D)+A*(B-N/s.Integer(2))+A*(K-C-D)+A+3*A*(A-1)
q_certificate=A*(3*(K-A)+2*(K-C-D-E)+(C+D)+3)
retained=[('0','A',1),('AB','CD',1),('CD','AB',1),('CD','AE',2)]
aug_jumps=[s.Matrix(list(v(u,w))+[1 if u=='0' else 0]) for u,w,k in retained]
invariant_rows=[s.Matrix([[1,0,1,0,0,-1]]),s.Matrix([[1,0,0,1,0,-1]]),s.Matrix([[-1,1,0,0,1,1]])]
paths={
 'target':(HERE.parent/'rate2_fixed_horizon_obstruction/RATE2_FIXED_HORIZON_ADDENDUM.md','415edfdf0829c1a95935bc200547d286a639f11e60f6366383be6548fa2d4232'),
 'original_root':(HERE.parent.parent/'neutral_return_obstruction_root_20261101/STABLE_PATH_NETWORK_BOUNDED_PROFILE_OBSTRUCTION.md','0f6a4405e9566b070100322606f004ea1f58dda08fd7ea46d03cec1da8d3e478'),
 'original_receipt':(HERE.parent/'root_obstruction_audit/INDEPENDENT_REVIEW.md','4321f9200831c54d5b33f5e430fad8ede9759b5d7392ccd18115fa46ef020590'),
}
checks={name+'_hash':hashlib.sha256(p.read_bytes()).hexdigest()==h for name,(p,h) in paths.items()}
checks.update({
 'exact_full_generator_A':s.expand(F[0]-LA)==0,
 'exact_bad_intensity':s.expand(qbad-qb)==0,
 'exact_total_drift':s.expand(sum(F)-(1-A))==0,
 'drift_bound_nonnegative_decomposition':s.expand(upper-LA-drift_certificate)==0,
 'bad_intensity_nonnegative_decomposition':s.expand((1+5*K)*A-qb-q_certificate)==0,
 'all_retained_linear_invariants':all((row*j)[0]==0 for row in invariant_rows for j in aug_jumps),
 'E_count_is_CD_to_AE_only':all(j[4]==(1 if (u,w)==('CD','AE') else 0) for j,(u,w,k) in zip(aug_jumps,retained)),
 'retained_CD_to_AE_rate_is_exactly_two_CD':prop('CD',2)==2*C*D,
 'all_internal_total_jumps_zero':all(sum(v(u,w))==0 for u,w,k in rs if u!='0' and w!='0'),
 'port_total_jumps_plus_and_minus_one':sum(v('0','A'))==1 and sum(v('A','0'))==-1,
})
checks={k:bool(v) for k,v in checks.items()}
r={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
   'scope':'Exact algebra only; probability/UI/Foster arguments are reviewed in INDEPENDENT_REVIEW.md.',
   'full_count_drift':[str(v) for v in F],'bad_intensity':str(qbad),
   'rate1_stationary_law_transferred':False}
(HERE/'independent_exact_results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
assert all(checks.values())
