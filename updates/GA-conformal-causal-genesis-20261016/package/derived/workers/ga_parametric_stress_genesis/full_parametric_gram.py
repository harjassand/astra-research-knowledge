import numpy as np,sympy as S,itertools,sys
from pathlib import Path
base=Path(__file__).parent
mode=sys.argv[1] if len(sys.argv)>1 else 'flex4'
r,a,b,c,d,s=S.symbols('r a b c d s',real=True);vs=(r,a,b,c,d,s)
u=(a+s)**2+c*c;v=b*b+(d+s)**2;j=(a+s)*(d+s)-b*c
al=S.Rational(3,8)*r/(r+2)
J=al*(u+v-2*j)**2+r*(r-1)*u*u/6+j*j+r*u*j
G=S.factor(J-(r+2)*(r+3)*s**4/6-(r+2)*(2*r+3)*s**3*a/3-(-(r+2)*s*s*b+4*al*b**3)*c-((r+2)*s**3+(5*r+2)*s*s*a+5*r*s*a*a+(r-4*al)*a**3)*d)
if mode=='simple':
 G=S.factor(J-(r+2)*(r+3)*s**4/6-(r+2)*(2*r+3)*s**3*a/3-(-(r+2)*s*s*b+7*r/(6*(r+2))*b**3)*c-((r+2)*s**3+(S.Rational(5,2)*r+2)*s*s*a+S.Rational(7,4)*r*s*a*a+r*(4*r+3)/(12*(r+2))*a**3)*d)
h=a*d-b*c+s*(a+d)
P=S.Poly(S.cancel((r+2)*G),vs)
mons=[k for k in itertools.product(range(3),repeat=5) if sum(k)==2 and k!=(0,0,0,0,2) and k!=(0,1,0,0,1)]
z=[S.prod(x**k for x,k in zip((a,b,c,d,s),m)) for m in mons]
z0=[x for x in z if x not in [b*b,d*d,b*d,d*s]]
w=[a*a+c*c+2*a*s,a*s,c*s]
zz0=[h]+[r*x for x in z0];zz1=z+[r*x for x in w]
zz=zz0+zz1;n0=len(zz0);n=len(zz)
exprs={};pairs=[(i,j) for i in range(n) for j in range(i,n) if (i<n0)==(j<n0)]
for i,j in pairs:exprs[i,j]=S.Poly(S.expand(zz[i]*zz[j]*(1 if i<n0 else r)),vs)
exps=sorted(set(P.monoms())|set(m for p in exprs.values() for m in p.monoms()))
mat=np.zeros((len(exps),len(pairs)))
for k,(i,j) in enumerate(pairs):
 for m,vv in exprs[i,j].terms():mat[exps.index(m),k]=float(vv)*(1 if i==j else 2)
rhs0=np.array([float(P.coeff_monomial(e)) for e in exps])
mode=sys.argv[1] if len(sys.argv)>1 else 'flex4'
free=[]
if mode in ['flex','flex4']:
 free=[(k,1,0,0,1,2) for k in [1,2]]+[(k,2,0,0,1,1) for k in [1,2]]
if mode=='flex4':free += [(k,3,0,0,1,0) for k in [1,2]]+[(k,0,3,1,0,0) for k in [1,2]]
free=[e for e in free if e in exps]
keep=[i for i,e in enumerate(exps) if e not in free];mm=mat[keep];rhs=rhs0[keep]
invw=np.array([1 if i==j else .5 for i,j in pairs]);op=(invw[:,None]*mm.T)@np.linalg.pinv((mm*invw)@mm.T,rcond=1e-12)
def affine(q):
 vec=np.array([q[i,j] for i,j in pairs]);vec+=op@(rhs-mm@vec)
 out=np.zeros_like(q)
 for v0,(i,j) in zip(vec,pairs):out[i,j]=out[j,i]=v0
 return out
q=np.eye(n);p1=np.zeros_like(q);p2=np.zeros_like(q);floor=float(sys.argv[2]) if len(sys.argv)>2 else 0
for it in range(400000):
 rr=q+p1;na=affine(rr);p1=rr-na
 rr=na+p2;qt=np.zeros_like(q)
 for sl in [slice(0,n0),slice(n0,n)]:
  ev,uu=np.linalg.eigh(rr[sl,sl]);qt[sl,sl]=(uu*np.maximum(ev,floor))@uu.T
 q=qt;p2=rr-q
 if it%5000==0:
  err=np.linalg.norm(mm@np.array([q[i,j] for i,j in pairs])-rhs)
  print(mode,it,err,np.linalg.eigvalsh(affine(q))[0],flush=True)
  if err<1e-10:break
Q=affine(q);delta=mat@np.array([Q[i,j] for i,j in pairs])-rhs0
print('free coefficients',[(e,float(delta[exps.index(e)])) for e in free],flush=True)
np.savez(base/f'full_parametric_{mode}.npz',gram=Q,mons=mons,mat=mat,rhs=rhs0,exps=exps,free=free,n0=n0,z0=[str(x) for x in zz0],z1=[str(x) for x in zz1])
