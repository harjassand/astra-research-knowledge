from fractions import Fraction as F
from itertools import product,permutations
import json,random,copy
import cover_seed as C
COUNT=dict(states=0,jumps=0,profile_checks=0,boundary_states=0,interior_states=0,outside_Foster=0,heavy_absorptions=0,mutations=0)
rows=[]
def run(raw,t,name):
 rec=C.recognize(raw);cert=C.numerical(raw,t,max_profile_steps=200000);assert cert['status']=='CERTIFIED_NUMERICAL';co=cert['constants'];n=rec['n'];a=rec['a'];edges=rec['edges'];E=len(edges)
 g=lambda r:C.profile(cert,r);d=lambda r:g(r)-g(r+1)
 # Every finite profile/head compensation join plus a deterministic spread of tail points.
 for r in list(range(1,co['J']+2))+[10*co['J'],10**20]:
  assert rec['lam']*(t*g(r+1)-g(r))-co['beta']*r*r*d(r)<=-co['epsilon0']*g(r)
  assert (r+1)**2*d(r)>=co['dstar'] and d(r-1)<=co['G']*d(r)
  er=rec['mu']*(g(r-1)/t-g(r))+co['Kf']*r*d(r-1)+2*co['beta']*r*d(r)+co['epsilon']*(rec['F0']+co['D'])
  if r<co['J']:assert co['q']*rec['kminus']/(4*(r+1)**2)>=max(er,0)
  else:assert er<=-co['D']/4
  COUNT['profile_checks']+=1
 states=list(product(range(3),repeat=n))
 N0=co['Nstar'];rng=random.Random(710+n+E)
 for scale in (N0,2*N0,10**30):
  for j in range(n):
   x=[0]*n;x[j]=scale;states.append(tuple(x))
   for A in (0,1,2,co['K']-1,co['J']):
    y=x.copy();y[a]+=A
    for v in range(n):
     z=y.copy();z[v]+=1;states.append(tuple(z))
  for _ in range(20):states.append(tuple(rng.randrange(0,scale+1)for j in range(n)))
 # Exact P4 adverse overlap ray, slow latent ray and balanced interior.
 if n==5 and edges==((1,2),(2,3),(3,4)):
  for scale in (1,10,N0,10**40):states.extend([(0,scale,1,1,scale),(0,1,1,0,scale),(0,scale,scale,scale,scale)])
 for x in states:
  N,A,tau,r,weights=C.coordinates(rec,cert,x);h=C.hvalue(rec,cert,x);assert F(3,4)<=h<=co['H']
  opt=[cc for cc,w in zip(cert['covers'],weights)if w==tau]
  bad=set(e for e in edges if any(e[0]in cc and e[1]in cc for cc in opt));qb=sum(x[u]*x[v]for u,v in bad);Q=sum(x[u]*x[v]for u,v in edges);qg=Q-qb
  heavy=[v for v in rec['satellites']if x[v]>r];hb=sum(x[v]for v in heavy)
  assert 4*E*Q>=tau*tau
  if hb:assert qb*hb<=E*r*qg;COUNT['heavy_absorptions']+=1
  f=F(A,(r+1)**2);lg=lf=lneg=F(0)
  for u,v,k in rec['internal']:
   rate=k*C.falling(x,u)
   if not rate:continue
   xp=tuple(xx-uu+vv for xx,uu,vv in zip(x,u,v));Np,Ap,taup,rp,wp=C.coordinates(rec,cert,xp)
   assert Np==N and abs(rp-r)<=1 and (not r or rp>=1)
   fp=F(Ap,(rp+1)**2);assert abs(fp-f)<=F(11,(r+1)**2)
   lg+=rate*(g(rp)-g(r));lf+=rate*(fp-f);lneg+=rate*(-co['epsilon']*F(Ap-A,N+1))
   if u[a]==0 and v[a]==2:
    edge=tuple(i for i,z in enumerate(u)if z);assert rp-r==(0 if edge in bad else 1)
   if u[a]==1 and v[a]==0:
    xx=next(i for i,z in enumerate(u)if i!=a and z)
    if xx in heavy:assert rp>=r and fp-f<=-F(1,(r+1)**2)
   COUNT['jumps']+=1
  if r:
   assert lg<=co['Kf']*A*r*d(r-1)+rec['smax']*qb*d(r-1)-rec['bmin']*qg*d(r)
   assert lf<=(-rec['kminus']*A*hb+11*co['Kf']*r*r+11*rec['smax']*Q)/(r+1)**2
   assert lneg<=co['epsilon']*rec['F0']*A-co['epsilon']*rec['b0']*F(Q,N+1)
  actual=C.scaled_drift(rec,cert,x)
  if N>=N0:
   assert actual<=-co['zeta']*h,(name,x,actual,co['zeta'],h)
   COUNT['outside_Foster']+=1
   if r and r<=co['delta']*N:
    assert qb<=qg and rec['smax']*qb*d(r-1)<=rec['bmin']*qg*d(r)/4
    assert 11*co['q']*rec['smax']*F(Q,(N+1)*(r+1)**2)<=rec['bmin']*qg*d(r)/4
    assert actual<=-co['epsilon0']*g(r)/2;COUNT['boundary_states']+=1
   elif r:
    assert actual<=co['Cint']-co['D']*A/2-co['epsilon']*rec['b0']*F(Q,N+1)
    assert actual<=-1;COUNT['interior_states']+=1
  COUNT['states']+=1
 rows.append(dict(name=name,dimension=n,edges=edges,t=t,cover_count=len(cert['covers']),K=co['K'],J=co['J'],Nstar=N0,work=cert['work'],certificate_sha256=C.digest(cert)))
 return rec,cert
rec,cert=run(C.fixture(),F(2),'nonCB_P4')
run(C.fixture(edges=((1,2),(2,3),(3,4),(4,5),(1,5)),n=6),F(3,2),'C5')
run(C.fixture(edges=((1,2),(1,3),(2,3)),n=4),F(3,2),'triangle')
run(C.fixture(edges=((1,2),(3,4)),n=6),F(3,2),'two_bicliques_and_free_passenger')
# Joint extreme t/rate choices keep paid profile loops finite; no universal efficiency claim.
raw=C.fixture()
for j,(u,v,k)in enumerate(raw):
 if sum(u)==0:raw[j]=(u,v,F(1,10000))
 elif u[0]==0 and v[0]==2:raw[j]=(u,v,F(10))
run(raw,F(100),'large_t_small_inflow')
raw=C.fixture()
for j,(u,v,k)in enumerate(raw):
 if sum(v)==0 or (u[0]==0 and v[0]==2):raw[j]=(u,v,F(10**60))
run(raw,1+F(1,10**50),'near_one_t_large_death_and_amplification')
# Inexact values and budget semantics.
for bad in (True,2.0,'2',F(1),0,-1):
 try:C.numerical(C.fixture(),bad)
 except (TypeError,ValueError):pass
 else:raise AssertionError(('bad_t',bad))
qual=C.qualitative(C.fixture());budget=C.numerical(C.fixture(),F(2),max_profile_steps=0)
assert qual['status']=='CERTIFIED_QUALITATIVE'and budget['status']=='UNKNOWN_NUMERICAL_BUDGET'and budget['qualitative']==qual
for graph,n in [(((1,2),(1,3),(2,3)),5),(((1,2),(2,3),(3,4)),6)]:
 raw=C.fixture(edges=graph,n=n,special=False);got=C.qualitative(raw);assert got['status']=='UNKNOWN'
 # All rates1 gives direct detailed-balance ordinary stability, not an instability witness.
 assert all(k==1 for u,v,k in raw)
for key in list(cert['constants']):
 mutated=copy.deepcopy(cert);mutated['constants'][key]+=1
 assert not C.receive_numerical(C.fixture(),F(2),mutated);COUNT['mutations']+=1
print(json.dumps(C.encode(dict(status='PASS',counts=COUNT,cases=rows,scope='Finite exact corroboration; no simulated stability inference',no_simulation=True,no_power_expansion=True,no_head_enumeration=True)),indent=2))
