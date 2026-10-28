"""Exact Marshall-positive minimal-rank factorization of the actual spin2 gate."""
import sys
sys.dont_write_bytecode=True
import sympy as S
from pathlib import Path
import json
D=5
BASE=Path(__file__).resolve().parents[1]

def spin():
 ms=list(range(-2,3));z=S.diag(*ms);p=S.zeros(D)
 for i,m in enumerate(ms[:-1]):p[i+1,i]=S.sqrt(6-m*(m+1))
 minus=p.T
 h=S.kronecker_product(z,z)-(S.kronecker_product(p,minus)+S.kronecker_product(minus,p))/2
 return ms,z,p,minus,h

def factors(delta):
 ms,z,p,minus,h=spin();d=S.sympify(delta);pairs=[];labels=[]
 # q0: quadratic Bernstein basis on m in[-2,2].
 for k in range(3):
  row=[];col=[]
  for m in ms:
   x=S.Rational(m+2,4);row.append([(1-x)**2,2*x*(1-x),x*x][k])
   P0=1+9*d*d-S.Rational(3,2)*d*d*m*m
   P1=-(d+d*d/4)*m;P2=S.Rational(3,4)*d*d*(m*m-2)
   col.append([P0-2*P1+4*P2,P0-4*P2,P0+2*P1+4*P2][k])
  pairs.append((S.diag(*row),S.diag(*col)));labels.append((0,k))
 # q+1 and q-1: exact rank2 positive endpoint interpolation.
 for q in (1,-1):
  for sign in (1,-1):
   L=S.zeros(D);R=S.zeros(D)
   for i,a in enumerate(ms):
    ap=a+q
    if ap not in ms:continue
    j=ms.index(ap);ladder=S.sqrt(6-a*ap);x=a+S.Rational(q,2)
    L[j,i]=ladder*(1+sign*x/S.Rational(3,2))
   for i,b in enumerate(ms):
    bp=b-q
    if bp not in ms:continue
    j=ms.index(bp);ladder=S.sqrt(6-b*bp);y=b-S.Rational(q,2)
    R[j,i]=d*S.Rational(1,4)*ladder*(1+d/4-sign*d*S.Rational(3,2)*y)
   pairs.append((L,R));labels.append((q,sign))
 # q+2 and q-2: rank1, two successive spin-flips.
 for q in (2,-2):
  left=p*p if q==2 else minus*minus
  right=minus*minus if q==2 else p*p
  pairs.append((left,d*d*right/8));labels.append((q,0))
 actual=S.eye(D*D)-d*h+d*d*h*h/2
 reconstructed=sum((S.kronecker_product(a,b) for a,b in pairs),S.zeros(D*D))
 assert S.simplify(actual-reconstructed)==S.zeros(D*D)
 return pairs,labels,actual,h


def run():
 d=S.symbols('delta',nonnegative=True);pairs,labels,G,h=factors(d)
 # Entrywise positivity is proved in the note for0<=delta<=1/2.
 for value in (S.Rational(1,1000),S.Rational(1,2)):
  pp,ll,gg,hh=factors(value)
  assert all(x>=0 for a,b in pp for x in list(a)+list(b))
 ranks={}
 for q in (-2,-1,0,1,2):
  ms=range(-2,3);rows=[(a+q,a) for a in ms if -2<=a+q<=2];cols=[(b-q,b) for b in ms if -2<=b-q<=2]
  M=S.Matrix([[G[5*(ap+2)+(bp+2),5*(a+2)+(b+2)] for bp,b in cols] for ap,a in rows])
  ranks[str(q)]=M.subs(d,S.Rational(1,1000)).rank()
 assert sum(ranks.values())==9
 out=dict(delta_domain='0<=delta<=1/2',exact_factor_terms=len(pairs),magnetization_block_ranks=ranks,
  operator_schmidt_rank_at_delta001=9,nonnegative_rank=9,
  statement='Actual Marshall-gauged quadratic spin2 Gibbs gate; exact nonnegative factorization, no noise or gate modification.',
  spectrum_hbond={str(k):v for k,v in h.eigenvals().items()})
 (BASE/'results/POSITIVE_GATE.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
 return pairs,labels,G,h

if __name__=='__main__':run()
