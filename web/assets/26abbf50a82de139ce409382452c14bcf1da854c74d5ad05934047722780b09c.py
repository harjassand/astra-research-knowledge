"""Acquire exact polynomial-size real-flat canonical POVM.
Outputs trace-dual finite-field labels for the Walsh embedding. This uses
integer arithmetic only; exact four-wise moment checks certify the frame.
No hardware circuit or floating point certification is claimed.
"""
from pathlib import Path
import itertools,json

def pmod(a,b):
 while a.bit_length()>=b.bit_length(): a^=b<<(a.bit_length()-b.bit_length())
 return a

def gcd(a,b):
 while b:a,b=b,pmod(a,b)
 return a

def mul(a,b,p,t):
 v=0
 while b:
  if b&1:v^=a
  b>>=1;a<<=1
  if a&(1<<t):a^=p
 return v

def irreducible(p,t):
 x=2;y=x
 for j in range(1,t+1):
  y=mul(y,y,p,t)
  if j<=t//2 and gcd(y^x,p)!=1:return False
 return y==x

def field(d):
 t=(d+1).bit_length()-1
 if (1<<t)<d+1:t+=1
 for p in range((1<<t)|1,1<<(t+1),2):
  if irreducible(p,t):return t,p
 raise RuntimeError('irreducible polynomial not found')

def trace(a,p,t):
 b=a;v=0
 for j in range(t):v^=b;b=mul(b,b,p,t)
 assert v in [0,1]
 return v

def acquire(d):
 t,p=field(d);q=1<<t;labels=[]
 for x in range(1,d+1):
  x3=mul(mul(x,x,p,t),x,p,t)
  a=sum(trace(mul(1<<j,x,p,t),p,t)<<j for j in range(t))
  b=sum(trace(mul(1<<j,x3,p,t),p,t)<<j for j in range(t))
  labels.append(a|(b<<t))
 assert len(set(labels))==d
 cnt=0
 for k in range(1,min(4,d)+1):
  for subset in itertools.combinations(labels,k):
   z=0
   for x in subset:z^=x
   assert z!=0
   cnt+=1
 # Sum_s s_i s_j = q^2 delta_ij exactly: character orthogonality.
 # Full signs are s(seed,i)=(-1)^popcount(seed & labels[i]).
 # Row W_seed,i=s(seed,i)/q. M_seed=|s><s|/q^2.
 return {'d':d,'field_degree':t,'irreducible_polynomial_bits':p,'q':q,'POVM_outcomes':q*q,'outcome_bits':2*t,'walsh_labels':labels,'distinct_subset_moment_checks':cnt,'mean_and_fourth_moments':'EXACT_BY_CHARACTER_ORTHOGONALITY','effect_entries':'s_i s_j / q^2','prepared_projector_entries':'s_i s_j / d'}
if __name__=='__main__':
 rows=[acquire(d)for d in [2,3,4,5,8,12,16]]
 Path(__file__).with_suffix('.json').write_text(json.dumps({'frames':rows,'scope':'implemented finite-field labels, exact moment tests, finite POVM; no gate compiler/hardware run'},indent=2)+'\n')
 print(json.dumps({'d_values':[r['d']for r in rows],'outcome_counts':[r['POVM_outcomes']for r in rows],'all_integer_checks_passed':True}))
