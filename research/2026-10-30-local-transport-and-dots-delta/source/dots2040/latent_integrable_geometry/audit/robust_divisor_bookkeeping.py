"""Exact hostile bookkeeping checks, not a numerical group-law implementation."""
import json
import sympy as s
x,z=s.symbols('x z')
g=2
F=s.prod(x-k for k in range(6)).expand()
H=s.sqrt(s.expand(z**6*F.subs(x,1/z)))
hseries=s.series(H,z,0,10).removeO()
A_cancel=s.expand(sum(hseries.coeff(z,k)*x**(4-k) for k in range(5)))
cases=[
 ('polynomial_branch_common_factor',x*(x-1),s.Integer(0)),
 ('y_times_branch_common_factor',s.Integer(0),x),
 ('one_infinity_high_order',A_cancel,x),
 ('ordinary_common_factor',(x-s.Rational(1,2))*(x*x+1),x-s.Rational(1,2)),
]
out=[]
for name,A,B in cases:
 A=s.expand(A); B=s.expand(B)
 C=s.gcd(A,B); C=s.Poly(C,x).monic().as_expr()
 A0=s.cancel(A/C); B0=s.cancel(B/C)
 R=s.expand(A*A-F*B*B)
 R0=s.expand(A0*A0-F*B0*B0)
 assert R!=0
 assert s.gcd(A0,B0)==1
 nozero=True if B0==0 else s.degree(s.gcd(R0,B0),x)==0
 assert nozero
 # Exact local section expansions at both infinities; H has rational coefficients.
 sp=s.expand(z**4*A.subs(x,1/z)+hseries*z*B.subs(x,1/z))
 sm=s.expand(z**4*A.subs(x,1/z)-hseries*z*B.subs(x,1/z))
 def order(poly):
  return min(k for k in range(9) if s.expand(poly).coeff(z,k)!=0)
 op,om=order(sp),order(sm)
 assert op+om==8-s.degree(R,x)
 assert s.degree(R,x)+op+om==8
 # gcd factors at simple F roots have twice the x multiplicity locally.
 common_branch=s.gcd(C,F)
 out.append(dict(case=name,A=str(A),B=str(B),common_factor=str(C),
  branch_common_factor=str(common_branch),norm_degree=int(s.degree(R,x)),
  infinity_orders=[op,om],total_section_zero_degree=8,
  reduced_sheet_denominator_coprime=True))
print(json.dumps(dict(status='exact bookkeeping only; no full arithmetic claim',curve=str(F),results=out),indent=2))
