#!/usr/bin/env python3
"""Independent exact checks for the frozen principal-density bridge.

The principal identity uses an arbitrary symmetric 4x4 Hessian and all 12
constant spatial/output coefficients. No source certificate is an input.
"""
from itertools import combinations, permutations
from pathlib import Path
import json
import sympy as s

ROOT = Path(__file__).resolve().parent
z = s.symbols('z0:6')
hs = s.symbols('H0:10')
H = s.zeros(4)
for value, (i, j) in zip(hs, combinations(range(5), 2)):
    # Convert the ten strict pairs in range(5) to symmetric pairs in range(4).
    H[i, j-1] = H[j-1, i] = value
assert len(set(H)) == 10
C11 = s.Matrix(2, 2, s.symbols('c11_0:4'))
C12 = s.Matrix(2, 2, s.symbols('c12_0:4'))
C22 = s.Matrix(2, 2, s.symbols('c22_0:4'))
Cs = [[C11, C12], [C12, C22]]
B = [s.Matrix([z[0], z[1], z[3], z[4]]),
     s.Matrix([z[1], z[2], z[4], z[5]])]
Z = [s.Matrix([[z[0], z[1]], [z[1], z[2]]]),
     s.Matrix([[z[3], z[4]], [z[4], z[5]]])]
div_DF = s.Matrix([
    sum(H[2*alpha+k, 2*beta+l]*Z[beta][l, k]
        for k in range(2) for beta in range(2) for l in range(2))
    for alpha in range(2)])
flow = sum((Cs[i][j]*s.Matrix([Z[alpha][i, j] for alpha in range(2)])
            for i in range(2) for j in range(2)), s.zeros(2, 1))
P = (div_DF.T*flow)[0]
E = sum((B[i].T*H*s.kronecker_product(Cs[i][j], s.eye(2))*B[j])[0]
        for i in range(2) for j in range(2))

# eta is written in row-major matrix coordinates; q = vec(DF).
q = s.Matrix(s.symbols('q0:4'))
q1, q2 = s.Matrix([q[0], q[2]]), s.Matrix([q[1], q[3]])
eta1 = C12.T*q1-C11.T*q2
eta2 = C22.T*q1-C12.T*q2
eta = s.Matrix([eta1[0], eta2[0], eta1[1], eta2[1]])
deta = s.zeros(4)
for r, t in combinations(range(4), 2):
    deta[r, t] = sum(s.diff(eta[t], q[k])*H[k, r]
                    -s.diff(eta[r], q[k])*H[k, t] for k in range(4))
    deta[t, r] = -deta[r, t]
assert s.expand(P-E-(B[0].T*deta*B[1])[0]) == 0

# Constant-coefficient Hessian symbol: 21 quadratic jet monomials -> 15.
aa, bb, xi, yi = s.symbols('aa bb xi yi')
pure = [aa*xi**2, aa*xi*yi, aa*yi**2,
        bb*xi**2, bb*xi*yi, bb*yi**2]
polys = [s.expand(pure[i]*pure[j])
         for i in range(6) for j in range(i, 6)]
mons = sorted(set(mon for pol in polys for mon, _ in
                  s.Poly(pol, aa, bb, xi, yi).terms()))
SM = s.Matrix([[s.Poly(pol, aa, bb, xi, yi).coeff_monomial(mon)
                for pol in polys] for mon in mons])
assert SM.shape == (15, 21) and SM.rank() == 15

# Closedness of a pullback null form is forced by independent third jets.
Ts = s.symbols('T012 T013 T023 T123')
Td = {}
for tri, value in zip(combinations(range(4), 3), Ts):
    for perm in permutations(tri):
        inv = sum(perm[i] > perm[j] for i in range(3) for j in range(i+1, 3))
        Td[perm] = (-1)**inv*value
tvec = [s.expand(sum(Td.get((i, k, l), 0)*B[0][k]*B[1][l]
                     for k in range(4) for l in range(4))) for i in range(4)]
y = s.symbols('y0:8')
zx, zy = [y[0], y[1], y[2], y[4], y[5], y[6]], [y[1], y[2], y[3], y[5], y[6], y[7]]
E1 = s.expand(sum(s.diff(tvec[0], z[i])*zx[i]
                  +s.diff(tvec[1], z[i])*zy[i] for i in range(6)))
selected = [s.expand(E1).coeff(zz).coeff(yy)
            for zz, yy in [(z[0], y[6]), (z[0], y[7]),
                           (z[3], y[6]), (z[3], y[7])]]
assert selected == [-Ts[0], -Ts[1], Ts[2], Ts[3]]

# Smooth, strongly parabolic variable-coefficient counterexample to P=E
# after integration. This is a density warning, not a counterexample to
# the frozen-density obstruction.
x, yvar, t = s.symbols('x y t', real=True)
phi1 = t*(s.sin(x)+s.sin(yvar))
phi2 = t*s.sin(x)*s.cos(yvar)
a, b = s.diff(phi1, x), s.diff(phi1, yvar)
u1xx, u1xy, u1yy = [s.diff(phi1, *axes) for axes in [(x, x), (x, yvar), (yvar, yvar)]]
u2xy, u2yy = s.diff(phi2, x, yvar), s.diff(phi2, yvar, yvar)
diff_density = 12*a**2*(u1xx*u1yy-u1xy**2
                             +b*(u1xx*u2yy-u1xy*u2xy))
integral = s.simplify(s.integrate(s.integrate(s.expand_trig(diff_density),
                                  (x, 0, 2*s.pi)), (yvar, 0, 2*s.pi)))
assert s.simplify(integral-3*s.pi**2*t**5) == 0

receipt = {
    'status': 'EXACT_PASS',
    'principal_bridge': 'P_C-E_C = d eta_C(B1,B2)',
    'scope': 'All symmetric Hessians and all 12 constant real output/spatial coefficients; no SOS hypothesis.',
    'symbol_dimensions': list(SM.shape),
    'symbol_rank': 15,
    'closedness_independent_third_jet_coefficients': [str(v) for v in selected],
    'variable_coefficient_warning': {
        'F': 'a^4', 'C11': 'I', 'C12': '0', 'C22': 'I + b E12',
        'periodic_potential': ['t(sin x + sin y)', 't sin x cos y'],
        'integral_P_minus_E': str(integral),
        'parabolicity': 'sym symbol >= (1-|b|/2)|n|^2 I, hence >= |n|^2 I/2 for |b|<=1'
    }
}
(ROOT/'density_bridge_receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt, indent=2))
