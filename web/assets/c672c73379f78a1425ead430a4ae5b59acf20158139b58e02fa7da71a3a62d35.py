import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from sampler import *
from instances import *
import time,json
from pathlib import Path
out=[]
t=time.perf_counter(); G,_=diffusion_gram(4)
lm,mask,ev,diag=calibrate_worm(G,10.,1000)
worm_run(G,10.,100,1,lm,mask)
for method in range(3): target_run(G,10.,10,1,method)
tempering_run(G,10.,10,1,np.linspace(0,1,8))
enumerate_target(G,10.)
print('compile_seconds',time.perf_counter()-t,flush=True)
for mode in ['local','irregular','cycle']:
 n=12; G,meta=diffusion_gram(n,314,mode)
 for beta in [100.,10000.]:
  p,logz,logs=enumerate_target(G,beta)
  idx=np.arange(1<<n); obs=np.array([int(i).bit_count()/n for i in idx])
  true=float(p@obs)
  print('instance',mode,beta,'topmass',sum(sorted(p)[-2:]),'mean',true,flush=True)
  t=time.perf_counter(); lm,mask,ev,diag=calibrate_worm(G,beta,60000,21)
  ct=time.perf_counter()-t
  t=time.perf_counter(); a,lm,mask,counts,ac,evp=worm_run(G,beta,200000,121,lm,mask)
  sec=time.perf_counter()-t
  def score(name,a,sec,evals,setup=0):
   hist=np.bincount(a,minlength=len(p))/max(1,len(a)); tv=.5*sum(abs(hist-p))
   r=dict(mode=mode,beta=beta,method=name,n_samples=len(a),seconds=sec,setup_seconds=setup,
          mean=float(np.mean(obs[a])) if len(a) else None,truth=true,tv=float(tv),det_evals=evals)
   out.append(r); print(r,flush=True)
  score('worm',a,sec,evp+ev,ct)
  for method in range(3):
   steps=100000 if method!=1 else 25000
   t=time.perf_counter(); a,b,ev2=target_run(G,beta,steps,31,method)
   score(['gibbs1','gibbs2','multiscale'][method],a,time.perf_counter()-t,ev2)
  t=time.perf_counter(); a,b,ev3,sw=tempering_run(G,beta,12500,41,np.linspace(0,1,8))
  score('tempering8',a,time.perf_counter()-t,ev3)
Path('results/pilot.json').write_text(json.dumps(out,indent=2))
