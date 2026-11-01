"""Complete candidate matched trial/current receiving on a literal PHYSICAL grid.
The earlier 15% clock service remains separately frozen and accepted.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
import positive_integrals as p
import acquire_derivative as ad
from shifted_current import Shifted
base=p.base;Unknown=p.Unknown;fs=p.fs;interval=base.enclosure;core=p.old.core
RATKEYS=['physical_spacing','path_error','query_absolute_width','beta','kappa','quad_relative','full_ratio','L','T']
PROOF_SHA='3828b8fde54e0774e2ef635c1f6c32cdd362d2d826a21d9c98000166fd963d8c'

def certify(raw,*,n,physical_spacing,event_lower,event_upper,path_error=F(1,10),query_absolute_width=F(1,5),jitter_error=None,
 Nt=1024,Ny=256,L=F(32),T=F(400),precision_bits=512,max_energy_bins=16384,max_y_cells=1024,max_integral_nodes=2000000,
 max_record_steps=1024,max_dp_updates=1000000,max_exp_terms=16384,
 beta=F(1),kappa=F(1),quad_relative=F(1,4000),full_ratio=F(2),
 max_dimension=1024,max_terms=100000,max_coefficient_bits=4096,max_exponent_entries=64000000,max_total_coefficient_bits=32000000,max_rational_bits=1000000,
 max_grid=131072,max_points=1000000,max_cutoff=65536,max_precision=16384,max_operations=30000000,max_integer_bits=1000000):
 start=time.perf_counter();args=locals().copy();args.pop('raw');args.pop('start')
 for k,v in args.items():
  if k not in RATKEYS+['jitter_error','event_lower','event_upper']:base.strict_int(v,k)
 for k in ['event_lower','event_upper']:
  if type(args[k])is not int or args[k]<0:raise Unknown('strict nonnegative count-event integer')
 if not 0<=event_lower<=event_upper<=n:raise Unknown('ordered count-event range within record length')
 if n>max_record_steps or n*(event_upper+2)>max_dp_updates:raise Unknown('finite record/DP allocation budget')
 for k in RATKEYS+(['jitter_error']if jitter_error is not None else []):
  z=base.frac(args[k],k,k!='L')
  if z<0 or core.bits(z)>max_coefficient_bits:raise Unknown('nonnegative exact external rational bit budget')
 if L>=T or path_error>=1 or query_absolute_width>1 or(jitter_error is not None and jitter_error>=1):raise Unknown('nonvacuous probability/window receiving conjunction')
 if Nt>max_energy_bins or Ny>max_y_cells or (Nt+1)*(Ny+1)>max_integral_nodes:raise Unknown('finite positive-grid resource preflight')
 if precision_bits<32 or precision_bits>max_precision or 2*precision_bits>max_integer_bits:raise Unknown('new fixed precision preallocation budget')
 if quad_relative>=1 or full_ratio<=1:raise Unknown('inherited scalar task conjunction')
 budgetkeys=['max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits']
 canonical,acq,H,dmin,alpha=ad.acquire(raw,**{k:args[k]for k in budgetkeys})
 vs=1+kappa;vb=1+F(9,16)*kappa;abar=vs*(1-F(1,2*alpha))
 if not vb<=abar<=vs:raise Unknown('shifted barrier parameter outside explicitly proved current family')
 scalar_keys=budgetkeys+['beta','kappa','quad_relative','full_ratio','max_grid','max_points','max_cutoff','max_precision','max_operations','max_integer_bits']
 mean=core.certify(canonical,**{k:args[k]for k in scalar_keys})
 Ml,Mh=F(mean['basin_mass']['lower']),F(mean['basin_mass']['upper']);used=mean['work']['fixed_operations'];remaining=max_operations-used
 point_remaining=max_points-mean['work']['scalar_points']
 if remaining<=0 or point_remaining<=0:raise Unknown('shared scalar work/point budget before shifted current')
 ii=Shifted(alpha,kappa,precision_bits,point_remaining,remaining,max_integer_bits,abar=abar);jl,jh=ii.slab(mean['N']);used+=ii.fixed.operations
 if used>=max_operations:raise Unknown('shared fixed-product budget before primal price')
 price=p.Price(alpha,beta,kappa,H,dmin,Nt=Nt,Ny=Ny,L=L,T=T,precision_bits=precision_bits,max_nodes=max_integral_nodes,max_operations=max_operations-used,max_integer_bits=max_integer_bits,max_exp_terms=max_exp_terms,max_rational_bits=max_rational_bits).run()
 used+=price['work']['fixed_operations'];Pu=price['P_total_upper']
 # These exact rational powers are separately guarded and recorded; they are
 # not silently counted as one of the fixed-product counters above.
 exact_power_calls=0;exact_power_bound=0
 def power(q,k):
  nonlocal exact_power_calls,exact_power_bound
  size=core.bits(q)*max(1,k);exact_power_bound=max(exact_power_bound,size)
  if size>max_integer_bits:raise Unknown('exact rational normalization-power bit precheck')
  exact_power_calls+=1;return q**k
 V=power(vs,alpha);c=mean['constants'];d=F(1,alpha)
 E=Mh*Mh*(F(1,2)+d)*F(c['G_b_power_upper'])+(vs*vs/(128*kappa*kappa*(alpha-1)**2*d*d)+F(c['K_upper'])*kappa*kappa)*F(c['G_1_power_upper'])+(1+F(c['global_transport_correction_upper']))/(16*kappa*kappa*(alpha-1)**2)
 bF=(Mh/Ml)**2*jh+2*E/(Ml*Ml*V);bR=power(1/(vs*(1+kappa/8)),alpha)/(4*Ml*Ml)
 roots=p.Roots(precision_bits,max_integer_bits);eps=Pu*(roots.upper(bF)+roots.upper(bR))**2-1
 if eps<0:raise Unknown('nonnegative full primal/dual inverse-form error')
 Cu=Pu/(beta*V);rate=Cu/Ml;x=rate*physical_spacing
 eta=F(mean['slab_to_basin_mass_ratio_upper']);s=eta/(2+eta);C=2+eta
 G=roots.upper(eps*(1+eps))/2+3*eps/8;delta=G+2*roots.upper(s)
 if used>=max_operations:raise Unknown('shared product budget before literal physical-grid query')
 fx=base.Fixed(precision_bits,max_operations-used,max_integer_bits,max_exp_terms,1);r4=fx.expminus(4*x);den=1-F(r4[1],fx.S)
 if den<=0:raise Unknown('positive physical-grid KL denominator unresolved')
 tv=roots.upper(C*n*delta*delta/(2*den))+n*eta
 jitter=tv+(C+1)*n*x*x/2+C*n*eps/4+F(3,2)*n*eta
 if tv>path_error:raise Unknown('full unchanged-physical-grid record error misses external target; no precision-only promise')
 if jitter_error is not None and jitter>jitter_error:raise Unknown('continuous hysteretic jump-jitter bound misses external target')
 r2=fx.expminus(2*x);q=((fx.S-r2[1])//2,(fx.S-r2[0]+1)//2)
 (cl,ch),updates=p.old.count_event(fx,q,n,event_lower,event_upper);clo,chi=F(cl,fx.S),F(ch,fx.S);lo=max(F(0),clo-tv);hi=min(F(1),chi+tv)
 if hi-lo>query_absolute_width:raise Unknown('actual fixed-grid count event misses external absolute-width request')
 files=['positive_integrals.py','acquire_derivative.py','shifted_current.py','receive_matched_clock.py']
 source_hashes={name:hashlib.sha256((Path(__file__).resolve().parent/name).read_bytes()).hexdigest()for name in files}
 return {'schema':'matched_energy_retained_clock.v1','proof_sha256':PROOF_SHA,'accepted_runtime_sha256':p.PARENT_SHA,'new_runtime_source_hashes':source_hashes,'task':{k:fs(v)if type(v)is F else v for k,v in args.items()},
 'observable':'same continuing original-model hysteretic record on externally specified literal PHYSICAL times, after ONCE exact FULL Gibbs|A initialization',
 'initialization':mean['initialization'],'actual_full_generator':mean['actual_full_generator'],
 'not_claimed':['full energy Markov closure','angular reset/mixing','exact finite-dimension iid clocks','physical model/preparation/event-detector authentication','unchanged accuracy for arbitrary angular coefficients or mobility','continuous timestamp TV','arbitrary adaptive schedules/controls','relative rare-record accuracy','unbounded moment receiving'],
 'raw_derivative_acquisition':acq,'inherited_source_certificate':mean,'primal_scalar_price':{k:fs(v)if type(v)is F else v for k,v in price.items()},
 'shifted_current_parameter':fs(abar),'scaled_shifted_resistance':interval(jl,jh),'well_remainder_upper_without_beta':fs(E),'normalized_odd_basin_source_inverse_upper':fs(bF),'normalized_odd_slab_residual_inverse_upper':fs(bR),
 'full_trial_energy_upper':fs(Cu),'global_moment_error_upper':fs(eps),'reference_flip_rate':fs(rate),'reference_correlation_decay_rate':fs(2*rate),'reference_mean_time':fs(1/rate),'actual_physical_spacing':fs(physical_spacing),'actual_physical_horizon':fs(n*physical_spacing),'reference_dimensionless_step':fs(x),
 'sharp_trial_vector_error_upper':fs(G),'sign_vector_error_upper':fs(delta),'slab_to_basin_mass_ratio_upper':fs(eta),'record_TV_error_upper':fs(tv),'continuous_jitter_failure_unclipped_upper':fs(jitter),'continuous_jitter_failure_upper':fs(min(F(1),jitter)),
 'comparison_flip_probability':interval(F(q[0],fx.S),F(q[1],fx.S)),'event':{'kind':'sampled_label_change_count_between_inclusive','lower_count':event_lower,'upper_count':event_upper,'comparison_probability':interval(clo,chi),'actual_probability':interval(lo,hi)},
 'work':{'inherited_fixed_operations':mean['work']['fixed_operations'],'shifted_fixed_operations':ii.fixed.operations,'new_primal_fixed_operations':price['work']['fixed_operations'],'query_fixed_operations':fx.operations,'total_fixed_operations':used+fx.operations,'inherited_and_shifted_points':mean['work']['scalar_points']+len(ii.cache),'new_tensor_nodes':price['work']['tensor_nodes'],'query_root_calls':roots.calls,'largest_query_root_operand_bound_bits':roots.max_bits,'exact_normalization_power_calls':exact_power_calls,'largest_exact_normalization_power_bit_precheck':exact_power_bound,'query_exponential_calls':fx.exp_calls,'dp_updates':updates,'dp_states':event_upper+2},'seconds':time.perf_counter()-start}

def verify(raw,certificate,**external_task):
 if type(certificate)is not dict:raise Unknown('certificate object')
 p.old.guard_certificate_tree(certificate)
 expected=certify(raw,**external_task)
 if not base.same(p.old.proof_record(certificate),p.old.proof_record(expected)):raise Unknown('strict original raw/aggregate/derivative/current/physical-grid/error/endpoint conjunction')
 return {'status':'PASS','scope':expected['observable'],'actual_raw_sha256':expected['raw_derivative_acquisition']['actual_raw_sha256'],'physical_spacing':expected['actual_physical_spacing'],'record_TV_error_upper':expected['record_TV_error_upper'],'physical_membership':'not authenticated'}

def external_from_record(c):
 t=dict(c['task'])
 for k in RATKEYS+(['jitter_error']if t['jitter_error']is not None else []):t[k]=F(t[k])
 return t

if __name__=='__main__':
 task=json.loads(Path('original_physical_task.json').read_text());raw=p.old.fixture()
 c=certify(raw,n=task['n'],physical_spacing=F(task['physical_spacing']),event_lower=task['event_lower'],event_upper=task['event_upper'])
 Path('matched_certificate.json').write_text(json.dumps(c,indent=2)+'\n')
 print('PASS candidate producer: literal original grid; TV',base.show(F(c['record_TV_error_upper'])),'event',c['event']['actual_probability']['display'],'work',c['work'],'seconds',c['seconds'],flush=True)
