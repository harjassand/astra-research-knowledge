"""Floating lower-field proposal followed by exact rational source certificate.

Optimization success is not acceptance. Every final trial is rounded, its
physical quadratic energy recomputed exactly, and the full source-box minimum
evaluated by the proved prefix rule. Needs NumPy/SciPy for proposals only.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,time,platform
import numpy as np
import scipy
from scipy.optimize import minimize
from source_normalization_cut import inverse,mv,dot,maximize_source,minimize_trial,serial

def run(feature,R):
 n=4;N=1<<n;q=F(1,26);eps=F(1,10000)
 mass=[q**g.bit_count()*(1-q)**(n-g.bit_count()) for g in range(N)]
 indicator={'all_open':lambda g:g==N-1,'first_open':lambda g:g&1,'all_closed':lambda g:g==0}[feature]
 wl=[F(1)]*N;wu=[F(1)+(R-1)*int(bool(indicator(g))) for g in range(N)]
 def form(w):
  a=[[F(0) for _ in range(N)] for _ in range(N)]
  for g in range(N):
   a[g][g]+=mass[g]*w[g]*q*(1 if (g>>(n-1))&1 else eps)
   for i in range(n):
    if (g>>i)&1:continue
    h=g|(1<<i);c=mass[g]*q*(1 if i==0 or (g>>(i-1))&1 else eps)*min(w[g],w[h])
    a[g][g]+=c;a[h][h]+=c;a[g][h]-=c;a[h][g]-=c
  return a
 lo=mass;hi=[x*y for x,y in zip(mass,wu)];ap=form(wu);gp=inverse(ap);gm=inverse(form(wl))
 ids=[i for i in range(N) if hi[i]>lo[i]];dd=[hi[i]-lo[i] for i in ids]
 gn=np.array(gp,dtype=float);ln=np.array(lo,dtype=float);dn=np.array(dd,dtype=float)
 scale=float(dot(lo,mv(gp,lo))/sum(lo))
 def obj(z):
  s=ln.copy();s[ids]+=z*dn;v=gn@s;Z=s.sum();Q=s@v
  return Q/Z/scale, dn*(2*v[ids]*Z-Q)/(Z*Z)/scale
 start=time.monotonic();best=None
 for z0 in [np.zeros(len(ids)),np.ones(len(ids)),np.full(len(ids),.5)]:
  candidate=minimize(lambda z:obj(z)[0],z0,jac=lambda z:obj(z)[1],bounds=[(0.,1.)]*len(ids),method='SLSQP',options=dict(ftol=1e-12,maxiter=300))
  if best is None or candidate.fun<best.fun:best=candidate
 s=ln.copy();s[ids]+=best.x*dn;vf=gn@s
 v=[F(round(float(z)*(1<<40)),1<<40) for z in vf]
 energy=dot(v,mv(ap,v));lower,profile=minimize_trial(lo,hi,v,energy)
 fixedv=mv(gp,lo);fixed,_=minimize_trial(lo,hi,fixedv,dot(lo,fixedv))
 upper,_,history=maximize_source(gm,lo,hi)
 assert lower<=upper
 # If numerical acquisition loses to the original fixed field, retain the
 # original certificate rather than reporting an inferior run as progress.
 chosen=max(lower,fixed)
 return dict(feature=feature,R=R,retained_states=N,optimizer_success=bool(best.success),optimizer_message=str(best.message),
  floating_minimum_proposal=float(best.fun*scale),dyadic_field=v,exact_energy=energy,optimized_trial_lower=lower,
  original_fixed_trial_lower=fixed,accepted_lower=chosen,cut_upper=upper,accepted_ratio=upper/chosen,
  cut_calls=len(history),seconds=time.monotonic()-start,scope='Exact valid bound;no claimed exact attainment of convex minimum or physical completion extrema.')

def main(out):
 rows=[run(f,R) for f in ['all_open','first_open','all_closed'] for R in [3,100]]
 result=dict(status='PASS',python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,rows=rows,
  acceptance='Exact field energy and exact affine-fractional source-box minimum;floating optimality not used.')
 out.mkdir(parents=True,exist_ok=True);(out/'OPTIMIZED_LOWER_CERTIFICATES.json').write_text(json.dumps(serial(result),indent=2)+'\n')
 print(json.dumps(serial([dict(feature=x['feature'],R=x['R'],lower=x['accepted_lower'],upper=x['cut_upper'],ratio=x['accepted_ratio'],optimizer_success=x['optimizer_success']) for x in rows]),indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True,type=Path);main(p.parse_args().output_dir)
