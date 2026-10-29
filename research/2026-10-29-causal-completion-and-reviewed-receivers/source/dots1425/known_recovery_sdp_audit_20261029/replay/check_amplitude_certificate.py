import sympy as s,json
rows=[]
for a in [s.Rational(i,10) for i in range(11)]+[s.Rational(4,5)]:
 b2=1-a*a
 W=s.zeros(4);W[0,0]=s.Rational(1,4);W[0,3]=W[3,0]=a/4;W[3,3]=a*a/4;W[1,1]=b2/4
 v=s.Matrix([1,0,0,1]);J=v*v.T
 Y=s.diag((1+a)/4,a*(1+a)/4);Z=s.kronecker_product(Y,s.eye(2))-W
 assert all(x>=0 for x in Z.eigenvals())
 primal=s.trace(W*J);dual=s.trace(Y);assert primal==dual==(1+a)**2/4
 for i in range(2):
  for j in range(2):assert sum(J[o+2*i,o+2*j] for o in range(2))==int(i==j)
 # a=0 makes the displayed invertible-output Petz formula require support completion; skip it.
 petz=((a+1/s.sqrt(2-a*a))**2+b2*b2/(2-a*a))/4 if a else None
 rows.append(dict(a=str(a),optimum=str(primal),dual_spectrum=[str(x) for x in Z.eigenvals()],petz_decimal=None if petz is None else float(petz)))
print(json.dumps(dict(scope='Exact rational primal/dual certificates; Petz decimal is supplementary',rows=rows),indent=2))
