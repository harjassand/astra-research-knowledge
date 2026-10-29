import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(192)
def grid(L):
 z,w=np.polynomial.legendre.leggauss(L+1);K=2*L+1;angles=np.arange(K)*2*np.pi/K;rots=[];weights=[]
 for a in angles:
  ca,sa=np.cos(a),np.sin(a);A=np.array([[ca,-sa,0],[sa,ca,0],[0,0,1]])
  for c in angles:
   cc,sc=np.cos(c),np.sin(c);C=np.array([[cc,-sc,0],[sc,cc,0],[0,0,1]])
   for x,ww in zip(z,w):
    si=np.sqrt(1-x*x);B=np.array([[x,0,si],[0,1,0],[-si,0,x]])
    rots.append((A@B@C).ravel());weights.append(ww/(2*K*K))
 return np.array(rots),np.array(weights)
checks=0;maxerr=0;rows=[]
for L in range(1,7):
 a,w=grid(L);b,z=grid(L+3);worst=0
 for _ in range(100):
  power=np.zeros(9,dtype=int)
  for i in rng.integers(9,size=int(rng.integers(L+1))):power[i]+=1
  x=w@np.prod(a**power,axis=1);y=z@np.prod(b**power,axis=1)
  worst=max(worst,abs(x-y));checks+=1
 assert worst<1e-12
 maxerr=max(maxerr,worst);rows.append(dict(L=L,nodes=len(w),max_reference_difference=worst))
out=dict(random_monomial_checks=checks,maximum_residual=maxerr,rows=rows,scope='Numerical polynomial quadrature checks; Wigner/Legendre argument governs exactness')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
