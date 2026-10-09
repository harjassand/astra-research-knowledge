from pathlib import Path
import sys, json, time, random
from fractions import Fraction as F
BASE=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(BASE/'gaussian_transfer'))
from displaced_evaluator import log_H,asarb,ceil_sqrt
from flint import arb,ctx
random.seed(612195)
cases=[]
for b in [1,2,16,64,256,1024,2048,8192,32768]:
 n=(1<<b)+2
 for p in [1,40,257]:
  for quadratic in [False,True]:
   v=F(1)
   cases.append((n,v if quadratic else F(0),F(0) if quadratic else v,p,'large_n'))
for b in [1,16,64,256,1024,2048,8192]:
 for v in [F(1,1<<b),F(1<<b),F((1<<b)+1,1<<b),F((1<<b)-1,1<<b)]:
  n=(1<<b)+2
  for quadratic in [False,True]:
   cases.append((n,v if quadratic else F(0),F(0) if quadratic else v,40,'scale_extreme'))
for n in [0,1,2,3,4,(1<<2048)-1,(1<<2048)]:
 for a,c in [(F(0),F(0)),(F(0),F(1)),(F(1),F(0))]:
  cases.append((n,a,c,1,'zero_and_small'))
rows=[]
for n,a,c,p,kind in cases:
 start=time.perf_counter()
 try:
  y,m=log_H(n,a,c,p)
  dur=time.perf_counter()-start
  if y is None:
   ok=(n>0 and ((a==0 and c==0) or(c==0 and n%2==1)))
   rows.append(dict(kind=kind,n_bits=n.bit_length(),a_num_bits=a.numerator.bit_length(),a_den_bits=a.denominator.bit_length(),c_num_bits=c.numerator.bit_length(),c_den_bits=c.denominator.bit_length(),p=p,method=m['method'],zero_ok=bool(ok),seconds=dur,ok=bool(ok)))
   continue
  L=max(abs(v.numerator).bit_length()+v.denominator.bit_length() for v in (a,c))
  K=p+ceil_sqrt(2*(p+16))+16
  wp=p+2*L+2*n.bit_length()+4*K+100
  with ctx.workprec(wp+100):
   target=arb(2)**(-(p+1))
   width_ok=bool(2*y.rad()<=target)
   if n==0: ref=arb(0)
   elif a==0:ref=n*asarb(c).log()-arb(n+1).lgamma()
   else:ref=(n//2)*(asarb(a)/2).log()-arb(n//2+1).lgamma()
   finite=bool(y.is_finite())
   encloses=bool(y.contains(ref))
   rad_log2=None if y.rad().is_zero() else float(y.rad().log()/arb(2).log())
  rows.append(dict(kind=kind,n_bits=n.bit_length(),a_num_bits=a.numerator.bit_length(),a_den_bits=a.denominator.bit_length(),c_num_bits=c.numerator.bit_length(),c_den_bits=c.denominator.bit_length(),p=p,method=m['method'],finite=finite,width_ok=width_ok,encloses_higher_precision=encloses,radius_log2=rad_log2,working_bits=wp,seconds=dur,ok=bool(finite and width_ok and encloses)))
 except Exception as e:
  rows.append(dict(kind=kind,n_bits=n.bit_length(),p=p,error=repr(e),ok=False))
 print(json.dumps(rows[-1]),flush=True)
Path(__file__).with_name('degeneracy_results.json').write_text(json.dumps(dict(cases=len(rows),passed=sum(r['ok'] for r in rows),rows=rows),indent=2)+'\n')
print(json.dumps({'cases':len(rows),'passed':sum(r['ok'] for r in rows),'total_seconds':sum(r.get('seconds',0) for r in rows)}))
