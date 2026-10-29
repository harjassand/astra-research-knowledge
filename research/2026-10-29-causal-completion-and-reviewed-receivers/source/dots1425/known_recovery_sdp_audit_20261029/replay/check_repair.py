import sympy as s,numpy as np,json,itertools
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
def vec(A):return s.Matrix([A[a,b] for b in range(A.cols) for a in range(A.rows)])
def rot(P,t):return ((1-t*t)*I+2*s.I*t*P)/(1+t*t)
def ptr(J):return s.Matrix(2,2,lambda i,j:sum(J[o+2*i,o+2*j] for o in range(2)))
def numeric(A):return np.array(A.evalf(),dtype=complex)
S=s.zeros(4)
for a in range(2):
 for b in range(2):S[b*2+a,a*2+b]=1
def psd(A):
 return all(s.simplify(A.extract(idx,idx).det())>=0 for r in range(1,A.rows+1) for idx in itertools.combinations(range(A.rows),r))
rows=[]
for j in range(1,25):
 U=rot(X,s.Rational(j,7));V=rot(Y,s.Rational(j+1,9));R=rot(Z,s.Rational(j+2,11));w=s.Rational(j,25)
 # Input-first physical Choi vector is row-flattened U; recovery vec uses column flattening.
 vc=s.Matrix([U[b,a] for a in range(2) for b in range(2)])
 vd=s.Matrix([V[b,a] for a in range(2) for b in range(2)])
 C=(w*vc*vc.H+(1-w)*vd*vd.H)/2
 W=(S*C.T*S.H/2).applyfunc(s.simplify)
 direct=((w*vec(U.H)*vec(U.H).H+(1-w)*vec(V.H)*vec(V.H).H)/4).applyfunc(s.simplify)
 assert W==direct and s.trace(W)==s.Rational(1,2)
 J0=(vec(R)*vec(R).H).applyfunc(s.simplify)
 fidelity=(w*abs(s.trace(R*U))**2+(1-w)*abs(s.trace(R*V))**2)/4
 assert s.simplify(s.trace(W*J0)-fidelity)==0
 xi=s.Rational(1,100+j)
 H=s.kronecker_product(X,Z)/2
 J=J0+xi*H;Jp=(J+xi*s.eye(4))/(1+2*xi)
 assert ptr(J).applyfunc(s.simplify)==I and ptr(Jp).applyfunc(s.simplify)==I
 assert psd(J+xi*s.eye(4))
 objdrop=s.simplify(s.trace(W*(J-Jp)))
 assert objdrop<=4*xi
 Yn=(s.Rational(1,2)-xi)*I;Yp=Yn+xi*I
 assert psd(s.kronecker_product(Yp,I)-W)
 actualnorm=float(np.linalg.eigvalsh(numeric(Jp-J)).__abs__().sum())
 assert actualnorm<=8*float(xi)+1e-12
 rows.append(dict(j=j,objective_drop=str(objdrop),trace_norm_to_bound=actualnorm/(8*float(xi))))
print(json.dumps(dict(scope='24 exact complex orientation/TP/PSD/objective repairs; numeric trace-norm supplement, no generic solver',cases=len(rows),max_trace_norm_ratio=max(x['trace_norm_to_bound'] for x in rows)),indent=2))
