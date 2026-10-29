import itertools,math,json,numpy as np
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).parent
# Exact standard GT raising coefficient formula, independently reduced on rectangles.
def comps(k,d):
 if d==1:yield (k,);return
 for a in range(k+1):
  for b in comps(k-a,d-1):yield (a,)+b
cases=0
for d in range(2,10):
 for k in range(6):
  for a in comps(k,d):
   ts=[k]
   for x in a:ts.append(ts[-1]-x)
   rows={j:[k]*(j-1)+[ts[j]] for j in range(1,d+1)}
   for j in range(1,d):
    if not a[j-1]:continue
    l=rows[j][j-1]-j
    numerator=-math.prod(rows[j+1][i-1]-i-l for i in range(1,j+2))*math.prod(rows[j-1][i-1]-i-l-1 for i in range(1,j))
    denominator=math.prod((rows[j][i-1]-i-l)*(rows[j][i-1]-i-l-1) for i in range(1,j))
    value=F(numerator,denominator);assert value==a[j-1]*(a[j]+1)
    b=list(a);b[j-1]-=1;b[j]+=1
    phase=lambda v:(-1)**sum((i+1)*x for i,x in enumerate(v))
    assert phase(a)==-phase(b);cases+=1
# Independently compute successive geometric waiting-time probability masses.
def renewal(N,rates,D,k):
 mass=[1]+[0]*N
 for r in list(rates)*k:
  out=[0]*(N+1)
  for n in range(1,N+1):out[n]=(D-r)*out[n-1]+r*mass[n-1]
  mass=out
 return sum((F(mass[n],D**n) for n in range(N+1)),F(0))
source=json.loads((P/'replay/exact_renewal_bound.json').read_text());count=0
for row in source['rows']:
 rates,D=([1]*8,8) if row['model']=='uniform_minus' else ([1,1,1,2,2,3,3,3],16 if row['model']=='two_axis_minus' else 36)
 assert renewal(row['steps'],rates,D,row['k'])==F(row['probability']);count+=1
# Exhaustively test RSK decreasing-subsequence criterion and renewal lower bound.
def shape(word):
 rows=[]
 for a in word:
  for row in rows:
   i=next((i for i,b in enumerate(row) if b>a),None)
   if i is None:row.append(a);break
   row[i],a=a,row[i]
  else:rows.append([a])
 return [len(r) for r in rows]
def greed(word):
 stage=0
 for a in word:
  if a==2-stage%3:stage+=1
 return stage//3
exhaustive=0
for N in range(9):
 ones=twos=greedtwo=0
 for word in itertools.product(range(3),repeat=N):
  sh=shape(word);k=sh[2] if len(sh)>2 else 0;g=greed(word);assert k>=g and (k>=1)==(g>=1);ones+=k>=1;twos+=k>=2;greedtwo+=g>=2;exhaustive+=1
 assert F(ones,3**N)==renewal(N,[1]*3,3,1)
 assert F(twos,3**N)>=renewal(N,[1]*3,3,2)==F(greedtwo,3**N)
# Dense d3 instrument independently expressed using central projectors, no SVD basis.
def perm(p):
 out=np.zeros((27,27))
 for x in itertools.product(range(3),repeat=3):
  y=[x[i] for i in p];out[9*y[0]+3*y[1]+y[2],9*x[0]+3*x[1]+x[2]]=1
 return out
Ps=sum(perm(p) for p in itertools.permutations(range(3)))/6
Pa=sum((-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))*perm(p) for p in itertools.permutations(range(3)))/6
P21=np.eye(27)-Ps-Pa;eps=np.zeros((3,9))
for p in itertools.permutations(range(3)):
 eps[p[0],3*p[1]+p[2]]=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))/math.sqrt(2)
T=np.kron(eps,np.eye(3));K0=T@P21;K1=T@P21@(perm((0,2,1))-.5*np.eye(27))/math.sqrt(.75);effect=K0.T@K0+K1.T@K1;err=np.linalg.norm(effect-P21)
rng=np.random.default_rng(110005);res=[]
for _ in range(24):
 U,_=np.linalg.qr(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)));c=U[:,0];W=U[:,1:];V=np.kron(np.kron(W,W),W);psi=rng.normal(size=(8,5))+1j*rng.normal(size=(8,5));psi=V@psi;psi/=np.linalg.norm(psi);discard=np.eye(3)-np.outer(c.conj(),c)
 res.append(max(np.linalg.norm(np.einsum('ab,bjk->ajk',discard,(K@psi).reshape(3,3,5))) for K in [K0,K1]))
assert err<1e-12 and max(res)<1e-12
out={'exact_GT_raising_phase_checks':cases,'exact_renewal_rows_reproduced':count,'exhaustive_RSK_words':exhaustive,'independent_dense_effect_residual':float(err),'memory_dimension':5,'complex_correlated_cases':len(res),'max_decoupling_residual':float(max(res))};(P/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
