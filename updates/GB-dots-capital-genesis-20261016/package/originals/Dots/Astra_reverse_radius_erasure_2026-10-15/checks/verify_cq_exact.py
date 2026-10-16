"""Exact rational-complex primal/dual certificates; no numerical optimizer."""
import sympy as s
import json
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
S=[(I+s.Rational(3,5)*P)/2 for P in [X,Y,Z]]
M=sum([T.inv() for T in S],s.zeros(2))/3; U=M.inv(); C=1-s.trace(U)
assert C==s.Rational(3,11)
assert all(s.simplify(s.trace((T-U).conjugate().T*T.inv()*(T-U)))==C for T in S)
assert S[0]*S[2]!=S[2]*S[0]
omega=U/s.trace(U)
assert all(s.simplify(s.trace(omega*T.inv()*omega))==s.Rational(11,8) for T in S)
b=s.Rational(1,4)
V=[(b,b,b),(b,-b,-b),(-b,b,-b),(-b,-b,b)]
T=[(I+x*X+y*Y+z*Z)/2 for x,y,z in V]
Mt=sum([A.inv() for A in T],s.zeros(2))/4; Ut=Mt.inv(); Ct=1-s.trace(Ut)
assert Ct==s.Rational(3,16)
assert all(s.simplify(s.trace((A-Ut).conjugate().T*A.inv()*(A-Ut)))==Ct for A in T)
result={'pauli_three_C':str(C),'pauli_three_K':'11/8','pauli_three_U':str(U),'tetra_C':str(Ct),'tetra_U':str(Ut),'all_exact_assertions':'PASS'}
print(json.dumps(result,indent=2))
# Exact weighted-simplex frame identity on a qubit reference.
Q=s.Matrix([[1/s.sqrt(2),-1/s.sqrt(2),0],[1/s.sqrt(6),1/s.sqrt(6),-2/s.sqrt(6)]])
vs=[Q[:,i] for i in range(3)]; Rs=[v*v.T for v in vs]; zs=[v/s.sqrt(3) for v in vs]
assert s.simplify(sum(Rs,s.zeros(2)))==I
assert s.simplify(sum(zs,s.zeros(2,1)))==s.zeros(2,1)
A=sum([s.kronecker_product(R,T) for R,T in zip(Rs,S)],s.zeros(4))
W=sum([s.kronecker_product(z,T) for z,T in zip(zs,S)],s.zeros(4,2))
G=s.simplify(W.conjugate().T*A.inv()*W)
expected=sum(S,s.zeros(2))/3-U
assert s.simplify(G-expected)==s.zeros(2)
assert s.simplify(s.trace(G))==C
# Input supported energy: eigenvalue of Ri is 2/3, giving 1.
E=sum([(z.T*R*z)[0]/s.Rational(2,3)**2 for z,R in zip(zs,Rs)])
assert s.simplify(E)==1
# Direct same-dimension Hermitian trace check at supported input baseline.
hs=[1,-1,0]; Hs=[h*R for h,R in zip(hs,Rs)];K=sum(Hs,s.zeros(2))
Zs=[s.simplify(H-R*K) for H,R in zip(Hs,Rs)]
J=sum([s.kronecker_product(Z,T) for Z,T in zip(Zs,S)],s.zeros(4))
Ephys=s.simplify(sum([s.trace(Z.conjugate().T*R*Z)/s.Rational(2,3)**2 for Z,R in zip(Zs,Rs)]))
Nphys=s.simplify(s.trace(J.conjugate().T*A.inv()*J))
assert s.simplify(Nphys/Ephys)==C
print(json.dumps({'frame_matrix_identity':'PASS','frame_input_energy':str(E),'frame_output_energy':str(s.trace(G)),'Hermitian_input_defect':str(Ephys),'Hermitian_output_defect':str(Nphys),'Hermitian_ratio':str(s.simplify(Nphys/Ephys))},indent=2))
