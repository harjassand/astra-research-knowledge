from fractions import Fraction as F
import math,json
from pathlib import Path
rows=[]
for h,d,e in [(4,2,F(1,8)),(6,3,F(1,16)),(20,5,F(1,100))]:
 tau=e*e/(4*h);M=(d+1)**2;mu=tau/M;m=0
 while F(1,2**m)>e/(4*h*(d+1)):m+=1
 j=0
 while 2**j<F(m)/mu:j+=1
 L=12/mu**2;eta=e/(8*h*(d+1)*j*L**j)
 bits=0
 while F(1,2**bits)>eta:bits+=1
 # Scalar endpoint/near-endpoint cases; round every iteration to fixed dyadic precision.
 for a in [mu,2*mu,F(1,2),F(1)]:
  x=F(1)
  for it in range(j):
   y=(3*x-a*x**3)/2
   x=F((y.numerator*2**bits)//y.denominator,2**bits)
  residual=abs(1-a*x*x)
  # No exact square root is needed: residual bounds root error on a<=1.
  target=e/(4*h*(d+1))+e/(8*h*(d+1))*2 # conservative diagnostic endpoint allowance
  assert residual<target
  rows.append(dict(h=h,d=d,e=str(e),a=str(a),iterations=j,dyadic_bits=bits,residual_float=float(residual)))
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(rows=rows,scope='Exact-rational scalar rounded Newton endpoint diagnostics, not generic matrix compiler execution'),indent=2)+'\n');print('passed',len(rows))
