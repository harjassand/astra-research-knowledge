"""Exact rational regression: nearest-neighbor gap hierarchy must start at n=3.
At n=2 a projector interaction gives gamma_2=1, but the proper AKLT parent
has a four-site periodic eigenvector at energy 1/3. All checks below are exact
integer/Fraction arithmetic; no floating eigensolver is used.
"""
from fractions import Fraction as F
from math import lcm,gcd
from pathlib import Path
import itertools,json
import numpy as np
OUT=Path(__file__).parent
# Six times the spin-2 projector in {|+>,|0>,|->}^{tensor 2}.
hi=np.zeros((9,9),dtype=np.int64)
hi[0,0]=hi[8,8]=6
for inds in [(1,3),(5,7)]:
 for i in inds:
  for j in inds:hi[i,j]=3
inds=[2,4,6];v=[1,2,1]
for a,i in enumerate(inds):
 for b,j in enumerate(inds):hi[i,j]=v[a]*v[b]
assert np.array_equal(hi@hi,6*hi)
assert np.array_equal(hi,hi.T) and np.any(hi)
N=4;d=3;dim=d**N;states=list(itertools.product(range(d),repeat=N));lookup={s:i for i,s in enumerate(states)}
H=np.zeros((dim,dim),dtype=np.int64)
for col,s in enumerate(states):
 for i in range(N):
  j=(i+1)%N;pair=d*s[i]+s[j]
  for q in range(d*d):
   if hi[q,pair]:
    t=list(s);t[i],t[j]=divmod(q,d);H[lookup[tuple(t)],col]+=hi[q,pair]
# Exact null vector of 6 H_physical - 2 I, hence E=1/3.
M=H-2*np.eye(dim,dtype=np.int64)
a=[[F(int(x)) for x in row] for row in M];piv=[];r=0
for c in range(dim):
 pivot=next((i for i in range(r,dim) if a[i][c]),None)
 if pivot is None:continue
 a[r],a[pivot]=a[pivot],a[r];z=a[r][c];a[r]=[x/z for x in a[r]]
 for i in range(r+1,dim):
  z=a[i][c]
  if z:a[i]=[x-z*y for x,y in zip(a[i],a[r])]
 piv.append(c);r+=1
 if r==dim:break
free=next(c for c in range(dim) if c not in piv);x=[F(0)]*dim;x[free]=F(1)
for i in range(len(piv)-1,-1,-1):
 c=piv[i];x[c]=-sum(a[i][j]*x[j] for j in range(c+1,dim))
den=lcm(*(q.denominator for q in x));vec=[int(q*den) for q in x];g=0
for q in vec:g=gcd(g,abs(q))
vec=[q//g for q in vec];assert any(vec)
for i in range(dim):assert sum(int(M[i,j])*vec[j] for j in range(dim))==0
result={'status':'PASS','natural_nearest_neighbor_minimum_level':3,'literal_appendix_D_minimum_level':4,
 'excluded_level_n2_objective_exact':'gamma_2=1 because h^2=h and Tr(rho h)=1; delta=1,Y=0 is primal feasible',
 'four_site_periodic_AKLT_excited_eigenvalue_exact':'1/3',
 'invalid_n2_claim':'gamma_2=1 is not <= Delta_4, since Delta_4<=1/3, even though 4>=2*2',
 'integer_interaction_scale':6,'interaction_integer_matrix':hi.tolist(),
 'periodic_sites':N,'physical_basis_order':'lexicographic 0,1,2 corresponding to +,0,-',
 'exact_integer_eigenvector':vec,'exact_integer_residual_zero':True,
 'note':'Every identity proving this counterexample uses exact integer/Fraction arithmetic; no floating eigensolver or rank calculation is used.'}
(OUT/'minimum_level_regression.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['interaction_integer_matrix','exact_integer_eigenvector']},indent=2))
