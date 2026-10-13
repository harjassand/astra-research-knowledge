"""Deterministic whole-domain physical policy certificate and shot-budget proof.
All reported enclosures are rational, apart from labelled decimal summaries.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import math,json,time,resource
from multi_poly import *
ROOT=Path(__file__).resolve().parent.parent

def pack(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {k:pack(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [pack(v) for v in x]
 return x

def sensor_choice(c):
 H=2*c.p[(2,0,0)];BU=c.p[(1,1,0)];BD=c.p[(1,0,1)]
 cu=F(round(float(-BU/H)*1024),1024)
 candidates=[]
 for k in range(2,65):
  cd=-cu*F(2*k,k*k-1)
  score=(H*cu+BU)**2+(H*cd+BD)**2
  candidates.append((score,k,cu,cd))
 _,k,cu,cd=min(candidates);norm=cu*F(k*k+1,k*k-1)
 assert cu*cu+cd*cd==norm*norm
 return cu,cd,norm,k

def sensor_polynomial(cu,cd,norm,k,degree=3):
 nr=F(2*k,k*k+1);ns=F(k*k-1,k*k+1)
 re={Z:F(1)};im={};s={}
 zr={(0,0,1):F(-1,2)};zi={(0,1,0):F(1,2)}
 for j in range(degree+1):
  s=add(s,scale(add(scale(re,nr),scale(im,ns)),2*norm/F(math.factorial(j))))
  re,im=add(mul(re,zr),mul(im,zi),-1),add(mul(re,zi),mul(im,zr))
 s[Z]-=2*norm*nr;s={a:v for a,v in s.items() if v}
 assert s[(0,1,0)]==cu and s[(0,0,1)]==cd
 return s,nr,ns

def exp_interval(x,terms=32):
 assert x>=0
 low=sum((x**j/F(math.factorial(j)) for j in range(terms+1)),F())
 next=x**(terms+1)/F(math.factorial(terms+1));assert x<F(terms+2)
 return low,low+next/(1-x/F(terms+2))

def log_interval(x,terms=12):
 assert x>0
 z=(x-1)/(x+1)
 s=2*sum((z**(2*j+1)/F(2*j+1) for j in range(terms)),F())
 rem=2*abs(z)**(2*terms+1)/((2*terms+1)*(1-z*z))
 return s-rem,s+rem

def fibre_interval(a,k=16):
 x=a/2;K=8
 sin=sum(((-1)**j*x**(2*j+1)/F(math.factorial(2*j+1)) for j in range(K+1)),F())
 cos=sum(((-1)**j*x**(2*j)/F(math.factorial(2*j)) for j in range(K+1)),F())
 es=abs(x)**(2*K+3)/F(math.factorial(2*K+3));ec=abs(x)**(2*K+2)/F(math.factorial(2*K+2))
 ratio=F(k*k-1,2*k)
 lo=cos-ec+ratio*(sin-es);hi=cos+ec+ratio*(sin+es)
 dl=2*log_interval(lo)[0];du=2*log_interval(hi)[1]
 scale10=10**12
 return F((dl*scale10).numerator//(dl*scale10).denominator,scale10),F(-((-du*scale10).numerator//(-du*scale10).denominator),scale10)

def run():
 start=time.perf_counter();central=json.loads((ROOT/'results/main_multi_exact.json').read_text());c=Certificate(central);delta=F(1,10)
 global_checks=[]
 for name,a,b in [('V0p0',F(0),F(1,4)),('V0p5',F(1,4),F(3,4)),('V1p0',F(3,4),F(5,4)),('V1p5',F(5,4),F(7,4))]:
  cc=Certificate(json.loads((ROOT/f'results/anchors/{name}_exact.json').read_text()))
  box=[(a-cc.centre[0],b-cc.centre[0]),(-delta,delta),(-delta,delta)]
  r=cc.compute(box,parts=(2,1,1));assert r['gradient'][0]>0
  global_checks.append(dict(V=[a,b],source=name,gradient=r['gradient']))
 for a,b,sign in [(F(7,4),F(2),1),(F(5,2),F(11,4),-1),(F(11,4),F(3),-1)]:
  r=c.compute([(a-c.centre[0],b-c.centre[0]),(-delta,delta),(-delta,delta)],parts=(8,1,1))
  assert r['gradient'][0]>0 if sign==1 else r['gradient'][1]<0
  global_checks.append(dict(V=[a,b],source='main',gradient=r['gradient']))
 corridor=c.compute([(F(2)-c.centre[0],F(5,2)-c.centre[0]),(-delta,delta),(-delta,delta)],parts=(8,1,1));assert corridor['curvature'][1]<0
 cu,cd,norm,k=sensor_choice(c);print('chosen',cu,cd,norm,k,flush=True)
 sensor,nr,ns=sensor_polynomial(cu,cd,norm,k)
 maps=[add(sensor,{(1,0,0):F(1)}),{(0,1,0):F(1)},{(0,0,1):F(1)}]
 Epoly=2*norm*F(10,9)*F(1,10)**4/F(24) # |(-b+ia)/2| <= .1
 el,eu=exp_interval(F(1));assert eu<F(87,32)
 Slo=2*norm*el;Sup=2*norm*eu
 sg=F(round(float((Slo+Sup)/2)*(1<<32)),1<<32);arithmetic=max(abs(sg-Slo),abs(sg-Sup));assert arithmetic<F(1,1<<32)
 offset=2*norm*nr
 policies=[]
 # Both budgets have the same rigorous coverage probability >99%.
 for N,h,tube in [(1<<18,F(13,2000),F(23,1000)),(1<<20,F(13,4000),F(12,1000))]:
  exponent=F(N)*h*h/2;exp_lower,_=exp_interval(exponent,32);assert exp_lower>200
  expectation_bias=F(1,10000);setting_error=F(1,2048)
  e=Sup*(h+expectation_bias)+setting_error+arithmetic+Epoly;assert e<tube
  res=c.compute([(-tube,tube),(-delta,delta),(-delta,delta)],maps=maps)
  G=max(map(abs,res['gradient']));mu=-res['curvature'][1];assert mu>0
  # Roots are inside the larger tube. For smaller tube use a root-containing
  # enlarged tube in curvature, while gradient is bounded on deployment tube.
  root_tube=F(23,1000);rootres=c.compute([(-root_tube,root_tube),(-delta,delta),(-delta,delta)],maps=maps)
  zero=c.compute([(F(0),F(0)),(-delta,delta),(-delta,delta)],maps=maps)
  g0=max(map(abs,zero['gradient']));root_mu=-rootres['curvature'][1]
  assert root_mu*root_tube>g0
  vrange=bound(maps[0],[(-root_tube,root_tube),(-delta,delta),(-delta,delta)])
  assert c.centre[0]+vrange[0]>2 and c.centre[0]+vrange[1]<F(5,2)
  regret=G*G/(2*root_mu)
  policies.append(dict(shots=N,hoeffding_radius=h,confidence_at_least=F(99,100),mean_bias_budget=expectation_bias,setting_error_total=setting_error,command_grid=F(1,2048),setting_rounding_error=F(1,4096),actuation_error_budget=F(1,4096),arithmetic_error=arithmetic,sensor_series_error=Epoly,total_control_error=e,checked_tube=tube,gradient_bound=G,curvature_lower=root_mu,regret_upper=regret,native_evolution_time=F(N,2),gradient_interval=res['gradient']))
  print('policy',N,'regret',float(regret),'gradient',float(G),'mu',float(root_mu),flush=True)
 # Lower bound on the minimax loss of any no-observation fixed control.
 left=F(263,125);right=F(2223,1000)
 rl=c.compute([(left-c.centre[0],left-c.centre[0]),(-delta,-delta),(delta,delta)])
 rr=c.compute([(right-c.centre[0],right-c.centre[0]),(delta,delta),(-delta,-delta)])
 assert rl['gradient'][1]<0 and rr['gradient'][0]>0
 midcurv=c.compute([(F(21,10)-c.centre[0],F(56,25)-c.centre[0]),(-delta,delta),(-delta,delta)],parts=(4,1,1))
 mu_fixed=F(7,100);assert midcurv['curvature'][1]<-mu_fixed
 no_data=mu_fixed*(right-left)**2/8
 assert policies[0]['regret_upper']<no_data and policies[1]['regret_upper']<no_data
 # Exactly observationally equivalent pairs, with d described by a logarithm.
 fibre=[];NO=load(central['residual_odd_norm_poly']);NE=load(central['residual_even_norm_poly'])
 for a in [F(-1,100),F(1,100)]:
  dl,du=fibre_interval(a,k);assert -delta<dl<du<delta
  box=[(F(0),F(0)),(a,a),(dl,du)]
  ph=bound(c.p,box);o=max(F(),bound(NO,box)[1]);e=max(F(),bound(NE,box)[1]);beta=min(F(1),(2+dl)/2)
  value=[ph[0]-4*e/beta,ph[1]+4*o/beta]
  fibre.append(dict(U=4+a,d_interval=[2+dl,2+du],D_interval=value,V=c.centre[0],mean='exp(-1)*2k/(k^2+1)',definition_delta_d='2 log(cos(delta_U/2)+(k^2-1)/(2k)*sin(delta_U/2))'))
 assert fibre[0]['D_interval'][0]>fibre[1]['D_interval'][1]
 separation=fibre[0]['D_interval'][0]-fibre[1]['D_interval'][1]
 result=dict(parameters=dict(t=F(1),U=[F(39,10),F(41,10)],d=[F(19,10),F(21,10)],V=[F(0),F(3)]),global_monotonicity=global_checks,central_curvature=corridor['curvature'],unique_global_optimizer_for_every_model=True,control_centre=c.centre[0],compensation=[cu,cd],compensation_norm=norm,pythagorean_k=k,readout_cos=nr,readout_sin=-ns,interrogation_time=F(1,2),gain_rounded=sg,gain_interval=[Slo,Sup],offset=offset,control_formula='round_to_1/2048(V0 + gain*sample_mean - offset), clipped to [0,3]; actuator error <=1/4096',sensor_mean_polynomial=dump(sensor),policy_certificates=policies,no_observation_minimax_regret_lower=no_data,no_observation_witness_gradient_left=rl['gradient'],no_observation_witness_gradient_right=rr['gradient'],indistinguishable_models=fibre,indistinguishable_D_separation_lower=separation,maximum_min_ring_size=max(central['min_ring_size'],21),seconds=time.perf_counter()-start,peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,evidence='Deterministic rational model/protocol certificate; no laboratory experiment.')
 path=ROOT/'results/policy_certificate.json';path.write_text(json.dumps(pack(result),indent=2));print(json.dumps(dict(regrets=[float(x['regret_upper']) for x in policies],no_data_lower=float(no_data),D_separation=float(separation),fibre=[dict(U=float(x['U']),d=list(map(float,x['d_interval'])),D=list(map(float,x['D_interval']))) for x in fibre],seconds=result['seconds']),indent=2),flush=True)
 return result
if __name__=='__main__':run()
