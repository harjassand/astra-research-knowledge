"""Fresh exact tests. Candidate used only as constructor; no candidate fixture/state helpers.
Finite tests corroborate separately recorded proof, not an unbounded-tail argument.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,combinations
import importlib.util,random,json,hashlib,time,os,copy
START=time.perf_counter();HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent if (HERE.parent/'multipartite_seed.py').exists() else HERE.parent/'stochastic_multipartite_seed_pending_20261031'
OUT=Path(os.environ.get('AUDIT_OUTPUT_DIR',str(HERE)));OUT.mkdir(parents=True,exist_ok=True)
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('candidate_under_test',SOURCE/'multipartite_seed.py');I=load('separate_receiver',SOURCE/'independent_audit/independent_multipartite_receiver.py')
RNG=random.Random(31105545)
COUNT=dict(states=0,enabled_internal_jumps=0,strict_boundary_states=0,boundary_destination_ties=0,global_max_switches=0,core_last_seed_deaths=0,outside_Foster_states=0,cone_states=0,master_checks=0,receiver_acceptances=0,graphs=0,graph_admissions=0,domain_refusals=0,structural_refusals=0,normalization_controls=0,extreme_states=0,radial_only_checks=0,free_passenger_checks=0)
TABLE=set()
def wire(x):
 if isinstance(x,Q):return str(x)
 if isinstance(x,dict):return {str(k):wire(v) for k,v in x.items()}
 if isinstance(x,(tuple,list,set)):return [wire(v) for v in x]
 return x

def build(n,a,parts=None,edges=None,full=False,varied=True):
 def v(*ix):return tuple(ix.count(i) for i in range(n))
 def rate():return Q(RNG.choice([1,2,3,5,7]),RNG.choice([1,2,3])) if varied else Q(1)
 if edges is None:edges=[(i,j) for pi,p in enumerate(parts) for q in parts[pi+1:] for i in p for j in q]
 hubs=[v(i,j) for i,j in edges];raw=[(v(),v(a),rate()),(v(a),v(),rate())]
 for h in hubs:raw.extend([(v(a,a),h,rate()),(h,v(a,a),rate())])
 for x in range(n):
  if x==a or not hubs:continue
  selected=hubs if full else RNG.sample(hubs,min(len(hubs),RNG.choice([1,2])))
  for h in selected:raw.extend([(v(a,x),h,rate()),(h,v(a,x),rate())])
 return raw

def prop(x,u,k):
 for xx,uu in zip(x,u):
  if xx<uu:return Q(0)
  for j in range(uu):k*=xx-j
 return k

def checker(raw,a,parts,t,cert):
 co=cert['constants'];eta,eps=co['eta'],co['epsilon'];n=len(raw[0][0]);lam,mu=raw[0][2],raw[1][2]
 kX={i:Q(0) for i in range(n) if i!=a};aa=Q(0);bs={};ss={};S=Q(0)
 for u,v,k in raw:
  if sum(u)!=sum(v):continue
  S+=k
  if u[a]==2:aa+=k
  elif u[a]==1:kX[next(i for i in kX if u[i])]+=k
  else:
   ss[u]=ss.get(u,Q(0))+k
   if v[a]==2:bs[u]=k
 assert co['S']==S and co['a_sum']==aa and co['kminus']==min(kX.values()) and co['kplus']==max(kX.values())
 assert co['F0']==2*aa+max(kX.values()) and co['bmin']==min(bs.values()) and co['smax']==max(ss.values()) and co['b0']==min(ss[u]+bs[u] for u in ss)
 assert 0<eta<=Q(1,16) and 0<eps<=Q(1,2) and eps*co['F0']<=co['D']/4
 assert co['Nstar']>=1 and co['kappa']*co['Nstar']>=co['Cint']+1
 def geo(x):
  N=sum(x);A=x[a];z=tuple(sum(x[i] for i in p) for p in parts);M=max(z);R=N-M;P=(1+eta)*R-eta*A
  return N,A,z,M,R,P
 def h(x):
  N,A,z,M,R,P=geo(x)
  return 4*t if not R else 1+1/P-eps*Q(A,N+1)
 def check(x):
  N,A,z,M,R,P=geo(x);hx=h(x);inv=la=full=core=Q(0);Qhub=sum(z[i]*z[j] for i in range(len(z)) for j in range(i+1,len(z)))
  assert Q(1,2)<=hx<=4*t
  d=z.index(M) if 0<R and 2*R<N else None
  if d is not None:assert z.count(M)==1;COUNT['strict_boundary_states']+=1
  for u,v,k in raw:
   rate=prop(x,u,k)
   if not rate:continue
   y=tuple(xx-uu+vv for xx,uu,vv in zip(x,u,v));NN,AA,zz,MM,RR,PP=geo(y)
   increment=rate*(t**(NN-N)*h(y)-hx);full+=increment
   if NN==N:
    assert R>=1 and RR>=1 and abs(RR-R)<=1 and abs(PP-P)<=1+2*eta
    assert abs(1/PP-1/P)<=6/P**2
    inv+=rate*(1/PP-1/P);la+=rate*(AA-A);COUNT['enabled_internal_jumps']+=1
    if z.index(M)!=zz.index(MM):COUNT['global_max_switches']+=1
    if d is not None:
     assert zz[d]==MM
     if zz.count(MM)>1:COUNT['boundary_destination_ties']+=1
     expected=-(1+eta)*(zz[d]-z[d])-eta*(AA-A);assert PP-P==expected
     isforward=u[a]>0;hub=v if isforward else u;touch=any(hub[i] for i in parts[d])
     if (u if isforward else v)[a]==2:
      label=('seed',isforward,touch);theory=(-1+eta if touch else 2*eta)*(1 if isforward else -1)
     else:
      active=u if isforward else v;species=next(i for i in kX if active[i]);inside=species in parts[d]
      forward_delta=eta if inside and touch else 1+2*eta if inside else -1 if touch else eta
      label=('arm',isforward,touch,inside);theory=forward_delta*(1 if isforward else -1)
     assert PP-P==theory,(x,u,v,label,PP-P,theory);TABLE.add(label)
   else:
    core+=increment
    if NN<N and R==1:assert A==P==1 and RR==0;COUNT['core_last_seed_deaths']+=1
  if not R:
   assert inv==la==0 and full==lam*(t*(2-eps/Q(N+2))-4*t)
   assert full<=-lam*hx/2
  else:
   assert R<=P<=(1+eta)*R and hx<=2
   assert la==-2*aa*A*(A-1)-A*sum(kX[i]*x[i] for i in kX)+sum((ss[u]+bs[u])*prop(x,u,Q(1)) for u in ss)
   assert la>=co['b0']*Qhub-co['F0']*A*N
   assert inv<=6*S*N*N/P**2
   if d is not None:assert inv<=-co['gamma']*M/P+6*S
   assert core<=2*lam*(t-1)-co['D']*A/2+5*mu
   master=co['B']+inv-co['D']*A/4-eps*co['b0']*Qhub/(N+1)
   assert full<=master;COUNT['master_checks']+=1
   if R<=co['delta']*N:assert full<=-1;COUNT['cone_states']+=1
  if N>=co['Nstar']:assert full<=-co['zeta']*hx;COUNT['outside_Foster_states']+=1
  else:assert full+co['zeta']*hx<=cert['Foster']['coefficient']*t
  COUNT['states']+=1
  return full
 return check,geo

CASES=[]
for name,n,a,parts,t,full in [
 ('minimal',3,0,[(1,),(2,)],Q(3,2),False),
 ('full_triangle',4,0,[(1,),(2,),(3,)],Q(2),True),
 ('two_nonsingleton_parts',6,0,[(1,2),(3,),(4,5)],Q(5,4),False),
 ('permuted_222',7,3,[(0,1),(2,4),(5,6)],Q(101,100),False),
 ('five_part_clique',6,2,[(0,),(1,),(3,),(4,),(5,)],Q(4),False),
 ('permuted_star',5,4,[(0,1,2),(3,)],Q(5),True)]:
 raw=build(n,a,parts,full=full);cert=C.numerical(raw,t);assert cert['status']=='CERTIFIED_NUMERICAL'
 assert I.receive_numerical(raw,t,cert) and I.receive_qualitative(raw,C.qualitative(raw));COUNT['receiver_acceptances']+=2
 check,geo=checker(raw,a,parts,t,cert);co=cert['constants'];before=COUNT['states']
 states=list(product(range(3 if n<=4 else 2),repeat=n))
 states += [tuple(RNG.randrange(8) for _ in range(n)) for _ in range(80)]
 # Sharp boundary M=R+1, exact N=2R joins, and max switches/ties, independent of Nstar.
 for R in range(1,7):
  for A in range(min(3,R)+1):
   for offset in [-1,0,1,2]:
    for d in range(len(parts)):
     x=[0]*n;x[a]=A;x[parts[d][0]]=max(0,R+offset);x[parts[(d+1)%len(parts)][0]]=R-A;states.append(tuple(x))
 # Explicit huge count and cone-threshold neighborhoods, no head enumeration.
 for mass in [co['Nstar']-1,co['Nstar'],co['Nstar']+1,10**30]:
  for d in range(len(parts)):
   for A in [0,1,2]:
    for outside in [0,1,2]:
     x=[0]*n;x[a]=A;x[parts[d][0]]=mass;x[parts[(d+1)%len(parts)][0]]=outside;states.append(tuple(x))
  cut=co['delta']*mass/(1-co['delta']);r0=cut.numerator//cut.denominator
  for r in [r0-1,r0,r0+1]:
   for A in [0,1]:
    if r>=A:
     x=[0]*n;x[a]=A;x[parts[0][0]]=mass;x[parts[1][0]]=r-A;states.append(tuple(x))
  for A in [0,1,mass]:
   x=[0]*n;x[a]=A
   for p in parts:x[p[0]]=mass
   states.append(tuple(x))
 for x in states:check(x)
 # Exact radial-only failure on equal occupied parts (q>=3), including every reverse jump.
 if len(parts)>=3:
  for mass in [co['Nstar'],co['Nstar']+1]:
   x=[0]*n
   for part in parts:x[part[0]]=mass
   x=tuple(x);N,A,z,M,R,P=geo(x);radial=Q(0)
   for u,v,k in raw:
    rate=prop(x,u,k)
    if not rate:continue
    y=tuple(xx-uu+vv for xx,uu,vv in zip(x,u,v));NN,AA,zz,MM,RR,PP=geo(y)
    if NN==N:assert PP<P and MM>=M
    radial+=rate*(t**(NN-N)*(1+1/PP)-(1+1/P))
   assert radial>0 and check(x)<0
   COUNT['radial_only_checks']+=1
 # Raw normalization: same math but correctly different input-work counters.
 dup=[]
 for u,v,k in raw:dup.extend([(u,v,k/5),(u,v,4*k/5)])
 dup.append(((0,)*n,(0,)*n,Q(17)));RNG.shuffle(dup);dc=C.numerical(dup,t)
 for field in ['raw_sha256','constants','profile','Foster','stationary_moment','implicit_head_states']:assert cert[field]==dc[field]
 assert I.receive_numerical(dup,t,dc);COUNT['normalization_controls']+=1
 CASES.append(dict(name=name,n=n,a=a,parts=parts,channels=len(raw),states=COUNT['states']-before,Nstar_bits=co['Nstar'].bit_length(),scalar_bits=cert['work']['retained_scalar_bits'],raw_sha256=cert['raw_sha256']))

# Exhaustive graph recognition independently characterized by transitive nonadjacency.
GRAPH=[]
for m in range(2,6):
 edges=list(combinations(range(1,m+1),2));admitted=0
 for mask in range(1<<len(edges)):
  actual={e for j,e in enumerate(edges) if mask>>j&1};nonneighbors={i:frozenset(j for j in range(1,m+1) if j==i or tuple(sorted((i,j))) not in actual) for i in range(1,m+1)}
  equivalence=all(nonneighbors[i]==nonneighbors[j] for i in nonneighbors for j in nonneighbors[i]);expected=equivalence and bool(actual)
  raw=build(m+1,0,edges=sorted(actual),full=True,varied=False);got=C.qualitative(raw)
  assert (got['status']=='CERTIFIED_QUALITATIVE')==expected
  assert I.receive_qualitative(raw,got)
  if expected:
   wanted=sorted(set(nonneighbors.values()),key=lambda p:min(p));assert got['inventory']['parts']==tuple(tuple(sorted(p)) for p in wanted)
   admitted+=1
  COUNT['graphs']+=1
 GRAPH.append(dict(satellites=m,graphs=1<<len(edges),admitted=admitted));COUNT['graph_admissions']+=admitted

# Compound parameter extremes: accepted compactly, no rate-ratio iteration.
EXTREMES=[]
base=build(4,0,[(1,),(2,),(3,)],full=True,varied=False)
for name,t,lam,mu,scale in [
 ('joint_tiny_death_near_one',1+Q(1,10**250),Q(1,10**150),Q(1,10**750),Q(1)),
 ('huge_t_reverse',Q(10**120),Q(10**100),Q(1,10**100),Q(10**400)),
 ('tiny_amplification',Q(3,2),Q(1),Q(1),Q(1,10**500))]:
 raw=[]
 for u,v,k in base:
  if sum(u)==0:k=lam
  elif sum(v)==0:k=mu
  elif u[0]==0 and ((name=='tiny_amplification' and v[0]==2) or (name=='huge_t_reverse' and v[0]==1)):k=scale
  raw.append((u,v,k))
 cert=C.numerical(raw,t);assert I.receive_numerical(raw,t,cert);COUNT['receiver_acceptances']+=1
 assert cert['work']['rate_dependent_iterations']==cert['work']['profile_recurrence_steps']==cert['work']['expanded_Foster_powers']==0
 check,geo=checker(raw,0,[(1,),(2,),(3,)],t,cert);mass=cert['constants']['Nstar']
 for x in [(0,mass,0,0),(1,mass,0,0),(0,mass,1,0),(0,mass,mass,mass),(2,mass,1,0),(mass,0,0,0)]:check(x);COUNT['extreme_states']+=1
 text=C.canonical(cert);assert I.receive_numerical(raw,t,json.loads(text))
 EXTREMES.append(dict(name=name,wire_bytes=len(text.encode()),Nstar_bits=mass.bit_length(),scalar_bits=cert['work']['retained_scalar_bits'],wire_sha256=hashlib.sha256(text.encode()).hexdigest()))

# Strict domains, including subclasses and invalid numerical domain before UNKNOWN.
class IntChild(int):pass
class FractionChild(Q):pass
def refuse(label,fn):
 try:fn()
 except (ValueError,TypeError):COUNT['domain_refusals']+=1;return
 raise AssertionError(label)
for val in [0,-1,True,False,1.0,float('nan'),float('inf'),'1',None,IntChild(1),FractionChild(1)]:
 rr=copy.deepcopy(base);u,v,k=rr[0];rr[0]=(u,v,val)
 for fn in [C.qualitative,I.qualitative]:refuse('rate '+repr(val),lambda fn=fn,rr=rr:fn(rr))
for val in [0,1,-1,Q(1,2),True,False,2.0,'2',None,IntChild(2),FractionChild(2)]:
 for fn in [C.numerical,I.numerical]:refuse('t '+repr(val),lambda fn=fn,val=val:fn(base,val))
for val in [-1,True,False,1.0,Q(1),'1',None,IntChild(1)]:
 rr=copy.deepcopy(base);u,v,k=rr[0];u=list(u);u[1]=val;rr[0]=(u,v,k)
 for fn in [C.qualitative,I.qualitative]:refuse('coordinate '+repr(val),lambda fn=fn,rr=rr:fn(rr))
for rr in [[],None,{},iter(base),[(base[0][0],base[0][1])],[(base[0][0],base[0][1][:-1],1)]]:
 # Generator is invalid regardless of whether any consumer has already tried it.
 for fn in [C.qualitative,I.qualitative]:refuse('raw shape',lambda fn=fn,rr=rr:fn(rr))
for fn in [C.numerical,I.numerical]:refuse('domain before UNKNOWN',lambda fn=fn:fn([((0,0,0),(1,0,0),1)],True))

# Valid syntax but structural refusal; no instability conclusion.
aa=(2,0,0,0);hub=(0,1,1,0);arm=(1,1,0,0)
negatives=[('absent_amplification',[row for row in base if (row[0],row[1]) not in [(aa,hub),(hub,aa)]]),('uncovered_arm',[row for row in base if row[0]!=arm and row[1]!=arm]),('nonreversible',base[:-1]),('active_active',base+[(aa,arm,1),(arm,aa,1)]),('square_hub',base+[(aa,(0,2,0,0),1),((0,2,0,0),aa,1)]),('extra_port',base+[((0,0,0,0),(0,1,0,0),1),((0,1,0,0),(0,0,0,0),1)]),('nonbinary',base+[((3,0,0,0),(0,3,0,0),1),((0,3,0,0),(3,0,0,0),1)])]
UNKNOWN=[]
for name,raw in negatives:
 got=C.qualitative(raw);assert got['status']=='UNKNOWN' and got['stability']=='UNKNOWN' and I.receive_qualitative(raw,got)
 COUNT['structural_refusals']+=1;UNKNOWN.append(dict(name=name,reason=got['reason']))

# Extrapolated candidate on a free-passenger ray: an explicit formula failure, not instability.
for t in [Q(2),1+Q(1,10**100)]:
 for eta in [Q(0),Q(1,16)]:
  mass=10**110;epsilon=Q(1,4);P=(1+eta)*mass
  radial=1+1/P
  scaled=t*(1+1/(P+1)-epsilon/Q(mass+2))-radial
  assert scaled>0;COUNT['free_passenger_checks']+=1

RESULT=dict(status='PASS',scope='Fresh finite exact controls; ordinary proof separately reviewed',source_sha256=hashlib.sha256((SOURCE/'multipartite_seed.py').read_bytes()).hexdigest(),counts=COUNT,boundary_channel_subcases=sorted(map(str,TABLE)),cases=CASES,graph_controls=GRAPH,compound_parameter_extremes=EXTREMES,structural_unknowns=UNKNOWN,seconds=time.perf_counter()-START,no_simulation=True,no_exception_enumeration=True,no_Foster_power_expansion=True)
(OUT/'INDEPENDENT_ADVERSARIAL_RESULTS.json').write_text(json.dumps(wire(RESULT),indent=2)+'\n');print(json.dumps(wire(RESULT),indent=2))
