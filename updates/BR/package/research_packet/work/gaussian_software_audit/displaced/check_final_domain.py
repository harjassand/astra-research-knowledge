from pathlib import Path
import sys,json,hashlib
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2]/'gaussian_transfer';sys.path.insert(0,str(ROOT))
from displaced_evaluator import log_H,ceil_sqrt
from flint import arb,ctx
out=[]
for p,a in [(1,F(1)),(20,F(1)),(20,F(4)),(100,F(1))]:
 n=1;R=ceil_sqrt(2*(p+16));M=4*(R+1)
 sqrta=1 if a==1 else 2
 center=F(sqrta*(M*M-n),M);tiny=F(1,10**80)
 for label,offset in [('below',-tiny),('equal',F(0)),('above',tiny)]:
  c=center+offset
  try:
   value,meta=log_H(n,a,c,p,force_integral=True)
   assert label!='below','below-domain integral accepted'
   with ctx.workprec(1600):
    exact=(arb(c.numerator)/arb(c.denominator)).log()
    assert value.contains(exact)
    assert value.rad()<=arb(2)**(-p-2)
   out.append({'p':p,'a':str(a),'case':label,'accepted':True,'method':meta['method']})
  except ValueError:
   assert label=='below','admissible integral rejected'
   out.append({'p':p,'a':str(a),'case':label,'accepted':False})
result={'evaluator_sha256':hashlib.sha256((ROOT/'displaced_evaluator.py').read_bytes()).hexdigest(),'checks':out,'total_cases':len(out)}
(Path(__file__).resolve().parent/'final_domain_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
