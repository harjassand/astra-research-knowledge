"""Exact rational sign certificate; not an actual conditional-expectation counterexample."""
import sympy as s,json
from pathlib import Path
q=s.Rational;I=s.eye(3);A=s.diag(1,q(1,1000),q(2,5));U=s.Matrix([[q(4,5),q(3,5),0],[0,0,1],[-q(3,5),q(4,5),0]]);assert U.T*U==I
X=U*A*U.T;B=(A+8*X)/9;C=(A+3*B)/4
assert s.trace(A)==s.trace(B)
N=60;rho=q(15,17);err=2*rho**(2*N+1)/((2*N+1)*(1-rho**2));res=[];bounds=[]
for Y in [B,C]:
 for D in [Y-I/16,I-Y]:
  z=[D[:i,:i].det() for i in [1,2,3]];assert all(a>0 for a in z);bounds.append(list(map(str,z)))
 Z=(Y-I)*(Y+I).inv();Z2=Z*Z;P=Z;v=q(0)
 for j in range(N):v+=2*P[0,0]/(2*j+1);P=P*Z2
 res.append(v)
f=res[0]-2*res[1];assert f+3*err<-q(1,200)
r={'scope':'Both index bounds and majorization do not imply top-eigenvector compressed-log sign. B is NOT asserted to be the physical conditional expectation of A.','A_diagonal':['1','1/1000','2/5'],'U':[[str(x)for x in U.row(i)]for i in range(3)],'log_sign_upper':'-1/200','series_center':str(s.N(f,18)),'combined_tail_bound':str(s.N(3*err,18)),'terms':N,'spectral_bounds':'I/16<B,C<I','sylvester_minors':bounds}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
