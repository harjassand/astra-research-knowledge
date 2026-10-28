#!/usr/bin/env python3
"""Direct true-PC obstruction search; no SOS/SDP relaxation.

A negative opposite-determinant pair would obstruct every global support,
including nonpolynomial selectors. A failed search proves no positivity.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,time
import sympy as S
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/
    "sol6_openings_20261027/independent_opening/vendor"))
try:
    from scipy.optimize import minimize
except ImportError:
    sys.path.insert(0,str(Path(__file__).resolve().parents[3]/
        "sol6_openings_20261027/independent_opening/vendor"))
    from scipy.optimize import minimize


def main():
    started=time.perf_counter()
    a,b,c,d,tau=S.symbols("a b c d tau",real=True)
    V=(a,b,c,d)
    u=a*a+c*c
    v=b*b+d*d
    w=a*b+c*d
    q=a*d-b*c
    F=u*u+v*v+3*w*w+tau*q*q+4*q*(u-v)
    grad=S.Matrix([S.diff(F,z) for z in V])
    hess=S.hessian(F,V)
    func=S.lambdify((*V,tau),(F,grad,hess),"numpy",cse=True)
    tc=float(89-12*S.sqrt(42))

    def T(r):
        f,g,h=func(*r.reshape(-1),tc)
        g=g.reshape(4)
        return h/2-np.outer(g,g)/(4*f)

    def rotation(t):
        z=np.cos(t);s=np.sin(t)
        return np.array([[z,-s],[s,z]])

    def matrices(x):
        s,t,phi,psi,theta=x
        rp=np.diag([np.exp(s),np.exp(-s)])@rotation(phi)
        rm=rotation(theta)@np.diag([np.exp(t),-np.exp(-t)])@rotation(psi)
        return rp,rm

    def objective(x):
        rp,rm=matrices(x)
        value=np.linalg.eigvalsh(T(rp)+T(rm))[0]
        return value/(np.sum(rp*rp)+np.sum(rm*rm))

    rng=np.random.default_rng(601628)
    trials=[]
    for _ in range(3000):
        x=np.array([rng.uniform(-3,3),rng.uniform(-3,3),
                    rng.uniform(-np.pi,np.pi),rng.uniform(-np.pi,np.pi),
                    rng.uniform(-np.pi,np.pi)])
        trials.append((objective(x),x))
    trials.sort(key=lambda z:z[0])
    best=trials[0]
    opt=[]
    bounds=[(-5,5),(-5,5)]+[(-np.pi,np.pi)]*3
    for _,x in trials[:16]:
        result=minimize(objective,x,method="L-BFGS-B",bounds=bounds,
                        options={"maxiter":120,"ftol":1e-13,"gtol":1e-9})
        opt.append({"value":float(result.fun),"success":bool(result.success),
                    "message":str(result.message),"x":result.x.tolist()})
        if result.fun<best[0]:
            best=(float(result.fun),result.x)
    rp,rm=matrices(best[1])
    eig,vec=np.linalg.eigh(T(rp)+T(rm))
    out={"status":"numerical diagnostic only; absence of a negative pair is inconclusive",
         "tau":tc,"parameterization":"detRp=1,detRm=-1, five polar parameters",
         "samples":3000,"local_refinements":16,
         "best_normalized_smallest_eigenvalue":float(best[0]),
         "best_raw_smallest_eigenvalue":float(eig[0]),
         "best_parameters":best[1].tolist(),
         "Rp":rp.tolist(),"Rm":rm.tolist(),
         "candidate_A_vector":vec[:,0].tolist(),
         "refinements":opt,"elapsed_seconds":time.perf_counter()-started}
    folder=Path(__file__).resolve().parent
    (folder/"DIRECT_PAIR_SEARCH.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
