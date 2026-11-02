"""Exact symbolic verification of the three-qubit Pauli compatibility basis."""
import sympy as s,json,os
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[I,X,Y,Z]
W=s.zeros(8);V=s.zeros(8)
for i in range(4):
 bell=P[i].T/s.sqrt(2)
 for a in range(2):
  for b in range(2):
   for c in range(2):
    for t in range(2):
     W[4*a+2*b+c,2*i+t]=bell[a,b]*P[i][c,t]
     V[4*a+2*b+c,2*i+t]=bell[a,c]*P[i][b,t]
H=s.Matrix([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])/2
checks={'W_unitary':W.H*W==s.eye(8),'V_unitary':V.H*V==s.eye(8),'change_of_pairing':V.H*W==s.kronecker_product(H,I),'Pauli_X_covariance':W.H*s.kronecker_product(X,X,X)*W==s.kronecker_product(s.eye(4),X),'Pauli_Z_covariance':W.H*s.kronecker_product(Z,Z,Z)*W==s.kronecker_product(s.eye(4),Z)}
assert all(checks.values())
json.dump(checks,open(os.path.dirname(__file__)+'/compatibility_basis_exact_check.json','w'),indent=2);print(checks)
