"""Exact monomial gauge check on actual five-qubit seed; finite thermal check."""
import itertools,json
import numpy as np
from scipy.special import logsumexp
from functools import reduce
I=np.eye(2); X=np.array([[0.,1.],[1.,0.]]); Z=np.diag([1.,-1.])
checks=[('X',[0,1,4]),('X',[2,3,4]),('Z',[0,2,4]),('Z',[1,3,4])]
P=[[reduce(np.kron,[(X if kind=='X' else Z) if k==j else I for k in range(5)]) for j in sites] for kind,sites in checks]
D=np.eye(32); S=[reduce(np.matmul,p) for p in P]
configs=list(itertools.product(range(3),repeat=4)); ix={c:i for i,c in enumerate(configs)}
U={}
for c in configs:
 u=D.copy()
 for a,q in enumerate(c):
  for j in range(q): u=u@P[a][j]
 U[c]=u
edges=[]; residual=0
for c in configs:
 for a,q in enumerate(c):
  v=list(c);v[a]=(q+1)%3;v=tuple(v)
  h=U[v].T@P[a][q]@U[c]
  target=S[a] if q==2 else D
  phase=np.trace(target.T@h)/32
  residual=max(residual,float(np.linalg.norm(h-phase*target)))
  assert abs(abs(phase)-1)<1e-12
  edges.append((ix[c],ix[v],a,q==2,float(phase)))
assert residual==0
records=[]
for delta in [20.,100.,1000.]:
 beta=2.;g=(delta**2/4.)**(1/3)
 vals={}
 for s in itertools.product([-1,1],repeat=4):
  H=np.diag([delta*sum(q!=0 for q in c) for c in configs])
  for i,j,a,wrap,phase in edges:
   v=-g*phase*(s[a] if wrap else 1);H[i,j]+=v;H[j,i]+=v
  ev=np.linalg.eigvalsh(H)
  vals[s]=-logsumexp(-beta*ev)/beta
 coeff={str(mask):sum(f*np.prod([s[a] for a in range(4) if mask>>a&1]) for s,f in vals.items())/16 for mask in range(1,16)}
 records.append(dict(delta=delta,g=g,ratio=g/delta,beta=beta,walsh_coefficients=coeff,max_cross=max(abs(v) for m,v in coeff.items() if int(m).bit_count()>1)))
r=dict(scope='Actual five-qubit seed only. Exact gauge algebra plus finite numerical thermodynamics; not a family proof.',gauge_residual=residual,clock_configurations=81,directed_edges=len(edges),results=records)
print(json.dumps(r,indent=2))
open(__file__.replace('.py','.json'),'w').write(json.dumps(r,indent=2)+'\n')
