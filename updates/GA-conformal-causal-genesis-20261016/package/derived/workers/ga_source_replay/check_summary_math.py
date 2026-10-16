"""Independent arithmetic checks on the displayed summary and packet values.

These overlap the producer verifier. They do not certify any analytic theorem.
"""
from pathlib import Path
from fractions import Fraction
from math import comb
import hashlib
import json
import sympy as sp

ROOT = Path(__file__).resolve().parent
checks = []


def require(name, condition, values=None):
    if not condition:
        raise RuntimeError(name)
    checks.append({'name': name, 'status': 'PASS', 'values': values})


a, b, c, d, r = sp.symbols('a b c d r')
j = a*d-b*c
u = a*a+c*c
J = 3*r*((a-d)**2+(b+c)**2)**2/(8*(r+2)) + r*(r-1)*u*u/6 + j*j + r*u*j
C = sp.diff(J, a)+sp.diff(J, d)
Q = (sp.diff(J, a, 2)+2*sp.diff(J, a, d)+sp.diff(J, d, 2))/2
q = (r+1)*a+d
kappa = r*(r+2)/3
require('general raw quadratic coefficient',
        sp.factor(Q-q*q-kappa*c*c-(r+2)*j) == 0)
U = 2*a*q-(r+2)*a*a+r*c*c-2*b*c
require('general cubic decomposition',
        sp.factor(C-q*U+kappa*a*(a*a+c*c)) == 0)

F = Fraction
A, C1, Q1 = F(14054717889, 640000), F(282507, 80), F(16569, 80)
ratio = C1*C1/(4*A*Q1)
background = -C1/(2*Q1)
gap = A-C1*C1/(4*Q1)
require('displayed P1 moment arithmetic',
        ratio == F(17735601122000, 25874735633649)
        and background == -F(94169, 11046)
        and gap == F(8139134511649, 1178240000)
        and F(2, 3) < ratio < 1,
        {'ratio': str(ratio), 'background': str(background), 'gap': str(gap)})


def convolution(first, second):
    out = {}
    for k, value in first.items():
        for ell, other in second.items():
            out[k+ell] = out.get(k+ell, F(0)) + value*other
    return out


# F(y)=cos(y/2)^16. The derivative's Fourier coefficients are i*k*Fhat[k].
carrier = {k: F(comb(16, 8+k), 2**16) for k in range(-8, 9)}
derivative_over_i = {k: k*value for k, value in carrier.items()}
square = convolution(carrier, carrier)
derivative_square = convolution(derivative_over_i, derivative_over_i)
moment2 = square[0]
moment4 = convolution(square, square)[0]
derivative_moment4 = convolution(derivative_square, derivative_square)[0]
mixed_moment = -convolution(square, derivative_square)[0]
n = 4
stress = (moment4-moment2*moment2)/4 + mixed_moment/(8*n*n)
fourA = 3*moment4/16 + mixed_moment/(8*n*n) + 3*derivative_moment4/(16*n**4)
require('independent Laurent integration of carrier stress gap',
        stress-fourA == F(159381921467360331, 147573952589676412928),
        {'gap': str(stress-fourA), 'stress_over_4A': float(stress/fourA),
         'scope': 'integrates the specified simplified stress; analytic stress identity is separate'})

receipt = {
    'schema': 'ga-summary-math-arithmetic/1',
    'status': 'PASS',
    'groups': len(checks),
    'checks': checks,
    'self_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope': 'Independent finite arithmetic on displayed formulas. Overlaps the 21-group producer replay. No new analytic proof or universal sharp estimate.',
}
(ROOT/'SUMMARY_MATH_CHECKS.json').write_text(json.dumps(receipt, indent=2)+'\n')
print('PASS', len(checks), 'independent summary arithmetic groups')
