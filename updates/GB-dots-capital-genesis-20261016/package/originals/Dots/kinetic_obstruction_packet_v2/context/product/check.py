from fractions import Fraction as R
from decimal import Decimal, localcontext
from collections import defaultdict
import json
D=R('8.2207')
def B(n): return R('2.676')*n*(n-1)+R('108.102')
def A(n): return R('.040')*n*(n-1)*(n-2)+R('37.881')*n
edges=[(i,j) for i in range(8) for j in range(8) if abs(i//4-j//4)+abs(i%4-j%4)==1]
deg=[sum(i==x for x,y in edges) for i in range(8)]
assert len(edges)==20 and sorted(deg)==[2]*4+[3]*4
# Enumerate the actual eight-site generator on each sparse state independently.
# Product evaluation reduces to active factor w[k] since all other counts <=1.
for i in range(8):
 for m in range(16,163):
  n=[0]*8;n[i]=m
  coeff=defaultdict(R)
  def jump(dest,rate):
   coeff[m]-=rate
   if max(dest)<163: coeff[dest[i]]+=rate  # overflow has zero payoff
  for j in range(8):
   dest=n.copy();dest[j]+=1;jump(dest,B(n[j]))
   if n[j]:
    dest=n.copy();dest[j]-=1;jump(dest,A(n[j]))
  for src,dst in edges:
   if n[src]:
    dest=n.copy();dest[src]-=1;dest[dst]+=1;jump(dest,D*n[src])
  expected={m:-(B(m)+A(m)+deg[i]*D*m),m-1:A(m)+deg[i]*D*m}
  if m<162:expected[m+1]=B(m)
  assert {k:v for k,v in coeff.items() if v}==expected
out={'sparse_states_verified':8*147,'directed_edges':edges,'degrees':deg,'degrees_results':{}}
lower=[]
for d in (2,3):
 mu=lambda n:A(n)+d*D*n
 c=min(mu(n)-B(n) for n in range(16,163))
 # Harmonic overflow probabilities via positive slope ratios, then verify
 # EVERY exact generator equation and both boundary values independently.
 slopes={16:R(1)}
 for n in range(16,163): slopes[n+1]=mu(n)*slopes[n]/B(n)
 z=sum(slopes.values()); h={15:R(0)}
 for n in range(16,164):h[n]=h[n-1]+slopes[n]/z
 assert h[15]==0 and h[163]==1
 for n in range(16,163):
  assert B(n)*(h[n+1]-h[n])+mu(n)*(h[n-1]-h[n])==0
 assert 0<h[50]<R(1,10**20)
 ell=1-R(35)/c-R(1,10**20)
 assert 0<ell<1
 lower.append(ell)
 with localcontext() as ctx:
  ctx.prec=40
  dec=lambda r:str(Decimal(r.numerator)/Decimal(r.denominator))
  out['degrees_results'][d]={'drift_minimum_exact':str(c),'drift_minimum_at':[n for n in range(16,163) if mu(n)-B(n)==c],'overflow_descriptive':dec(h[50]),'conservative_deadline_lower_exact':str(ell),'conservative_deadline_lower_descriptive':dec(ell)}
p=lower[0]**4*lower[1]**4
assert p>R(26,100)
with localcontext() as ctx:
 ctx.prec=40
 out['conservative_product_lower_descriptive']=str(Decimal(p.numerator)/Decimal(p.denominator))
out['exact_assertion_passed']='conservative product lower > 26/100'
print(json.dumps(out,indent=2))
