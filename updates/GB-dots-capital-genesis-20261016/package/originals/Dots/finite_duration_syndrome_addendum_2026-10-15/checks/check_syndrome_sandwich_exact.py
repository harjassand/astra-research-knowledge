"""Exact syndrome-sandwich bath witness, with genuine measurement labels."""
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1)
R=[s.diag(1,0),s.diag(0,1)];kron=s.kronecker_product
c=s.Rational(99,101);t=s.Rational(20,101)
U=kron(I,R[0])+kron(c*I-s.I*t*X,R[1])
A0=s.diag(1,c);A1=s.diag(0,-s.I*t)
# Completed correction: reset ancilla with active X on syndrome 1.
C=[R[0],X*R[1]]
K=[];bad_effect=s.zeros(4)
for pre in range(2):
  for j in range(2):
    L=C[j]*R[pre]
    if L==s.zeros(2): continue
    predicted=0 # X correction maps either incoming syndrome to Z=+1.
    assert R[predicted]*L==L
    for post in range(2):
      B=kron(R[post],I)*U*kron(L,I)
      expected=kron(L,A0) if post==0 else kron(X*L,A1)
      assert B==expected
      K.append(B)
      if post!=predicted: bad_effect+=B.H*B
assert sum((B.H*B for B in K),s.zeros(4))==s.eye(4)
assert bad_effect==kron(I,s.diag(0,t*t))
# Per-sector norm-to-mismatch identity, valid for both measured sectors.
D=U-s.eye(4)
for pre in range(2):
    P=kron(R[pre],I)
    assert (s.eye(4)-P)*U*P==(s.eye(4)-P)*D*P
print('PASS: four exact measurement/correction Kraus operators, TP completeness, and real-label mismatch effect.')
print('Bad effect I_A tensor diag(0,',t*t,') <=',2-2*c,'I; no frame randomization used.')
