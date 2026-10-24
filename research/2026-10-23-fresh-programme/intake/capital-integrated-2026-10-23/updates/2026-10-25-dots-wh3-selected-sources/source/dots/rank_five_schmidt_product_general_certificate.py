"""All-Schmidt exact coherence-monotonicity certificate, no numeric optimization."""
import sympy as s,json
a,b,v,t,x,y,z=s.symbols('a b v t x y z',nonnegative=True)
S=x+y+z;A=x+y;B=y+z
DY=t*t+(a*S+b)*t+S*v
D2=t*t+(a*A+b)*t+A*v
DR=t*t+(a*A+b)*t+y*v+a*a*x*y
D3=(a*z+t)*(B*v+t*(a*S+b+t))+a*a*x*y*t
N=s.expand(-S*D2*DR*D3+A*DY*DR*D3+B*(a*z+t)*DY*D2*DR-y*DY*D2*D3)
SOS=x*z*a*b*b*t*t*(a*y-t)**2
remainder=s.Poly(s.expand(N-SOS),a,b,v,t,x,y,z)
assert all(c>=0 for c in remainder.coeffs())
assert s.expand(N-SOS-remainder.as_expr())==0
integrand=-S/DY+A/D2+B*(a*z+t)/D3-y/DR
assert s.factor(integrand-N/(DY*D2*DR*D3))==0
# Retain a compact grouped representation for human checking.
grouped=s.Poly(s.cancel((N-SOS)/(x*z)),a,b,v,t)
assert all(c>=0 for coeff in grouped.coeffs() for c in s.Poly(coeff,x,y,z).coeffs())
terms=[{'powers_a_b_v_t':powers,'coefficient_xyz':str(s.factor(coeff))} for powers,coeff in grouped.terms()]
result=dict(exact_cleared_denominator_identity=True,exact_square_decomposition=True,square=str(SOS),nonnegative_monomials=len(remainder.terms()),grouped_nonnegative_remainder_after_factoring_xz=terms,scope='All nonnegative Schmidt weights x,y,z with positive sum; apply normalization at the end. Product direction is one off-diagonal Schmidt-basis product, not an arbitrary superposition.')
print(json.dumps(result,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(result,indent=2)+'\n')
