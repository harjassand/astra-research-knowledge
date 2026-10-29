"""Full rational-angular exact-form acquisition, alpha=P_5(A)/|A|^2.

No polynomial-two-form restriction: only the numerator P_5 is polynomial.
All linear maps are acquired from exact symbolic differentiation.  Numerical
proposals must be qualified before use in quasiconvexity.
"""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import numpy as np
import sympy as sp
from scipy import sparse
import cvxpy as cp
from compile_sos import acquire,degree

HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cross',action='store_true');ap.add_argument('--subtract-det',action='store_true')
    ap.add_argument('--solver',default='CLARABEL');args=ap.parse_args()
    if args.cross and args.subtract_det:raise ValueError('Product nu*gamma requires a separately fixed proposal')
    start=time.perf_counter();rhs0,_,_,cross0,det0,base=acquire('hopf')
    aa=sp.symbols('a:4');hh=sp.symbols('h0:6');T=sum(a*a for a in aa)
    B1=sp.Matrix([hh[0],hh[1],hh[3],hh[4]])
    B2=sp.Matrix([hh[1],hh[2],hh[4],hh[5]])
    mons=[a+h for a in degree(6,4) for h in degree(2,6)];lookup={m:i for i,m in enumerate(mons)}
    W=np.zeros((len(mons),len(rhs0)),dtype=int)
    for j,m in enumerate(base['monomials']):
        for nu,coef in sp.Poly(T*T,aa).terms():
            new=tuple(m[k]+nu[k] for k in range(4))+tuple(m[4:]);W[lookup[new],j]+=int(coef)
    columns=[];primitives=[]
    for s in range(4):
        for nu in degree(5,4):
            f=sp.prod(aa[k]**nu[k] for k in range(4));expr=0
            for r in range(4):
                if r!=s:expr+=(T*sp.diff(f,aa[r])-2*aa[r]*f)*(B1[r]*B2[s]-B1[s]*B2[r])
            poly=sp.Poly(sp.expand(expr),aa+hh)
            col=np.zeros(len(mons),dtype=int)
            for mon,coef in poly.terms():col[lookup[mon]]=int(coef)
            columns.append(col);primitives.append([s,list(nu)])
    J=np.array(columns,dtype=float).T
    z=[]
    for nu in degree(3,4):
        for j in range(6):
            h=[0]*6;h[j]=1;z.append(nu+tuple(h))
    n=len(z);rows=[];cols=[]
    for i,zi in enumerate(z):
        for j,zj in enumerate(z):rows.append(lookup[tuple(a+b for a,b in zip(zi,zj))]);cols.append(n*i+j)
    gram=sparse.coo_matrix((np.ones(n*n),(rows,cols)),shape=(len(mons),n*n)).tocsc()
    Q=cp.Variable((n,n),symmetric=True);t=cp.Variable(J.shape[1]);tau=cp.Variable()
    nu=cp.Variable() if args.cross else cp.Constant(0.);gamma=cp.Variable(nonneg=True) if args.subtract_det else cp.Constant(0.)
    eq=gram@cp.vec(Q,order='C')==W@rhs0+J@t+nu*(W@cross0)-gamma*(W@det0)
    problem=cp.Problem(cp.Maximize(tau),[eq,Q-tau*np.eye(n)>>0])
    acq=time.perf_counter()-start;t0=time.perf_counter()
    if args.solver=='CLARABEL':options=dict(max_iter=150,tol_gap_abs=1e-8,tol_feas=1e-8,tol_gap_rel=1e-8)
    else:options=dict(eps=1e-6,max_iters=10000)
    problem.solve(solver=args.solver,**options)
    result=dict(status=problem.status,value=problem.value,cross=args.cross,subtract_det=args.subtract_det,
                solver=args.solver,n=n,equations=len(mons),primitives=len(primitives),
                acquisition_seconds=acq,solver_seconds=time.perf_counter()-t0,
                nu=None if nu.value is None else float(nu.value),gamma=None if gamma.value is None else float(gamma.value),
                Q=None if Q.value is None else Q.value.tolist(),alpha=None if t.value is None else t.value.tolist(),
                equality_dual=None if eq.dual_value is None else eq.dual_value.tolist())
    if Q.value is not None:
        result['min_Q']=float(np.linalg.eigvalsh(Q.value).min())
        result['identity_residual']=float(np.max(abs(gram@Q.value.reshape(-1)-W@rhs0-J@t.value-float(nu.value)*(W@cross0)+float(gamma.value)*(W@det0))))
    label=f'RATIONAL_{"cross_" if args.cross else ""}{"subdet_" if args.subtract_det else ""}{args.solver}'
    (HERE/f'{label}_PROPOSAL.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'RATIONAL_MAP.json').write_text(json.dumps(dict(monomials=mons,primitives=primitives,z=z,J=J.astype(int).tolist()),separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['Q','alpha','equality_dual']},indent=2))

if __name__=='__main__':main()
