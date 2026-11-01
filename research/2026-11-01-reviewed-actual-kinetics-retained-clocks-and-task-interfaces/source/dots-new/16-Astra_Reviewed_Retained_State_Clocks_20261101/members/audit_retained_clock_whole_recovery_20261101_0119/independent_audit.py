from pathlib import Path
from fractions import Fraction as F
from math import comb,isqrt
from copy import deepcopy
import importlib.util,json,random,time
H=Path(__file__).resolve().parent;S=H/'replay/retained_state_renewal_clock_20261101'
spec=importlib.util.spec_from_file_location('c',S/'receive_clock.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
checks=0;cats={};refusals=[];rng=random.Random(11010119);start=time.perf_counter()
def ok(a,k):
 global checks
 assert a,k
 checks+=1;cats[k]=cats.get(k,0)+1

def no(fn,k):
 try:fn()
 except c.Unknown as e:refusals.append({'test':k,'reason':str(e)});ok(True,k)
 else:raise AssertionError('false admission: '+k)

def ex(x):
 x=F(x);s=0
 while x>F(1,2):x/=2;s+=1
 z=t=F(1)
 for j in range(1,161):
  t*=-x/j;z+=t
  if j==159:lo=z
 hi=z
 for j in range(s):lo*=lo;hi*=hi
 return lo,hi

for x in [F(0),F(1,10**12),F(1,8),F(1,2),F(1),F(2),F(4),F(20)]+[F(rng.randrange(1,1000),rng.randrange(1,1000))for _ in range(100)]:
 f=c.base.Fixed(128,100000,100000,1024,1);a,b=f.expminus(x);l,h=ex(x)
 ok(F(a,f.S)<=l<=h<=F(b,f.S),'independent alternating Taylor exponential enclosure')
 s=max(0,x.numerator.bit_length()-x.denominator.bit_length()+2)
 ok(f.operations==(4*f.exp_terms+1+2*s if x else 0),'exact exponential product count')
for i in range(500):
 n=rng.randrange(1,21);L=rng.randrange(n+1);U=rng.randrange(L,n+1);q=F(rng.randrange(101),100)
 f=c.base.Fixed(96,1000000,10000,1024,1);qi=f.rat(q);before=f.operations;(a,b),updates=c.count_event(f,qi,n,L,U)
 val=sum((F(comb(n,j))*q**j*(1-q)**(n-j)for j in range(L,U+1)),F(0))
 ok(F(a,f.S)<=val<=F(b,f.S),'capped DP versus independent exact binomial')
 ok(updates==sum(min(j,U+1)+1 for j in range(n)) and f.operations-before==4*sum(min(j,U)+1 for j in range(n)),'exact DP update and product ledger')
 ok(updates<=n*(U+2),'DP conservative preallocation budget')
for n in range(1,10):
 for p,q in [(F(0),F(1)),(F(1,4),F(3,4)),(F(0),F(1,16)),(F(15,16),F(1))]:
  f=c.base.Fixed(64,1000000,10000,1024,1);L=n//3;U=2*n//3;(a,b),_=c.count_event(f,(int(p*f.S),int(q*f.S)),n,L,U)
  for x in [p,(p+q)/2,q]:
   v=sum((comb(n,j)*x**j*(1-x)**(n-j)for j in range(L,U+1)),F(0));ok(F(a,f.S)<=v<=F(b,f.S),'wide interval parameter including overflow')
for i in range(250):
 q=F(rng.randrange(1,10**8),rng.randrange(1,10**8));P=rng.choice([16,32,64,256]);r=c.core.Roots(P,100000).upper(q)
 ok(r*r>=q and (r-F(1,1<<P))**2<q,'independent square/minimal outward root')

raw=c.fixture(64);task=dict(n=1,x=F(1),event_lower=0,event_upper=1,path_error=F(9,10),query_absolute_width=F(1),quad_relative=F(1,8),full_ratio=F(10))
cert=c.certify(raw,**task);task=c.external_from_record(cert)
(H/'independent_small_raw.json').write_text(json.dumps(raw,indent=2)+'\n');(H/'independent_small_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
ok(c.verify(raw,cert,**task)['status']=='PASS','fresh small literal task receive')
def leaves(o,p=()):
 if type(o)is dict:
  for k,v in o.items():
   if k not in ['work','display','seconds']:yield from leaves(v,p+(k,))
 elif type(o)is list:
  for k,v in enumerate(o):yield from leaves(v,p+(k,))
 else:yield p,o
for p,v in list(leaves(cert)):
 b=deepcopy(cert);o=b
 for k in p[:-1]:o=o[k]
 o[p[-1]]=v+'__forge' if type(v)is str else int(v) if type(v)is bool else bool(v) if type(v)is int else 'forged_null'
 no(lambda b=b:c.verify(raw,b,**task),'every typed proof leaf mutation rejected')
for path in [(),('task',),('event',),('mean_engine_certificate','acquisition')]:
 b=deepcopy(cert);o=b
 for k in path:o=o[k]
 o['unreceived_claim']='iid waits';no(lambda b=b:c.verify(raw,b,**task),'extra proof claims rejected')
for b in [None,[],True,1,'bad']:no(lambda b=b:c.verify(raw,b,**task),'malformed certificate top-level')
b=deepcopy(cert);b['work']={};b['seconds']=None;b['event']['actual_probability']['display']=['no','evidence'];ok(c.verify(raw,b,**task)['status']=='PASS','diagnostic display/cost/seconds are not evidence')
for k,v in task.items():
 t=task.copy();t[k]=F(99,100) if v is None else v+1 if type(v)is int else v+F(1,100000)
 no(lambda t=t:c.verify(raw,cert,**t),'every changed external task field bound')
for k,v in task.items():
 if type(v)is int:
  for alias in [True,1.0,F(1),None,-1]:
   t=task.copy();t[k]=alias;no(lambda t=t:c.certify(raw,**t),'strict integer external parser')
for k in c.RATKEYS+['jitter_error']:
 for alias in [True,1,1.0,'1/2',F(0),F(-1),F(1,1<<5000)]:
  t=task.copy();t[k]=alias;no(lambda t=t:c.certify(raw,**t),'strict exact rational malformed/oversized')
for t0 in [dict(n=0),dict(event_lower=2),dict(event_upper=2),dict(event_lower=1,event_upper=0),dict(path_error=F(1)),dict(jitter_error=F(1)),dict(query_absolute_width=F(2)),dict(x=F(1,10**100),precision_bits=16),dict(max_terms=1),dict(max_exponent_entries=1),dict(max_total_coefficient_bits=1),dict(max_rational_bits=1),dict(max_cutoff=1),dict(max_points=1),dict(max_grid=32),dict(full_ratio=F(101,100))]:
 t=task.copy();t.update(t0);no(lambda t=t:c.certify(raw,**t),'failed domain/numerical/full-error conjunction')
mut=[]
for k,v in [('dimension',True),('dimension',64.0),('dimension',0),('energy_terms',{}),('mobility_program',None)]:r=deepcopy(raw);r[k]=v;mut.append(r)
r=deepcopy(raw);r['extra']='hidden dynamics';mut.append(r)
for v in ['0','-1','01','1.0','1/0','1/01','1/2/3',True,1,'9'*10000]:r=deepcopy(raw);r['energy_terms'][-1]['coefficient']=v;mut.append(r)
for v in [True,1,-2,6,F(2),2.0]:r=deepcopy(raw);r['energy_terms'][-1]['powers'][-1]=v;mut.append(r)
r=deepcopy(raw);r['energy_terms'].append(deepcopy(r['energy_terms'][0]));mut.append(r)
r=deepcopy(raw);r['energy_terms'].pop(63);mut.append(r)
r=deepcopy(raw);r['energy_terms'][-1]['powers'].pop();mut.append(r)
for v in [{'kind':'constant_isotropic','value':'0'},{'kind':'constant_isotropic','value':'-1'},{'kind':'constant_diagonal','entries':['1']*63},{'kind':'constant_diagonal','entries':['1']*63+['0']},{'kind':'state_dependent','value':'1'},{'kind':'constant_isotropic','value':'1','cross':'1'}]:r=deepcopy(raw);r['mobility_program']=v;mut.append(r)
for r in mut:no(lambda r=r:c.certify(r,**task),'complete raw grammar including late mutation')
r=deepcopy(raw);r['energy_terms'][-1]['coefficient']='21';no(lambda:c.verify(r,cert,**task),'valid late raw coefficient bound to certificate')
for name,budget in [('max_operations',cert['work']['total_fixed_operations']),('max_dp_updates',task['n']*(task['event_upper']+2)),('max_record_steps',task['n']),('max_integer_bits',max(cert['work']['largest_extra_root_integer_bound_bits'],cert['work']['largest_extra_guarded_product_bits'],cert['mean_engine_certificate']['work']['largest_guarded_product_bits'],cert['mean_engine_certificate']['work']['largest_root_integer_bound_bits']))]:
 t=task.copy();t[name]=budget;z=c.certify(raw,**t);ok(z['record_TV_error_upper']==cert['record_TV_error_upper'],'exact paid budget admits')
 t[name]=budget-1;no(lambda t=t:c.certify(raw,**t),'one below exact paid budget refuses')

out=[]
for name,t in [('ten_mean_scale_observations',dict(n=10,x=F(1),event_lower=4,event_upper=6)),('one_horizon_hysteretic_jitter',dict(n=8,x=F(1,8),event_lower=0,event_upper=2,path_error=F(1,5),jitter_error=F(9,20),query_absolute_width=F(2,5)))]:
 rr=c.fixture();z=c.certify(rr,**t);t=c.external_from_record(z);m=z['mean_engine_certificate'];parts={k:F(v)for k,v in m['upper_source_A_components'].items()};UA=sum(parts.values());g=2*UA-parts['parallel_slab']
 ok(c.base.canonical_hash(rr)=='e693d5c1ccf5fe43336f3e845d78fdad3a308d0fe88094cc8c4688a5caca76ff','identical actual original 513D raw model')
 ok(g==F(z['global_odd_source_inverse_per_mass_upper']) and UA<g<2*UA,'global current one slab twice every well')
 ml,mh=(F(m['basin_mass'][k])for k in ['lower','upper']);rl,rh=(F(m['slab_resistance'][k])for k in ['lower','upper']);eta=F(m['slab_to_basin_mass_ratio_upper']);C=2+eta;s=eta/C;bf=g/(t['beta']*ml*rl);eps=(1+eta/2)*(bf+eta*F(m['source_S_slab_factor_upper'])/2)-1
 ok(eps==F(z['global_spectral_error_upper']) and eps>0,'weighted separate global/residual source error')
 l=1/(t['beta']*mh*rh);u=1/(t['beta']*ml*rl);rate=(l+u)/2;d=(u-l)/(u+l)
 ok(F(z['reference_flip_rate'])==rate and F(z['reference_correlation_decay_rate'])==2*rate,'flip and correlation rates not interchanged')
 ok(F(z['relative_rate_uncertainty_upper'])==d and (1-d)*rate==l and (1+d)*rate==u,'midpoint exact rational rate uncertainty')
 ok(F(z['physical_grid_spacing'])==t['x']/rate and F(z['physical_horizon'])==t['n']*t['x']/rate and F(z['jump_time_tolerance'])==t['x']/rate,'physical spacing horizon and jitter exact')
 G=F(z['sharp_trial_vector_error_upper']);root=2*(G-3*eps/8);ok(root*root>=eps*(1+eps) and (root-F(1,1<<t['precision_bits']))**2<eps*(1+eps),'sharp vector independent root square')
 delta=F(z['sign_vector_error_upper']);root=(delta-G-3*d/(8*(1-d)))/2;ok(root*root>=s and (root-F(1,1<<t['precision_bits']))**2<s,'stationary slab independent root square')
 tv=F(z['record_TV_error_upper']);l4,h4=ex(4*t['x']);ok((tv-t['n']*eta)**2>=C*t['n']*delta*delta/(2*(1-h4)),'independent exact exponential entropy denominator')
 jitter=tv+(C+1)*t['n']*t['x']**2/2+C*t['n']*eps/4+F(3,2)*t['n']*eta+C*t['n']*d*t['x'];ok(jitter==F(z['continuous_jitter_failure_unclipped_upper']) and min(F(1),jitter)==F(z['continuous_jitter_failure_upper']),'complete F2 all cluster/slab/rate penalties')
 l2,h2=ex(2*t['x']);ql,qh=(1-h2)/2,(1-l2)/2;cp=z['comparison_flip_probability'];ok(F(cp['lower'])<=ql<=qh<=F(cp['upper']),'independent exact reference q bounds')
 n=t['n'];L=t['event_lower'];U=t['event_upper'];plo=sum((comb(n,j)*ql**j*(1-qh)**(n-j)for j in range(L,U+1)),F(0));phi=sum((comb(n,j)*qh**j*(1-ql)**(n-j)for j in range(L,U+1)),F(0));ev=z['event']
 ok(F(ev['comparison_probability']['lower'])<=plo<=phi<=F(ev['comparison_probability']['upper']),'production count event exact binomial interval')
 ok(F(ev['actual_probability']['lower'])==max(F(0),F(ev['comparison_probability']['lower'])-tv) and F(ev['actual_probability']['upper'])==min(F(1),F(ev['comparison_probability']['upper'])+tv),'actual event whole-record TV clipping')
 ok(tv<=t['path_error'] and F(ev['actual_probability']['upper'])-F(ev['actual_probability']['lower'])<=t['query_absolute_width'],'actual total width not scalar precision only')
 harder=t.copy();harder['path_error' if t['jitter_error']is None else 'jitter_error']=F(1,10);no(lambda harder=harder:c.certify(rr,**harder),'original stronger ten-percent target refused')
 paid=t.copy();paid['max_operations']=z['work']['total_fixed_operations']-1;no(lambda paid=paid:c.certify(rr,**paid),'production shared scalar/exp/DP budget enforced')
 out.append({'name':name,'certificate':z})
(H/'independent_production_replays.json').write_text(json.dumps(out,indent=2)+'\n')
report={'status':'PASS','checks':checks,'categories':cats,'refusals':refusals,'seconds':time.perf_counter()-start,'recovery':'fresh executed evidence; does not claim missing preincident outputs were restored'}
(H/'independent_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='refusals'},indent=2));print('UNKNOWN refusals',len(refusals))
