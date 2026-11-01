"""Autonomous Gibbs|A mean B-hitting time via an acquired Poisson current.
This is a new actual engineered-model observable; not an inherited capacity label.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,hashlib,json,time
SOURCE=Path(__file__).resolve().parent.parent/'radial_kinetic_service_20261031'/'receive_kinetic.py'
SOURCE_SHA='b4b75f4eb063e13a8c4fe49a34af5c55f182df87317a1cde4c0c14b3aefdf8cb'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA:raise RuntimeError('accepted kinetic acquisition dependency hash mismatch')
spec=importlib.util.spec_from_file_location('accepted_kinetic_for_mfpt',SOURCE);base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
Unknown=base.Unknown;fs=base.fs;interval=base.enclosure

def bits(q):return max(q.numerator.bit_length(),q.denominator.bit_length())
class Scalar:
 def __init__(self,alpha,kappa,P,max_points,max_operations,max_integer_bits):
  self.alpha=alpha;self.kappa=kappa;self.P=P;self.S=1<<P;self.fixed=base.Fixed(P,max_operations,max_integer_bits,1,1)
  self.max_points=max_points;self.cache={};self.powers=0;self.tails={}
 def power(self,q,n):
  if q<=0 or type(n)is not int or n<0:raise Unknown('positive integer-power interface')
  self.powers+=1;x=self.fixed.rat(q);a=(self.S,self.S)
  while n:
   if n&1:a=self.fixed.mul(a,x)
   n//=2
   if n:x=self.fixed.mul(x,x)
  return a
 def point(self,y,kind):
  key=(y,kind)
  if key in self.cache:return self.cache[key]
  if len(self.cache)>=self.max_points:raise Unknown('total scalar-point budget')
  if kind=='q':
   if y<F(1,2):raise Unknown('mass profile domain')
  elif kind=='r':
   if not 0<=y<=F(1,2):raise Unknown('resistance profile domain')
  else:raise Unknown('scalar profile kind')
  v=1+self.kappa*(1-y*y)**2;z=self.power(1/v if kind=='q' else v,self.alpha)
  self.cache[key]=z;return z
 def integrate(self,a,b,N,kind):
  if not a<b or type(N)is not int or N<=0:raise Unknown('integration arguments')
  if kind=='q' and not (F(1,2)<=a<b<=1 or 1<=a<b):raise Unknown('mass interval crosses monotonicity join')
  if kind=='r' and not 0<=a<b<=F(1,2):raise Unknown('resistance interval outside monotone slab')
  h=(b-a)/N;prev=self.point(a,kind);lo=hi=0
  for j in range(1,N+1):
   cur=self.point(a+j*h,kind);lo+=min(prev[0],cur[0]);hi+=max(prev[1],cur[1]);prev=cur
  return h*F(lo,self.S),h*F(hi,self.S)
 def tail(self,T):
  if T in self.tails:return self.tails[T]
  if T<=1:raise Unknown('infinite tail cutoff must exceed one')
  # Exact analytic bound T/(4alpha-1)*[kappa(T²-1)²]^(-alpha), rounded upward.
  _,hi=self.power(1/(self.kappa*(T*T-1)**2),self.alpha)
  self.tails[T]=T*F(hi,self.S)/(4*self.alpha-1);return self.tails[T]

def acquire(raw,**budgets):
 if type(raw)is not dict or set(raw)!={'dimension','energy_terms','tangent_program','radial_gain'}:raise Unknown('complete actual radial-gain kinetic model')
 gamma=base.raw_frac(raw['radial_gain'],budgets['max_coefficient_bits'])
 if gamma<=0:raise Unknown('positive actual radial gain')
 m=base.strict_int(raw['dimension'],'dimension')
 if m>budgets['max_dimension']:raise Unknown('dimension budget before witness allocation')
 energy={k:raw[k] for k in ['dimension','energy_terms','tangent_program']}
 # This algebraic witness is not the actual Gibbs|A initialization.
 witness=[F(1)]+[F(0)]*(m-1);info,_,alpha=base.acquire(energy,witness,**budgets)
 info['energy_probe_at_e1']=info.pop('initial_energy');info['probe_rational_operations']=info.pop('initial_energy_rational_operations');info['probe_max_stored_bits']=info.pop('initial_energy_max_stored_bits')
 info['raw_sha256']=base.canonical_hash(raw);info['radial_gain']=fs(gamma)
 info['model']='actual radial-gain divergence-form homogeneous lift plus complete-pair tangent diffusion'
 if alpha.denominator!=1 or alpha<4:raise Unknown('finite scalar-only MFPT backend requires integer alpha>=4')
 return info,alpha.numerator,gamma

def certify(raw,*,beta=F(1),kappa=F(1),quad_relative=F(1,1000),full_ratio=F(101,100),
 max_dimension=1024,max_terms=100000,max_coefficient_bits=4096,max_exponent_entries=64000000,max_total_coefficient_bits=32000000,max_rational_bits=1000000,
 max_grid=131072,max_points=1000000,max_cutoff=65536,max_precision=16384,max_operations=30000000,max_integer_bits=1000000):
 start=time.perf_counter();task=locals().copy();task.pop('raw');task.pop('start')
 for k,v in task.items():
  if k not in ['beta','kappa','quad_relative','full_ratio']:base.strict_int(v,k)
 for k in ['beta','kappa','quad_relative','full_ratio']:
  v=base.frac(task[k],k,True)
  if bits(v)>max_coefficient_bits:raise Unknown('task rational bit budget')
 if quad_relative>=1 or full_ratio<=1:raise Unknown('numerical tolerance<1 and requested total ratio>1')
 if max_grid<64 or max_cutoff<2:raise Unknown('initial grid/cutoff budget')
 budgetkeys=['max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits']
 info,alpha,gamma=acquire(raw,**{k:task[k]for k in budgetkeys})
 a=1+F(9,16)*kappa;transport_factor=1+4*kappa/(beta*gamma*a*a)
 if transport_factor>=full_ratio:raise Unknown('this sufficient transport-current bound cannot meet requested total width at the declared radial gain')
 P=max(192,alpha*(bits(kappa)+2)+128)
 if P>max_precision or 2*P>max_integer_bits:raise Unknown('fixed precision allocation budget')
 ii=Scalar(alpha,kappa,P,max_points,max_operations,max_integer_bits)
 seed=ii.integrate(F(1),F(5,4),32,'q')[0]
 if seed<=0:raise Unknown('positive basin seed unresolved at paid precision')
 T=F(2)
 while ii.tail(T)>quad_relative*seed/8:
  T*=2
  if T>max_cutoff:raise Unknown('infinite-tail cutoff budget')
 N=64
 while True:
  if N>max_grid:raise Unknown('monotone quadrature grid budget')
  ml,mh=ii.integrate(F(1,2),F(1),N,'q');left=F(1)
  while left<T:
   lo,hi=ii.integrate(left,2*left,N,'q');ml+=lo;mh+=hi;left*=2
  mh+=ii.tail(T);rl,rh=ii.integrate(F(0),F(1,2),N,'r');rl*=2;rh*=2
  if ml>0 and rl>0 and mh*rh<=(1+quad_relative)*ml*rl:break
  N*=2
 b=F(1,2);d=F(1,alpha);v_d=1+kappa*(1-(1+d)**2)**2
 ap=ii.power(a,alpha);cp=ii.power(v_d,alpha);am=ii.power(a,alpha-3);ainv=ii.power(1/a,alpha)
 Ahi=F(ap[1],ii.S);Chi=F(cp[1],ii.S);Amhi=F(am[1],ii.S)
 S0=(1-b)*Ahi+d*Chi;S1=(1+d-b)*16*kappa*kappa*Amhi;Wfar=1/(64*kappa*kappa*(alpha-1)**2*d)
 r=F(ainv[1],ii.S)/ml
 components={'slab_with_transport':beta*mh*rh*transport_factor,'basin_near_longitudinal':beta*mh*S0,
 'basin_far_longitudinal':beta*Wfar/ml,'basin_near_radial':F(alpha)*mh*S1/gamma,'basin_far_radial':F(alpha)/(gamma*(alpha-1)**2)}
 low=beta*ml*rl;high=(1+r)*sum(components.values(),F(0));ratio=high/low
 if ratio>full_ratio:raise Unknown('full autonomous MFPT outer interval misses requested TOTAL ratio; structural slack is not only numerical error')
 return {'schema':'autonomous_homogeneous_radial_mfpt.v1','dependency_sha256':SOURCE_SHA,'task':{k:fs(v)if type(v)is F else v for k,v in task.items()},'acquisition':info,
 'observable':'E[tau_{Y>=1/2}] from Gibbs conditioned on Y<=-1/2, or identical (Y,U) initial pushforward',
 'actual_projected_generator':'beta^-1 d_yy - v_prime*u d_y + gamma*(alpha/beta-v*u) d_u + gamma*u/beta d_uu',
 'initialization':'rho_A proportional to 1_{y<=-1/2} u^(alpha-1) exp(-beta*v(y)*u); angular Gibbs sampling not required for the observable law, physical preparation not authenticated',
 'proof_method':'zero-resolvent source-A/current-S comparison and finite conditional-transport Poisson resistance; not capacity substitution',
 'not_claimed':['original constant-mobility model','arbitrary initial (y,u) hitting-time mean','actual physical generator identification','physical actuation or preparation','angular mixing'],
 'basin_mass':interval(ml,mh),'slab_resistance':interval(rl,rh),'mean_hitting_time':interval(low,high),'total_ratio_exact':fs(ratio),
 'transport_factor_upper':fs(transport_factor),'slab_to_basin_mass_ratio_upper':fs(r),
 'upper_components':{k:fs(v)for k,v in components.items()},'source_cross_multiplier_upper':fs(1+r),
 'constants':{'a':fs(a),'d':fs(d),'v_1_plus_d':fs(v_d),'S0_upper':fs(S0),'S1_upper':fs(S1),'Wfar_upper':fs(Wfar)},
 'N':N,'T':fs(T),'tail_upper':fs(ii.tail(T)),'precision_bits':P,
 'work':{'scalar_points':len(ii.cache),'integer_power_calls':ii.powers,'fixed_operations':ii.fixed.operations,'largest_guarded_product_bits':ii.fixed.max_guarded_bits},'seconds':time.perf_counter()-start}

def verify(raw,certificate,**external_task):
 exp=certify(raw,**external_task)
 if type(certificate)is not dict:raise Unknown('certificate object')
 for k in ['schema','dependency_sha256','task','acquisition','observable','actual_projected_generator','initialization','proof_method','not_claimed','total_ratio_exact','transport_factor_upper','slab_to_basin_mass_ratio_upper','upper_components','source_cross_multiplier_upper','constants','N','T','tail_upper','precision_bits']:
  if not base.same(certificate.get(k),exp[k]):raise Unknown('strict original model/task/proof binding: '+k)
 for k in ['basin_mass','slab_resistance','mean_hitting_time']:
  if type(certificate.get(k))is not dict:raise Unknown('interval schema')
  for side in ['lower','upper']:
   if not base.same(certificate[k].get(side),exp[k][side]):raise Unknown('exact recomputed endpoint: '+k)
 return {'status':'PASS','scope':exp['observable'],'actual_radial_gain':exp['acquisition']['radial_gain'],'m':exp['acquisition']['m'],'total_ratio_exact':exp['total_ratio_exact'],'physical_membership':'not authenticated'}

def fixture(m,coupling=F(20),tangent=F(1),gamma=F(512),p=4):
 raw=base.fixture(m,p,coupling,tangent);raw['radial_gain']=fs(gamma);return raw

def external_from_record(cert):
 d=dict(cert['task'])
 for k in ['beta','kappa','quad_relative','full_ratio']:d[k]=F(d[k])
 return d

if __name__=='__main__':
 out=[]
 for m,gain,tol,target,coupling,tangent in [(64,F(512),F(1,1000),F(11,10),F(20),F(1)),(128,F(512),F(1,1000),F(101,100),F(20),F(1)),(256,F(512),F(1,1000),F(101,100),F(20),F(1)),(512,F(512),F(1,1000),F(101,100),F(20),F(1)),(512,F(512),F(1,1000),F(101,100),F(10**100),F(10**80))]:
  made=time.perf_counter();raw=fixture(m,coupling,tangent,gain);generation_seconds=time.perf_counter()-made
  raw_bytes=len(json.dumps(raw,sort_keys=True,separators=(',',':')).encode());cert=certify(raw,quad_relative=tol,full_ratio=target)
  row={'fixture':{'m':m,'coupling':fs(coupling),'tangent':fs(tangent),'radial_gain':fs(gain)},'fixture_generation_seconds':generation_seconds,'raw_serialized_bytes':raw_bytes,'certificate':cert};out.append(row)
  Path('results.json').write_text(json.dumps(out,indent=2)+'\n');print(m,cert['mean_hitting_time']['display'],float(F(cert['total_ratio_exact'])),cert['work'],cert['seconds'],flush=True)

# intentional isolated audit corruption
