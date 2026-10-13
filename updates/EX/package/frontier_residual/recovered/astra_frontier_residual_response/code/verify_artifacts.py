"""Reconstruct every stored response certificate without any numerical optimization."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time,sys,resource,math
import numpy as np
from jet_certificate import compile_exact
from jet_design import bernstein,ev

def verify_one(p):
 t=time.perf_counter();data=np.load(p,allow_pickle=False);ref=json.loads(p.with_suffix('.json').read_text())
 assert hashlib.sha256(p.read_bytes()).hexdigest()==ref['witness_sha256']
 fw=[tuple(map(int,w)) for w in data['fw']];gw=[tuple(map(int,w)) for w in data['gw']]
 pars=dict(zip(['t','U','V','d'],data['params']))
 got=compile_exact(fw,gw,data['FN'],data['GN'],int(data['den'][0]),pars)
 for k,v in got.items():assert v==ref[k],(p.name,k)
 return dict(file=p.name,seconds=time.perf_counter()-t,verified=True,nonzero_f_jet_coefficients=int(np.count_nonzero(data['FN'])),nonzero_g_jet_coefficients=int(np.count_nonzero(data['GN'])))

def run(root):
 t=time.perf_counter();names=['V0','Vhalf','V1','V1half','V3','V2','V2half']
 rows=[verify_one(root/'fresh/witness.npz')]+[verify_one(root/'anchors'/f'{n}.npz') for n in names]
 # Reject an actual population-balance defect in a copied finite packet.
 p=root/'anchors/V0.npz';data=np.load(p,allow_pickle=False);fw=[tuple(map(int,w)) for w in data['fw']];gw=[tuple(map(int,w)) for w in data['gw']]
 from fast_algebra import build
 rr,aa=build(fw,1.,0.,0.);pop=aa[[w[0]==0 for w in rr],:].tocsc();j=int(np.flatnonzero(np.diff(pop.indptr))[0])
 ff=data['FN'].copy();ff[0,j]+=1
 try:compile_exact(fw,gw,ff,data['GN'],int(data['den'][0]),dict(zip(['t','U','V','d'],data['params'])))
 except AssertionError as e:
  assert 'population imbalance' in str(e);corrupt=True
 else:raise RuntimeError('Unbalanced corrupted packet accepted')
 # Exact convex-hull bounds checked against independent rational evaluations.
 rng=np.random.default_rng(8231);cnt=0
 for n in range(1,10):
  for rep in range(8):
   c=[F(int(x),17) for x in rng.integers(-99,100,size=n+1)]
   a=F(int(rng.integers(-20,20)),7);b=a+F(int(rng.integers(1,20)),11)
   lo,hi=bernstein(c,a,b)
   for i in range(41):assert lo<=ev(c,a+(b-a)*F(i,40))<=hi;cnt+=1
 out=dict(verified=True,packets=rows,corrupted_population_defect_rejected=corrupt,exact_Bernstein_point_checks=cnt,seconds=time.perf_counter()-t,peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Independent of optimization, same-investigation code; not external proof review or formal verification.')
 (root/'standalone_verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));return out
if __name__=='__main__':run(Path(sys.argv[1]))
