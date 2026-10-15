#!/usr/bin/env python3
"""Finite checks of identities used in PROOF.md, not a positivity proof."""
from pathlib import Path
import json
import platform
import sympy as sp
import mpmath as mp

HERE = Path(__file__).resolve().parent
s, t = sp.symbols('s t', real=True)
a, b, c = sp.symbols('a b c', real=True)
Q = (s*t - 1)**2 + s**2
checks = {}

def exact_zero(label, expression):
    reduced = sp.simplify(expression)
    checks[label] = {'pass': reduced == 0, 'residual': str(reduced)}
    if reduced != 0:
        raise AssertionError((label, reduced))

exact_zero('completed_square_margin', Q - ((1+t*t)*(s-t/(1+t*t))**2+1/(1+t*t)))

def heat_contraction(expr):
    return a*sp.diff(expr, s, 2)+2*b*sp.diff(expr, s, t)+c*sp.diff(expr, t, 2)

gaussian = Q-heat_contraction(Q)/2+heat_contraction(heat_contraction(Q))/8
gaussian_expected = Q-a*(t*t+1)-c*s*s-4*b*s*t+2*b+a*c+2*b*b
exact_zero('arbitrary_gaussian_identity', gaussian-gaussian_expected)
checks['gaussian_axis_leading_coefficient'] = str(sp.expand(gaussian.subs(s, 0)).coeff(t, 2))
assert sp.expand(gaussian.subs(s, 0)).coeff(t, 2) == -a

x, y = sp.symbols('x y', real=True)
V = sp.Function('V')(x, y)
p = sp.exp(-V)
gx, gy = sp.diff(V,x), sp.diff(V,y)
v11, v22, v12 = sp.diff(V,x,2),sp.diff(V,y,2),sp.diff(V,x,y)
v112,v122,v1122 = sp.diff(V,x,2,y),sp.diff(V,x,y,2),sp.diff(V,x,2,y,2)
direct = (sp.diff(p,x,2,y,2)-2*sp.diff(p,x,y)+p+sp.diff(p,x,2))/p
bell = ((gx*gy-1)**2+gx*gx-v11*(gy*gy+1)-v22*gx*gx
        +(2-4*gx*gy)*v12+v11*v22+2*v12*v12+2*gy*v112+2*gx*v122-v1122)
exact_zero('quartic_bell_identity',direct-bell)

z = sp.symbols('z', real=True)
rho = sp.sqrt(1+z*z)
f = rho*sp.log(rho)
exact_zero('canonical_first_derivative',sp.diff(f,z)-(1+sp.log(rho))*z/rho)
exact_zero('canonical_second_derivative',sp.diff(f,z,2)-(1/rho+sp.log(rho)/rho**3))

sx=sp.Matrix([[0,1],[1,0]])
sy=sp.Matrix([[0,-sp.I],[sp.I,0]])
free_example=sp.eye(2)+sp.I*(sx*sy-sy*sx)
checks['free_commutator_eigenvalues'] = sorted(int(v) for v in free_example.eigenvals())
assert checks['free_commutator_eigenvalues']==[-1,3]

# Evaluate the exact Bell formula at the valley g=(1/t,t). No tiny density
# values are exponentiated; the displayed quantity is Q(-D)p/p.
mp.mp.dps=100
beta=sp.symbols('beta',positive=True)
f_beta=((1+x*x+y*y)**((1+beta)/2)-1)/(1+beta)
orders=[(2,0),(0,2),(1,1),(2,1),(1,2),(2,2)]
jet_funcs=[sp.lambdify((x,y,beta),sp.diff(f_beta,x,aa,y,bb),'mpmath') for aa,bb in orders]
power_rows=[]
for beta_text in ('0.2','0.25'):
    beta_value=mp.mpf(beta_text)
    L=mp.mpf(10)
    for power in (5,10,20,40):
        R=mp.power(10,power)
        rho_value=mp.sqrt(1+R*R)
        q=R*rho_value**(beta_value-1)
        tt=mp.sqrt((q*q+mp.sqrt(q**4-4))/2)
        xx,yy=R/(q*tt),R*tt/q
        jets=[fn(xx,yy,beta_value)/L**(aa+bb-1) for fn,(aa,bb) in zip(jet_funcs,orders)]
        h11,h22,h12,h112,h122,h1122=jets
        value=(tt**-2-h11*(tt*tt+1)-h22/tt**2-2*h12
               +h11*h22+2*h12*h12+2*tt*h112+2*h122/tt-h1122)
        leading=tt**-2-tt**3/(L*R)
        power_rows.append({'beta':beta_text,'L':'10','z_radius_power10':power,
            'exact_ratio_approx':mp.nstr(value,25),
            'two_term_asymptotic':mp.nstr(leading,25),
            'negative_over_positive_scale':mp.nstr(tt**5/(L*R),25),
            'scaled_value_t2':mp.nstr(value*tt**2,25)})
checks['power_tail_numeric_diagnostics']=power_rows
assert mp.mpf(power_rows[3]['exact_ratio_approx'])>0
assert mp.mpf(power_rows[-1]['exact_ratio_approx'])<0

# Numeric witnesses for the infinite-dimensional canonical-template failure.
# These finite rows illustrate the proved asymptotic; they are not the proof.
infinite_rows=[]
for L_text in ('1','1000000'):
    LL=mp.mpf(L_text)
    for n in (5,10,20):
        def slope(zz):
            rr=mp.sqrt(1+zz*zz)
            return zz/rr*(1+mp.log(rr))
        zn=mp.findroot(lambda zz:slope(zz)-n,(mp.exp(n-1)*mp.mpf('0.9'),mp.exp(n-1)*mp.mpf('1.1')))
        rr=mp.sqrt(1+zn*zn)
        curvature=(1/rr+mp.log(rr)/rr**3)/LL
        diagonal=(mp.exp(-2*n*n)-curvature)/(n*n+mp.exp(-2*n*n))
        infinite_rows.append({'L':L_text,'n':n,'output_entry_over_p':mp.nstr(diagonal,25),
                              'curvature':mp.nstr(curvature,25)})
        assert diagonal<0
checks['infinite_operator_numeric_witnesses']=infinite_rows

result={'status':'PASS','scope':'Finite symbolic identities and illustrative high-precision evaluations only; not formal verification or a global numerical certificate.',
        'python':platform.python_version(),'sympy':sp.__version__,'mpmath':mp.__version__,'checks':checks}
(HERE/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
