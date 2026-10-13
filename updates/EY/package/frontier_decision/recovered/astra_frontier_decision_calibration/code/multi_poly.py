"""Exact rational sparse-polynomial utilities and certified box estimates."""
from fractions import Fraction as F
from collections import defaultdict
import itertools,math
Z=(0,0,0)
def load(rows):return {tuple(a):F(c) for a,c in rows if F(c)}
def dump(p):return [[list(a),str(c)] for a,c in sorted(p.items()) if c]
def add(p,q,scale=F(1)):
 r=defaultdict(F,p)
 for a,c in q.items():r[a]+=scale*c
 return {a:c for a,c in r.items() if c}
def mul(p,q):
 r=defaultdict(F)
 for a,c in p.items():
  for b,d in q.items():r[tuple(x+y for x,y in zip(a,b))]+=c*d
 return {a:c for a,c in r.items() if c}
def deriv(p,axis,times=1):
 for _ in range(times):
  r={}
  for a,c in p.items():
   if a[axis]:b=list(a);b[axis]-=1;r[tuple(b)]=c*a[axis]
  p=r
 return p
def scale(p,s):return {a:c*s for a,c in p.items() if c*s}
def evalpoly(p,x):return sum((c*math.prod(F(y)**k for y,k in zip(x,a)) for a,c in p.items()),F())
def compose(p,maps):
 degree=[max((a[i] for a in p),default=0) for i in range(3)]
 powers=[]
 for i in range(3):
  pp=[{Z:F(1)}]
  for k in range(degree[i]):pp.append(mul(pp[-1],maps[i]))
  powers.append(pp)
 out={}
 for a,c in p.items():
  v={Z:c}
  for i,k in enumerate(a):v=mul(v,powers[i][k])
  out=add(out,v)
 return out

def shift(p,centre):
 """p(centre+y), expanding one coordinate at a time."""
 out=p
 for ax in range(3):
  c=F(centre[ax]);r=defaultdict(F)
  for a,v in out.items():
   for k in range(a[ax]+1):
    b=list(a);b[ax]=k;r[tuple(b)]+=v*math.comb(a[ax],k)*c**(a[ax]-k)
  out={a:v for a,v in r.items() if v}
 return out

def bound(p,box):
 cen=[(a+b)/2 for a,b in box];rad=[(b-a)/2 for a,b in box];s=shift(p,cen)
 mid=s.get(Z,F());err=sum((abs(c)*math.prod(r**k for r,k in zip(rad,a)) for a,c in s.items() if a!=Z),F())
 return mid-err,mid+err

def partition_bound(p,box,parts=(1,1,1)):
 bestlo=None;besthi=None
 for idx in itertools.product(*[range(n) for n in parts]):
  cell=[]
  for i,j in enumerate(idx):
   a,b=box[i];cell.append((a+(b-a)*F(j,parts[i]),a+(b-a)*F(j+1,parts[i])))
  lo,hi=bound(p,cell);bestlo=lo if bestlo is None else min(bestlo,lo);besthi=hi if besthi is None else max(besthi,hi)
 return bestlo,besthi

def factorial(a):return math.prod(math.factorial(k) for k in a)
def residual_norm_poly(rec,derivative=(0,0,0),which='both'):
 inds=[tuple(a) for a in rec['residual_indices']]
 go=rec['residual_odd_gram_exact'];ge=rec['residual_even_gram_exact'];p=defaultdict(F)
 active=[]
 for i,a in enumerate(inds):
  if all(ai>=di for ai,di in zip(a,derivative)):
   b=tuple(ai-di for ai,di in zip(a,derivative));active.append((i,b,F(1,factorial(b))))
 for i,a,c in active:
  for j,b,d in active:
   v=(F(go[i][j]) if which!='even' else F())+(F(ge[i][j]) if which!='odd' else F())
   p[tuple(ai+bi for ai,bi in zip(a,b))]+=c*d*v
 return {a:v for a,v in p.items() if v}

def sqrt_upper(x,bits=44):
 x=F(x)
 if x<0:raise ValueError(x)
 s=1<<bits;n=(x.numerator*s*s+x.denominator-1)//x.denominator;k=math.isqrt(n)
 if k*k<n:k+=1
 return F(k,s)

class Certificate:
 def __init__(self,rec):
  self.rec=rec;self.p=load(rec['corrected_D_poly']);self.centre=[F(rec['parameters'][k]) for k in ['V','U','d']]
  self.q=[residual_norm_poly(rec,(i,0,0)) for i in range(3)]
  self.grad=deriv(self.p,0);self.curv=deriv(self.grad,0)
 def compute(self,box,parts=(1,1,1),maps=None):
  # box refers to the coordinates after maps. d = d0 + maps[2].
  q=self.q;gp=self.grad;cp=self.curv
  if maps is not None:
   q=[compose(v,maps) for v in q];gp=compose(gp,maps);cp=compose(cp,maps)
   dmin=self.centre[2]+bound(maps[2],box)[0]
  else:dmin=self.centre[2]+box[2][0]
  beta=min(F(1),dmin/self.centre[2]);assert beta>0
  Q=[sqrt_upper(max(F(),partition_bound(v,box,parts)[1])) for v in q]
  e1=4*(2*Q[0]*Q[1]/beta+Q[0]**2/beta**2)
  e2=4*(2*Q[0]*Q[2]/beta+2*Q[1]**2/beta+4*Q[0]*Q[1]/beta**2+2*Q[0]**2/beta**3)
  gl,gu=partition_bound(gp,box,parts);cl,cu=partition_bound(cp,box,parts)
  return dict(gradient=[gl-e1,gu+e1],curvature=[cl-e2,cu+e2],corrected_gradient=[gl,gu],corrected_curvature=[cl,cu],residual_norms=Q,beta=beta,gradient_error=e1,curvature_error=e2)
