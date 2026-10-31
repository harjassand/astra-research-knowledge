#!/usr/bin/env python3
"""Independent algebra and finite diagnostics; the accompanying proof carries universality.
No PDE solver and no sampled inequality is promoted to a proof.
"""
import json
import math
import random
from fractions import Fraction
from pathlib import Path
import sympy as sp
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent
checks = {}
y, z, k, eps, a, b = sp.symbols('y z k eps a b', real=True)
v = 1 + (1-y*y)**2
F = v*z*z/2
D = sp.Matrix([[1,k],[k,k*k/(1-eps)]])
x = sp.Matrix([y,z])
V = 1 + (x.T*D.inv()*x)[0]
gradF = sp.Matrix([sp.diff(F,t) for t in (y,z)])
gradV = sp.Matrix([sp.diff(V,t) for t in (y,z)])
LV = sp.trace(D*sp.hessian(V,(y,z))) - (gradV.T*D*gradF)[0]
expected = 4-(6*(y*y-sp.Rational(2,3))**2+sp.Rational(4,3))*z*z
assert sp.factor(LV-expected) == 0
checks['special_family_Lyapunov_exact'] = True
D00, D01, D11 = sp.symbols('D00 D01 D11', real=True)
Dgeneral = sp.Matrix([[D00,D01],[D01,D11]])
Vgeneral = 1+(x.T*Dgeneral.inv()*x)[0]
gradVgeneral = sp.Matrix([sp.diff(Vgeneral,t) for t in (y,z)])
LVgeneral = sp.trace(Dgeneral*sp.hessian(Vgeneral,(y,z))) - (gradVgeneral.T*Dgeneral*gradF)[0]
assert sp.factor(LVgeneral-expected)==0
checks['every_constant_SPD_Lyapunov_exact'] = True
assert sp.factor(v-1-(1-y*y)**2) == 0
assert sp.factor(v-y**4/2-(y*y-2)**2/2) == 0
checks['global_v_lower_bounds_exact'] = True
assert sp.factor(D.det()-k*k*eps/(1-eps)) == 0
checks['SPD_determinant_exact'] = True
alpha = (1-eps)/k
g = sp.Matrix([a+b,-alpha*a])
q = (g.T*D*g)[0]
assert sp.factor(q-(eps*a*a+2*eps*a*b+b*b)) == 0
assert sp.factor(q-(eps*(a+b)**2+(1-eps)*b*b)) == 0
checks['patched_gradient_energy_exact'] = True
hy, hz = sp.symbols('hy hz', real=True)
g0 = sp.Matrix([hy,hz])
q0 = (g0.T*D*g0)[0]
assert sp.factor(q0-eps*hy*hy-D[1,1]*(hz+alpha*hy)**2) == 0
assert sp.factor(q0-(hy+k*hz)**2-(D[1,1]-k*k)*hz*hz) == 0
checks['Schur_and_tilted_line_decompositions_exact'] = True

# Direct finite checks on the explicitly smooth cutoff used in the proof.
def psi(t):
    return math.exp(-1/(1-16*t*t)) if abs(t)<0.25 else 0.0
norm = quad(psi,-0.25,0.25,epsabs=1e-13)[0]
def u(t):
    if t <= -0.25: return 0.0
    if t >= 0.25: return 1.0
    return quad(psi,-0.25,t,epsabs=1e-12)[0]/norm
def up(t): return psi(t)/norm
def chi(y0): return 1-u(4*(abs(y0)-7/16))
def chip(y0):
    if y0 == 0: return 0.0
    return -4*up(4*(abs(y0)-7/16))*(1 if y0>0 else -1)
def h(y0,z0,k0,e0):
    c = chi(y0)
    return c*u(y0-(1-e0)*z0/k0)+(1-c)*u(y0)
for y0 in (-100,-1,-0.5,0.5,1,100):
    expected0 = float(y0>0)
    for z0 in (-1e8,-100,-1,0,1,100,1e8):
        for k0,e0 in ((1,0.01),(2,0.99),(100,0.5)):
            assert h(y0,z0,k0,e0)==expected0
checks['full_fiber_boundary_samples_including_extreme_z'] = True
assert up(0)<6
rng = random.Random(20261031)
max_patch_q = 0.0
for _ in range(2500):
    y0 = rng.choice((-1,1))*rng.uniform(3/8,1/2)
    k0 = rng.choice((1,2,4,8,16))
    e0 = rng.uniform(0.0001,0.9999)
    z0 = rng.uniform(-40,40)
    s = y0-(1-e0)*z0/k0
    aa = chi(y0)*up(s)
    bb = chip(y0)*(u(s)-u(y0))
    energy = e0*aa*aa+2*e0*aa*bb+bb*bb
    assert energy>=-1e-10 and energy<=900+1e-8
    if abs(aa)+abs(bb)>1e-10:
        assert abs(z0)>=k0/8-1e-10
    max_patch_q=max(max_patch_q,energy)
checks['patch_energy_and_rare_support_2500_samples'] = True

# The rational report uses e^{-x} <= 2^{-floor(x)}; exact arithmetic thereafter.
report=[]
for kval in (16,32,64,128,256):
    e = Fraction(1,kval)
    tail = Fraction(1,2**(kval*kval//128))
    upper = 36*e+Fraction(1200,kval)*tail
    lower = e/16
    report.append({'k':kval,'epsilon':str(e),'capacity_lower_rational':str(lower),
                   'capacity_upper_rational':str(upper),
                   'conductance_upper_rational':str(4*upper)})
checks['rational_receiving_examples_exact_after_exponential_majorant'] = True

Z = quad(lambda t: math.sqrt(2*math.pi/(1+(1-t*t)**2)), -math.inf,math.inf,epsabs=1e-10)[0]
ZA = quad(lambda t: math.sqrt(2*math.pi/(1+(1-t*t)**2)), -math.inf,-0.5,epsabs=1e-10)[0]
assert Z>3 and Z<16 and ZA/Z>=0.25
checks['partition_and_mass_quadrature_diagnostic_only'] = True
result={'status':'PASS','checks':checks,'smooth_u_max_derivative':up(0),
        'max_sampled_patch_energy':max_patch_q,
        'diagnostic_Z':Z,'diagnostic_mu_A':ZA/Z,
        'rational_examples':report,
        'limits':'Symbolic equalities and rational arithmetic are exact. Sampling/quadrature are diagnostics, not proof substitutes. No capacity PDE was solved.'}
(HERE/'independent_check_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
