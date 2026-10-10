#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent

def inv(a):
 n=len(a); b=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
 for i in range(n):
  s=next(j for j in range(i,n) if b[j][i]);b[i],b[s]=b[s],b[i]; t=b[i][i];b[i]=[x/t for x in b[i]]
  for j in range(n):
   if j!=i:
    t=b[j][i];b[j]=[x-t*y for x,y in zip(b[j],b[i])]
 return [row[n:] for row in b]
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def tr(a):return list(map(list,zip(*a)))
def mv(a,b):return [sum(x*y for x,y in zip(row,b)) for row in a]
def top(a,k):return sum(sorted(a,reverse=True)[:k],F(0))
def native(n,es,p):
 A=[[F((i==a)-(i==b)) for a,b in es] for i in range(n-1)];K=mm(A,tr(A));Z=inv(K);C=mm(Z,A);T=mm(tr(A),C);f=mv(tr(A),mv(Z,p[:-1]));return A,K,T,f,Z

def cert(n,k,p,iterations=8):
 es=list(combinations(range(n),2));A,K,T,f,Z=native(n,es,list(map(F,p)));m=len(es);d=[1-T[i][i] for i in range(m)]
 rho=max(top([abs(T[i][j]) for j in range(m) if i!=j],k-1)/d[i] for i in range(m));assert rho<1
 a=max(abs(f[i])/d[i] for i in range(m));u=[a/(1-rho)]*m;L=[-x for x in u];U=u[:]
 for _ in range(iterations):
  Un=[(f[i]+top([max(T[i][j]*L[j],T[i][j]*U[j],F(0)) for j in range(m) if i!=j],k-1))/d[i] for i in range(m)]
  Ln=[(f[i]-top([max(-T[i][j]*L[j],-T[i][j]*U[j],F(0)) for j in range(m) if i!=j],k-1))/d[i] for i in range(m)]
  assert all(L[i]<=Ln[i]<=Un[i]<=U[i] for i in range(m));L,U=Ln,Un
 assert all(d[i]*U[i]>=f[i]+top([max(T[i][j]*L[j],T[i][j]*U[j],F(0)) for j in range(m) if i!=j],k-1) for i in range(m))
 assert all(d[i]*L[i]<=f[i]-top([max(-T[i][j]*L[j],-T[i][j]*U[j],F(0)) for j in range(m) if i!=j],k-1) for i in range(m))
 hi=[f[i]+top([max(T[i][j]*L[j],T[i][j]*U[j],F(0)) for j in range(m) if i!=j],k) for i in range(m)]
 lo=[f[i]-top([max(-T[i][j]*L[j],-T[i][j]*U[j],F(0)) for j in range(m) if i!=j],k) for i in range(m)]
 count=0;maxflow=F(0)
 for kk in range(k+1):
  for S in combinations(range(m),kk):
   KS=[[K[i][j]-sum(A[i][s]*A[j][s] for s in S) for j in range(n-1)] for i in range(n-1)]
   ff=mv(tr(A),mv(inv(KS),p[:-1]));count+=1
   for e in range(m):
    if e not in S:assert lo[e]<=ff[e]<=hi[e];maxflow=max(maxflow,abs(ff[e]))
 out={'n':n,'m':m,'k':k,'p':list(map(str,p)),'rho':str(rho),'iterations':iterations,'exact_cases_checked':count,'all_supersolution_and_direct_flow_checks_passed':True,'max_actual_abs_flow':str(maxflow),'max_enclosure_abs_flow':str(max(map(abs,lo+hi))),'inverse':[[str(x) for x in row]for row in Z],'L':list(map(str,L)),'U':list(map(str,U)),'lo':list(map(str,lo)),'hi':list(map(str,hi))}
 return out

def counterexample():
 n=5;p=list(map(F,[0,0,3,-1,-2]));es=list(combinations(range(n),2));A,K,T,f,Z=native(n,es,p);best=(-F(10),None);star=(-F(10),None)
 for kk in range(3):
  for S in combinations(range(1,len(es)),kk):
   KS=[[K[i][j]-sum(A[i][s]*A[j][s]for s in S)for j in range(n-1)]for i in range(n-1)];theta=mv(inv(KS),p[:-1]);val=theta[0]-theta[1]
   if val>best[0]:best=(val,S)
   if all(0 in es[s] or 1 in es[s] for s in S) and val>star[0]:star=(val,S)
 assert best[0]==F(7,20) and star[0]==F(1,3)
 return {'graph':'unit K5','p':list(map(str,p)),'monitored_edge':[0,1],'budget':2,'unrestricted_maximum':str(best[0]),'unrestricted_outage_edges':[es[i] for i in best[1]],'endpoint_incident_only_maximum':str(star[0]),'endpoint_incident_outage_edges':[es[i] for i in star[1]],'exact_gap':str(best[0]-star[0])}

if __name__=='__main__':
 out={'certificates':[cert(6,2,[1,-1,-1,-1,1,1]),cert(6,3,[3,-2,0,1,-1,-1])],'false_double_star_shortcut':counterexample()}
 (ROOT/'exact_results.json').write_text(json.dumps(out,indent=2));print(json.dumps({**out,'certificates':[{k:v for k,v in c.items() if k not in ['inverse','L','U','lo','hi']}for c in out['certificates']]},indent=2))
