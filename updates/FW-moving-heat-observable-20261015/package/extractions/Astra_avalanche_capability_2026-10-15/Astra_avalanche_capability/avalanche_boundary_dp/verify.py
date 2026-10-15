from pathlib import Path
import sys,time,json,numpy as np
from scipy.linalg import solve
from boundary_dp import *
sys.path.insert(0,str(Path(__file__).resolve().parent.parent / 'failure_source_benchmark'))
from verify_avalanche_clock import independent_Q
rng=np.random.default_rng(42);results={};maxerr=0;cases=0
for n in range(1,13):
 for j in range(8):
  s=rng.random(n);F=rng.choice([0.,.05,.125,.2,.4,1.])*n;p=rng.random(n)
  a=pmf(s,F,p);b=exhaustive(s,F,p);maxerr=max(maxerr,float(np.max(abs(a-b))));cases+=1
  assert np.max(abs(a-b))<1e-12
for s,F in [([.5,.5],1.),([.25,.5],.5),([0.,0.,1.],0.),([.25,.5,1.,2.],1.),([1.,1.,1.,1.],2.)]:
 for p in [np.full(len(s),.5),np.zeros(len(s)),np.ones(len(s))]:
  a=pmf(s,F,p);b=exhaustive(s,F,p);maxerr=max(maxerr,float(np.max(abs(a-b))));cases+=1
  assert np.max(abs(a-b))<1e-12
results['exhaustive']={'cases':cases,'max_absolute_error':maxerr,'n_max':12}
s=np.sort(np.random.RandomState(0).rand(5));F=5*.125;T=.05
Q,states,idx=independent_Q(s,F/len(s),T);keep=[i for i,st in enumerate(states) if st];means=solve(-Q[np.ix_(keep,keep)],np.ones(len(keep)))
a=time.perf_counter();num=mean_quad(s,F,T);num['seconds']=time.perf_counter()-a
num['phase_type_mean']=float(means[keep.index(0)]);num['absolute_difference']=abs(num['mean']-num['phase_type_mean']);results['author_fixture']=num
scaling=[]
for n in [5,25,100,400]:
 s=np.sort(np.random.RandomState(0).rand(n));F=n*.125;T=.05
 a=time.perf_counter();b=mean_geometric_bracket(s,F,T,relative_gap=.01);b['seconds']=time.perf_counter()-a;b['n']=n;b['F']=F;b['T']=T
 scaling.append(b);print(n,b,flush=True)
results['geometric_brackets']=scaling
open(str(Path(__file__).resolve().parent.parent / 'avalanche_boundary_dp/results.json'),'w').write(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
