from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations,product
from copy import deepcopy
import sys,json,hashlib,random,time
A=Path(__file__).resolve().parent;version=sys.argv[1]if len(sys.argv)>1 else 'v1';sys.path.insert(0,str(A/('replay_'+version)));import common_box as C
checks=0;cats={};rng=random.Random(11010320);start=time.perf_counter()
def ok(z,k):
 global checks
 assert z,k
 checks+=1;cats[k]=cats.get(k,0)+1

def ceil(q):return (q.numerator+q.denominator-1)//q.denominator

def log2(q):
 if q<=1:return 0
 k=q.numerator.bit_length()-q.denominator.bit_length()
 if k<0:k=0
 return k+(Q(2**k)<q)

def reference(raw):
 m=len(raw[0][0]);rates={}
 for u,v,l,h in raw:
  key=(tuple(u),tuple(v));old=rates.get(key,(Q(0),Q(0)));rates[key]=(old[0]+l,old[1]+h)
 zero=(0,)*m;one=next(v for u,v in rates if u==zero);axis=one.index(1);two=tuple(2*z for z in one);sat=tuple(i for i in range(m)if i!=axis)
 hubs=sorted({u for u,v in rates if sum(u)==2 and u[axis]==0});edges=tuple(sorted(tuple(i for i,z in enumerate(u)if z)for u in hubs))
 la,La=rates[(zero,one)];mu,Mu=rates[(one,zero)];aa=sum(rates[(two,u)][1]for u in hubs);bb=min(rates[(u,two)][0]for u in hubs);ss=max(sum(h for (u,v),(l,h)in rates.items()if u==hub)for hub in hubs)
 lower=[];upper=[]
 for i in sat:
  arm=tuple(one[j]+(j==i)for j in range(m));lower.append(sum(l for (u,v),(l,h)in rates.items()if u==arm));upper.append(sum(h for (u,v),(l,h)in rates.items()if u==arm))
 kl=min(lower);ku=max(upper);S=sum(h for (u,v),(l,h)in rates.items()if sum(u)==2);n=m-1
 M=max(2,ceil(12*ss/bb));q=Q(M+1,M);g=kl*M*(2*M+1)/(M+1)**2;h=bb*M/4;cs=2916*(M+1);ca=cs*(aa+ku)+18*Mu*M;ch=cs*ss;d=Q(1,72*(M+1)**2)
 T=max(1,ceil(4*ca/g),ceil(4*len(edges)*ch/h));B=1+n*T;R=(B+1)**2/d;K=max(2,ceil(2**(n+2)*ch*R/h));pb=(K+1)**n;ra=pb*ca*(B+1);rq=pb*ch*(B+1)**2
 delta=Q(1,4);eta=Q(1,16*n);hh=eta**(n-1)/(2*n);ec=min(Q(1,4),hh*hh/2,hh/8);gam=hh/32;star=min(g,h)*d*ec/4;birth=La*(1+pb)+Mu*Mu/4;eps=min(Q(1),star/(16*birth));t=1+eps;D=mu*eps/t;fw=2*aa+ku;e=min(Q(1,4),D/(4*fw+4));H=1+eps*(1+pb);da=Q(1,8*(3*M+1)**2)
 Ns=max(ceil(x)for x in [Q(2),4*ra/D,rq/(e*bb),1+4*Mu*H/(g*da),4*(birth*eps+1)/(D*gam),2*(birth*eps+1)/(e*bb*gam*gam)]);nu=min(la,Q(1),star/8);ht=1+pb+H;zeta=nu/ht;c0=(zeta+La+Mu*Ns+S*Ns**2)*ht
 scalars=dict(M=M,q=q,aw=2*M,W=2*M+2,g=g,h=h,Cstep=cs,CA=ca,CH=ch,d=d,T=T,B=B,R=R,K=K,Pbar=pb,RA=ra,RQ=rq,delta=delta,eta=eta,hh=hh,epsC=ec,gamma=gam,sstar=star,Cbirth=birth,eps=eps,t=t,D=D,Fwd=fw,e=e,H=H,dA=da,Nstar=Ns,nu=nu,Htot=ht,zeta=zeta,CF_prefactor=c0)
 parsed=dict(m=m,A=axis,n=n,sat=sat,edges=edges,channels=tuple((u,v,l,h)for (u,v),(l,h)in sorted(rates.items())),lam_lo=la,lam_hi=La,mu_lo=mu,mu_hi=Mu,a_hi=aa,b_lo=bb,s_hi=ss,kmin_lo=kl,kmax_hi=ku,Srate_hi=S)
 return scalars,parsed

def make(n):
 m=n+1;port=rng.randrange(m);sat=[i for i in range(m)if i!=port];z=lambda *ix:tuple(ix.count(i)for i in range(m));hubsets=list(combinations(sat,2));rng.shuffle(hubsets);hubsets=hubsets[:rng.randrange(1,len(hubsets)+1)]
 arcs=[(z(),z(port))]
 for u,v in hubsets:arcs.append((z(port,port),z(u,v)))
 for i in sat:
  u,v=rng.choice(hubsets);arcs.append((z(port,i),z(u,v)))
 rows=[]
 for u,v in arcs:
  for a,b in [(u,v),(v,u)]:
   lo=Q(rng.randrange(1,15),rng.randrange(1,15));hi=lo+Q(rng.randrange(8),rng.randrange(1,11))
   if rng.randrange(3)==0:rows.extend([(a,b,lo/3,hi/3),(a,b,2*lo/3,2*hi/3)])
   else:rows.append((a,b,lo,hi))
 rng.shuffle(rows);return rows

def budget_ref(p,r,U,T,a):
 half=a/2;b=ceil(1/p['eps']);L=max(U,p['Nstar']+1)if T else U;ratio=Q(8,3)*(p['Htot']+T*p['CF_prefactor'])/a;k=log2(ratio);RF=L+b*k;RP=U+2*ceil(r['lam_hi']*T)+log2(1/half);R=min(RF,RP);rate=r['lam_hi']+r['mu_hi']*R+r['Srate_hi']*R*R;fire=2*ceil(rate*T)+log2(1/half)
 return dict(count_level=R,firing_level=fire,foster_count_level=RF,immigration_count_level=RP,total_rate_cap=rate,selected_count_cap='COMMON_FOSTER_LOG_HORIZON'if RF<RP else 'ORDINARY_IMMIGRATION_POISSON'),(b,L,ratio,k)

for case in range(48):
 raw=C.fixture()if case==0 else make(2+case%6);p=C.construct(raw);ps,rr=reference(raw)
 for k,v in rr.items():ok(p['raw'][k]==v,'independent raw graph aggregation and all endpoint constants')
 for k,v in ps.items():ok(p[k]==v,'independent complete scalar acquisition including lower death and immigration')
 ok(p['CF_expression']=={'coefficient':ps['CF_prefactor'],'base':ps['t'],'exponent':ps['Nstar']+1},'finite head remains exact factored power not evaluated')
 for j in range(6):
  U=rng.randrange(100)if j<4 else 2**(500+j);T=Q(0)if j==0 else Q(1<<1122)if case==0 and j==5 else Q(rng.randrange(1000),rng.randrange(1,100));a=Q(1,rng.randrange(2,1000))
  b=C.resource_budget(p,U,T,a);br,wr=budget_ref(ps,rr,U,T,a)
  for k,v in br.items():ok(b[k]==v,'independent exact count firing and ordinary-versus-Foster cap')
  block,L,ratio,k=wr;ok(block*ps['eps']>=1 and (block-1)*ps['eps']<1,'minimal Bernoulli block')
  ok(Q(2**k)>=ratio and (k==0 or Q(2**(k-1))<ratio),'minimal dyadic Foster ceiling')
  ok(b['count_level']>U and b['firing_level']>0,'zero horizon and initially bounded count off-by-one')
for num in range(1,85):
 for den in range(1,50):
  x=Q(num,den);k=0
  while 2**k<x:k+=1
  ok(C.ceil_log2_at_least_one(x)==k,'brute least dyadic ceiling')
# Exact Poisson exponential-polynomial bound independent of exp floats.
for n in range(100):
 mean=Q(rng.randrange(100),rng.randrange(1,30));risk=Q(1,rng.randrange(2,300));b=C.poisson_dyadic_threshold(mean,risk);m=b['threshold'];vc=ceil(mean);k=log2(1/risk)
 ok(m==2*vc+k and Q(1,2**k)<=risk,'actual Poisson dyadic cap with one confidence allocation')
# Full smaller graph faces and actual literal multiplier and drift, no source oracle.
raw=make(2);p=C.construct(raw);r=p['raw'];fs=C.faces(p);sat=r['sat'];ind=[]
for size in range(1,len(sat)+1):
 for I in combinations(sat,size):
  I=set(I)
  if any(a in I and b in I for a,b in r['edges']):continue
  near={b for a,b in r['edges']if a in I}|{a for a,b in r['edges']if b in I};near-=I
  weights=tuple(p['aw']if i==r['A']else 0 if i in I else p['W']if i in near else p['M']+1 for i in range(r['m']));ind.append((weights,p['K']**(r['n']-len(I))))
ok(set(fs)==set(ind),'actual all-independent-face weights resource geometry')
# Use exact full profile within explicitly permitted exponent/bit budgets.
def mult(x):
 N=sum(x);av=x[r['A']];value=1-p['e']*Q(av,N+1)+(p['H']if av==0 and all(x[i]*x[j]==0 for i,j in r['edges'])else 0)
 return value+sum((w*(1-p['q']**(-sum(a*b for a,b in zip(weights,x))-p['M']))/(sum(a*b for a,b in zip(weights,x))+p['M'])for weights,w in ind),Q(0))
for x in list(product(range(2),repeat=3))+[tuple(1 if i==r['A']else 3 for i in range(3))]:
 fx=mult(x);ok(C.multiplier(p,x,fs,max_exponent=100000,max_bits=2000000)==fx,'actual full multiplier including inactive and last-copy states')
 total=Q(0);fxv=fx;wit=[]
 for u,v,l,h in r['channels']:
  prop=1
  for a,b in zip(u,x):
   for j in range(a):prop*=max(0,b-j)
  if prop:
   y=tuple(xx-uu+vv for xx,uu,vv in zip(x,u,v));coeff=prop*((p['t']if sum(v)>sum(u)else 1/p['t']if sum(v)<sum(u)else 1)*mult(y)-fxv);z=h if coeff>0 else l;total+=z*coeff;wit.append(z)
  else:wit.append(l)
 got=C.worst_scaled_drift(p,x,mult);ok(got==(total,tuple(wit)),'actual full multiplier box extremum endpoint and falling-factorial mapping')
# Same fixture exact practical cap and enormous crossover.
p=C.construct(C.fixture())
for T,which in [(Q(1),'ORDINARY_IMMIGRATION_POISSON'),(Q(1<<1121),'ORDINARY_IMMIGRATION_POISSON'),(Q(1<<1122),'COMMON_FOSTER_LOG_HORIZON')]:
 b=C.resource_budget(p,10,T,Q(1,100));ok(b['selected_count_cap']==which,'ordinary comparator and enormous adjacent dyadic crossover retained')
 if T==1:ok((b['count_level'],b['firing_level'])==(24,116462),'literal short horizon count and firing levels')
report={'status':'PASS','version':version,'checks':checks,'categories':cats,'seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256(Path(C.__file__).read_bytes()).hexdigest(),'scope':'independent exact full scalar and raw endpoint acquisition, integer caps, actual small full profiles/drifts; no stochastic simulation or sensor assurance'}
(A/('arithmetic_'+version+'_results.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
