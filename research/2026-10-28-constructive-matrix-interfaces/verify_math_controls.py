"""Independent exact intake controls; no imports from acquired scientific code."""
import json
from fractions import Fraction

def mul2(x,y,p):
 out=0
 for i in range(p):
  for j in range(2):
   out|=((((x>>(2*i))&1)*((y>>j)&1)) ^ (((x>>(2*i+1))&1)*((y>>(2+j))&1)))<<(2*i+j)
 return out

def rank2(y):
 rows=[y&3,y>>2];return int(any(rows))+int(rows[0]!=0 and rows[1]!=0 and rows[0]!=rows[1])

def product8(x,y):
 answer=0
 for i in range(8):
  row=(x>>(8*i))&255;value=0
  for k in range(8):
   if row&(1<<k):value^=(y>>(8*k))&255
  answer|=value<<(8*i)
 return answer

def diagonal(a,b):
 answer=0
 for shift,m in [(0,a),(2,a),(4,b),(6,b)]:
  for i in range(2):
   for j in range(2):
    if m&(1<<(2*i+j)):answer|=1<<(8*(i+shift)+j+shift)
 return answer

def controls():
 rows=[]
 for p in range(1,5):
  pairs=[(x,y)for x in range(1<<(2*p))for y in range(16)if mul2(x,y,p)==0]
  constrained=[(x,y)for x,y in pairs if ((y&1)^((y>>3)&1))]
  assert len(pairs)==(1<<(2*p))+9*(1<<p)+6
  assert len(constrained)==6*(1<<p)+2
  # Branch by complete binary Y prefixes using independent literal counts;
  # then choose X uniformly. Every leaf gets the same exact rational mass.
  for x,y in constrained:
   probability=Fraction(1);parent=len(constrained)
   for k in range(1,5):
    prefix=y&((1<<k)-1)
    child=sum(1 for _,w in constrained if w&((1<<k)-1)==prefix)
    probability*=Fraction(child,parent);parent=child
   probability/=sum(1 for _,w in constrained if w==y)
   assert probability==Fraction(1,len(constrained))
  rows.append(dict(p=p,full=len(pairs),trace_one=len(constrained),uniform_rational_leaves=len(constrained)))
 assert [sum(rank2(y)==r for y in range(16))for r in range(3)]==[1,9,6]
 E13=1<<2
 old={diagonal(a,b)for a in range(16)for b in range(16)}
 dual=old|{x^E13 for x in old}
 basis=[diagonal(1<<i,0)for i in range(4)]+[diagonal(0,1<<i)for i in range(4)]+[E13]
 # I belongs to D', so any multiplier must itself lie in these512 candidates.
 multipliers={x for x in dual if all(product8(x,d)in dual for d in basis)}
 expected={diagonal(a,b)for a in range(16)for b in range(16)if not a&4}
 assert multipliers==expected and len(multipliers)==128
 radical=diagonal(2,0)
 assert radical and radical in multipliers and product8(radical,radical)==0
 assert all(product8(radical,t)in (0,radical)and product8(t,radical)in (0,radical)for t in multipliers)
 return dict(scope='Independent finite binary controls only; not a producer replay,native acquisition,full algorithm audit or performance experiment.',rejection_and_uniformity=rows,rank_counts=[1,9,6],conditioned_dual_candidates=len(dual),exact_left_multipliers=len(multipliers),nonzero_square_zero_two_sided_radical=True)

if __name__=='__main__':print(json.dumps(controls(),indent=2))
