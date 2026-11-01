"""Independent literal generator and rigorous rational interval supplements.
No author code imported; no evaluated head is inferred from finite tests.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from itertools import product
import hashlib,json,time
PTH=Path(__file__).resolve().parent
r=F(1000001,1000000);delta=r-1;Delta=1-1/r;kappa=F(1,1000)
def v(*xs):return tuple(xs.count(i)for i in range(5))
rows=[(v(),v(0),1,'birth'),(v(0),v(),1,'death')]
for i in [2,3,4]:rows.extend([(v(0,0),v(0,i),1,'forward_'+str(i)),(v(0,i),v(0,0),1,'reverse_'+str(i))])
rows.extend([(v(0,4),v(2,3),1,'AE_CD'),(v(2,3),v(0,4),2,'CD_AE'),(v(2,3),v(0,1),1,'CD_AB'),(v(0,1),v(2,3),1,'AB_CD')])
def coords(x):A,B,C,D,E=x;return A+C,A+D,F(B-A-99*E,100)
def Q(c,d,t):return c*d*t+F(c+d,2)*t*t+t*t*t/3
@lru_cache(None)
def root(c,d,H):
 if H<=0:return F(0),F(0)
 lo=F(0);hi=F(1)
 while 2*Q(c,d,hi)<H:hi*=2
 for _ in range(256):
  m=(lo+hi)/2;z=2*Q(c,d,m)
  if z==H:return m,m
  if z<H:lo=m
  else:hi=m
 return lo,hi
@lru_cache(None)
def ex(x):
 if x<0:
  l,h=ex(-x);return 1/h,1/l
 if x>1:
  l,h=ex(x/2);return l*l,h*h
 term=total=F(1)
 for k in range(1,65):term=term*x/k;total+=term
 rem=(term*x/65)/(1-x/66)
 return total,total+rem

def trans(x):
 for u,w,k,name in rows:
  rate=k
  for a,b in zip(x,u):
   if a<b:rate=0;break
   for j in range(b):rate*=a-j
  if rate:yield rate,tuple(a-b+c for a,b,c in zip(x,u,w)),sum(w)-sum(u),name

def rec(x):
 A=x[0];c,d,H=coords(x);return F(1,c+1)+F(1,d+1),-F(A,(c+1)*(d+1))
@lru_cache(None)
def val(x):
 A,B,C,D,E=x;tl,th=root(*coords(x));hl=1+20*F(A*A,B+1)*min(tl*tl/4,1);hh=1+20*F(A*A,B+1)*min(th*th/4,1);el,eh=ex(tl)[0],ex(th)[1];P,R=rec(x)
 assert 1<=hl<=hh<=F(21,20)
 return tl,th,hl,hh,el,eh,el*hl+10*P+kappa*R,eh*hh+10*P+kappa*R

def ceil(x):return -(-x.numerator//x.denominator)
def floor(x):return x.numerator//x.denominator

def main():
 start=time.monotonic();states=set();pairs=[(0,0),(1,1),(0,10**12),(10**12,0),(1,10**12),(10**12,1),(10**12,10**12)]
 for A,E,(C,D),hn in product([0,1,2,1000],[0,10**24],pairs,[-101,-100,-99,-1,0,1,99,100]):
  B=A+99*E+hn
  if B>=0:states.add((A,B,C,D,E))
 for A,E,(C,D),t in product([0,1,2,1000],[0,10**24],pairs,[F(1,10**6),F(1,2),F(4,5),F(1999,1000),F(2),F(2001,1000),F(3)]):
  hn=100*2*Q(A+C,A+D,t)
  for j in {floor(hn),ceil(hn)}:states.add((A,A+99*E+j,C,D,E))
 for n,A,(C,D),t in product([10,10**3,10**6,10**12,10**24],[0,1,5],[(0,0),(1,1),(0,1),(1,0)], [F(0),F(1,10**6),F(1)]):
  for cc,dd in [(C+n,D+n),(C,D+n),(C+n,D),(C,D)]:
   E=n;hn=ceil(200*Q(A+cc,A+dd,t));states.add((A,A+99*E+hn,cc,dd,E))
 for n in [1,10,1000,10**6,10**12,10**24]:states.add((n,n,0,0,0))
 counts={'low_budget':0,'charging_budget':0,'P_exact_identity':0,'R_upper_budget':0,'AE_bare_six':0,'AE_bare_nonpositive_above_4_5':0,'AE_phase_7':0,'death_positive_remainder':0,'actual_kink_entrances':0,'actual_clip_crossings':0};positive=[];maxN=0;worstlow=None;worstcharge=None
 for x in sorted(states):
  A,B,C,D,E=x;c,d,H=coords(x);tl,th,hl,hh,el,eh,fl,fh=val(x);tr=list(trans(x));maxN=max(maxN,sum(x));gl=gh=F(0);LP=F(0);DR=F(0);ae=[]
  dc=F(1,(c+1)*(c+2));dd=F(1,(d+1)*(d+2));P,R=rec(x)
  for rate,y,dn,name in tr:
   yl,yh,hyl,hyh,eyl,eyh,fyl,fyh=val(y);gl+=rate*(r**dn*fyl-fh);gh+=rate*(r**dn*fyh-fl);py,ry=rec(y);LP+=rate*(py-P);DR+=rate*(r**dn*ry-R)
   counts['actual_kink_entrances']+=int(H<=0 and yl>0);counts['actual_clip_crossings']+=int(tl>=2 and yh<2 or th<2 and yl>=2)
   if name in ['reverse_4','AE_CD']:ae.append((y,eyl,eyh,hyl,hyh))
   if name=='death'and th<2:
    assert rate*(eyh*hyh-el*hl)<=32*el,(x,'death remainder');counts['death_positive_remainder']+=1
  pos=(2*A*A-A)*(F(1,c*(c+1))+F(1,d*(d+1)))if A else F(0)
  assert LP==pos-(1+A*E)*(dc+dd)-A*C*dd-A*D*dc;counts['P_exact_identity']+=1
  rbound=F(9,2)+delta+76*A*E*(dc+dd)-F(3*C*D,(c+1)*(d+1))
  if A:rbound+=200*A*th*(1+th/A+th*th/(3*A*A))
  assert DR<=rbound,(x,'R upper');counts['R_upper_budget']+=1
  if ae:
   assert len(ae)==2 and A*E>0
   barehi=sum(z[2]for z in ae)-2*el
   assert barehi<=6*(dc+dd),(x,'AE bare six');counts['AE_bare_six']+=1
   if tl>=F(4,5):assert barehi<=0,(x,'AE bare nonpositive');counts['AE_bare_nonpositive_above_4_5']+=int(tl>=F(4,5))
   if th<2:
    ph=sum(ex(val(y)[1]-tl)[1]*(hyh-1)for y,eyl,eyh,hyl,hyh in ae)-2*(hl-1)
    b=F(20,B+1)*(F(3,2)*th*th+2*th+F(1,2*c*d))
    assert ph<=b,(x,'AE phase7');counts['AE_phase_7']+=1
  assert th<2 or tl>=2,(x,'ambiguous threshold')
  if th<2:
   bound=2700-Delta*A-F(981,250)*A*E*(dc+dd)-10*(dc+dd)-10*A*C*dd-10*A*D*dc-F(3,1000)*F(C*D,(c+1)*(d+1))
   assert gh<=bound,(x,'low budget',str(gh-bound));counts['low_budget']+=1
   margin=floor((bound-gh)*10**6)
   if worstlow is None or margin<worstlow['margin_millionths']:worstlow={'x':x,'margin_millionths':margin}
  else:
   assert gh+fh/100<=0,(x,'charging budget');counts['charging_budget']+=1
   margin=floor((-gh-fh/100)*10**6)
   if worstcharge is None or margin<worstcharge['margin_millionths']:worstcharge={'x':x,'margin_millionths':margin}
  if gl>0:positive.append({'x':x,'N':sum(x),'drift_lower_millionths':floor(gl*10**6),'drift_upper_millionths':ceil(gh*10**6)})
 # Preserve the finite positive drift at A=B=1000: it refutes any head-free reading.
 witness=next(z for z in positive if z['x']==(1000,1000,0,0,0));assert witness['drift_lower_millionths']>0
 result={'status':'PASS_EXACT_RATIONAL_GLOBAL_PROOF_SUPPLEMENTS','counts':counts,'states':len(states),'maximum_population':str(maxN),'positive_drift_states_retained':len(positive),'positive_finite_head_witness':witness,'worst_low_budget_margin':worstlow,'worst_charging_margin':worstcharge,'root_bisection_steps':256,'exponential_taylor_degree':64,'author_code_imported':False,'giant_r_power_expanded':False,'finite_head_evaluated':False,'runtime_admission_claimed':False,'inputs':{n:hashlib.sha256((PTH/n).read_bytes()).hexdigest()for n in ['GLOBAL_FOSTER_FINITE_HEAD_AUTHOR.md','ANGULAR_BASELINE_FAILURE.md','AE_EXPONENTIAL_PAID_BY_SIX_RECIPROCALS.md']}}
 (PTH/'INDEPENDENT_GLOBAL_CHECKS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'elapsed_seconds':time.monotonic()-start,'states':len(states),'counts':counts},sort_keys=True))
if __name__=='__main__':main()
