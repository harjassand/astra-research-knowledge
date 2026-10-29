from pathlib import Path
import sympy as s,json
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
e0=s.Matrix([1,0]);e1=s.Matrix([0,1]); basis=[s.Matrix([1,0,0,1])/s.sqrt(2),s.Matrix([1,0,0,-1])/s.sqrt(2)]
# Choi ordering output, memory, reference; embed Bell output/reference with memory.
def embed(v):
 T=s.zeros(8,2)
 for o in range(2):
  for m in range(2):
   for r in range(2):T[4*o+2*m+r,m]=v[2*o+r]
 return T
T0,Tz=map(embed,basis)
def choi(K):
 v=s.Matrix([K[o*2+m,r] for o in range(2) for m in range(2) for r in range(2)])/s.sqrt(2)
 return v*v.H
count=0
for a,t in [(s.Rational(4,5),s.Rational(3,5)),(s.Rational(12,13),s.Rational(5,13)),(1/s.sqrt(2),1/s.sqrt(2))]:
 p=t*t; A=s.kronecker_product(I,a*e0)+s.kronecker_product(Z,t*e1)
 for c,u in [(s.Rational(12,13),s.Rational(5,13)),(s.Rational(24,25),s.Rational(7,25)),(s.Rational(4,5),s.Rational(3,5))]:
  b=u*u; W=c*I-s.I*u*Z
  learned=s.zeros(8); exact=s.zeros(8)
  for Q in [I,X,Y,Z]:
   learned+=choi(s.kronecker_product(Q.H*W,I)*A*Q)/4
   exact+=choi(s.kronecker_product(Q.H,I)*A*Q)/4
  D=s.Matrix([[-b*(1-p),s.I*c*u*a*t],[-s.I*c*u*a*t,b*p]])
  assert s.simplify(learned-exact-T0*D*T0.H+Tz*D*Tz.H)==s.zeros(8)
  l=s.Matrix([c*a,-s.I*u*t]); diff=l*l.H-c*c*(1-p)*e0*e0.H
  assert s.simplify(diff.det()+c*c*u*u*p*(1-p))==0
  assert diff.det()<0
  # Opposite-sign eigenvalues: squared trace norm = trace^2 - 4det.
  assert s.simplify(D.trace()**2-4*D.det()-b*(b*(1-2*p)**2+4*p*(1-p)))==0
  count+=1
result={'status':'PASS_INDEPENDENT_EXACT_COMPLETE_TWIRL','rational_or_algebraic_fixtures':count,'whole_choi_twirl_checked':True,'negative_cp_difference_determinants':count,'distance_formula_checked':True,'source_calls':0,'scope':'Exact finite isometry algebra; no learning, hardware or future-accessibility claim.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
