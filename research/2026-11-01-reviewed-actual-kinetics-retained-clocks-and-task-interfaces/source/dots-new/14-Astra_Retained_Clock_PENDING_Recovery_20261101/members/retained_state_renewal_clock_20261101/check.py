from fractions import Fraction as F
from pathlib import Path
from copy import deepcopy
from math import comb
import json,random,hashlib
import sympy as sp
import receive_clock as c
checks=0;categories={};rng=random.Random(110101)
def ok(v,label):
 global checks
 assert v,label
 checks+=1;categories[label]=categories.get(label,0)+1
def unknown(fn,label):
 try:fn()
 except c.Unknown:ok(True,label)
 else:raise AssertionError('unexpected admission: '+label)

# Exact source/transport/weighted-Cauchy identities. Not substitutes for the
# closed-form, committor/local-time or infinity arguments in the written proof.
y,z1,z2,beta,kap=sp.symbols('y z1 z2 beta kappa',positive=True)
v=1+kap*(1-y*y)**2;U=z1**4+z2**4+17*z1*z1*z2*z2;vp=sp.diff(v,y)
continuity=sp.Rational(1,2)*vp/v-beta*vp*U
for z in [z1,z2]:
 b=-vp*z/(4*v);continuity+=sp.diff(b,z)-beta*v*b*sp.diff(U,z)
ok(sp.simplify(continuity)==0,'full-z conditional continuity identity')
a,b,t=sp.symbols('a b t',nonnegative=True)
ok(sp.expand((1+t)*(a*a+t*b*b)-(a+t*b)**2-t*(a-b)**2)==0,'global-source weighted Cauchy identity')
slab,left=sp.symbols('slab left',nonnegative=True)
ok(sp.expand(2*(slab/2+left)-(slab+2*left))==0,'one slab and two wells after reflection')
q0,L0=sp.symbols('q0 L0')
for old,new in [(0,1),(1,0)]:
 ok((new-new)**2-(new-old)**2==-1,'opposite-boundary square reset exactly minus one')
for num in range(201):ok((num>=2)<=F(num-(num%2),2),'count-parity cluster inequality')

# Finite reversible networks independently check the ordinary count/flux
# identity, including arbitrary invariant masses and bottleneck conductances.
for size in range(3,12):
 for rep in range(12):
  masses=[F(rng.randrange(1,20),rng.randrange(1,20))for _ in range(size)];Z=sum(masses)
  cond=[F(rng.randrange(1,20),rng.randrange(1,20))for _ in range(size-1)]
  resist=[1/x for x in cond];R=sum(resist);q=[F(0)]
  for x in resist:q.append(q[-1]+x/R)
  cap=sum(cond[i]*(q[i+1]-q[i])**2 for i in range(size-1))
  incoming_B=cond[-1]*(1-q[-2])/Z;incoming_A=cond[0]*q[1]/Z
  ok(cap==1/R,'network committor capacity exactly')
  ok(incoming_A+incoming_B==2*cap/Z,'stationary augmented transition count equals two fluxes')
  for i in range(1,size-1):ok(cond[i-1]*(q[i-1]-q[i])+cond[i]*(q[i+1]-q[i])==0,'interior harmonic identity')

# Conditional-Jensen and Bernoulli chi-square constants are algebraic. The
# entropy inequality and Pinsker are proved in the separately received source.
for rep in range(300):
 p=F(rng.randrange(0,31),30);q=F(rng.randrange(1,30),30)
 chisq=p*p/q+(1-p)*(1-p)/(1-q)-1
 ok(chisq==(p-q)**2/(q*(1-q)),'binary chi-square exact denominator')
 w=F(rng.randrange(1,30),30);a=F(rng.randrange(-30,31),30);b=F(rng.randrange(-30,31),30)
 ok(w*a*a+(1-w)*b*b-(w*a+(1-w)*b)**2==w*(1-w)*(a-b)**2,'actual-history conditional Jensen')

# Exact DP reference, including endpoint probabilities and overflow. No rare
# full-state trajectories are simulated in these checks.
for n in range(1,11):
 for q in [F(0),F(1,16),F(1,3),F(1,2),F(3,4),F(1)]:
  for lo,hi in [(0,0),(0,n),(n,n),(n//3,2*n//3)]:
   fx=c.base.Fixed(96,100000,10000,1024,1);qi=fx.rat(q)
   (a,b),updates=c.count_event(fx,qi,n,lo,hi)
   exact=sum((F(comb(n,j))*q**j*(1-q)**(n-j)for j in range(lo,hi+1)),F(0))
   ok(F(a,fx.S)<=exact<=F(b,fx.S),'outward finite-state event DP against exact binomial')
   ok(updates<=n*(hi+2),'paid finite-state update upper bound')

# Ordinary outward root and exponential representatives, not independent proof
# of the already received arithmetic engine.
for rep in range(150):
 q=F(rng.randrange(1,10000),rng.randrange(1,10000));rt=c.core.Roots(64,10000).upper(q)
 ok(rt*rt>=q,'outward root exact square check')
 x=F(rng.randrange(1,50),100);fx=c.base.Fixed(128,100000,10000,1024,1);a,b=fx.expminus(2*x)
 ok(1-F(b,fx.S)>=2*x-2*x*x,'representative lower odd-parity bound via exact outward exponential')

raw=c.fixture(64);task=dict(n=1,x=F(1),event_lower=0,event_upper=1,path_error=F(9,10),query_absolute_width=F(1),quad_relative=F(1,8),full_ratio=F(10))
cert=c.certify(raw,**task);ok(c.verify(raw,cert,**task)['status']=='PASS','small complete raw receiving replay')
Path('small_raw_fixture.json').write_text(json.dumps(raw,indent=2)+'\n');Path('small_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
Path('small_receiving_replay.json').write_text(json.dumps(c.verify(raw,cert,**task),indent=2)+'\n')
integer_keys=['n','event_lower','event_upper','precision_bits','max_record_steps','max_dp_updates','max_exp_terms','max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits','max_grid','max_points','max_cutoff','max_precision','max_operations','max_integer_bits']
for key in integer_keys:
 for alias in [True,1.0,None,-1]:
  tt=dict(task);tt[key]=alias;unknown(lambda tt=tt:c.certify(raw,**tt),'strict external integer types')
for key in c.RATKEYS+['jitter_error']:
 for alias in [True,1,1.0,float('nan'),F(0),F(-1)]:
  tt=dict(task);tt[key]=alias;unknown(lambda tt=tt:c.certify(raw,**tt),'strict external exact rational types')
for key,value in [('max_record_steps',1),('max_dp_updates',1),('max_exp_terms',1),('max_dimension',1),('max_grid',32),('max_points',1),('max_cutoff',1),('max_precision',1),('max_operations',1),('max_integer_bits',1)]:
 tt=dict(task);tt[key]=value
 if key=='max_record_steps':tt['n']=2
 unknown(lambda tt=tt:c.certify(raw,**tt),'finite paid-budget UNKNOWN')
for bad in [dict(event_lower=2),dict(event_upper=2),dict(path_error=F(1)),dict(jitter_error=F(1)),dict(query_absolute_width=F(2)),dict(x=F(1,10**100),precision_bits=16)]:
 tt=dict(task);tt.update(bad);unknown(lambda tt=tt:c.certify(raw,**tt),'scope/width/short-lag UNKNOWN')
for key in ['record_TV_error_upper','global_spectral_error_upper','reference_flip_rate','physical_horizon','jump_time_tolerance','global_odd_source_inverse_per_mass_upper']:
 cc=deepcopy(cert);cc[key]='0';unknown(lambda cc=cc:c.verify(raw,cc,**task),'strict new global/path certificate endpoint binding')
for where in ['task','event','acquisition']:
 cc=deepcopy(cert)
 if where=='task':cc['task']['n']=True
 elif where=='event':cc['event']['lower_count']=False
 else:cc['mean_engine_certificate']['acquisition']['transverse_SPD_everywhere']=1
 unknown(lambda cc=cc:c.verify(raw,cc,**task),'recursive typed binding rejects numeric aliases')
cc=deepcopy(cert);cc['event']['actual_probability']['lower']='1';unknown(lambda:c.verify(raw,cc,**task),'actual event interval cannot be forged')
cc=deepcopy(cert);cc['event']['actual_probability']['display']=['diagnostic','only'];cc['seconds']=None;cc['work']={}
ok(c.verify(raw,cc,**task)['status']=='PASS','non-proof displays/counters/timing explicitly ignored')
rr=deepcopy(raw);rr['energy_terms'][0]['coefficient']='2';unknown(lambda:c.verify(rr,cert,**task),'actual model hash/coefficient binding')
tt=dict(task);tt['x']=F(2);unknown(lambda:c.verify(raw,cert,**tt),'external deterministic schedule binding')
tt=dict(task);tt['event_lower']=1;unknown(lambda:c.verify(raw,cert,**tt),'external event binding')

# Actual production recaptures: same model and once-only initial law as the old
# 513D kinetic service; later queries do not regenerate or reset a trajectory.
rows=json.loads(Path('results.json').read_text());production=[];failures=[]
rawbig=c.fixture()
for row in rows:
 record=row['certificate'];taskbig=c.external_from_record(record)
 new=c.certify(rawbig,**taskbig)
 ok(c.base.same(c.proof_record(record),c.proof_record(new)),'actual production certificate full recomputation')
 ok(new['mean_engine_certificate']['acquisition']['raw_sha256']=='e693d5c1ccf5fe43336f3e845d78fdad3a308d0fe88094cc8c4688a5caca76ff','same accepted 513D raw model, not new favorable fixture')
 production.append({'name':row['name'],'status':'PASS','record_TV_error_upper':new['record_TV_error_upper'],'continuous_jitter_failure_upper':new['continuous_jitter_failure_upper']})
 # Full rerun of a stronger externally requested target: retain honest refusal.
 tt=dict(taskbig)
 if row['name'].startswith('ten'):tt['path_error']=F(1,10)
 else:tt['jitter_error']=F(1,10)
 try:c.certify(rawbig,**tt)
 except c.Unknown as e:ok(True,'actual sharper production request refused');failures.append({'name':row['name'],'changed_task':{k:c.fs(v)if type(v)is F else v for k,v in tt.items()},'status':'UNKNOWN','reason':str(e)})
 else:raise AssertionError('false stronger-width production PASS')
Path('honest_refusals.json').write_text(json.dumps(failures,indent=2)+'\n')
report={'status':'PASS','checks':checks,'categories':categories,'production_replays':production,'scope':'exact algebra and executable regressions, not replacement of the written continuum proof'}
Path('check_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':checks,'categories':categories},indent=2))
