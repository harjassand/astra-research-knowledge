import numpy as np, math, json
from fractions import Fraction as F
from pathlib import Path
rng=np.random.default_rng(1311)
def polar(A):
 u,s,v=np.linalg.svd(A);return u@v
rows=[]
for a in [.00001,.01,.2]:
 for trial in range(50):
  U=np.linalg.qr(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))[0]
  V=np.linalg.qr(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))[0]
  G=U@np.diag([a,1.1*a,.5,2])@V.conj().T
  E=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));E*=a*.01/np.linalg.norm(E)
  Q=polar(G);P=polar(G+E)
  err=np.linalg.norm(P-Q);bound=2*np.linalg.norm(E)/a
  assert err<=bound+1e-12
  rows.append(err/bound)
# Worst-corner derivative and matrix-rounding constants at declared scales.
from mpmath import mp
mp.dps=70; derivatives=[]
for nu in [F(1,2),F(1,10),F(1,1000),F(1,10**12)]:
 u0=nu/128;a=nu/16;h=nu*a*u0*u0/512
 assert h<=u0
 assert 60*h/u0**2+6*nu*a/512<nu*a/4
 assert 32*u0+16*a*a<nu/2
 for u in [mp.mpf(u0.numerator)/(2*u0.denominator),1-mp.mpf(u0.numerator)/(2*u0.denominator)]:
  radial=1/(2*u*mp.sqrt(-mp.log(u)));angular=2*mp.pi*mp.sqrt(-mp.log(u));bd=10/(mp.mpf(u0.numerator)/u0.denominator)**2
  assert max(radial,angular)<bd;derivatives.append(float(max(radial,angular)/bd))
# BHH primary's explicit bound dominated by integer prescription.
checks=0;minratio=mp.inf
for q in [2,3,8,32]:
 for t in [1,2,3,17,100]:
  for eps in [F(1,2),F(1,100),F(1,10**8)]:
   ee=mp.mpf(eps.numerator)/eps.denominator;ell=math.ceil(math.log2(4*t));c=math.ceil(math.log2(8/float(eps)))
   L=170000*q*ell**2*t**10*(2*q*t+c)
   bhh=170000*q*ell**2*mp.mpf(t)**(5+mp.mpf('3.1')/mp.log(2))*(2*q*t*mp.log(2)+mp.log(8/ee))
   assert L>=bhh;checks+=1;minratio=min(minratio,L/bhh)
res=dict(near_singular_polar_cases=len(rows),max_polar_bound_ratio=max(rows),derivative_corner_checks=len(derivatives),max_derivative_ratio=max(derivatives),BHH_length_cases=checks,min_BHH_length_ratio=str(minratio),scope='Independent arithmetic and near-singular stability diagnostics, not certified sampler or full quantum design execution')
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
