"""One direct pointwise differential-LMI proposal, NO SOS Gram.

This keeps the same P5/T profile; its actual symmetries cover all gradients
by A=(1,b,0,d), b²+d²<=1. A finite-grid negative outcome is not a theorem.
"""
from pathlib import Path
from fractions import Fraction
import hashlib,json,time
import sympy as S
import numpy as np
import cvxpy as cp


def main():
    start=time.perf_counter();here=Path(__file__).parent
    raw=json.loads((here/'ANGULAR_REDUCTION.json').read_text())
    A=S.symbols('a b c d',real=True);v=[S.Symbol(n,real=True)for n in raw['effective_parameters']]
    loc={str(x):x for x in (*A,*v)}
    C=S.Matrix([[S.sympify(x,locals=loc)for x in row]for row in raw['cleared_completion']])
    C=S.simplify(C.subs({A[0]:1,A[2]:0}));zero=dict.fromkeys(v,0)
    pieces=[C.subs(zero)]+[C.diff(p)for p in v]
    functions=[S.lambdify((A[1],A[3]),p,'numpy',cse=True)for p in pieces]
    N=8;points=[(Fraction(i,N),Fraction(j,N))for i in range(N+1)for j in range(-N,N+1)if i*i+j*j<=N*N]
    y=cp.Variable(len(v));margin=cp.Variable();constraints=[]
    for b,d in points:
        b,d=float(b),float(d);T=1+b*b+d*d
        M=[np.array(f(b,d),dtype=float)/T**3 for f in functions]
        target=cp.Constant(M[0])
        for i in range(len(v)):target+=y[i]*M[i+1]
        weight=(1-(2*d/T)**2)**2
        constraints.append(target-margin*weight*np.eye(6)>>0)
    model=cp.Problem(cp.Maximize(margin),constraints);setup=time.perf_counter()-start;tick=time.perf_counter()
    error=None
    try:model.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-9,max_iter=180)
    except Exception as e:error=repr(e)
    out={'scope':'one same-profile direct6parameter pointwise proposal; finite grid NOT all-angular/all-profile proof',
         'points':[[str(x)for x in p]for p in points],'profile_parameters':raw['effective_parameters'],
         'status':model.status,'error':error,'margin':None if margin.value is None else float(margin.value),
         'parameters':None if y.value is None else y.value.tolist(),
         'mapping_seconds':setup,'solve_seconds':time.perf_counter()-tick,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'input_sha256':hashlib.sha256((here/'ANGULAR_REDUCTION.json').read_bytes()).hexdigest(),
         'random_starts':0,'SOS_Gram':False}
    (here/'POINTWISE_PROFILE_PROPOSAL.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k]for k in ('status','error','margin','parameters','mapping_seconds','solve_seconds')},indent=2))


if __name__=='__main__':main()
