"""Theorem supplement only: no author imports, no process simulation."""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from pathlib import Path
import json
checks=0

def ok(x,label):
 global checks
 checks+=1
 if not x:raise AssertionError(label)
def ceil(x):
 x=F(x);return -(-x.numerator//x.denominator)
def clog(x):
 x=F(x)
 if x<=1:return 0
 k=max(0,x.numerator.bit_length()-x.denominator.bit_length())
 return k+(F(1<<k)<x)
def scalar(n,edges,la,La,mu,Mu,a,b,s,kl,ku,S):
 M=max(2,ceil(12*s/b));q=F(M+1,M);g=kl*M*(2*M+1)/(M+1)**2;h=b*M/4
 cs=(4*M+4)*3**6;ca=cs*(a+ku)+18*Mu*M;ch=cs*s;d=F(1,8*(3*M+3)**2)
 T=max(1,ceil(4*ca/g),ceil(4*ch*len(edges)/h));B=1+n*T;R=(B+1)**2/d
 K=max(2,ceil(4*2**n*ch*R/h));pb=(K+1)**n;ra=pb*ca*(B+1);rq=pb*ch*(B+1)**2
 hh=F(1,16*n)**(n-1)/(2*n);ec=min(F(1,4),hh**2/2,hh/8);ga=hh/32;ss=min(g,h)*d*ec/4
 cb=La*(1+pb)+Mu**2/4;ep=min(F(1),ss/(16*cb));t=1+ep;D=mu*ep/t;fw=2*a+ku;e=min(F(1,4),D/(4*(fw+1)));H=1+ep*(1+pb);da=F(1,8*(3*M+1)**2)
 N=ceil(max(F(2),4*ra/D,rq/(e*b),1+4*Mu*H/(g*da),4*(cb*ep+1)/(D*ga),2*(cb*ep+1)/(e*b*ga**2)))
 nu=min(la,F(1),ss/8);ht=1+pb+H;z=nu/ht;c0=(z+La+Mu*N+S*N*N)*ht
 p=dict(n=n,edges=edges,la=la,La=La,mu=mu,Mu=Mu,a=a,b=b,s=s,kl=kl,ku=ku,S=S,M=M,q=q,g=g,h0=h,Cstep=cs,CA=ca,CH=ch,d=d,T=T,B=B,R=R,K=K,Pbar=pb,RA=ra,RQ=rq,hh=hh,epsC=ec,gamma=ga,sstar=ss,Cbirth=cb,eps=ep,t=t,D=D,Fwd=fw,e=e,H=H,dA=da,Nstar=N,nu=nu,Htot=ht,zeta=z,c0=c0)
 ok(0<ep<=1 and 0<e<=F(1,4),'admitted tilt and correction')
 ok(e*Mu<=mu*Mu*ep/4<=Mu*Mu*ep/4,'different death endpoints')
 ok((1-e)*D-e*fw>=D/2,'baseline margin')
 ok(ep*cb<=ss/16,'face margin')
 ok(4*Mu*H<=g*(N-1)*da,'worst last-copy threshold')
 ok(ra/(N+1)<=D/4 and rq/(N+1)<=e*b,'residual payments')
 ok(D*ga*N/4>=ep*cb+1 and e*b*ga**2*N*N/(N+1)>=ep*cb+1,'both interior payments')
 ok(0<nu<=la and nu<=1 and nu<=ss/8,'common negative rate')
 ok(s*(q*q-1)<=5*b/24,'worst grouped adverse gap')
 return p

def from_rows(rows):
 # Supplied audit fixture uses port coordinate zero. No public raw admission API.
 rows=[(tuple(u),tuple(v),F(lo),F(hi)) for u,v,lo,hi in rows]
 n=len(rows[0][0])-1;zero=(0,)*(n+1);one=(1,)+(0,)*n;two=(2,)+(0,)*n
 port={u:(lo,hi) for u,v,lo,hi in rows if (u,v) in [(zero,one),(one,zero)]}
 internal=[r for r in rows if sum(r[0])==2]
 hubs=sorted({u if u[0]==0 else v for u,v,lo,hi in internal})
 edges=[tuple(i for i in range(1,n+1) if h[i]) for h in hubs]
 kl={i:F(0) for i in range(1,n+1)};ku=kl.copy()
 for u,v,lo,hi in internal:
  if u[0]==1:
   i=next(i for i in range(1,n+1) if u[i]);kl[i]+=lo;ku[i]+=hi
 p=scalar(n,edges,*port[zero],*port[one],sum(hi for u,v,lo,hi in internal if u==two),min(lo for u,v,lo,hi in internal if v==two),max(sum(hi for u,v,lo,hi in internal if u==h) for h in hubs),min(kl.values()),max(ku.values()),sum(hi for u,v,lo,hi in internal))
 return p,rows

def toy(n):
 def z(*idx):return tuple(idx.count(i) for i in range(n+1))
 hub=z(1,2)
 rows=[(z(),z(0),F(1,7),F(3)),(z(0),z(),F(1,3),F(5,2)),(z(0,0),hub,F(2,3),F(4,3)),(hub,z(0,0),F(1),F(2))]
 for i in range(1,n+1):rows.extend([(z(0,i),hub,F(1,2),F(3,2)),(hub,z(0,i),F(1,4),F(5,4))])
 return rows

def propensity(u,x):
 z=1
 for a,b in zip(u,x):
  if a>b:return 0
  for j in range(a):z*=b-j
 return z

def worst(rows,p,x,fn):
 fx=fn(x);out=F(0)
 for u,v,lo,hi in rows:
  prop=propensity(u,x)
  if prop:
   y=tuple(a-b+c for a,b,c in zip(x,u,v));coef=prop*(p['t']**(sum(v)-sum(u))*fn(y)-fx)
   out+=coef*(hi if coef>0 else lo)
 return out

rows_out=[]
for n in [2,3]:
 p,rows=from_rows(toy(n));sat=set(range(1,n+1));faces=[]
 for mask in range(1,1<<n):
  I={i+1 for i in range(n) if mask>>i&1}
  if any(set(e)<=I for e in p['edges']):continue
  near={j for edge in p['edges'] if set(edge)&I for j in edge}-I;far=sat-I-near
  weights=tuple(2*p['M'] if i==0 else 0 if i in I else 2*p['M']+2 if i in near else p['M']+1 for i in range(n+1))
  faces.append((I,near,far,weights,p['K']**(n-len(I))))
 @lru_cache(None)
 def Z(j):return (1-p['q']**(-(j+p['M'])))/(j+p['M'])
 def profile(w,x):return Z(sum(a*b for a,b in zip(w,x)))
 def base(x):return 1-p['e']*x[0]/(sum(x)+1)
 def inactive(x):return x[0]==0 and all(x[i]*x[j]==0 for i,j in p['edges'])
 def multiplier(x):return base(x)+sum(w*profile(ww,x) for I,near,far,ww,w in faces)+(p['H'] if inactive(x) else 0)
 # N<=2 exercises all boundary channels; selected sparse larger states add death.
 states=list(product(range(3),repeat=n+1));states=[x for x in states if sum(x)<=2]
 states += [tuple([3]+[1]*n),tuple([1]+[0]*(n-1)+[5])]
 for x in states:
  A=x[0];N=sum(x);Q=sum(x[i]*x[j] for i,j in p['edges'])
  bbound=p['La']*p['eps']+p['e']*p['Mu']-p['D']*A/2-2*p['e']*p['b']*Q/(N+1)
  ok(worst(rows,p,x,base)<=bbound,'full-box baseline channel check')
  for I,near,far,w,wt in faces:
   j=sum(a*b for a,b in zip(w,x));DD=Z(j)-Z(j+1);U=A+sum(x[i] for i in sat-I);FI=sum(x[i] for i in I)
   cross=sum(x[i]*x[k] for i,k in p['edges'] if (i in I)!=(k in I));fq=sum(x[i]*x[k] for i,k in p['edges'] if i in far and k in far);bad=Q-cross-fq
   reserve=(p['g']*A*FI+p['h0']*(cross+fq))*DD
   upper=p['La']*p['eps']*Z(j)-reserve+p['CA']*A*(U+1)*DD+p['CH']*bad*DD
   ok(worst(rows,p,x,lambda y:profile(w,y))<=upper,'uniform local source inequality')
  if inactive(x):ok(worst(rows,p,x,multiplier)<=-p['la'],'actual coefficient inactive cancellation')
 rows_out.append({'case':'exact full-box endpoint supremum','satellites':n,'states':len(states),'faces':len(faces)})
 Z.cache_clear()
# Extremely separated rate endpoints test each positive floor is retained.
for ell in [1,32,200,512]:
 p=scalar(5,[(1,2)],F(1,1<<ell),F(3),F(1,1<<ell),F(1<<ell),F(4),F(1,1<<ell),F(8),F(1,1<<ell),F(9),F(20))
 ok(p['D']==p['mu']*p['eps']/p['t'],'lower death endpoint actually used')
 ok(p['nu']<=p['la'],'lower immigration endpoint actually used')
 rows_out.append({'case':'separated endpoints','rate_exponent':ell,'M_bits':p['M'].bit_length(),'Nstar_bits':p['Nstar'].bit_length()})
# Independently acquire actual frozen-fixture scalar/budget formulas.
def dec(x):
 if isinstance(x,list):return [dec(v) for v in x]
 if isinstance(x,dict) and set(x)=={'QHEX'}:return F(int(x['QHEX'][0],16),int(x['QHEX'][1],16))
 return x
root=Path(__file__).resolve().parent
p,raw=from_rows(dec(json.loads((root/'inputs/raw_box.json').read_text())))
def budget(p,U,T,alpha):
 beta=alpha/2;block=ceil(1/p['eps']);L=max(U,p['Nstar']+1) if T else U
 ratio=F(4,3)*(p['Htot']+p['c0']*T)/beta;k=clog(ratio);RF=L+block*k
 im=2*ceil(p['La']*T)+clog(1/beta);RP=U+im;R=min(RF,RP)
 Lam=p['La']+p['Mu']*R+p['S']*R*R;m=2*ceil(Lam*T)+clog(1/beta)
 ok(block*p['eps']>=1,'Bernoulli block')
 ok(F(1<<k)>=ratio and (k==0 or F(1<<(k-1))<ratio),'minimal dyadic count exponent')
 ok(F(4,3)*(p['Htot']+p['c0']*T)/F(1<<k)<=beta,'Foster cap probability arithmetic')
 ok(R>U and m>=1,'nontrivial boundary at horizon zero too')
 ok(F(1,1<<clog(1/beta))<=beta,'Poisson cap confidence arithmetic')
 return R,m,RF<RP
for T in [F(0),F(1),F(1<<1121),F(1<<1122)]:
 R,m,f=budget(p,10,T,F(1,100));rows_out.append({'case':'frozen raw fixture budget','horizon_exponent':T.numerator.bit_length()-1 if T else None,'Foster_wins':f,'count_level_bits':R.bit_length(),'firing_level_bits':m.bit_length()})
 if T==1:ok((R,m)==(24,116462),'ordinary short-horizon reported fixture')
 if T==1<<1121:ok(not f,'pre-crossover reported fixture')
 if T==1<<1122:ok(f,'crossover reported fixture')
# Check log ceilings independently against a brute dyadic loop on modest rationals.
for a in range(1,45):
 for b in range(1,35):
  q=F(a,b);k=0
  while F(1<<k)<q:k+=1
  ok(clog(q)==k,'exact ceil_log2')
# Path-dependent overlapping-episode risk accounting: every finite branch remains paid.
for history in product([0,1],repeat=8):
 total=F(1,20);spent=F(0)
 for j,bit in enumerate(history):
  allocated=(total-spent)/(2+bit)
  ok(allocated>0 and spent+allocated<=total,'predictable remaining-risk reservation')
  spent+=allocated
 ok(spent<total,'finite branch sum invariant')
result={'status':'PASS_INDEPENDENT_COMMON_BOX_THEOREM_CHECKS','assertions':checks,'no_author_code_imported':True,'no_process_simulation':True,'code_acceptance':False,'rows':rows_out}
(root/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
