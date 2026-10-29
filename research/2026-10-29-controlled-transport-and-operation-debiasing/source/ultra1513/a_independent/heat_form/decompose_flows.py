"""Construct a finite sum of independent quasiconvex flow certificates.

Each summand has its own constant parabolic generator and exact-form
correction. This never assumes one common energy-monotone flow exists.
"""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import numpy as np
import sympy as sp
import cvxpy as cp
from compile_sos import acquire

HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--complex',action='store_true');args=ap.parse_args()
    start=time.perf_counter()
    _,gram,J,_,_,base=acquire('hopf')
    aa=sp.symbols('a b c d');hh=sp.symbols('h0:6');a,b,c,d=aa
    u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
    polys=[u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w]
    B1=sp.Matrix([hh[0],hh[1],hh[3],hh[4]])
    B2=sp.Matrix([hh[1],hh[2],hh[4],hh[5]])
    JJ=sp.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
    maps=[]
    for f in polys:
        H=sp.hessian(f,aa)
        expr=[(B1.T*H*B1)[0],2*(B1.T*H*B2)[0],(B2.T*H*B2)[0],
              (B1.T*H*JJ*B1)[0],(B1.T*H*JJ*B2)[0]+(B2.T*H*JJ*B1)[0],(B2.T*H*JJ*B2)[0]]
        maps.append([[float(sp.Poly(sp.expand(e),aa+hh).coeff_monomial(m)) for m in base['monomials']] for e in expr])
    maps=np.array(maps).transpose(1,2,0)
    metrics=[(1,0,1),(2,0,.5),(.5,0,2),(1,.6,1),(1,-.6,1)]
    imag=[(0,0,0)]
    if args.complex:imag += [(0,-.1,0),(0,.1,0),(.25,0,.25),(-.25,0,-.25)]
    flows=[m+n for m in metrics for n in imag]
    n=len(flows)
    P=cp.Variable((9,n));tau=cp.Variable();gamma=cp.Variable(nonneg=True)
    Qs=[cp.Variable((24,24),symmetric=True) for _ in flows]
    ts=[cp.Variable(80) for _ in flows]
    detvec=np.array([0,0,1,-1,0,0,0,0,0.])
    target=np.array([1,1,12.08,-10.08,0,0,3.96,-3.96,0.])
    constraints=[cp.sum(P,axis=1)+gamma*detvec==target]
    for j,flow in enumerate(flows):
        L=sum(flow[k]*maps[k] for k in range(6))
        constraints += [gram@cp.vec(Qs[j],order='C')==L@P[:,j]+J@ts[j],Qs[j]-tau*np.eye(24)>>0]
    prob=cp.Problem(cp.Maximize(tau),constraints)
    acq=time.perf_counter()-start;t0=time.perf_counter()
    prob.solve(solver='CLARABEL',max_iter=200,tol_gap_abs=1e-8,tol_feas=1e-8,tol_gap_rel=1e-8)
    result=dict(complex=args.complex,flows=flows,status=prob.status,value=prob.value,
                acquisition_seconds=acq,solver_seconds=time.perf_counter()-t0,
                gamma=None if gamma.value is None else float(gamma.value),
                P=None if P.value is None else P.value.tolist(),
                Qs=[None if Q.value is None else Q.value.tolist() for Q in Qs],
                ts=[None if t.value is None else t.value.tolist() for t in ts])
    if P.value is not None:
        result['sum_residual']=float(np.max(abs(np.sum(P.value,axis=1)+float(gamma.value)*detvec-target)))
        result['min_Q']=min(float(np.linalg.eigvalsh(Q.value).min()) for Q in Qs)
    (HERE/f'{"complex" if args.complex else "ordinary"}_DECOMPOSITION_PROPOSAL.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['Qs','ts','P','flows']},indent=2))

if __name__=='__main__':main()
