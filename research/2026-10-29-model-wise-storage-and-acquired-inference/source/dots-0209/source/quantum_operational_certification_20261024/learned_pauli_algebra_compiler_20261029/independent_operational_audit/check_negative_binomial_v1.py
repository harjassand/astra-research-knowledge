"""Exact-rational tail indexing and adaptive opportunity-prefix checks."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
checks=0
for m in range(1,8):
 for p in [F(1,4),F(1,2),F(3,4)]:
  q=1-p
  for t in range(21):
   cdf=sum(F(comb(m+f-1,f))*p**m*q**f for f in range(t+1))
   tail=sum(F(comb(m+t,j))*p**j*q**(m+t-j) for j in range(m))
   assert 1-cdf==tail;checks+=1
# Exact finite-tree policies with state (rank,faults,services,round,lastrole).
# Opportunities may depend on all past represented information, not currentcoin.
policies={'always':lambda r,f,s,t,last:True,'alternating':lambda r,f,s,t,last:t%2==0,'history_dependent':lambda r,f,s,t,last:(last==1 or t%3==0)}
rows=[]
for name,policy in policies.items():
 m=3;p=F(1,3);q=1-p;J=8;cap=18
 states={(0,0,0,0,0):F(1)};done={}
 for t in range(cap):
  nxt={}
  for (r,f,s,_,last),weight in states.items():
   opportunity=r<m and policy(r,f,s,t,last)
   for role,prob in [(0,p),(1,q)]:
    rr=r+int(opportunity and role==0);ff=f+int(opportunity and role==1);ss=s+role
    if ss==J:done[ff]=done.get(ff,F(0))+weight*prob
    else:
     key=(rr,ff,ss,t+1,role);nxt[key]=nxt.get(key,F(0))+weight*prob
  states=nxt
 for (r,f,s,t,last),w in states.items():done[f]=done.get(f,F(0))+w
 assert sum(done.values())==1
 for t in range(J+1):
  actual=sum(w for f,w in done.items() if f>t)
  bound=sum(F(comb(m+t,j))*p**j*q**(m+t-j) for j in range(m))
  assert actual<=bound
 rows.append({'policy':name,'exact_tail_checks':J+1})
result={'exact_NB_binomial_identity_checks':checks,'adaptive_stopped_policy_checks':rows,'scope':'Exact finite arithmetic consistency, not replacement for stream-coupling proof.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
