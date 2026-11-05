"""Bounded unbiased physical spin-correlation estimates from independent exact loops.
The algorithm is exact under ideal independent fair random bits. Implementation uses
Python's PRNG for reproducible numerical diagnostics, not certified randomness.
No mixing, ancestor-time, or path-length cutoff is introduced. Floating arithmetic
appears only in reporting the mean and confidence bound, not sampling decisions.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,json,math,random,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'square_aklt_boundary_operation_20261105'))
from perfect_loop_sampler import PerfectLoopSampler
from torus_loop_birth_sampler import TorusLoopBirthSampler
from open_trail_sampler import OpenTrailSampler,suppression

def estimate(width,height,root,attempts,target=(1,0),seed=20261105,alpha=.05,bernoulli=False):
 assert attempts>=1 and 0<alpha<1 and 0<=root[0]<width and 0<=root[1]<height
 if target is not None:
  assert target!=(0,0) and 0<=root[0]+target[0]<width and 0<=root[1]+target[1]<height
 setup=time.monotonic();paths=OpenTrailSampler(seed,target=target)
 loopsampler=PerfectLoopSampler(width,height,seed+104729,birth_factory=TorusLoopBirthSampler)
 coins=random.Random(seed+15485863);setup=time.monotonic()-setup
 C=paths.majorant;total=F(0);sumsq=F(0);valid=0;nonzero=0;work=Counter();pt=lt=0.
 start=time.monotonic()
 for k in range(attempts):
  t=time.monotonic();p=paths.propose_path(width,height,root);pt+=time.monotonic()-t
  if p is None:continue
  valid+=1;t=time.monotonic();loops,stats=loopsampler.sample();lt+=time.monotonic()-t;work.update(stats)
  s=suppression(p,loops)
  if bernoulli:s=F(int(coins.randrange(s.denominator)<s.numerator))
  total+=s;sumsq+=s*s;nonzero+=bool(s)
 sign=1 if target is None or sum(target)%2==0 else -1;offset=6 if target is None else 0
 mean=offset+sign*9*C*total/attempts
 variance=(81*C*C*(sumsq-total*total/attempts)/(attempts-1)) if attempts>1 else None
 halfwidth=9*float(C)*math.sqrt(math.log(2/alpha)/(2*attempts))
 return {'physical_state':'Open spin2 AKLT virtual-identity boundary mixture V I V† / Tr(V I V†)',
  'observable':'equal-time staggered correlation sum at root' if target is None else 'S_i dot S_j',
  'box':[width,height],'root':root,'target_displacement':target,'attempts':attempts,'majorant_exact':str(C),
  'majorant':float(C),'estimate_exact':str(mean),'estimate':float(mean),
  'range':[offset+min(0,sign*9*float(C)),offset+max(0,sign*9*float(C))],
  'confidence_probability':1-alpha,'hoeffding_halfwidth':halfwidth,
  'sample_variance':float(variance) if variance is not None else None,
  'empirical_standard_error_not_a_certificate':math.sqrt(float(variance)/attempts) if variance is not None else None,
  'path_valid_count':valid,'nonzero_count':nonzero,'independent_full_loop_samples':valid,
  'setup_seconds':setup,'path_proposal_seconds':pt,'perfect_loop_seconds':lt,'elapsed_seconds_excluding_setup':time.monotonic()-start,
  'mean_work_per_full_loop_sample':{k:v/valid for k,v in work.items()} if valid else {},
  'bernoulli_thinning':bernoulli,
  'confidence_scope':'Fixed attempt count selected before observations; Hoeffding for independent exact draws. Formula evaluated in binary64 for report. PRNG run is a diagnostic, not a proof of randomness.'}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--size',type=int,default=3);ap.add_argument('--attempts',type=int,default=1000)
 ap.add_argument('--dx',type=int,default=1);ap.add_argument('--dy',type=int,default=0);ap.add_argument('--staggered-sum',action='store_true')
 ap.add_argument('--seed',type=int,default=20261105);ap.add_argument('--bernoulli',action='store_true');ap.add_argument('--output')
 a=ap.parse_args();root=((a.size-1)//2,(a.size-1)//2)
 r=estimate(a.size,a.size,root,a.attempts,None if a.staggered_sum else(a.dx,a.dy),a.seed,bernoulli=a.bernoulli)
 out=Path(a.output) if a.output else Path(__file__).parent/f'correlation_{a.size}x{a.size}_{a.attempts}.json'
 out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)
