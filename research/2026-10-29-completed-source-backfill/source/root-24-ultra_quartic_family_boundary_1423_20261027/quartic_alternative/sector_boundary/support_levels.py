"""Ordinary norm-power support hierarchy, numerical exploration only."""
from pathlib import Path
import sys,json,time,math
import numpy as np
import sympy as s
import scipy.sparse as sp
import cvxpy as cp


def powers(degree):
    return [(a,b,c,degree-a-b-c) for a in range(degree+1)
            for b in range(degree-a+1) for c in range(degree-a-b+1)]


def compile_level(level,tau):
    a=s.symbols('a0:4');x=s.symbols('x0:4');variables=a+x
    def inv(y):
        aa,b,c,d=y
        return aa*aa+c*c,b*b+d*d,aa*b+c*d,aa*d-b*c
    def energy(y):
        u,v,w,q=inv(y)
        return u*u+v*v+3*w*w+tau*q*q+4*q*(u-v)
    f=energy(a);u,v,w,q=inv(a);qx=inv(x)[3];norm=sum(t*t for t in x)
    P=s.Poly((energy(tuple(ai+xi for ai,xi in zip(a,x)))-f-
              sum(s.diff(f,ai)*xi for ai,xi in zip(a,x)))*norm**level,variables)
    mults=[s.Poly(t*qx*norm**level,variables) for t in (u-v,q)]
    def mon(e):return s.prod(xi**ei for xi,ei in zip(x,e))
    z=[ai*mon(e) for ai in a for e in powers(level+1)]+[mon(e) for e in powers(level+2)]
    exponents=[s.Poly(zi,variables).monoms()[0] for zi in z]
    terms=[(i,j,tuple(e+f for e,f in zip(exponents[i],exponents[j])))
           for i in range(len(z)) for j in range(i,len(z))]
    monoms=sorted(set(P.monoms()).union((e for i,j,e in terms),
                                       *(set(p.monoms()) for p in mults)))
    lookup={e:i for i,e in enumerate(monoms)};rr=[];cc=[];dd=[]
    for col,(i,j,e) in enumerate(terms):rr.append(lookup[e]);cc.append(col);dd.append(1 if i==j else 2)
    for j,p in enumerate(mults):
        for e,v in p.terms():rr.append(lookup[e]);cc.append(len(terms)+j);dd.append(float(v))
    M=sp.coo_matrix((dd,(rr,cc)),shape=(len(monoms),len(terms)+len(mults))).tocsr()
    b=np.zeros(len(monoms))
    for e,c in P.terms():b[lookup[e]]=float(c)
    return M,b,terms,len(z)


def solve(level,tau):
    start=time.monotonic();M,b,terms,n=compile_level(level,tau)
    v=cp.Variable(M.shape[1]);rho=cp.Variable();rr=[];cc=[];vv=[]
    for col,(i,j,e) in enumerate(terms):
        rr.append(i*n+j);cc.append(col);vv.append(1)
        if i!=j:rr.append(j*n+i);cc.append(col);vv.append(1)
    embed=sp.coo_matrix((vv,(rr,cc)),shape=(n*n,M.shape[1])).tocsr()
    Q=cp.reshape(embed@v,(n,n),order='C');weights=np.sqrt(np.asarray(M.multiply(M).sum(axis=1)).ravel())
    problem=cp.Problem(cp.Maximize(rho),[sp.diags(1/weights)@M@v==b/weights,Q-rho*np.eye(n)>>0])
    problem.solve(solver='CLARABEL',max_iter=180,tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-9)
    out={'status':'NUMERICAL_ONLY','level':level,'tau':str(tau),'features':n,'equations':M.shape[0],
         'solver_status':problem.status,'margin':None if rho.value is None else float(rho.value),
         'selector':None if v.value is None else v.value[-2:].tolist(),
         'affine_residual':None if v.value is None else float(np.max(np.abs(M@v.value-b))),
         'seconds':time.monotonic()-start}
    if Q.value is not None:
        np.savez(Path(__file__).resolve().parent/f'LEVEL_{level}_{str(tau).replace("/","_")}.npz',gram=Q.value,selector=v.value[-2:],margin=rho.value)
    return out


def main():
    out=[]
    for level,tau in [(1,s.Rational(1404,125)),(2,s.Rational(1404,125)),
                      (1,89-12*s.sqrt(42))]:
        result=solve(level,tau);out.append(result);print(json.dumps(result),flush=True)
        (Path(__file__).resolve().parent/'SUPPORT_LEVELS.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':main()
