"""Exact Fraction audit of boundary, uniform, and near-uniform fixtures."""
from fractions import Fraction as Q
from itertools import permutations
import json
from pathlib import Path

PERMS=tuple(permutations(range(4)))
ZERO=Q(0);ONE=Q(1)

def vals(p):
    x=(p[0]+p[1]-p[2]-p[3],p[0]-p[1]+p[2]-p[3],p[0]-p[1]-p[2]+p[3])
    A=sum(v*v for v in x); B=x[0]*x[1]*x[2]
    C=x[0]**2*x[1]**2+x[0]**2*x[2]**2+x[1]**2*x[2]**2
    H=B-A*A/10-3*C/20+3*A*B/10-A**3/50+7*A*C/100-51*B**2/100
    F=4*A-3*B+7*A*A/10-4*C-4*A*B/5
    G=1-161*A/100-31*B/10+773*A*A/1000+4*C-199*A*B/50
    return A,H,F,G

def margins(p,q):
    Ap,Hp,Fp,Gp=vals(p);Aq,Hq,Fq,Gq=vals(q)
    za=ZERO;zh=ZERO
    for perm in PERMS:
      U=tuple(4*p[i]*q[perm[i]] for i in range(4));z=sum(U)
      if z:
        As,Hs,_,_=vals(tuple(u/z for u in U));za+=z*As;zh+=z*Hs
    za/=24;zh/=24;cubic=Ap*Aq*(Ap+Aq)
    base=Ap+Aq-Hp*Fq-Fp*Hq-za
    return base-cubic/1000,zh-Hp*Gq-Gp*Hq,base/cubic if cubic else None

def grid(n):
 return sorted(set(tuple(sorted((Q(a,n),Q(b,n),Q(c,n),Q(n-a-b-c,n)),reverse=True)) for a in range(n+1) for b in range(n-a+1) for c in range(n-a-b+1)))

def main():
 pts=grid(12);minima=[None,None,None];negative=[0,0,0];count=0
 for i,p in enumerate(pts):
  for q in pts[:i+1]:
   vv=margins(p,q);count+=1
   for j,v in enumerate(vv):
    if v is None:continue
    if v<0:negative[j]+=1
    if minima[j] is None or v<minima[j]['value']:
      minima[j]={'value':v,'p':p,'q':q}
 def conv(r):return {'value':str(r['value']),'p':[str(v) for v in r['p']],'q':[str(v) for v in r['q']]}
 result={'grid_size':len(pts),'unordered_pairs':count,'negative_counts':negative,'minima':[conv(r) for r in minima],'near_uniform':[]}
 u=(Q(1,4),)*4
 v=(ONE,ZERO,ZERO,ZERO);w=(Q(1,2),Q(1,2),ZERO,ZERO)
 for k in [2,4,8,12]:
  t=Q(1,10**k);p=tuple(ui+t*(vi-ui) for ui,vi in zip(u,v));q=tuple(ui+t*(wi-ui) for ui,wi in zip(u,w))
  vv=margins(p,q)
  result['near_uniform'].append({'scale':str(t),'A_residual':str(vv[0]),'H_residual':str(vv[1]),'cubic_coefficient':str(vv[2]),'cubic_float':float(vv[2])})
 Path(__file__).with_name('rational_exact_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
