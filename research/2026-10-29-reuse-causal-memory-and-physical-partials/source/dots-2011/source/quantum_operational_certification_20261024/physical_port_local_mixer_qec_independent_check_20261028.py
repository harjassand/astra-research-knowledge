#!/usr/bin/env python3
"""Exact physical framing/code CP reduction; no source samples or RNG."""
import itertools,json
from pathlib import Path
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
def kron(*xs):
    r=s.ones(1,1)
    for a in xs:r=s.kronecker_product(r,a)
    return r
def clean(A):return A.applyfunc(s.expand)
def unit(dim,a,b):
    E=s.zeros(dim);E[a,b]=1;return E
K=[s.diag(s.Rational(3,5),s.Rational(4,5)),s.Matrix([[0,s.Rational(3,5)],[s.Rational(4,5),0]])]
assert sum((A.H*A for A in K),s.zeros(2))==I and K[0]*K[1]!=K[1]*K[0]
P=[kron(I,I),kron(I,X),kron(X,I),kron(Z,I)]
logical=[I,I,X,Z]
weights=[[s.Rational(7,10),s.Rational(1,5),s.Rational(1,20),s.Rational(1,20)],
         [s.Rational(3,5),s.Rational(1,10),s.Rational(1,5),s.Rational(1,10)]]
assert all(sum(w)==1 for w in weights)
CN=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
V=clean(CN*(3*s.eye(4)-4*s.I*kron(Z,I))/5)
assert clean(V.H*V)==s.eye(4)
t=s.Rational(1,10);co=(1-t*t)/(1+t*t);si=2*t/(1+t*t)
PE=kron(Y,X);R=co*s.eye(4)-s.I*si*PE
b=si*si;assert clean(R.H*R)==s.eye(4)
Rhat=clean(R*V.H)
frames=[kron(A,B) for A,B in itertools.product([I,X,Y,Z],repeat=2)]
moment_entries=0;twirl_entries=0
for a,c in itertools.product(range(2),repeat=2):
    M=unit(2,a,c);km=[A*M*A.H for A in K];T=sum(km,s.zeros(2))
    F=[sum((weights[z][f]*km[z] for z in range(2)),s.zeros(2)) for f in range(4)]
    out=sum((kron(clean(V*P[f]*(s.eye(4)/4)*P[f].H*V.H),F[f]) for f in range(4)),s.zeros(8))
    assert out==kron(s.eye(4)/4,T);moment_entries+=64
    for G in [kron(X,I),kron(Z,I),kron(I,X),kron(I,Z)]:
        signs=[]
        for A in P:
            signs.append(1 if A*G==G*A else -1)
            assert A*G==signs[-1]*G*A
        # Positive scalar coefficient on every memory Kraus branch proves CP bias.
        assert all(sum(weights[z][f]*signs[f] for f in range(4))>=0 for z in range(2))
        H=sum((signs[f]*F[f] for f in range(4)),s.zeros(2))
        got=sum((kron(clean(V*P[f]*(G/4)*P[f].H*V.H),F[f]) for f in range(4)),s.zeros(8))
        assert clean(got)==clean(kron(V*G*V.H/4,H));moment_entries+=64
    for i,j in itertools.product(range(4),repeat=2):
        E=unit(4,i,j);actual=s.zeros(8);target=s.zeros(8)
        for f in range(4):
            avg=s.zeros(4)
            for Q in frames:
                # Physical Q before the source, Qdag AFTER learned inverse.
                A=clean(Q.H*Rhat*V*P[f]*Q)
                avg+=A*E*A.H/len(frames)
            want=(1-b)*P[f]*E*P[f].H+b*PE*P[f]*E*P[f].H*PE.H
            assert clean(avg)==clean(want)
            actual+=kron(avg,F[f]);target+=kron(want,F[f])
        assert clean(actual)==clean(target);twirl_entries+=64

# Known 2-wire encoder and coherent decoder: good patterns I,X2 are corrected.
# This is an explicit partial good set, NOT a claim to correct arbitrary weight 1.
Enc=s.zeros(4,2);Enc[0,0]=1;Enc[3,1]=1
def decode(A):
    mid=CN*A*CN.H
    return s.Matrix(2,2,lambda i,j:sum(mid[2*i+g,2*j+g] for g in range(2)))
code_entries=0
for f in range(4):
    for i,j in itertools.product(range(2),repeat=2):
        E=unit(2,i,j);actual=decode(P[f]*Enc*E*Enc.H*P[f].H)
        assert actual==logical[f]*E*logical[f].H
        learned_error=decode(PE*P[f]*Enc*E*Enc.H*P[f].H*PE.H)
        assert clean(learned_error)==clean(Y*logical[f]*E*logical[f].H*Y.H)
        code_entries+=8

def choiterm(A):
    v=s.Matrix([A[row,col] for col in range(A.cols) for row in range(A.rows)])
    return v*v.H
rm=s.Rational(3,10);eta=b+rm-b*rm;c=(1-b)*(1-rm)
J=s.zeros(16);Jbase=s.zeros(16);Jres=s.zeros(16);positive_coefficients=[]
for z,A in enumerate(K):
    bad=weights[z][2]+weights[z][3]
    assert bad<=rm
    Jbase+=choiterm(kron(I,A))
    coeff=(1-b)*(rm-bad);assert coeff>=0
    positive_coefficients.append(str(coeff));Jres+=coeff*choiterm(kron(I,A))
    for f in range(4):
        w=weights[z][f]
        J+=(1-b)*w*choiterm(kron(logical[f],A))+b*w*choiterm(kron(Y*logical[f],A))
        Jres+=b*w*choiterm(kron(Y*logical[f],A))
        if f>=2:Jres+=(1-b)*w*choiterm(kron(logical[f],A))
assert clean(J-c*Jbase)==clean(Jres)
effect=s.Matrix(4,4,lambda i,j:sum(Jres[4*i+out,4*j+out] for out in range(4)))
assert effect==eta*s.eye(4)
assert all(s.trace(Jres[4*i:4*i+4,4*i:4*i+4])==eta for i in range(4))

# Independent unequal-rate tail domination and the sharp correlated obstruction.
tail_cases=0
for rates in [[s.Rational(1,10),s.Rational(1,5),s.Rational(1,20)],
              [s.Rational(1,100),s.Rational(1,4),s.Rational(1,8)]]:
    pm=max(rates)
    tail=sum((s.prod(rates[i] if f&(1<<i) else 1-rates[i] for i in range(3))
              for f in range(8) if f.bit_count()>1),s.Rational(0))
    bound=3*pm*pm-2*pm**3
    assert tail<=bound;tail_cases+=1
p=s.Rational(1,10);iidtail=3*p*p-2*p**3
assert p>iidtail and 1-2*p>0
correlated={'patterns':{'000':str(1-p),'111':str(p)},
            'each_site_nonidentity_CP_rate':str(p),'X_signed_bias':'1','Z_signed_bias':str(1-2*p),
            'actual_repetition_logical_loss':str(p),'invalid_iid_tail_if_inferred':str(iidtail),
            'putative_CP_tail_residual_scalar':str(iidtail-p)}
# Independent error events can STILL violate the claimed CP-map domination if
# their error label is retained. The scalar probability/effect bound survives.
tag_T=s.diag(1-p,p);tag_bad=s.diag(0,p)
tag_residual=p*tag_T-tag_bad
assert s.trace(tag_bad)==p and tag_residual[1,1]==-p*(1-p)<0
tag_signed=s.diag(1-p,-p)
assert tag_signed[1,1]<0 and s.trace(tag_signed)==1-2*p>0
tag_boundary={'error_probability':str(p),
              'bad_effect_bound':'p I (valid)',
              'pT_minus_bad_negative_retained_tag_entry':str(tag_residual[1,1]),
              'signed_Z_map_negative_tag_entry':str(tag_signed[1,1]),
              'signed_Z_effect':str(s.trace(tag_signed)),
              'inside_current_CP_bias_or_scalar_mixture_tail_promise':False}
out={'status':'PASS_FULL_PHYSICAL_FRAMES_COMPLETE_MEMORY_KNOWN_CODE_CP_REDUCTION',
     'source_outcomes':0,'rng_draws':0,'physical_qubits':2,'memory_dimension':2,
     'noncommuting_memory_Kraus':True,'retired_physical_frames_per_map':16,
     'complete_calibration_moment_entries':moment_entries,'complete_framed_map_entries':twirl_entries,
     'known_code_matrix_entries':code_entries,'known_good_patterns':['II','IX'],
     'known_code_corrects_all_weight_one_Paulis':False,
     'learned_inverse_Bell_defect':str(b),'supplied_native_bad_CP_bound':str(rm),'eta':str(eta),
     'explicit_positive_residual_Kraus_sum':True,'CP_residual_Choi_entries':256,
     'residual_trace_effect':'eta I4','CP_clean_surplus_coefficients':positive_coefficients,
     'unequal_independent_tail_cases':tail_cases,'correlated_three_wire_failure':correlated,
     'retained_error_tag_CP_order_failure':tag_boundary,
     'sampled_acquisition_or_production_synthesis':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
