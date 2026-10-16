import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import resource
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import numpy as np,json,sys,time
sys.path.insert(0,str(__import__('pathlib').Path(__file__).parents[1]))
import diagnostic as d
from stream_norm import norm_sum
from pathlib import Path
start=time.perf_counter();rng=np.random.default_rng(432)
# Small dense tensors including mixed signs and a near cancellation.
def dense(q):
 t=q[0][0]
 for a in q[1:]:t=np.tensordot(t,a,axes=(-1,0))
 return t[...,0]
results=[]
for scale in [1.,1e-9]:
 x=[rng.normal(size=(1,5,3)),rng.normal(size=(3,5,4)),rng.normal(size=(4,5,1))]
 y=[a.copy() for a in x];y[1]+=scale*rng.normal(size=y[1].shape)
 terms=[(x,1.),(y,-.99999999)];got,meta=norm_sum(terms);expected=np.linalg.norm(dense(x)-.99999999*dense(y));rel=abs(got-expected)/expected
 assert rel<1e-6 if scale<1e-8 else rel<1e-12
 results.append(dict(kind='dense',perturbation=scale,got=got,expected=expected,relative_error=rel,**meta))
z=np.load(d.P/'candidate.npz');m=z['time_coefficients'].shape[0];basis=[[z[f'basis_{j}_core_{i}'] for i in range(8)] for j in range(m)];C=z['projected_generator'];mu=np.exp(-.5*((d.N-50)/4)**2);mu/=mu.sum();mu=.999*mu+.001/d.D
for j in [0,1,12]:
 a=d.Agrid(basis[j]);terms=[(a,1)]+[(basis[i],-C[i,j]) for i in range(m)];got,meta=norm_sum(terms,[mu]*8)
 record=json.loads((d.P/'result.json').read_text())['details'][j];expected=record['full_weighted_grid_defect_norm'];rel=abs(got-expected)/expected;assert rel<1e-8
 results.append(dict(kind='prior_full_defect',column=j,got=got,expected=expected,relative_error=rel,**meta))
out=dict(tests=results,seconds=time.perf_counter()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(Path(__file__).parent/'stream_validation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
