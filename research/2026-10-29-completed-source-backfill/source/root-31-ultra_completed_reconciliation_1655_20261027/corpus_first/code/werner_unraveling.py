"""Constructive all-dimensional two-site separable unraveling for equal Werner noise.
This is a numerical replay of the accompanying analytic proof, not a proof by grid.
"""
import sys
sys.dont_write_bytecode=True
import numpy as np,json,time
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
CSTAR=(1+np.sqrt(3))/2

def prime_at_least(d):
 for p in range(max(d,3),max(d,3)*3):
  if p%2 and all(p%k for k in range(2,int(p**.5)+1)):return p
 raise RuntimeError('prime search')

def nonnegative_factor(lam,c):
 d=len(lam);x=np.sqrt(lam);delta=c*c-2*c*lam
 A=np.outer(x,x)+np.diag(delta)
 order=list(np.argsort(lam));M=A[np.ix_(order,order)].copy();cols=[]
 for k in range(d):
  pivot=M[k,k]
  assert pivot> -1e-11
  if pivot<1e-13:
   assert np.max(abs(M[k:,k]))<1e-10
   continue
  v=np.zeros(d);v[k:]=M[k:,k]/np.sqrt(pivot)
  assert min(v)>=-2e-10
  cols.append(v);M-=np.outer(v,v);M=(M+M.T)/2
 V=np.array(cols).T;unsorted=np.empty_like(V);unsorted[order,:]=V
 assert np.max(abs(unsorted@unsorted.T-A))<2e-9
 return np.maximum(unsorted,0),A

def phase_moments(d):
 p=prime_at_least(d);w=np.exp(2j*np.pi/p);mom=np.zeros((d,d,d,d),complex)
 for a in range(p):
  for b in range(p):
   z=np.array([w**((a*i+b*i*i)%p) for i in range(d)])
   mom+=np.einsum('i,j,k,l->ijkl',z,z.conj(),z.conj(),z)/(p*p)
 wanted=np.zeros_like(mom)
 for i in range(d):
  for j in range(d):
   for k in range(d):
    for l in range(d):wanted[i,j,k,l]=int((i==j and k==l) or (i==k and j==l))
 return p,float(np.max(abs(mom-wanted)))

def replay():
 start=time.monotonic();rng=np.random.default_rng(800632);cases=[]
 for d in (2,3,4,6,9,12):
  for c in (CSTAR,1.4,1.5,1.8,2.):
   maximum=0.;minimum=1.;masserr=0.
   for trial in range(60):
    if trial==0:lam=np.r_[.5,.5,np.zeros(d-2)]
    elif trial==1:lam=np.r_[1.,np.zeros(d-1)]
    elif trial==2:lam=np.r_[.99,np.full(d-1,.01/(d-1))]
    else:lam=rng.dirichlet(np.ones(d)*.4)
    V,A=nonnegative_factor(lam,c);x=np.sqrt(lam)
    B=c*c-c*(lam[:,None]+lam[None,:])-np.outer(x,x)
    np.fill_diagonal(B,0.)
    assert np.min(B)>-2e-12
    mass=np.sum(np.sum(V,axis=0)**2)+np.sum(B)
    maximum=max(maximum,float(np.max(abs(V@V.T-A))))
    minimum=min(minimum,float(np.min(B)))
    masserr=max(masserr,abs(mass-(c*d-1)**2))
   p,err=phase_moments(d)
   assert err<1e-11
   cases.append(dict(d=d,c=float(c),spectra=60,max_factor_residual=maximum,
    min_residual_population=minimum,max_mass_residual=masserr,
    phase_prime=p,phase_assignments=p*p,phase_moment_residual=err))
 result=dict(threshold='(1+sqrt(3))/2',all_dimensions='d>=2 (analytic proof)',
  tested_spectra=sum(r['spectra'] for r in cases),cases=cases,
  scope='Explicit equal-Werner-noise two-site decomposition; arithmetic construction, no generic separability oracle; numerical replay does not establish novelty.',
  elapsed_seconds=time.monotonic()-start)
 (BASE/'results'/'UNRAVELING_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))

if __name__=='__main__':replay()
