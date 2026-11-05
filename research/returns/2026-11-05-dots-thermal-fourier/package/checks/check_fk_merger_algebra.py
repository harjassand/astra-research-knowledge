#!/usr/bin/env python3
"""Finite algebra audits, not a replacement for the infinite-volume proof."""
from fractions import Fraction as F
from itertools import product
from math import tanh
import json
from pathlib import Path

E=[(0,1),(0,2),(1,3),(2,3)]
HE=E+[(a+4,b+4) for a,b in E]
P=[(frozenset([0,1]),0,F(1,7)),(frozenset([1,3]),1,F(1,11)),
   (frozenset([2,3]),2,F(1,13)),(frozenset(range(4)),0,F(1,17))]
compatible=[]
for mask in range(1<<len(P)):
 seen=set(); ok=True; w=F(1)
 for i,(support,anchor,activity) in enumerate(P):
  if mask>>i&1:
   if seen&support: ok=False;break
   seen|=support;w*=activity
 if ok: compatible.append((mask,w))
def clusters(bits,mask):
 par=list(range(8))
 def root(x):
  while par[x]!=x:x=par[x]
  return x
 def union(a,b):par[root(a)]=root(b)
 for i,(a,b) in enumerate(HE):
  if bits>>i&1:union(a,b)
 for i,(_,a,_) in enumerate(P):
  if mask>>i&1:union(a,a+4)
 return len({root(x) for x in range(8)})
def weight(bits,mask):return F(3**bits.bit_count()*2**clusters(bits,mask))
zfk=F(0); horizontal_checks=0; polymer_checks=0
for mask,w in compatible:
 for bits in range(1<<len(HE)):
  zfk+=w*weight(bits,mask)
  for e in range(len(HE)):
   if bits>>e&1:continue
   conditional=weight(bits|1<<e,mask)/(weight(bits,mask)+weight(bits|1<<e,mask))
   assert conditional in [F(3,5),F(3,4)]
   horizontal_checks+=1
  for i,(_,_,a) in enumerate(P):
   if mask>>i&1 or not any(m==(mask|1<<i) for m,_ in compatible):continue
   ratio=a*weight(bits,mask|1<<i)/weight(bits,mask)
   assert ratio in [a/2,a]
   polymer_checks+=1
zspin=F(0)
for spin in product([-1,1],repeat=8):
 base=1
 for a,b in HE:base*=1+3*(spin[a]==spin[b])
 for mask,w in compatible:
  if all(not(mask>>i&1) or spin[a]==spin[a+4] for i,(_,a,_) in enumerate(P)):
   zspin+=base*w
assert zfk==zspin

# Exact component-swap invariance on a 2x3 square grid.
n=6
edges=[(0,1),(1,2),(3,4),(4,5),(0,3),(1,4),(2,5)]
swaps=0
for spin in product([-1,1],repeat=12):
 s=list(spin[:6]);r=list(spin[6:]);D={x for x in range(6) if s[x]!=r[x]}
 energy=sum(s[a]*s[b]+r[a]*r[b] for a,b in edges)
 remaining=set(D)
 while remaining:
  comp={remaining.pop()};stack=list(comp)
  while stack:
   a=stack.pop()
   for e in edges:
    if a in e:
     b=e[0] if e[1]==a else e[1]
     if b in remaining:remaining.remove(b);comp.add(b);stack.append(b)
  ss=s[:];rr=r[:]
  for x in comp:ss[x],rr[x]=rr[x],ss[x]
  assert energy==sum(ss[a]*ss[b]+rr[a]*rr[b] for a,b in edges)
  assert all((ss[x]==rr[x])==(s[x]==r[x]) for x in range(6))
  swaps+=1
q=tanh(3)**2;alpha=3*(1-q)
assert q>.99 and alpha<.03
bounds={}
for R in [1,2,5,10,20,100]:
 k=max(4,2*R)
 bounds[str(R)]=4*alpha**k*(k/(1-alpha)+alpha/(1-alpha)**2)
assert all(bounds[str(R)]<1 for R in [1,2,5,10,20,100])
report={"finite_partition_functions_equal":True,"partition_function":str(zfk),
        "compatible_polymer_families":len(compatible),"horizontal_conditional_checks":horizontal_checks,
        "polymer_insertion_ratio_checks":polymer_checks,"component_swap_checks":swaps,
        "J_convention":"Boltzmann exponent J(ss+rr), equivalent mismatch cost 2J",
        "J":3,"common_iid_q":q,"contour_alpha":alpha,"pair_hole_tail_bounds":bounds,
        "all_TI_scope":"Uses the independently reviewed canonical-lift equilibrium/recoloring theorem; finite tests audit local algebra only, not the infinite-volume proof.",
        "mixed_color_warning":"An edge joining fixed opposite boundary colors has conditional opening probability zero; ordinary FK bounds cannot simply be asserted for arbitrary Gibbs states."}
Path(__file__).with_name('fk_merger_algebra_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
