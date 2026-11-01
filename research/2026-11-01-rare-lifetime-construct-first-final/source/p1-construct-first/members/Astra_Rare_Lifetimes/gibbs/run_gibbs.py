"""Acquire local factors; compute rare cylinder mass and initialization;
then execute the exact-rational short-excursion receiver on an 80-bit model.

The unknown source is synthetic. Clamped native-rate access is a structural
contract, not justified by Gibbs equilibrium alone. No true collective target
mass or true stationary sampler is passed to the receiver.
"""
from fractions import Fraction as F
from pathlib import Path
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
import json,subprocess,time,math,random
import numpy as np

P=Path(__file__).resolve().parent
D=100000

def out(x,up=False):
 with localcontext() as ctx:
  ctx.prec=18;ctx.rounding=ROUND_CEILING if up else ROUND_FLOOR
  return str(Decimal(x.numerator)/Decimal(x.denominator))
def ser(x):return dict(numerator=str(x.numerator),denominator=str(x.denominator))
def exp_bounds(x,n=100):
 assert 0<=x<n+2
 term=F(1);total=term
 for k in range(1,n+1):term*=x/k;total+=term
 return total,total+(term*x/(n+1))/(1-x/(n+2))
def quant(x,lo,hi):
 x=min(hi,max(lo,x));k=(x.numerator*D*2+x.denominator)//(2*x.denominator)
 return F(k,D)

def messages(a,b,fixed):
 """suffix[i][previous_bit], including the edge from i-1 into i."""
 n=len(a);suf=[[F(1),F(1)] for _ in range(n+1)]
 prob=[[F(0),F(0)] for _ in range(n)]
 for i in range(n-1,-1,-1):
  for prev in (0,1):
   terms=[]
   for x in (0,1):
    ok=i not in fixed or fixed[i]==x
    weight=(a[i] if x else 1)*(b[i-1] if i>0 and prev and x else 1)
    terms.append(weight*suf[i+1][x] if ok else F(0))
   suf[i][prev]=sum(terms)
   prob[i][prev]=terms[1]/suf[i][prev] if suf[i][prev] else F(0)
 return suf[0][0],prob

def fixture_check():
 """Meaningful local flow and exact conditional-mass verification on 4 bits."""
 n=4;a=[F(94+3*i,100) for i in range(n)];b=[F(95+2*i,100) for i in range(n-1)]
 w=lambda x: math.prod(a[i] if x>>i&1 else F(1) for i in range(n))*math.prod(b[i] if (x>>i&3)==3 else F(1) for i in range(n-1))
 Z,pr=messages(a,b,{0:1,2:0});enum=sum(w(x) for x in range(2**n) if x&1 and not x&4)
 assert Z==enum
 # Exact path-law reconstruction from the conditional tables.
 for x in range(2**n):
  if not(x&1) or (x&4):continue
  prob=F(1)
  for i in range(n):
   q=pr[i][(x>>(i-1))&1] if i else pr[i][0]
   prob*=q if x>>i&1 else 1-q
  assert prob==w(x)/Z
 # Actual nonreversible Q, exact weighted stationarity.
 Q=[[F(0) for _ in range(2**n)] for _ in range(2**n)]
 for x in range(2**n):
  for i in range(n):
   r=a[i]*(b[i-1] if i>0 and (x>>(i-1))&1 else 1)*(b[i] if i+1<n and (x>>(i+1))&1 else 1)
   rate=1/(1+r) if x>>i&1 else r/(1+r)
   Q[x][x^(1<<i)]+=rate;Q[x][x]-=rate
  for i in range(n-1):
   old=(x>>i)&3;new=([3,0,2,1] if i&1 else [1,3,2,0])[old]
   y=(x&~(3<<i))|(new<<i)
   v=(a[i] if x>>i&1 else 1)*(a[i+1] if x>>(i+1)&1 else 1)
   v*=b[i] if old==3 else 1
   if i>0 and (x>>(i-1))&3==3:v*=b[i-1]
   if i+2<n and (x>>(i+1))&3==3:v*=b[i+1]
   rate=F(7,10)/v;Q[x][y]+=rate;Q[x][x]-=rate
 for y in range(2**n):assert sum(w(x)*Q[x][y] for x in range(2**n))==0
 return dict(states=2**n,exact_conditional_probability_checks=4,exact_stationarity_checks=2**n,all_pass=True)

def main():
 start=time.perf_counter();n=80;T=16_000_000_000;eta=F(1,10000);trials=40000
 rng=np.random.default_rng(20261102)
 a=[F(94+(7*i)%13,100) for i in range(n)]
 b=[F(94+(11*i)%13,100) for i in range(n-1)]
 alpha=[F(55+(7*i)%26,100) for i in range(n-1)]
 countrows=[];ahat=[];bhat=[];alhat=[]
 def observe(rate,label):
  k=int(rng.poisson(float(rate)*T));assert k>0
  countrows.append(dict(label=label,source_rate=ser(rate),count=k))
  return F(k,T)
 for i in range(n):
  r=a[i];rp=observe(r/(1+r),f'heatbath_{i}_00_current0');rm=observe(1/(1+r),f'heatbath_{i}_00_current1')
  r00=rp/rm;ahat.append(quant(r00,F(9,10),F(11,10)))
  if i+1<n:
   r=a[i]*b[i];rp=observe(r/(1+r),f'heatbath_{i}_01_current0');rm=observe(1/(1+r),f'heatbath_{i}_01_current1')
   bhat.append(quant((rp/rm)/r00,F(9,10),F(11,10)))
 for i,x in enumerate(alpha):alhat.append(quant(observe(x,f'cycle_{i}_00'),F(1,2),F(1)))
 assert len(countrows)==5*n-3
 # Rational conservative perturbation qualification, including quantization.
 t=eta/(1-eta);roundlog=F(1,50000)
 u=(6*n-4)*t+(2*n-1)*roundlog;v=u+t+roundlog
 exponent=3*u+F(7,6)*v;model_factor=F(5,4)
 assert exp_bounds(exponent)[1]<model_factor
 alpha_cal=F(2*len(countrows))/exp_bounds(F(1,3)*T*eta*eta/3)[0]
 Z,_=messages(ahat,bhat,{})
 compile_start=time.perf_counter()
 subprocess.run(['g++','-O3','-std=c++17',str(P/'gibbs_excursions.cpp'),'-o',str(P/'gibbs_excursions')],check=True)
 compile_seconds=time.perf_counter()-compile_start
 rows=[];joint=alpha_cal;radius=F(1,100);screen=F(21,20);ptrueZ,_=messages(a,b,{})
 fixtures=[('contiguous_64',{i:0 for i in range(64)}),('alternating_64',{i:i%2 for i in range(64)})]
 for ix,(name,fixed) in enumerate(fixtures):
  ZA,probs=messages(ahat,bhat,fixed);p=ZA/Z
  trueZA,_=messages(a,b,fixed);ptrue=trueZA/ptrueZ
  mask=sum(1<<i for i in fixed);pattern=sum(x<<i for i,x in fixed.items())
  lines=[f'{n} {trials} {86241+ix} {D} {mask&((1<<64)-1)} {mask>>64} {pattern&((1<<64)-1)} {pattern>>64}']
  for arr in [ahat,bhat,alhat]:lines.append(' '.join(str(int(x*D)) for x in arr))
  tic_init=time.perf_counter();initial_rng=random.Random(781233+ix)
  for trial in range(trials):
   x=pattern
   for i in range(n):
    if i in fixed:continue
    prev=(x>>(i-1))&1 if i else 0
    q=probs[i][prev]
    if initial_rng.randrange(q.denominator)<q.numerator:x|=1<<i
   lines.append(f'{x&((1<<64)-1)} {x>>64}')
  initialization_seconds=time.perf_counter()-tic_init
  path=P/(name+'_model.txt');path.write_text('\n'.join(lines)+'\n')
  tic=time.perf_counter();done=subprocess.run([str(P/'gibbs_excursions'),str(path)],check=True,capture_output=True,text=True)
  sim=json.loads(done.stdout);sim['simulation_seconds']=time.perf_counter()-tic
  sim['exact_initialization_seconds']=initialization_seconds
  s=F(1,40);R=F(sim['relevant_weight'],40);theta=F(sim['successes'],trials)
  rlo=s+R*max(F(0),theta-radius);rhi=s+R*min(F(1),theta+radius)
  assert p*(s+R)<s/2
  lo=(1/rhi-p/s)/(p*(1-p)*screen*model_factor)
  hi=(1/rlo-p/s)*screen*model_factor/(p*(1-p))
  query_failure=F(2)/exp_bounds(2*trials*radius**2)[0];joint+=query_failure
  p_factor=exp_bounds(2*u)[1]
  p_lo=p/p_factor;p_hi=p*p_factor
  # Unknown true mass is covered, not silently replaced by fitted mass.
  assert p_lo<=ptrue<=p_hi
  row=dict(name=name,n=n,target_constraints=len(fixed),fitted_target_mass=ser(p),
   true_target_mass_for_diagnostic_only=out(ptrue),fitted_target_mass_outward=[out(p),out(p,True)],
   true_target_mass_interval=[out(p_lo),out(p_hi,True)],mean_lower_outward=out(lo),mean_upper_outward=out(hi,True),
   exact_mean_lower=ser(lo),exact_mean_upper=ser(hi),simulator=sim)
  rows.append(row);print(json.dumps({k:v for k,v in row.items() if not k.startswith('exact_') and k!='fitted_target_mass'}),flush=True)
 result=dict(model='Unknown Gibbs path with native local clamp calibration; synthetic observations',
  n=n,states=str(2**n),observed_rates=len(countrows),per_clamp_duration=T,
  sequential_calibration_duration=T*len(countrows),observed_calibration_counts=sum(x['count'] for x in countrows),
  expected_selected_attempts=(6*n-4)*T,
  expected_full_device_attempts_if_background_runs=(3*n-2)*(5*n-3)*T,
  calibration_work_qualification='Sequential clamps; selected attempts and running-background attempts separately charged; clamp/reset work is an additional source-control resource',
  relative_count_tolerance=ser(eta),rounding_denominator=D,
  source_a=[ser(x) for x in a],source_b=[ser(x) for x in b],source_alpha=[ser(x) for x in alpha],
  fitted_a=[ser(x) for x in ahat],fitted_b=[ser(x) for x in bhat],fitted_alpha=[ser(x) for x in alhat],
  calibration_data=countrows,log_weight_error_bound=ser(u),log_flow_error_bound=ser(v),
  source_mean_factor=ser(model_factor),screening_factor=ser(screen),true_and_fitted_gap_lower='1/2',
  killing_rate='1/40',expected_excursion_duration_upper=40,
  calibration_failure_upper=out(alpha_cal,True),joint_failure_upper=out(joint,True),confidence_lower=out(1-joint),
  exact_local_fixture=fixture_check(),compile_seconds=compile_seconds,targets=rows,
  total_seconds=time.perf_counter()-start)
 (P/'gibbs_results.json').write_text(json.dumps(result,indent=2))
 print(json.dumps({k:v for k,v in result.items() if k not in ['calibration_data','source_a','source_b','source_alpha','fitted_a','fitted_b','fitted_alpha','targets']},indent=2))
if __name__=='__main__':main()
