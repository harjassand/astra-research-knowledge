"""Exact frame-co-transform and coarse-measurement obstructions."""
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
c=s.Rational(99,101);t=s.Rational(20,101)
C=(I-s.I*X)/s.sqrt(2);E=c*I-s.I*t*X
assert C.H*C==I and E.H*E==I
logical=[]
for g in [I,X,Y,Z]:
    ideal_core=g*C*g.H
    actual_core=g*C*E*g.H
    assert g.H*ideal_core*g==C
    logical.append(s.simplify(g.H*actual_core*g))
assert all(U==C*E for U in logical)
K0=sum(logical,s.zeros(2))/4
assert K0==C*E
for P in [X,Y,Z]:
    K=s.zeros(2)
    for g,U in zip([I,X,Y,Z],logical):
        sign=1 if g*P==P*g else -1
        K+=sign*U/4
    assert K==s.zeros(2)
psi=s.Matrix([1,0]);v=C*psi;w=C*E*psi
rho=v*v.H;sigma=w*w.H
assert s.simplify((v.H*w)[0])==c
assert s.simplify((rho-sigma).det())==-t*t
# Coarse active projector |11>, versus measuring both Z bits and forgetting them.
R=[s.diag(*[int(i==j) for i in range(4)]) for j in range(4)]
Pactive=R[3];Pinactive=s.eye(4)-Pactive
v=s.Matrix([1,1,0,0])/s.sqrt(2);rho=v*v.H
coarse=Pactive*rho*Pactive+Pinactive*rho*Pinactive
fine=sum((r*rho*r for r in R),s.zeros(4))
assert coarse==rho and fine!=coarse
assert coarse[0,1]==s.Rational(1,2) and fine[0,1]==0
print('PASS: desired Clifford is unchanged by compiler for every frame; actual overrotation survives entirely in zero character.')
print('Error norm squared =',2-2*c,'; pure-state output trace distance =',2*t)
print('PASS: full measurement + forgotten lookup labels removes inactive-sector coherence preserved by literal coarse correction.')
# Positive compiler: the SAME noisy physical core C E for each frame.
fixed=[]
for g in [I,X,Y,Z]:
    output=C*g.H*C.H
    fixed.append(s.simplify(output*(C*E)*g))
    assert s.simplify(output*C*g)==C
    assert fixed[-1]==s.simplify(C*g.H*E*g)
coeff={}
for name,P in [('I',I),('X',X),('Y',Y),('Z',Z)]:
    K=s.zeros(2)
    for g,U in zip([I,X,Y,Z],fixed):
        sign=1 if g*P==P*g else -1
        K+=sign*U/4
    coeff[name]=s.simplify(K)
assert coeff['I']==c*C
assert coeff['X']==s.simplify(-s.I*t*C*X)
assert coeff['Y']==coeff['Z']==s.zeros(2)
assert s.simplify(coeff['X'].H*coeff['X'])==t*t*I
print('PASS: fixed physical Clifford core plus Pauli wrappers gives K0=c C, KX=-i s C X, bad effect 400/10201 I.')
# Why a trusted controller record cannot be an arbitrary mutable bath subsystem.
# Tensor order: data, record. Ideal feedforward applies X iff record=1.
R0=s.diag(1,0);R1=s.diag(0,1)
feed=s.kronecker_product(I,R0)+s.kronecker_product(X,R1)
v=s.kronecker_product(s.Matrix([1,0]),s.Matrix([0,1]))
record_flip=s.kronecker_product(I,X)
assert feed*v==s.kronecker_product(s.Matrix([0,1]),s.Matrix([0,1]))
assert feed*record_flip*v==s.kronecker_product(s.Matrix([1,0]),s.Matrix([1,0]))
for g in [I,X,Y,Z]:
    frame=s.kronecker_product(g,I)
    assert frame.H*record_flip*frame==record_flip
print('PASS: mutable record error has trivial data character but causes wrong feedforward; protected classical records are necessary here.')
