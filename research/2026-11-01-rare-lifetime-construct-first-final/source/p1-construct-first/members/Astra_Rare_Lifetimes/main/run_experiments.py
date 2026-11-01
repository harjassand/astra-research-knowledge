"""Fully charged synthetic acquisition and short-excursion computation.
No physical measurements are claimed. See MAIN_PROOF.txt for the contract.
"""
from pathlib import Path
import json, math, subprocess, time
import numpy as np
from scipy.linalg import solve, eigvalsh
ROOT=Path(__file__).resolve().parent

def moves_for(n,fast=False):
 ans=[]
 for i in range(n):
  rate=.75+((17*i)%13)/20
  if fast and i==0:rate=64.
  ans.append(dict(type=0,i=i,j=i,inverse=0,rate=rate))
 for i in range(n-1):
  ans.append(dict(type=1,i=i,j=i+1,inverse=i%2,rate=.55+((11*i)%17)/20))
 return ans

def apply(x,a):
 if a['type']==0:return x^(1<<a['i'])
 i,j=a['i'],a['j'];old=((x>>i)&1)+2*((x>>j)&1)
 z=([3,0,2,1] if a['inverse'] else [1,3,2,0])[old]
 return (x&~((1<<i)|(1<<j)))|((z&1)<<i)|((z>>1)<<j)

def generator(n,moves):
 d=1<<n;Q=np.zeros((d,d))
 for x in range(d):
  for a in moves:
   y=apply(x,a);Q[x,y]+=a['rate'];Q[x,x]-=a['rate']
 return Q

def exact_case(n,mask,pattern,s,fast=False):
 ms=moves_for(n,fast);Q=generator(n,ms);d=len(Q)
 A=np.array([(x&mask)==pattern for x in range(d)]);B=~A
 p=float(A.mean());b=1-p;L=-Q
 t=solve(L[np.ix_(B,B)],np.ones(B.sum()));M=float(t.mean())
 u=np.ones(d);u[B]=solve(L[np.ix_(B,B)]+s*np.eye(B.sum()),Q[np.ix_(B,A)].sum(1))
 mu=float((Q[np.ix_(A,B)]@(1-u[B])).mean());r=s+mu;R=1/(p*r)-1/s
 gap=float(eigvalsh((L+L.T)/2)[1]);fac=1+s/gap
 flux=float(Q[np.ix_(A,B)].sum())/d;lo=R/(b*fac);hi=R*fac/b
 return dict(n=n,states=d,target_size=int(A.sum()),p=p,s=s,symmetric_gap=gap,
   mean_exact=M,screened_mean=R/b,interval=[lo,hi],contains=bool(lo<=M<=hi),
   flux_shortcut=b/flux,flux_shortcut_ratio=(b/flux)/M,mu=mu,
   stationarity_residual=float(abs(Q.sum(0)).max()),
   nonreversibility_norm=float(np.linalg.norm(Q-Q.T)),
   flux_identity_residual=abs(p*r-s*u.mean()))

def main():
 t0=time.perf_counter();cs=time.perf_counter()
 subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'short_excursions.cpp'),'-o',str(ROOT/'short_excursions')],check=True)
 compile_seconds=time.perf_counter()-cs
 exact=[]
 for n in [3,5,8]:
  for m in [1,n//2,n-1]:
   for s in [.03,.3]:exact.append(exact_case(n,(1<<m)-1,(1<<m)-1,s))
 exact.append(exact_case(6,(1<<3)-1,0,.03,True))
 assert all(x['contains'] for x in exact)
 (ROOT/'small_dense_results.json').write_text(json.dumps(exact,indent=2))
 n=64;ms=moves_for(n);rng=np.random.default_rng(20261101)
 calibration_time=200000;eps=.02;known_floor=.5
 counts=rng.poisson(np.array([a['rate'] for a in ms])*calibration_time)
 for a,c in zip(ms,counts):a['count']=int(c);a['fit_rate']=int(c)/calibration_time
 eta_actual=max(abs(a['fit_rate']/a['rate']-1) for a in ms)
 failure_calibration=2*len(ms)*math.exp(-eps*eps*known_floor*calibration_time/3)
 K=2/math.sqrt(3);model_factor=math.exp(2*math.asinh(eps*K/(2*math.sqrt(1-eps))))
 clock_weight=min(a['count'] for a in ms if a['type']==0)
 s=clock_weight/(10*calibration_time);gap=2*clock_weight/calibration_time
 specs=[('contiguous_48',(1<<48)-1,0),('distributed_48',sum(1<<i for i in range(64) if i%4!=3),None),('alternating_48',(1<<48)-1,sum(1<<i for i in range(48) if i%2))]
 targets=[]
 for ix,(name,mask,pattern) in enumerate(specs):
  if pattern is None:pattern=int(rng.integers(0,2**64,dtype=np.uint64))&mask
  m=mask.bit_count();trials=30000;model_file=ROOT/(name+'_model.txt')
  rows=[f'{n} {len(ms)} {mask} {pattern} {clock_weight} {99173+ix} {trials}']
  rows += [f"{a['type']} {a['i']} {a['j']} {a['inverse']} {10*a['count']}" for a in ms]
  model_file.write_text('\n'.join(rows)+'\n')
  begin=time.perf_counter()
  raw=subprocess.run([str(ROOT/'short_excursions'),str(model_file)],check=True,text=True,capture_output=True)
  simulation_seconds=time.perf_counter()-begin;empirical=json.loads(raw.stdout)
  p=2.**(-m);b=1-p;R=empirical['relevant_weight']/(10*calibration_time)
  theta=empirical['theta_hat'];w=.012;tlo=max(0.,theta-w);thi=min(1.,theta+w)
  rlo=s+R*tlo;rhi=s+R*thi;klo=1/rhi-p/s;khi=1/rlo-p/s
  fitlo=klo/(p*b*(1+s/gap));fithi=khi*(1+s/gap)/(p*b)
  interval=[fitlo/model_factor,fithi*model_factor]
  empirical.update(name=name,n=n,states=str(2**n),target_constraints=m,target_mass=p,
   mask=str(mask),pattern=str(pattern),kill_rate=s,certified_symmetric_gap=gap,relevant_rate=R,
   theta_interval=[tlo,thi],hoeffding_radius=w,mc_failure=2*math.exp(-2*trials*w*w),
   fitted_mean_interval=[fitlo,fithi],true_mean_interval=interval,
   screened_point=(1/(s+R*theta)-p/s)/(p*b),interval_ratio=interval[1]/interval[0],
   model_factor=model_factor,screening_factor=1+s/gap,simulation_seconds=simulation_seconds,
   expected_excursion_duration_upper=1/s,mean_marked_events_per_attempt=empirical['events']/trials,
   rarity_free_theta_lower=s*gap*b/(R*(s+gap*p)),
   complete_mc_event_budget_upper=trials*(empirical['total_weight']+clock_weight)/clock_weight)
  targets.append(empirical)
 payload=dict(kind='synthetic local marked-clock source; no physical measurements',n=n,primitives=len(ms),
  calibration_duration=calibration_time,calibration_events=int(counts.sum()),relative_calibration_bound=eps,
  actual_synthetic_max_relative_error=eta_actual,calibration_failure_upper=failure_calibration,
  model_factor=model_factor,total_statistical_failure_upper=failure_calibration+sum(x['mc_failure'] for x in targets),
  compilation_seconds=compile_seconds,total_seconds=time.perf_counter()-t0,moves=ms,targets=targets)
 (ROOT/'large_results.json').write_text(json.dumps(payload,indent=2))
 print(json.dumps({k:v for k,v in payload.items() if k!='moves'},indent=2))
if __name__=='__main__':main()
