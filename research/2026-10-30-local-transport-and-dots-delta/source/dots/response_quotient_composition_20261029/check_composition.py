import sympy as s, json
from pathlib import Path
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
P=[X,Y,Z]; lam=s.Rational(1,5)
def N(A,t):
 return s.trace(A)*(I+t*Z)/2+sum((s.trace(p*A)*lam*p/2 for p in P),s.zeros(2))
def nn(A,t):
 out=s.zeros(4)
 for i in range(2):
  for j in range(2):
   for k in range(2):
    for l in range(2):
     E=s.zeros(2);E[i,j]=1;F=s.zeros(2);F[k,l]=1
     out+=A[2*i+k,2*j+l]*s.kronecker_product(N(E,t),N(F,t))
 return out
V=s.zeros(4,2);V[0,0]=1;V[3,1]=1
K0=V.T; K1=s.zeros(2,4);K1[1,1]=1;K2=s.zeros(2,4);K2[1,2]=1
Ks=[K0,K1,K2];assert sum((k.H*k for k in Ks),s.zeros(4))==s.eye(4)
def R(A):return sum((k*A*k.H for k in Ks),s.zeros(2))
results=[]
for t,expected in [(s.S(0),s.Rational(8,25)),(s.Rational(4,5),s.Rational(9,25))]:
 ds=[nn(V*p*V.H,t) for p in P]
 norms=[sum(abs(e)*m for e,m in d.eigenvals().items()) for d in ds]
 values=[s.trace(p*R(d)) for p,d in zip(P,ds)]
 assert values==norms
 f=s.Rational(1,4)+sum(values)/8
 assert f==expected
 results.append({'t':str(t),'optimal_two_use_repetition_fidelity':str(f),'trace_norm_upper_bounds':[str(x) for x in norms]})
assert N(X,0)==N(X,s.Rational(4,5))
A=s.kronecker_product(X/2,I/2)
D=nn(A,0)-nn(A,s.Rational(4,5))
assert D==s.kronecker_product(X/10,-s.Rational(2,5)*Z)
results.append({'tensor_response_difference_trace_norm':str(sum(abs(e)*m for e,m in D.eigenvals().items()))})
Path(__file__).with_suffix('.json').write_text(json.dumps(results,indent=2)+'\n');print(results)
