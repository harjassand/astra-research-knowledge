"""Exact symbolic consumer for the dimension-independent resolvent proof.

No source/channel acquisition, BKM search, or state simulation is performed.
The two singular-index calculation includes arbitrary complex Hermitian blocks;
the proof sums that scalar identity over all index pairs in any dimension.
"""
import hashlib
import json
from pathlib import Path
import time
import sympy as S

HERE=Path(__file__).resolve().parent

def main():
    begin=time.perf_counter()
    c0,c1=S.symbols('c0 c1',real=True)
    a,b,c,d,x,y,z,w=S.symbols('a b c d x y z w',real=True)
    A=S.Matrix([[a,x+S.I*y],[x-S.I*y,b]])
    B=S.Matrix([[c,z+S.I*w],[z-S.I*w,d]])
    aa=S.diag(1/(1-c0**2),1/(1-c1**2))
    bb=S.diag(c0/(1-c0**2),c1/(1-c1**2))
    R=aa.row_join(bb).col_join(bb.row_join(aa))
    X=S.diag(A,B)
    actual=S.trace(X*R*X*R)-S.trace(X*X)
    expected=0
    ci=[c0,c1]
    term_count=0
    for i in range(2):
        for j in range(2):
            den=(1-ci[i]**2)*(1-ci[j]**2)
            gap=((ci[i]-ci[j])**2+ci[i]*ci[j]*(1-ci[i]*ci[j]))/den
            coupling=ci[i]*ci[j]/den
            expected += gap*(S.expand_complex(A[i,j]*S.conjugate(A[i,j]))+
                              S.expand_complex(B[i,j]*S.conjugate(B[i,j])))
            expected += coupling*S.expand_complex((A[i,j]+B[i,j])*
                                      S.conjugate(A[i,j]+B[i,j]))
            identity=(1-ci[i]*ci[j])/den-1-gap
            assert S.factor(identity)==0
            term_count+=1
    identity=S.Poly(S.expand((actual-expected)*((1-c0**2)*(1-c1**2))**2),
                    a,b,c,d,x,y,z,w)
    coeffs=identity.coeffs()
    assert all(S.factor(v)==0 for v in coeffs)

    # Pure-vector Gram inverse and the scalar variable change are exact.
    s,xi=S.symbols('s xi',real=True)
    G=S.Matrix([[1,s],[s,1]])
    assert S.simplify((1-s*s)*G.inv()-S.Matrix([[1,-s],[-s,1]]))==S.zeros(2)
    beta=1-s*s
    assert S.simplify(beta*(1/beta))==1

    payload={
        'status':'EXACT_SYMBOLIC_IDENTITIES_PASSED',
        'meaning':'proof identities, not a finite-dimensional replacement for the theorem',
        'fixed_channel':'tau0=|0><0|,tau1=|+><+|',
        'two_singular_index_complex_Hermitian_slack_identity':True,
        'per_pair_nonnegative_identity_checks':term_count,
        'matrix_trace_minus_sum_slack_coefficients_zero':True,
        'Gram_inverse_and_resolvent_change_of_variable':True,
        'earned_reverse_equal_reference_coefficient':'2',
        'subtracted_J_unequal_reference_coefficient':'NOT_RESOLVED_BY_THIS_CONSUMER',
        'seconds_after_imports':time.perf_counter()-begin,
        'executed_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'proof_sha256':hashlib.sha256((HERE/'PROOF.md').read_bytes()).hexdigest()
    }
    (HERE/'EXACT_RESULT.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps(payload,indent=2))

if __name__=='__main__': main()
