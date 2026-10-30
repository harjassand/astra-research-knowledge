"""Pointwise drift and finite correlated-batch regression; not a global CRN proof."""
import itertools, math, json
import numpy as np
from scipy.stats import poisson
from scipy.linalg import expm
rng=np.random.default_rng(20261030)
def phi(r,u,q,beta):return math.exp(-beta*u)*(1. if r==0 else poisson.sf(r-1,q*u))
max_excess=0.;cases=0
for _ in range(500):
 n=4;L=int(rng.integers(1,5));k=int(rng.integers(1,5));a=float(rng.uniform(.1,.8));q=float(rng.uniform(.2,3));b=float(rng.uniform(.1,2));u=float(rng.uniform(.001,2));r=rng.integers(0,L+1,n)
 beta=b/(1-a)**(k-1);ph=np.array([phi(int(x),u,q,beta) for x in r]);f=1-a*ph;F=float(np.prod(f))
 # derivative + exact single-step progress = -beta F sum a phi/f.
 phprev=np.array([phi(max(0,int(x)-1),u,q,beta) for x in r]);dtime=F*sum(a*(q*(phprev-ph)-beta*ph)/f)
 progress=0.
 for i in range(n):
  if r[i]>0:progress+=q*F*((1-a*phprev[i])/f[i]-1)
 expected=-beta*F*sum(a*ph/f)
 assert abs(dtime+progress-expected)<1e-10
 # Every k-subset at equal rate ensuring per-label total b; worst output has f<=1.
 sets=list(itertools.combinations(range(n),k));rate=b/math.comb(n-1,k-1)
 adverse=sum(rate*F*(1/float(np.prod(f[list(A)]))-1) for A in sets)
 excess=dtime+progress+adverse;max_excess=max(max_excess,excess);assert excess<1e-10;cases+=1
# An explicit correlated reset of ALL 3 labels, rate b per label.
n=3;L=2;k=3;q=1.2;b=.7;a=.5;beta=b/(1-a)**(k-1)
states=list(itertools.product(range(L+1),repeat=n));idx={s:i for i,s in enumerate(states)};Q=np.zeros((len(states),len(states)))
for s in states:
 i=idx[s]
 for j in range(n):
  if s[j]:t=list(s);t[j]-=1;Q[i,idx[tuple(t)]]+=q;Q[i,i]-=q
 t=(L,)*n
 if t!=s:Q[i,idx[t]]+=b;Q[i,i]-=b
rows=[]
for T in [.05,.2,1.,2.]:
 dist=expm(T*Q)[idx[(L,)*n]];mgf=sum(dist[i]*(1-a)**s.count(0) for i,s in enumerate(states));p=phi(L,T,q,beta);bound=(1-a*p)**n
 assert mgf<=bound+1e-10
 rows.append({'T':T,'actual_mgf':float(mgf),'product_upper_bound':bound,'p':p})
print(json.dumps({'pointwise_cases':cases,'max_positive_drift_excess':max_excess,'correlated_all_label_resets':rows,'scope':'persistent fixed population only; no seed Green or global chemical import'},indent=2))
