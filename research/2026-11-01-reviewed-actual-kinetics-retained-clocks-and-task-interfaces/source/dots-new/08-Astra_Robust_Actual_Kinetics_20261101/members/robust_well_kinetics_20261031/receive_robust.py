"""Candidate finite robust full-GibbsA kinetics for an exact atom-weight family.
No actual member, conditional law or angular relaxation is silently reconstructed.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,hashlib,json,time
SOURCE=Path(__file__).resolve().parent.parent/'well_redistribution_mfpt_20261031'/'receive_mfpt.py'
SOURCE_SHA='4a4603007fd4e339011d0f8fc8eed6a5ff90f298762b74fd8ef8634e8b1adfa0'
PROOF_SHA='cb68b2f121f89e2553b4f6330dee2b60ae185309b715491fe4ec487cac7b5366'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA:raise RuntimeError('accepted well-current runtime dependency hash mismatch')
spec=importlib.util.spec_from_file_location('well_current_for_robust_family',SOURCE);well=importlib.util.module_from_spec(spec);spec.loader.exec_module(well)
base=well.base;Unknown=base.Unknown;fs=base.fs;interval=base.enclosure;Roots=well.Roots;bits=well.bits

def acquire(raw,**budgets):
 if type(raw)is not dict or set(raw)!={'dimension','energy_terms','mobility_program','uncertainty_program'}:raise Unknown('complete actual uncertain model family required')
 u=raw['uncertainty_program'];ts=raw['energy_terms']
 if type(ts)is not list or len(ts)>budgets['max_terms']:raise Unknown('finite complete energy atom count')
 if type(u)is not dict or set(u)!={'kind','ranges'}or u['kind']!='fixed_independent_atom_weights':raise Unknown('global fixed atom-weight family grammar')
 rs=u['ranges']
 if type(rs)is not list or len(rs)!=len(ts):raise Unknown('one complete global weight interval for every atom')
 cb=0;points=0
 for r in rs:
  if type(r)is not list or len(r)!=2:raise Unknown('closed atom-weight interval schema')
  lo,hi=(base.raw_frac(x,budgets['max_coefficient_bits'])for x in r)
  if not 0<=lo<=hi<=1:raise Unknown('global 0<=V<=U coefficient certificate')
  cb+=sum(x.numerator.bit_length()+x.denominator.bit_length()for x in (lo,hi));points+=lo==hi
  if cb>budgets['max_total_coefficient_bits']:raise Unknown('total uncertainty coefficient bit budget')
 nominal={k:raw[k]for k in ['dimension','energy_terms','mobility_program']}
 info,alpha,mu,dmin=well.acquire(nominal,**budgets)
 if cb+info['coefficient_bits_read']+info['mobility_coefficient_bits_read']>budgets['max_total_coefficient_bits']:raise Unknown('shared energy+mobility+uncertainty coefficient bit budget')
 info['nominal_raw_sha256']=info['raw_sha256'];info['raw_sha256']=base.canonical_hash(raw)
 info.update({'uncertain_atom_intervals_read':len(rs),'uncertainty_coefficient_bits_read':cb,'point_atom_weights':points,'unidentified_atom_weights':len(rs)-points,
 'family':'all fixed real atom weights in their declared intervals; F=vU+defect*gV, 0<=V<=U globally','physical_membership':'not authenticated'})
 return info,alpha,mu,dmin

class Scalar(well.Scalar):
 def __init__(self,*args,defect,**kw):super().__init__(*args,**kw);self.defect=defect
 def point(self,y,kind):
  if kind not in ['qb','re']:return super().point(y,kind)
  if (kind=='qb'and y<F(1,2))or(kind=='re'and not 0<=y<=F(1,2)):raise Unknown('robust scalar profile domain')
  key=(y,kind)
  if key in self.cache:return self.cache[key]
  if len(self.cache)>=self.max_points:raise Unknown('shared total robust scalar-point budget')
  x=y*y;v=1+self.kappa*(1-x)**2;g=x*(1-x)**2/(1+x);b=v+self.defect*g
  if kind=='qb':q=1/b
  else:
   vstar=1+self.kappa;den=2*vstar-b
   if den<=0:raise Unknown('positive robust parallel denominator required')
   q=vstar*vstar/den
  z=self.power(q,self.alpha);self.cache[key]=z;return z
 def integrate(self,a,b,N,kind):
  if kind not in ['qb','re']:return super().integrate(a,b,N,kind)
  valid=(F(1,2)<=a<b<=1 or 1<=a<b)if kind=='qb'else 0<=a<b<=F(1,2)
  if not valid or type(N)is not int or N<=0:raise Unknown('proved monotone robust integration segment')
  h=(b-a)/N;prev=self.point(a,kind);lo=hi=0
  for j in range(1,N+1):
   cur=self.point(a+j*h,kind);lo+=min(prev[0],cur[0]);hi+=max(prev[1],cur[1]);prev=cur
  return h*F(lo,self.S),h*F(hi,self.S)

def certify(raw,*,defect=F(1,1000),beta=F(1),kappa=F(1),quad_relative=F(1,1000),full_ratio=F(101,100),ks_error=F(1,100),times=None,query_absolute_width=F(1,50),max_queries=1024,max_exp_terms=16384,
 max_dimension=1024,max_terms=100000,max_coefficient_bits=4096,max_exponent_entries=64000000,max_total_coefficient_bits=32000000,max_rational_bits=1000000,
 max_grid=131072,max_points=1000000,max_cutoff=65536,max_precision=16384,max_operations=30000000,max_integer_bits=1000000):
 if times is None:times=[]
 start=time.perf_counter();task=locals().copy();task.pop('raw');task.pop('start')
 rats=['defect','beta','kappa','quad_relative','full_ratio','ks_error','query_absolute_width']
 for k,v in task.items():
  if k not in rats+['times']:base.strict_int(v,k)
 for k in rats:
  v=base.frac(task[k],k,k!='defect')
  if bits(v)>max_coefficient_bits:raise Unknown('task exact rational bit budget')
 if not 0<=defect<kappa:raise Unknown('received nonnegative defect strictly below kappa')
 if quad_relative>=1 or full_ratio<=1 or ks_error>=1 or query_absolute_width>1:raise Unknown('meaningful original total accuracy controls')
 if max_grid<64 or max_cutoff<2:raise Unknown('initial scalar grid/cutoff budget')
 if type(times)is not list or len(times)>max_queries:raise Unknown('finite complete query list/count')
 for t in times:
  base.frac(t,'query time')
  if t<0 or bits(t)>max_coefficient_bits:raise Unknown('nonnegative exact query time bit budget')
 keys=['max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits']
 info,alpha,mu,dmin=acquire(raw,**{k:task[k]for k in keys})
 P=max(192,alpha*(bits(kappa)+bits(defect)+2)+128)
 if P>max_precision or 2*P>max_integer_bits:raise Unknown('allocated robust scalar/root precision budget')
 roots=Roots(P,max_integer_bits);a=1+F(9,16)*kappa;star=1+kappa;d=F(1,alpha)
 cs=1+kappa*roots.upper(1/(beta*dmin*a**3))/(2*mu)
 dmax=4*alpha*max(kappa,F(1))*roots.upper(1/(beta*dmin))/mu
 K=F(alpha)*roots.upper(1/(beta*dmin))/(8*mu)
 ii=Scalar(alpha,kappa,P,max_points,max_operations,max_integer_bits,defect=defect)
 seed=ii.integrate(F(1),F(5,4),32,'qb')[0]
 if seed<=0:raise Unknown('positive lower-density basin seed unresolved')
 T=F(2)
 while ii.tail(T)>quad_relative*seed/8:
  T*=2
  if T>max_cutoff:raise Unknown('full infinite-tail cutoff budget')
 N=64
 while True:
  if N>max_grid:raise Unknown('robust monotone quadrature grid budget')
  masses=[]
  for kind in ['q','qb']:
   lo,hi=ii.integrate(F(1,2),F(1),N,kind);left=F(1)
   while left<T:
    l,h=ii.integrate(left,2*left,N,kind);lo+=l;hi+=h;left*=2
   hi+=ii.tail(T);masses.append((lo,hi))
  ml,mh=masses[0];bl,bh=masses[1]
  rl,rh=ii.integrate(F(0),F(1,2),N,'r');rl*=2;rh*=2
  el,eh=ii.integrate(F(0),F(1,2),N,'re');el*=2;eh*=2
  if min(ml,bl,rl,el)>0 and mh*rh<=(1+quad_relative)*ml*rl and bh*rh<=(1+quad_relative)*bl*rl and eh<=(1+quad_relative)*el:break
  N*=2
 L=1/(1-defect/kappa);lp=ii.power(L,alpha);H=F(lp[1],ii.S)*roots.upper(L)
 Gb=star*star/(2*star-a);G1=star*star/(2*star-1)
 gb=F(ii.power(Gb,alpha)[1],ii.S);g1=F(ii.power(G1,alpha)[1],ii.S);su=F(ii.power(1/a,alpha)[1],ii.S)
 rest={'near':mh*mh*(F(1,2)+d)*gb,'middle':star*star*g1/(128*kappa*kappa*(alpha-1)**2*d*d),'vertical':K*kappa*kappa*g1,'far':(1+dmax)/(16*kappa*kappa*(alpha-1)**2)}
 BA=beta*(mh*mh*eh+H*sum(rest.values(),F(0)));BS=H*beta*su*su*rh*cs
 eta=su/ml;rho=su/bl
 low=beta*bl*rl;high=((1+eta/2)*BA+(eta/2)*H*beta*mh*mh*rh*cs)/bl
 if high/low>full_ratio:raise Unknown('actual robust mean misses requested TOTAL ratio; shape uncertainty is not numerical error')
 eps=(1+eta)*(BA+eta*H*beta*mh*mh*rh*cs)/(beta*rl*bl*bl)-1
 if eps<0:raise Unknown('robust spectral defect must be nonnegative')
 init=rho+roots.upper(rho*(1+rho));kl=1/(beta*bh*rh);kh=1/(beta*bl*rl);km=(kl+kh)/2;rate_error=F(3,16)*(kh/kl-1);error=eps+init+rate_error
 if error>ks_error:raise Unknown('actual robust all-time KS bound misses original tolerance')
 fixed=base.Fixed(P,max_operations-ii.fixed.operations,max_integer_bits,max_exp_terms,1);queries=[]
 for t in times:
  if t==0:lo=hi=F(0)
  else:
   l,h=fixed.expminus(km*t);lo=max(F(0),1-F(h,fixed.S)-error);hi=min(F(1),1-F(l,fixed.S)+error)
  if hi-lo>query_absolute_width:raise Unknown('actual robust CDF query absolute width missed')
  queries.append({'time':fs(t),'cdf':interval(lo,hi)})
 return {'schema':'localized_uncertain_full_gibbs_passage.v1','dependency_sha256':SOURCE_SHA,'proof_sha256':PROOF_SHA,
 'task':{k:fs(v)if type(v)is F else [fs(t)for t in v]if k=='times'else v for k,v in task.items()},'acquisition':info,
 'observable':'mean and all-time absolute CDF of tau_{Y>=1/2}, uniformly over every fixed admitted atom-weight choice, from its OWN EXACT FULL Gibbs conditioned on Y<=-1/2',
 'actual_generator_family':'beta^-1 d_yy - F_y d_y + beta^-1 trace(M Hess_z) - (M grad_z F) dot grad_z; F=vU+defect*gV',
 'not_claimed':['identified actual atom weights','physical global envelope acquisition','nominal Gibbs or fixed-ray initialization','finite-bit preparation','time-varying/adaptive perturbations','relative extreme-tail or exponential-moment accuracy','capacity-to-mean substitution'],
 'nominal_basin_mass':interval(ml,mh),'lower_density_basin_mass':interval(bl,bh),'nominal_resistance':interval(rl,rh),'robust_slab_resistance':interval(el,eh),
 'mean_hitting_time':interval(low,high),'total_mean_ratio':fs(high/low),'reference_rate_enclosure':interval(kl,kh),'reference_exponential_rate':fs(km),
 'spectral_error_upper':fs(eps),'initial_law_error_upper':fs(init),'finite_rate_error_upper':fs(rate_error),'uniform_KS_error_upper':fs(error),
 'source_A_upper':fs(BA),'source_S_upper':fs(BS),'nominal_rest_components_upper':{k:fs(v)for k,v in rest.items()},
 'constants':{'density_price_factor_upper':fs(H),'L':fs(L),'S_upper':fs(su),'eta_v_upper':fs(eta),'rho_actual_upper':fs(rho),'source_S_nominal_factor_upper':fs(cs),'K_upper':fs(K),'Dmax_upper':fs(dmax)},
 'N':N,'T':fs(T),'tail_upper':fs(ii.tail(T)),'precision_bits':P,'queries':queries,
 'work':{'scalar_points':len(ii.cache),'integer_power_calls':ii.powers,'scalar_fixed_operations':ii.fixed.operations,'query_fixed_operations':fixed.operations,'total_fixed_operations':ii.fixed.operations+fixed.operations,'largest_scalar_product_bound_bits':ii.fixed.max_guarded_bits,'largest_query_product_bound_bits':fixed.max_guarded_bits,'root_calls':roots.calls,'largest_root_integer_bound_bits':roots.max_bits,'exp_calls':fixed.exp_calls,'exp_terms':fixed.exp_terms},'seconds':time.perf_counter()-start}

def proof_record(c):
 if type(c)is not dict:raise Unknown('certificate object')
 d=dict(c);d.pop('work',None);d.pop('seconds',None)
 for key in ['nominal_basin_mass','lower_density_basin_mass','nominal_resistance','robust_slab_resistance','mean_hitting_time','reference_rate_enclosure']:
  if type(d.get(key))is not dict:raise Unknown('exact interval schema')
  d[key]=dict(d[key]);d[key].pop('display',None)
 if type(d.get('queries'))is not list:raise Unknown('query schema')
 out=[]
 for q in d['queries']:
  if type(q)is not dict or type(q.get('cdf'))is not dict:raise Unknown('query interval schema')
  r=dict(q);r['cdf']=dict(r['cdf']);r['cdf'].pop('display',None);out.append(r)
 d['queries']=out;return d

def verify(raw,cert,**original_task):
 expected=certify(raw,**original_task)
 if not base.same(proof_record(cert),proof_record(expected)):raise Unknown('full actual family, original task, robust source/initial-law/rate and exact endpoint conjunction')
 return {'status':'PASS','scope':expected['observable'],'total_mean_ratio':expected['total_mean_ratio'],'uniform_KS_error_upper':expected['uniform_KS_error_upper'],'physical_membership':'not authenticated'}

def fixture(m=512,coupling=F(20),diagonal=False):
 raw=well.fixture(m,coupling,F(1),diagonal);raw['uncertainty_program']={'kind':'fixed_independent_atom_weights','ranges':[['0','1']for _ in raw['energy_terms']]};return raw

if __name__=='__main__':
 rows=[]
 for e,coupling,diag in [(F(0),F(20),False),(F(1,1000),F(20),False),(F(1,1000),F(10**100),True)]:
  raw=fixture(512,coupling,diag);times=[F(0),F(10**36),F(4*10**36),F(10**37),F(10**38)]
  c=certify(raw,defect=e,times=times);rows.append({'fixture':{'m':512,'coupling':fs(coupling),'diagonal':diag},'original_defect':fs(e),'certificate':c})
  Path('results.json').write_text(json.dumps(rows,indent=2)+'\n');print(fs(e),float(F(c['total_mean_ratio'])),float(F(c['uniform_KS_error_upper'])),c['work'],c['seconds'],flush=True)
