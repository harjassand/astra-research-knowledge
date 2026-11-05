"""Physical finite-box AKLT spin correlation using only path-local loop queries.
Exactness depends on the independently audited conditional-Poisson invariant
of local_perfect_sampler.py. No whole-box loop configuration is materialized.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,math,json,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'square_aklt_observable_join_20261105'))
from open_trail_sampler import OpenTrailSampler,suppression
from local_perfect_sampler import LocalPerfectLoopSampler
from exact_confidence import confidence_radius,rational_probability

def estimate(size,attempts,target=(1,0),seed=20261105,alpha=.05,progress_every=0):
 assert (size is None or size>=2) and attempts>=1 and 0<alpha<1 and target!=(0,0)
 root=(0,0) if size is None else ((size-1)//2,(size-1)//2)
 if size is not None:assert all(0<=root[k]+target[k]<size for k in range(2))
 setup=time.monotonic();paths=OpenTrailSampler(seed,target=target)
 local=LocalPerfectLoopSampler([root],box=None if size is None else (size,size),seed=seed+104729)
 setup=time.monotonic()-setup;C=paths.majorant
 total=F(0);sumsq=F(0);valid=nonzero=0;work=Counter();pt=lt=0.;maxclan=maxlen=0
 t0=time.monotonic()
 for attempt in range(attempts):
  if progress_every and attempt and attempt%progress_every==0:
   print(json.dumps({'completed_attempts':attempt,'fixed_total_attempts':attempts,'local_queries':valid,'elapsed_seconds':time.monotonic()-t0}),flush=True)
  t=time.monotonic();p=paths.propose_path(size,size,root);pt+=time.monotonic()-t
  if p is None:continue
  valid+=1;t=time.monotonic();loops,stats=local.sample(query_vertices=set(p));lt+=time.monotonic()-t
  work.update(stats);maxclan=max(maxclan,stats.get('clan_size',0));maxlen=max(maxlen,stats.get('maximum_loop_length',0))
  z=suppression(p,loops);total+=z;sumsq+=z*z;nonzero+=bool(z)
 sign=-1 if sum(target)%2 else 1
 radius=confidence_radius(9*C,attempts,alpha)
 mean=sign*9*C*total/attempts;variance=81*C*C*(sumsq-total*total/attempts)/(attempts-1) if attempts>1 else None
 return {'physical_state':'Thermodynamic pair-correlation limit of expanding open spin2 AKLT virtual-identity mixtures' if size is None else 'Open spin2 AKLT virtual-identity boundary mixture','observable':'S_i dot S_j',
  'box':None if size is None else [size,size],'root':root,'target_displacement':target,'attempts':attempts,'seed':seed,
  'majorant_exact':str(C),'estimate_exact':str(mean),'estimate':float(mean),
  'confidence_probability':1-alpha,'hoeffding_halfwidth':float(radius),
  'hoeffding_radius_exact_upper':str(radius),'confidence_interval_exact':[str(mean-radius),str(mean+radius)],
  'failure_probability_exact':str(rational_probability(alpha)),
  'sample_variance':float(variance) if variance is not None else None,
  'empirical_standard_error_not_a_certificate':math.sqrt(float(variance)/attempts) if variance is not None else None,
  'valid_paths_and_independent_local_queries':valid,'nonzero_count':nonzero,
  'setup_seconds':setup,'path_proposal_seconds':pt,'local_perfect_loop_seconds':lt,'elapsed_seconds_excluding_setup':time.monotonic()-t0,
  'mean_work_per_local_query':{k:v/valid for k,v in work.items()} if valid else {},
  'maximum_observed_clan':maxclan,'maximum_observed_loop_length':maxlen,
  'scope':'Specified finite-box or thermodynamic-limit pair correlation. Exact-law claim conditional on local engine audit; mathematical confidence assumes ideal fair bits. PRNG diagnostic; confidence endpoints are outward rational bounds, not floating decisions. No Kubo response or quantum preparation claim.'}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--size',type=int,default=3);ap.add_argument('--attempts',type=int,default=10000);ap.add_argument('--seed',type=int,default=20261105);ap.add_argument('--infinite',action='store_true');ap.add_argument('--progress-every',type=int,default=0);ap.add_argument('--output')
 a=ap.parse_args();r=estimate(None if a.infinite else a.size,a.attempts,seed=a.seed,progress_every=a.progress_every)
 out=Path(a.output) if a.output else Path(__file__).with_name(f'physical_local_{a.size}x{a.size}_{a.attempts}.json')
 out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)
