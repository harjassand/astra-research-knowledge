#!/usr/bin/env python3
"""Exact rational interval-Bernstein check for all translated W_a backgrounds.
The only numerical inputs are already outward-certified moment endpoints.
No parameter/background sampling is used by this proof.
"""
from fractions import Fraction as F
from math import comb
import json, sys
class I:
 def __init__(self,a=0,b=None): self.l=F(a);self.h=F(a if b is None else b);assert self.l<=self.h
 def __add__(self,o):
  o=iv(o);return I(self.l+o.l,self.h+o.h)
 __radd__=__add__
 def __neg__(self):return I(-self.h,-self.l)
 def __sub__(self,o):return self+-iv(o)
 def __rsub__(self,o):return iv(o)+-self
 def __mul__(self,o):
  if isinstance(o,P):return o*self
  o=iv(o);p=[self.l*o.l,self.l*o.h,self.h*o.l,self.h*o.h];return I(min(p),max(p))
 __rmul__=__mul__
 def __truediv__(self,o):
  o=iv(o);assert o.l>0 or o.h<0;return self*I(1/o.h,1/o.l)
 def __repr__(self):return f'I({float(self.l)},{float(self.h)})'
def iv(a):return a if isinstance(a,I) else I(a)
class P:
 # Bernstein coefficients on x in[0,1], with a=2x-1.
 def __init__(self,co):self.c=[iv(x) for x in co]
 @property
 def n(self):return len(self.c)-1
 def elevate(self,n):
  co=self.c[:];m=self.n
  while m<n:
   co=[co[0]]+[F(i,m+1)*co[i-1]+F(m+1-i,m+1)*co[i] for i in range(1,m+1)]+[co[-1]];m+=1
  return P(co)
 def __add__(self,o):
  o=poly(o);n=max(self.n,o.n);return P([a+b for a,b in zip(self.elevate(n).c,o.elevate(n).c)])
 __radd__=__add__
 def __neg__(self):return P([-x for x in self.c])
 def __sub__(self,o):return self+-poly(o)
 def __rsub__(self,o):return poly(o)+-self
 def __mul__(self,o):
  o=poly(o);m=self.n;n=o.n
  return P([sum((self.c[i]*o.c[k-i]*F(comb(m,i)*comb(n,k-i),comb(m+n,k)) for i in range(max(0,k-n),min(m,k)+1)),I()) for k in range(m+n+1)])
 __rmul__=__mul__
def poly(x):return x if isinstance(x,P) else P([x])
def interval_json(x):return {'lower_exact':str(x.l),'upper_exact':str(x.h),'lower_float':float(x.l),'upper_float':float(x.h)}
def run(moment_path,delta=F(1)):
 raw=json.load(open(moment_path));mom=raw.get('moments',raw)
 def fetch(key):
  v=mom[key]
  if 'lower_hex' in v:return I(F.from_float(float.fromhex(v['lower_hex'])),F.from_float(float.fromhex(v['upper_hex'])))
  return I(F.from_float(v['lower']),F.from_float(v['upper']))
 sig=fetch('s');m1=fetch('m1');m2=fetch('m2');m3=[fetch('m3_1'),fetch('m3_2')];m4=[fetch('m4_1'),fetch('m4_2')]
 A4=fetch('A4')-F(81,22400);B4=fetch('B4')-F(51,22400);C4=fetch('C4')-F(57,22400)
 # Signed lower-bound moment functional: nu1 -(1/30)ball +(1/30)delta0.
 base=F(99,200);m=F(3,2)*base-F(25,4)*sig
 M=[[base/2-F(9,4)*sig,3*sig],[3*sig,base-4*sig]];c=[F(15,4)*sig,base-5*sig]
 a=P([-1,1]);one=poly(1);al=P([0,-4,16]);be=P([0,24,0]);ga=P([16,-4,0])
 k=al*A4+be*B4+ga*C4-delta
 L=(3*a+1)*m1+3*(1-a)*m2
 N=[3*(1+a)*m3[i]-(3*a-1)*m4[i] for i in range(2)]
 E=[[poly(2*m*m if i==j else 0)-(3*a-1)*m*M[i][j]-3*(1-a)*c[i]*c[j] for j in range(2)] for i in range(2)]
 v=[m*N[i]-L*c[i] for i in range(2)]
 det=E[0][0]*E[1][1]-E[0][1]*E[1][0]
 adjform=v[0]*v[0]*E[1][1]-2*v[0]*v[1]*E[0][1]+v[1]*v[1]*E[0][0]
 numerator=(3*m*k-2*L*L)*det-6*(1-a)*adjform
 assert numerator.n==4
 out={'moment_file':moment_path,'lower_gap_target':str(delta),'method':'exact rational interval Bernstein coefficients on a in[-1,1]; all backgrounds eliminated algebraically','s_interval':interval_json(sig),'proxy_m_interval':interval_json(m),'bernstein_coefficients':[interval_json(x) for x in numerator.c],'all_positive':all(x.l>0 for x in numerator.c)}
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':
 out=run(sys.argv[1],F(sys.argv[2]) if len(sys.argv)>2 else F(1))
 if len(sys.argv)>3:open(sys.argv[3],'w').write(json.dumps(out,indent=2)+'\n')
 assert out['all_positive'], 'Moment box did not certify all Bernstein coefficients.'
