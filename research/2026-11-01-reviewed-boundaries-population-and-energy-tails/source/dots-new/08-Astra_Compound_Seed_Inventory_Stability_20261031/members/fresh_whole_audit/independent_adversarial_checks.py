"""Independent raw-state and domain audit; author used only as constructor under test.
No author inventory, profile, propensity, drift, fixture, or local-test helper is used.
Deterministic finite controls supplement, and do not replace, the ordinary proof audit.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import sys,importlib.util,random,json,time,hashlib,copy,os
START=time.perf_counter(); HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('AUDIT_OUTPUT_DIR',str(HERE)));ROOT.mkdir(parents=True,exist_ok=True)
SOURCE=HERE.parent if (HERE.parent/'compound_seed.py').exists() else HERE.parent/'stochastic_compound_seed_pending_20261031'
spec=importlib.util.spec_from_file_location('under_test',SOURCE/'compound_seed.py'); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
ispec=importlib.util.spec_from_file_location('separate_receiver',SOURCE/'independent_audit/independent_receiver.py'); I=importlib.util.module_from_spec(ispec);ispec.loader.exec_module(I)
RNG=random.Random(31102026)
COUNTS=dict(states=0,enabled_jumps=0,outside_head_states=0,profile_points=0,core_scalar_checks=0,domain_refusals=0,unsupported_families=0,metamorphic_checks=0,independent_receiver_checks=0)

def serial(o):
 if isinstance(o,Q):return str(o)
 if isinstance(o,dict):return {str(k):serial(v) for k,v in o.items()}
 if isinstance(o,(tuple,list)):return [serial(v) for v in o]
 return o

def raw_case(n,a,parts,random_rates=True):
 def v(*ix):return tuple(ix.count(i) for i in range(n))
 def rate():return Q(RNG.choice([1,2,3,5]),RNG.choice([1,2])) if random_rates else Q(1)
 raw=[(v(),v(a),rate()),(v(a),v(),rate())]
 hubs=[v(i,j) for left,right in parts for i in left for j in right]
 for h in hubs:raw.extend([(v(a,a),h,rate()),(h,v(a,a),rate())])
 # Minimal sparse coverage, not the author's all-incidence fixture.
 for i in range(n):
  if i==a:continue
  selected=RNG.sample(hubs,1 if len(hubs)==1 else RNG.choice([1,2]))
  for h in selected:raw.extend([(v(a,i),h,rate()),(h,v(a,i),rate())])
 return raw

def inventory(x,a,parts):return x[a]+sum(min(sum(x[i] for i in left),sum(x[i] for i in right)) for left,right in parts)
def propensity(x,u,k):
 for xi,ui in zip(x,u):
  if xi<ui:return Q(0)
  for j in range(ui):k*=xi-j
 return k

def audit_case(name,n,a,parts,t):
 raw=raw_case(n,a,parts); cert=mod.numerical(raw,t,max_profile_steps=100000)
 assert cert['status']=='CERTIFIED_NUMERICAL',name
 assert I.receive_numerical(raw,t,cert) and I.receive_qualitative(raw,mod.qualitative(raw))
 COUNTS['independent_receiver_checks']+=2
 co=cert['constants']; head=cert['profile']['head']; q=co['q'];K,J=co['K'],co['J']
 def g(r):return head[r] if r<len(head) else 1+co['c']/Q(r)
 def d(r):return g(r)-g(r+1)
 lam=raw[0][2];mu=raw[1][2]
 def h(x):
  r=inventory(x,a,parts);return g(r)+q*Q(x[a],(sum(x)+1)*(r+1)**2)
 assert len(head)==K+1 and g(0)==2*t*g(1)
 assert all(g(r)>g(r+1)>1 for r in range(K+2))
 assert co['epsilon']==min(Q(1),(lam+co['beta'])/2)
 assert co['Nstar']>=max(1,4*J,q,22*q*co['sratio']/co['dstar'],2*q*co['Ce']/co['epsilon'])
 for r in list(range(1,J+2))+[10**6,10**30]:
  assert lam*(t*g(r+1)-g(r))-co['beta']*r*r*d(r)<=-co['epsilon']*g(r)
  assert (r+1)**2*d(r)>=co['dstar']
  E=mu*(g(r-1)/t-g(r))+co['Kf']*r*d(r-1)+2*co['beta']*r*d(r)
  if r<J:assert q*co['kminus']/(4*(r+1)**2)>=max(E,0)
  else:assert E<=-co['D']/2
  COUNTS['profile_points']+=1
 # Exhaustive tiny states, random small states, and large adversarial exact faces.
 states=list(product(range(3 if n<=4 else 2),repeat=n))
 states += [tuple(RNG.randrange(12) for _ in range(n)) for _ in range(100)]
 for size in [co['Nstar']-1,co['Nstar'],co['Nstar']+1,10**30]:
  for axis in range(n):
   for active in [0,1,2,K-1,K,J-1,J,J+1]:
    x=[0]*n;x[axis]=size;x[a]+=active;states.append(tuple(x))
  for level in [1,K-1,K,J-1,J]:
   x=[level]*n;x[a]=0;x[next(i for i in range(n) if i!=a)]+=size;states.append(tuple(x))
 for x in states:
  N=sum(x); r=inventory(x,a,parts); A=x[a];fv=Q(A,(r+1)**2)
  lintf=lintg=drift=corecorr=Q(0);bad=neutral=bsum=ssum=Q(0)
  for u,v,k in raw:
   rate=propensity(x,u,k)
   if not rate:continue
   y=tuple(xi-ui+vi for xi,ui,vi in zip(x,u,v));rr=inventory(y,a,parts)
   fp=Q(y[a],(rr+1)**2);delta=sum(v)-sum(u)
   drift+=rate*(t**delta*h(y)-h(x));COUNTS['enabled_jumps']+=1
   if delta:
    corecorr+=rate*q*(t**delta*fp/(sum(y)+1)-fv/(N+1))
   else:
    assert r>0 and rr>0 and abs(rr-r)<=1
    assert abs(fp-fv)<=Q(11,(r+1)**2)
    lintf+=rate*(fp-fv);lintg+=rate*(g(rr)-g(r))
    if u[a]>0 and rr==r-1:bad+=rate
    if u[a]==1 and rr==r:neutral+=rate
    if not u[a]:
     ssum+=rate
     if v[a]==2:bsum+=rate
  if r:
   assert bad<=co['Kf']*A*r
   assert neutral>=co['kminus']*A*(N-2*r+A)
   assert lintg<=co['Kf']*A*r*d(r-1)-bsum*d(r)
   assert lintf<=-co['kminus']*A*Q(N-2*r+A,(r+1)**2)+11*co['Kf']*Q(r*r,(r+1)**2)+11*ssum/Q((r+1)**2)
   assert corecorr<=q*(12*lam*t+12*mu)/(N+1)
  else:assert lintf==lintg==0
  if N>=co['Nstar']:
   assert drift<=-co['zeta']*h(x),(name,x,drift)
   COUNTS['outside_head_states']+=1
  else:assert drift+co['zeta']*h(x)<=cert['Foster']['coefficient']
  COUNTS['states']+=1
 # Splitting duplicated channels, adding null channels, order changes: same numerical mathematics.
 duplicated=[]
 for u,v,k in raw:duplicated.extend([(u,v,k/3),(u,v,2*k/3)])
 duplicated.append(((0,)*n,(0,)*n,Q(7)))
 RNG.shuffle(duplicated)
 dc=mod.numerical(duplicated,t,max_profile_steps=100000)
 for key in ['raw_sha256','constants','profile','Foster','stationary_moment','implicit_head_states']:assert cert[key]==dc[key]
 COUNTS['metamorphic_checks']+=1
 needed=cert['budget']['required_iterations']
 assert mod.numerical(raw,t,needed-1)['status']=='NUMERICAL_UNKNOWN'
 assert mod.numerical(raw,t,needed)['status']=='CERTIFIED_NUMERICAL'
 COUNTS['metamorphic_checks']+=2
 return dict(name=name,n=n,a=a,parts=parts,channels=len(raw),raw_sha256=cert['raw_sha256'],t=t,K=K,J=J,Nstar=co['Nstar'],retained_scalar_bits=cert['work']['retained_scalar_bits'])

CASES=[]
for args in [('small',3,0,[((1,),(2,))],Q(3,2)),('free',4,0,[((2,),(3,))],Q(2)),('sparse_K22',6,0,[((2,3),(4,5))],Q(3,2)),('cross_components',6,0,[((1,),(2,)),((3,),(4,))],Q(3,2)),('permuted_K22',7,3,[((0,5),(1,6))],Q(3,2)),('near_one',4,1,[((0,),(3,))],Q(101,100))]:
 CASES.append(audit_case(*args))

# Direct scalar physical-core inequality, entirely independent of graph/constructor.
for t in [Q(10001,10000),Q(2),Q(100)]:
 for lam,mu in [(Q(1),Q(1)),(Q(1,10**6),Q(10**6)),(Q(10**6),Q(1,10**6))]:
  for r in range(1,41):
   for a in range(r+1):
    for N in [2*r-a,2*r-a+1,10**12]:
     f=Q(a,(N+1)*(r+1)**2)
     got=lam*(t*Q(a+1,(N+2)*(r+2)**2)-f)
     if a:got+=mu*a*(Q(a-1,N*r*r)/t-f)
     assert got<=(12*lam*t+12*mu)/(N+1)
     COUNTS['core_scalar_checks']+=1

base=raw_case(4,0,[((2,),(3,))],False)
def refused(label,fn):
 try:fn()
 except (TypeError,ValueError):COUNTS['domain_refusals']+=1;return
 raise AssertionError('invalid domain accepted: '+label)
for bad in [0,-1,True,False,1.0,float('inf'),float('nan'),'1',None]:
 rr=copy.deepcopy(base);u,v,k=rr[0];rr[0]=(u,v,bad);refused('rate '+repr(bad),lambda rr=rr:mod.qualitative(rr))
for bad in [True,False,2.0,'2',None,0,1,-1,Q(1,2)]:refused('t '+repr(bad),lambda bad=bad:mod.numerical(base,bad))
for bad in [True,False,2.0,'2',None,-1,Q(3)]:refused('budget '+repr(bad),lambda bad=bad:mod.numerical(base,Q(2),bad))
for bad in [True,False,-1,1.0,Q(1),'1',None]:
 rr=copy.deepcopy(base);u,v,k=rr[0];u=list(u);u[1]=bad;rr[0]=(u,v,k);refused('coordinate '+repr(bad),lambda rr=rr:mod.qualitative(rr))
for rr in [[],{},None,iter(base),[base[0][:2]],[(base[0][0],base[0][1][:-1],1)]]:refused('shape',lambda rr=rr:mod.qualitative(rr))
# Invalid domain is checked even when the raw family is unsupported.
for t,budget in [(True,100),(2,False)]:refused('domain before UNKNOWN',lambda t=t,budget=budget:mod.numerical([((0,0,0),(1,0,0),1)],t,budget))

# Distinct validly-typed families whose stability must remain UNKNOWN.
def unsupported(label,raw):
 got=mod.qualitative(raw);assert got['status']=='UNKNOWN' and got['stability']=='UNKNOWN',(label,got)
 COUNTS['unsupported_families']+=1;return dict(name=label,reason=got['reason'])
UNKNOWN=[]
UNKNOWN.append(unsupported('missing_reverse',base[:-1]))
UNKNOWN.append(unsupported('uncovered_satellite',[r for r in base if r[0]!=(1,1,0,0) and r[1]!=(1,1,0,0)]))
UNKNOWN.append(unsupported('missing_amplification',[r for r in base if r[0]!=(2,0,0,0) and r[1]!=(2,0,0,0)]))
UNKNOWN.append(unsupported('extra_port',base+[((0,0,0,0),(0,1,0,0),1),((0,1,0,0),(0,0,0,0),1)]))
UNKNOWN.append(unsupported('nonbinary',base+[((3,0,0,0),(0,3,0,0),1),((0,3,0,0),(3,0,0,0),1)]))
UNKNOWN.append(unsupported('square_hub',base+[((2,0,0,0),(0,0,2,0),1),((0,0,2,0),(2,0,0,0),1)]))
UNKNOWN.append(unsupported('hub_to_hub',base+[((0,1,1,0),(0,0,1,1),1),((0,0,1,1),(0,1,1,0),1)]))
UNKNOWN.append(unsupported('active_to_active',base+[((2,0,0,0),(1,1,0,0),1),((1,1,0,0),(2,0,0,0),1)]))
# Construct non-biclique hub graphs using singleton edge components without presupposing valid partitioning.
UNKNOWN.append(unsupported('induced_P4',raw_case(5,0,[((1,),(2,)),((2,),(3,)),((3,),(4,))],False)))
UNKNOWN.append(unsupported('triangle',raw_case(4,0,[((1,),(2,)),((2,),(3,)),((3,),(1,))],False)))
for t in [Q(10**30),Q(2)]:
 rr=copy.deepcopy(base)
 if t==2:u,v,k=rr[1];rr[1]=(u,v,Q(1,10**30))
 c=mod.numerical(rr,t,100000);assert c['status']=='NUMERICAL_UNKNOWN' and c['qualitative']['status']=='CERTIFIED_QUALITATIVE';assert c['work']=={'profile_recurrence_steps':0,'finite_head_checks':0}
 COUNTS['metamorphic_checks']+=1

RESULT=dict(status='PASS',scope='independent finite controls plus separately recorded ordinary proof audit; not a standalone receiver',source_sha256=hashlib.sha256((SOURCE/'compound_seed.py').read_bytes()).hexdigest(),counts=COUNTS,cases=CASES,unknown_controls=UNKNOWN,seconds=time.perf_counter()-START,no_simulation=True,no_Foster_power_expansion=True,no_exception_state_enumeration=True)
(ROOT/'INDEPENDENT_ADVERSARIAL_RESULTS.json').write_text(json.dumps(serial(RESULT),indent=2)+'\n')
print(json.dumps(serial(RESULT),indent=2))
