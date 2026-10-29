"""Exact rational intertwining test, not a threshold or hardware simulation."""
from pathlib import Path
import sympy as s,json,hashlib
P=Path(__file__); I=s.eye
kron=s.kronecker_product
z=s.zeros
# two data qubits, path-overlap boxes0--1--2
A=[s.diag(1,s.Rational(4,5)),s.Matrix([[0,s.Rational(3,5)],[0,0]])]
B=[s.diag(1,s.Rational(3,5)),s.Matrix([[0,s.Rational(4,5)],[0,0]])]
C=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
Ks=[[kron(k,I(2)) for k in A],[C],[kron(I(2),k) for k in B]]
dims=[3,2,3];Da=18;D=72
sets=[(),(0,),(1,),(2,),(0,2)];index={a:i for i,a in enumerate(sets)}
nei=[[1],[0,2],[1]]
def ketbra(d,a,b):
 M=z(d);M[a,b]=1;return M
def ancop(x,m,guard=False):
 return kron(*[m if j==x else (ketbra(d,0,0) if guard and j in nei[x] else I(d)) for j,d in enumerate(dims)])
V=[];Hg=z(D);Hu=z(D)
for x,kk in enumerate(Ks):
 vv=sum((kron(k,ancop(x,ketbra(dims[x],r+1,0))) for r,k in enumerate(kk)),z(D))
 vg=sum((kron(k,ancop(x,ketbra(dims[x],r+1,0),True)) for r,k in enumerate(kk)),z(D))
 V.append(vv);Hg+=vg+vg.T;Hu+=vv+vv.T
ready=kron(*[s.eye(d)[:,0] for d in dims]);W0=kron(I(4),ready)
blocks=[]
for S in sets:
 w=W0
 for x in S:w=V[x]*w
 blocks.append(w)
W=s.Matrix.hstack(*blocks);hc=z(len(sets));low=[]
for x in range(3):
 a=z(len(sets))
 for S in sets:
  if x in S:a[index[tuple(j for j in S if j!=x)],index[S]]=1
 low.append(a);hc+=a+a.T
Hc=kron(hc,I(4))
checks={'isometry':W.T*W==I(W.cols),'hamiltonian_intertwining':Hg*W==W*Hc,
 'unguarded_residual_nonzero':Hu*W!=W*Hc}
jn=[];no=z(D);ne=z(W.cols)
for x,kk in enumerate(Ks):
 for r,k in enumerate(kk):
  L=kron(I(4),ancop(x,ketbra(dims[x],0,r+1)));Le=kron(low[x],k)
  jn.append(L*W==W*Le);no+=L.T*L;ne+=Le.T*Le
checks['every_emission_intertwines']=all(jn)
checks['total_no_jump_intertwines']=no*W==W*ne
checks['single_kraus_no_jump_need_not_intertwine']=any((kron(I(4),ancop(x,ketbra(dims[x],r+1,r+1)))*W != W*(kron(low[x].T*low[x],k.T*k))) for x,kk in enumerate(Ks) for r,k in enumerate(kk))
out={'status':'exact finite intertwining only','physical_dimension':D,'logical_clock_dimension':len(sets),'logical_data_dimension':4,'checks':checks,'source_sha256':hashlib.sha256(P.read_bytes()).hexdigest()}
assert all(checks.values());P.with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
