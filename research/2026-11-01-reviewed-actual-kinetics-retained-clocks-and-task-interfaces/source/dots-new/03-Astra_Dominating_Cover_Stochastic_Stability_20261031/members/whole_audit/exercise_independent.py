"""Fresh whole-state/graph/receiving checks, separate from candidate test helpers."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations,product,permutations
import importlib.util,random,json,time,copy,os,hashlib
import independent_cover_receiver as I
START=time.perf_counter();HERE=Path(__file__).resolve().parent
SOURCE=Path(os.environ['COVER_SOURCE_DIR']) if os.environ.get('COVER_SOURCE_DIR') else next(p for p in [HERE.parent/'frozen_cover_source',HERE.parent,HERE.parent/'stochastic_cover_seed_pending_20261031'] if (p/'cover_seed.py').exists())
OUT=Path(os.environ.get('AUDIT_OUTPUT_DIR',str(HERE)));OUT.mkdir(parents=True,exist_ok=True)
s=importlib.util.spec_from_file_location('candidate_under_test',SOURCE/'cover_seed.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
RNG=random.Random(202610312235)
COUNTS=dict(states=0,internal_jumps=0,cover_switches=0,optimal_cover_ties=0,reverse_arm_decrements=0,heavy_captures=0,heavy_bounds=0,profile_checks=0,boundary_states=0,interior_states=0,outside_Foster=0,last_seed_deaths=0,raw_receipts=0,semantic_mutations=0,budget_controls=0,domain_refusals=0,normalization_controls=0,qualitative_no_cover_calls=0)

def raw_graph(n,a,edges,full=False,unit=False):
 def vec(*ids):return tuple(ids.count(i) for i in range(n))
 hubs=[vec(i,j) for i,j in edges];raw=[(vec(),vec(a),Q(1) if unit else Q(1,2)),(vec(a),vec(),Q(1) if unit else Q(2))]
 for j,h in enumerate(hubs):raw.extend([(vec(a,a),h,Q(1) if unit else Q(2+j%3,2)),(h,vec(a,a),Q(1) if unit else Q(4+j))])
 for off,x in enumerate(i for i in range(n) if i!=a):
  selected=range(len(hubs)) if full else [off%len(hubs)] if hubs else []
  for j in selected:raw.extend([(vec(a,x),hubs[j],Q(1) if unit else Q(1+off%2)),(hubs[j],vec(a,x),Q(1) if unit else Q(1+(j+off)%4))])
 return raw

def all_covers(vs,edges):
 return [frozenset(vs[j] for j in range(len(vs)) if mask>>j&1) for mask in range(1<<len(vs)) if all(mask>>vs.index(u)&1 or mask>>vs.index(v)&1 for u,v in edges)]
def prop(x,u,k):
 for xx,uu in zip(x,u):
  if xx<uu:return Q(0)
  for j in range(uu):k*=xx-j
 return k

def exercise_case(name,n,a,edges,t,full=False,raw=None):
 raw=raw_graph(n,a,edges,full=full) if raw is None else raw
 cert=C.numerical(raw,t,max_profile_steps=200000);assert cert['status']=='CERTIFIED_NUMERICAL'
 assert I.receive_numerical(raw,t,cert,max_profile_steps=200000) and I.receive_qualitative(raw,C.qualitative(raw));COUNTS['raw_receipts']+=2
 rec=I.parse(raw);co=cert['constants'];cv=all_covers(rec['satellites'],edges);minimal=[v for v in cv if not any(w<v for w in cv)]
 assert set(minimal)==set(map(frozenset,cert['covers']))
 lam,mu=rec['lam'],rec['mu'];q,eps=co['q'],co['epsilon'];E=len(edges)
 def g(k):return cert['profile_head'][k] if k<co['K'] else 1+co['c']/Q(k)
 def d(k):return g(k)-g(k+1)
 def geom(x):
  weights=[sum(x[v] for v in cover) for cover in cv];tau=min(weights);opt=[cover for cover,w in zip(cv,weights) if w==tau];mins=[cover for cover in minimal if sum(x[v] for v in cover)==tau]
  return sum(x),x[a],tau,x[a]+tau,opt,mins
 def h(x):
  N,A,tau,r,opt,mins=geom(x);return g(r)+q*Q(A,(N+1)*(r+1)**2)-eps*Q(A,N+1)
 for r in list(range(1,co['J']+2))+[10**20]:
  assert lam*(t*g(r+1)-g(r))-co['beta']*r*r*d(r)<=-co['epsilon0']*g(r)
  assert (r+1)**2*d(r)>=co['dstar'] and d(r-1)<=co['G']*d(r)
  er=mu*(g(r-1)/t-g(r))+co['Kf']*r*d(r-1)+2*co['beta']*r*d(r)+eps*(rec['F0']+co['D'])
  if r<co['J']:assert q*rec['kminus']/(4*(r+1)**2)>=max(er,0)
  else:assert er<=-co['D']/4
  COUNTS['profile_checks']+=1
 def check(x):
  N,A,tau,r,opt,mins=geom(x);old=h(x);assert Q(3,4)<=old<=co['H']
  if len(mins)>1:COUNTS['optimal_cover_ties']+=1
  bad={e for e in edges if any(e[0] in cover and e[1] in cover for cover in opt)}
  qb=sum(x[u]*x[v] for u,v in bad);Qhub=sum(x[u]*x[v] for u,v in edges);qg=Qhub-qb
  heavy={v for v in rec['satellites'] if x[v]>r};hb=sum(x[v] for v in heavy)
  assert 4*E*Qhub>=tau*tau and hb>=N-n*r
  if hb:assert qb*hb<=E*r*qg;COUNTS['heavy_bounds']+=1
  f=Q(A,(r+1)**2);lg=lf=ln=pcore=ncore=full=Q(0)
  for u,v,k in raw:
   rate=prop(x,u,k)
   if not rate:continue
   y=tuple(xx-uu+vv for xx,uu,vv in zip(x,u,v));NN,AA,tt,rr,oo,mm=geom(y);fp=Q(AA,(rr+1)**2);delta=NN-N
   full+=rate*(t**delta*h(y)-old)
   if not delta:
    assert r>=1 and rr>=1 and abs(rr-r)<=1 and abs(fp-f)<=Q(11,(r+1)**2)
    lg+=rate*(g(rr)-g(r));lf+=rate*(fp-f);ln-=eps*rate*Q(AA-A,N+1)
    if set(mins)!=set(mm):COUNTS['cover_switches']+=1
    if not u[a]:
     edge=tuple(i for i,z in enumerate(u) if z)
     if v[a]==2:assert rr-r==(0 if edge in bad else 1)
     elif rr<r:assert edge in bad;COUNTS['reverse_arm_decrements']+=1
    elif u[a]==1:
     xindex=next(i for i,z in enumerate(u) if z and i!=a)
     if xindex in heavy:assert rr>=r and fp-f<=-Q(1,(r+1)**2);COUNTS['heavy_captures']+=1
    COUNTS['internal_jumps']+=1
   else:
    pcore+=rate*q*(t**delta*fp/(NN+1)-f/(N+1))
    ncore-=rate*eps*(t**delta*Q(AA,NN+1)-Q(A,N+1))
    if delta<0 and rr==0:assert r==A==1;COUNTS['last_seed_deaths']+=1
  if r:
   assert lg<=co['Kf']*A*r*d(r-1)+rec['smax']*qb*d(r-1)-rec['bmin']*qg*d(r)
   assert lf<=(-rec['kminus']*A*hb+11*co['Kf']*r*r+11*rec['smax']*Qhub)/(r+1)**2
   assert pcore<=q*co['Ccore']/(N+1)
   assert ln+ncore<=eps*(rec['F0']+co['D'])*A+eps*mu-eps*rec['b0']*Qhub/(N+1)
  else:
   assert lg==lf==ln==0
   assert full==lam*(t*g(1)-g(0))+q*lam*t/Q(4*(N+2))-eps*lam*t/Q(N+2)
  if N>=co['Nstar']:
   assert full<=-co['zeta']*old;COUNTS['outside_Foster']+=1
   if 0<r<=co['delta']*N:
    assert qb<=qg and rec['smax']*qb*d(r-1)<=rec['bmin']*qg*d(r)/4
    assert 11*q*rec['smax']*Qhub/((N+1)*(r+1)**2)<=rec['bmin']*qg*d(r)/4
    er=mu*(g(r-1)/t-g(r))+co['Kf']*r*d(r-1)+2*co['beta']*r*d(r)
    master=-co['epsilon0']*g(r)+A*(er+eps*(rec['F0']+co['D']))-q*rec['kminus']*A*hb/((N+1)*(r+1)**2)+q*co['Ce']/(N+1)+eps*mu-eps*rec['b0']*Qhub/(N+1)
    assert full<=master and full<=-co['epsilon0']*g(r)/2;COUNTS['boundary_states']+=1
   elif r:
    assert full<=co['Cint']-co['D']*A/2-eps*rec['b0']*Qhub/(N+1) and full<=-1;COUNTS['interior_states']+=1
  else:assert full+co['zeta']*old<=cert['Foster']['coefficient']*t
  COUNTS['states']+=1
 states=list(product(range(3 if n<=6 else 2),repeat=n));states += [tuple(RNG.randrange(8) for _ in range(n)) for _ in range(60)]
 for mass in [co['Nstar']-1,co['Nstar'],co['Nstar']+1,10**30]:
  for axis in range(n):
   for A in [0,1,2,co['K'],co['J']]:
    x=[0]*n;x[axis]=mass;x[a]+=A;states.append(tuple(x))
  for offset in [-1,0,1]:states.append(tuple(mass+offset*(i%2) for i in range(n)))
  if n==5 and a==0:
   states += [(0,mass,1,1,mass),(0,1,1,0,mass),(1,mass,1,1,mass)]
  # Cross cone using a pure active state plus one bulk coordinate: tau may be zero,
  # so R=A gives an exact controllable split independent of the graph.
  cut=co['delta']*mass/(1-co['delta']);a0=cut.numerator//cut.denominator
  for aa in [max(1,a0-1),max(1,a0),a0+1]:
   x=[0]*n;x[a]=aa;x[next(i for i in range(n) if i!=a)]=mass;states.append(tuple(x))
 before=COUNTS['states']
 for x in states:check(x)
 # Mathematical normalization, not identical raw-work claims.
 split=[]
 for u,v,k in raw:split.extend([(u,v,k/7),(u,v,6*k/7)])
 split.append(((0,)*n,(0,)*n,Q(5)));RNG.shuffle(split);z=C.numerical(split,t,max_profile_steps=200000)
 assert I.receive_numerical(split,t,z,max_profile_steps=200000)
 for field in ['raw_sha256','covers','constants','profile_head','Foster','stationary_moment']:assert I.canonical(z[field])==I.canonical(cert[field])
 COUNTS['normalization_controls']+=1
 return dict(name=name,n=n,a=a,edges=edges,states=COUNTS['states']-before,K=co['K'],J=co['J'],Nstar=co['Nstar'],covers=len(cert['covers']),work=cert['work'],raw_sha256=cert['raw_sha256']),raw,cert

CASES=[]
for args in [('P4_full',5,0,[(1,2),(2,3),(3,4)],Q(3,2),True),('C5',6,0,[(1,2),(2,3),(3,4),(4,5),(1,5)],Q(3,2),False),('house',6,0,[(1,2),(2,3),(3,4),(1,4),(2,5),(3,5)],Q(3,2),False),('star_free',6,0,[(1,2),(1,3),(1,4)],Q(3,2),False),('three_edges_free',8,0,[(1,2),(3,4),(5,6)],Q(3,2),False),('permuted_P4',5,3,[(0,1),(1,2),(2,4)],Q(3,2),False)]:
 row,raw,cert=exercise_case(*args);CASES.append(row)
 if args[0]=='P4_full':base_raw,base_cert=raw,cert

# Independent direct domination over minimal covers versus polynomial recognizer.
GRAPH=dict(graphs=0,admitted=0,domination_checks=0,packing_states=0,heavy_states=0)
for m in range(2,6):
 possible=list(combinations(range(1,m+1),2))
 for mask in range(1,1<<len(possible)):
  edges=[e for j,e in enumerate(possible) if mask>>j&1];es=set(edges);vs=tuple(range(1,m+1));cv=all_covers(vs,edges);mins=[v for v in cv if not any(w<v for w in cv)]
  condition=all(any(tuple(sorted((w,z))) in es for z in (u,v)) for cover in mins for u,v in edges if u in cover and v in cover for w in vs if w not in cover)
  raw=raw_graph(m+1,0,edges,unit=True);got=C.qualitative(raw)
  assert (got['status']=='CERTIFIED_QUALITATIVE')==condition and I.receive_qualitative(raw,got)
  GRAPH['graphs']+=1;GRAPH['admitted']+=condition;GRAPH['domination_checks']+=1
  for _ in range(12):
   x={v:RNG.randrange(5) for v in vs};tau=min(sum(x[v] for v in cover) for cover in cv);Qhub=sum(x[u]*x[v] for u,v in edges)
   assert 4*len(edges)*Qhub>=tau*tau;GRAPH['packing_states']+=1
   if condition:
    opt=[cover for cover in mins if sum(x[v] for v in cover)==tau];qb=sum(x[u]*x[v] for u,v in edges if any(u in cover and v in cover for cover in opt));qg=Qhub-qb
    for A in [0,1,3]:
     r=A+tau;hb=sum(x[v] for v in vs if x[v]>r)
     if hb:assert qb*hb<=len(edges)*r*qg;GRAPH['heavy_states']+=1

# Qualitative and insufficient-budget receiving provably never call cover enumeration.
for module in [C,I]:
 name='covers' if module is C else 'minimal_covers';original=getattr(module,name)
 def forbidden_call(*args,**kwargs):raise AssertionError('cover enumeration entered qualitative/preflight path')
 setattr(module,name,forbidden_call)
 try:
  assert module.qualitative(base_raw)['status']=='CERTIFIED_QUALITATIVE'
  assert module.numerical(base_raw,Q(3,2),max_cover_masks=0)['status']=='UNKNOWN_NUMERICAL_BUDGET'
  assert module.numerical(base_raw,Q(3,2),max_profile_steps=0)['status']=='UNKNOWN_NUMERICAL_BUDGET';COUNTS['qualitative_no_cover_calls']+=3
 finally:setattr(module,name,original)

# Numeric boundary refuses before enumeration/scans; successful exact-budget construction.
steps=base_cert['work']['profile_steps'];masks=base_cert['work']['cover_masks_enumerated']
for a,b,status in [(steps-1,masks,'UNKNOWN_NUMERICAL_BUDGET'),(steps,masks-1,'UNKNOWN_NUMERICAL_BUDGET'),(steps,masks,'CERTIFIED_NUMERICAL')]:
 cc=C.numerical(base_raw,Q(3,2),max_profile_steps=a,max_cover_masks=b);assert cc['status']==status and I.receive_numerical(base_raw,Q(3,2),cc,max_profile_steps=a,max_cover_masks=b);COUNTS['budget_controls']+=1
for t,mu in [(Q(2),Q(1,10**5000)),(1+Q(1,10**200),Q(1)),(Q(10**100),Q(1))]:
 rr=[(u,v,mu if sum(v)==0 else k) for u,v,k in base_raw];cc=C.numerical(rr,t,max_profile_steps=1000)
 assert cc['status']=='UNKNOWN_NUMERICAL_BUDGET' and cc['qualitative']['status']=='CERTIFIED_QUALITATIVE' and I.receive_numerical(rr,t,cc,max_profile_steps=1000);COUNTS['budget_controls']+=1

# Independent exact tampering: each constant, covers, profile joins, metadata and factored bounds.
t=Q(3,2)
for key in base_cert['constants']:
 forged=copy.deepcopy(base_cert);forged['constants'][key]+=1;assert not I.receive_numerical(base_raw,t,forged);COUNTS['semantic_mutations']+=1
for key in ['covers','profile_head','Foster','stationary_moment','work','qualitative','t','raw_sha256','family','status','cost_scope']:
 forged=copy.deepcopy(base_cert);forged[key]=None;assert not I.receive_numerical(base_raw,t,forged);COUNTS['semantic_mutations']+=1
for index in [0,1,len(base_cert['profile_head'])//2,len(base_cert['profile_head'])-1]:
 forged=copy.deepcopy(base_cert);head=list(forged['profile_head']);head[index]+=1;forged['profile_head']=tuple(head);assert not I.receive_numerical(base_raw,t,forged);COUNTS['semantic_mutations']+=1
for key in I.qualitative(base_raw):
 forged=copy.deepcopy(I.qualitative(base_raw));forged[key]=None;assert not I.receive_qualitative(base_raw,forged);COUNTS['semantic_mutations']+=1

# Invalid domains against both implementations; malformed values never become stability verdicts.
def refuse(fn):
 try:fn()
 except (TypeError,ValueError):COUNTS['domain_refusals']+=1;return
 raise AssertionError('invalid domain accepted')
for val in [True,False,1.0,'1',0,-1,None,float('nan'),float('inf')]:
 rr=copy.deepcopy(base_raw);u,v,k=rr[0];rr[0]=(u,v,val)
 for module in [C,I]:refuse(lambda module=module,rr=rr:module.qualitative(rr))
for val in [True,False,2.0,'2',0,1,-1,None]:
 for module in [C,I]:refuse(lambda module=module,val=val:module.numerical(base_raw,val))
for val in [True,False,1.0,Q(1),'1',-1,None]:
 rr=copy.deepcopy(base_raw);u,v,k=rr[0];u=list(u);u[1]=val;rr[0]=(u,v,k)
 for module in [C,I]:refuse(lambda module=module,rr=rr:module.qualitative(rr))
for val in [True,False,1.0,Q(1),'1',-1,None]:
 for module in [C,I]:
  for field in ['max_profile_steps','max_cover_masks']:refuse(lambda module=module,val=val,field=field:module.numerical(base_raw,t,**{field:val}))

RESULT=dict(status='PASS',scope='Separate receiver plus fresh finite exact checks; ordinary proof audited independently',counts=COUNTS,graph_controls=GRAPH,cases=CASES,seconds=time.perf_counter()-START,source_sha256=hashlib.sha256((SOURCE/'cover_seed.py').read_bytes()).hexdigest(),receiver_sha256=hashlib.sha256((HERE/'independent_cover_receiver.py').read_bytes()).hexdigest(),no_simulation=True,no_exception_enumeration=True,no_Foster_power_expansion=True,new_compact_compiler_outside_scope=True)
(OUT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(I.wire(RESULT),indent=2)+'\n');print(json.dumps(I.wire(RESULT),indent=2))
