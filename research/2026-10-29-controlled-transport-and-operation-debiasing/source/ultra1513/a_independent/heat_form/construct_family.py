"""Construct a heat-certificate frontier in a fixed physical quartic family.

Floating SDP proposals only.  The scalar-flow comparator gets exactly the
same polynomial coefficient acquisition and exact-form freedom.
"""
from __future__ import annotations
import json,time
from pathlib import Path
import numpy as np
import sympy as sp
import cvxpy as cp
from compile_sos import acquire

HERE=Path(__file__).resolve().parent

def main():
    start=time.perf_counter()
    _,gram,J,_,_,base=acquire('hopf')
    aa=sp.symbols('a b c d');hh=sp.symbols('h0:6');a,b,c,d=aa
    T=sum(z*z for z in aa);q=a*d-b*c;x=a*a+c*c-b*b-d*d
    polys=[T*T,q*q,q*x]
    B1=sp.Matrix([hh[0],hh[1],hh[3],hh[4]])
    B2=sp.Matrix([hh[1],hh[2],hh[4],hh[5]])
    JJ=sp.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
    E=[];S=[]
    for f in polys:
        H=sp.hessian(f,aa)
        e=sp.Poly(sp.expand((B1.T*H*B1)[0]+(B2.T*H*B2)[0]),aa+hh)
        s=sp.Poly(sp.expand((B1.T*H*JJ*B2)[0]+(B2.T*H*JJ*B1)[0]),aa+hh)
        E.append([float(e.coeff_monomial(m)) for m in base['monomials']])
        S.append([float(s.coeff_monomial(m)) for m in base['monomials']])
    E=np.array(E).T;S=np.array(S).T
    Q=cp.Variable((24,24),symmetric=True);t=cp.Variable(80);bb=cp.Variable()
    avec=cp.Parameter(210);bvec=cp.Parameter(210)
    eq=gram@cp.vec(Q,order='C')==avec+bb*bvec+J@t
    prob=cp.Problem(cp.Maximize(bb),[eq,Q>>0])
    records=[]
    for avalue in [1,2,4,8,10.08,12,20]:
        for nu in [-.5,-.25,-.1,0,.1,.25,.5]:
            L=E+nu*S;avec.value=L[:,0]+avalue*L[:,1];bvec.value=L[:,2]
            tic=time.perf_counter()
            try:
                prob.solve(solver='CLARABEL',max_iter=200,tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9)
                rec=dict(a=avalue,nu=nu,b=prob.value,status=prob.status,seconds=time.perf_counter()-tic)
                if Q.value is not None:
                    rec['eig_min']=float(np.linalg.eigvalsh(Q.value).min())
                    rec['residual']=float(np.max(abs(gram@Q.value.reshape(-1)-avec.value-float(bb.value)*bvec.value-J@t.value)))
            except Exception as e:rec=dict(a=avalue,nu=nu,error=str(e),seconds=time.perf_counter()-tic)
            records.append(rec)
    result=dict(records=records,total_seconds=time.perf_counter()-start)
    (HERE/'FAMILY_PROPOSALS.json').write_text(json.dumps(result,indent=2)+'\n')
    for avalue in [1,2,4,8,10.08,12,20]:
        rows=[r for r in records if r['a']==avalue and r.get('b') is not None]
        print(json.dumps(dict(a=avalue,scalar=next(r['b'] for r in rows if r['nu']==0),best=max(rows,key=lambda r:r['b'])),indent=2))

if __name__=='__main__':main()
