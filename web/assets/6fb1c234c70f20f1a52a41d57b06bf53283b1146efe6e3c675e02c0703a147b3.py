#!/usr/bin/env python3
"""Exact algebra replay of the blind angular reduction, not a PI proof."""
import json
import sympy as s

checks = []


def equal(a, b, label):
    delta = a - b
    ok = (all(s.simplify(x) == 0 for x in delta) if isinstance(delta, s.MatrixBase)
          else s.simplify(delta) == 0)
    assert ok, (label, s.simplify(delta))
    checks.append(label)


g = s.symbols('g', positive=True)
x, y, z, pop, coh = s.symbols('x y z pop coh', real=True)
rad, v, angle_sine, nu, R, K, bound = s.symbols('r v h nu R K c', real=True)
X = s.Matrix([[0, 1], [1, 0]])
Z = s.diag(1, -1)
N = s.Matrix([[z, x - s.I * y], [x + s.I * y, -z]])
ref_s = s.diag(g, 1)
mu = (g - 1) / (g + 1)
lam = 2 * s.sqrt(g) / (g + 1)
ref_b = 2 * g / (g ** 2 + 1)
ref_q = (g ** 2 - 1) / (g ** 2 + 1)
Cosh = (g + 1 / g) / 2
Sinh = (g - 1 / g) / 2
VN = s.Matrix([[z ** 2 + (x ** 2 + y ** 2) / g, 2 * mu * z * (x - s.I * y)],
               [2 * mu * z * (x + s.I * y), z ** 2 + g * (x ** 2 + y ** 2)]])
equal(VN * ref_s + ref_s * VN, 2 * N * ref_s * N, 'exact Lyapunov noise coefficient')
S = s.diag(s.sqrt(g), 1)
noise = S * N * S.inv()
left = S * VN * S.inv()
equal((left + left.conjugate().T) / 2, noise.conjugate().T * noise,
      'physical TP identity including Hamiltonian component')
rho = s.Matrix([[pop, coh], [coh, 1 - pop]])
delta = (left * rho + rho * left.conjugate().T) / 2 - noise * rho * noise.conjugate().T
equal(s.trace(delta), 0, 'physical Schrodinger defect trace zero')
expected_dz = (x ** 2 + y ** 2) * ((g + 1 / g) * pop - g) - 2 * lam * z * coh * x
expected_dx = coh * (2 * z ** 2 + (Cosh - 1) * x ** 2 + (Cosh + 1) * y ** 2) \
              - lam * ((g + 1 / g) * pop - g) * z * x
equal(delta[0, 0], expected_dz, 'actual defect diagonal formula')
equal(s.re(delta[0, 1]).expand(complex=True), expected_dx, 'actual defect real coherence formula')
equal(Cosh, 1 / ref_b, 'reference cosh/Bloch identity')
equal(Sinh, ref_q / ref_b, 'reference sinh/Bloch identity')
equal(mu, ref_q / (1 + ref_b), 'reference root-imbalance identity')
equal(lam ** 2, 2 * ref_b / (1 + ref_b), 'reference lambda identity')

sub_state = {pop: (1 + rad * v) / 2, coh: rad * angle_sine / 2}
J = s.expand(2 * R * angle_sine * expected_dx.subs(sub_state)
             + 2 * (R * v - K) * expected_dz.subs(sub_state))
J = s.expand(J).subs(angle_sine ** 2, 1 - v ** 2)
Jz = 2 * rad * R * (1 - v ** 2)
Jx = rad * R * (1 - v ** 2) * (1 / ref_b - 1) \
     + 2 * (R * v - K) * (rad * v - ref_q) / ref_b
Jy = Jx + Jz
Jzx = -lam * angle_sine * (R * (rad * v - ref_q) / ref_b + rad * (R * v - K))
equal(J, Jz * z ** 2 + Jx * x ** 2 + Jy * y ** 2 + 2 * Jzx * z * x,
      'full actual entropy-production quadratic form')

alpha, beta = s.symbols('alpha beta', real=True)
root = alpha * s.eye(2) + beta * (angle_sine * X + v * Z)
Hroot = (VN * root + root * VN) / 2 - N * root * N
E_raw = s.Poly(s.expand(s.trace(root * Hroot)), alpha, beta)
E = 0
sub_roots = {(2, 0): (1 + nu) / 4, (0, 2): (1 - nu) / 4,
             (1, 1): rad / 4}
for powers, coefficient in E_raw.terms():
    assert powers in sub_roots
    E += coefficient * sub_roots[powers]
E = s.expand(E).subs(angle_sine ** 2, 1 - v ** 2)
Ez = (1 - nu) * (1 - v ** 2)
Ex = 1 / ref_b - rad * v * ref_q / ref_b - 1 + (1 - nu) * v ** 2
Ey = Ex + Ez
Ezx = angle_sine * (mu * rad - (1 - nu) * v)
equal(E, Ez * z ** 2 + Ex * x ** 2 + Ey * y ** 2 + 2 * Ezx * z * x,
      'full actual root-energy quadratic form')

Zc = 2 * rad * R - bound * (1 - nu)
P0 = (1 / ref_b - 1) * (rad * R - bound) + 2 * ref_q * K / ref_b
P1 = -2 * (ref_q * R + rad * K) / ref_b + bound * rad * ref_q / ref_b
P2 = rad * R * (1 + 1 / ref_b) - bound * (1 - nu)
Q0 = lam * (ref_q * R / ref_b + rad * K) - bound * mu * rad
Q1 = -lam * rad * R * (1 + 1 / ref_b) + bound * (1 - nu)
Pv = P0 + P1 * v + P2 * v ** 2
Qv = Q0 + Q1 * v
equal(Jx - bound * Ex, Pv, 'noise block polynomial P')
equal(Jzx - bound * Ezx, angle_sine * Qv, 'noise block polynomial Q')
equal(Jy - bound * Ey, Pv + (1 - v ** 2) * Zc, 'decoupled y equals trace of real block')
det_normalized = s.expand(Zc * Pv - Qv ** 2)
concavity_coefficient = s.Poly(det_normalized, v).coeff_monomial(v ** 2)
expected_concavity = -2 * bound * rad * R * (1 - nu) * (1 - lam) ** 2 / lam ** 2
equal(concavity_coefficient, expected_concavity, 'exact normalized determinant concavity coefficient')
for sign in [-1, 1]:
    boundary_P = 2 * (sign * R - K) * (sign * rad - ref_q) / ref_b \
                 - bound * ((1 - sign * rad * ref_q) / ref_b - nu)
    boundary_Q = -lam * (R * (sign * rad - ref_q) / ref_b + rad * (sign * R - K)) \
                 - bound * (mu * rad - sign * (1 - nu))
    equal(Pv.subs(v, sign), boundary_P, f'boundary P at angle {sign}')
    equal(Qv.subs(v, sign), boundary_Q, f'boundary Q at angle {sign}')

# Exact leading determinant as rho approaches the maximally mixed state.
q, b, l, m = s.symbols('q b l m', real=True)
u, U = s.symbols('u U', real=True)
N00 = 2 - bound / 2
Nuu = 2 * U / u - bound / 2
N0u = 1 + (1 - u ** 2) * U / u - bound * s.sqrt(1 - u ** 2) / 2
limit_P = (2 * q * K - bound * (1 - b)) / b
limit_Q = l * (q / b + K) - bound * m
limit_F = (2 - bound / 2) * limit_P - limit_Q ** 2
limit_subs = {q: 2 * u / (1 + u ** 2), b: (1 - u ** 2) / (1 + u ** 2),
              l: s.sqrt(1 - u ** 2), m: u, K: 2 * U}
equal(s.simplify(limit_F.subs(limit_subs)),
      4 * u ** 2 * (N00 * Nuu - N0u ** 2) / (1 - u ** 2),
      'maximally mixed state limit exactly matches two-point Hardy determinant')

print(json.dumps({
    'status': 'PASS_EXACT_BLIND_REDUCTION',
    'checks': len(checks),
    'assertions': checks,
    'global_pi_status': 'UNKNOWN before proof exposure',
    'remaining_gate': 'F_pi(r,q,+1)>=0 and F_pi(r,q,-1)>=0 for all admissible r,q',
    'supplied_Hardy_kernel_interface': 'Exact match in r->0 limit; full boundary interface not derived in blind attempt',
    'floating_point_used': False,
    'numeric_scan': False
}, indent=2))
