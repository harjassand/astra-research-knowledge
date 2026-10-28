#!/usr/bin/env python3
"""Acquire rational opposite determinant cuts at one fixed base point."""
import json,time
from pathlib import Path
import numpy as np
from scipy.optimize import differential_evolution
from geometry_search import pair_ratio,sigma,sphere

OUT=Path(__file__).resolve().parent
H=np.array([np.diag([1.,-1.,1.,-1.]),
            [[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],
            [[0,0,0,1],[0,0,-1,0],[0,-1,0,0],[1,0,0,0]]])
I=np.array([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
K=np.array([[1.,0,.99],[0,1.,0],[.99,0,3.52]])

def hopf(A):return np.einsum('i,kij,j->k',A,H,A)
def lift(n):
    a=np.sqrt((1+n[0])/2)
    return np.array([a,n[1]/(2*a),0.,n[2]/(2*a)])
def tf(R):
    h=hopf(R);f=h@K@h;b=H@R
    df=4*b.T@K@h
    hh=2*np.einsum('k,kij->ij',K@h,H)+4*b.T@K@b
    return hh-np.outer(df,df)/(4*f)
def minimize_phase(A,n):
    R=lift(n);V=np.stack((R,I@R),axis=1)
    # T_F is equivariant under this phase, so minimize A against rotated R.
    W=np.stack((A,-I@A),axis=1)
    M=W.T@tf(R)@W
    ev,U=np.linalg.eigh(M)
    coeff=U[:,0]
    RR=V@coeff
    assert abs(float(A@tf(RR)@A)-float(ev[0]))<1e-10
    return RR,float(ev[0])

def main():
    started=time.perf_counter()
    fit=differential_evolution(lambda x:-float(pair_ratio(K,np.array([np.pi,x[0],0.,x[1]]))),
          [(1e-5,np.pi/2)]*2,seed=1728,tol=1e-12)
    n=sphere(np.array([np.pi,fit.x[0]]));p=sphere(np.array([0.,fit.x[1]]))
    sn,sp=sigma(K,n),sigma(K,p)
    v=(p[2]*(K@n-sn*n)-n[2]*(K@p-sp*p))
    m=-v/np.linalg.norm(v)
    A=lift(m)
    R,c1=minimize_phase(A,n);S,c2=minimize_phase(A,-p)
    den=10**7
    data={'status':'ACQUIRED_NUMERICAL_ONLY_PENDING_EXACT_REPLAY','K':K.tolist(),
          'F':'x^2+y^2+(99/50)xz+(88/25)z^2',
          'denominator':den,'A':[int(x) for x in np.rint(A*den)],
          'R_plus':[int(x) for x in np.rint(R*den)],
          'R_minus':[int(x) for x in np.rint(S*den)],
          'angles':fit.x.tolist(),'pair_ratio':-fit.fun,
          'unrounded_cuts':[c1,c2],'unrounded_hopf_base':m.tolist(),
          'elapsed_seconds':time.perf_counter()-started}
    (OUT/'OPPOSITE_CUT_INPUT.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
