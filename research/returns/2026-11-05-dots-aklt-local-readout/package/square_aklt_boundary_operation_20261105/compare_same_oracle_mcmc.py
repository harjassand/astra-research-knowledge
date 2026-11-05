"""Same-access approximate MCMC comparator, not a convergence certificate.
Uniformization preserves the exact target law; finite burn-in is heuristic.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import random,time,json,argparse,math
import numpy as np
from torus_loop_birth_sampler import TorusLoopBirthSampler
from perfect_loop_sampler import geometry

class ForwardChain:
 def __init__(self,side,seed,packed=False):
  self.side=side;self.rng=random.Random(seed);self.birth=TorusLoopBirthSampler(seed+1)
  self.lam=self.birth.rate_per_vertex*side*side;self.Kmax=(2*side*(side-1))//4
  self.active=[];self.objects={};self.index=defaultdict(set);self.nextid=0
  self.sweep_steps=math.ceil(self.lam+self.Kmax)
  if packed:
   for x in range(0,side-1,2):
    for y in range(0,side-1,2):self.add(((x,y),(x+1,y),(x+1,y+1),(x,y+1)))
 def add(self,p):
  i=self.nextid;self.nextid+=1;g=geometry(p);self.objects[i]=g;self.active.append(i)
  for v in g[0]:self.index[v].add(i)
 def remove(self,j):
  i=self.active[j];self.active[j]=self.active[-1];self.active.pop();g=self.objects.pop(i)
  for v in g[0]:
   self.index[v].remove(i)
   if not self.index[v]:del self.index[v]
 def step(self):
  r=self.rng
  if r.randrange(self.lam.numerator+self.Kmax*self.lam.denominator)>=self.lam.numerator:
   j=r.randrange(self.Kmax)
   if j<len(self.active):self.remove(j)
   return
  p=self.birth.propose(self.side,self.side)
  if p is None:return
  g=geometry(p);others=set()
  for v in g[0]:others.update(self.index.get(v,()))
  k=0
  for i in others:
   h=self.objects[i]
   if g[1]&h[1]:return
   k+=len(g[0]&h[0])
  if r.randrange(5**k)<3**k:self.add(p)
 def sweep(self):
  for _ in range(self.sweep_steps):self.step()
  return len(self.active)

def ess_estimate(x):
 x=np.asarray(x,dtype=float);x-=x.mean();n=len(x);var=float(x@x/n)
 if var==0:return n,1.,[]
 cov=np.correlate(x,x,'full')[n-1:]/np.arange(n,0,-1);acf=cov/cov[0]
 # Initial-positive paired-autocorrelation truncation, empirical only.
 total=0.;lags=[]
 for k in range(1,min(n-1,n//2),2):
  pair=float(acf[k]+acf[k+1])
  if pair<=0:break
  total+=pair;lags.extend([float(acf[k]),float(acf[k+1])])
 tau=max(1.,1+2*total)
 return n/tau,tau,lags

def run(side,burn,samples):
 records=[]
 for packed in [False,True]:
  c=ForwardChain(side,20261105+side+int(packed),packed);start=time.monotonic();warm=[]
  for _ in range(burn):warm.append(c.sweep())
  burntime=time.monotonic()-start;x=[];t=time.monotonic()
  for k in range(samples):
   x.append(c.sweep())
   if (k+1)%max(1,samples//5)==0:print(side,'packed',packed,'sweep',k+1,'elapsed',time.monotonic()-t,flush=True)
  seconds=time.monotonic()-t;ess,tau,acf=ess_estimate(x)
  records.append({'initial':'packed plaquettes' if packed else 'empty','burn_sweeps':burn,'sample_sweeps':samples,'steps_per_sweep':c.sweep_steps,
   'burn_seconds':burntime,'sample_seconds':seconds,'mean_loop_count':float(np.mean(x)),'stdev_loop_count':float(np.std(x,ddof=1)),
   'estimated_iact_loop_count':tau,'estimated_ess_loop_count':ess,'seconds_per_estimated_ess':seconds/ess,
   'burn_history':warm,'loop_count_series':x,'positive_acf_window':acf})
 return {'side':side,'sites':side*side,'records':records,'scope':'Same rational torus birth oracle, same target law. Finite burn-in and autocorrelation ESS are empirical, not exact-sampling or TV-error guarantees. Only loop count benchmarked.'}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--side',type=int,default=32);a.add_argument('--burn',type=int,default=30);a.add_argument('--samples',type=int,default=500);z=a.parse_args();r=run(z.side,z.burn,z.samples)
 (Path(__file__).parent/f'mcmc_comparison_L{z.side}.json').write_text(json.dumps(r,indent=2)+'\n')
 for x in r['records']:print({k:v for k,v in x.items() if k not in ['burn_history','loop_count_series','positive_acf_window']})
