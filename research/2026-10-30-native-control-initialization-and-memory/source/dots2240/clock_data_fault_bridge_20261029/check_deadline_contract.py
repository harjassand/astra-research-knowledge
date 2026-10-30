"""Exact finite checks: single-shot amplitude-damping channel cell and Boolean hyperedge bookkeeping."""
import sympy as s,itertools,json
from pathlib import Path
I=s.eye; K=[s.diag(1,s.Rational(3,5)),s.Matrix([[0,s.Rational(4,5)],[0,0]])]
m=4;d=2;n=d*m
basis=lambda j:s.eye(m)[:,j]
e=lambda i,j:basis(i)*basis(j).T
k=s.kronecker_product
V=sum((k(K[r],e(r+1,0)) for r in range(2)),s.zeros(n))
H=V+V.T
J=[k(I(d),e(3,r+1)) for r in range(2)]
W0=k(I(d),basis(0));W1=V*W0;WD=k(I(d),basis(3))
checks={'kraus_complete':sum((a.T*a for a in K),s.zeros(d))==I(d),'ready_to_bundled':H*W0==W1,'bundled_to_ready':H*W1==W0,'done_dark':H*WD==s.zeros(n,d),'terminal_total_loss':sum((j.T*j for j in J),s.zeros(n))*W1==W1,'terminal_kraus_semantics':all(J[r]*W1==WD*K[r] for r in range(2))}
# Fixed triangle hypergraph; all marked subsets, all Boolean insertion sets.
edges=[{0,1},{1,2},{2,3},{0},{3}];b=max(map(len,edges));D=max(sum(v in e for e in edges) for v in range(4))
poly_ok=degree_ok=count_ok=True
for mask in range(1,16):
 S={i for i in range(4) if mask>>i&1};poly={frozenset():1};raw=1
 for j in S:
  inc=[i for i,e in enumerate(edges) if j in e];terms=[]
  for z in range(1,1<<len(inc)):
   T=frozenset(inc[t] for t in range(len(inc)) if z>>t&1);terms.append((T,(-1)**(len(T)+1)))
  raw*=len(terms);out={}
  for T,c in poly.items():
   for U,a in terms: out[T|U]=out.get(T|U,0)+c*a
  poly={T:c for T,c in out.items() if c};
 degree_ok &= all(len(T)*b>=len(S) for T in poly)
 count_ok &= sum(abs(c) for c in poly.values())<=raw<=(2**D-1)**len(S)
 for xx in range(1<<len(edges)):
  active={i for i in range(len(edges)) if xx>>i&1}
  val=sum(c for T,c in poly.items() if T<=active)
  truth=all(any(j in edges[i] for i in active) for j in S)
  poly_ok &= val==truth
checks.update(coverage_polynomial_exact=poly_ok,coverage_degree_bound=degree_ok,coverage_coefficient_bound=count_ok)
assert all(checks.values())
out={'checks':checks,'scope':'Exact isolated channel-cell algebra and finite hypergraph polynomial checks; general fault norm and completion-tail proofs are in companion documents.'}
Path('producer-workspace/check_deadline_contract.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
