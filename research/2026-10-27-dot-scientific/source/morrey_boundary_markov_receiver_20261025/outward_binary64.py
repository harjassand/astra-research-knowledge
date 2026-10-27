"""Outward IEEE-754 binary64 arrays. No transcendental library value is trusted.
Every basic operation is widened one adjacent binary64 number. Subnormals are
supported; overflow/non-finite values reject. sqrt is proposal-only with outward
squared inequalities receiving it. Trig uses rational Taylor remainder after
pi/2 range reduction with an exact Machin pi enclosure. Sums use explicit
pairwise additions, never BLAS/einsum implicit summation error assumptions.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import factorial
import sys,json,numpy as np
P=Path(__file__).parent
sys.path.insert(0,str(P.parent/'morrey_global_w1_receiver_20261025'))
from certified_w1_receiver import pi_interval
NEG=-np.inf;POS=np.inf

def down(x):
 y=np.nextafter(x,NEG);assert np.all(np.isfinite(y));return y

def up(x):
 y=np.nextafter(x,POS);assert np.all(np.isfinite(y));return y

def rat(x):
 x=Q(x);z=float(x);lo=z if Q(z)<=x else np.nextafter(z,NEG);hi=z if Q(z)>=x else np.nextafter(z,POS)
 assert Q(float(lo))<=x<=Q(float(hi));return np.asarray(lo),np.asarray(hi)

def box(lo,hi=None):
 if hi is None:hi=lo
 a=rat(lo)[0];b=rat(hi)[1];assert a<=b;return a,b

def arr(lo,hi):return np.asarray(lo,dtype=float),np.asarray(hi,dtype=float)
def exact(x):return arr(x,x)
def add(a,b):return down(a[0]+b[0]),up(a[1]+b[1])
def neg(a):return -a[1],-a[0]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 vv=np.broadcast_arrays(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]);return down(np.minimum.reduce(vv)),up(np.maximum.reduce(vv))
def square(a):
 lo=np.where((a[0]<=0)&(a[1]>=0),0,np.minimum(a[0]*a[0],a[1]*a[1]));hi=np.maximum(a[0]*a[0],a[1]*a[1]);return np.maximum(0,down(lo)),up(hi)
def div(a,b):
 assert np.all((b[0]>0)|(b[1]<0));vv=np.broadcast_arrays(a[0]/b[0],a[0]/b[1],a[1]/b[0],a[1]/b[1]);return down(np.minimum.reduce(vv)),up(np.maximum.reduce(vv))
def sqrt(a):
 assert np.all(a[0]>=0);lo=np.sqrt(a[0]);hi=np.sqrt(a[1])
 # np.sqrt values merely propose endpoints. Multiplication is the verifier.
 for unused in range(8):
  badlo=(lo>0)&(up(lo*lo)>a[0]);badhi=down(hi*hi)<a[1]
  if not np.any(badlo|badhi):break
  lo=np.where(badlo,np.nextafter(lo,NEG),lo);hi=np.where(badhi,np.nextafter(hi,POS),hi)
 else:raise ArithmeticError('sqrt proposal not received')
 assert np.all((lo==0)|(up(lo*lo)<=a[0])) and np.all(down(hi*hi)>=a[1]);return lo,hi

def sum_axis(a,axis=0):
 lo=np.moveaxis(a[0],axis,0);hi=np.moveaxis(a[1],axis,0)
 while len(lo)>1:
  n=len(lo)//2;ll=down(lo[:2*n:2]+lo[1:2*n:2]);hh=up(hi[:2*n:2]+hi[1:2*n:2])
  if len(lo)%2:ll=np.concatenate((ll,lo[-1:]));hh=np.concatenate((hh,hi[-1:]))
  lo,hi=ll,hh
 return lo[0],hi[0]
def sl(a,key):return a[0][key],a[1][key]
def reshape(a,shape):return a[0].reshape(shape),a[1].reshape(shape)
def stack(a,axis=0):return np.stack([x[0]for x in a],axis),np.stack([x[1]for x in a],axis)
PI0=pi_interval();PI=box(PI0.lo,PI0.hi);HALFPI=mul(PI,rat(Q(1,2)))

def sinc_small(x):
 assert np.all(np.maximum(abs(x[0]),abs(x[1]))<=.8);xx=square(x);p=rat(Q((-1)**11,factorial(23)))
 for j in range(10,-1,-1):p=add(mul(p,xx),rat(Q((-1)**j,factorial(2*j+1))))
 e=Q(4,5)**24/factorial(25);return add(p,box(-e,e))

def sincos(x):
 # Integer selection need not be accurate: final residual domain is checked.
 k=np.rint((x[0]+x[1])/np.pi).astype(np.int64);r=sub(x,mul(exact(k),HALFPI));assert np.all(np.maximum(abs(r[0]),abs(r[1]))<=.8)
 xx=square(r);co=rat(Q((-1)**11,factorial(22)))
 for j in range(10,-1,-1):co=add(mul(co,xx),rat(Q((-1)**j,factorial(2*j))))
 e=Q(4,5)**24/factorial(24);co=add(co,box(-e,e));si=mul(r,sinc_small(r));kk=k%4
 so=(np.where(kk==0,si[0],np.where(kk==1,co[0],np.where(kk==2,-si[1],-co[1]))),np.where(kk==0,si[1],np.where(kk==1,co[1],np.where(kk==2,-si[0],-co[0]))))
 cc=(np.where(kk==0,co[0],np.where(kk==1,-si[1],np.where(kk==2,-co[1],si[0]))),np.where(kk==0,co[1],np.where(kk==1,-si[0],np.where(kk==2,-co[0],si[1]))))
 return so,cc

def cm(a,b):return sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0]))
def cpowers(x,n):
 si,co=sincos(x);one=exact(np.ones(np.broadcast_shapes(x[0].shape,x[1].shape)));zero=exact(np.zeros_like(one[0]));out=[(one,zero)]
 for k in range(n):out.append(cm(out[-1],(co,si)))
 ordered=[(out[k][0],neg(out[k][1]))for k in range(n,0,-1)]+out
 return stack([v[0]for v in ordered]),stack([v[1]for v in ordered])

class Fourier:
 def __init__(self,path=P/'vertex_weighted_exact_candidate.json'):
  self.path=Path(path);data=json.loads(self.path.read_text());terms=data['T'];self.n=max(max(map(abs,r['frequency']))for r in terms);n=self.n;lo=np.zeros((2*n+1,2*n+1));hi=lo.copy()
  for r in terms:
   k,l=r['frequency'];a=rat(Q(r['coefficient']));lo[k+n,l+n]=a[0];hi[k+n,l+n]=a[1]
  self.C=(lo,hi)
 def evaluate(self,a,b):
  # b has shape (m,) and a is (m,m) or (m,); output grid first axis a,
  # except Duffy a is indexed(t,s), b(t). Branch selected by rank.
  n=self.n;bp=cpowers(b,n);C=reshape(self.C,(2*n+1,2*n+1,1));cr=sum_axis(mul(C,sl(bp[0],(None,slice(None),slice(None)))),axis=1);ci=sum_axis(mul(C,sl(bp[1],(None,slice(None),slice(None)))),axis=1)
  ap=cpowers(a,n)
  if a[0].ndim==2:
   cc=(sl(cr,(slice(None),slice(None),None)),sl(ci,(slice(None),slice(None),None)));bb=sl(b,(slice(None),None))
  else:
   cc=(sl(cr,(slice(None),None,slice(None))),sl(ci,(slice(None),None,slice(None))));ap=(sl(ap[0],(slice(None),slice(None),None)),sl(ap[1],(slice(None),slice(None),None)));a=sl(a,(slice(None),None));bb=sl(b,(None,slice(None)))
  val=cm(ap,cc);T=sum_axis(val[0],0);im=sum_axis(val[1],0);assert np.all(im[0]<=0)and np.all(im[1]>=0)
  sa=sincos(a)[0];sb=sincos(bb)[0];sc=sincos(add(a,bb))[0];S=add(add(square(sa),square(sb)),square(sc));return mul(square(S),T)

def gauss_from_receipt(path):
 d=json.loads(Path(path).read_text());ns=[];ws=[]
 for r in d['Gauss_node_weight_receipts']:
  lo,hi=map(Q,r['Legendre_root']);ns.append(box((lo+1)/2,(hi+1)/2));lo,hi=map(Q,r['unit_interval_weight_outward']);ws.append(box(lo,hi))
 return stack(ns),stack(ws)

def integrate_duffy(candidate,nodes,weights,theta_a,theta_b,h,edge=0,fold=1):
 t=sl(nodes,(slice(None),None));s=sl(nodes,(None,slice(None)));w=sub(rat(1),mul(rat(2),s));hh=rat(h)
 if edge==0:v1,v2=mul(hh,w),hh
 elif edge==1:v1,v2=hh,mul(hh,w)
 elif edge==2:v1,v2=neg(mul(hh,w)),neg(hh)
 else:v1,v2=neg(hh),neg(mul(hh,w))
 # f evaluation assumes b depends t only. For horizontal sides swap source
 # a/b and evaluate transposed T by full direct workaround separately below.
 if edge in(1,3):raise NotImplementedError('swap Fourier matrix for horizontal Duffy edge')
 vs=add(v1,v2);x1=mul(mul(t,v1),rat(Q(1,2)));x2=mul(mul(t,v2),rat(Q(1,2)));x3=add(x1,x2);si1=sinc_small(x1);si2=sinc_small(x2);si3=sinc_small(x3)
 sa=sincos(theta_a)[0];sab=sincos(add(theta_a,theta_b))[0];sa1=sincos(add(theta_a,x1))[0];sb2,cb2=sincos(add(theta_b,x2));sab3=sincos(add(add(theta_a,theta_b),x3))[0]
 W1=neg(mul(v1,mul(sa1,si1)));W2=neg(mul(v2,mul(sb2,si2)));W3=neg(mul(vs,mul(sab3,si3)));qq=add(add(square(W1),square(W2)),square(W3));AA=add(neg(mul(sab,mul(v1,si1))),mul(sa,mul(vs,mul(cb2,si3))));BB=mul(sa,mul(vs,mul(sb2,si3)));nn=add(square(AA),square(BB));den=mul(qq,sqrt(qq));pre=div(rat(Q(fold)*2*Q(h)**2),mul(rat(8),PI));aa=add(theta_a,mul(t,v1));bb=add(theta_b,mul(t,v2));value=candidate.evaluate(aa,reshape(bb,(-1,)));integrand=mul(div(mul(pre,nn),den),value);weighted=mul(integrand,mul(sl(weights,(slice(None),None)),sl(weights,(None,slice(None)))));return sum_axis(sum_axis(weighted,0),0)
