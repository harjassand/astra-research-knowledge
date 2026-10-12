"""Exact moment checks and floating checks of the isospectral/full-state bridge."""
from fractions import Fraction as F
from math import comb, factorial, sqrt
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm

counts={}
def ck(k,x):
    if not x: raise AssertionError(k)
    counts[k]=counts.get(k,0)+1

def inner(p,q,x,w):
    return sum(wi*sum(a*xx**i for i,a in enumerate(p))*sum(a*xx**i for i,a in enumerate(q)) for xx,wi in zip(x,w))

def jacobi(x,w):
    pols=[]; norms=[]; aa=[]; bb=[]
    for j in range(len(x)):
        p=[F(0)]*j+[F(1)]
        for q,norm in zip(pols,norms):
            coeff=inner(p,q,x,w)/norm
            for k,z in enumerate(q): p[k]-=coeff*z
        norm=inner(p,p,x,w)
        pols.append(p); norms.append(norm)
        aa.append(inner([F(0)]+p,p,x,w)/norm)
        if j: bb.append(norm/norms[j-1])
    mat=np.diag([float(v) for v in aa])
    for j,v in enumerate(bb): mat[j,j+1]=mat[j+1,j]=-sqrt(float(v))
    return aa,bb,mat

max_eig=0.
for m in [1,3,5,7,9,11]:
    n=m+1; d=(m+1)//2
    x=[F(3,8)+F(j,4*m) for j in range(n)]
    wp=[F(1,4*n)+(F(1,2*n) if j%2==0 else 0)+(F(comb(m,j),2**m) if j%2==0 else 0) for j in range(n)]
    wm=[F(1,4*n)+(F(1,2*n) if j%2==0 else 0)+(F(comb(m,j),2**m) if j%2 else 0) for j in range(n)]
    ck('probability_measures',sum(wp)==1 and sum(wm)==1)
    ck('weight_floor',min(wp+wm)>=F(1,4*n))
    for k in range(m):
        ck('exact_moment_match',sum((p-q)*xx**k for p,q,xx in zip(wp,wm,x))==0)
    ap,bp,A=jacobi(x,wp); am,bm,B=jacobi(x,wm)
    for j in range(d-1): ck('exact_common_diagonal',ap[j]==am[j])
    for j in range(d-1): ck('exact_common_bond_squared',bp[j]==bm[j])
    e=np.eye(n)[:,0]
    for j in range(d): ck('full_vector_jet_match',np.linalg.norm(np.linalg.matrix_power(A,j)@e-np.linalg.matrix_power(B,j)@e)<2e-13)
    err=max(np.max(abs(np.linalg.eigvalsh(A)-np.array(x,float))),np.max(abs(np.linalg.eigvalsh(B)-np.array(x,float))));max_eig=max(max_eig,float(err))
    ck('isospectral_float',err<2e-13)
    for tau in [0.,.01,.1,1.,5.,10.,25.,100.]:
        y=expm(-tau*A/2)@e; z=expm(-tau*B/2)@e
        xb=np.r_[1.,np.sqrt(3)*y]; xc=np.r_[1.,np.sqrt(3)*z]
        xb/=np.linalg.norm(xb);xc/=np.linalg.norm(xc)
        # Stable distance through wedge, rather than subtracting nearly equal fidelities.
        dist=np.linalg.norm(xb-xc)*np.sqrt(max(0.,1-np.linalg.norm(xb-xc)**2/4))
        bound=2*np.sqrt(3)*min((tau/16)**d/factorial(d),3.**(-d))
        ck('full_snapshot_bridge_bound',dist<=bound+5e-13)
    t=4*np.pi*m
    amp1=(1+3*np.vdot(e,expm(-1j*t*A)@e))/4
    amp2=(1+3*np.vdot(e,expm(-1j*t*B)@e))/4
    ck('real_time_return_probabilities',abs(abs(amp1)**2-97/256)<5e-13 and abs(abs(amp2)**2-25/256)<5e-13)

out={'status':'passed','checks_by_type':counts,'total_assertions':sum(counts.values()),'max_spectral_error':max_eig,'scope':'Fraction arithmetic for moments and recurrence prefixes; floating arithmetic for matrices and propagators. No general-proof certification.'}
Path(__file__).with_name('genesis_bridge_diagnostics.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
