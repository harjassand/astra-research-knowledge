"""Independent exact real-integer checks and complex numerical diagnostics."""
from __future__ import annotations
from fractions import Fraction
from pathlib import Path
import json
import numpy as np
from npt_core import endpoint, endpoint_numerator, swap_metric_numerator, partial_trace


def run() -> dict:
    rng = np.random.default_rng(20261009)
    exact = []
    complex_errors = []
    for m in range(0,4):
        dims = (3,)*m
        D = 3**m
        for trial in range(6):
            u,v,x0,x1,y0,y1 = [rng.integers(-2,3,D).astype(object) for _ in range(6)]
            eps = trial%3+1
            X = np.column_stack([x0,x1]); Y = np.column_stack([y0,y1])
            U = np.vstack([np.column_stack([u,0*u]),np.column_stack([0*u,u]),eps*X])
            V = np.vstack([np.column_stack([v,0*v]),np.column_stack([0*v,v]),eps*Y])
            C = U@V.T
            small = X@Y.T
            lhs = endpoint_numerator(C,(3,)+dims)
            h = sum(swap_metric_numerator(np.kron(x,v)-np.kron(u,y),dims)
                    for x,y in [(x0,y0),(x1,y1)])
            rhs = 2*eps**2*h + eps**4*endpoint_numerator(small,dims)
            assert lhs == rhs, (m,trial,lhs,rhs)
            assert h >= 0
            exact.append({'remaining_sites':m,'trial':trial,'epsilon':eps,
                          'scaled_lhs':str(lhs),'scaled_rhs':str(rhs),
                          'scaled_square_sum':str(h)})
        # Complex diagnostics use a separately constructed partial-trace sum.
        for trial in range(4):
            vs = [rng.normal(size=D)+1j*rng.normal(size=D) for _ in range(6)]
            u,v,x0,x1,y0,y1=vs
            eps=.17+.19*trial
            X=np.column_stack([x0,x1]); Y=np.column_stack([y0,y1])
            U=np.vstack([np.column_stack([u,0*u]),np.column_stack([0*u,u]),eps*X])
            V=np.vstack([np.column_stack([v,0*v]),np.column_stack([0*v,v]),eps*Y])
            C=U@V.conj().T
            small=X@Y.conj().T
            h=0.0
            for x,y in [(x0,y0),(x1,y1)]:
                z=(np.kron(x,v)-np.kron(u,y)).reshape(dims+dims)
                out=z.copy()
                for i in range(m): out=out-.5*out.swapaxes(i,m+i)
                h+=np.vdot(z,out).real
            lhs=endpoint(C,(3,)+dims)
            rhs=eps**2*h+.5*eps**4*endpoint(small,dims)
            direct=0.0
            ds=(3,)+dims
            for mask in range(1<<len(ds)):
                S=tuple(i for i in range(len(ds)) if mask>>i&1)
                tr=partial_trace(C,ds,S)
                direct+=(-.5)**len(S)*np.vdot(tr,tr).real
            err=max(abs(lhs-rhs),abs(lhs-direct))/max(1.,abs(lhs),abs(rhs))
            assert err<2e-12,(m,trial,err)
            complex_errors.append(float(err))
    # Detect a known inadmissible rank-three negative case, not an NPT-bound-entanglement witness.
    neg=endpoint_numerator(np.eye(3,dtype=object),(3,))
    assert neg == -3 # q_1(I_3)=-3/2
    # Detect a known admissible one-copy zero.
    zero=endpoint_numerator(np.diag([1,1,0]).astype(object),(3,))
    assert zero == 0
    return {'status':'exact finite identity checks only; all-copy question unresolved',
            'seed':20261009,'exact_checks':len(exact),'exact_records':exact,
            'complex_diagnostics':len(complex_errors),
            'maximum_relative_complex_residual':max(complex_errors),
            'negative_control_q1_I3':str(Fraction(neg,2)),
            'zero_control_q1_diag110':str(Fraction(zero,2))}

if __name__=='__main__':
    result=run()
    p=Path(__file__).with_name('IDENTITY_RECEIPT.json')
    p.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='exact_records'},indent=2))
