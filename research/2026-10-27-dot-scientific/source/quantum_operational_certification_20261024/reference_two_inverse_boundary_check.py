import sympy as s
from pathlib import Path
import json
# Canonical maximally entangled rank2 kernel vector on physical3/reference2.
I=s.eye(6);phi=s.zeros(6,1);phi[0]=1;phi[3]=1;P=phi*phi.T/2
PT=lambda A:s.Matrix(6,6,lambda i,j:A[2*(j//2)+i%2,2*(i//2)+j%2])
trA=lambda A:s.Matrix(2,2,lambda i,j:sum(A[2*k+i,2*k+j] for k in range(3)))
N=lambda A:(s.kronecker_product(s.eye(3),trA(A))-PT(A))/2
Q=N(P)
assert Q.eigenvals()=={s.Rational(1,2):1,s.Rational(1,4):2,0:3}
M=s.zeros(6);M[0,0]=2;M[3,3]=2;v=s.zeros(6,1);v[1]=1;v[2]=1;M+=v*v.T
assert trA(M)==3*s.eye(2)
Y=N(M)
assert Y.eigenvals()=={0:1,1:3,s.Rational(3,2):2}
assert M*Q==s.zeros(6)
report={'status':'PASS','input_spectrum':str(M.eigenvals()),'output_spectrum':str(Y.eigenvals()),'Q_spectrum':str(Q.eigenvals()),'coercivity_limit_coefficient':'3/2+sqrt(2)>2','scope':'reference2 boundary geometry and stationary reduction; not inverse-trace sign'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
