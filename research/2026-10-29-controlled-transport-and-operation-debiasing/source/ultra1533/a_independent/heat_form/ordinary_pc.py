"""Give the ordinary route a global polynomial minor support construction.

A positive exact-qualified SOS proposal proves actual polyconvexity. A
negative margin only fails this particular polynomial-support ansatz.
"""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import numpy as np
import sympy as sp
import cvxpy as cp
from compile_sos import degree

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--a',default='12');ap.add_argument('--b',default='3.975');args=ap.parse_args()
    start=time.perf_counter();aa=sp.symbols('a:4');xx=sp.symbols('x:4');variables=aa+xx
    def energy(z):
        a,b,c,d=z;q=a*d-b*c;T=sum(x*x for x in z);x=a*a+c*c-b*b-d*d
        return T*T+sp.Rational(args.a)*q*q+sp.Rational(args.b)*q*x
    F=energy(aa);gap=sp.Poly(sp.expand(energy([aa[i]+xx[i] for i in range(4)])-F-sum(sp.diff(F,aa[i])*xx[i] for i in range(4))),variables)
    kmon=list(degree(2,4));mons=[a+x for da in [0,1,2] for a in degree(da,4) for x in degree(4-da,4)]
    lookup={m:i for i,m in enumerate(mons)};rhs=np.array([float(gap.coeff_monomial(m)) for m in mons])
    delta=xx[0]*xx[3]-xx[1]*xx[2]
    K=[]
    for nu in kmon:
        p=sp.Poly(sp.prod(aa[i]**nu[i] for i in range(4))*delta,variables)
        K.append([float(p.coeff_monomial(m)) for m in mons])
    K=np.array(K).T
    z=[]
    for i in range(4):
        for j in range(4):
            m=[0]*8;m[i]=1;m[4+j]=1;z.append(tuple(m))
    z += [(0,)*4+nu for nu in degree(2,4)]
    n=len(z);G=np.zeros((len(mons),n*n))
    for i,zi in enumerate(z):
        for j,zj in enumerate(z):G[lookup[tuple(a+b for a,b in zip(zi,zj))],n*i+j]=1
    Q=cp.Variable((n,n),symmetric=True);k=cp.Variable(10);tau=cp.Variable()
    eq=G@cp.vec(Q,order='C')==rhs-K@k
    prob=cp.Problem(cp.Maximize(tau),[eq,Q-tau*np.eye(n)>>0])
    acq=time.perf_counter()-start;t0=time.perf_counter()
    prob.solve(solver='CLARABEL',max_iter=250,tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9)
    result=dict(a=args.a,b=args.b,status=prob.status,value=prob.value,
                acquisition_seconds=acq,solver_seconds=time.perf_counter()-t0,
                Q=None if Q.value is None else Q.value.tolist(),k=None if k.value is None else k.value.tolist(),kmon=kmon,
                monomials=mons,z=z,rhs=[str(gap.coeff_monomial(m)) for m in mons])
    if Q.value is not None:
        result['min_Q']=float(np.linalg.eigvalsh(Q.value).min());result['residual']=float(np.max(abs(G@Q.value.reshape(-1)-rhs+K@k.value)))
    Path(__file__).with_name(f'ORDINARY_PC_a{args.a}_b{args.b}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['Q','k','kmon','monomials','z','rhs']},indent=2))

if __name__=='__main__':main()
