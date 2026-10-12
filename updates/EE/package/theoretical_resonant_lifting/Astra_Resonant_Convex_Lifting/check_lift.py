"""Exact symbolic diagnostics for the resonant convex Hamiltonian lift.
These finite examples check algebra; the general theorem requires the written proof.
"""
import json
from pathlib import Path
import sympy as s

q = s.Matrix(s.symbols('q0:4'))
p = s.Matrix(s.symbols('p0:4'))
v = s.Matrix(s.symbols('v0:4'))
B = []
for ell in range(4):
    M = s.zeros(4)
    for i in range(1,4):
        for j in range(i+1,4):
            M[i,j] = (ell+1)*(i-j) + (i+j if ell % 2 else -i)
            M[j,i] = -M[i,j]
    B.append(M)

def mat(x):
    return sum((x[l]*B[l] for l in range(4)), s.zeros(4))
def field(x):
    return x[0]*mat(x)*x

K = s.expand((p.dot(field(q)) - q.dot(field(p))))
Kfact = sum((q[0]*q[l]+p[0]*p[l])*(p.dot(B[l]*q)) for l in range(4))
checks = {}
checks['quartic_factorization'] = s.expand(K-Kfact)==0
checks['energy_tangency'] = s.expand(v.dot(mat(v)*v))==0
checks['anchor_fixed'] = s.expand((mat(v)*v)[0])==0
checks['oscillator_poisson_commutation'] = s.expand(sum(q[i]*s.diff(K,p[i])-p[i]*s.diff(K,q[i]) for i in range(4)))==0
zero_p = {x:0 for x in p}
checks['zero_section_value'] = s.expand(K.subs(zero_p))==0
checks['zero_section_q_gradient'] = all(s.expand(s.diff(K,x).subs(zero_p))==0 for x in q)
checks['zero_section_p_gradient'] = all(s.expand(s.diff(K,p[i]).subs(zero_p)-field(q)[i])==0 for i in range(4))

# Exact tensor lift for a polynomial tangent field on R^2.
x,y = s.symbols('x y')
u=s.Matrix([x,y])
Y=s.Matrix([-y*(1+x+x*y),x*(1+x+x*y)])
A=s.zeros(2)
for deg in range(1,4):
    Yd=s.Matrix([sum(coeff*x**powers[0]*y**powers[1] for powers,coeff in s.Poly(f,x,y).terms() if sum(powers)==deg) for f in Y])
    Jac=Yd.jacobian(u)
    A+=(Jac-Jac.T)/(deg+1)
checks['skew_reconstruction'] = all(s.expand(f)==0 for f in A*u-Y) and A.T==-A
Psi=s.Matrix([1,x,y,x*x,x*y,y*x,y*y])
Bt=s.diag(s.zeros(1), A, s.kronecker_product(A,s.eye(2))+s.kronecker_product(s.eye(2),A))
checks['tensor_chain_rule'] = all(s.expand(f)==0 for f in Psi.jacobian(u)*Y-Bt*Psi)
checks['tensor_norm'] = s.expand(Psi.dot(Psi)-(1+(x*x+y*y)+(x*x+y*y)**2))==0

# Stereographic derivative formula, before time rescaling.
x=s.symbols('x', real=True)
a=(x*x-1)/(1+x*x)
b=2*x/(1+x*x)
checks['circle_derivative_a'] = s.simplify(s.diff(a,x)-b*(1-a))==0
checks['circle_derivative_b'] = s.simplify(s.diff(b,x)+a*(1-a))==0
checks['circle_radius'] = s.simplify(a*a+b*b-1)==0

# Error-window output constants for epsilon=1/8.
checks['nonhalt_margin'] = s.Rational(4,53)<s.Rational(1,8)
checks['off_clock_margin'] = s.Rational(1,16)<s.Rational(1,8)
checks['halt_margin'] = s.Rational(4,5)>s.Rational(3,4)

# Bounded latch and convergent-bit stage: exact algebra and constants.
u, ell, raw, M = s.symbols('u ell raw M', real=True)
latch = 60*M*(2-u)*(u*(u+1)+raw)
checks['latch_lower_boundary'] = s.expand(latch.subs(u,-1)-180*M*raw)==0
checks['latch_upper_boundary'] = s.expand(latch.subs(u,2))==0
checks['latch_nonhalt_barrier'] = s.expand(latch.subs(u,-s.Rational(1,2))-150*M*(raw-s.Rational(1,4)))==0
checks['latch_quadratic_minimum_identity'] = s.expand(u*(u+1)+s.Rational(1,4)-(u+s.Rational(1,2))**2)==0
checks['latch_pulse_time_budget'] = s.Rational(2,25)<s.Rational(1,10)
checks['latch_positive_region_identity'] = s.expand(u*(u+1)-2-(u-1)*(u+2))==0
checks['logistic_logit_identity'] = s.simplify(s.diff(s.log(ell/(1-ell)),ell)*u*ell*(1-ell)-u)==0
checks['convergent_output_initial_gap'] = s.Rational(64,1025)<s.Rational(1,8)
checks['second_time_change_lower_bound'] = s.Rational(1,64)*s.Rational(2,5)**3==s.Rational(1,1000)
checks['convergent_output_monotonicity_identity'] = s.simplify(s.diff(2*ell/(1+ell**2),ell)-2*(1-ell**2)/(1+ell**2)**2)==0

checks = {k:bool(val) for k,val in checks.items()}
report={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'count':len(checks),'scope':'Finite exact symbolic examples only; not a formalization or an executed universal simulator.'}
path=Path(__file__).with_name('symbolic_checks.json')
path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert all(checks.values())
