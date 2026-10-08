"""Independent post-exposure rational sharpness and generic permutation checks."""
from sympy import Matrix, eye, I, symbols, Rational as R, kronecker_product as kron, simplify
from itertools import permutations,product
J=[Matrix([[0,0,0],[0,0,-I],[0,I,0]]),Matrix([[0,0,I],[0,0,0],[-I,0,0]]),Matrix([[0,-I,0],[I,0,0],[0,0,0]])]
weights=symbols('w1 w2 w3');qs=symbols('q1 q2 q3');Id=eye(3)
Q=Matrix.diag(*qs)
W=sum((-weights[i]*(kron(J[i],J[i],Id)+kron(J[i],Id,J[i])) for i in range(3)),Matrix.zeros(27))
D=(3*kron(Q,Id,Id)+kron(Id,Q,Id)+kron(Id,Id,Q))/5-W
for perm in permutations(range(3)):
    P=Matrix.zeros(3)
    for i in range(3):P[perm[i],i]=1
    for i in range(3):assert P*J[i]*P.T==P.det()*J[perm[i]]
    U=kron(P,P,P);inv=[perm.index(i) for i in range(3)]
    sub={weights[i]:weights[inv[i]] for i in range(3)}|{qs[i]:qs[inv[i]] for i in range(3)}
    assert simplify(U*D*U.T-D.subs(sub,simultaneous=True))==Matrix.zeros(27)
print('PASS: all6 permutation identities, including improper determinant sign cancellation.')

def ev(a,b,c):
    v=Matrix.zeros(27,1);v[9*a+3*b+c]=1;return v
V=[]
for i in range(3):
    j,k=[x for x in range(3) if x!=i]
    v=4*ev(i,i,i)-2*ev(i,j,j)-2*ev(i,k,k)+3*(ev(j,i,j)+ev(j,j,i)+ev(k,i,k)+ev(k,k,i))
    assert (v.T*v)[0]==60
    V.append(v)
M=Matrix.hstack(*V);assert M.T*M==60*eye(3)
R0=M*M.T/180
assert R0.trace()==1
assert R0*R0==R0/3

def one_marginal(R0,site):
    out=Matrix.zeros(3)
    for a,b in product(range(3),repeat=2):
        for c,d in product(range(3),repeat=2):
            rs=[None]*3;cs=[None]*3;rs[site]=a;cs[site]=b
            other=[k for k in range(3) if k!=site]
            rs[other[0]]=cs[other[0]]=c;rs[other[1]]=cs[other[1]]=d
            out[a,b]+=R0[9*rs[0]+3*rs[1]+rs[2],9*cs[0]+3*cs[1]+cs[2]]
    return out
for k in range(3):assert one_marginal(R0,k)==eye(3)/3
BC=Matrix.zeros(27)
for a,b,c in product(range(3),repeat=3):BC[9*a+3*c+b,9*a+3*b+c]=1
assert BC*R0*BC==R0
AB=Matrix(9,9,lambda u,v:sum(R0[9*(u//3)+3*(u%3)+c,9*(v//3)+3*(v%3)+c] for c in range(3)))
F=Matrix.zeros(9)
for a,b in product(range(3),repeat=2):F[3*b+a,3*a+b]=1
assert F*AB.T*F==AB

def Phi(X):return Matrix(3,3,lambda b,c:3*sum(X[a,d]*AB[3*a+b,3*d+c] for a,d in product(range(3),repeat=2)))
assert Phi(eye(3))==eye(3)
for i in range(3):assert Phi(J[i])==R(3,4)*J[i]
H=W.subs({x:1 for x in weights})
assert (R0*H).trace()==3
print('PASS: R0 rational outer-product PSD rank3, trace1, all three marginals I3/3, BCswap, real HS-adjoint Choi symmetry.')
print('PASS: exact Phi(Ji)=3Ji/4; 2s=3, V=2, k=1, sharp defect ratio2.')
