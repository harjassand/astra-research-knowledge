from sympy import Rational as R, Matrix, sqrt, simplify, eye
from sympy.physics.wigner import wigner_6j
j=R(3,2)
h=Matrix([[simplify(4*(-1)**(3+J+l)*wigner_6j(j,j,l,j,j,J)) for J in range(4)] for l in range(4)])
print('Channel rank l rows, pair J columns:'); print(h)
maxspec={}
for K in [R(1,2),R(3,2),R(5,2),R(7,2),R(9,2)]:
    allowed=[L for L in range(4) if abs(L-j)<=K<=L+j]
    U=Matrix([[sqrt((2*L+1)*(2*J+1))*wigner_6j(j,j,L,j,K,J) for J in allowed] for L in allowed])
    assert simplify(U*U.T)==eye(len(allowed))
    H=[simplify(U*Matrix.diag(*[h[l,J] for J in allowed])*U.T) for l in range(4)]
    for parity in [0,1]:
        ids=[i for i,L in enumerate(allowed) if L%2==parity]
        if not ids: continue
        A=[M.extract(ids,ids) for M in H]
        print('K',K,'L',[allowed[i] for i in ids]);
        for l in range(1,4):
            print(' H',l,A[l],'eigs',A[l].eigenvals())
        for label,M in [('lambda1',A[1]),('lambda2',A[2]),('lambda3',A[3]),('3lambda1+7lambda3',3*A[1]+7*A[3])]:
            vals=list(M.eigenvals())
            print(' support',label,vals)
            maxspec.setdefault(label,[]).extend(vals)
print('GLOBAL SUPPORTS')
for label,vals in maxspec.items(): print(label,max(vals,key=lambda x:float(x)),sorted(set(vals),key=lambda x:float(x)))
