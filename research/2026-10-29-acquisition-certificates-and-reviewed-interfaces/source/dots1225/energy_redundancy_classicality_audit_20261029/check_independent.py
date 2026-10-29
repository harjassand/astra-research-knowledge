import numpy as np, json, hashlib
from fractions import Fraction as F
from pathlib import Path
from itertools import product
p=Path(__file__).parent
root=p.parent/'energy_redundancy_classicality_20261029'
manifest=json.loads((root/'AUTHOR_FREEZE.json').read_text())
assert all(hashlib.sha256((root/f).read_bytes()).hexdigest()==h for f,h in manifest.items())
# Exact rational path/cutoff checks: no invariant-family premise; singleton input.
rho=[F(9,10),F(1,10),F(0)]
T0=[[F(9,10),F(0),F(1)],[F(0),F(1),F(0)],[F(1,10),F(0),F(0)]]
T1=[[F(1),F(0),F(0)],[F(0),F(3,4),F(1)],[F(0),F(1,4),F(0)]]
# These stochastic marginals have a legitimate joint classical broadcast extension.
def app(M,x):return [sum(a*b for a,b in zip(row,x)) for row in M]
def td(x,y):return sum(abs(a-b) for a,b in zip(x,y))/2
def cutoff(x):return [x[0]+x[2],x[1],F(0)]
b=max(td(app(T,rho),rho) for T in [T0,T1]);cases=0
# Includes a coherent-input analogue below; here replace input by an arbitrary perturbed state.
original=[F(4,5),F(1,10),F(1,10)]
br=max(td(app(T,original),original) for T in [T0,T1]);dr=td(original,cutoff(original))
for ell in range(9):
 for path in product([T0,T1],repeat=ell):
  x=rho[:];y=original[:];z=cutoff(original)
  for T in path:x=app(T,x);y=app(T,y);z=app(T,z)
  assert td(x,rho)<=ell*b
  assert td(cutoff(z),cutoff(original))<=ell*br+dr
  cases+=1
# Coherent cutoff tests include tiny tails and off-diagonal coherence; projector is not normalized postselection.
max_ratio=0.;rows=[]
for tail in [1e-12,1e-9,1e-6,.001,.01,.1,.5,.9]:
 v=np.array([0,np.sqrt(1-tail),np.sqrt(tail)],complex);rr=np.outer(v,v.conj())
 c=np.diag([tail,1-tail,0]).astype(complex)
 distance=float(abs(np.linalg.eigvalsh(rr-c)).sum()/2)
 bound=np.sqrt(tail)+tail/2
 assert distance<=bound+1e-14
 # The exact nonzero difference eigenvalues are -p and (p±sqrt(4p-3p²))/2.
 exact=(tail+np.sqrt(4*tail-3*tail*tail))/2
 assert abs(distance-exact)<1e-14
 max_ratio=max(max_ratio,distance/bound);rows.append({'tail':tail,'distance':distance,'bound':bound})
# Roundup/substitution and inversion constants over broad grids.
constant_checks=0
for E in [1e-9,.01,1.,1e6]:
 for b0 in [1e-6,.001,.01,.1,.9]:
  R=16*E/b0**2;d=int(R)+1
  ell=int(np.ceil(2*np.log2(d)+np.log2(1/b0)))
  lhs=ell*b0+2*(np.sqrt(E/R)+E/R)+d*d/2**ell
  rhs=b0*(2*np.log2(d)+np.log2(1/b0)+21/8)
  assert lhs<=rhs+1e-10
  constant_checks+=1
out={'author_manifest_verified':True,'exact_rational_path_and_cutoff_cases':cases,'coherent_tail_cases':rows,'max_gentle_ratio':max_ratio,'constant_checks':constant_checks,'scope':'Exact rational nonclosed-family path checks and floating coherent cutoff/constant diagnostics; not full de Finetti compiler or laboratory execution.'}
(p/'independent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
