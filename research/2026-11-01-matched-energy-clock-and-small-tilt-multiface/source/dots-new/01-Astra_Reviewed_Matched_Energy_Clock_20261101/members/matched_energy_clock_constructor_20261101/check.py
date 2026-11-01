"""Exact author checks. Full production is freshly verified once, not memoized.
Schema mutation-only replay explicitly substitutes an already recomputed record;
raw/task/production recaptures below invoke the actual constructor.
"""
from fractions import Fraction as F
from math import factorial,comb
from pathlib import Path
import json,copy,random,time,hashlib
import receive_matched_clock as r
p=r.p;ad=r.ad;base=r.base;Unknown=r.Unknown
count=0;refusals=0;categories={}
def ck(value,label):
 global count
 assert value,label
 count+=1;categories[label.split(':')[0]]=categories.get(label.split(':')[0],0)+1
def no(fn,label):
 global refusals
 try:fn()
 except Unknown:refusals+=1;ck(True,label);return
 raise AssertionError('not UNKNOWN: '+label)

def int_phi_power(k,l,u,kappa=F(1)):
 return kappa**k*sum((F(comb(k,j)*2**(k-j)*(-1)**j,2*k+2*j+1)*(u**(2*k+2*j+1)-l**(2*k+2*j+1))for j in range(k+1)),F(0))
def int_f(t,l,u,kappa=F(1),moment=False,N=80):
 a=t/(1+kappa)
 q=sum(((-a)**k/F(factorial(k))*int_phi_power(k+int(moment),l,u,kappa)for k in range(N+1)),F(0))
 error=(u-l)*(a*F(7,16)*kappa)**(N+1)/factorial(N+1)*(F(7,16)*kappa if moment else 1)
 return q-error,q+error

def tests():
 start=time.perf_counter();rng=random.Random(291011)
 # Exact generic interval arithmetic against rational point values.
 fx=p.Intervals(96,1000000,10000,1024,1)
 for _ in range(120):
  a=F(rng.randrange(1,100),rng.randrange(1,100));b=F(rng.randrange(1,100),rng.randrange(1,100));A=fx.rat(a);B=fx.rat(b)
  for ans,val in [(fx.add(A,B),a+b),(fx.mul(A,B),a*b),(fx.div(A,B),a/b),(fx.positive_sub(A,B),max(F(0),a-b)),(fx.power(A,3),a**3)]:ck(F(ans[0],fx.S)<=val<=F(ans[1],fx.S),'interval:exact containment')
 # Integrated Taylor polynomial is independent of candidate trapezoids and
 # Machin/incomplete-Gamma lower-J formulas. Remainder is Lagrange absolute.
 price=p.Price(16,F(1),F(1),F(100),F(1),Nt=8,Ny=16,L=F(0),T=F(32),precision_bits=192)
 for t in [F(0),F(1,10),F(1),F(4),F(8),F(16),F(32)]:
  lo,hi=int_f(t,F(0),F(1,2));analytic=F(price.analytic_J_lower(t),price.fx.S)
  ck(analytic<=hi,'analyticJ:independent integrated Taylor upper')
  row=price.row(t,[price.fx.expminus(t*v/2)for v in price.phi]);ck(F(row['Jlo'],price.fx.S)<=hi,'row:independent J reference')
  if t==0:ck(analytic==F(1,2),'analyticJ:exact endpoint')
  for j in [1,5,10,15]:
   y=F(j,32);al,ah=int_f(t,0,y);bl,bh=int_f(t,y,F(1,2));apl,aph=int_f(t,0,y,moment=True);bpl,bph=int_f(t,y,F(1,2),moment=True)
   dlo=max(F(0),al*bpl-aph*bh)
   upper=F(row['A0hi'][j+1]*row['BphiHi'][j]-row['AphiLo'][j]*row['B0lo'][j+1],price.fx.S**2)
   ck(upper>=dlo,'row:positive cell D ceiling')
 # Exact actual Hessian, including literal duplicate contributions and mobility.
 for case in range(30):
  raw=p.old.fixture(16,F(case%7),F(1),diagonal=bool(case%2))
  for i in range(16):raw['energy_terms'][i]['coefficient']=str(F(i%5+1,3))
  split=copy.deepcopy(raw['energy_terms'][case%16]);old=F(split['coefficient']);raw['energy_terms'][case%16]['coefficient']=str(old/2);split['coefficient']=str(old/2);raw['energy_terms'].append(split)
  zero=copy.deepcopy(split);zero['coefficient']='0';raw['energy_terms'].append(zero)
  canonical,acq,H,dm,alpha=ad.acquire(raw);ck(acq['duplicate_terms_aggregated']==2,'raw:all duplicates read');ck(acq['zero_terms_read']==1,'raw:zero atoms read');ck(alpha==4,'raw:physical dimension')
  mu=[F(1)]*16 if not case%2 else [F(x)for x in raw['mobility_program']['entries']]
  for repeat in range(4):
   z=[F(rng.randrange(-3,4),2)for _ in range(16)];U=F(0);tr=F(0)
   for term in raw['energy_terms']:
    powers=term['powers'];coef=F(term['coefficient']);U+=coef*__import__('functools').reduce(lambda a,b:a*b,(zz**ee for zz,ee in zip(z,powers)),F(1))
    for i,ei in enumerate(powers):
     if ei:tr+=mu[i]*coef*ei*(ei-1)*__import__('functools').reduce(lambda a,b:a*b,(zz**(ee-2 if j==i else ee)for j,(zz,ee)in enumerate(zip(z,powers))),F(1))
   acquired=sum((F(c)*zz*zz for c,zz in zip(acq['actual_Hessian_trace_coefficients'],z)),F(0))
   ck(tr==acquired,'raw:literal Hessian equality');ck(tr*tr*dm<=H*U,'raw:paid trace coercivity ceiling')
 # New raw parser cannot inherit an oracle for negative, rotated or missing forms.
 raw=p.old.fixture(16,F(2));original=copy.deepcopy(raw)
 for mut in [lambda x:x.update(extra=1),lambda x:x.update(dimension=True),lambda x:x['energy_terms'][0].update(coefficient='-1'),lambda x:x['energy_terms'][0].update(coefficient='0'),lambda x:x['energy_terms'][0]['powers'].__setitem__(0,True),lambda x:x['energy_terms'][0].update(coefficient='1.0'),lambda x:x['mobility_program'].update(value='0')]:
  bad=copy.deepcopy(raw);mut(bad);no(lambda:ad.acquire(bad),'raw-refusal:grammar')
 for name,val in [('max_dimension',15),('max_terms',1),('max_exponent_entries',10),('max_total_coefficient_bits',1),('max_coefficient_bits',1),('max_rational_bits',2)]:no(lambda n=name,v=val:ad.acquire(raw,**{n:v}),'raw-refusal:paid budgets')
 ck(raw==original,'raw:unmodified input')
 for kw in [dict(Nt=True),dict(Ny=0),dict(L=F(-1)),dict(T=F(0)),dict(precision_bits=10**9,max_integer_bits=100),dict(max_nodes=1),dict(max_operations=1),dict(max_rational_bits=10),dict(max_exp_terms=1)]:
  no(lambda k=kw:p.Price(16,F(1),F(1),F(100),F(1),**k).run(),'price-refusal:finite exact interface')
 # Small actual raw producer/replay. L=0 exercises endpoint in a complete run.
 small=json.loads(Path('small_certificate.json').read_text());small_raw=p.old.fixture(64,F(1));smalltask=r.external_from_record(small)
 check=r.verify(small_raw,small,**smalltask);ck(check['status']=='PASS','small:actual recapture')
 ck(F(small['record_TV_error_upper'])<F(9,10),'small:received finite accuracy')
 for key,value in [('n',True),('physical_spacing',float('nan')),('precision_bits',10**9),('Nt',True),('max_integral_nodes',1),('max_dp_updates',1),('path_error',F(1)),('L',F(-1)),('kappa',F(1,100000))]:
  task=dict(smalltask);task[key]=value;no(lambda t=task:r.certify(small_raw,**t),'task-refusal:exact external preflight')
 for key,value in [('max_operations',1000),('max_grid',1),('max_points',1),('path_error',F(1,1000)),('query_absolute_width',F(1,1000)),('jitter_error',F(1,1000))]:
  task=dict(smalltask);task[key]=value;no(lambda t=task:r.certify(small_raw,**t),'task-refusal:actual finite-budget/gate run')
 # Certificate binding only: save repeated 35s scientific recomputations. This
 # DOES NOT stand for original-task verification, which is executed separately.
 real=r.certify;r.certify=lambda *a,**k:small
 try:
  for key,value in [('schema',False),('reference_flip_rate','0'),('record_TV_error_upper','0'),('actual_physical_spacing','1'),('normalized_odd_slab_residual_inverse_upper','0'),('full_trial_energy_upper','1')]:
   bad=copy.deepcopy(small);bad[key]=value;no(lambda b=bad:r.verify(small_raw,b,**smalltask),'binding-only:strict value/type')
  for branch in ['raw_derivative_acquisition','inherited_source_certificate','primal_scalar_price','task','event']:
   bad=copy.deepcopy(small);bad[branch]['unexpected']=0;no(lambda b=bad:r.verify(small_raw,b,**smalltask),'binding-only:nested schema')
  bad=copy.deepcopy(small);bad['seconds']='ignored';bad['work']={'untrusted':float('nan')};ck(r.verify(small_raw,bad,**smalltask)['status']=='PASS','binding-only:named diagnostics excluded')
  bad={};bad['x']=bad;no(lambda:r.verify(small_raw,bad,**smalltask),'tree:cycle preflight')
  bad={};t=bad
  for _ in range(1100):t['x']={};t=t['x']
  no(lambda:r.verify(small_raw,bad,**smalltask),'tree:depth preflight')
 finally:r.certify=real
 # FULL literal production receiving, no cached price, no changed physical grid.
 full=json.loads(Path('matched_certificate.json').read_text());raw=p.old.fixture();task=r.external_from_record(full)
 fullstart=time.perf_counter();replay=r.verify(raw,full,**task);fullseconds=time.perf_counter()-fullstart;ck(replay['status']=='PASS','production:actual original-task verify')
 old=json.loads((Path(__file__).parent.parent/'retained_state_renewal_clock_20261101'/'results.json').read_text())[0]['certificate']
 ck(full['raw_derivative_acquisition']['actual_raw_sha256']=='e693d5c1ccf5fe43336f3e845d78fdad3a308d0fe88094cc8c4688a5caca76ff','comparison:identical raw SHA')
 ck(full['actual_full_generator']==old['actual_full_generator'],'comparison:identical original generator');ck(full['initialization']==old['initialization'],'comparison:identical FULL GibbsA law')
 ck(full['actual_physical_spacing']==old['physical_grid_spacing'],'comparison:identical physical spacing');ck(full['actual_physical_horizon']==old['physical_horizon'],'comparison:identical physical horizon')
 ck(full['task']['n']==old['task']['n'] and full['event']['lower_count']==old['event']['lower_count'] and full['event']['upper_count']==old['event']['upper_count'],'comparison:identical observable query')
 ck(F(full['record_TV_error_upper'])<F(1,10)<F(old['record_TV_error_upper']),'comparison:actual formerly refused target crossed')
 ck(F(full['event']['actual_probability']['upper'])-F(full['event']['actual_probability']['lower'])<=F(1,5),'production:external event width')
 report={'status':'PASS','assertions':count,'UNKNOWN_refusals':refusals,'categories':categories,'full_actual_replay':replay,'production_replay_seconds':fullseconds,'total_seconds':time.perf_counter()-start,'scientific_scope':'candidate author evidence only; numerical/full receiver requires independent review','binding_only_tests_explicitly_stubbed':True}
 Path('author_checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':tests()
