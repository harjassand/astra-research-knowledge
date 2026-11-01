"""Retained-state finite records and hysteretic time-jitter, original model.
No restart, no assumed angular equilibration, no continuous timestamp-TV claim.
Candidate until this new global current and full consumer are independently received.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,importlib.util,json,time
SOURCE=Path(__file__).resolve().parent.parent/'well_redistribution_mfpt_20261031'/'receive_mfpt.py'
SOURCE_SHA='4a4603007fd4e339011d0f8fc8eed6a5ff90f298762b74fd8ef8634e8b1adfa0'
PROOF_SHA='4a8110be17507c8f0552a6ff5553e7b8f5caecfc94808900a4a05fda31cc1892'
COROLLARY_SHA='a71d9b0aa28300d6f23783dc9a045ec87a62ecc32eea66820b59ad1c9a30ed86'
SHARP_VECTOR_SHA='8da465ed3817a2e5cf0088cd0efba23e056a148422bf5a3120b96606a960a403'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA:raise RuntimeError('accepted well-current dependency hash mismatch')
spec=importlib.util.spec_from_file_location('well_current_for_retained_clock',SOURCE);core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
base=core.base;Unknown=base.Unknown;fs=base.fs;interval=base.enclosure
RATKEYS=['x','path_error','query_absolute_width','beta','kappa','quad_relative','full_ratio']

def count_event(fixed,q,n,lower,upper):
 """Capped finite-state interval DP. Counts OBSERVED label changes only."""
 S=fixed.S;stay=(S-q[1],S-q[0]);overflow=upper+1
 dp=[(0,0)]*(overflow+1);dp[0]=(S,S);updates=0
 for i in range(n):
  out=[(0,0)]*(overflow+1)
  for j in range(min(i,overflow)+1):
   updates+=1
   if j==overflow:
    out[j]=(out[j][0]+dp[j][0],out[j][1]+dp[j][1]);continue
   a=fixed.mul(dp[j],stay);b=fixed.mul(dp[j],q)
   out[j]=(out[j][0]+a[0],out[j][1]+a[1]);out[j+1]=(out[j+1][0]+b[0],out[j+1][1]+b[1])
  dp=[(max(0,a),min(S,b))for a,b in out]
 return (max(0,sum(dp[j][0]for j in range(lower,upper+1))),min(S,sum(dp[j][1]for j in range(lower,upper+1)))),updates

def certify(raw,*,n,x,event_lower,event_upper,path_error=F(3,20),jitter_error=None,query_absolute_width=F(3,10),
 precision_bits=256,max_record_steps=1024,max_dp_updates=1000000,max_exp_terms=16384,
 beta=F(1),kappa=F(1),quad_relative=F(1,1000),full_ratio=F(2),
 max_dimension=1024,max_terms=100000,max_coefficient_bits=4096,max_exponent_entries=64000000,max_total_coefficient_bits=32000000,max_rational_bits=1000000,
 max_grid=131072,max_points=1000000,max_cutoff=65536,max_precision=16384,max_operations=30000000,max_integer_bits=1000000):
 start=time.perf_counter();args=locals().copy();args.pop('raw');args.pop('start')
 for k,v in args.items():
  if k not in RATKEYS+['jitter_error','event_lower','event_upper']:base.strict_int(v,k)
 for k in ['event_lower','event_upper']:
  if type(args[k])is not int or args[k]<0:raise Unknown('nonnegative strict event-count integer')
 if not 0<=event_lower<=event_upper<=n:raise Unknown('ordered event count within record length')
 if n>max_record_steps or n*(event_upper+2)>max_dp_updates:raise Unknown('finite record/state-DP budget before allocation')
 for k in RATKEYS+(['jitter_error']if jitter_error is not None else []):
  q=base.frac(args[k],k,True)
  if core.bits(q)>max_coefficient_bits:raise Unknown('external task rational bit budget')
 if path_error>=1 or query_absolute_width>1 or(jitter_error is not None and jitter_error>=1):raise Unknown('nonvacuous external path/jitter error and query width<=1')
 if precision_bits<16 or precision_bits>max_precision or 2*precision_bits>max_integer_bits:raise Unknown('extra root/exponential precision budget')
 extra=['n','x','event_lower','event_upper','path_error','jitter_error','query_absolute_width','precision_bits','max_record_steps','max_dp_updates','max_exp_terms']
 mean=core.certify(raw,**{k:v for k,v in args.items()if k not in extra})
 ml,mh=F(mean['basin_mass']['lower']),F(mean['basin_mass']['upper']);rl,rh=F(mean['slab_resistance']['lower']),F(mean['slab_resistance']['upper'])
 comps={k:F(v)for k,v in mean['upper_source_A_components'].items()}
 # The full odd source has ONCE the slab and TWICE each well: not 2*B_A.
 global_per_mass=comps['parallel_slab']+2*sum((v for k,v in comps.items()if k!='parallel_slab'),F(0))
 bf=global_per_mass/(beta*ml*rl);eta=F(mean['slab_to_basin_mass_ratio_upper']);Cs1=F(mean['source_S_slab_factor_upper'])
 eps=(1+eta/2)*(bf+eta*Cs1/2)-1
 if eps<0:raise Unknown('nonnegative global odd-source moment error')
 s=eta/(2+eta);C=2+eta
 roots=core.Roots(precision_bits,max_integer_bits)
 def root(q):return F(0)if q==0 else roots.upper(q)
 G=root(eps*(1+eps))/2+3*eps/8
 ll=1/(beta*mh*rh);lh=1/(beta*ml*rl);rate=(ll+lh)/2;d=(lh-ll)/(lh+ll)
 rate_error=3*d/(8*(1-d));delta=G+2*root(s)+rate_error
 remaining=max_operations-mean['work']['fixed_operations']
 if remaining<0:raise Unknown('shared total fixed-operation budget')
 fixed=base.Fixed(precision_bits,remaining,max_integer_bits,max_exp_terms,1)
 r4=fixed.expminus(4*x);den=1-F(r4[1],fixed.S)
 if den<=0:raise Unknown('positive short-lag KL denominator unresolved at paid precision')
 tv_sign=root(C*n*delta*delta/(2*den));tv=tv_sign+n*eta
 jitter=tv+(C+1)*n*x*x/2+C*n*eps/4+F(3,2)*n*eta+C*n*d*x
 if tv>path_error:raise Unknown('entire retained-state sampled-record TV misses external request; no reset or precision-only promise')
 if jitter_error is not None and jitter>jitter_error:raise Unknown('continuous hysteretic jump-jitter failure bound misses external request')
 r2=fixed.expminus(2*x);q=((fixed.S-r2[1])//2,(fixed.S-r2[0]+1)//2)
 (cl,ch),updates=count_event(fixed,q,n,event_lower,event_upper)
 clo,chi=F(cl,fixed.S),F(ch,fixed.S);alo=max(F(0),clo-tv);ahi=min(F(1),chi+tv)
 if ahi-alo>query_absolute_width:raise Unknown('actual finite-record event outer interval misses external width')
 task={k:fs(v)if type(v)is F else v for k,v in args.items()}
 return {'schema':'retained_state_quartic_clock.v1','dependency_sha256':SOURCE_SHA,'global_proof_sha256':PROOF_SHA,'finite_rate_corollary_sha256':COROLLARY_SHA,'sharp_vector_sha256':SHARP_VECTOR_SHA,'task':task,
 'observable':'same continuing hysteretic last-visited-A/B process, started ONCE from EXACT FULL Gibbs conditioned on A',
 'actual_full_generator':mean['actual_full_generator'],'initialization':mean['initialization'],
 'not_claimed':['reset or angular rethermalization','exact finite-dimension iid clocks','continuous jump-time total variation','continuous raw sign process','arbitrary adaptive observations or controls','physical model/preparation/event-detection authentication','relative rare-transcript error','unbounded moment control'],
 'mean_engine_certificate':mean,'global_odd_source_inverse_per_mass_upper':fs(global_per_mass),'global_odd_normalized_inverse_upper':fs(bf),'global_spectral_error_upper':fs(eps),'slab_to_basin_mass_ratio_upper':fs(eta),'stationary_slab_probability_upper':fs(s),'initial_density_upper':fs(C),
 'exact_flip_rate_enclosure':interval(ll,lh),'reference_flip_rate':fs(rate),'reference_correlation_decay_rate':fs(2*rate),'relative_rate_uncertainty_upper':fs(d),'finite_rate_vector_error_upper':fs(rate_error),
 'sharp_trial_vector_error_upper':fs(G),'sign_vector_error_upper':fs(delta),'record_TV_error_upper':fs(tv),'continuous_jitter_failure_unclipped_upper':fs(jitter),'continuous_jitter_failure_upper':fs(min(F(1),jitter)),
 'physical_grid_spacing':fs(x/rate),'physical_horizon':fs(n*x/rate),'jump_time_tolerance':fs(x/rate),
 'comparison_flip_probability':interval(F(q[0],fixed.S),F(q[1],fixed.S)),
 'event':{'kind':'sampled_label_change_count_between_inclusive','lower_count':event_lower,'upper_count':event_upper,'comparison_probability':interval(clo,chi),'actual_probability':interval(alo,ahi)},
 'work':{'extra_root_calls':roots.calls,'largest_extra_root_integer_bound_bits':roots.max_bits,'extra_fixed_operations':fixed.operations,'total_fixed_operations':mean['work']['fixed_operations']+fixed.operations,'extra_exponential_calls':fixed.exp_calls,'extra_exp_terms':fixed.exp_terms,'largest_extra_guarded_product_bits':fixed.max_guarded_bits,'dp_updates':updates,'dp_states':event_upper+2},'seconds':time.perf_counter()-start}

def proof_record(obj):
 """Only named non-proof timing, arithmetic counters and float displays omitted."""
 if type(obj)is dict:return {k:proof_record(v)for k,v in obj.items()if k not in ['seconds','work','display']}
 if type(obj)is list:return [proof_record(v)for v in obj]
 return obj

def verify(raw,certificate,**external_task):
 expected=certify(raw,**external_task)
 if type(certificate)is not dict or not base.same(proof_record(certificate),proof_record(expected)):raise Unknown('strict model, once-only initial law, global current, external grid/event/error and exact endpoint conjunction')
 return {'status':'PASS','scope':expected['observable'],'record_TV_error_upper':expected['record_TV_error_upper'],'continuous_jitter_failure_upper':expected['continuous_jitter_failure_upper'],'physical_membership':'not authenticated'}

def external_from_record(cert):
 args=dict(cert['task'])
 for k in RATKEYS+(['jitter_error']if args['jitter_error']is not None else []):args[k]=F(args[k])
 return args

def fixture(m=512,coupling=F(20),mobility=F(1),diagonal=False):return core.fixture(m,coupling,mobility,diagonal)

if __name__=='__main__':
 raw=fixture();rows=[]
 for label,task in [('ten_mean_scale_observations',dict(n=10,x=F(1),event_lower=4,event_upper=6)),('one_horizon_hysteretic_jitter',dict(n=8,x=F(1,8),event_lower=0,event_upper=2,path_error=F(1,5),jitter_error=F(9,20),query_absolute_width=F(2,5)))]:
  c=certify(raw,**task);rows.append({'name':label,'raw_serialized_bytes':len(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()),'certificate':c})
  Path('results.json').write_text(json.dumps(rows,indent=2)+'\n')
  print(label,'TV',base.show(F(c['record_TV_error_upper'])),'jitter',base.show(F(c['continuous_jitter_failure_upper'])),'event',c['event']['actual_probability']['display'],'seconds',c['seconds'],flush=True)
