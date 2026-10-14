"""Exact reconstruction of a rational closed profile cycle; no floating gradients.
The JSON input records Fourier coefficients, durations, and the rank-one-convex
integrand G is written below. SymPy QQ(i) polynomial arithmetic is used.
"""
from pathlib import Path
import json,sys
from functools import lru_cache
import sympy as S
from sympy.polys.domains import QQ,QQ_I
ROOT=Path(__file__).resolve().parent
Z=QQ_I.zero;ONE=QQ_I.one;ii=QQ_I.dtype(0,1)
def rat(x):return QQ.convert(S.Rational(str(x)))
def gr(a,b=0):return QQ_I.dtype(rat(a),rat(b))
def conj(a):return QQ_I.dtype(a.x,-a.y)
def add(a,b):
 d=a.copy()
 for k,v in b.items():d[k]=d.get(k,Z)+v
 return {k:v for k,v in d.items() if v!=Z}
def scale(a,c):return {k:v*c for k,v in a.items() if v*c!=Z}
def mul(a,b):
 d={}
 for (t,n),v in a.items():
  for (s,m),w in b.items():
   k=t+s,n+m;d[k]=d.get(k,Z)+v*w
 return {k:v for k,v in d.items() if v!=Z}
def reim(c):
 cc={(t,-n):conj(v) for (t,n),v in c.items()}
 return scale(add(c,cc),gr('1/2')),scale(add(c,scale(cc,gr(-1))),-ii/2)
def avg(a):
 v=sum((c/gr(t+1) for (t,n),c in a.items() if n==0),Z)
 assert v.y==0
 return S.Rational(str(v.x))

def reconstruct(d):
 ns=d['frequencies'];nodes=d['nodes'];widths=[S.Rational(t) for t in d['widths']]
 aa,bb,cc,dd=x=S.symbols('a b c d',real=True)
 u=aa*aa+cc*cc;v=bb*bb+dd*dd;q=aa*dd-bb*cc
 F=3*(u+v-2*q)**2+S.Rational(35,24)*u*u+q*q-S.Rational(5,2)*q*u
 norm=(u+v)**2
 df=S.Matrix([S.diff(F,z) for z in x]);hess=S.hessian(F,x)
 needed=[F,norm]+list(df)+list(hess)+list(S.Matrix(x)*S.Matrix(x).T)+list(x)+[q]
 polys=[S.Poly(p,*x) for p in needed]
 totals=[S.Rational(0) for _ in needed]
 for e,width in enumerate(widths):
  a0={(0,n):gr(*c) for n,c in zip(ns,nodes[e]) if c!=['0','0']}
  a1={(0,n):gr(*c) for n,c in zip(ns,nodes[(e+1)%len(nodes)]) if c!=['0','0']}
  dv=scale(add(a1,scale(a0,gr(-1))),gr(1)/gr(str(width)))
  py0={(0,n):ii*n*c for (_,n),c in a0.items() if n}
  pyd=add({(0,n):ii*n*c for (_,n),c in a1.items() if n},scale(py0,gr(-1)))
  py=add(py0,{(1,n):c for (_,n),c in pyd.items()})
  da,dc=reim(dv);db,dd=reim(py);entries=[da,db,dc,dd]
  @lru_cache(None)
  def mp(ex):
   if sum(ex)==0:return {(0,0):ONE}
   j=next(i for i,z in enumerate(ex) if z);pr=list(ex);pr[j]-=1
   return mul(mp(tuple(pr)),entries[j])
  for i,p in enumerate(polys):
   totals[i]+=width*sum(co*avg(mp(ex)) for ex,co in p.terms())
  print('edge',e+1,'/',len(widths),'exact',flush=True)
 period=sum(widths);totals=[v/period for v in totals]
 c,n4=totals[:2];b=S.Matrix(totals[2:6]);H=S.Matrix(4,4,totals[6:22]);C=S.Matrix(4,4,totals[22:38]);mean=S.Matrix(totals[38:42]);det=totals[42]
 assert mean==S.zeros(4,1) and det==0
 assert all(H[:j,:j].det()>0 for j in range(1,5))
 assert all(C[:j,:j].det()>0 for j in range(1,5))
 B=-H.inv()*b;gap=c+b.dot(B)+S.Rational(1,2)*(B.T*H*B)[0];ratio=S.factor(gap/n4)
 return dict(period=str(period),c=str(c),n4=str(n4),H=[[str(z) for z in H.row(i)] for i in range(4)],b=[str(z) for z in b],B_opt=[str(z) for z in B],gap=str(gap),ratio=str(ratio),ratio_decimal=str(S.N(ratio,22)),mean_zero=True,determinant_mean_zero=True,H_positive_definite=True,C_positive_definite=True)
if __name__=='__main__':
 p=ROOT/'rational_free_cycle.json'
 if '--from-search' in sys.argv:
  raw=json.load(open(ROOT/'exploration/free_cycles_N3_K5.json'))
  best=min(raw,key=lambda d:d['ratio']);N=best['N'];den=10**6
  fmt=lambda x:str(S.Rational(round(float(x)*den),den))
  d=dict(frequencies=list(range(-N,N+1)),nodes=[[[fmt(a),fmt(b)] for a,b in row] for row in best['nodes']],widths=[fmt(t) for t in best['tau']],source='rounded best retained G free-time five-profile cycle; exact timings below are rational, not certified optimal')
  json.dump(d,open(p,'w'),indent=2)
 else:d=json.load(open(p))
 r=reconstruct(d)
 exact_ratio=S.Rational(r['ratio'])
 assert S.Rational(19,20)<exact_ratio<S.Rational(24,25)
 r['certified_lower_bound']='19/20'
 r['certified_upper_bound']='24/25'
 json.dump(r,open(ROOT/'rational_free_cycle_verification.json','w'),indent=2)
 print('EXACT positive ratio',r['ratio_decimal'])
