#!/usr/bin/env python3
"""Non-SDP true-PC obstruction search. Numerical screening is not proof."""
import sys
sys.dont_write_bytecode=True
import json,time
from pathlib import Path
import numpy as np
import sympy as S
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/
    "sol6_openings_20261027/independent_opening/vendor"))
from scipy.optimize import minimize,minimize_scalar


def main():
    started=time.perf_counter()
    a,b,c,d,C,dx,dy,R=S.symbols("a b c d C dx dy R",real=True)
    v=(a,b,c,d)
    x=a*a+c*c-b*b-d*d;y=2*(a*b+c*d);z=2*(a*d-b*c)
    F=x*x+C*y*y+R*z*z+2*dx*x*z+2*dy*y*z
    grad=S.Matrix([S.diff(F,w) for w in v])
    fun=S.lambdify((*v,C,dx,dy,R),(F,grad,S.hessian(F,v)),"numpy",cse=True)
    th=np.linspace(0,2*np.pi,2048,endpoint=False)
    ct,st=np.cos(th),np.sin(th)
    rng=np.random.default_rng(842110)

    def roc_threshold(C,dx,dy):
        k=ct*ct+C*st*st;n=st*st+C*ct*ct;l=(C-1)*ct*st
        m=dx*ct+dy*st;p=-dx*st+dy*ct
        aa=2*k*n-k*k-3*l*l-m*m
        if aa.min()<=1e-5:return None
        values=(k*k+3*m*m+l*l+4*(k*p-l*m)**2/aa)/(2*k)
        maximum=float(values.max())
        def minus(t):
            co=np.cos(t);si=np.sin(t)
            k=co*co+C*si*si;n=si*si+C*co*co;l=(C-1)*co*si
            m=dx*co+dy*si;p=-dx*si+dy*co
            aa=2*k*n-k*k-3*l*l-m*m
            return -(k*k+3*m*m+l*l+4*(k*p-l*m)**2/aa)/(2*k)
        for idx in np.argsort(values)[-4:]:
            t=th[idx]
            opt=minimize_scalar(minus,bounds=(t-.01,t+.01),method="bounded",
                                options={"xatol":1e-12})
            maximum=max(maximum,float(-opt.fun))
        return maximum,float(aa.min())

    def rotation(t):
        co=np.cos(t);si=np.sin(t)
        return np.array([[co,-si],[si,co]])

    def matrices(x):
        s,t,phi,psi,theta=x
        return (np.diag([np.exp(s),np.exp(-s)])@rotation(phi),
                rotation(theta)@np.diag([np.exp(t),-np.exp(-t)])@rotation(psi))

    params=np.column_stack([rng.uniform(-3.5,3.5,(512,2)),
                            rng.uniform(-np.pi,np.pi,(512,3))])
    pairs=[matrices(t) for t in params]
    rows=[];best=None
    for trial in range(100):
        C=float(rng.uniform(.56,1.9))
        angle=float(rng.uniform(-np.pi,np.pi))
        k=ct*ct+C*st*st;n=st*st+C*ct*ct;l=(C-1)*ct*st
        abase=2*k*n-k*k-3*l*l
        proj=(np.cos(angle)*ct+np.sin(angle)*st)**2
        maxsize=float(np.min(abase/np.maximum(proj,1e-15)))
        if maxsize<=0:continue
        size=np.sqrt(maxsize*float(rng.uniform(.15,.985)))
        dx=float(size*np.cos(angle));dy=float(size*np.sin(angle))
        threshold=roc_threshold(C,dx,dy)
        if threshold is None:continue
        r=float(np.ceil((threshold[0]+.001)*100000)/100000)
        spec=(C,dx,dy,r)
        def T(mat):
            f,g,h=fun(*mat.reshape(-1),*spec)
            g=g.reshape(4)
            return h/2-np.outer(g,g)/(4*f)
        def obj(t):
            rp,rm=matrices(t)
            return np.linalg.eigvalsh(T(rp)+T(rm))[0]/(
                np.sum(rp*rp)+np.sum(rm*rm))
        localbest=None
        for idx,(rp,rm) in enumerate(pairs):
            value=float(np.linalg.eigvalsh(T(rp)+T(rm))[0]/(
                np.sum(rp*rp)+np.sum(rm*rm)))
            if localbest is None or value<localbest[0]:
                localbest=(value,params[idx])
        opt=minimize(obj,localbest[1],method="L-BFGS-B",
                     bounds=[(-5,5)]*2+[(-np.pi,np.pi)]*3,
                     options={"maxiter":80,"ftol":1e-12})
        if opt.fun<localbest[0]:localbest=(float(opt.fun),opt.x)
        row={"trial":trial,"Kxy_diag":[1,C],"d":[dx,dy],"Kzz":r,
             "numeric_ROC_r_threshold":threshold[0],
             "min_schur_A_grid":threshold[1],
             "direct_pair_minimum":localbest[0],
             "pair_parameters":localbest[1].tolist()}
        rows.append(row)
        if best is None or row["direct_pair_minimum"]<best["direct_pair_minimum"]:
            best=row
    out={"status":"numerical only; no ROC or PC theorem from these signs",
         "candidate_count":len(rows),"pairs_per_candidate":512,
         "best":best,"candidates":rows,"elapsed_seconds":time.perf_counter()-started,
         "no_SDP_used":True,"exact_promotion_executed":False}
    folder=Path(__file__).resolve().parent
    (folder/"EVEN_SECTOR_SEARCH.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":main()
