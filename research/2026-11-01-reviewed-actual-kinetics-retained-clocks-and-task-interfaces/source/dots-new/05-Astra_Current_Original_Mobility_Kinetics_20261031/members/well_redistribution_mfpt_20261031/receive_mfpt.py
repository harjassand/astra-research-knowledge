"""Ordinary unit-mobility-capable MFPT via explicit well redistribution.
New dual source current, not a changed physical generator or a fiber PDE oracle.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,hashlib,json,time
SOURCE=Path(__file__).resolve().parent.parent/'constant_spd_mfpt_20261031'/'receive_mfpt.py'
SOURCE_SHA='7c3a732589bec0aa4240c3970c84be2079421343f791ce68b2e4e92bd65b81ca'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA:raise RuntimeError('accepted constant-SPD acquisition dependency hash mismatch')
spec=importlib.util.spec_from_file_location('constant_spd_for_well_current',SOURCE);core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
base=core.base;Unknown=base.Unknown;fs=base.fs;interval=base.enclosure;bits=core.bits;Roots=core.Roots;acquire=core.acquire
class Scalar(core.Scalar):
 def point(self,y,kind):
  if kind!='rplus':return super().point(y,kind)
  if not 0<=y<=F(1,2):raise Unknown('parallel resistance profile outside slab')
  key=(y,kind)
  if key in self.cache:return self.cache[key]
  if len(self.cache)>=self.max_points:raise Unknown('total scalar-point budget including extra Rplus profile')
  v=1+self.kappa*(1-y*y)**2;vstar=1+self.kappa;den=2*vstar-v
  if den<=0:raise Unknown('positive parallel-current denominator')
  z=self.power(vstar*vstar/den,self.alpha);self.cache[key]=z;return z
 def integrate(self,a,b,N,kind):
  if kind!='rplus':return super().integrate(a,b,N,kind)
  if not 0<=a<b<=F(1,2)or type(N)is not int or N<=0:raise Unknown('monotone Rplus integration arguments')
  h=(b-a)/N;prev=self.point(a,kind);lo=hi=0
  for j in range(1,N+1):
   cur=self.point(a+j*h,kind);lo+=min(prev[0],cur[0]);hi+=max(prev[1],cur[1]);prev=cur
  return h*F(lo,self.S),h*F(hi,self.S)

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
 # Do NOT impose the old O(1/mu) slab-factor gate: the new A-current
 # has zero transverse slab flow. C_s now controls the SEPARATE S-current only.
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
  pl,ph=ii.integrate(F(0),F(1,2),N,'rplus');pl*=2;ph*=2
  if ml>0 and rl>0 and pl>0 and mh*rh<=(1+quad_relative)*ml*rl and ph<=(1+quad_relative)*pl:break
  N*=2
 b=F(1,2);d=F(1,alpha);vstar=1+kappa;Gb=vstar*vstar/(2*vstar-a);G1=vstar*vstar/(2*vstar-1)
 gb=ii.power(Gb,alpha);g1=ii.power(G1,alpha);ainv=ii.power(1/a,alpha)
 Gbhi=F(gb[1],ii.S);G1hi=F(g1[1],ii.S)
 K=F(alpha)*roots.upper(1/(beta*dmin))/(8*mu)
 r=F(ainv[1],ii.S)/ml
 components={'parallel_slab':beta*mh*ph,'near_well_longitudinal':beta*mh*(1+d-b)*Gbhi,
 'middle_well_longitudinal':beta*vstar*vstar*G1hi/(128*kappa*kappa*(alpha-1)**2*d*d*ml),
 'well_vertical_redistribution':beta*K*kappa*kappa*G1hi/ml,
 'far_conditional_tail':beta*(1+D_max)/(16*kappa*kappa*(alpha-1)**2*ml)}
 UA=sum(components.values(),F(0));low=beta*ml*rl;T0hi=beta*mh*rh
 US=r*r*T0hi*transport_factor
 high=(1+r/2)*UA+(r/2)*T0hi*transport_factor;ratio=high/low

 if ratio>full_ratio:raise Unknown('full autonomous MFPT outer interval misses requested TOTAL ratio; structural slack is not only numerical error')
 return {'schema':'well_redistribution_constant_spd_mfpt.v1','dependency_sha256':SOURCE_SHA,'task':{k:fs(v)if type(v)is F else v for k,v in task.items()},'acquisition':info,
 'observable':'E[tau_{Y>=1/2}] from EXACT FULL Gibbs conditioned on Y<=-1/2',
 'actual_full_generator':'beta^-1 d_yy - v_prime*U d_y + beta^-1 trace(M Hess_z) - v*(M grad U) dot grad_z',
 'initialization':'exact full rho_A proportional to 1_{y<=-1/2} exp(-beta*v(y)*U(z)); neither fixed-ray nor approximate total-variation preparation is authenticated',
 'proof_method':'zero-resolvent join with explicit well-redistributed A-current and SEPARATE conditional S-current; no capacity substitution or physical intervention',
 'not_claimed':['projected energy Markov closure','arbitrary initial-law hitting-time mean','fixed-ray initialization equivalence','actual physical generator identification','physical implementation or finite-bit preparation','angular mixing'],
 'basin_mass':interval(ml,mh),'slab_resistance':interval(rl,rh),'parallel_slab_resistance':interval(pl,ph),'mean_hitting_time':interval(low,high),'total_ratio_exact':fs(ratio),
 'source_S_slab_factor_upper':fs(transport_factor),'slab_to_basin_mass_ratio_upper':fs(r),
 'source_A_inverse_per_mass_upper':fs(UA),'source_S_inverse_per_mass_upper':fs(US),
 'upper_source_A_components':{k:fs(v)for k,v in components.items()},'source_cross_AMGM_upper':fs(r*(UA+T0hi*transport_factor)/2),
 'constants':{'a_b':fs(a),'delta':fs(d),'vstar':fs(vstar),'G_b':fs(Gb),'G_1':fs(G1),'G_b_power_upper':fs(Gbhi),'G_1_power_upper':fs(G1hi),'K_upper':fs(K),'global_transport_correction_upper':fs(D_max)},
 'N':N,'T':fs(T),'tail_upper':fs(ii.tail(T)),'precision_bits':P,
 'work':{'scalar_points':len(ii.cache),'integer_power_calls':ii.powers,'fixed_operations':ii.fixed.operations,'largest_guarded_product_bits':ii.fixed.max_guarded_bits,'root_calls':roots.calls,'largest_root_integer_bound_bits':roots.max_bits},'seconds':time.perf_counter()-start}

def verify(raw,certificate,**external_task):
 exp=certify(raw,**external_task)
 if type(certificate)is not dict:raise Unknown('certificate object')
 for k in ['schema','dependency_sha256','task','acquisition','observable','actual_full_generator','initialization','proof_method','not_claimed','total_ratio_exact','source_S_slab_factor_upper','slab_to_basin_mass_ratio_upper','source_A_inverse_per_mass_upper','source_S_inverse_per_mass_upper','upper_source_A_components','source_cross_AMGM_upper','constants','N','T','tail_upper','precision_bits']:
  if not base.same(certificate.get(k),exp[k]):raise Unknown('strict original model/task/proof binding: '+k)
 for k in ['basin_mass','slab_resistance','parallel_slab_resistance','mean_hitting_time']:
  if type(certificate.get(k))is not dict:raise Unknown('interval schema')
  for side in ['lower','upper']:
   if not base.same(certificate[k].get(side),exp[k][side]):raise Unknown('exact recomputed endpoint: '+k)
 return {'status':'PASS','scope':exp['observable'],'actual_mobility_floor':exp['acquisition']['mobility_floor'],'m':exp['acquisition']['m'],'total_ratio_exact':exp['total_ratio_exact'],'physical_membership':'not authenticated'}

def fixture(m,coupling=F(20),mobility=F(1),diagonal=False):
 raw=base.fixture(m,4,coupling,F(0));raw.pop('tangent_program')
 raw['mobility_program']={'kind':'constant_diagonal','entries':[fs(mobility*(i+1))for i in range(m)]} if diagonal else {'kind':'constant_isotropic','value':fs(mobility)}
 return raw

def external_from_record(cert):
 d=dict(cert['task'])
 for k in ['beta','kappa','quad_relative','full_ratio']:d[k]=F(d[k])
 return d

if __name__=='__main__':
 out=[]
 for m,mobility,target,coupling,diagonal in [(128,F(1),F(11,10),F(20),False),(256,F(1),F(103,100),F(20),False),(512,F(1),F(101,100),F(20),False),(512,F(1),F(101,100),F(10**100),True)]:
  made=time.perf_counter();raw=fixture(m,coupling,mobility,diagonal);generation_seconds=time.perf_counter()-made
  raw_bytes=len(json.dumps(raw,sort_keys=True,separators=(',',':')).encode());cert=certify(raw,full_ratio=target)
  row={'fixture':{'m':m,'coupling':fs(coupling),'mobility':fs(mobility),'diagonal':diagonal},'fixture_generation_seconds':generation_seconds,'raw_serialized_bytes':raw_bytes,'certificate':cert};out.append(row)
  Path('results.json').write_text(json.dumps(out,indent=2)+'\n');print(m,cert['mean_hitting_time']['display'],float(F(cert['total_ratio_exact'])),cert['work'],cert['seconds'],flush=True)
