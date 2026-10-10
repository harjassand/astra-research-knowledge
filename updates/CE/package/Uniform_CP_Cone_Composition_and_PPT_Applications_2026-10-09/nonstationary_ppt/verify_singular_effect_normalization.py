"""Exact rational/radical checks of support-completed backwards normalization."""
from pathlib import Path
import json
import sympy as s
d=3; I=s.eye(d); zero=s.zeros(d)
def units():
 for i in range(d):
  for j in range(d):
   e=s.zeros(d);e[i,j]=1;yield e
E=list(units())
def act(K,X):return sum((k*X*k.H for k in K),s.zeros(d))
def adj(K,X):return sum((k.H*X*k for k in K),s.zeros(d))
def simple(M):return M.applyfunc(s.simplify)
def iszero(M):return simple(M)==zero
P=[s.diag(1,0,2),s.diag(0,1,1),s.diag(1,1,0)]
Q=[s.diag(1,2,0),s.diag(1,1,1),s.diag(0,1,2)]
# D + (1/4)id is PPT: its partially transposed Choi is I+(1/4)swap>0.
base=[I/2]+E
K=[[q*k*p for k in base] for p,q in zip(P,Q)]
Y=[None]*4;Y[3]=I
for j in range(2,-1,-1):Y[j]=adj(K[j],Y[j+1])
Theta=[];S=[];ranks=[]
for j in range(3):
 y0,y1=Y[j],Y[j+1]
 assert y0.is_diagonal() and y1.is_diagonal()
 support=s.diag(*[int(y0[i,i]!=0) for i in range(d)])
 b=s.diag(*[1/s.sqrt(y0[i,i]) if y0[i,i]!=0 else 0 for i in range(d)])
 sy0=s.diag(*[s.sqrt(y0[i,i]) for i in range(d)])
 sy1=s.diag(*[s.sqrt(y1[i,i]) for i in range(d)])
 L=[sy1*k*b for k in K[j]]
 for a in range(d):
  for c in range(d):
   if support[c,c]==0:
    z=s.zeros(d);z[a,c]=1/s.sqrt(d);L.append(z)
 assert iszero(adj(L,I)-I)
 for e in E:
  assert iszero(act(L,sy0*e*sy0)-sy1*act(K[j],e)*sy1)
 Theta.append(L);S.append(sy0);ranks.append(int(y0.rank()))
for e in E:
 lhs=e;rhs=S[0]*e*S[0]
 for j in range(3):
  lhs=act(K[j],lhs);rhs=act(Theta[j],rhs)
 assert iszero(lhs-rhs)
# Include a genuinely zero intermediate effect, handled by the completion alone.
Kzero=[s.zeros(d)]
assert adj(Kzero,I)==zero
replacement=[e/s.sqrt(d) for e in E]
assert iszero(adj(replacement,I)-I)
for e in E:assert act(replacement,zero*e*zero)==act(Kzero,e)==zero
report={'status':'PASS','arithmetic':'Exact SymPy rational and radical expressions','dimension':d,'factors':3,'backwards_effect_ranks':ranks+[d],'local_matrix_unit_identities':3*d*d,'global_matrix_unit_identities':d*d,'zero_effect_identities':d*d,'trace_preserving_completions':4,'scope':'Exact identities for singular support-completed normalization; not a computation of exponential constants.'}
Path(__file__).with_name('singular_effect_normalization_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
