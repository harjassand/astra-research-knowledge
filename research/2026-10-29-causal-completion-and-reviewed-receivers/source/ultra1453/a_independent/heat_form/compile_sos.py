"""Acquire an exact polynomial linear map, then request an SDP proposal.

No solver status is a mathematical certificate.  The polynomial map uses
SymPy rationals; proposal data are saved for exact downstream verification.
"""
from __future__ import annotations
import argparse, hashlib, json, time
from pathlib import Path
import numpy as np
import sympy as sp
import cvxpy as cp

HERE=Path(__file__).resolve().parent

def degree(d,n):
    if n==1:
        yield (d,)
    else:
        for j in range(d+1):
            for tail in degree(d-j,n-1):
                yield (j,)+tail

def acquire(kind):
    aa=sp.symbols('a b c d'); hh=sp.symbols('h0:6')
    a,b,c,d=aa
    T=a*a+b*b+c*c+d*d; q=a*d-b*c
    x=a*a+c*c-b*b-d*d
    if kind=='hopf': F=T*T+sp.Rational(252,25)*q*q+sp.Rational(99,25)*q*x
    elif kind=='dm': F=T*T-2*T*q
    elif kind=='norm': F=T*T
    else: raise ValueError(kind)
    B1=sp.Matrix([hh[0],hh[1],hh[3],hh[4]])
    B2=sp.Matrix([hh[1],hh[2],hh[4],hh[5]])
    Hess=sp.hessian(F,aa)
    I=sp.Poly(sp.expand((B1.T*Hess*B1)[0]+(B2.T*Hess*B2)[0]),aa+hh)
    mons=[p+q for p in degree(2,4) for q in degree(2,6)]
    lookup={m:i for i,m in enumerate(mons)}
    rhs=np.array([float(I.coeff_monomial(m)) for m in mons])
    rhs_exact=[str(I.coeff_monomial(m)) for m in mons]
    z=[]
    for i in range(4):
        for j in range(6):
            m=[0]*10; m[i]=1;m[4+j]=1;z.append(tuple(m))
    gram=np.zeros((210,24*24))
    for i,zi in enumerate(z):
        for j,zj in enumerate(z):
            m=tuple(x+y for x,y in zip(zi,zj));gram[lookup[m],24*i+j]=1
    corrections=[]; alpha=[]
    for s in range(4):
        for nu in degree(3,4):
            basis=sp.prod(aa[k]**nu[k] for k in range(4))
            expr=0
            for r in range(4):
                if r!=s:
                    expr+=sp.diff(basis,aa[r])*(B1[r]*B2[s]-B1[s]*B2[r])
            p=sp.Poly(sp.expand(expr),aa+hh)
            corrections.append([int(p.coeff_monomial(m)) for m in mons])
            alpha.append([s,list(nu)])
    J=np.array(corrections,dtype=float).T
    return rhs,gram,J,dict(kind=kind,F=str(F),monomials=mons,rhs=rhs_exact,
                            correction_matrix=J.astype(int).tolist(),alpha=alpha,z=z)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--kind',default='hopf',choices=['hopf','dm','norm'])
    ap.add_argument('--solver',default='CLARABEL');args=ap.parse_args()
    start=time.perf_counter();rhs,gram,J,exact=acquire(args.kind);acq=time.perf_counter()-start
    Q=cp.Variable((24,24),symmetric=True);t=cp.Variable(80);tau=cp.Variable()
    con=gram@cp.vec(Q,order='C')==rhs+J@t
    psd=Q-tau*np.eye(24)>>0
    prob=cp.Problem(cp.Maximize(tau),[con,psd])
    solve_start=time.perf_counter()
    options=dict(max_iter=300,tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9) if args.solver=='CLARABEL' else dict(eps=1e-7,max_iters=100000)
    value=prob.solve(solver=args.solver,**options)
    result=dict(kind=args.kind,status=prob.status,value=value,
                acquisition_seconds=acq,solver_seconds=time.perf_counter()-solve_start,
                solver=args.solver,solver_stats=str(prob.solver_stats),
                map_sha256=hashlib.sha256(json.dumps(exact,sort_keys=True).encode()).hexdigest(),
                exact_linear_rank=int(np.linalg.matrix_rank(J)),
                Q=None if Q.value is None else Q.value.tolist(),
                alpha_coefficients=None if t.value is None else t.value.tolist(),
                equality_dual=None if con.dual_value is None else con.dual_value.tolist(),
                psd_dual=None if psd.dual_value is None else psd.dual_value.tolist())
    if Q.value is not None:
        result['minimum_eigenvalue']=float(np.linalg.eigvalsh(Q.value).min())
        result['max_identity_residual']=float(np.max(abs(gram@Q.value.reshape(-1)-rhs-J@t.value)))
    (HERE/f'{args.kind}_map.json').write_text(json.dumps(exact,indent=2)+'\n')
    (HERE/f'{args.kind}_{args.solver}_proposal.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['Q','alpha_coefficients','equality_dual','psd_dual','solver_stats']},indent=2))

if __name__=='__main__':main()
