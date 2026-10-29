"""Exact GF2 sampling, distance verification and phase-aware Clifford compiler."""
import numpy as np, random,json,subprocess,time,hashlib
from pathlib import Path
from itertools import combinations,product
from math import comb
from fractions import Fraction as F
from received_algebra_compiler_v1 import compile_algebra,unitary,pauli
ROOT=Path(__file__).parent

def rbasis(rows):
 b={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in b:v^=b[p]
   else:
    b[p]=v;break
 return b

def member(v,b):
 while v:
  p=v.bit_length()-1
  if p not in b:return False
  v^=b[p]
 return True

def nullspace(rows,width):
 # echelon constraints with highest pivot; assign each free bit, solve low pivots first
 b=rbasis(rows);free=[j for j in range(width) if j not in b];out=[]
 for j in free:
  v=1<<j
  for p in sorted(b):
   if (b[p]&v).bit_count()%2:v^=1<<p
  assert all((q&v).bit_count()%2==0 for q in rows)
  out.append(v)
 return out

def swap(v,n):return (v>>n)|((v&((1<<n)-1))<<n)
def sp(v,w,n):return (swap(v,n)&w).bit_count()%2

def isotropic(n,k,rng,cap=64):
 rows=[];attempts=0
 for j in range(n-k):
  ker=nullspace([swap(v,n) for v in rows],2*n);b=rbasis(rows)
  for _ in range(cap):
   attempts+=1;bits=rng.getrandbits(len(ker));v=0
   for a,w in enumerate(ker):
    if bits>>a&1:v^=w
   if not member(v,b):break
  else:raise RuntimeError('finite isotropic sampler exhausted')
  assert all(sp(v,w,n)==0 for w in rows)
  rows.append(v)
 return rows,attempts

def transform(v,phase,gates,n):
 mask=(1<<n)-1;x=v&mask;z=v>>n
 for g in gates:
  typ,*a=g
  if typ=='H':
   j=a[0];xx=(x>>j)&1;zz=(z>>j)&1;phase+=2*xx*zz
   if xx!=zz:x^=1<<j;z^=1<<j
  elif typ=='S':
   j=a[0];xx=(x>>j)&1;phase+=xx
   if xx:z^=1<<j
  elif typ=='CX':
   c,t=a
   if x>>c&1:x^=1<<t
   if z>>t&1:z^=1<<c
  elif typ=='SW':
   i,j=a
   if ((x>>i)^(x>>j))&1:x^=(1<<i)|(1<<j)
   if ((z>>i)^(z>>j))&1:z^=(1<<i)|(1<<j)
  else:raise ValueError(g)
 return x|(z<<n),phase%4

def array(rows,n):return np.array([[(v>>j)&1 for j in range(2*n)] for v in rows],dtype=np.uint8)
def low_errors(n,maximum):
 yield 0
 for w in range(1,maximum+1):
  for pos in combinations(range(n),w):
   for typ in product((1,2,3),repeat=w):
    v=0
    for j,p in zip(pos,typ):
     if p&1:v^=1<<j
     if p&2:v^=1<<(n+j)
    yield v

def syndrome(v,rows,n):return sum(sp(v,w,n)<<j for j,w in enumerate(rows))
def verify(rows,n,d):
 inp=[f'{n} {d}']
 for j in range(n):
  for p in (1,2,3):
   v=((p&1)<<j)|(((p>>1)&1)<<(n+j));s=syndrome(v,rows,n)
   inp.append(f'{s&((1<<64)-1)} {s>>64}')
 cp=subprocess.run([str(ROOT/'verify_low_weight')],input='\n'.join(inp),capture_output=True,text=True)
 count,failed=map(int,cp.stdout.split());return count,not failed

def build(n,k,d,rng):
 tries=0
 while True:
  tries+=1;rows,draws=isotropic(n,k,rng);count,ok=verify(rows,n,d)
  if ok:break
  if tries>=16:raise RuntimeError('code sampling cap exhausted')
 out=compile_algebra(array(rows,n),n);gates=out['gates'];assert out['a']==0 and out['b']==n-k and out['k']==k
 mapped=[transform(v,0,gates,n)[0] for v in rows];allowed=((1<<(n-k))-1)<<n
 assert all(v&~allowed==0 for v in mapped) and len(rbasis(mapped))==n-k
 table={};r=(d-1)//2;mask=(1<<n)-1
 for e in low_errors(n,r):
  v,phase=transform(e,(e&(e>>n)&mask).bit_count()%4,gates,n)
  sy=v&((1<<(n-k))-1);logical=((v&mask)>>(n-k))|((v>>(2*n-k))<<k)
  if sy in table:assert table[sy]['logical']==logical
  else:table[sy]={'logical':logical,'representative':hex(e),'transformed_phase':phase}
 # Every distinct pair of correctable errors has nonzero syndrome unless equal,
 # because verifier excludes ALL normalizer weights<d (stronger than necessary).
 expected=sum(comb(n,w)*3**w for w in range(r+1));assert len(table)==expected
 return dict(n=n,k=k,minimum_distance_verified=d,code_tries=tries,isotropic_draws=draws,
  checked_low_weight_paulis=count,expected_check_count=sum(comb(n,w)*3**w for w in range(1,d)),
  generators=[hex(x) for x in rows],decoder_gates=[list(g) for g in gates],
  gate_count=len(gates),gate_counts={typ:sum(g[0]==typ for g in gates) for typ in ('H','S','CX','SW')},
  correction_radius=r,syndrome_table={str(s):v for s,v in table.items()},
  canonical_span_verified=True,phase_convention='i^phase X^x Z^z; code is Udag(|0>^(n-k) tensor logical), generator signs induced by actual circuit')

def main():
 subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'verify_low_weight.cpp'),'-o',str(ROOT/'verify_low_weight')],check=True)
 rng=random.Random(2910290534);results=[]
 for h in [2,3,4,5]:
  start=time.time();out=build(16*h,h,h,rng);out['h']=h;out['elapsed_seconds']=time.time()-start
  assert out['checked_low_weight_paulis']==out['expected_check_count']
  (ROOT/f'inner_h{h}.json').write_text(json.dumps(out,indent=2)+'\n')
  results.append({k:v for k,v in out.items() if k not in ('generators','decoder_gates','syndrome_table')})
  print(json.dumps(results[-1]),flush=True)
 (ROOT/'construction_results.json').write_text(json.dumps({'seed':2910290534,'scope':'Exact binary instances; seeded pseudorandom execution is not a physical randomness source. The uniform sampler theorem uses ideal independent fair bits.','cases':results},indent=2)+'\n')
if __name__=='__main__':main()
