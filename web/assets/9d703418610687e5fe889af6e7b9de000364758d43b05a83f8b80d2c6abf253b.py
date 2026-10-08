"""Scoped symbolic diagnostics for the independently derived identities.

These are algebra checks, not a formal proof of the spectral existence theorem.
Run: python3 work/agents/spectral_crossblock_audit/checks/exact_algebra.py
"""
import json
from pathlib import Path
import sympy as s

l=s.symbols('l', positive=True, integer=True)
z=s.symbols('z', real=True)
q=s.symbols('q', nonnegative=True, real=True)
x=s.symbols('x', real=True)
a=s.Function('a')(x)
F=(1-z*z)**l
delta_F=(1-z*z)*s.diff(F,z,2)-2*z*s.diff(F,z)
raw_recurrence=s.simplify(delta_F+2*l*(2*l+1)*F-4*l*l*(1-z*z)**(l-1))
# SymPy leaves equivalent powers of the same base unnested when its sign is
# unspecified. On the sphere away from the poles, u=1-z^2 is positive; after
# this exact substitution the residual simplifies. The polynomial identity
# then extends to the poles by continuity for integer l.
u=s.symbols('u',positive=True)
recurrence=s.simplify(raw_recurrence.subs(z,s.sqrt(1-u)))
assert recurrence==0

b=s.diff(a,x)/a
potential=s.simplify(s.diff(b,x)+b*b+s.cot(x)*b)
expected=(s.diff(a,x,2)+s.cot(x)*s.diff(a,x))/a
assert s.simplify(potential-expected)==0

gap_numerator=s.expand((4*l+10)*(2*l-3)**2-(12*l-9)*(l+1)*(l+2))
assert gap_numerator==4*l**3-35*l**2-81*l+108
assert gap_numerator.subs(l,11)>0
assert s.diff(gap_numerator,l).subs(l,11)>0
assert s.diff(gap_numerator,l,2).subs(l,11)>0
ratio_derivative=s.factor(s.diff(q*(q+1)/(4*q+6),q))
assert s.simplify(ratio_derivative-(4*q*q+12*q+6)/(4*q+6)**2)==0

j=s.symbols('j', integer=True, nonnegative=True)
dimension_target=s.summation(4*j+1,(j,0,l))
dimension_source=(2*l+1)*(2*l+2)/2
assert s.simplify(dimension_source-dimension_target)==0

parity_checks=[]
for degree in range(101):
    same=sum(2*k+1 for k in range(degree+1) if (k-degree)%2==0)
    opposite=sum(2*k+1 for k in range(degree+1) if (k-degree)%2!=0)
    assert same==(degree+1)*(degree+2)//2
    assert opposite==degree*(degree+1)//2
    assert same+opposite==(degree+1)**2
parity_checks.append('counts checked exactly for degrees 0 through 100')

result={
    'status':'all scoped algebra checks passed',
    'harmonic_product_casimir_residual':str(recurrence),
    'casimir_normalization':'positive base u=1-z^2; poles handled by polynomial continuity',
    'liouville_potential_residual':str(s.simplify(potential-expected)),
    'uniform_same_parity_gap_polynomial':str(gap_numerator),
    'gap_polynomial_at_11':int(gap_numerator.subs(l,11)),
    'gap_polynomial_first_derivative_at_11':int(s.diff(gap_numerator,l).subs(l,11)),
    'gap_polynomial_second_derivative_at_11':int(s.diff(gap_numerator,l,2).subs(l,11)),
    'gap_ratio_derivative':str(ratio_derivative),
    'product_dimension_residual':str(s.simplify(dimension_source-dimension_target)),
    'parity_count_checks':parity_checks,
    'limitations':'Symbolic algebra and finite count checks only; not a proof certificate of analytic spectral assertions.'
}
output=Path(__file__).with_name('exact_algebra_results.json')
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
