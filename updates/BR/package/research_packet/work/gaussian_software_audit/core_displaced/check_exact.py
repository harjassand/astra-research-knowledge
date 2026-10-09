from pathlib import Path
import sys,time,json,hashlib,math
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'gaussian_transfer'))
SOURCE_PATH=Path(__file__).resolve().parents[2]/'gaussian_transfer/displaced_evaluator.py'
SOURCE_BYTES=SOURCE_PATH.read_bytes()
SOURCE_SHA256=hashlib.sha256(SOURCE_BYTES).hexdigest()
from displaced_evaluator import log_H
from flint import arb,ctx

def coeff(n,a,c):
 # Independent exact scaled Gaussian moment recurrence: avoids repeated
 # rational GCDs, so large denominator cases remain practical.
 if n==0:return F(1)
 Q=math.lcm(a.denominator,c.denominator)
 A=a.numerator*(Q*Q//a.denominator)
 C=c.numerator*(Q//c.denominator)
 prev,cur=1,C
 for k in range(2,n+1):prev,cur=cur,C*cur+(k-1)*A*prev
 return F(cur,Q**n*math.factorial(n))

cases=[]
# Finite sums, degeneracies, even/odd, and a wide exact rational scale grid.
for n in [0,1,2,3,4,15,50,101]:
 for a,c in [(F(0),F(0)),(F(0),F(3,7)),(F(2,3),F(0)),(F(1),F(1)),(F(3,7),F(5,13)),(F(1),F(1,10**30)),(F(1,10**30),F(1)),(F(10**30),F(1,10**30))]:
  cases.append((n,a,c,40,False))
# force_integral takes n small but d large; this valid branch has exact coefficients.
for n in [1,2,3,15,100]:
 for a,c in [(F(1),F(64)),(F(1,10**20),F(1)),(F(10**20),F(10**20))]:
  cases.append((n,a,c,40,True))
# Natural integral branch around its cutoff; include odd tiny displacement.
for n in [2304,2305,2500,2501]:
 for a,c in [(F(1),F(1)),(F(1),F(1,10**30)),(F(2,7),F(5,11))]:
  cases.append((n,a,c,40,False))
# Degree/working-precision stress; enforce large saddle to admit branch.
for p in [1,10,100,200]:
 for n in [1,3]:cases.append((n,F(1),F(200),p,True))

rows=[]; failures=[]
for idx,(n,a,c,p,force) in enumerate(cases):
 start=time.perf_counter(); exact=coeff(n,a,c)
 try:
  answer,meta=log_H(n,a,c,p,force_integral=force)
  with ctx.workprec(max(1024,p+256)):
   if exact==0:
    contains=answer is None and meta['zero'];widthok=True;finite=True;rad='zero'
   else:
    reference=(arb(exact.numerator)/arb(exact.denominator)).log()
    contains=answer is not None and answer.contains(reference)
    finite=answer is not None and answer.is_finite()
    widthok=answer is not None and 2*answer.rad()<=arb(2)**(-p-1)
    rad=str(answer.rad()) if answer is not None else 'none'
  row={'n':n,'a':str(a),'c':str(c),'p':p,'force_integral':force,'method':meta['method'],'finite':finite,'contains_reference':contains,'width_ok':widthok,'radius':rad,'seconds':time.perf_counter()-start}
 except Exception as e:
  row={'n':n,'a':str(a),'c':str(c),'p':p,'force_integral':force,'exception':repr(e),'seconds':time.perf_counter()-start}
  failures.append(row)
 else:
  if not (contains and finite and widthok):failures.append(row)
 rows.append(row)
 if idx%10==0:print('completed',idx+1,'/',len(cases),'failures',len(failures),flush=True)
output={'source_sha256':SOURCE_SHA256,'checks':len(rows),'failures':failures,'cases':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'checks':len(rows),'failures':failures},indent=2))
