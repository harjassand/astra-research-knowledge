"""Local measurement-to-control protocol and labelled synthetic data checks.
No connected laboratory instrument is used. Sampling here is synthetic.
Optional coarse calibration includes its own shot budget and can be inconclusive.
"""
from pathlib import Path
from fractions import Fraction as F
import math,json,time
import numpy as np
from certify_policy import exp_interval,log_interval
from multi_poly import Certificate
ROOT=Path(__file__).resolve().parent.parent

def sqrt_interval(x,bits=100):
 x=F(x);assert x>=0;s=1<<bits;k=math.isqrt((x.numerator*s*s)//x.denominator)
 assert F(k*k,s*s)<=x<=F((k+1)**2,s*s)
 return F(k,s),F(k+1,s)

def atan_interval(x,terms=80):
 x=F(x)
 if x<0:
  lo,hi=atan_interval(-x,terms);return -hi,-lo
 if x>4:raise ValueError('outside supported calibration sector')
 rlo,rhi=sqrt_interval(1+x*x);zlo=x/(1+rhi);zhi=x/(1+rlo)
 def at(z):
  ss=sum(((-1)**j*z**(2*j+1)/F(2*j+1) for j in range(terms)),F());rem=z**(2*terms+1)/F(2*terms+1)
  return ss-rem,ss+rem
 return 2*at(zlo)[0],2*at(zhi)[1]

def coarse_calibrate(plus_x,plus_y,shots_each=1<<20):
 if shots_each!=1<<20:raise ValueError('the specified confidence budget uses 2^20 per axis')
 for n in [plus_x,plus_y]:
  if not isinstance(n,int) or not 0<=n<=shots_each:raise ValueError('invalid count')
 x=F(2*plus_x-shots_each,shots_each);y=F(2*plus_y-shots_each,shots_each)
 if x<=0:return dict(accepted=False,reason='quadrature outside calibrated phase sector')
 try:alo,ahi=atan_interval(y/x)
 except ValueError:return dict(accepted=False,reason='quadrature outside supported ratio')
 rlo,rhi=sqrt_interval(x*x+y*y)
 if rlo<=0:return dict(accepted=False,reason='insufficient contrast')
 loglo=log_interval(rlo,40)[0];loghi=log_interval(rhi,40)[1]
 rad=F(79,1000)
 Ui=(8*alo-rad,8*ahi+rad);di=(-8*loghi-rad,-8*loglo+rad)
 def outward(I):
  lo,hi=I;s=10**12
  return (F((lo*s).numerator//(lo*s).denominator,s),F(-((-hi*s).numerator//(-hi*s).denominator),s))
 Ui,di=outward(Ui),outward(di)
 accepted=(Ui[0]>=F(39,10) and Ui[1]<=F(41,10) and di[0]>=F(19,10) and di[1]<=F(21,10))
 return dict(accepted=accepted,U_interval=list(map(str,Ui)),d_interval=list(map(str,di)),mean_x=str(x),mean_y=str(y))

def select_control(plus_count,shots,certificate=None):
 rec=certificate or json.loads((ROOT/'results/policy_certificate.json').read_text())
 if shots not in [int(a['shots']) for a in rec['policy_certificates']]:raise ValueError('unsupported shot budget')
 if not isinstance(plus_count,int) or not 0<=plus_count<=shots:raise ValueError('invalid count')
 mean=F(2*plus_count-shots,shots)
 raw=F(rec['control_centre'])+F(rec['gain_rounded'])*mean-F(rec['offset'])
 q=round(raw*2048);return max(F(0),min(F(3),F(q,2048)))

def run():
 start=time.perf_counter();pol=json.loads((ROOT/'results/policy_certificate.json').read_text());rng=np.random.default_rng(20261013)
 # Exact optional-coarse budget, starting only from U in [0,8], d in [1,4].
 Nc=1<<20;hc=F(1,250);exc=F(Nc)*hc**2/2
 assert exp_interval(exc)[0]>4000 # four one-sided events: failure <.001
 assert exp_interval(F(1,2))[1]<F(5,3) # true contrast exp(-d/8) > .6
 coarse_bias=F(1,10000);rho=F(5799,10**6);assert rho**2>2*(hc+coarse_bias)**2
 parameter_error=8*rho/(F(3,5)-rho);assert parameter_error<F(79,1000)
 for item in pol['policy_certificates']:
  h=F(item['hoeffding_radius']);N=int(item['shots'])
  assert exp_interval(F(N)*h*h/2)[0]>250 # decision-stage failure <.008
 # One synthetic coarse calibration, not a measurement of a physical device.
 rx=math.exp(-2/8)*math.cos(4/8);ry=math.exp(-2/8)*math.sin(4/8)
 px=int(rng.binomial(Nc,(1+rx)/2));py=int(rng.binomial(Nc,(1+ry)/2));coarse=coarse_calibrate(px,py,Nc)
 # Good-event demonstration at several unknown parameters; no exact D or optimum is used.
 c=Certificate(json.loads((ROOT/'results/main_multi_exact.json').read_text()));cases=[]
 psi=math.atan2(float(F(pol['readout_sin'])),float(F(pol['readout_cos'])))
 for U,d in [(3.9,1.9),(3.9,2.1),(4.,2.),(4.1,1.9),(4.1,2.1)]:
  mean=math.exp(-d/2)*math.cos((U-4)/2+psi)
  for item in pol['policy_certificates']:
   n=int(item['shots']);plus=int(rng.binomial(n,(1+mean)/2));V=select_control(plus,n,pol);observed=(2*plus-n)/n
   good=abs(observed-mean)<=float(F(item['hoeffding_radius']))
   assert good
   rr=c.compute([(V-c.centre[0],V-c.centre[0]),(F(str(U))-4,F(str(U))-4),(F(str(d))-2,F(str(d))-2)])
   g=max(map(abs,rr['gradient']));mu=F(item['curvature_lower']);point_bound=g*g/(2*mu)
   assert point_bound<=F(item['regret_upper'])
   cases.append(dict(true_U=U,true_d=d,shots=n,synthetic_plus_count=plus,synthetic_mean=observed,control=str(V),good_event=good,model_certified_regret_upper=str(point_bound)))
 # Single-copy variance optimum within this fixed local probe model.
 cu,cd=map(F,pol['compensation']);tau=.5;r=math.exp(-1);var=(float(cu*cu+cd*cd)/r**2-float(cd*cd))/tau**2
 out=dict(coarse_stage=dict(prior_U=[0,8],prior_d=[1,4],shots_per_axis=Nc,total_shots=2*Nc,interrogation_time='1/8',native_evolution_time=Nc//4,statistical_failure_less_than='1/1000',quadrature_statistical_radius=str(hc),quadrature_mean_bias_budget=str(coarse_bias),parameter_error_upper=str(parameter_error),accepted_region_rule='Entire outward calibration box must lie inside U=[3.9,4.1], d=[1.9,2.1]. Otherwise return inconclusive.',synthetic_observation=coarse),combined_stage_failure_less_than='9/1000',interpretation='P(return an uncertified decision AND accept coarse calibration) <.009 under the broad structural prior. This is not a conditional-on-acceptance probability; no acceptance probability is guaranteed for every true model.',synthetic_policy_cases=cases,single_copy_locally_unbiased_variance=float(var),seconds=time.perf_counter()-start,evidence='Synthetic counts and deterministic budget checks only; no experiment was performed.')
 (ROOT/'results/acquisition_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(dict(coarse_accepted=coarse['accepted'],synthetic_cases=len(cases),locally_optimal_variance=var,seconds=out['seconds']),indent=2))
if __name__=='__main__':run()
