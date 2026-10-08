"""Exact finite certificate replay; no numerical eigenvalue inference."""
from sympy import Rational as R, Matrix, sqrt, simplify, eye, factorial, prod
j=R(3,2)

def triangle(a,b,c):
    if c<abs(a-b) or c>a+b or (a+b+c).q!=1: return R(0)
    return sqrt(factorial(a+b-c)*factorial(a-b+c)*factorial(-a+b+c)/factorial(a+b+c+1))

def sixj(a,b,c,d,e,f):
    pref=triangle(a,b,c)*triangle(a,e,f)*triangle(d,b,f)*triangle(d,e,c)
    if pref==0: return R(0)
    lo=max(a+b+c,a+e+f,d+b+f,d+e+c)
    hi=min(a+b+d+e,a+c+d+f,b+c+e+f)
    return simplify(pref*sum((-1)**z*factorial(z+1)/(
        factorial(z-a-b-c)*factorial(z-a-e-f)*factorial(z-d-b-f)*factorial(z-d-e-c)
        *factorial(a+b+d+e-z)*factorial(a+c+d+f-z)*factorial(b+c+e+f-z)
    ) for z in range(int(lo),int(hi)+1)))

h=Matrix([[simplify(4*(-1)**(3+J+l)*sixj(j,j,l,j,j,J)) for J in range(4)] for l in range(4)])
assert h==Matrix([[1,1,1,1],[1,R(11,15),R(1,5),-R(3,5)],[1,R(1,5),-R(3,5),R(1,5)],[1,-R(3,5),R(1,5),-R(1,35)]])


def psd_1_or_2(M):
    """All principal minors, sufficient and necessary for these sizes."""
    M=simplify(M)
    assert M==M.T and M.rows<=2
    assert all(M[i,i].is_nonnegative is True for i in range(M.rows)),M
    assert M.det().is_nonnegative is True,M

blocks=[]
for K in [R(1,2),R(3,2),R(5,2),R(7,2),R(9,2)]:
    allowed=[L for L in range(4) if abs(L-j)<=K<=L+j]
    U=Matrix([[sqrt((2*L+1)*(2*J+1))*sixj(j,j,L,j,K,J) for J in allowed] for L in allowed])
    assert simplify(U*U.T)==eye(len(allowed))
    H=[simplify(U*Matrix.diag(*[h[l,J] for J in allowed])*U.T) for l in range(4)]
    for parity in [0,1]:
        ids=[i for i,L in enumerate(allowed) if L%2==parity]
        if not ids: continue
        A=[M.extract(ids,ids) for M in H]
        I=eye(len(ids))
        psd_1_or_2(R(4,5)*I-A[1])
        psd_1_or_2(R(3,5)*I-A[2])
        psd_1_or_2(R(9,14)*I-A[3])
        psd_1_or_2(6*I-3*A[1]-7*A[3])
        blocks.append((K,[allowed[i] for i in ids],A[1:]))
for K,L,A in blocks: print('K='+str(K)+' L='+str(L)+' scores='+str(A))
print('PASS: 9 exact blocks; all four support-bound matrix differences PSD by exact principal minors.')

# The non-dominance witness is the d=4 universal cloner.
A=next(A for K,L,A in blocks if K==R(3,2) and L==[1,3])
v=Matrix([sqrt(R(3,10)),sqrt(R(7,10))])
assert [simplify((v.T*M*v)[0]) for M in A]==[R(3,5)]*3
print('PASS: non-dominance extension witness lambda=(3/5,3/5,3/5).')

# Diagnostic only for general theorem: exact finite instances accompany its analytic product proof.
for n in range(1,31):
    for l in range(n+1):
        c=lambda nn: R(factorial(nn)*factorial(nn+1),factorial(nn-l)*factorial(nn+l+1))
        a,b=c(n),c(2*n)
        assert 1-a<=2*(1-a/b)
print('PASS: optional exact finite checks n<=30; infinite-n statement rests on analytic proof.')
