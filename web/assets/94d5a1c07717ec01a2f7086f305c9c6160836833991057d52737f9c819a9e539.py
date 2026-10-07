"""Small matrix diagnostics for the symbolic symmetric-splitter EB bound.
No optimization, large systems, or asymptotic inference. NumPy one-thread.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
from fractions import Fraction
from math import comb, factorial, sqrt
import numpy as np
import json, time
START=time.monotonic()

def occ(n,d):
    if d==1:return [(n,)]
    return [(i,)+t for i in range(n+1) for t in occ(n-i,d-1)]
def mult(n):
    v=factorial(sum(n))
    for k in n:v//=factorial(k)
    return v
def mu(n,d,l):
    p=Fraction(1)
    for j in range(l):p*=Fraction(n-j,n+d+j)
    return p
def build(d,s):
    n=2*s; a=occ(n,d); b=occ(s,d); D=len(a); Q=len(b)
    ids={x:i for i,x in enumerate(a)}
    V=np.zeros((Q*Q,D))
    for i,k in enumerate(b):
      for j,l in enumerate(b):
        t=tuple(x+y for x,y in zip(k,l))
        V[i*Q+j,ids[t]]=sqrt(np.prod([comb(x,y) for x,y in zip(t,k)])/comb(n,s))
    K=[V.reshape(Q,Q,D)[:,j,:] for j in range(Q)]
    def T(x):return sum(k@x@k.T for k in K)
    def R(x):return Q/D*sum(k.T@x@k for k in K)
    def Phi(x):return R(T(x))
    PH=np.empty((D*D,D*D))
    for i in range(D):
      for j in range(D):
        x=np.zeros((D,D));x[i,j]=1
        PH[:,i*D+j]=Phi(x).reshape(-1)
    PS=np.zeros_like(PH)
    pf=[sqrt(mult(x)) for x in a]
    base=Fraction(D*factorial(d-1),factorial(2*n+d-1))
    for g,gg in enumerate(a):
      for h,hh in enumerate(a):
        for i,aa in enumerate(a):
          for j,bb in enumerate(a):
            left=tuple(x+y for x,y in zip(aa,hh))
            right=tuple(x+y for x,y in zip(bb,gg))
            if left!=right:continue
            mom=base
            for k in right:mom*=factorial(k)
            PS[g*D+h,i*D+j]=float(mom)*pf[g]*pf[h]*pf[i]*pf[j]
    expected=[]; expected_psi=[]
    for l in range(n+1):
      dl=comb(l+d-1,d-1);prev=0 if l==0 else comb(l+d-2,d-1)
      m=dl*dl-prev*prev
      lam=mu(s,d,l)/mu(n,d,l) if l<=s else Fraction(0)
      expected.extend([float(lam)]*m)
      expected_psi.extend([float(mu(n,d,l))]*m)
    rng=np.random.default_rng(700402+d*10+s)
    z=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));x=z@z.conj().T;x/=np.trace(x)
    vv=V@x@V.T
    joint=np.zeros((D*D,D*D),complex)
    for k in K:
      for l in K:
        C=Q/D*np.kron(k.T,l.T)
        joint+=C@vv@C.T
    j4=joint.reshape(D,D,D,D)
    B=np.trace(j4,axis1=1,axis2=3);C=np.trace(j4,axis1=0,axis2=2)
    eigph=np.linalg.eigvalsh((PH+PH.T)/2)
    eigps=np.linalg.eigvalsh((PS+PS.T)/2)
    rr={'d':d,'s':s,'N':n,'D_N':D,'D_s':Q,
      'isometry_residual':float(np.max(np.abs(V.T@V-np.eye(D)))),
      'reference_T_residual':float(np.max(np.abs(T(np.eye(D)/D)-np.eye(Q)/Q))),
      'reference_Phi_residual':float(np.max(np.abs(Phi(np.eye(D)/D)-np.eye(D)/D))),
      'Phi_symmetry_residual':float(np.max(np.abs(PH-PH.T))),
      'Phi_spectrum_residual':float(np.max(np.abs(eigph-np.sort(expected)))),
      'Psi_spectrum_residual':float(np.max(np.abs(eigps-np.sort(expected_psi)))),
      'commuting_superoperators_residual':float(np.max(np.abs(PH@PS-PS@PH))),
      'Dirichlet_c2_min_eig':float(np.linalg.eigvalsh(2*(np.eye(D*D)-PH)-(np.eye(D*D)-PS)).min()),
      'joint_min_eig':float(np.linalg.eigvalsh(joint).min()),
      'joint_trace_residual':float(abs(np.trace(joint)-1)),
      'both_marginal_residual':float(max(np.max(np.abs(B-Phi(x))),np.max(np.abs(C-Phi(x)))))}
    tol=1e-10
    assert all(v<tol for k,v in rr.items() if 'residual' in k),rr
    assert rr['Dirichlet_c2_min_eig']>-tol and rr['joint_min_eig']>-tol,rr
    return rr

def main():
    fixtures=[build(d,s) for d,s in [(2,1),(3,1),(4,1),(2,2),(3,2)]]
    maxratio=Fraction(0); where=None; cases=0
    for d in range(2,26):
      for s in range(1,31):
        for l in range(1,2*s+1):
          a=mu(2*s,d,l);lam=mu(s,d,l)/a if l<=s else Fraction(0)
          ratio=(1-a)/(1-lam)
          assert ratio<=2
          if ratio>maxratio:maxratio=ratio;where=(d,s,l)
          cases+=1
    result={'status':'PASS_DIAGNOSTIC_ONLY','fixtures':fixtures,'exact_scalar_cases':cases,
      'max_scalar_ratio':str(maxratio),'max_ratio_parameters_d_s_l':where,
      'cpu_wall_seconds':time.monotonic()-START,
      'scope':'Small explicit matrix transcriptions and finite exact rational scalar checks. General theorem justified by symbolic proof, not these tests.'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
