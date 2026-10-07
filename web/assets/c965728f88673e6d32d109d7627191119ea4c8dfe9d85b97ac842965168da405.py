"""Bounded exact rational checks of the new O(d) comparator.
The proof is analytic; these checks verify formulas and explicit compressed
star actions, not inference about arbitrary compatible channels.
"""
from fractions import Fraction as Q
from pathlib import Path
import json, datetime

def sub(A,B): return [[x-y for x,y in zip(a,b)] for a,b in zip(A,B)]
def mul(A,B): return [[sum(x*y for x,y in zip(a,b)) for b in zip(*B)] for a in A]
def transpose(A):return list(map(list,zip(*A)))
def psd_ldl(A):
 n=len(A);L=[[Q(i==j) for j in range(n)] for i in range(n)];D=[]
 for j in range(n):
  v=A[j][j]-sum(L[j][k]**2*D[k] for k in range(j));D.append(v)
  assert v>=0
  for i in range(j+1,n):
   r=A[i][j]-sum(L[i][k]*L[j][k]*D[k] for k in range(j))
   if v:L[i][j]=r/v
   else:assert r==0
 return [str(x) for x in D]
rows=[];admitted=0
for d in range(2,25):
 G=[[Q(d if i==j else 1) for j in range(3)] for i in range(3)]
 DP=[[Q(d),Q(1),Q(1)],[Q(1),Q(d),Q(1)],[Q(0),Q(0),Q(0)]]
 S=[[Q(1),Q(0),Q(1)],[Q(0),Q(1),Q(1)],[Q(1),Q(1),Q(0)]]
 KA=[[x/2 for x in r] for r in sub(DP,S)]
 KS=[[((DP[i][j]+S[i][j])/2-Q(2,d)*(i==j)) for j in range(3)] for i in range(3)]
 bounds=[('antisymmetric',KA,Q(d,2)),('symmetric',KS,Q(d,2)+Q(3,2)-Q(2,d)),('all',[[DP[i][j]-Q(2,d)*(i==j) for j in range(3)]for i in range(3)],Q(d+1)-Q(2,d))]
 exact=[]
 for name,K,b in bounds:
  A=[[b*(i==j)-K[i][j] for j in range(3)]for i in range(3)]
  GA=mul(G,A)
  assert GA==transpose(GA)
  exact.append({'witness':name,'ldl_pivots':psd_ldl(GA)})
 ra=Q(d*(d-1),2);rs=Q((d-1)*(d+2),2)
 max_slack_a=Q(1);max_slack_s=Q(1)
 for ia in range(101):
  la=Q(ia,100)
  for iss in range(101):
   ls=Q(iss,100)
   if la>Q(d,2*(d-1)) or ls>Q(d+4,2*(d+2)) or ra*la+rs*ls>Q((d-1)*(d+2),2):continue
   ma=max(Q(0),2*la-1);ms=Q(2,d+2)-Q(d,d+2)*ma
   assert 0<=ma<=Q(1,d-1) and 0<=ms<=1
   assert 1-ma<=2*(1-la) and 1-ms<=2*(1-ls)
   assert ra*ma+rs*ms==d-1
   max_slack_a=min(max_slack_a,2*(1-la)-(1-ma));max_slack_s=min(max_slack_s,2*(1-ls)-(1-ms));admitted+=1
 rows.append({'d':d,'compressed_star_exact_psd':exact,'grid_min_slack_a':str(max_slack_a),'grid_min_slack_s':str(max_slack_s)})
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'dimensions':rows,'grid_admitted_pairs':admitted,'status':'EXACT_FORMULA_CHECKS','scope':'rational compressed witness PSD and comparator formulas under necessary compatibility inequalities; analytic proof supplies all d, no solver or generic EB classification'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'dimensions':len(rows),'admitted_pairs':admitted,'all_exact_checks_passed':True}))
