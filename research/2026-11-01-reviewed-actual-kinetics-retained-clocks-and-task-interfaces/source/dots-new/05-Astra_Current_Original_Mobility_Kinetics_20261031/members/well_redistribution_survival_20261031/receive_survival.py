"""Uniform absolute autonomous passage-time CDF certificate, actual constant SPD.
Candidate until the spectral theorem and complete wrapper are independently received.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,importlib.util,json,time
SOURCE=Path(__file__).resolve().parent.parent/'well_redistribution_mfpt_20261031'/'receive_mfpt.py'
SOURCE_SHA='4a4603007fd4e339011d0f8fc8eed6a5ff90f298762b74fd8ef8634e8b1adfa0'
ROOT_PROOF_SHA='7d4d7f61e03860e11e0e550ab850714497acc6f395b5179e4f318a1739434e83'
COROLLARY_SHA='943bd0f5a4b30359ee5d61a5aedd4dd0b66a4e65062a145476727cc72b56f70e'
SEPARATE_SOURCE_SHA='5a98beb1d277777aa03016e6d56b76f29ebe52188c5fe981b0cf95c050dee7f4'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA:raise RuntimeError('well-current MFPT dependency hash mismatch')
spec=importlib.util.spec_from_file_location('well_current_mfpt_for_survival',SOURCE);core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
base=core.base;Unknown=base.Unknown;fs=base.fs;interval=base.enclosure

def certify(raw,*,times,ks_error=F(1,100),query_absolute_width=F(1,50),precision_bits=256,max_queries=1024,max_exp_terms=16384,
 beta=F(1),kappa=F(1),quad_relative=F(1,1000),full_ratio=F(101,100),
 max_dimension=1024,max_terms=100000,max_coefficient_bits=4096,max_exponent_entries=64000000,max_total_coefficient_bits=32000000,max_rational_bits=1000000,
 max_grid=131072,max_points=1000000,max_cutoff=65536,max_precision=16384,max_operations=30000000,max_integer_bits=1000000):
 start=time.perf_counter();args=locals().copy();args.pop('raw');args.pop('start')
 ratkeys=['ks_error','query_absolute_width','beta','kappa','quad_relative','full_ratio']
 for k,v in args.items():
  if k not in ratkeys+['times']:base.strict_int(v,k)
 for k in ratkeys:
  q=base.frac(args[k],k,True)
  if core.bits(q)>max_coefficient_bits:raise Unknown('external task rational bit budget')
 if ks_error>=1 or query_absolute_width>1:raise Unknown('KS error<1 and query width<=1 required')
 if precision_bits<16 or precision_bits>max_precision or 2*precision_bits>max_integer_bits:raise Unknown('additional root/exponential precision budget')
 if type(times)is not list or len(times)>max_queries:raise Unknown('finite external query list/count')
 for t in times:
  base.frac(t,'external query time')
  if t<0 or core.bits(t)>max_coefficient_bits:raise Unknown('nonnegative external query time and bit budget')
 extra=['times','ks_error','query_absolute_width','precision_bits','max_queries','max_exp_terms']
 mean_task={k:v for k,v in args.items()if k not in extra}
 mean=core.certify(raw,**mean_task)
 ml,mh=F(mean['basin_mass']['lower']),F(mean['basin_mass']['upper']);rl,rh=F(mean['slab_resistance']['lower']),F(mean['slab_resistance']['upper'])
 rho=F(mean['slab_to_basin_mass_ratio_upper'])
 bbar=F(mean['source_A_inverse_per_mass_upper'])/(beta*ml*rl);cbar=F(mean['source_S_slab_factor_upper'])
 eps=(1+rho)*(bbar+rho*cbar)-1
 if eps<0:raise Unknown('source spectral upper error must be nonnegative')
 roots=core.Roots(precision_bits,max_integer_bits);init_error=rho+roots.upper(rho*(1+rho))
 kl=1/(beta*mh*rh);kh=1/(beta*ml*rl);kstar=(kl+kh)/2
 rate_error=F(3,16)*(kh/kl-1);delta=eps+init_error+rate_error
 if delta>ks_error:raise Unknown('full all-time KS bound misses external request; structural and numerical errors both retained')
 remaining=max_operations-mean['work']['fixed_operations']
 if remaining<0:raise Unknown('shared total fixed-operation budget')
 fixed=base.Fixed(precision_bits,remaining,max_integer_bits,max_exp_terms,1);queries=[]
 for t in times:
  if t==0:lo=hi=F(0)
  else:
   el,eh=fixed.expminus(kstar*t);lo=max(F(0),1-F(eh,fixed.S)-delta);hi=min(F(1),1-F(el,fixed.S)+delta)
  if hi-lo>query_absolute_width:raise Unknown('outward actual-CDF query misses external absolute-width request')
  queries.append({'time':fs(t),'cdf':interval(lo,hi)})
 task={k:fs(v)if type(v)is F else [fs(t)for t in v]if k=='times' else v for k,v in args.items()}
 return {'schema':'well_redistributed_constant_spd_passage_cdf.v1','dependency_sha256':SOURCE_SHA,'root_theorem_sha256':ROOT_PROOF_SHA,'finite_rate_corollary_sha256':COROLLARY_SHA,'separate_source_theorem_sha256':SEPARATE_SOURCE_SHA,'task':task,
 'observable':'CDF of tau_{Y>=1/2} from EXACT FULL Gibbs conditioned on Y<=-1/2, for the original constant-SPD Langevin model',
 'initialization':mean['initialization'],'actual_full_generator':mean['actual_full_generator'],
 'uniform_statement':'For every real t>=0, abs(P[tau_B<=t]-(1-exp(-reference_exponential_rate*t))) <= uniform_KS_error_upper',
 'not_claimed':['relative extreme-tail accuracy','exact exponential waiting times','exponential moments','arbitrary-start or fixed-ray initialization','physical parameter/preparation authentication','energy Markov closure','global spectral gap'],
 'mean_certificate':mean,'exact_rate_enclosure':interval(kl,kh),'reference_exponential_rate':fs(kstar),'spectral_error_upper':fs(eps),'source_A_normalized_inverse_upper':fs(bbar),'source_S_slab_factor_upper':fs(cbar),'slab_mass_ratio_upper':fs(rho),
 'initial_law_comparison_error_upper':fs(init_error),'finite_rate_error_upper':fs(rate_error),'uniform_KS_error_upper':fs(delta),'queries':queries,
 'work':{'extra_root_calls':roots.calls,'largest_extra_root_integer_bound_bits':roots.max_bits,'extra_fixed_operations':fixed.operations,'total_fixed_operations':mean['work']['fixed_operations']+fixed.operations,'extra_exponential_calls':fixed.exp_calls,'extra_exp_terms':fixed.exp_terms,'largest_extra_guarded_product_bits':fixed.max_guarded_bits},'seconds':time.perf_counter()-start}

def proof_record(record,depth=0):
 if type(record)is not dict:raise Unknown('certificate object')
 d=dict(record);d.pop('seconds',None);d.pop('work',None)
 for k in ['basin_mass','slab_resistance','parallel_slab_resistance','mean_hitting_time','exact_rate_enclosure']:
  if k in d:
   if type(d[k])is not dict:raise Unknown('interval object')
   d[k]=dict(d[k]);d[k].pop('display',None)
 if 'mean_certificate'in d:
  if depth!=0:raise Unknown('unexpected recursive nested mean certificate')
  d['mean_certificate']=proof_record(d['mean_certificate'],1)
 if 'queries'in d:
  if type(d['queries'])is not list:raise Unknown('query records')
  qs=[]
  for q in d['queries']:
   if type(q)is not dict or type(q.get('cdf'))is not dict:raise Unknown('query interval schema')
   q=dict(q);q['cdf']=dict(q['cdf']);q['cdf'].pop('display',None);qs.append(q)
  d['queries']=qs
 return d

def verify(raw,certificate,**external_task):
 expected=certify(raw,**external_task)
 if not base.same(proof_record(certificate),proof_record(expected)):raise Unknown('strict actual model, original task, spectral/rate/init and exact endpoint conjunction')
 return {'status':'PASS','scope':expected['observable'],'uniform_KS_error_upper':expected['uniform_KS_error_upper'],'reference_exponential_rate':expected['reference_exponential_rate'],'queries':len(expected['queries']),'physical_membership':'not authenticated'}

def fixture(m=512,coupling=F(20),mobility=F(1),diagonal=False):return core.fixture(m,coupling,mobility,diagonal)

def original_task(m):
 if m==128:return {'times':[F(0),F(10**8),F(3*10**8),F(10**9)],'ks_error':F(1,20),'query_absolute_width':F(1,10),'full_ratio':F(11,10)}
 if m==256:return {'times':[F(0),F(10**17),F(4*10**17),F(10**18),F(10**19)],'ks_error':F(1,50),'query_absolute_width':F(1,25),'full_ratio':F(103,100)}
 if m==512:return {'times':[F(0),F(10**36),F(4*10**36),F(10**37),F(10**38)]}
 raise Unknown('no literal production task for this dimension')

if __name__=='__main__':
 rows=[]
 for m,coupling,diagonal in [(128,F(20),False),(256,F(20),False),(512,F(20),False),(512,F(10**100),True)]:
  t=time.perf_counter();raw=fixture(m,coupling,diagonal=diagonal);generation=time.perf_counter()-t
  cert=certify(raw,**original_task(m));rows.append({'fixture':{'m':m,'coupling':fs(coupling),'mobility':'1','diagonal':diagonal},'fixture_generation_seconds':generation,'raw_serialized_bytes':len(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()),'certificate':cert})
  Path('results.json').write_text(json.dumps(rows,indent=2)+'\n')
  print(m,float(F(cert['uniform_KS_error_upper'])),[(x['time'],x['cdf']['display'])for x in cert['queries']],cert['work'],cert['seconds'],flush=True)
