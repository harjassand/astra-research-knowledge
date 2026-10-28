#!/usr/bin/env python3
"""Exact paired-axis coarse confidence, strict threshold and funded-cap checks."""
from fractions import Fraction as F
from pathlib import Path
import json

def clog(x):
 k=0
 while F(2)**k<x:k+=1
 return k
cases=[];cap_fail_cases=0
for n,q,w in [(3,1,3),(5,2,2),(8,4,3),(2,2,1)]:
 d0=2**w;M=n-w+1
 for beta in [F(1,8),F(1,1000)]:
  bc=beta/2
  for lam in [F(1),F(1,2),F(1,17),F(1,1000)]:
   s=0
   while F(1,4*2**s)>lam/4:s+=1
   Sc=s+2;L=clog(F(4*d0*q*M*(Sc+1),1)/bc)
   Ns=[]
   for k in range(Sc+1):
    eta=F(1,4*2**k);N=8*12**w*L/(eta*eta);assert N.denominator==1;Ns.append(int(N))
    a=eta/d0;den=2*(2*3**w+F(4*d0,3)*a)
    assert den<=5*3**w and N*a*a/den>=L
    # Strict support threshold separates all disjoint scores from qualifying true scores.
    assert F(5,4)*eta<2*eta
    if 4*eta<=1:assert 4*eta-F(5,4)*eta>2*eta
   assert F(4*d0*q*M*(Sc+1),2**L)<=bc
   assert sum(Ns[:s+1])<F(4,3)*Ns[s]
   assert Ns[s]<=F(512*12**w*L,1)/(lam*lam)
   assert sum(Ns)==Ns[0]*(4**(Sc+1)-1)//3
   if s>0:
    insufficient=s-1
    assert F(1,4*2**insufficient)>lam/4
    cap_fail_cases+=1
   cases.append({'n':n,'q':q,'w':w,'beta':str(beta),'max_axis_mass':str(lam),'first_sufficient_stage':s,'funded_cap':Sc,'first_sufficient_blocks':Ns[s],'worst_coarse_blocks':sum(Ns)})
result={'status':'PASS exact margin-free paired-coarse budgets','source_draws':0,'rng_draws':0,'paired_coarse_budget_cases':len(cases),'insufficient_caller_cap_witnesses':cap_fail_cases,'cases':cases}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
