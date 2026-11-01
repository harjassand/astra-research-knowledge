from pathlib import Path
from fractions import Fraction as Q
from itertools import product,permutations,combinations
import copy,json,os,sys,time,random
import independent_glue_receiver as I
HERE=Path(__file__).resolve().parent;SOURCE=Path(os.environ.get('GLUE_SOURCE_DIR',(HERE.parent if (HERE.parent/'free_port_glue.py').is_file() else HERE.parent/'stochastic_free_port_glue_pending_20261031'))).resolve();OUT=Path(os.environ.get('AUDIT_OUTPUT_DIR',HERE)).resolve();OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(SOURCE));import free_port_glue as G # Driver comparisons only; receiver never imports G.
start=time.monotonic();count={};cases=[]
def add(k,n=1):count[k]=count.get(k,0)+n
def fixture(kind='triangle',scale=Q(1),extra=False):
 edges=[(1,2),(1,3),(2,3)]if kind=='triangle'else [(1,2),(2,3),(3,4)]if kind=='p4'else [(1,2)]
 rare=3 if kind=='triangle'else 4 if kind=='p4'else 2
 n=rare+2+int(extra);a=0;f=n-1;z=lambda *v:tuple(v.count(j)for j in range(n));raw=[(z(),z(0),scale),(z(0),z(),scale)]
 for e in edges:raw.extend([(z(0,0),z(*e),scale),(z(*e),z(0,0),scale)])
 for j in range(1,n):
  e=edges[0]if j>=rare+1 else edges[(j-1)%len(edges)]
  raw.extend([(z(0,j),z(*e),scale),(z(*e),z(0,j),scale*(2 if j==rare else 1))])
 return raw

def partial(r,c,gamma):
 co=c['constants'];p=c['core_profile'];delta=gamma*co['delta_unit'];kap=min(co['D']*delta/4,co['e']*r['b0']*delta**2/(32*len(r['edges'])))
 ci=2*co['L']+2*r['mu']+(2*p['c']+11*co['rho0'])*r['S']/delta**2+co['rho0']*(11*r['lam']*c['t']+co['CA'])
 return I.ceil(max(Q(1),Q(p['K'])/delta,4*co['CA']/(r['krminus']*gamma),4*co['Qhead']/(co['rho0']*r['krminus']*gamma),(ci+1)/kap))

def check_state(r,c,x,gamma=None):
 co=c['constants'];N,A,f,U,R,P=I.coordinates(r,x);h,z,phi=I.pieces(r,c,x);lh,lz,cross,whole=I.drift(r,c,x)
 assert (lh,lz,cross,whole)==G.scaled_pieces(G.recognize(RAW),c,x)
 assert P<=R<=U and Q(3,4)<=h<=co['H0'] and 0<=z<=co['CZ']/Q(P+1) and 0<=phi<=1
 assert lh<=co['C0'] and cross<=co['Ccross']/co['Jcut'];add('states')
 if A==1:add('last_copy_death_states')
 if P==0:add('pair_zero_states')
 if R==0:add('core_zero_states')
 if phi:assert U+1<=co['deltaF']*f;add('nonzero_actual_cutoff_states')
 if U+1<=co['deltaF']*f:assert lz<=-co['cfree'];add('free_cone_bounds')
 if gamma:
  assert U>=gamma*N and N>=partial(r,c,gamma)
  assert lh<=-co['zeta0']*h and whole<=-co['zeta0']/2;add('partial_core_and_full_negative')
 for u,v,rate,y in I.enabled(r,x):
  NN,AA,ff,UU,RR,PP=I.coordinates(r,y)
  if sum(u)!=sum(v):continue
  assert NN==N and abs(RR-R)<=1 and abs(PP-P)<=2
  df=Q(AA,(PP+1)**2)-Q(A,(P+1)**2)
  if u[r['a']]==0:
   assert PP>=P and df<=Q(2,(P+1)**2)
   if v[r['a']]==2:assert PP>=P+1
  else:assert PP<=P and abs(df)<=Q(20,(P+1)**2)
  if u[r['f']]or v[r['f']]:assert PP==P
  if PP!=P:add('pair_switches')
  if RR!=R:add('cover_switches')
  add('internal_jumps')

def run(raw,t,name,small=True):
 global RAW
 RAW=raw;r=I.parse(raw);c=I.construct(raw,t);assert c['status']=='CERTIFIED_SYMBOLIC_FOSTER'
 assert I.canonical(c)==I.canonical(G.construct(raw,t));assert I.receive_qualitative(raw,G.qualitative(raw));add('full_certificate_receipts')
 co=c['constants'];p=c['core_profile'];pf=c['free_profile']
 # Explicit head and tail identities for both independently computed profiles.
 for pp in (p,pf):
  for j in list(range(1,pp['K']+3))+[10**4,10**50]:
   gg=I.g(pp,j);dr=gg-I.g(pp,j+1)
   assert r['lam']*(t*I.g(pp,j+1)-gg)-pp['beta']*j*j*dr<=-pp['eps']*gg
   assert dr>=pp['dlow']/Q((j+1)**2)
   assert I.g(pp,j-1)-gg<=pp['D1']/Q((j+1)**2)
   assert I.g(pp,max(0,j-2))-gg<=pp['D2']/Q((j+1)**2)
   add('profile_identity_checks')
 if small:
  for x in product(range(3),repeat=r['n']):check_state(r,c,x)
 for A in (0,1,2,3,pf['K'],10**30):
  for rv in ([0]*len(r['rare']),[1]*len(r['rare']),[2,0]+[4]*(len(r['rare'])-2),[0,2]+[1]*(len(r['rare'])-2),[10**40]+[1]*(len(r['rare'])-1)):
   x=[0]*r['n'];x[r['a']]=A
   for v,z in zip(r['rare'],rv):x[v]=z
   x[r['f']]=I.ceil(4*Q(sum(x)+1)/co['deltaF']);check_state(r,c,tuple(x))
 for gamma in (Q(1),Q(1,2),Q(1,1<<20),Q(1,10**100)):
  head=partial(r,c,gamma);U=2*I.ceil(gamma*head)+100;f=I.ceil(U*(1-gamma)/gamma)
  for A in (0,1,2,p['K'],U//2):
   for b in r['rare']:
    x=[0]*r['n'];x[r['a']]=A;x[r['f']]=f;x[b]=U-A;check_state(r,c,tuple(x),gamma)
   x=[0]*r['n'];x[r['a']]=A;x[r['f']]=f
   for v in r['rare']:x[v]=(U-A)//len(r['rare'])
   x[r['rare'][0]]+=(U-A)%len(r['rare']);check_state(r,c,tuple(x),gamma)
 # Synthetic narrow cutoffs are lemma-only, never full Foster certificates.
 for width in (1,3,8):
  s=copy.deepcopy(c);s['constants']['Jcut']=width;b,cc=r['h0']
  for U in (0,1,2,3,8,31,256):
   for A in range(min(2,U)+1):
    for power in (co['L0']-1,co['L0'],co['L0']+width,co['L0']+width+1):
     for off in (-2,-1,0,1,2):
      x=[0]*r['n'];x[r['a']]=A;x[b]=(U-A)//2;x[cc]=U-A-x[b];x[r['f']]=max(0,((U+1)<<power)+off-1);x=tuple(x)
      h,z,phi=I.pieces(r,s,x);lh,lz,cross,w=I.drift(r,s,x)
      assert cross<=co['Ccross']/width
      if phi:assert U+1<=co['deltaF']*x[r['f']] and lz<=-co['cfree']
      for u,v,rate,y in I.enabled(r,x):
       np=I.pieces(r,s,y)[2]
       if np>phi:
        death=sum(v)<sum(u);freereverse=v[r['f']]>u[r['f']]
        assert death or freereverse
        assert np-phi<=Q(2 if death else 4,width*U)
        if not phi:add('zero_cutoff_crossings')
        if np==1:add('one_cutoff_crossings')
        add('increasing_cutoff_jumps')
      add('synthetic_cutoff_lemma_states')
 assert not I.outside_head(c,10**1000) and I.expand_head(c,100000)==G.expand_head(c,100000)
 cases.append(dict(name=name,t=t,profile_steps=c['work']['profile_steps'],retained_scalar_bits=c['work']['retained_scalar_bits'],Jcut=co['Jcut'],power_bits=c['symbolic_head']['exponent']+1,certificate_sha256=I.digest(c),wire_bytes=len(I.canonical(c).encode())))
 return r,c
raw=fixture();r,c=run(raw,Q(2),'independent_triangle_nonCB')
_,cp=run(fixture('p4'),Q(3,2),'independent_p4_nonCB')
_,ce=run(fixture('edge',extra=True),Q(5,4),'accepted_core_with_additional_isolated_passenger')
# Extreme positive domain: reverse rates and immigration are enormous/small but profiles remain acquired.
rr=fixture('edge')
rr=[(u,v,Q(1,10**200)if sum(u)==0 else Q(10**1500)if sum(u)==2 and u[0]==0 else k)for u,v,k in rr]
_,cx=run(rr,Q(10**100),'huge_t_and_reverse_tiny_immigration',small=False)
# Structural permutations and coordinate invariance.
for j,perm in enumerate(permutations(range(5))):
 rr=[(tuple(u[k]for k in perm),tuple(v[k]for k in perm),q)for u,v,q in raw]
 assert I.canonical(I.qualitative(rr))==I.canonical(G.qualitative(rr));add('qualitative_permutations')
 if j in (0,23,71,119):
  cc=I.construct(rr,Q(2));assert cc['constants']==c['constants'] and cc['symbolic_head']==c['symbolic_head'];assert I.canonical(cc)==I.canonical(G.construct(rr,Q(2)));add('symbolic_permutations')
# Every semantic certificate field is reacquired, not merely digest checked.
for key in c:
 bad=copy.deepcopy(c);bad[key]=None;assert not I.receive_symbolic(raw,Q(2),bad);add('symbolic_mutations')
for key in c['constants']:
 bad=copy.deepcopy(c);bad['constants'][key]+=1;assert not I.receive_symbolic(raw,Q(2),bad);add('symbolic_mutations')
for key in ('core_profile','free_profile'):
 for sub in c[key]:
  bad=copy.deepcopy(c);bad[key][sub]=None;assert not I.receive_symbolic(raw,Q(2),bad);add('symbolic_mutations')
for key in c['qualitative']:
 bad=copy.deepcopy(c['qualitative']);bad[key]=None;assert not I.receive_qualitative(raw,bad);add('qualitative_mutations')
for key in ('exponent','coefficients','formula'):
 bad=copy.deepcopy(c);bad['symbolic_head'][key]=None;assert not I.receive_symbolic(raw,Q(2),bad);add('symbolic_mutations')
# Extreme refusals stay qualitative and do not attempt profile expansion.
for change in ('mu_tiny','t_near_one','t_huge'):
 rr=copy.deepcopy(raw);t=Q(2)
 if change=='mu_tiny':rr=[(u,v,Q(1,10**5000)if sum(v)==0 else q)for u,v,q in rr]
 if change=='t_near_one':t=1+Q(1,10**200)
 if change=='t_huge':t=Q(10**100)
 a=I.construct(rr,t,10);b=G.construct(rr,t,10);assert I.canonical(a)==I.canonical(b) and a['status']=='UNKNOWN_PROFILE_BUDGET' and a['qualitative']['status']=='CERTIFIED_QUALITATIVE';add('extreme_profile_refusals')
steps=c['work']['profile_steps']
for budget in (0,steps-1,steps):
 cc=I.construct(raw,Q(2),budget);assert I.canonical(cc)==I.canonical(G.construct(raw,Q(2),budget));assert (cc['status']=='CERTIFIED_SYMBOLIC_FOSTER')==(budget==steps);add('exact_loop_budget_boundaries')
# Distinguish bounded intermediate power from unbounded coefficient input/output bits.
for exp in (0,1,2,7,30,100,1000):
 for denom_bits in (1,17,1000,10000):
  den=(1<<denom_bits)+1;co=(Q(1)+Q(1,den),Q(3,den),Q((1<<denom_bits)+3,den+2));s={'symbolic_head':dict(exponent=exp,coefficients=co)}
  u=2*((1<<exp)+1);exact=I.ceil(co[0]*u+co[1]*u*u+co[2]*u**4+1)
  assert I.expand_head(s,exp+1)==exact==G.expand_head(s,exp+1)
  assert I.expand_head(s,exp)['status']=='UNKNOWN_POWER_EXPANSION_BUDGET'
  for N in (0,1,1<<exp,exact-1,exact,exact+1,exact*2):assert I.outside_head(s,N)==G.outside_head(s,N)==(N>=exact);add('head_reader_comparisons')
large={'symbolic_head':dict(exponent=10**5000,coefficients=(Q(1),Q(1),Q(1)))}
assert I.outside_head(large,10**1000)==False;assert I.expand_head(large,100000)['required_power_bits']==10**5000+1;add('astronomical_guard_checks',2)

def rejects(call):
 try:call()
 except (ValueError,TypeError):add('domain_refusals')
 else:raise AssertionError('expected domain refusal')
for bad in (True,2.0,'2',Q(1),0,-1,None):
 for mod in (I,G):rejects(lambda mod=mod,bad=bad:mod.construct(raw,bad))
for bad in (True,1.0,-1,None):
 for mod in (I,G):
  rejects(lambda mod=mod,bad=bad:mod.construct(raw,2,bad));rejects(lambda mod=mod,bad=bad:mod.expand_head(c,bad))
for bad in (True,1.0,'1',Q(1),-1,None):
 rr=copy.deepcopy(raw);u,v,k=rr[0];u=list(u);u[1]=bad;rr[0]=(u,v,k)
 for mod in (I,G):rejects(lambda mod=mod,rr=rr:mod.qualitative(rr))
for bad in (True,1.0,'1',0,-1,None):
 rr=copy.deepcopy(raw);u,v,k=rr[0];rr[0]=(u,v,bad)
 for mod in (I,G):rejects(lambda mod=mod,rr=rr:mod.qualitative(rr))
for bad in (True,1.0,'1',-1,None):
 for mod in (I,G):rejects(lambda mod=mod,bad=bad:mod.outside_head(c,bad))
for bad in (True,1.0,Q(1),0,-1,None):
 for mod in (I,G):rejects(lambda mod=mod,bad=bad:mod.dyadic(bad))
# Raw well-typed frontier and reversible unit-rate stable UNKNOWNs.
z=lambda *ix:tuple(ix.count(i)for i in range(5))
neg=[raw[:-1],raw+[(z(0,4),z(1,3),Q(1)),(z(1,3),z(0,4),Q(1))],raw+[(z(0,0),z(1,4),Q(1)),(z(1,4),z(0,0),Q(1))]]
rr=[(u+(0,),v+(0,),Q(1))for u,v,k in raw];zz=lambda *ix:tuple(ix.count(i)for i in range(6));rr.extend([(zz(0,5),zz(1,2),Q(1)),(zz(1,2),zz(0,5),Q(1))]);neg.append(rr)
for rawneg in neg:
 assert I.qualitative(rawneg)['status']==G.qualitative(rawneg)['status']=='UNKNOWN';add('structural_unknowns')
for rawneg in neg[1:]:
 unit=[(u,v,Q(1))for u,v,k in rawneg];pairs={(u,v)for u,v,k in unit};assert all((v,u)in pairs for u,v in pairs);assert I.qualitative(unit)['status']=='UNKNOWN';add('unit_rate_stable_unknowns')
# Duplicated directed rates, zero nulls, and mixed tuple/list nulls normalize correctly.
u,v,k=raw[2]
for null in [(list(z(0)),z(0),Q(7)),(z(),list(z()),Q(9))]:
 rr=raw[:2]+[(u,v,k/7),(u,v,6*k/7)]+raw[3:]+[null]
 assert I.parse(rr)['raw_sha256']==r['raw_sha256'] and G.recognize(rr)['raw_sha256']==r['raw_sha256'];add('normalization_controls')
result=dict(status='PASS_INDEPENDENT',seconds=time.monotonic()-start,counts=count,cases=cases,scope='New separate receiver and whole proof audit; synthetic cutoffs only test lemma; actual enormous global-head and phi=1 tail not expanded.',no_candidate_imports_in_receiver=True,no_new_source_retrieval=True)
(OUT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(I.wire(result),indent=2)+'\n');print(json.dumps(I.wire(result),indent=2))
