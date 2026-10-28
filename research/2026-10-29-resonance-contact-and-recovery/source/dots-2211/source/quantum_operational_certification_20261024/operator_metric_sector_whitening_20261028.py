"""Exact sector cancellation and noncommuting-spectator obstruction; no source calls."""
from pathlib import Path
import sympy as s,json
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1); P=[X,Y,Z]
p0=s.diag(1,0);p1=s.diag(0,1);pp=s.ones(2)/2
u=s.Matrix([s.Rational(3,5),0,s.Rational(4,5)])
Ts=[s.diag(s.Rational(4,5),s.Rational(4,5),s.Rational(16,25)),s.Rational(4,5)*s.eye(3)-s.Rational(4,25)*u*u.T]
# Hide the flag decomposition by a rational real entangling rotation.
V=s.eye(4);V[0,0]=V[3,3]=s.Rational(3,5);V[0,3]=s.Rational(4,5);V[3,0]=-s.Rational(4,5)
assert V.H*V==s.eye(4)
C=[]
for j in range(3):
 C.append(V*(sum((s.kronecker_product(sum((T[k,j]*P[k] for k in range(3)),s.zeros(2)),F) for T,F in zip(Ts,[p0,p1])),s.zeros(4))/4)*V.H)
H=s.BlockMatrix([[(C[j]*C[k]+C[k]*C[j])/2 for k in range(3)] for j in range(3)]).as_explicit()
# Exact inverse square root witness used ONLY to verify data-defined functional calculus.
W=s.BlockMatrix([[V*s.kronecker_product(I,s.diag(4*Ts[0].inv()[j,k],4*Ts[1].inv()[j,k]))*V.H for k in range(3)] for j in range(3)]).as_explicit()
assert W.H==W and W*H*W==s.eye(12) and W*H==H*W
# W is positive: unitary equivalent to directsum(4*T_a^-1 tensor I2), with both T_a SPD.
assert all(T.is_positive_definite for T in Ts)
for j in range(3):
 F=sum((C[k]*W[4*k:4*k+4,4*j:4*j+4] for k in range(3)),s.zeros(4))
 assert F==V*s.kronecker_product(P[j],I)*V.H
 assert F*F==s.eye(4)
assert all(H[4*j:4*j+4,4*k:4*k+4]*C[l]==C[l]*H[4*j:4*j+4,4*k:4*k+4] for j in range(3) for k in range(3) for l in range(3))
# Noncommuting spectator branch states, still positive SPD contractions.
A=s.Rational(1,4)*p0+s.Rational(1,8)*pp
B=s.Rational(1,8)*p0+s.Rational(1,4)*pp
Cx=s.kronecker_product(X,A); Cz=s.kronecker_product(Z,B)
Hxz=(Cx*Cz+Cz*Cx)/2
assert Hxz!=-s.zeros(4) and Hxz*Cx!=Cx*Hxz
r={'status':'PASS_EXACT_AUTHOR_DIAGNOSTICS','hidden_flag_dimension':4,'operator_metric_dimension':12,'exact_recovered_generators':3,'central_metric_blocks':9,'noncommuting_spectator_centrality_failure':True,'source_calls':0,'classification':'Candidate construction, not independent receiving; inverse-square-root witness verifies the data-defined operation, not supplied learner sectors.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
