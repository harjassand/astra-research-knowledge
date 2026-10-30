"""Necessary smooth-completion jet LMI, not a polynomial-form relaxation.

At the null rank-one Hessian h0, its diagonal is fixed by F, independent
of the correction. Positivity nearby therefore bounds C' h0 by this fixed
quadratic curvature. Closedness/invariance are exact linear inputs.
"""
from pathlib import Path
import hashlib,json,time
import sympy as S
import numpy as np
import cvxpy as cp


def main():
    start=time.perf_counter();here=Path(__file__).parent
    receipt=json.loads((here/'LOCAL_CLOSED_JET.json').read_text())
    o=S.symbols('o0:6');w=S.symbols('w0:24');unknown=(*o,*w)
    mat=S.Matrix([[S.Rational(v) for v in row] for row in receipt['matrix']])
    rhs=S.Matrix([S.Rational(v) for v in receipt['rhs']])
    solution=next(iter(S.linsolve((mat,rhs),unknown)))
    substitution=dict(zip(unknown,solution));free=sorted(set().union(*(v.free_symbols for v in solution)),key=str)
    A=S.symbols('a b c d');h=S.symbols('h0:6');base=S.Matrix([1,0,0,1]);pairs=[(i,j) for i in range(4) for j in range(i+1,4)]
    Omega=S.zeros(4)
    for n,(i,j) in enumerate(pairs):
        Omega[i,j]=o[n]+sum(w[4*n+k]*(A[k]-base[k]) for k in range(4));Omega[j,i]=-Omega[i,j]
    T=sum(v*v for v in A);q=A[0]*A[3]-A[1]*A[2];x=A[0]**2+A[2]**2-A[1]**2-A[3]**2
    F=T*T+12*q*q+4*q*x;H=S.hessian(F,A)
    B1=S.Matrix([h[0],h[1],h[3],h[4]]);B2=S.Matrix([h[1],h[2],h[4],h[5]])
    C=S.hessian((B1.T*H*B1+B2.T*H*B2+B1.T*Omega*B2)[0],h)/2
    at=dict(zip(A,base));C0=C.subs(at).subs(substitution)
    h0=S.Matrix([0,0,1,0,0,0]);h1=S.Matrix([0,1,0,0,0,-2])
    X=S.Matrix.hstack(*(C.diff(v).subs(at).subs(substitution)*h0 for v in A))
    fixed=H.subs(dict(zip(A,[0,1,0,0])))
    block=fixed.row_join(X.T).col_join(X.row_join(C0))
    kernels=[base.col_join(S.zeros(6,1)),S.zeros(4,1).col_join(h0),S.zeros(4,1).col_join(h1)]
    K=S.Matrix.hstack(*kernels);assert block*K==S.zeros(10,3)
    R=S.Matrix.hstack(*K.T.nullspace());reduced=S.simplify(R.T*block*R)
    zero=dict.fromkeys(free,0);constant=np.array(reduced.subs(zero),dtype=float)
    derivatives=[np.array(reduced.diff(v),dtype=float) for v in free]
    y=cp.Variable(len(free));margin=cp.Variable()
    value=cp.Constant(constant)
    for i,M in enumerate(derivatives):value=value+y[i]*M
    constraint=value-margin*np.eye(7)>>0
    problem=cp.Problem(cp.Maximize(margin),[constraint]);tick=time.perf_counter()
    problem.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10,max_iter=150)
    out={'scope':'necessary C1 closed-completion jet curvature; no finite degree assumption',
         'free_parameters':[str(v) for v in free],'reduced_matrix':[[str(v) for v in row] for row in reduced.tolist()],
         'status':problem.status,'margin':None if margin.value is None else float(margin.value),
         'parameters':None if y.value is None else y.value.tolist(),
         'dual':None if constraint.dual_value is None else constraint.dual_value.tolist(),
         'map_seconds':tick-start,'solve_seconds':time.perf_counter()-tick,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'input_sha256':hashlib.sha256((here/'LOCAL_CLOSED_JET.json').read_bytes()).hexdigest()}
    (here/'FIRST_JET_CURVATURE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('free_parameters','status','margin','parameters','map_seconds','solve_seconds')},indent=2))


if __name__=='__main__':main()
