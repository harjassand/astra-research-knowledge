from itertools import product
from random import Random
from fractions import Fraction
rng=Random(20261101)
checks=0
for trial in range(200):
 n=5; gates=[]
 for j in range(7):
  ins=tuple(sorted(rng.sample(range(n+j),2)))
  truth=[0]+[rng.randrange(2) for _ in range(3)]
  gates.append((ins,truth))
 reject=(n+5,n+6)
 def run(mask):
  val=[(mask>>i)&1 for i in range(n)];objects={}
  for i in range(n):
   if val[i]:objects[('i',i)]=(frozenset([i]),(1,))
  for j,(ins,truth) in enumerate(gates):
   out=truth[2*val[ins[0]]+val[ins[1]]];val.append(out)
   if any(val[k] for k in ins):objects[('g',j)]=(frozenset((*ins,n+j)),tuple(val[k] for k in (*ins,n+j)))
  unseen=set(objects);components=[]
  while unseen:
   seed=unseen.pop();todo=[seed];comp={seed}
   while todo:
    a=todo.pop()
    new={b for b in unseen if objects[a][0]&objects[b][0]}
    unseen-=new;comp|=new;todo+=list(new)
   components.append(frozenset((a,objects[a]) for a in comp))
  return not any(val[k] for k in reject),components
 polys={}; valid={}
 for mask in range(1<<n):
  ok,cs=run(mask)
  if not ok:continue
  valid[mask]=cs
  for c in cs:
   inp=sum(1<<a[1] for a,_ in c if a[0]=='i')
   ok2,cs2=run(inp)
   assert ok2 and cs2==[c]
   st=frozenset().union(*(obj[0] for _,obj in c))
   polys[c]=(inp,st)
 P=list(polys);seen={};gas=Fraction(0);q=Fraction(1,7)
 def enumerate_families(j,mask,st,chosen):
  global gas
  if j==len(P):
   ok,cs=run(mask);assert ok and set(cs)==set(chosen)
   assert mask not in seen
   seen[mask]=tuple(chosen);gas+=q**mask.bit_count();return
  enumerate_families(j+1,mask,st,chosen)
  inp,s=polys[P[j]]
  if not st&s:
   assert not mask&inp
   enumerate_families(j+1,mask|inp,st|s,chosen+[P[j]])
 enumerate_families(0,0,frozenset(),[])
 assert set(seen)==set(valid)
 assert gas==sum((q**m.bit_count() for m in valid),Fraction(0))
 checks+=len(valid)
print('PASS: 200 zero-preserving DAGs; all32 inputs; exact split/recombination/uniqueness/partition;',checks,'accepting executions')
