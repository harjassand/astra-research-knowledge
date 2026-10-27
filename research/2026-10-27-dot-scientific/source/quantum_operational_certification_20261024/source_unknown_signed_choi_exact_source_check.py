import sympy as s
I=s.I;u=s.Matrix([1,I,1,1])/2;U=s.eye(4)-2*u*u.conjugate().T;V=U[:,:3]
assert V.conjugate().T*V==s.eye(3)
w=s.Matrix([1,2*I,3,4]);tau=w*w.conjugate().T/30
p=s.Rational(2,5);q=1-p;P=V*V.conjugate().T
vv=s.Matrix([V[j,i] for i in range(3) for j in range(4)])
Phi=vv*vv.conjugate().T/3
J=p*Phi+q*s.kronecker_product(s.eye(3)/3,tau)
sigma=p*P/3+q*tau;omega=s.kronecker_product(s.eye(3)/3,sigma)
A=s.simplify(J-omega)
assert A==p*Phi-p*s.kronecker_product(s.eye(3),P)/9
assert s.simplify(A*vv-8*p*vv/9)==s.zeros(12,1)
assert s.simplify(A*(s.eye(12)-s.kronecker_product(s.eye(3),P)))==s.zeros(12)
# Bell ancilla/projector amplitude: exactly V*/3 (no basis conjugation error).
K=s.Matrix(3,4,lambda i,j:s.conjugate(V[j,i])/3)
assert K==V.conjugate().T/3
assert s.simplify(K*V-s.eye(3)/3)==s.zeros(3)
# Exact controlled collision first derivative after tracing its program.
rho=s.Matrix([[s.Rational(2,3),I/6],[-I/6,s.Rational(1,3)]])
X=s.Matrix([[1,I,2,0],[-I,2,1,I],[2,1,3,-I],[0,-I,I,4]])/10
S=s.zeros(4)
for i in range(2):
 for j in range(2):S[2*j+i,2*i+j]=1
C=s.diag(0,1);H=s.kronecker_product(C,S);XX=s.kronecker_product(X,rho)
comm=H*XX-XX*H
tr=s.Matrix(4,4,lambda i,j:sum(comm[2*i+k,2*j+k] for k in range(2)))
G=s.kronecker_product(C,rho)
assert s.simplify(tr-(G*X-X*G))==s.zeros(4)
print('PASS exact complex signed-Choi cancellation/eigenspace, inverse factor1/3, and controlled collision generator including coherences')
