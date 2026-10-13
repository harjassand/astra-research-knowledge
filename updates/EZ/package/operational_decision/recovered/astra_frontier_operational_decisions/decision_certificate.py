"""Exact decision/exclusion and common-access information bounds.
Uses rational many-body response enclosures, not sampled payoffs.
"""
from fractions import Fraction as F
from pathlib import Path
import math,json,time
from finite_certificates import PARS,ceil_sqrt,zero,mono_radius,fstr

def down(x,bits=48):
 d=1<<bits; return F(x.numerator*d//x.denominator,d)

def up(x,bits=48):
 return -down(-x,bits)

def atan_bounds(x:F,n=100):
 s=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(n)),F(0))
 t=(-1)**n*x**(2*n+1)/F(2*n+1)
 return min(s,s+t),max(s,s+t)

def pi_bounds():
 a,b=atan_bounds(F(1,5),32);c,d=atan_bounds(F(1,239),10)
 return down(16*a-4*d,60),up(16*b-4*c,60)

def exp_bounds(x:F,n=20):
 if x<0:
  a,b=exp_bounds(-x,n);return 1/b,1/a
 s=sum((x**k/F(math.factorial(k)) for k in range(n+1)),F(0))
 rem=x**(n+1)/F(math.factorial(n+1))/(1-x/F(n+2))
 return s,s+rem

def sin_positive_bounds(x:F,n=32):
 # Alternating series; arguments here are between zero and 1.5.
 s=sum(((-1)**k*x**(2*k+1)/F(math.factorial(2*k+1)) for k in range(n)),F(0))
 nxt=(-1)**n*x**(2*n+1)/F(math.factorial(2*n+1))
 return min(s,s+nxt),max(s,s+nxt)

def sqrt_bounds(x):
 u=ceil_sqrt(x,52);return u-F(1,2**52),u

def polynomial(rec):return {tuple(map(int,k.split(','))):F(v) for k,v in rec['coefficient_polynomial'].items()}

def combine(items,ideal=True):
 p={};err=F(0)
 for fac,rec in items:
  err+=abs(fac)*F(rec['error'])
  for a,x in polynomial(rec).items():
   if ideal and a[4]+a[5]:continue
   p[a]=p.get(a,F(0))+fac*x
 mid=p.get(zero,F(0));rad=sum(abs(x)*mono_radius(a) for a,x in p.items() if a!=zero)
 return mid-rad-err,mid+rad+err

def produce(folder='results'):
 st=time.perf_counter();folder=Path(folder)
 data={(rec['kind'],rec['kappa']):rec for rec in json.loads((folder/'all_cases.json').read_text())}
 # Establish same nonmatching-phase drain setting is best throughout the four-parameter box.
 best=data['good',4]; checks=[]
 for key,rec in data.items():
  if key==('good',4):continue
  lo,hi=combine([(F(1),best),(F(-1),rec)])
  assert lo>0,(key,float(lo))
  checks.append({'competitor':str(key),'gain_lower':fstr(lo),'gain_upper':fstr(hi)})
 Glo,Ghi=combine([(F(1),best),(F(-1),data['bad',4])]);assert Glo>0
 # Best no-observation randomized control: uniform phases and drain 4.
 blind_checks=[]
 for k in [2,8]:
  lo,hi=combine([(F(2),best),(F(1),data['bad',4]),(F(-2),data['good',k]),(F(-1),data['bad',k])])
  assert lo>0
  blind_checks.append({'kappa':k,'sum_payoff_domination_lower':fstr(lo)})
 # Sensor is derived from an actual half-swap under physical dephasing.
 pl,pu=pi_bounds();Tlo,Thi=pl/4,pu/4;d=F(1,100)
 ol,ou=sqrt_bounds(F(4)-d*d/4)
 elo,ehi=exp_bounds(-d*Thi/2); _,ehi=exp_bounds(-d*Tlo/2)
 gaphi=pu*(2-ol)/4
 slo=down(2/ou*elo*(1-gaphi*gaphi/2));shi=up(2/ol*ehi)
 pbad=up((1-slo)/3)
 probe_tv=F(1,2000)
 bad_total=pbad+probe_tv
 act=max(F(data[k,4]['actuation_allowance']) for k in ['bad','good'])
 expected=bad_total*Ghi+act
 # Helstrom bound for ANY controlled acquisition protocol whose total unknown-link time <= pi/4.
 root3lo,root3hi=sqrt_bounds(F(3))
 angle_hi=root3hi*Thi
 _,dist_hi=sin_positive_bounds(angle_hi)
 identification_failure_lower=down((1-up(dist_hi,60))/2)
 assert bad_total < F(1,500) # >99.8% near-optimal control
 assert identification_failure_lower > F(1,100) # even 99%-confidence phase learning impossible
 # Payoff operators: domination across drain settings for arbitrary one-copy POVMs on this probe.
 # Probe population component z=e^-dT/2(cos Omega T+d/(2Omega)sin Omega T).
 # cos(Omega T)<=gap, sin<=1.
 zupper=up(ehi*(gaphi+d/(2*ol)))
 povm_dom=[]
 for k in [2,8]:
  al,ah=combine([(F(2,6),best),(F(1,6),data['bad',4]),(F(-2,6),data['good',k]),(F(-1,6),data['bad',k])])
  bl,bh=combine([(F(1,6),data['bad',4]),(F(-1,6),best),(F(-1,6),data['bad',k]),(F(1,6),data['good',k])])
  margin=al*(1-zupper)-max(abs(bl),abs(bh))*shi
  assert margin>0
  povm_dom.append({'kappa':k,'PSD_lower_margin':fstr(margin)})
 out={'model':'4-site hard-core diamond, finite-density stationary output',
      'uncertainty_center':[4,3,1,2], 'interaction_radius':'1/25',
      'phase_hypotheses':['0','2*pi/3','4*pi/3'],
      'actions':{'phase_commands':['pi','pi/3','-pi/3'],'drain_rates':[2,4,8]},
      'pump_rate':'2/5','physical_dephasing':'1/100',
      'probe_exposure_pi_fraction':'1/4','probe_transverse_lower':fstr(slo),'probe_transverse_upper':fstr(shi),
      'ideal_bad_probability_upper':fstr(pbad),'allowed_total_variation_error':fstr(probe_tv),
      'bad_probability_upper':fstr(bad_total), 'good_event_regret_upper':fstr(act),
      'expected_regret_upper':fstr(expected), 'ideal_good_minus_bad_lower':fstr(Glo), 'ideal_good_minus_bad_upper':fstr(Ghi),
      'any_no_observation_worst_expected_regret_lower':fstr(Glo/3),
      'no_observation_to_policy_certified_ratio':fstr(Glo/3/expected),
      'all_adaptive_identification_worst_failure_lower':fstr(identification_failure_lower),
      'phase_actuation_radius':fstr(PARS[4]),'drain_actuation_radius':fstr(PARS[5]),
      'best_action_checks':checks,'blind_domination':blind_checks,'POVM_payoff_domination':povm_dom,
      'proof_pi_interval':[fstr(pl),fstr(pu)],'seconds':time.perf_counter()-st,
      'evidence':'analytical probability and exact rational model certificates; no physical or random assay claimed'}
 (folder/'decision_certificate.json').write_text(json.dumps(out,indent=2))
 for k in ['probe_transverse_lower','ideal_bad_probability_upper','bad_probability_upper','good_event_regret_upper','expected_regret_upper','any_no_observation_worst_expected_regret_lower','no_observation_to_policy_certified_ratio','all_adaptive_identification_worst_failure_lower']:
  print(k,float(F(out[k])))
 return out
if __name__=='__main__':produce()
