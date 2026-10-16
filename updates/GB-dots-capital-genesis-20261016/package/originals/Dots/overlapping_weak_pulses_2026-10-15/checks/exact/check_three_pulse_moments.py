"""Exact noncommuting shared-bath stress test, not proof of general lemma."""
import sympy as s, itertools, json
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
# Three disjoint memory qubits, each coupled via X_i to same bath qubit.
# Interleaving A,B,C,A,B,C; every pulse holds its own private Z_i frame.
segments=[(0,X,s.Rational(1,20)),(1,Z,s.Rational(1,19)),(2,Y,s.Rational(1,18)),(0,Z,s.Rational(-1,20)),(1,Y,s.Rational(-1,19)),(2,X,s.Rational(-1,18))]
B={j:s.zeros(2) for j in range(8)}; B[0]=I
upper=[s.Rational(0)]*3
for i,P,t in segments:
 c=(1-t*t)/(1+t*t); v=2*t/(1+t*t)
 B={mask:s.simplify(c*B[mask]-s.I*v*P*B[mask^(1<<i)]) for mask in range(8)}
 upper[i]+=2*abs(t) # |angle|=2atan|t| <=2|t|
effects={m:s.simplify(b.conjugate().T*b) for m,b in B.items()}
assert s.simplify(sum(effects.values(),s.zeros(2)))==I
results=[]
for size in range(1,4):
 for subset in itertools.combinations(range(3),size):
  mask=sum(1<<i for i in subset)
  E=s.simplify(sum((e for m,e in effects.items() if m&mask==mask),s.zeros(2)))
  bound=s.prod(upper[i]**2 for i in subset)
  gap=s.simplify(bound*I-E)
  assert gap==gap.conjugate().T
  assert gap[0,0]>=0 and gap[1,1]>=0 and gap.det()>=0
  results.append({'subset':subset,'bound':str(bound),'gap_determinant_positive':bool(gap.det()>0)})
print(json.dumps({'PASS':True,'exact_normalization':True,'subset_checks':results},indent=2))
