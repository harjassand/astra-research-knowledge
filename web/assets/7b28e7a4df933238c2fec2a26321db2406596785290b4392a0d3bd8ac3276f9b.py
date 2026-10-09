"""Exact depth-one physical tree and normalization checks; no originator imports."""
from itertools import product
from pathlib import Path
import json
from sympy import Matrix, eye, zeros, Rational as R, sqrt, I, simplify, kronecker_product as kron

def simp(X):return X.applyfunc(simplify)
def tr2(X,d):
    return Matrix(d,d,lambda a,b:sum(X[d*a+c,d*b+c] for c in range(d)))

# Spin1 maximal-output-spin broadcaster. Construct the projection directly
# as symmetric traceless tensors in the real vector representation.
d=3;Id=eye(d)
J=[Matrix([[0,0,0],[0,0,-I],[0,I,0]]),
   Matrix([[0,0,I],[0,0,0],[-I,0,0]]),
   Matrix([[0,-I,0],[I,0,0],[0,0,0]])]
swap=zeros(9)
for a,b in product(range(3),repeat=2):swap[3*b+a,3*a+b]=1
omega=sum((kron(Id[:,a],Id[:,a]) for a in range(3)),zeros(9,1))/sqrt(3)
P=(eye(9)+swap)/2-omega*omega.T
assert P*P==P and P.H==P and P.trace()==5 and tr2(P,3)==R(5,3)*Id
def Badj(Y):return simp(R(3,5)*tr2(P*Y*P,3))
assert Badj(eye(9))==Id
E=[sqrt(R(3,2))*A for A in J]
for a in E:
    assert Badj(kron(a,Id))==R(3,4)*a
    assert Badj(kron(Id,a))==R(3,4)*a
rhoBC=P/5
assert tr2(rhoBC,3)==Id/3
C=Matrix(3,3,lambda a,b:simplify((rhoBC*kron(E[a],E[b])).trace()))
assert C==eye(3)/2

# Extend to a COMPLETE tau-orthonormal traceless Hermitian basis.
H=E+[sqrt(R(3,2))*Matrix.diag(1,-1,0),Matrix.diag(1,1,-2)/sqrt(2)]
for a,b in [(0,1),(0,2),(1,2)]:
    H.append(sqrt(R(3,2))*(Id[:,a]*Id[:,b].T+Id[:,b]*Id[:,a].T))
assert Matrix(8,8,lambda a,b:simplify((H[a]*H[b]).trace()/3))==eye(8)

leaf=[]
for a in range(3):
    ji=J[a]
    for sign,proj in [(1,(ji*ji+ji)/2),(-1,(ji*ji-ji)/2),(0,Id-ji*ji)]:
        x=zeros(3,1);x[a]=3*sign*sqrt(R(3,2))
        leaf.append((proj/3,x))
assert sum((F for F,x in leaf),zeros(3))==Id
assert sum(((F.trace()/3)*(x*x.T) for F,x in leaf),zeros(3))==3*eye(3)

N=zeros(3);S=zeros(8);cross=zeros(8,3)
moments=[zeros(3) for a in range(3)]
total_effect=zeros(3);outcome_count=0
for (Fl,xl),(Fr,xr) in product(leaf,repeat=2):
    M=Badj(kron(Fl,Fr))
    x=R(2,3)*(xl+xr) # (1/(2lambda)) with lambda3/4
    total_effect+=M
    for a in range(3):moments[a]+=x[a]*M
    prob=simplify(M.trace()/3)
    if prob==0:assert M==zeros(3);continue
    outcome_count+=1
    post=Matrix([simplify((M*A).trace()/(3*prob)) for A in H])
    N+=prob*x*x.T;S+=prob*post*post.T;cross+=prob*post*x.T
N=simp(N);S=simp(S);cross=simp(cross)
assert simp(total_effect)==Id
for a in range(3):assert simp(moments[a])==E[a]
assert N==R(28,9)*eye(3)
embedding=zeros(8,3)
for a in range(3):embedding[a,a]=1
assert cross==embedding
assert S==Matrix.diag(*S.diagonal())
residual=simp(S-embedding*N.inv()*embedding.T)
assert all(x.is_nonnegative is True for x in residual.diagonal())
D=R(32,9)*eye(3)
assert D-N==R(4,9)*eye(3)
print('PASS exact correlated spin1 depth1: one81-outcome POVM, unbiased all3 noncommuting E_a, C=I/2, N=28I/9, D=32I/9.',flush=True)
print('PASS full8-coordinate posterior crossmoment=embedding and exact Schur residual diagonalPSD:',list(residual.diagonal()),flush=True)

# Signed unit-modulus qubit: measure Z, prepare opposite Z on both outputs.
Z=Matrix.diag(1,-1);I2=eye(2)
ps=[(I2+e*Z)/2 for e in [1,-1]]
Rbc=sum((kron(ps[1-i],ps[1-i])/2 for i in range(2)),zeros(4))
assert (Rbc*kron(Z,Z)).trace()==1
def flip_Badj(Y):
    return sum((ps[i]*(kron(ps[1-i],ps[1-i])*Y).trace() for i in range(2)),zeros(2))
assert flip_Badj(kron(Z,I2))==-Z
unit_N=R(0);unit_cross=R(0);unit_S=R(0);first=zeros(2);total=zeros(2)
for (i,Pb),(j,Pc) in product(enumerate(ps),repeat=2):
    M=flip_Badj(kron(Pb,Pc));prob=M.trace()/2
    x=-R(1,2)*((1-2*i)+(1-2*j))
    total+=M;first+=x*M
    if prob==0:continue
    post=(M*Z).trace()/(2*prob)
    unit_N+=prob*x*x;unit_cross+=prob*post*x;unit_S+=prob*post*post
assert total==I2 and first==Z and unit_N==unit_cross==unit_S==1
print('PASS negative lambda=-1 mode: exact same-POVM unbiasedness, N=1, canonical score1; no singular inverse or sign loss.',flush=True)

# Exact purely algebraic C8 reduction on a legal nonnormal qubit EB matrix.
T=Matrix([[0,1,0],[0,0,0],[0,0,0]])
theta=T.T*T
assert 2*eye(3)-T-T.T-(eye(3)-theta)==(eye(3)-T).T*(eye(3)-T)
print('PASS arbitrary-channel energy comparison via exact (I-T)^T(I-T) factorization.',flush=True)

Path(__file__).with_name('EXACT_TREE_CHECKS.json').write_text(json.dumps({
    'schema_version':1,'all_pass':True,'scope':'Exact physical finite tree/normalization diagnostics; universal theorem is proved analytically in audit text.',
    'spin1':{'outcomes':outcome_count,'retained_modes':3,'C':'I/2','N1':'28I/9','D1':'32I/9','posterior_S_diagonal':[str(x) for x in S.diagonal()],
             'full8_Schur_residual_diagonal':[str(x) for x in residual.diagonal()]},
    'signed_unit_mode':{'lambda':'-1','N':'1','canonical_score':'1'},
    'arbitrary_channel_energy':'2(I-symT)-(I-T^T T)=(I-T)^T(I-T)'
},indent=2)+'\n')
