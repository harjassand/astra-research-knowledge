"""Actual constant-SPD Langevin Gibbs|A mean passage-time enclosure.
No energy Markov closure, angular mixing, fixed-ray preparation or capacity relabel.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,hashlib,json,time
SOURCE=Path(__file__).resolve().parent.parent/'autonomous_radial_mfpt_20261031'/'receive_mfpt.py'
SOURCE_SHA='607f90e242e47de87d217ca8e19aa16115780eeb10bdfc83a1e3d2dbf915cff0'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA:raise RuntimeError('scalar acquisition dependency hash mismatch')
spec=importlib.util.spec_from_file_location('frozen_mfpt_scalar',SOURCE);scalar=importlib.util.module_from_spec(spec);spec.loader.exec_module(scalar)
base=scalar.base;Unknown=base.Unknown;fs=base.fs;interval=base.enclosure;Scalar=scalar.Scalar
from math import isqrt

def bits(q):return max(q.numerator.bit_length(),q.denominator.bit_length())
class Roots:
 def __init__(self,P,limit):self.P=P;self.limit=limit;self.calls=0;self.max_bits=0
 def upper(self,q):
  if q<=0:raise Unknown('positive root argument')
  size=bits(q);self.max_bits=max(self.max_bits,size)
  if size>self.limit:raise Unknown('root argument integer budget')
  self.calls+=1;n=isqrt(q.numerator);d=isqrt(q.denominator)
  if n*n==q.numerator and d*d==q.denominator:return F(n,d)
  size=q.numerator.bit_length()+2*self.P;self.max_bits=max(self.max_bits,size)
  if size>self.limit:raise Unknown('scaled root integer budget')
  t=(q.numerator<<(2*self.P))//q.denominator
  return F(isqrt(t)+1,1<<self.P)

def acquire(raw,**budgets):
 if type(raw)is not dict or set(raw)!={'dimension','energy_terms','mobility_program'}:raise Unknown('complete actual constant-mobility model')
 m=base.strict_int(raw['dimension'],'dimension')
 if m>budgets['max_dimension']:raise Unknown('dimension budget before witness allocation')
 program=raw['mobility_program'];cb=budgets['max_coefficient_bits']
 if type(program)is not dict:raise Unknown('actual mobility program schema')
 if set(program)=={'kind','value'} and program['kind']=='constant_isotropic':
  values=[base.raw_frac(program['value'],cb)];mobility_entries=1
 elif set(program)=={'kind','entries'} and program['kind']=='constant_diagonal':
  if type(program['entries'])is not list or len(program['entries'])!=m:raise Unknown('actual diagonal mobility dimension')
  values=[base.raw_frac(x,cb)for x in program['entries']];mobility_entries=m
 else:raise Unknown('constant isotropic or diagonal actual mobility required')
 if any(x<=0 for x in values):raise Unknown('actual mobility must be SPD')
 mu=min(values);mobility_bits=sum(x.numerator.bit_length()+x.denominator.bit_length()for x in values)
 # Reuse ONLY the energy/coercivity grammar. Synthetic zero tangent and e1 are
 # algebraic parser inputs, not this model or its exact Gibbs initialization.
 energy={'dimension':m,'energy_terms':raw['energy_terms'],'tangent_program':{'kind':'complete_pair_gradient','weight':'0'}}
 witness=[F(1)]+[F(0)]*(m-1);info,_,alpha=base.acquire(energy,witness,**budgets)
 if info['p']!=4 or alpha.denominator!=1 or alpha<4:raise Unknown('quartic finite MFPT backend requires integer alpha>=4')
 if info['coefficient_bits_read']+mobility_bits>budgets['max_total_coefficient_bits']:raise Unknown('total energy plus mobility coefficient budget')
 info['energy_probe_at_e1']=info.pop('initial_energy');info['probe_rational_operations']=info.pop('initial_energy_rational_operations');info['probe_max_stored_bits']=info.pop('initial_energy_max_stored_bits')
 info.pop('tangent_weight');info.pop('transverse_SPD_away_origin')
 info['raw_sha256']=base.canonical_hash(raw);info['mobility_kind']=program['kind'];info['mobility_floor']=fs(mu);info['mobility_entries_read']=mobility_entries;info['mobility_coefficient_bits_read']=mobility_bits
 info['model']='ordinary constant-SPD Langevin; unit longitudinal mobility and zero cross mobility'
 info['transverse_SPD_everywhere']=True
 return info,alpha.numerator,mu,F(info['pure_coefficient_min'])

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
 info,alpha,mu,dmin=acquire(raw,**{k:task[k]for k in budgetkeys})
 a=1+F(9,16)*kappa
 P=max(192,alpha*(bits(kappa)+2)+128)
 if P>max_precision or 2*P>max_integer_bits:raise Unknown('fixed precision allocation budget')
 roots=Roots(P,max_integer_bits)
 C_s=kappa*roots.upper(1/(beta*dmin*a*a*a))/(2*mu)
 D_max=4*alpha*max(kappa,F(1))*roots.upper(1/(beta*dmin))/mu
 transport_factor=1+C_s
 if transport_factor>=full_ratio:raise Unknown('this sufficient current bound cannot meet requested width at the actual mobility floor')
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
 ap=ii.power(a,alpha);cp=ii.power(v_d,alpha);ainv=ii.power(1/a,alpha)
 Ahi=F(ap[1],ii.S);Chi=F(cp[1],ii.S)
 S0=(1-b)*Ahi+d*Chi;Wfar=1/(64*kappa*kappa*(alpha-1)**2*d)
 r=F(ainv[1],ii.S)/ml
 components={'slab_with_transport':beta*mh*rh*transport_factor,'basin_near_with_global_transport':beta*(1+D_max)*mh*S0,'basin_far_with_global_transport':beta*(1+D_max)*Wfar/ml}
 low=beta*ml*rl;high=(1+r)*sum(components.values(),F(0));ratio=high/low
 if ratio>full_ratio:raise Unknown('full autonomous MFPT outer interval misses requested TOTAL ratio; structural slack is not only numerical error')
 return {'schema':'ordinary_constant_spd_quartic_mfpt.v1','dependency_sha256':SOURCE_SHA,'task':{k:fs(v)if type(v)is F else v for k,v in task.items()},'acquisition':info,
 'observable':'E[tau_{Y>=1/2}] from EXACT FULL Gibbs conditioned on Y<=-1/2',
 'actual_full_generator':'beta^-1 d_yy - v_prime*U d_y + beta^-1 trace(M Hess_z) - v*(M grad U) dot grad_z',
 'initialization':'exact full rho_A proportional to 1_{y<=-1/2} exp(-beta*v(y)*U(z)); neither fixed-ray nor approximate total-variation preparation is authenticated',
 'proof_method':'zero-resolvent source-A/current-S comparison and finite conditional-transport Poisson resistance; not capacity substitution',
 'not_claimed':['projected energy Markov closure','arbitrary initial-law hitting-time mean','fixed-ray initialization equivalence','actual physical generator identification','physical implementation or finite-bit preparation','angular mixing'],
 'basin_mass':interval(ml,mh),'slab_resistance':interval(rl,rh),'mean_hitting_time':interval(low,high),'total_ratio_exact':fs(ratio),
 'transport_factor_upper':fs(transport_factor),'slab_to_basin_mass_ratio_upper':fs(r),
 'upper_components':{k:fs(v)for k,v in components.items()},'source_cross_multiplier_upper':fs(1+r),
 'constants':{'a':fs(a),'d':fs(d),'v_1_plus_d':fs(v_d),'S0_upper':fs(S0),'global_transport_correction_upper':fs(D_max),'Wfar_upper':fs(Wfar)},
 'N':N,'T':fs(T),'tail_upper':fs(ii.tail(T)),'precision_bits':P,
 'work':{'scalar_points':len(ii.cache),'integer_power_calls':ii.powers,'fixed_operations':ii.fixed.operations,'largest_guarded_product_bits':ii.fixed.max_guarded_bits,'root_calls':roots.calls,'largest_root_integer_bound_bits':roots.max_bits},'seconds':time.perf_counter()-start}

def verify(raw,certificate,**external_task):
 exp=certify(raw,**external_task)
 if type(certificate)is not dict:raise Unknown('certificate object')
 for k in ['schema','dependency_sha256','task','acquisition','observable','actual_full_generator','initialization','proof_method','not_claimed','total_ratio_exact','transport_factor_upper','slab_to_basin_mass_ratio_upper','upper_components','source_cross_multiplier_upper','constants','N','T','tail_upper','precision_bits']:
  if not base.same(certificate.get(k),exp[k]):raise Unknown('strict original model/task/proof binding: '+k)
 for k in ['basin_mass','slab_resistance','mean_hitting_time']:
  if type(certificate.get(k))is not dict:raise Unknown('interval schema')
  for side in ['lower','upper']:
   if not base.same(certificate[k].get(side),exp[k][side]):raise Unknown('exact recomputed endpoint: '+k)
 return {'status':'PASS','scope':exp['observable'],'actual_mobility_floor':exp['acquisition']['mobility_floor'],'m':exp['acquisition']['m'],'total_ratio_exact':exp['total_ratio_exact'],'physical_membership':'not authenticated'}

def fixture(m,coupling=F(20),mobility=F(64),diagonal=False):
 raw=base.fixture(m,4,coupling,F(0));raw.pop('tangent_program')
 raw['mobility_program']={'kind':'constant_diagonal','entries':[fs(mobility*(i+1))for i in range(m)]} if diagonal else {'kind':'constant_isotropic','value':fs(mobility)}
 return raw

def external_from_record(cert):
 d=dict(cert['task'])
 for k in ['beta','kappa','quad_relative','full_ratio']:d[k]=F(d[k])
 return d

if __name__=='__main__':
 out=[]
 for m,mobility,target,coupling,diagonal in [(512,F(1),F(13,10),F(20),False),(64,F(64),F(11,10),F(20),False),(128,F(64),F(101,100),F(20),False),(256,F(64),F(101,100),F(20),False),(512,F(64),F(101,100),F(20),False),(512,F(64),F(101,100),F(10**100),True)]:
  made=time.perf_counter();raw=fixture(m,coupling,mobility,diagonal);generation_seconds=time.perf_counter()-made
  raw_bytes=len(json.dumps(raw,sort_keys=True,separators=(',',':')).encode());cert=certify(raw,full_ratio=target)
  row={'fixture':{'m':m,'coupling':fs(coupling),'mobility':fs(mobility),'diagonal':diagonal},'fixture_generation_seconds':generation_seconds,'raw_serialized_bytes':raw_bytes,'certificate':cert};out.append(row)
  Path('results.json').write_text(json.dumps(out,indent=2)+'\n');print(m,cert['mean_hitting_time']['display'],float(F(cert['total_ratio_exact'])),cert['work'],cert['seconds'],flush=True)
