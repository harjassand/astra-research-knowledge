"""Search full scalar-minor support incompatibility with background eliminated.

The background is the leading eigenvector of the two-cut difference.
Common left SO(2) symmetry eliminates one angle from the pair of cuts.
Failure of a bounded search is never a polyconvexity theorem.
"""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import differential_evolution

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--a',default='12');ap.add_argument('--b',default='3.975');args=ap.parse_args()
    start=time.perf_counter()
    aa=sp.symbols('a b c d');a,b,c,d=aa
    q=a*d-b*c;T=sum(x*x for x in aa);x=a*a+c*c-b*b-d*d
    F=T*T+sp.Rational(args.a)*q*q+sp.Rational(args.b)*q*x
    fs=sp.lambdify(aa,F,'numpy');gs=sp.lambdify(aa,sp.Matrix([sp.diff(F,x) for x in aa]),'numpy');hs=sp.lambdify(aa,sp.hessian(F,aa),'numpy')
    def tf(R):
        z=R.reshape(-1);g=gs(*z).reshape(-1)
        return .5*hs(*z)-np.outer(g,g)/(4*fs(*z))
    def rot(th):
        c=np.cos(th);s=np.sin(th);return np.array([[c,-s],[s,c]])
    def cuts(z):
        sp_,sm,phip,phim,rel=z
        Rp=np.diag([np.exp(sp_),np.exp(-sp_)])@rot(phip)
        Rm=rot(rel)@np.diag([np.exp(sm),-np.exp(-sm)])@rot(phim)
        return Rp,Rm
    def get(z,vectors=False):
        Rp,Rm=cuts(z);D=-tf(Rm)-tf(Rp)
        if vectors:return np.linalg.eigh(D)
        return np.linalg.eigvalsh(D)[-1]
    fit=differential_evolution(lambda z:-get(z),[(0,5),(0,5),(-np.pi,np.pi),(-np.pi,np.pi),(-np.pi,np.pi)],
                               seed=246,polish=True,maxiter=1500,popsize=18,tol=1e-10)
    eig,vec=get(fit.x,True);Rp,Rm=cuts(fit.x)
    result=dict(a=args.a,b=args.b,gap=float(eig[-1]),A=vec[:,-1].reshape(2,2).tolist(),Rplus=Rp.tolist(),Rminus=Rm.tolist(),
                parameters=fit.x.tolist(),success=fit.success,nfev=fit.nfev,seconds=time.perf_counter()-start,
                scope='Bounded floating search; positive gaps need exact qualification; negative gaps do not prove PC')
    Path(__file__).with_name(f'FULL_SUPPORT_a{args.a}_b{args.b}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
