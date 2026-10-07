"""Exact rational LP diagnostics of sel:exponents; not an analytic proof."""
from sympy import symbols, Rational as Q, linear_eq_to_matrix, Matrix
from sympy.solvers.simplex import linprog, InfeasibleLPError
alpha,b,y,H,z,c,t=symbols('alpha b y H z c t')
xs=(alpha,b,y,H,z,c,t)
Delta=Q(1,100000)*(alpha+b+y+H)
core=[2*alpha+H/2+2*y-z-Delta+t,
      2*H/3+z/6-Delta/3-b+t,
      b-H-2*y+z/2-Delta+t]
aeq,beq=linear_eq_to_matrix([z+c-1],xs)
objective=Matrix([[0,0,0,0,0,0,-1]])
def solve(tag,extra):
 a,rhs=linear_eq_to_matrix(core+extra,xs)
 try:
  value,sol=linprog(objective,a,rhs,aeq,beq)
  checks=all(expr.subs(dict(zip(xs,sol)))<=0 for expr in core+extra)
  assert checks
  print(tag,'maximum common strictness margin =',-value,'witness =',dict(zip(xs,sol)))
 except InfeasibleLPError:
  print(tag,'infeasible even after replacing every strict inequality with <=')
# H<=2c energy branch; unsafe is impossible strictly.
solve('energy branch H<=2c',[b-H/2+alpha-Delta+t,H-2*c])
# H>2c branch leaves actual unsafe candidates without improved occupation.
solve('energy branch H>2c',[b-H+c+alpha-Delta+t,2*c-H+t])
# Final improved far constraint, relaxed by dropping nonnegative min(alpha,c).
# This test assumes improved occupation has already been justified; it does not check its window.
solve('H>2c plus improved far bound',[b-H+c+alpha-Delta+t,2*c-H+t,b-H/2-Q(29,50)*y-Delta+t])
print('Scope: exact rational check of finite exponent inequalities only. No continuum occupation or uniform-threshold estimate is certified.')
