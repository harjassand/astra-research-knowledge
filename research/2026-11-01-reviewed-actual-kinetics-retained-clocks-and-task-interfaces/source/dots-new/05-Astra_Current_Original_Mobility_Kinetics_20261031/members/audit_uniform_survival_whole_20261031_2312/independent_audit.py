from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import importlib.util,json,random,time,shutil
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_survival',H/'uniform_survival_receiver_20261031/receive_survival.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
counts={};refusals=[];start=time.perf_counter();rng=random.Random(2313)
def ok(b,label):
 assert b,label
 counts[label]=counts.get(label,0)+1
def unknown(fn,label):
 try:fn()
 except c.Unknown as e:ok(True,label);refusals.append({'test':label,'reason':str(e)})
 else:raise AssertionError('admitted '+label)
def reference_exp(x,P=384):
 # Independent exact alternating Taylor, then independent dyadic square rounding.
 if not x:return F(1),F(1)
 s=0;r=x
 while r>F(1,2):r/=2;s+=1
 term=F(1);a=F(1);even=None
 for n in range(1,162):
  term*=-r/n;a+=term
  if n==160:even=a
 S=1<<P
 def floor(q):return F(q.numerator*S//q.denominator,S)
 def ceil(q):return F(-(-q.numerator*S//q.denominator),S)
 lo,hi=floor(a),ceil(even)
 for _ in range(s):lo,hi=floor(lo*lo),ceil(hi*hi)
 return lo,hi
xs=[F(0),F(1,2**400),F(1,2),F(1),F(2),F(32),F(10**30),F(1<<1000)]+[F(rng.randrange(1,100000),rng.randrange(1,10000))for _ in range(72)]
for P in [64,128,256]:
 for x in xs:
  fx=c.base.Fixed(P,100000,20000,4096,1);lo,hi=fx.expminus(x);rl,rh=reference_exp(x)
  ok(F(lo,fx.S)<=rl<=rh<=F(hi,fx.S),'independent alternating and dyadic exponential enclosure');ok(0<=lo<=hi<=fx.S,'exponential probability range')
for _ in range(350):
 q=F(rng.randrange(1,10**8),rng.randrange(1,10**8));P=rng.randrange(16,257);rt=c.core.Roots(P,10000);u=rt.upper(q)
 ok(u*u>=q and (u-F(1,1<<P))**2<=q,'extra root upper and one-ulp accuracy');ok(rt.calls==1 and rt.max_bits>=c.core.bits(q),'extra root count and bit ledger')
for _ in range(400):
 kl=F(rng.randrange(1,1000),rng.randrange(1,1000));kh=kl*(1+F(rng.randrange(0,1000),1000));k=(kl+kh)/2;k0=kl+(kh-kl)*F(rng.randrange(0,1001),1000)
 ok(abs(k-k0)/min(k,k0)<=(kh/kl-1)/2,'exact midpoint worst-relative-rate inequality')
ok(sum((F(1),F(1),F(1,2),F(1,6),F(1,24)))>F(8,3),'strict Euler lower bound from finite positive series');ok(F(3,8)+F(9,16)<1,'spectral remainder plus mean correction constant')
for n in range(2,100):
 x=F(1,2**n);w=F(1,2**(2*n));y=(1-w*x)/(1-w);inv=w/x+(1-w)/y;defect=w*(x-1)**2/x+(1-w)*(y-1)**2/y
 ok(w*x+(1-w)*y==1 and defect==inv-1 and defect>=0,'spectral tiny-support exact moment identity')
raw=c.fixture(64);task={'times':[F(0),F(1000),F(10000)],'ks_error':F(3,10),'query_absolute_width':F(3,5),'quad_relative':F(1,20),'full_ratio':F(6,5)}
cert=c.certify(raw,**task);ok(c.verify(raw,cert,**task)['status']=='PASS','independent cheap literal original-task roundtrip')
def arithmetic(cc,beta,times):
 m=cc['mean_certificate'];ml,mh=F(m['basin_mass']['lower']),F(m['basin_mass']['upper']);rl,rh=F(m['slab_resistance']['lower']),F(m['slab_resistance']['upper']);rho=F(m['slab_to_basin_mass_ratio_upper']);eps=(1+rho)*F(m['mean_hitting_time']['upper'])/(beta*ml*rl)-1
 kl=1/(beta*mh*rh);kh=1/(beta*ml*rl);ref=(kl+kh)/2;root=F(cc['initial_law_comparison_error_upper'])-rho;rate=F(3,16)*(kh/kl-1);delta=eps+rho+root+rate
 ok(F(cc['spectral_error_upper'])==eps and eps>=0,'independent received source spectral defect');ok(F(cc['exact_rate_enclosure']['lower'])==kl and F(cc['exact_rate_enclosure']['upper'])==kh and F(cc['reference_exponential_rate'])==ref,'independent full absolute-time midpoint and interval');ok(root*root>=rho*(1+rho) and root>0,'initial law square-root inequality');ok(F(cc['finite_rate_error_upper'])==rate and F(cc['uniform_KS_error_upper'])==delta,'independent total KS decomposition')
 operations=0;exp_calls=0;terms=0
 for q,t in zip(cc['queries'],times):
  lo,hi=F(q['cdf']['lower']),F(q['cdf']['upper']);ok(F(q['time'])==t and 0<=lo<=hi<=1,'original query time and CDF range')
  if not t:ok(lo==hi==0,'continuous separated-set exact zero-time CDF');continue
  el,eh=reference_exp(ref*t);ok(lo<=max(F(0),1-eh-delta) and hi>=min(F(1),1-el+delta),'independent actual CDF query enclosure')
  fx=c.base.Fixed(cc['task']['precision_bits'],100000,1000000,16384,1);fx.expminus(ref*t);x=ref*t;s=max(0,x.numerator.bit_length()-x.denominator.bit_length()+2);expected=4*fx.exp_terms+1+2*s
  ok(fx.operations==expected,'extra exponential product ledger per query');operations+=expected;exp_calls+=1;terms+=fx.exp_terms
 ok(cc['work']['extra_fixed_operations']==operations and cc['work']['total_fixed_operations']==m['work']['fixed_operations']+operations and cc['work']['extra_exponential_calls']==exp_calls and cc['work']['extra_exp_terms']==terms,'shared all-query complete fixed-product ledger')
arithmetic(cert,F(1),task['times'])
class FF(F):pass
class II(int):pass
for key in ['ks_error','query_absolute_width','beta','kappa','quad_relative','full_ratio']:
 for bad in [True,1,1.0,None,F(0),F(-1),FF(1,2)]:unknown(lambda key=key,bad=bad:c.certify(raw,**dict(task,**{key:bad})),'strict exact task rational rejection')
for key in ['precision_bits','max_queries','max_exp_terms','max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits','max_grid','max_points','max_cutoff','max_precision','max_operations','max_integer_bits']:
 for bad in [False,1.0,None,0,-1,II(100)]:unknown(lambda key=key,bad=bad:c.certify(raw,**dict(task,**{key:bad})),'strict external resource integer rejection')
for times in [None,(),[True],[1],[1.0],[FF(1)],[F(-1)],[F(1<<4097)]]:unknown(lambda times=times:c.certify(raw,**dict(task,times=times)),'malformed negative or oversized original time rejection')
for key,value in [('max_queries',2),('max_exp_terms',1),('precision_bits',15),('max_integer_bits',500),('max_precision',128),('max_operations',1),('max_terms',1),('max_dimension',63),('max_exponent_entries',100),('max_total_coefficient_bits',1),('max_rational_bits',1),('max_grid',32),('max_cutoff',1),('max_points',1),('ks_error',F(1)),('query_absolute_width',F(2))]:unknown(lambda key=key,value=value:c.certify(raw,**dict(task,**{key:value})),'budget and tolerance domain refusal')
for mutation in ['coefficient','odd','duplicate','nonhomogeneous','missingpure','late_mobility','dense','extra','dim_bool']:
 rr=deepcopy(raw)
 if mutation=='coefficient':rr['energy_terms'][-1]['coefficient']='-1'
 elif mutation=='odd':rr['energy_terms'][-1]['powers'][-1]=1
 elif mutation=='duplicate':rr['energy_terms'].append(deepcopy(rr['energy_terms'][0]))
 elif mutation=='nonhomogeneous':rr['energy_terms'][-1]['powers']=[0]*64;rr['energy_terms'][-1]['powers'][-1]=2
 elif mutation=='missingpure':rr['energy_terms'].pop(63)
 elif mutation=='late_mobility':rr['mobility_program']={'kind':'constant_diagonal','entries':['64']*63+['0']}
 elif mutation=='dense':rr['mobility_program']={'kind':'constant_dense','entries':[]}
 elif mutation=='extra':rr['physical_membership']=True
 else:rr['dimension']=True
 unknown(lambda rr=rr:c.certify(rr,**task),'complete raw acquisition rejection: '+mutation)
ops=cert['work']['total_fixed_operations'];mean_ops=cert['mean_certificate']['work']['fixed_operations']
ok(c.certify(raw,**dict(task,max_operations=ops))['queries']==cert['queries'],'exact shared product budget passes');unknown(lambda:c.certify(raw,**dict(task,max_operations=ops-1)),'one-below shared product budget refuses');unknown(lambda:c.certify(raw,**dict(task,max_operations=mean_ops)),'query arithmetic not gifted a fresh budget')
for ts in [[],[F(0)],[F(0),F(0)]]:
 cc=c.certify(raw,**dict(task,times=ts,max_operations=mean_ops));ok(cc['work']['extra_fixed_operations']==0 and cc['work']['extra_root_calls']==1,'no-query or zero-time paid root but no exponential products')
delta=F(cert['uniform_KS_error_upper']);w=max(F(q['cdf']['upper'])-F(q['cdf']['lower'])for q in cert['queries'])
ok(c.certify(raw,**dict(task,ks_error=delta))['uniform_KS_error_upper']==str(delta),'exact KS threshold passes');unknown(lambda:c.certify(raw,**dict(task,ks_error=delta-F(1,1<<300))),'below exact KS threshold refuses');ok(c.certify(raw,**dict(task,query_absolute_width=w))['queries']==cert['queries'],'exact total query width threshold passes');unknown(lambda:c.certify(raw,**dict(task,query_absolute_width=w-F(1,1<<300))),'below exact outward query width refuses')
paths=[('schema',),('dependency_sha256',),('root_theorem_sha256',),('finite_rate_corollary_sha256',),('observable',),('initialization',),('actual_full_generator',),('uniform_statement',),('not_claimed',),('reference_exponential_rate',),('spectral_error_upper',),('slab_mass_ratio_upper',),('initial_law_comparison_error_upper',),('finite_rate_error_upper',),('uniform_KS_error_upper',),('exact_rate_enclosure','lower'),('exact_rate_enclosure','upper'),('task','beta'),('task','max_operations'),('task','times'),('task','ks_error'),('mean_certificate','acquisition','transverse_SPD_everywhere'),('mean_certificate','initialization'),('mean_certificate','mean_hitting_time','upper'),('mean_certificate','task','beta'),('queries',0,'time'),('queries',1,'cdf','lower')]
for path in paths:
 cc=deepcopy(cert);x=cc
 for k in path[:-1]:x=x[k]
 x[path[-1]]=None;unknown(lambda cc=cc:c.verify(raw,cc,**task),'strict complete proof-field receiving')
for bad in [None,[],True,{}, {'mean_certificate':None}]:unknown(lambda bad=bad:c.verify(raw,bad,**task),'malformed outer certificate refusal')
cc=deepcopy(cert);cc['mean_certificate']=cc;unknown(lambda:c.verify(raw,cc,**task),'cyclic mean certificate finite refusal')
cc=deepcopy(cert);cc['queries']=[cc];unknown(lambda:c.verify(raw,cc,**task),'cyclic malformed query finite refusal')
cc=deepcopy(cert);cc['task']['times']=[cc];unknown(lambda:c.verify(raw,cc,**task),'cyclic wrong-type task finite refusal')
cc=deepcopy(cert);cc['new_theorem']='relative extreme tails';unknown(lambda:c.verify(raw,cc,**task),'unknown extra proof claim rejected')
cc=deepcopy(cert);cc['work']=None;cc['seconds']=None;cc['mean_certificate']['work']=None;cc['mean_certificate']['seconds']=None;cc['exact_rate_enclosure']['display']=None;cc['queries'][1]['cdf']['display']=None;ok(c.verify(raw,cc,**task)['status']=='PASS','diagnostic fields intentionally excluded from proof')
unknown(lambda:c.verify(raw,cert,**dict(task,times=list(reversed(task['times'])))),'external time order binds despite same query set');unknown(lambda:c.verify(raw,cert,**dict(task,times=task['times']+[F(2)])),'external extra query binds')
rr=c.fixture(64,mobility=F(64,3));scaled=c.certify(rr,**dict(task,beta=F(9),times=[9*t for t in task['times']]))
ok(F(scaled['reference_exponential_rate'])==F(cert['reference_exponential_rate'])/9 and scaled['uniform_KS_error_upper']==cert['uniform_KS_error_upper'],'beta mobility scaling has correct absolute reference rate');ok([q['cdf']for q in scaled['queries']]==[q['cdf']for q in cert['queries']],'scaled absolute-time queries match exact outer CDF')
saved=[]
for row in json.loads((H/'uniform_survival_receiver_20261031/results.json').read_text()):
 f=row['fixture'];rr=c.fixture(f['m'],F(f['coupling']),F(f['mobility']),f['diagonal'])
 if f['m']==128:tt={'times':[F(0),F(10**8),F(3*10**8),F(10**9)],'ks_error':F(1,100),'query_absolute_width':F(1,50)}
 elif f['m']==256:tt={'times':[F(0),F(10**17),F(4*10**17),F(10**18),F(10**19)]}
 elif f['m']==512:tt={'times':[F(0),F(10**36),F(4*10**36),F(10**37),F(10**38)]}
 else:raise AssertionError('unrecognized fixture')
 cc=c.certify(rr,**tt);old=row['certificate'];ok(c.base.same(c.proof_record(cc),c.proof_record(old)),'actual saved original-task full proof recapture');ok(cc['work']==old['work'],'actual saved extra work recapture');ok(cc['mean_certificate']['work']==old['mean_certificate']['work'],'actual saved mean work recapture');arithmetic(cc,F(1),tt['times'])
 ok(F(cc['uniform_KS_error_upper'])<=tt.get('ks_error',F(1,200)) and all(F(q['cdf']['upper'])-F(q['cdf']['lower'])<=tt.get('query_absolute_width',F(1,100))for q in cc['queries']),'saved total KS and query widths meet external originals')
 saved.append({'fixture':f,'KS_display':float(F(cc['uniform_KS_error_upper'])),'reference_rate_display':float(F(cc['reference_exponential_rate'])),'queries':[{'time':q['time'],'display':[float(F(q['cdf']['lower'])),float(F(q['cdf']['upper']))]}for q in cc['queries']],'work':cc['work'],'raw_sha256':cc['mean_certificate']['acquisition']['raw_sha256']})
rr=json.loads((H/'uniform_survival_receiver_20261031/small_raw_fixture.json').read_text());cc=json.loads((H/'uniform_survival_receiver_20261031/small_certificate.json').read_text());st={'times':[F(0),F(10**8),F(3*10**8),F(10**9)],'ks_error':F(1,100),'query_absolute_width':F(1,50)}
ok(c.verify(rr,cc,**st)['status']=='PASS','standalone fixture literal task replay');unknown(lambda:c.verify(rr,cc,times=st['times']),'omitted KS default not adopted from certificate');unknown(lambda:c.certify(c.fixture(512,mobility=F(1)),times=[],full_ratio=F(13,10)),'unit mobility fails requested small KS despite receiving a mean')
d=H/'dependency_tamper';(d/'uniform_survival_receiver_20261031').mkdir(parents=True,exist_ok=True);(d/'constant_spd_mfpt_20261031').mkdir(exist_ok=True);shutil.copyfile(H/'uniform_survival_receiver_20261031/receive_survival.py',d/'uniform_survival_receiver_20261031/receive_survival.py');(d/'constant_spd_mfpt_20261031/receive_mfpt.py').write_bytes((H/'constant_spd_mfpt_20261031/receive_mfpt.py').read_bytes()+b'\n# intentional isolated mismatch\n')
spec=importlib.util.spec_from_file_location('tampered_survival',d/'uniform_survival_receiver_20261031/receive_survival.py');mod=importlib.util.module_from_spec(spec)
try:spec.loader.exec_module(mod)
except RuntimeError as e:ok(str(e)=='constant-SPD MFPT dependency hash mismatch','runtime dependency hash refusal before import')
else:raise AssertionError('changed dependency admitted')
report={'status':'PASS','checks':sum(counts.values()),'categories':counts,'refusals':refusals,'saved_recaptured':saved,'seconds_diagnostic':time.perf_counter()-start,'scope':'Uniform absolute autonomous passage-time CDF under ordinary constant SPD, EXACT FULL Gibbs|A initial law; not relative extreme tails or physical preparation.'};(H/'independent_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['refusals','saved_recaptured']},indent=2))
