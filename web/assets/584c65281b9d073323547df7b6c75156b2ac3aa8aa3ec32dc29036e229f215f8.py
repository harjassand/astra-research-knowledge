"""Exact rational-complex eight-site witnesses to the sharp factor 3."""
from fractions import Fraction as Q
from itertools import combinations,permutations
from pathlib import Path
import json,time

def add(a,b):return(a[0]+b[0],a[1]+b[1])
def neg(a):return(-a[0],-a[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return(a[0],-a[1])
def norm(a):return a[0]*a[0]+a[1]*a[1]
def det(a):
 n=len(a);s=(Q(0),Q(0))
 for p in permutations(range(n)):
  v=(-1 if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2 else 1,0)
  for i in range(n):v=mul(v,a[i][p[i]])
  s=add(s,v)
 return s
zero=(Q(0),Q(0));one=(Q(1),Q(0))
def Z(F,U):
 R=[i for i in range(len(F)) if i not in U];k=len(R)//2
 if len(R)%2:return Q(0)
 return sum((norm(det([[F[i][j] for j in R if j not in I] for i in I])) for I in combinations(R,k)),Q(0))
def construct(a,b):
 rho=(Q(b*b-a*a,b*b+a*a),Q(2*a*b,b*b+a*a));rho2=mul(rho,rho)
 u=[one,zero,neg(rho2),rho];v=[zero,one,rho,rho2]
 F=[[zero for j in range(8)] for i in range(8)]
 F[4][:4]=u;F[4][5]=one;F[5][:4]=v
 F[6][:4]=[conj(x) for x in u];F[6][7]=one;F[7][:4]=[conj(x) for x in v]
 return F,rho
start=time.time();rows=[];a,b=2,1
for step in range(4):
 assert a*a-3*b*b==1
 F,rho=construct(a,b);r=rho[0]*rho[0]
 f={():Z(F,()),(0,1,2,3):Z(F,(0,1,2,3))}
 for U in combinations(range(4),2):f[U]=Z(F,U)
 assert f[()]==(4+12*r-16*r*r)**2
 assert f[(0,1,2,3)]==1
 assert f[(0,1)]==8*r
 for U in ((0,2),(0,3),(1,2),(1,3),(2,3)):assert f[U]==2
 products=[f[(0,1)]*f[(2,3)],f[(0,2)]*f[(1,3)],f[(0,3)]*f[(1,2)]]
 ratio=f[()]/sum(products)
 assert 3*sum(products)-f[()]==8*(4*r-1)**2*(1+2*r-2*r*r)>0
 rows.append({'step':step,'a':a,'b':b,'rho':[str(x) for x in rho],'r':str(r),'hole_coefficients':{str(U):str(v) for U,v in f.items()},'pair_products':[str(v) for v in products],'ratio':str(ratio),'ratio_float':float(ratio),'gap_from_three':str(3-ratio),'F':[[[str(v) for v in z] for z in row] for row in F]})
 a,b=2*a+3*b,a+2*b
assert all(rows[j]['ratio_float']<rows[j+1]['ratio_float'] for j in range(3))
result={'status':'PASS','fixture_count':len(rows),'dimension':8,'activities':'all one','field':'Q(i)','runtime_seconds':time.time()-start,'fixtures':rows,'scope':'Exact rational-complex complementary-minor sums and sharp-constant construction, no sampler or FPRAS.'}
Path('work/cycle6/c02_s02/revisions/sharp_factor_three_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='fixtures'}))
print(json.dumps([{'a':x['a'],'b':x['b'],'ratio':x['ratio_float']} for x in rows]))
