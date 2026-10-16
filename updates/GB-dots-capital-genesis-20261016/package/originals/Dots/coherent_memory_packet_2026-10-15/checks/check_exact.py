"""Exact rational certificate. No floating point and no downloaded code."""
import sympy as s
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Z=s.diag(1,-1)
kron=s.kronecker_product
N=16; In=s.eye(N)
X1=kron(X,s.eye(8)); Z1=kron(Z,s.eye(8)); Z2=kron(I,Z,s.eye(4))
c=s.Rational(99,101); t=s.Rational(20,101); q=s.Rational(16,101)
U=(c*In-s.I*t*X1)*(c*In-s.I*t*X1*Z2)
assert U.H*U==In
G=[In,Z1,Z2,Z1*Z2]
U0=sum((g*U*g for g in G),s.zeros(N))/4
U1=(U-Z1*U*Z1)/2
assert U0==c*c*In-t*t*Z2
assert U1==-s.I*c*t*X1*(In+Z2)
assert U==U0+U1
assert U0.H*U0+U1.H*U1==In
# ||individual rotation-I||^2=2-2c=4/101;
# triangle inequality bounds ||U-I||^2 by 4*(4/101)=q.
assert q==4*(2-2*c) and 0<q<1
print('q =',q)
for z in [-1,1]:
    a=c*c-t*t*z
    b2=c*c*t*t*(1+z)**2
    residual=s.factor(a*a-(1-q))
    assert a*a+b2==1 and residual>=0
    print('output Z2 =',z,'a =',a,'nontrivial probability =',b2,'identity residual =',residual)
Ks=[]
for j in range(7):
    K=s.zeros(N);K[0,j]=1;Ks.append(K)
Ks.append(s.diag(*([0]*7+[1]*9)))
Ls=[]
for K in Ks:
    for z1 in [-1,1]:
        for z2 in [-1,1]:
            R=(In+z1*Z1)*(In+z2*Z2)/4
            L=K*R
            if L!=s.zeros(N): Ls.append(L)
assert sum((L.H*L for L in Ls),s.zeros(N))==In
# Sparse exact Choi calculation; weighted outers avoid square roots.
def vec(A):
    return s.SparseMatrix(N*N,1,{(i+N*j,0):A[i,j] for i in range(N) for j in range(N) if A[i,j]!=0})
def outer(A):
    v=vec(A);return v*v.H
Jref=sum((outer(L) for L in Ls),s.zeros(N*N))
Jtw=sum((outer(g*U*g*L)/4 for g in G for L in Ls),s.zeros(N*N))
Jres=s.zeros(N*N)
for L in Ls:
    outputs=[i for i in range(N) if any(L[i,j]!=0 for j in range(N))]
    z=Z2[outputs[0],outputs[0]]
    assert all(Z2[i,i]==z for i in outputs)
    a=c*c-t*t*z
    assert U0*L==a*L
    Jres+=(a*a-(1-q))*outer(L)+outer(U1*L)
assert Jtw-(1-q)*Jref==Jres
# Trace-preservation of the residual normalized by q.
residual_completeness=s.zeros(N)
for L in Ls:
    outputs=[i for i in range(N) if any(L[i,j]!=0 for j in range(N))]
    z=Z2[outputs[0],outputs[0]];a=c*c-t*t*z
    residual_completeness+=(a*a-(1-q))*L.H*L+(U1*L).H*(U1*L)
assert residual_completeness==q*In
print('PASS: exact Choi identity and positive weighted-Kraus certificate;',len(Ls),'nonzero refined correction Kraus operators.')
