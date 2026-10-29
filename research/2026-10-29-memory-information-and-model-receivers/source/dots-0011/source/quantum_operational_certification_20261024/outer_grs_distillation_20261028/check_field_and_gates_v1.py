#!/usr/bin/env python3
"""Deterministic small-field construction and elementary binary gate compiler."""
from pathlib import Path
import json,itertools,random
from grs_wrapper_v1 import GF,construct,field_linear_gates,apply_gates
HERE=Path(__file__).parent

def rem(a,b):
 while a and a.bit_length()>=b.bit_length():a^=b<<(a.bit_length()-b.bit_length())
 return a
def gcd(a,b):
 while b:a,b=b,rem(a,b)
 return a
def irreducible(m,f):
 if f.bit_length()!=m+1 or not f&1:return False
 g=GF(m,f);x=rem(2,f);z=x
 for i in range(1,m+1):
  z=g.mul(z,z)
  if i<=m//2 and gcd(z^x,f)!=1:return False
 return z==x
def first_field(m):
 tested=0
 for f in range((1<<m)|1,1<<(m+1),2):
  tested+=1
  if irreducible(m,f):return f,tested
 raise AssertionError('finite field does not exist')
def binary_linear(g,A):
 # Compiles a field-linear map into actual qubit CNOT and SWAP operations.
 m=g.m;ops=[];g2=GF(1,3)
 for kind,i,j,a in field_linear_gates(g,A):
  if kind=='swap':
   ops.extend([('SWAP',i*m+b,j*m+b) for b in range(m)])
  elif kind=='add':
   for b in range(m):
    prod=g.mul(a,1<<b)
    ops.extend([('CX',i*m+b,j*m+c) for c in range(m) if (prod>>c)&1])
  else:
   M=[[(g.mul(a,1<<b)>>c)&1 for c in range(m)] for b in range(m)]
   for kk,ii,jj,aa in field_linear_gates(g2,M):
    assert kk in ['swap','add']
    ops.append(('SWAP' if kk=='swap' else 'CX',i*m+ii,i*m+jj))
 return ops
def apply_binary(bits,ops):
 bits=bits[:]
 for op,i,j in ops:
  if op=='SWAP':bits[i],bits[j]=bits[j],bits[i]
  else:bits[j]^=bits[i]
 return bits
def fieldvec(bits,m):return [sum(bits[i*m+b]<<b for b in range(m)) for i in range(len(bits)//m)]
def main():
 fields=[]
 for m in range(1,11):
  f,tested=first_field(m);fields.append({'h':m,'polynomial_bits':bin(f),'candidates_tested':tested,'q':1<<m});assert tested<=1<<(m-1)
 rng=random.Random(202610282347);cases=[]
 for m,B,t in [(3,5,1),(3,7,1),(4,9,2),(4,13,3)]:
  f,_=first_field(m);g=GF(m,f);c=construct(g,B,t)
  enc=binary_linear(g,c['T']);dec=binary_linear(g,c['Ti'])
  for j in range(B*m):
   bits=[int(i==j) for i in range(B*m)];x=fieldvec(bits,m)
   assert fieldvec(apply_binary(bits,enc),m)==g.rowmul(x,c['T'])
   assert apply_binary(apply_binary(bits,enc),dec)==bits
  # Trace-Fourier convention: H^m followed by the inverse trace-Gram map.
  gram=[[g.trace(g.mul(1<<i,1<<j)) for j in range(m)] for i in range(m)];g2=GF(1,3);K=g2.inverse(gram)
  fourier_binary=field_linear_gates(g2,K)
  for x,y in itertools.product(range(g.q),repeat=2):
   xb=[(x>>i)&1 for i in range(m)];yb=[(y>>i)&1 for i in range(m)]
   # Pre-permutation Hadamard output z = y K^{-1} = y gram.
   z=g2.rowmul(yb,gram);phase=sum(a*b for a,b in zip(xb,z))%2
   assert phase==g.trace(g.mul(x,y))
  # Joint stripe guarantee: arbitrary correlations inside each bad inner block.
  stripe_patterns=0
  for _ in range(250):
   from grs_wrapper_v1 import one_way_correction
   bad=rng.sample(range(B),rng.randrange(t+1))
   for stripe in range(5):
    e=[0]*B;z=[0]*B
    for p in bad:e[p]=rng.randrange(g.q);z[p]=rng.randrange(g.q)
    a,b,ok=one_way_correction(g,c,e,z);assert ok and not any(a) and not any(b);stripe_patterns+=1
  cases.append({'h':m,'B':B,'t':t,'binary_encoder_linear_gates':enc,'binary_decoder_linear_gates':dec,'binary_encoder_linear_gate_count':len(enc),'binary_decoder_linear_gate_count':len(dec),'trace_Gram':gram,'trace_Fourier_after_H_linear_gates':fourier_binary,'Hadamards_per_Fourier':m,'joint_stripe_pattern_checks':stripe_patterns})
 out={'status':'PASS_DETERMINISTIC_FIELD_AND_ELEMENTARY_BINARY_CLIFFORD_CHECKS','fields':fields,'cases':cases,'scope':'Exact Boolean/finite-field gate action and Pauli propagation, no noisy hardware.'}
 (HERE/'field_and_gate_checks_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'fields':fields,'cases':[{k:v for k,v in c.items() if not isinstance(v,list)} for c in cases]},indent=2))
if __name__=='__main__':main()
