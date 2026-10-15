from fractions import Fraction as F
from math import isqrt
class I:
 def __init__(self,a,b=None): self.l=F(a);self.h=F(a if b is None else b)
 def __add__(a,b):
  b=iv(b);return I(a.l+b.l,a.h+b.h)
 __radd__=__add__
 def __neg__(a):return I(-a.h,-a.l)
 def __sub__(a,b):return a+-iv(b)
 def __rsub__(a,b):return iv(b)+-a
 def __mul__(a,b):
  b=iv(b);v=[a.l*b.l,a.l*b.h,a.h*b.l,a.h*b.h];return I(min(v),max(v))
 __rmul__=__mul__
 def __truediv__(a,b):
  b=iv(b);assert b.l*b.h>0,(float(b.l),float(b.h));return a*I(1/b.h,1/b.l)
 def __rtruediv__(a,b):return iv(b)/a
 def sqrt(a):
  assert a.l>0
  k=10**30
  return I(F(isqrt(a.l.numerator*k*k//a.l.denominator),k),F(isqrt(a.h.numerator*k*k//a.h.denominator)+1,k))
 def __repr__(a):return '[%.12g, %.12g]'%(float(a.l),float(a.h))
def iv(x):return x if isinstance(x,I) else I(x)
def solve(A,b):
 A=[[iv(x) for x in r]+[iv(y)] for r,y in zip(A,b)];n=len(b)
 for k in range(n):
  p=A[k][k];A[k]=[x/p for x in A[k]]
  for j in range(n):
   if j!=k:
    p=A[j][k];A[j]=[x-p*y for x,y in zip(A[j],A[k])]
 return [r[-1] for r in A]
def response(H,a,u):
 x=solve([[int(i==j)+H[i][j]*u[j] for j in range(3)] for i in range(3)],[1]*3)
 return 10-sum(a[i]*u[i]*x[i] for i in range(3))
H=[[F(2),F(1,5),F(1,2)],[F(3,10),F(2),F(11,10)],[F(7,10),F(13,10),F(2)]];a=[F(1),F(2),F(3)]
import sys
eta=F(sys.argv[1] if len(sys.argv)>1 else '1e-8')
# Exact central readings with declared error bars. True values lie at their centers.
measurement_log=[]
def measure(u):
 z=response(H,a,u);assert z.l==z.h
 measurement_log.append((tuple(map(str,u)),str(z.l),str(eta)))
 return I(z.l-eta,z.h+eta)
f0=measure([0]*3);aa=[];dd=[];sing=[]
for i in range(3):
 ds=[]
 for t in [F(1,2),F(1)]:
  u=[0]*3;u[i]=t;ds.append(f0-measure(u))
 d=(ds[1]-2*ds[0])/(ds[0]-ds[1]);ai=2*ds[0]*(1+d/2)
 dd.append(d);aa.append(ai);sing.append(ds[0]-ds[1])
edges={};gaps=[];discs=[]
for i,j in [(0,1),(0,2),(1,2)]:
 ds=[];rs=[]
 for t in [F(1,2),F(1)]:
  u=[0]*3;u[i]=u[j]=t;delta=f0-measure(u);ds.append(delta)
  rs.append((aa[i]*t+aa[j]*t+(aa[i]*dd[j]+aa[j]*dd[i])*t*t-delta*(1+dd[i]*t)*(1+dd[j]*t))/(t*t))
 p=(rs[0]-rs[1])/(ds[1]-ds[0]);q=rs[0]+ds[0]*p;disc=q*q-4*aa[i]*aa[j]*p;sq=disc.sqrt();discs.append(disc);gaps.append(ds[1]-ds[0])
 edges[i,j]=[((q-sq)/(2*aa[i]),(q+sq)/(2*aa[j])),((q+sq)/(2*aa[i]),(q-sq)/(2*aa[j]))]
print('eta',eta,'single denominators',sing,'pair gaps',gaps,'discriminants',discs)
print('a',aa,'d',dd)
y=measure([1]*3);print('triple observed',y)
keep=[]
for s in [0,1]:
 for t in [0,1]:
  HH=[[iv(dd[i]) if i==j else iv(0) for j in range(3)] for i in range(3)]
  for (i,j),choice in zip([(0,1),(0,2),(1,2)],[0,s,t]):HH[i][j],HH[j][i]=edges[i,j][choice]
  z=response(HH,aa,[1]*3);ok=max(y.l,z.l)<=min(y.h,z.h)
  print('branch',s,t,z,'retain',ok)
  if ok:keep.append(HH)
assert len(keep)==1
HH=keep[0]
# Convenient rational nominal center chosen independently, verified inside these boxes.
E=max(max(abs(HH[i][j].l-H[i][j]),abs(HH[i][j].h-H[i][j])) for i in range(3) for j in range(3))
EA=max(max(abs(aa[i].l-a[i]),abs(aa[i].h-a[i])) for i in range(3))
# ||E||2 <=3*maxentry; ||aerror||2 ||1||2 <=3*maxentry.
deltaH=3*E;h=F(1,5)-deltaH;B=1/(1+h)
# ||ahat||2 ||1||2 =sqrt(42)<6.481; use 13/2.
bound=eta+3*EA*B+F(13,2)*B*B*deltaH
print('H intervals',HH,'max H entry radius',float(E),'max a entry radius',float(EA))
print('deltaH',float(deltaH),'robust h',float(h),'B',float(B),'uniform bound',float(bound))

print("RAW RECEIPT: control vector, central response, radius")
for row in measurement_log: print(row)
