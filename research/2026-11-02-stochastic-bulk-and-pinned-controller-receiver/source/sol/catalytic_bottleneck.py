#!/usr/bin/env python3
"""A general binary weakly-reversible single-port bottleneck discriminator.

All rates are 1. Enzyme phases C_0,...,C_m have one copy in total.
B+C_j <-> C_{j+1}; A+C_0 <-> B+C_0; 0 <-> A.
The exact product stationary law is ordinary detailed balance. A high-inventory
cutset then proves zero L2 spectral gap for every m>=2. No claim of novelty.
"""
from pathlib import Path
from fractions import Fraction as F
import math,json
P=Path(__file__).resolve().parent

def state_weight(a,b,j,m):return F(1,math.factorial(a)*math.factorial(b)*(m+1))

def reactions(a,b,j,m):
 out=[((a+1,b,j),F(1))]
 if a:out.append(((a-1,b,j),F(a)))
 if j==0:
  if a:out.append(((a-1,b+1,j),F(a)))
  if b:out.append(((a+1,b-1,j),F(b)))
 if j<m and b:out.append(((a,b-1,j+1),F(b)))
 if j>0:out.append(((a,b+1,j-1),F(1)))
 return out

if __name__=='__main__':
 count=0
 for m in [2,3,5]:
  for a in range(5):
   for b in range(7):
    for j in range(m+1):
     x=(a,b,j)
     for y,r in reactions(*x,m):
      rev=sum(rr for yy,rr in reactions(*y,m) if yy==x)
      assert state_weight(*x,m)*r==state_weight(*y,m)*rev
      # A+B+j is conserved by internal reactions; bath changes only A.
      if y[1:]!=x[1:]:assert sum(x)==sum(y)
      count+=1
 rows=[]
 for m in [2,3,5]:
  for n in [10,100,1000]:
   # q(S_n,S_n^c)=n*pi(B=n,J=0); pi(S_n)>=pi(B=n-m,J=m).
   # Common factors cancel exactly, as do the equal phase weights.
   bound=F(n)
   for k in range(m):bound/=n-k
   rows.append({'enzyme_capacity':m,'inventory_threshold':n,'conductance_upper':str(bound),'float_upper':float(bound)})
 out={'scope':'Exact detailed-balance and count-conservation checks for an analytic family. The Rayleigh-quotient argument, not finite enumeration, proves zero spectral gap.',
      'binary_reactions':True,'closed_core_conservative_weight':'w_A=w_B=1, w_Cj=j+1',
      'sole_flow':'0 <-> A','stationary':'A,B independent Poisson(1); enzyme phase uniform on 0..m',
      'high_inventory':'N=B+j','conductance_bound':'n/(n(n-1)...(n-m+1))',
      'conclusion':'gap_L2=0 for every fixed m>=2; all stationary exponential count moments are finite',
      'finite_detailed_balance_edges_checked':count,'bounds':rows,
      'role':'A general higher-rank extension cannot assume a uniform mixing gap. This is not a new recurrence result; the strongest ordinary detailed-balance construction already solves the stationary law.'}
 (P/'results').mkdir(exist_ok=True);(P/'results/catalytic_bottleneck.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
