"""Independent exact matrix reconstruction; does not import author's code.
The generator is assembled using Bloch derivatives and a compact drift.
"""
from pathlib import Path
import json,time
import sympy as S
st=time.monotonic()
I=S.eye(2);pauli=[S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-S.I],[S.I,0]]),S.diag(1,-1)]
R=S.Rational
m=S.Matrix([R(1,7),R(-2,9),R(1,11)])
C=S.Matrix([[R(3),R(1,5),R(-1,7)],[R(1,5),R(2),R(1,9)],[R(-1,7),R(1,9),R(5,2)]])
b=S.Matrix([R(1,3),R(-2,5),R(1,7)])
P=S.eye(3)-m*m.T
cross=S.Matrix([[0,-m[2],m[1]],[m[2],0,-m[0]],[-m[1],m[0],0]])
D=P*C*P-cross*C*cross.T
def tensor(factors):
 a=S.ones(1,1)
 for f in factors:a=S.kronecker_product(a,f)
 return a
records=[]
for N in [1,2,3]:
 q=(I+sum((m[i]*pauli[i] for i in range(3)),S.zeros(2)))/2
 k=tensor([q]*N)
 grad=[];hess=[];J=[]
 for a in range(3):
  grad.append(sum((tensor([pauli[a]/2 if j==i else q for j in range(N)]) for i in range(N)),S.zeros(2**N)))
  J.append(sum((tensor([pauli[a]/2 if j==i else I for j in range(N)]) for i in range(N)),S.zeros(2**N)))
 for a in range(3):
  row=[]
  for bb in range(3):
   row.append(sum((tensor([pauli[a]/2 if j==i else pauli[bb]/2 if j==h else q for j in range(N)]) for i in range(N) for h in range(N) if i!=h),S.zeros(2**N)))
  hess.append(row)
 # Scale-free H=Q_C+b.J, matching G's coefficients with s=1.
 Q=sum((C[a,bb]*(J[a]*J[bb]+J[bb]*J[a])/2 for a in range(3) for bb in range(3)),S.zeros(2**N))
 H=Q+sum((b[a]*J[a] for a in range(3)),S.zeros(2**N))
 exact=(H*k+k*H)/2
 drift=(N-1)*P*C*m/2+P*b/2
 V=(N*(S.trace(C)+(N-1)*(m.T*C*m)[0]))/4+N*(b.T*m)[0]/2
 diffusion=V*k+sum((drift[a]*grad[a] for a in range(3)),S.zeros(2**N))+sum((D[a,bb]*hess[a][bb]/4 for a in range(3) for bb in range(3)),S.zeros(2**N))
 residual=(exact-diffusion).applyfunc(S.expand)
 assert residual==S.zeros(2**N),residual
 assert S.expand(S.trace(exact)-V)==0
 records.append({'N':N,'matrix_identity':'EXACT_ZERO','trace_potential_identity':'EXACT_ZERO'})
# Independent symbolic axis curvature cancellation.
x,y,z=S.symbols('x y z',real=True);v=S.Matrix([-z*x,-z*y,1-z*z]);rr=S.Matrix([-y,x,0]);vars=[x,y,z]
vv=v.jacobian(vars)*v;rrr=rr.jacobian(vars)*rr
assert S.simplify(vv-rrr+2*z*v)==S.zeros(3,1)
result={'status':'PASS_EXACT_TRANSCRIPTION','fixtures':records,'symbolic_drift_cancellation':'EXACT_ZERO','wall_seconds':time.monotonic()-st,'scope':'Independent finite checks supplement the symbolic all-N audit; they do not establish asymptotic tails, historical novelty or a compiler.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
