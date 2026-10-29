#!/usr/bin/env python3
"""Exact conventional correlated-block certification; no source samples."""
import math,json,hashlib,itertools
from fractions import Fraction
from pathlib import Path
D=Path(__file__).resolve().parent

def bad_accept(n,m,t,c):
 N=n+m; vals=[]
 for w in range(t+1,N+1):
  p=Fraction()
  for h in range(max(0,w-n),min(m,w-t-1)+1):
   sf=sum(math.comb(h,j)*2**j for j in range(min(c,h)+1))
   p+=Fraction(math.comb(m,h)*math.comb(n,w-h)*sf,math.comb(N,w)*3**h)
  vals.append((p,w))
 return max(vals)

def pauli(s):
 x=z=0
 for i,a in enumerate(s):
  if a in 'XY': x|=1<<i
  if a in 'ZY': z|=1<<i
 return x,z

def sym(a,b): return ((a[0]&b[1]).bit_count()+(a[1]&b[0]).bit_count())%2
G=[pauli(s) for s in ['XZZXI','IXZZX','XIXZZ','ZXIXZ']]
LX=pauli('XXXXX');LZ=pauli('ZZZZZ')
normal=[]
for s in itertools.product('IXYZ',repeat=5):
 e=pauli(''.join(s));w=(e[0]|e[1]).bit_count()
 if not any(sym(e,g) for g in G) and (sym(e,LX) or sym(e,LZ)):normal.append(w)
assert min(normal)==3
# Concatenated 25-qubit stabilizers; outer X/Z become inner logical X/Z.
CG=[]
for b in range(5):
 for x,z in G: CG.append((x<<(5*b),z<<(5*b)))
for x,z in G:
 xx=zz=0
 for b in range(5):
  if x>>b&1: xx|=31<<(5*b)
  if z>>b&1: zz|=31<<(5*b)
 CG.append((xx,zz))
assert all(sym(a,b)==0 for a in CG for b in CG)
# binary rank of symplectic rows
rows=[x|(z<<25) for x,z in CG];rank=0
for bit in range(50):
 p=next((j for j in range(rank,len(rows)) if rows[j]>>bit&1),None)
 if p is not None:
  rows[rank],rows[p]=rows[p],rows[rank]
  for j in range(len(rows)):
   if j!=rank and rows[j]>>bit&1:rows[j]^=rows[rank]
  rank+=1
assert rank==24
out={'status':'exact analytic fixture, not hardware or sampled acquisition','n':25,'t':4,'inner_distance':min(normal),'concatenated_stabilizer_rank':rank,'generator_weights':[(x|z).bit_count() for x,z in CG],'syndrome_candidates_up_to_weight4':sum(math.comb(25,j)*3**j for j in range(5)),'rows':[]}
for m in [25,50,100,200,500]:
 p,w=bad_accept(25,m,4,0)
 out['rows'].append({'m':m,'max_bad_accept_num':p.numerator,'max_bad_accept_den':p.denominator,'max_bad_accept_float':float(p),'maximizing_total_weight':w})
p=Fraction(1,100);m=100
out['honest_iid_diagnostic']={'physical_pauli_rate':str(p),'accept_probability':float((1-Fraction(2,3)*p)**m),'remaining_weight_gt4':float(sum(Fraction(math.comb(25,j))*p**j*(1-p)**(25-j) for j in range(5,26))),'assumption':'iid only for this yield diagnostic, not soundness'}
out['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(D/'exact_block_test_v1.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
