"""Exact author checks; --skip-saved runs unit checks without the costly saved replays."""
from fractions import Fraction as F
from copy import deepcopy
from pathlib import Path
from math import comb
import json,random,sys
import receive_robustness as c
checks=0;categories={}
def ok(v,label):
 global checks
 assert v,label
 checks+=1;categories[label]=categories.get(label,0)+1

def unknown(fn,label):
 try:fn()
 except c.Unknown:ok(True,label)
 else:raise AssertionError('unexpected admission: '+label)

def val(p,t):
 z=F(0)
 for q in reversed(p):z=z*t+q
 return z
rng=random.Random(9917)
for _ in range(2400):
 x=F(rng.randint(1,100),rng.randint(1,100));n=rng.randint(-31,31);d=rng.choice([1,2,4]);P=rng.randint(3,100)
 ii=c.Integrator(1,F(1),4,F(1,100),'critical_flat',P,100,100000)
 lo,hi=ii.bounds(x,n,d)
 ok(F(lo,1<<P)**d<=x**n<=F(hi,1<<P)**d,'outward fixed-point power/root');ok(0<=lo<=hi,'nonnegative ordered enclosure')
for D in range(1,13):
 for _ in range(20):
  p=[F(rng.randint(-9,9)) for j in range(D+1)];x=F(rng.randint(1,19),20);t=x/(1-x)
  B=sum((p[j]/comb(D,j))*comb(D,j)*x**j*(1-x)**(D-j) for j in range(D+1))
  ok(B==(1-x)**D*val(p,t),'projective Bernstein identity')
for p in [[F(1)],[F(0)],[F(1),F(-2),F(1)],[F(1),F(-2),F(2)],c.ppow([F(1),F(-1)],4)]:
 c.Bernstein(1000,16,10000).positive(p);ok(True,'positive polynomial certificate')
for _ in range(160):
 p=[F(rng.randint(-5,5)) for j in range(rng.randint(1,7))]
 neg=any(val(p,F(j,7))<0 for j in range(51))
 try:c.Bernstein(10000,12,100000).positive(p)
 except c.Unknown:ok(True,'bounded polynomial refusal or certificate')
 else:ok(not neg,'no false polynomial PASS on exact witnesses')
unknown(lambda:c.Bernstein(10,1,10000).positive([F(4),F(-4),F(1)]),'positive square can be bounded UNKNOWN')
unknown(lambda:c.Bernstein(100,16,10000).positive([F(10**12-1),F(-2*10**6),F(1)]),'remote narrow negative region rejected')
# Exact derivative brackets and both profile maxima, including tails.
for shape in ['well_sensitive','critical_flat']:
 for k in [F(1,100),F(1),F(100)]:
  delta=k/(2*(1+k))
  for j in range(101):
   t=F(j,7);s=1+k*(1-t)**2;s0=1+k
   if shape=='well_sensitive':e=t/(1+t)**2;et=(1-t)/(1+t)**3
   else:e=t*(t-1)**2/(1+t)**4;et=-(t-1)*(t*t-6*t+1)/(1+t)**5
   ok(0<=e<=c.error_max(shape),'exact profile sup bound')
   for sign in [-1,1]:
    derivative=2*k*(t-1)*(1+sign*delta*e)+sign*delta*s*et
    ok(derivative*(t-1)>=0,'profile monotonicity')
   h=min(F(1,8),k/2)*(1-delta*c.error_max(shape))
   ok(s*(1-delta*e)>=h*(1+t)**2,'global Lyapunov lower profile')
# Outward tail rounding is paid and cannot reduce the analytic bound.
for m in [1,2,7,32]:
 for shape in ['well_sensitive','critical_flat']:
  ii=c.Integrator(m,F(3,2),4,F(1,500),shape,256,100,100000)
  for T in [F(2),F(4),F(8)]:
   exact=F(3,2)**(-m)*(1-1/(T*T))**(-2*m)*T**(1-4*m)/(4*m-1)
   for kind in ['ql','qu']:
    z=exact/(1-F(1,500)*c.error_max(shape))**m if kind=='ql' else exact
    u=ii.tail(T,kind)
    ok(z<=u<z+F(1,2**256),'analytic tail rounded outward')

# Fully raw acquisition, without provided useful axis or kappa.
for m in [1,2,3]:
 for axis in range(m+1):
  for shape in ['well_sensitive','critical_flat']:
   raw=c.fixture(m,shape=shape,kappa=F(3,2),axis=axis);a=c.acquire(raw,F(1,500),shape)
   ok(a['axis']==axis and F(a['kappa'])==F(3,2) and a['m']==m,'acquired axis and nominal parameter')
   ok(F(a['anchor_q_min'])>0 and F(a['lyapunov_K'])>1,'acquired coercivity/nonexplosion')
raw=c.fixture(2);a=c.acquire(raw,F(1,500),'critical_flat')
ok(a['distinct_normalized_profiles']<a['quadratic_atoms']+a['quartic_atoms'],'ordinary normalized-profile proof reuse')
# Saturated heterogeneous profiles: fixture uses half its delta, so2delta reaches the envelope.
r=c.fixture(2,delta=F(1,250));ok(c.acquire(r,F(1,500),'critical_flat')['delta']=='1/500','boundary defects actually admitted')
unknown(lambda:c.acquire(r,F(1,1000),'critical_flat'),'too tight defect budget refused')
# Generic polynomial profile that is NOT an assumed r_j=s(1+e_j e) identity.
r=c.fixture(2,delta=F(0));terms={tuple(x['powers']):F(x['coefficient']) for x in r['terms']}
Q=c.scale(c.mul(c.ppow([F(2),F(-2),F(1)],2),c.mul(c.error_numerator('critical_flat'),c.ppow([F(1),F(1)],12))),F(1,1000))
for j,q in enumerate(Q):
 if q:
  v=(2*j,2,0);terms[v]=terms.get(v,F(0))+q
r['terms']=[{'powers':list(v),'coefficient':c.fs(q)} for v,q in terms.items() if q]
ok(c.acquire(r,F(1,500),'critical_flat')['quadratic_atoms']==2,'inequality admission beyond fixture identity')
# Actual tiny tail violation is not inferred safe from bounded samples.
r=deepcopy(raw);r['terms'].append({'powers':[42,2,0],'coefficient':'1/1000000000000'})
unknown(lambda:c.acquire(r,F(1,500),'critical_flat'),'unbounded tail outside envelope grammar')
for bad in [None,[],dict(raw,extra=True),dict(raw,n=True),dict(raw,n=3.0)]:unknown(lambda bad=bad:c.acquire(bad,F(1,500),'critical_flat'),'strict raw schema')
for den in [{'axis':False,'power':16},{'axis':0,'power':16.0},{'axis':1,'power':16},{'axis':0,'power':15}]:
 r=deepcopy(raw);r['denominator']=den;unknown(lambda r=r:c.acquire(r,F(1,500),'critical_flat'),'actual denominator binding')
for v in [True,1.0,'1.0','01','2/2','nan','0','1/0']:
 r=deepcopy(raw);r['terms'][0]['coefficient']=v;unknown(lambda r=r:c.acquire(r,F(1,500),'critical_flat'),'strict coefficient syntax')
for v in [True,1.0,-1,53]:
 r=deepcopy(raw);r['terms'][0]['powers'][0]=v;unknown(lambda r=r:c.acquire(r,F(1,500),'critical_flat'),'strict exponent syntax')
r=deepcopy(raw);r['terms'].append(deepcopy(r['terms'][0]));unknown(lambda:c.acquire(r,F(1,500),'critical_flat'),'duplicate raw term')
r=deepcopy(raw);r['terms'].append({'powers':[1,2,0],'coefficient':'1'});unknown(lambda:c.acquire(r,F(1,500),'critical_flat'),'odd-y symmetry not assumed')
r=deepcopy(raw);r['terms'].append({'powers':[0,1,1],'coefficient':'1'});unknown(lambda:c.acquire(r,F(1,500),'critical_flat'),'unknown rotated/off-diagonal atom')
# Uniform angular rescaling changes unknown partition, not the acquired defect.
small=c.fixture(1);cert=c.certify(small,delta=F(1,500))
scaled=c.certify(c.fixture(1,angular_scale=F(10**40)),delta=F(1,500))
for key in ['mass_lower_profile','mass_upper_profile','resistance_lower_profile','jensen_upper_profile','uniform_rate_enclosure']:
 ok(cert[key]==scaled[key],'irrelevant angular scale not charged')
# Pure quadratic is retained with degree2, and exact dilation is delta0.
cq=c.certify(c.fixture(1,delta=F(0),mixed=False),delta=F(0))
ok(cq['acquisition']['degree_cap']==2,'strong quadratic comparator')
ok(c.verify(c.fixture(1,delta=F(0),mixed=False),cq,delta=F(0))['status']=='PASS','zero-defect receiving')
for kw in [dict(delta=.002),dict(delta=True),dict(delta=F(-1)),dict(shape=None),dict(shape=True),dict(beta=1),dict(beta=float('nan')),dict(quad_relative=F(0)),dict(full_ratio=1.01),dict(full_ratio=F(1))]:
 task=dict(delta=F(1,500));task.update(kw);unknown(lambda task=task:c.certify(raw,**task),'strict external task')
for key in ['max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_bernstein_nodes','max_bernstein_depth','max_bernstein_bits','max_grid','max_evaluations','max_cutoff','max_precision','max_power_bits']:
 for v in [True,0,1.5]:unknown(lambda key=key,v=v:c.certify(raw,delta=F(1,500),**{key:v}),'strict receiving budgets')
for kw in [dict(max_dimension=2),dict(max_terms=10),dict(max_exponent_entries=20),dict(max_total_coefficient_bits=10),dict(max_coefficient_bits=2),dict(max_bernstein_nodes=1),dict(max_bernstein_bits=4),dict(max_grid=63),dict(max_grid=64),dict(max_evaluations=5),dict(max_cutoff=1),dict(max_precision=100),dict(max_power_bits=10),dict(full_ratio=F(1000001,1000000))]:
 unknown(lambda kw=kw:c.certify(raw,delta=F(1,500),**kw),'finite budget/total-width UNKNOWN')
# Strict raw/task/model receiving, including nested aliases and altered valid inputs.
for key,value in [('schema','wrong'),('dependency_sha256','0'*64),('observable','MFPT'),('basins','partial fibers'),('N',float(cert['N'])),('precision_bits',True),('full_ratio_exact','1')]:
 cc=deepcopy(cert);cc[key]=value;unknown(lambda cc=cc:c.verify(small,cc,delta=F(1,500)),'original model/task binding')
for key,value in [('axis',False),('m',True),('bernstein_nodes',float(cert['acquisition']['bernstein_nodes'])),('delta',.002),('anchor_q_min','0'),('lyapunov_K','1'),('raw_potential_sha256','0'*64)]:
 cc=deepcopy(cert);cc['acquisition'][key]=value;unknown(lambda cc=cc:c.verify(small,cc,delta=F(1,500)),'typed acquired proof binding')
for key in cert['mobility_family']:
 cc=deepcopy(cert);cc['mobility_family'][key]='wrong';unknown(lambda cc=cc:c.verify(small,cc,delta=F(1,500)),'kinetic family binding')
for key in ['mass_lower_profile','mass_upper_profile','resistance_lower_profile','jensen_upper_profile','uniform_rate_enclosure']:
 for side in ['lower','upper']:
  cc=deepcopy(cert);cc[key][side]=c.fs(F(cc[key][side])+F(1,77));unknown(lambda cc=cc:c.verify(small,cc,delta=F(1,500)),'exact endpoint binding')
unknown(lambda:c.verify(c.fixture(1,angular_scale=F(2)),cert,delta=F(1,500)),'changed valid raw input bound')
unknown(lambda:c.verify(small,cert,delta=F(1,400)),'changed external defect hypothesis')
cc=deepcopy(cert);cc['seconds']='untrusted';cc['scalar_evaluations']=False;cc['uniform_rate_enclosure']['lower_display']='untrusted'
ok(c.verify(small,cc,delta=F(1,500))['status']=='PASS','diagnostics not proof fields')
tiny=c.certify(small,delta=F(1,500),beta=F(1,2**2000));ok(tiny['uniform_rate_enclosure']['lower_display']is None,'display overflow remains optional')
replays=[]
if '--skip-saved' not in sys.argv:
 for row in json.loads(Path('results.json').read_text()):
  cert=row['certificate'];task=cert['task'];external={k:(F(v) if k in ['delta','beta','quad_relative','full_ratio'] and v is not None else v) for k,v in task.items()}
  raw=c.fixture(row['m'],F(task['delta']),task['shape']);out=c.verify(raw,cert,**external)
  ok(out['status']=='PASS','actual saved full replay');replays.append({'m':row['m'],'shape':task['shape'],'status':'PASS'})
  if task['full_ratio']is not None:ok(F(out['full_ratio_exact'])<=F(task['full_ratio']),'requested total width received')
 ok(c.verify(json.loads(Path('small_raw_fixture.json').read_text()),json.loads(Path('small_certificate.json').read_text()),delta=F(1,500))['status']=='PASS','saved nonfirst axis replay')
report={'status':'PASS','checks':checks,'categories':categories,'saved_replays':replays,'scope':'Exact receiving tests supplement ordinary proofs; no physical membership or MFPT claim.'}
Path('unit_check_results.json' if '--skip-saved'in sys.argv else 'check_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
