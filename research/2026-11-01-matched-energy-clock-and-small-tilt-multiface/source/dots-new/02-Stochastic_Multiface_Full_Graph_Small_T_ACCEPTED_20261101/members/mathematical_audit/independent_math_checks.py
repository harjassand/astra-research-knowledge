#!/usr/bin/env python3
"""Independent tests of 1bb09538 theorem. No candidate code imported.
Finite tests supplement the analytic audit; they are not an executable admission.
No q**J at acquired global thresholds is expanded.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import hashlib, json, pathlib, time
HERE=pathlib.Path(__file__).resolve().parent
INPUT=HERE/'THEOREM_INPUT.md'
EXPECTED='1bb095387e1efe086117f6be61cffe4563d49efbdacb6309be864979aa2284f7'
assert hashlib.sha256(INPUT.read_bytes()).hexdigest()==EXPECTED
C={}
def count(k,n=1): C[k]=C.get(k,0)+n
def ceil(x): return -(-x.numerator//x.denominator)
def independent(n,E):
 return [frozenset(i for i in range(n) if mask>>i&1) for mask in range(1,1<<n) if all(not(mask>>i&1 and mask>>j&1) for i,j in E)]
def parts(n,E,I):
 near={v for e in E for v in e if v not in I and any(i in I for i in e)}
 return near,set(range(n))-I-near
@lru_cache(None)
def Z(M,j):
 assert j>=0
 q=F(M+1,M)
 return (1-q**(-j-M))/F(j+M)
def D(M,j): return Z(M,j)-Z(M,j+1)
def prefix(ids,x,eta):
 ids=sorted((i for i in ids if x[i]>0),key=lambda i:(-x[i],i))
 assert ids
 for k in range(1,len(ids)):
  if x[ids[k]]<=eta*x[ids[k-1]]: return set(ids[:k])
 return set(ids)
def cover(n,E,A,x):
 N=A+sum(x); assert N
 delta=F(1,4); eta=delta/(4*n); hh=eta**(n-1)/(2*n)
 eps=min(F(1,4),hh*hh/2,hh/8); gamma=delta*hh/8
 if A>gamma*N: return 'A',0
 I=prefix(range(n),x,eta)
 assert min(x[i] for i in I)>=hh*N
 if any(i in I and j in I for i,j in E):
  assert any(x[i]>gamma*N and x[j]>gamma*N for i,j in E)
  return 'edge',0
 stages=0
 while True:
  stages+=1; assert stages<=n
  assert all(not(i in I and j in I) for i,j in E)
  near,far=parts(n,E,I); U=A+sum(x[i] for i in range(n) if i not in I); FI=sum(x[i] for i in I)
  assert U<=delta*min(x[i] for i in I)
  act=A*FI+sum(x[i]*x[j] for i,j in E if (i in I) != (j in I) or i in far and j in far)
  if U==0 or act>=eps*U*U:
   if U==0: assert A==0 and all(x[i]*x[j]==0 for i,j in E)
   return 'face',stages
  assert A+sum(x[i] for i in near)<eps*delta*U
  assert sum(x[i] for i in far)>U/2
  J=prefix(far,x,eta)
  assert min(x[i] for i in J)>=hh*U
  assert all(not(i in J and j in J) for i,j in E)
  assert not (I&J)
  old=I; I=I|J
  newU=A+sum(x[i] for i in range(n) if i not in I)
  assert newU<=3*delta*min(x[i] for i in I)/8
  count('selector_strict_enlargements')

def source_profile_checks():
 for M in [2,3,4,12,13,24,48,96]:
  q=F(M+1,M); Cstep=(4*M+4)*3**6
  assert q**M>=2 and q**(2*M)<9
  for j in [0,1,2,M-1,M,2*M,4*M,10*M]:
   z,d=Z(M,j),D(M,j)
   assert 0<z<=F(1,j+1)
   assert F(1,8*(j+M+1)**2)<=d<=F(1,(j+1)**2)
   count('profile_bounds')
   if j>=2*M:
    assert Z(M,j-2*M)-z<=18*M*d
    count('true_death_profile_bounds')
  for k in range(1,17):
   z=1-(1-1/q)*F(k,16)
   for jump in range(-4*M-4,4*M+5):
    assert abs(z**jump-1)<=Cstep*(1-z)
    count('all_signed_jump_bounds')
   # The worst selected hub: amplification gain m=2M-2 and adverse -2.
   # The s used here upper bounds adverse outgoing rates; M >=12s/b.
   b=F(1); s=F(M,12); h=b/(4*(q-1))
   assert b*(z**(2*M-2)-1)+s*(z**-2-1)<=-h*(1-z)
   g=(1-q**-2)/(q-1)
   assert z*z-1<=-g*(1-z)
   count('selected_source_convexity_points',2)

def selector_checks():
 for n in range(2,5):
  pairs=list(combinations(range(n),2))
  for mask in range(1,1<<len(pairs)):
   E=[p for k,p in enumerate(pairs) if mask>>k&1]
   for state in product(range(3),repeat=n+1):
    if not sum(state): continue
    typ,st=cover(n,E,state[0],state[1:]); count('selector_exhaustive_states'); count('selector_'+typ)
   # Widely separated strata force the repeated-Far enlargement branch.
   for perm in [tuple(range(n)),tuple(reversed(range(n)))]:
    for base in [10**3,10**12,10**40]:
     x=[base**perm[i] for i in range(n)]
     for A in [0,1,base]:
      cover(n,E,A,x); count('selector_separated_scale_states')
 # Empty graph is not an input theorem, but its face selector still works.
 for n in range(2,8):
  cover(n,[],0,[10**(50*i) for i in range(n)]); count('selector_empty_graph_controls')

def make(n,E,variant=0):
 # Every A+i has an arm to every hub. Rates deliberately unequal in variant1.
 lam=F(2,3) if variant else F(1); mu=F(5,4) if variant else F(1)
 amp={e:(F(2,3) if variant else F(1)) for e in E}
 rev={e:(F(3,2) if variant else F(1)) for e in E}
 k={(i,e):(F(2+i%2,3) if variant else F(1)) for i in range(n) for e in E}
 r={(i,e):(F(3+i%2,4) if variant else F(1)) for i in range(n) for e in E}
 if variant==2:
  # Exactly one arm per satellite, including arms to nonincident hubs.
  for i in range(n):
   for idx,e in enumerate(E):
    if idx!=i%len(E): k[i,e]=F(0);r[i,e]=F(0)
 ki=[sum(k[i,e] for e in E) for i in range(n)]
 a=sum(amp.values()); km=min(ki); kM=max(ki); b=min(rev.values())
 s=max(rev[e]+sum(r[i,e] for i in range(n)) for e in E)
 M=max(2,ceil(12*s/b)); q=F(M+1,M); W=2*M+2
 g=km*(1-q**-2)/(q-1); h=b/(4*(q-1)); cs=(4*M+4)*3**6
 CA=cs*(a+kM)+18*mu*M; CH=cs*s
 d=F(1,8*(W+M+1)**2)
 T=max(1,ceil(4*CA/g),ceil(4*CH*len(E)/h)); B=1+n*T; R=(B+1)**2/d
 K=max(2,ceil(4*(2**n)*CH*R/h))
 faces=independent(n,E); weights={I:K**(n-len(I)) for I in faces}; P=sum(weights.values())
 RA=P*CA*(B+1); RQ=P*CH*(B+1)**2
 delta=F(1,4); eta=delta/(4*n); hh=eta**(n-1)/(2*n); epsC=min(F(1,4),hh*hh/2,hh/8); gamma=delta*hh/8
 ss=min(g,h)*d*epsC/4; cb=lam*(1+P)+mu*mu/4
 eps=min(F(1),ss/(16*cb)); t=1+eps; dd=mu*(1-1/t); forward=2*a+kM; ee=min(F(1,4),dd/(4*(forward+1))); H=1+eps*(1+P)
 Ns=max(2,ceil(4*RA/dd),ceil(RQ/(ee*b)),ceil(1+4*mu*H/(g*D(M,2*M))),ceil(4*(cb*eps+1)/(dd*gamma)),ceil(2*(cb*eps+1)/(ee*b*gamma*gamma)))
 return locals()
def transitions(c,state):
 A,*x=state; n=c['n']; N=sum(state)
 yield c['lam'],(A+1,*x),1,'birth'
 if A: yield c['mu']*A,(A-1,*x),-1,'death'
 for e in c['E']:
  i,j=e
  if A>=2:
   y=list(state);y[0]-=2;y[i+1]+=1;y[j+1]+=1
   yield c['amp'][e]*A*(A-1),tuple(y),0,'amp_forward'
  if x[i] and x[j]:
   y=list(state);y[0]+=2;y[i+1]-=1;y[j+1]-=1
   yield c['rev'][e]*x[i]*x[j],tuple(y),0,'amp_reverse'
  for u in range(n):
   if A and x[u] and c['k'][u,e]>0:
    y=list(state);y[0]-=1;y[u+1]-=1;y[i+1]+=1;y[j+1]+=1
    yield c['k'][u,e]*A*x[u],tuple(y),0,'arm_forward'
   if x[i] and x[j] and c['r'][u,e]>0:
    y=list(state);y[0]+=1;y[u+1]+=1;y[i+1]-=1;y[j+1]-=1
    yield c['r'][u,e]*x[i]*x[j],tuple(y),0,'arm_reverse'
def face(c,I,state):
 A,*x=state; near,far=parts(c['n'],c['E'],I)
 U=A+sum(x[i] for i in range(c['n']) if i not in I); FI=sum(x[i] for i in I)
 j=2*c['M']*A+(2*c['M']+2)*sum(x[i] for i in near)+(c['M']+1)*sum(x[i] for i in far)
 qc=sum(x[i]*x[j] for i,j in c['E'] if (i in I)!=(j in I))
 qf=sum(x[i]*x[j] for i,j in c['E'] if i in far and j in far)
 qb=sum(x[i]*x[j] for i,j in c['E'])-qc-qf
 z,di=Z(c['M'],j),D(c['M'],j)
 rr=(c['g']*A*FI+c['h']*(qc+qf))*di
 return z,rr,U,qb,di,j

def generator_checks():
 rows=[]
 fixtures=[(2,[(0,1)],0),(3,[(0,1),(1,2)],1),(3,[(0,1),(0,2),(1,2)],0),(4,[(0,1),(1,2),(2,3)],1),(4,[(0,1),(1,2),(0,2)],0),(5,[(0,1),(1,2),(0,2),(3,4)],0),(5,[(0,1),(1,2),(2,3)],2)]
 for n,E,v in fixtures:
  c=make(n,E,v)
  @lru_cache(None)
  def values(state):
   A,*x=state;N=sum(state);Q=sum(x[i]*x[j] for i,j in E)
   pp=sum(c['weights'][I]*face(c,I,state)[0] for I in c['faces'])
   SS=sum(c['weights'][I]*face(c,I,state)[1] for I in c['faces'])
   bb=1-c['ee']*F(A,N+1); inactive=(A==0 and Q==0)
   return pp,SS,bb,bb+pp+c['H']*inactive,inactive,Q
  states=list(product(range(3),repeat=n+1)) if n<=3 else [tuple([A]+[int((mask>>i)&1)*k for i in range(n)]) for A in [0,1,2,4] for mask in range(1<<n) for k in [1,3]]
  if n>=4: states=states[::max(1,len(states)//40)]
  for state in states:
   A,*x=state;N=sum(state);pp,SS,bb,hh,inactive,Q=values(state)
   tr=list(transitions(c,state)); assert all(all(z>=0 for z in y) and sum(y)==N+dN for rate,y,dN,name in tr)
   tilt=F(3,2)
   for I in c['faces']:
    z,rr,U,qb,di,j=face(c,I,state)
    gen=sum(rate*(tilt**dN*face(c,I,y)[0]-z) for rate,y,dN,name in tr)
    rhs=c['lam']*(tilt-1)*z-rr+c['CA']*A*(U+1)*di+c['CH']*qb*di
    assert gen<=rhs
    assert c['d']/F((U+1)**2)<=di<=F(1,(U+1)**2)
    count('exact_face_generator_inequalities')
   gen=sum(rate*(tilt**dN*values(y)[0]-pp) for rate,y,dN,name in tr)
   rhs=c['lam']*(tilt-1)*pp-SS/2+c['RA']*F(A,N+1)+c['RQ']*F(Q,(N+1)**2)
   assert gen<=rhs; count('exact_global_subset_inequalities')
   genB=sum(rate*(c['t']**dN*values(y)[2]-bb) for rate,y,dN,name in tr)
   rhsB=c['lam']*c['eps']+c['ee']*c['mu']-c['dd']*A/2-2*c['ee']*c['b']*F(Q,N+1)
   assert genB<=rhsB; count('exact_baseline_inequalities')
   genH=sum(rate*(c['t']**dN*values(y)[3]-hh) for rate,y,dN,name in tr)
   if inactive:
    assert genH<=-c['lam']; count('exact_inactive_drift_checks')
   if A==1 and Q==0 and N>=2:
    assert SS>=c['g']*(N-1)*D(c['M'],2*c['M']);count('last_copy_capture_checks')
   for rate,y,dN,name in tr:
    targetInactive=values(y)[4]
    if name not in ['birth','death']: assert not targetInactive
    if targetInactive and not inactive: assert name=='death' and A==1 and Q==0
    count('actual_indicator_transition_checks')
  # Constants are exactly acquired without expanding t**Nstar or q**(W*Nstar).
  assert c['eps']>0 and c['eps']<=1 and c['eps']*c['cb']<=c['ss']/16
  assert c['ee']*c['mu']<=c['mu']**2*c['eps']/4
  assert c['K']>=4*(2**n)*c['CH']*c['R']/c['h']
  assert c['Ns']>=c['RQ']/(c['ee']*c['b']) and c['Ns']>=4*c['RA']/c['dd']
  rows.append({'n':n,'edges':E,'rate_variant':v,'faces':len(c['faces']),'M':c['M'],'T':c['T'],'K_bits':c['K'].bit_length(),'P_bits':c['P'].bit_length(),'tilt_numerator_bits':c['t'].numerator.bit_length(),'tilt_denominator_bits':c['t'].denominator.bit_length(),'Nstar_bits':c['Ns'].bit_length(),'Nstar_conservative_bits':max(c['Ns'],ceil(1+4*c['mu']*c['H']/(c['g']*F(1,8*(3*c['M']+1)**2)))).bit_length(),'giant_powers_expanded':False})
  values.cache_clear()
 return rows

def hierarchy_checks():
 # Construct all classifications with states at and around the enormous actual T.
 for n,E in [(3,[(0,1),(1,2)]),(4,[(0,1),(1,2),(2,3)]),(5,[(0,1),(1,2),(0,2),(3,4)])]:
  c=make(n,E);T=c['T']
  for I in c['faces']:
   for Lmask in range(1<<len(I)):
    L={i for k,i in enumerate(sorted(I)) if Lmask>>k&1}
    for A in [0,1,3]:
     x=[1]*n;U=A+n-len(I)
     for i in I:x[i]=T*(U+1) if i in L else T*(U+1)-1
     got={i for i in I if x[i]>=T*(U+1)};assert got==L
     N=A+sum(x);near,far=parts(n,E,I)
     bad=[(i,j) for i,j in E if i not in I and j not in I and (i in near or j in near)]
     if L:
      nearL,farL=parts(n,E,L)
      assert sum(x[i] for i in I)>=T*(U+1)
      for i,j in bad:
       if i in nearL or j in nearL:
        v=i if i in nearL else j
        u=next(u for u in L if (min(u,v),max(u,v)) in E)
        assert x[i]*x[j]<=F(x[u]*x[v],T); count('bad_to_cross_charges')
       else: assert i in farL and j in farL;count('strict_subset_far_transfers')
      if L==I: assert not any(i in farL and j in farL for i,j in bad)
      UJ=A+sum(x[i] for i in range(n) if i not in L)
      assert UJ<=c['B']*(U+1) and UJ+1<=(c['B']+1)*(U+1)
     else:
      assert N<=c['B']*(U+1) and N+1<=(c['B']+1)*(U+1)
     count('hierarchy_threshold_states')

if __name__=='__main__':
 started=time.monotonic(); source_profile_checks();selector_checks();hierarchy_checks();rows=generator_checks()
 out={'status':'PASS_FINITE_SUPPLEMENT_NOT_EXECUTABLE_ADMISSION','input_sha256':EXPECTED,'counts':C,'fixtures':rows,'no_author_code_imported':True,'no_global_head_power_expanded':True}
 (HERE/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':out['status'],'counts':C,'elapsed_seconds':time.monotonic()-started},sort_keys=True))
