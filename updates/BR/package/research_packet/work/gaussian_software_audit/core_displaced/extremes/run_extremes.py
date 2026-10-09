import sys,time,json
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path('work/gaussian_transfer').resolve()))
from displaced_evaluator import log_H,asarb
from flint import arb,ctx
out=Path('work/gaussian_software_audit/core_displaced/extremes')
rows=[]
cases=[]
for b in [64,256,1024,4096]:
 for kind,a,c in [('unit',F(1),F(1)),('tiny_a',F(1,2**b),F(1)),('tiny_c',F(1),F(1,2**b)),('huge_a',F(2**b),F(1)),('huge_c',F(1),F(2**b)),('mixed',F(1,2**b+1),F(2**b+1,3)),('both_tiny',F(1,2**b),F(1,2**b)),('both_huge',F(2**b),F(2**b))]:
  for odd in [0,1]: cases.append((kind,b,2**b+odd,a,c,20,False))
# Low-degree integral with extreme large displacement; exact rational coefficients.
for b in [64,256,1024,4096]:
 for n in [1,2,3,7]:cases.append(('forced_extreme',b,n,F(1,2**b),F(2**b),20,True))
# Very tiny odd bmode compared with all ordinary precisions.
for b in [256,1024,4096]:
 cases.append(('tiny_parity',b,2**64+1,F(1),F(1,2**b),40,False))
# Larger requested precisions.
for p in [1,2,100,256]:cases.append(('precision',256,2**256+1,F(1,2**256),F(1,2**256),p,False))
for kind,b,n,a,c,p,force in cases:
 row={'kind':kind,'b':b,'n_bits':n.bit_length(),'n_small':n if n<10 else None,'p':p,'force':force}
 start=time.perf_counter()
 try:
  value,meta=log_H(n,a,c,p,force_integral=force)
  with ctx.workprec(meta.get('working_bits',max(100,p*2))+100):
   row.update(method=meta['method'],working_bits=meta.get('working_bits'),finite=value.is_finite(),radius_ok=bool(value.rad()<=arb(2)**(-p-1)),width_ok=bool(2*value.rad()<=arb(2)**(-p-1)),radius=str(value.rad()),mid=str(value.mid()))
   if n<=7:
    import math
    exact=sum((F(1,math.factorial(q)*math.factorial(n-2*q))*(a/2)**q*c**(n-2*q) for q in range(n//2+1)),F(0))
    truth=asarb(exact).log()
    row['exact_overlap']=value.overlaps(truth)
   # Positive coefficient limiting bounds: H>=term q=floor(n/2); H<=leading*exp(n*c^2/(2*a)).
   if kind in ['tiny_c','huge_a','tiny_parity']:
    k=n//2
    lo=k*(asarb(a)/2).log()-arb(k+1).lgamma()+(asarb(c).log() if n%2 else 0)
    hi=lo+asarb(F(n)*c*c/(2*a))
    row['limiting_bounds_overlap']=bool(value.upper()>=lo.lower() and value.lower()<=hi.upper())
 except Exception as exc:row['exception']=repr(exc)
 row['seconds']=time.perf_counter()-start
 rows.append(row)
 out.joinpath('results.json').write_text(json.dumps(rows,indent=2))
 print(json.dumps({k:v for k,v in row.items() if k not in ['mid','radius']}),flush=True)
print('DONE',len(rows))
