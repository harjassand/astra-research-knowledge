"""Polynomial multiplier relaxation of the pointwise exact-form criterion.

It strictly enlarges the degree-(1,1) SOS representation. A proposal must be
verified in rational arithmetic before it is used as a theorem.
"""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import numpy as np
import cvxpy as cp
import sympy as sp
from compile_sos import acquire,degree

HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--kind',default='hopf')
    ap.add_argument('--cross',action='store_true');ap.add_argument('--subtract-det',action='store_true')
    ap.add_argument('--level',type=int,default=2);args=ap.parse_args()
    if args.cross and args.subtract_det:raise ValueError('bilinear cross/subtraction parameter not admitted')
    start=time.perf_counter()
    rhs,_,J,cross,detheat,base=acquire(args.kind)
    p=args.level
    mons=[aa+hh for aa in degree(2*p,4) for hh in degree(2,6)]
    lookup={m:i for i,m in enumerate(mons)}
    aa=sp.symbols('a:4');mult=sp.Poly(sum(a*a for a in aa)**(p-1),aa).terms()
    W=np.zeros((len(mons),len(rhs)))
    for j,old in enumerate(base['monomials']):
        for nu,coeff in mult:
            new=tuple(old[k]+nu[k] for k in range(4))+tuple(old[4:])
            W[lookup[new],j]+=int(coeff)
    z=[]
    for nu in degree(p,4):
        for i in range(6):
            hh=[0]*6;hh[i]=1;z.append(nu+tuple(hh))
    n=len(z);gram=np.zeros((len(mons),n*n))
    for i,zi in enumerate(z):
        for j,zj in enumerate(z):
            m=tuple(x+y for x,y in zip(zi,zj));gram[lookup[m],n*i+j]=1
    Q=cp.Variable((n,n),symmetric=True);t=cp.Variable(80);tau=cp.Variable()
    nu=cp.Variable() if args.cross else cp.Constant(0.)
    gamma=cp.Variable(nonneg=True) if args.subtract_det else cp.Constant(0.)
    eq=gram@cp.vec(Q,order='C')==W@rhs+(W@J)@t+nu*(W@cross)-gamma*(W@detheat)
    prob=cp.Problem(cp.Maximize(tau),[eq,Q-tau*np.eye(n)>>0])
    acq=time.perf_counter()-start
    t0=time.perf_counter()
    prob.solve(solver='CLARABEL',max_iter=200,tol_gap_abs=1e-8,tol_feas=1e-8,tol_gap_rel=1e-8)
    result=dict(kind=args.kind,level=p,n=n,equations=len(mons),cross=args.cross,subtract_det=args.subtract_det,
                status=prob.status,value=prob.value,acquisition_seconds=acq,solver_seconds=time.perf_counter()-t0,
                nu=None if nu.value is None else float(nu.value),gamma=None if gamma.value is None else float(gamma.value),
                Q=None if Q.value is None else Q.value.tolist(),alpha_coefficients=None if t.value is None else t.value.tolist(),
                equality_dual=None if eq.dual_value is None else eq.dual_value.tolist())
    if Q.value is not None:
        result['minimum_eigenvalue']=float(np.linalg.eigvalsh(Q.value).min())
        result['max_identity_residual']=float(np.max(abs(gram@Q.value.reshape(-1)-W@rhs-(W@J)@t.value-float(nu.value)*(W@cross)+float(gamma.value)*(W@detheat))))
    out=HERE/f'{args.kind}_level{p}_{"cross_" if args.cross else ""}{"subdet_" if args.subtract_det else ""}proposal.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['Q','alpha_coefficients','equality_dual']},indent=2))

if __name__=='__main__':main()
