"""Rational continuous-domain design checks from certified residual jets."""
from fractions import Fraction as F
import math,json,argparse
from pathlib import Path

def ev(c,x):
 ans=F()
 for a in c[::-1]:ans=ans*x+a
 return ans

def diff(c,k=1):
 for _ in range(k):c=[(i+1)*c[i+1] for i in range(len(c)-1)]
 return c

def bernstein(c,a,b):
 n=len(c)-1;h=b-a
 d=[h**i*sum((c[j]*math.comb(j,i)*a**(j-i) for j in range(i,n+1)),F()) for i in range(n+1)]
 bb=[sum((d[i]*F(math.comb(k,i),math.comb(n,i)) for i in range(k+1)),F()) for k in range(n+1)]
 return min(bb),max(bb)

def residual_bounds(Q,a,b):
 h=max(abs(a),abs(b))
 return [sum((Q[j]*h**(j-k)/math.factorial(j-k) for j in range(k,len(Q))),F()) for k in range(len(Q))]

def error_jet(Q,k,w=F(1)):
 return 4*sum((F(math.factorial(k),math.factorial(a)*math.factorial(b))*Q[a]*Q[b]*w**(k-a-b) for a in range(k+1) for b in range(k-a+1)),F())

def interval(rec,left,right,k=1):
 c=list(map(F,rec['corrected_D_polynomial_exact']));q=list(map(F,rec['residual_norm_upper_exact']));ctr=F(rec['parameters']['V'])
 a=F(left)-ctr;b=F(right)-ctr
 lo,hi=bernstein(diff(c,k),a,b);e=error_jet(residual_bounds(q,a,b),k)
 return lo-e,hi+e

def main(file):
 rec=json.loads(Path(file).read_text());ctr=F(rec['parameters']['V']);out=[]
 for a,b in [(F(2),F(19,8)),(F(15,8),F(21,8)),(F(7,4),F(11,4)),(F(2),F(5,2))]:
  lo,hi=interval(rec,a,b,2);mu=-hi
  er=F(rec['D_jet_radii_exact'][1]);g=abs(F(rec['corrected_D_derivatives_exact'][1]))+er
  x=dict(I=[str(a),str(b)],curvature=[float(lo),float(hi)],mu=float(mu),g_bound=float(g))
  if mu>0:
   x.update(regret_exact=str(g*g/(2*mu)),regret_float=float(g*g/(2*mu)),root_radius=float(g/mu))
  out.append(x)
 print(json.dumps(out,indent=2))
 Path(file).with_name('local_design_diagnostics.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('file');a=p.parse_args();main(a.file)

def gram_q_bounds(rec,left,right):
 from jet_certificate import sqrt_upper
 GO=[[F(a) for a in r] for r in rec['residual_odd_gram_exact']]
 GE=[[F(a) for a in r] for r in rec['residual_even_gram_exact']]
 H=[[a+b for a,b in zip(u,v)] for u,v in zip(GO,GE)];n=len(H)
 ctr=F(rec['parameters']['V']);aa=F(left)-ctr;bb=F(right)-ctr
 Q=[]
 for k in range(n):
  coeff=[F() for _ in range(2*(n-k)-1)]
  for i in range(k,n):
   for j in range(k,n):coeff[i+j-2*k]+=H[i][j]/(math.factorial(i-k)*math.factorial(j-k))
  lo,hi=bernstein(coeff,aa,bb)
  if hi<0:raise ValueError('negative norm polynomial upper')
  Q.append(sqrt_upper(hi))
 return Q

def tight_interval(rec,left,right,k=1):
 c=list(map(F,rec['corrected_D_polynomial_exact']));ctr=F(rec['parameters']['V'])
 lo,hi=bernstein(diff(c,k),F(left)-ctr,F(right)-ctr)
 e=error_jet(gram_q_bounds(rec,left,right),k)
 return lo-e,hi+e
