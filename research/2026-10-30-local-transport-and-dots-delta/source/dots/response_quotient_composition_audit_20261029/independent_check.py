"""Independent Choi-first, exact arithmetic audit; no optimization numerics."""
import sympy as s, json
from pathlib import Path
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1); P=[X,Y,Z]
J0=s.Matrix([[3,0,0,1],[0,2,0,0],[0,0,2,0],[1,0,0,3]])/10
J1=s.Matrix([[5,0,0,1],[0,0,0,0],[0,0,4,0],[1,0,0,1]])/10

def channel(J,A):
 return s.Matrix(2,2,lambda a,b:2*sum(A[i,j]*J[2*i+a,2*j+b] for i in range(2) for j in range(2)))
def pt(J): return s.Matrix(4,4,lambda a,b:J[2*(a//2)+b%2,2*(b//2)+a%2])
def tn(A): return s.simplify(sum(abs(e)*mult for e,mult in A.eigenvals().items()))
def fe(C):
 bell=s.Matrix([1,0,0,1])/s.sqrt(2)
 return s.simplify((bell.H*C*bell)[0])
V=s.zeros(4,2);V[0,0]=V[3,1]=1
L=[V.T,s.zeros(2,4),s.zeros(2,4)];L[1][1,1]=1;L[2][1,2]=1
assert sum((l.H*l for l in L),s.zeros(4))==s.eye(4)
def recover(A):return sum((l*A*l.H for l in L),s.zeros(2))
def tensor_channel(J,A):
 out=s.zeros(4)
 for i in range(4):
  for j in range(4):
   E=s.zeros(2);F=s.zeros(2);E[i//2,j//2]=1;F[i%2,j%2]=1
   out+=A[i,j]*s.kronecker_product(channel(J,E),channel(J,F))
 return out
results=[]
for J,t,target in [(J0,s.S(0),s.Rational(8,25)),(J1,s.Rational(4,5),s.Rational(9,25))]:
 assert s.Matrix(2,2,lambda i,j:sum(J[2*i+a,2*j+a] for a in range(2)))==I/2
 assert all(e>=0 for e in J.eigenvals())
 assert channel(J,I/2)==(I+t*Z)/2
 assert all(channel(J,p)==p/5 for p in P)
 assert fe(J)==s.Rational(2,5)
 ds=[tensor_channel(J,V*p*V.H) for p in P]
 norms=[tn(d) for d in ds]
 assert norms==[s.Rational(2,25),s.Rational(2,25),2*(1+t)/5]
 assert [s.trace(p*recover(d)) for p,d in zip(P,ds)]==norms
 # Direct logical Choi construction, independent of the Pauli fidelity formula.
 JC=s.zeros(4)
 for i in range(2):
  for j in range(2):
   E=s.zeros(2);E[i,j]=1
   JC+=s.kronecker_product(E,recover(tensor_channel(J,V*E*V.H)))/2
 assert fe(JC)==target==s.Rational(1,4)+sum(norms)/8
 results.append({'t':str(t),'choi_spectrum':{str(e):m for e,m in J.eigenvals().items()},'partial_transpose_spectrum':{str(e):m for e,m in pt(J).eigenvals().items()},'single_use_optimum':'2/5','encoded_optimum':str(target),'direct_choi_overlap':str(fe(JC)),'response_norms':list(map(str,norms))})
# Independent explicit entanglement-breaking decomposition of first channel.
# 1/5 times each of the three Pauli measure/reprepare channels + 2/5 replacement.
for i in range(2):
 for j in range(2):
  A=s.zeros(2);A[i,j]=1
  deph=sum(((A+p*A*p)/2 for p in P),s.zeros(2))/5+2*s.trace(A)*I/10
  assert channel(J0,A)==deph
assert (2-s.sqrt(5))/10 in pt(J1).eigenvals()
# Tensor witness H=X/2 has unit trace norm; attain advertised s*background bound.
H=X/2; A=s.kronecker_product(H,I/2)
diff=tensor_channel(J0,A)-tensor_channel(J1,A)
assert diff==s.kronecker_product(X/10,-2*Z/5)
assert tn(diff)==s.Rational(4,25)==s.Rational(1,5)*tn(channel(J0,I/2)-channel(J1,I/2))
# Symbolic entire physical interpolation: Choi affine, CPTP by endpoint convexity.
t=s.symbols('t', real=True); J=J0+(5*t/4)*(J1-J0)
dz=s.simplify(tensor_channel(J,V*Z*V.H))
assert dz==s.diag((1+t)/5,-t/5,-t/5,-(1-t)/5)
assert s.simplify(tensor_channel(J,V*X*V.H))==V*X*V.H/25
assert s.simplify(tensor_channel(J,V*Y*V.H))==V*Y*V.H/25
out={'exact_cases':results,'entanglement_breaking_decomposition_matrix_units':4,'tensor_witness_trace_norm':'4/25','symbolic_interval':'0<=t<=4/5','symbolic_optimum':'8/25+t/20','scope':'Exact arithmetic; all-recovery upper bound is analytical unital-adjoint trace-norm bound. No capacity or optimized-encoder claim.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
