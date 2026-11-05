import json,sympy as s
from sympy.physics.wigner import wigner_6j
from pathlib import Path
p=Path(__file__).resolve().parents[1]
for rec in json.loads((p/'exact_lp_certificates.json').read_text()):
 n=rec['n'];D=n+1;j=s.Rational(n,2)
 M=s.Matrix([[(2*k+1)*(-1)**(n+k+l)*wigner_6j(j,j,k,j,j,l)for l in range(D)]for k in range(D)])
 saved=s.Matrix([[s.Rational(x)for x in row]for row in json.loads((p/f'transform_n{n}.json').read_text())]);assert M==saved
 assert M*M==s.eye(D)
 G=2*M-s.eye(D);H=s.eye(D).col_join(G);E=G[1:5,:]
 beta=s.Rational(rec['beta']);y=s.Matrix([s.Rational(x)for x in rec['inequality_multipliers']]);z=s.Matrix([s.Rational(x)for x in rec['equality_multipliers']])
 assert all(v>=0 for v in y)
 assert beta*s.ones(D,1)-H.T*y-E.T*z==s.eye(D)[:,0]
 bound=beta*D/2;assert bound==s.Rational(rec['upper_a0'])
 print(n,bound,'EXCLUDED'if bound<1 else 'NOT EXCLUDED',flush=True)
