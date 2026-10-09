import sys,json
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path('work/gaussian_transfer').resolve()))
from displaced_evaluator import log_H,asarb,ceil_sqrt
from flint import arb,ctx
out=Path('work/gaussian_software_audit/core_displaced/extremes')
rows=[]
# Entire rigorous limiting interval must be contained in returned interval.
# Parity dominant term: q=floor(n/2), log ratio <= n*c^2/(2*a).
# Linear dominant term: q=0, log ratio <= a*n^2/(2*c^2).
for b in [64,256,1024,4096]:
 for parity in [0,1]:
  n=2**b+parity
  for mode,a,c in [('parity',F(1),F(1,2**b)),('linear',F(1,2**b),F(2**b))]:
   ans,meta=log_H(n,a,c,20)
   with ctx.workprec(meta['working_bits']+100):
    if mode=='parity':
     k=n//2
     lo=k*(asarb(a)/2).log()-arb(k+1).lgamma()+(asarb(c).log() if n%2 else 0)
     hi=lo+asarb(F(n)*c*c/(2*a))
    else:
     lo=n*asarb(c).log()-arb(n+1).lgamma()
     hi=lo+asarb(a*n*n/(2*c*c))
    rows.append(dict(mode=mode,b=b,parity=parity,contains_full_rigorous_limiting_interval=bool(ans.lower()<=lo.lower() and ans.upper()>=hi.upper())))
# Force-integral guard at exact m=4(R+1), and ordinary out-of-domain force.
for p in [1,2,20,40,100]:
 M=4*(ceil_sqrt(2*(p+16))+1)
 for n in [1,2,7,M*M-1]:
  c=F(M)-F(n,M)
  row=dict(mode='boundary_guard',p=p,n=n,a='1',c=str(c),exact_m=M,exactly_in_domain=True)
  try:
   v,meta=log_H(n,1,c,p,force_integral=True)
   row['result']=meta['method']
  except ValueError as e:row['result']=str(e)
  rows.append(row)
try:log_H(1,1,1,20,force_integral=True)
except ValueError as e:rows.append(dict(mode='out_of_domain_guard',p=20,n=1,a='1',c='1',result=str(e),exactly_in_domain=False))
out.joinpath('limiting_and_boundary_results.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
