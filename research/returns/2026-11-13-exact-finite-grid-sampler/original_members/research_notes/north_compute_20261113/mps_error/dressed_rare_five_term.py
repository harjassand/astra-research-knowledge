"""Exact verification of a five-product-operator MPO for dressed rare Q."""
import sympy as s,itertools,json
from pathlib import Path
I=s.I;eta=(3+4*I)/5
out=[]
for n,edges,counts,pair in [(3,[(0,1),(1,2),(0,2)],[2,3,4],(0,1)),(4,[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],[1,2,3,4,5,6],(0,1))]:
 N=2**n
 def z(x,j):return 1-2*((x>>(n-1-j))&1)
 phase=[sum(c*z(x,u)*z(x,v) for (u,v),c in zip(edges,counts)) for x in range(N)]
 w=[s.expand(eta**e if e>=0 else s.conjugate(eta)**(-e)) for e in phase]
 W=s.diag(*w);XX=s.zeros(N);mask=sum(1<<(n-1-j) for j in pair)
 for x in range(N):XX[x^mask,x]=1
 direct=(W.conjugate().T*XX*W).applyfunc(s.expand)
 summed=s.zeros(N)
 for zu,zv in itertools.product([1,-1],repeat=2):
  factors=[];zs=dict(zip(pair,(zu,zv)))
  for j in range(n):
   if j in pair:
    factor=s.zeros(2);b=(1-zs[j])//2;factor[1-b,b]=1
   else:
    power=2*sum(c*zs[v if u==j else u] for (u,v),c in zip(edges,counts) if j in(u,v) and (v if u==j else u) in pair)
    x=s.expand(eta**power if power>=0 else s.conjugate(eta)**(-power));factor=s.diag(x,s.conjugate(x))
   factors.append(factor)
  summed+=s.kronecker_product(*factors)
 assert (direct-summed).applyfunc(s.expand)==s.zeros(N)
 V=s.Rational(12,13)*s.eye(N)-5*I*summed/13
 assert (V.conjugate().T*V-s.eye(N)).applyfunc(s.expand)==s.zeros(N)
 out.append(dict(n=n,edges=edges,counts=counts,pair=pair,exact_equality=True,exact_unitarity=True,product_terms=5,shared_neighbor_controls=True))
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
