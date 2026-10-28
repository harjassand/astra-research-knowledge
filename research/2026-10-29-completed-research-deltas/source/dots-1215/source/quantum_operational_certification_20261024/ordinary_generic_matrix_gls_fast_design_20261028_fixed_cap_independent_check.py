#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import random,hashlib,json
random.seed(281154)
def ceilq(x):return -(-x.numerator//x.denominator)
def clog2(x):
 assert x>0
 n=x.numerator;d=x.denominator
 k=n.bit_length()-d.bit_length()
 if k>=0:
  if n>d*(1<<k):k+=1
 else:
  if n*(1<<(-k))>d:k+=1
 return k
cases=0;max_sumratio=F(0);max_qratio=F(0)
for k,R in [(1,1),(2,1),(3,3),(5,2),(8,4)]:
 d=2*k;r=min(d,3*R);D=10*d*d;L=8*D;Dp=d*r;Dplus=1<<clog2(F(Dp))
 for j in [1,7,19,37]:
  eta=F(1,2**j);n=ceilq(F(2**24*D*L)/eta);fl=ceilq(2+F(r)/eta);mb=n+fl+1
  z=min(eta/(10**6*D*n),F(1,mb*mb));Sz=10+ceilq(D*F(clog2(F(4)/eta/F(1,2**20)) ))+1
  Lz=2+clog2(1/z);lb=mb+Lz;bb=z/(1000*lb*lb*Dp*Dp*mb*mb)
  n0bar=320*Dplus*clog2(12*Dplus/bb)+1
  for ss in [1,3,17]:
   S=min(ss,Sz);ints=[random.randrange(1,1000) for _ in range(S)];tot=sum(ints);pi=[F(v,tot) for v in ints]
   mi=[ceilq(n*x)+fl for x in pi]
   assert max(mi)<=mb and sum(mi)<=n+Sz*(fl+1)
   raw=0
   for mm in mi:
    assert z<=F(1,mm*mm)
    li=max(mm,(clog2(4/z)+1)//2)
    bi=z/(1000*li*li*Dp*Dp*mm*mm)
    assert li<=mm+Lz<=lb and bi>=bb
    # Outward base-two logarithm caps, permitted by the companion.
    n0i=320*Dplus*clog2(12*Dplus/bi)
    assert n0i<=n0bar
    qi=n0i+mm+li;assert qi<=n0bar+2*mm+Lz
    max_qratio=max(max_qratio,F(qi,n0bar+2*mm+Lz));raw+=qi
   bound=2*n+Sz*(2*(fl+1)+n0bar+Lz)
   assert raw<=bound;max_sumratio=max(max_sumratio,F(raw,bound));cases+=1
p=Path(__file__).resolve().parent/'ordinary_generic_matrix_gls_fast_design_20261028_fixed_cap.md'
out={'status':'PASS_INDEPENDENT_PREDETERMINED_RAW_CAP','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exact_rational_schedule_cases':cases,'largest_actual_over_per_query_cap':float(max_qratio),'largest_actual_over_whole_support_cap':float(max_sumratio),'scope':'Exact rational ceilings, dyadic logarithm upper bounds, local zeta restrictions and raw-source ledgers; no local query or hardware execution.'}
p.with_name(p.stem+'_independent_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
