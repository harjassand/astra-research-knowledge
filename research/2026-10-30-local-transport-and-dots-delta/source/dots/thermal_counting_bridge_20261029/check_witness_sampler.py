import sympy as s,json
from itertools import product
from pathlib import Path
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P={'X':X,'Y':Y,'Z':Z}
def embed(a,j):return s.kronecker_product(a,I) if j==0 else s.kronecker_product(I,a)
G=[2*s.eye(4)-embed(X,0),2*s.eye(4)-embed(Y,1),2*s.eye(4)-s.kronecker_product(Z,Z)]
word=G+list(reversed(G));word=word*2
A=s.eye(4)
for g in word:A=g*A
A=s.simplify(A);normal=s.trace(A);assert normal>0
rho=A/normal

def phase_counts(word):
 d=word[0].rows;T=s.eye(4*d)
 for g in word:
  U=s.zeros(4*d)
  for i,j,p in product(range(d),range(d),range(4)):
   for v,q in [(s.re(g[j,i]),0),(s.im(g[j,i]),1)]:
    v=int(v)
    if v:U[((p+q+(2 if v<0 else 0))%4)*d+j,p*d+i]+=abs(v)
  T=U*T
 return [sum(int(T[p*d+i,i]) for i in range(d)) for p in range(4)]

records=[]
for bases in product('XYZ',repeat=2):
 probs=[]
 for signs in product([1,-1],repeat=2):
  effects=[embed(I+signs[j]*P[bases[j]],j) for j in range(2)] # denom2 each
  counts=phase_counts(word+effects)
  z=s.Rational(counts[0]-counts[2],4)
  true=s.simplify(s.trace(effects[1]*effects[0]*A)/4)
  assert z==true and z>=0 and counts[1]==counts[3]
  probs.append(z/normal)
 assert sum(probs)==1
 # Prefix conservation and exact conditional probabilities.
 for a in [1,-1]:
  effect=embed(I+a*P[bases[0]],0)
  cnt=phase_counts(word+[effect]);prefix=s.Rational(cnt[0]-cnt[2],2)/normal
  children=sum(probs[i] for i,sg in enumerate(product([1,-1],repeat=2)) if sg[0]==a)
  assert prefix==children
 records.append({'bases':''.join(bases),'probabilities':[str(p) for p in probs]})
out={'normalization_numerator':str(normal),'density_matrix':str(rho),'basis_settings':9,'joint_outcomes_checked':36,'prefix_conservation_checks':18,'records':records,'scope':'Exact phase-count and dense-matrix checks of rational witness product-Pauli sampling; no true-Gibbs TV or hardware claim.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
