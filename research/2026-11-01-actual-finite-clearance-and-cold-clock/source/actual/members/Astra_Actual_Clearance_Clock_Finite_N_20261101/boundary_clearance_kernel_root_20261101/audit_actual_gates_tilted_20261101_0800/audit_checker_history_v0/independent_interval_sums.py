#!/usr/bin/env python3
"""Independent directed interval enclosure of the literal six gate sums.
No author imports. Decimal elementary functions are correctly rounded; one
additional ulp outward encloses each such result. All ordinary arithmetic is
rounded toward the appropriate endpoint. Tiny terms use a separately proved
safe cutoff, not the author's expupper cutoff.
"""
from decimal import Decimal as D, localcontext, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN
from fractions import Fraction as F
from pathlib import Path
import json, math
P=Path(__file__).resolve().parent; PREC=100

def op(f,mode):
 with localcontext() as c:
  c.prec=PREC;c.rounding=mode;return +f()
def tr(x,name,upper):
 with localcontext() as c:
  c.prec=PREC;c.rounding=ROUND_HALF_EVEN
  y=getattr(x,name)()
  return y.next_plus() if upper else y.next_minus()
class I:
 def __init__(self,lo,hi=None):self.lo=D(lo);self.hi=D(lo if hi is None else hi);assert self.lo<=self.hi
 def __add__(a,b):
  b=asI(b);return I(op(lambda:a.lo+b.lo,ROUND_FLOOR),op(lambda:a.hi+b.hi,ROUND_CEILING))
 __radd__=__add__
 def __neg__(a):return I(-a.hi,-a.lo)
 def __sub__(a,b):return a+-asI(b)
 def __rsub__(a,b):return asI(b)+-a
 def __mul__(a,b):
  b=asI(b);pairs=[(x,y) for x in (a.lo,a.hi) for y in (b.lo,b.hi)]
  return I(min(op(lambda:x*y,ROUND_FLOOR) for x,y in pairs),max(op(lambda:x*y,ROUND_CEILING) for x,y in pairs))
 __rmul__=__mul__
 def __truediv__(a,b):
  b=asI(b);assert not b.lo<=0<=b.hi
  return a*I(op(lambda:1/b.hi,ROUND_FLOOR),op(lambda:1/b.lo,ROUND_CEILING))
 def __rtruediv__(a,b):return asI(b)/a
 def __pow__(a,n):
  assert isinstance(n,int) and n>=0
  y=I(1)
  for k in range(n):y=y*a
  return y
 def ln(a):assert a.lo>0;return I(tr(a.lo,'ln',False),tr(a.hi,'ln',True))
 def sqrt(a):assert a.lo>=0;return I(0 if a.lo==0 else tr(a.lo,'sqrt',False),tr(a.hi,'sqrt',True))
 def exp(a):return I(tr(a.lo,'exp',False),tr(a.hi,'exp',True))
 def ceil(a):return I(a.lo.to_integral_value(rounding=ROUND_CEILING),a.hi.to_integral_value(rounding=ROUND_CEILING))
 def out(a):return {'lower':str(a.lo),'upper':str(a.hi)}
def asI(x):return x if isinstance(x,I) else I(x)
def minimum(*xs):
 xs=[asI(x) for x in xs];return I(min(x.lo for x in xs),min(x.hi for x in xs))
# Prove exp(-128)<1e-55 by the positive rational exponential partial sum.
term=F(1);lower=term
for k in range(1,401):term*=F(128,k);lower+=term
assert lower>10**55
all_exps=[]
def pe(y,label):
 all_exps.append((label,y))
 if y.hi<=-128:return I(0,'1e-55')
 return y.exp()
rows=[]
for power in range(20,26):
 N=I(10**power);T=(N.ln()/5).exp();mu=I('.9')*N;m=I(400);ln2=I(2).ln()
 r0=1+3*m*m;H0=2*m*r0/(mu-2*m);rho0=(r0+8*m**3+2*m)/mu
 startup={'A':2*m*r0*rho0**2,'marks':(4+2*m)*H0,
  'E':pe(-(8*ln2-4)*m**3,(power,'startupE')),
  'time':pe(-(1-ln2)*m,(power,'startupTime'))}
 total=sum(startup.values(),I(0));num=0;categories={k:I(0) for k in ['A','Z','floor','time','birth','source']};m_int=400
 while m_int<10**power/5000:
  m=I(m_int);h=m/400;U=minimum(2*m,N/5000);d=minimum(4*m,4*T)
  Ebar=minimum(128*m**3,2*(N*m).sqrt(),N/100).ceil()
  r=1+3*U**2;b=Ebar+2*U;rho=(r/h+b)/mu
  assert rho.hi<D('.545')
  a=I(2) if num==0 else h
  DD=a+2*(Ebar+1)+d;v=8*U*DD/mu;dz=h+1
  if num==0:
   pa=rho+d*r*rho**2
   # Still inspect the exact author exponent before its initial correction.
   oldloga=(1+d*r).ln()+2*rho.ln();all_exps.append(((power,num,'authorA0'),oldloga))
  else:pa=pe((1+d*(r+b*(h-1))).ln()+(h+1)*rho.ln(),(power,num,'A'))
  ratio=dz/v;asinh=(ratio+(1+ratio**2).sqrt()).ln()
  # Stable exact identity sqrt(v^2+dz^2)-v=dz^2/(sqrt(...)+v).
  logz=ln2-dz*asinh+dz**2/((v**2+dz**2).sqrt()+v)
  probs={'A':pa,'Z':pe(logz,(power,num,'Z')),
   'floor':pe(-ln2*m/2,(power,num,'floor')),
   'time':pe(ln2*(m+1)-4*(2*ln2-1)*m,(power,num,'time')),
   'birth':pe(-(128*ln2-64)*m**3,(power,num,'birth')),
   'source':pe(-DD/124,(power,num,'source'))}
  for k,val in probs.items():categories[k]=categories[k]+val;total=total+val
  m_int*=2;num+=1
 author=json.loads((P/'source_snapshot/gates/actual_gates_checks.json').read_text())['results'][power-20]
 claimed=D(author['outward_table_bound'])
 assert total.hi<claimed,(power,total.out(),str(claimed))
 rows.append({'power':power,'stage_count':num,'total':total.out(),'author_table_bound':str(claimed),
              'strict_upper_margin':str(op(lambda:claimed-total.hi,ROUND_FLOOR)),
              'startup':{k:v.out() for k,v in startup.items()},'stage_sums':{k:v.out() for k,v in categories.items()}})
# The author's universal clamp is not universally outward. For this finite set
# of actual invocations, however, every clamped exponent is safely <=-9211.
# ln10<2.3026 implies exp(-9211)<1e-4000. Certify ln10 upper with intervals.
assert I(10).ln().hi<D('2.3026')
clamped=[(label,y) for label,y in all_exps if y.hi<-9200]
assert all(y.hi<=-9211 for label,y in clamped)
nearest=max(clamped,key=lambda a:a[1].hi)
out={'status':'PASS_INDEPENDENT_OUTWARD_ENCLOSURES_ALL_SIX_LITERAL_TABLE_ROWS',
     'precision':PREC,'tiny_cutoff_proof':'positive rational exp(128) partial sum through k=400 exceeds 10^55',
     'total_exponential_arguments':len(all_exps),'author_clamped_arguments':len(clamped),
     'author_clamp_caution':'Not a universal bound on (-4000 log 10,-9200); every actual declared argument independently verified outside that interval.',
     'nearest_actual_author_clamped_argument':{'label':nearest[0],'interval':nearest[1].out()},'rows':rows}
(P/'INDEPENDENT_INTERVAL_SUMS.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status']);print('nearest author clamp',out['nearest_actual_author_clamped_argument'])
for r in rows:print(r['power'],r['total']['upper'], '<',r['author_table_bound'])
