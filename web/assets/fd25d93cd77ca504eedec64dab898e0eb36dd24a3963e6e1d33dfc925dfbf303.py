#!/usr/bin/env python3
"""Exposed exact identity audit and one independently embedded upper witness."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time
import sympy as s

checks = []


def equal(a, b, label):
    delta = a - b
    ok = (all(s.simplify(x) == 0 for x in delta) if isinstance(delta, s.MatrixBase)
          else s.simplify(delta) == 0)
    assert ok, (label, delta)
    checks.append(label)


x, y, lam = s.symbols('x y lambda', real=True)
alpha = x - y
expanded_endpoint = x * (s.sinh(alpha) * s.cosh(x)
                         - (s.cosh(alpha) + 1) * s.sinh(x)) \
                    + alpha * s.sinh(x) - 2 * lam * s.sinh(alpha / 2) * s.sinh(x) \
                    + 2 * lam * s.cosh(alpha / 2) * (s.cosh(x) - 1)
Txy = x * s.sinh(y) + y * s.sinh(x) \
      - 4 * lam * s.sinh(x / 2) * s.sinh(y / 2)
equal(s.simplify(s.expand_trig((expanded_endpoint + Txy).rewrite(s.exp))), 0,
      'general endpoint cross identity with x-y=alpha')
equal(Txy.subs(y, x), 2 * (x * s.sinh(x) - lam * (s.cosh(x) - 1)),
      'hyperbolic kernel diagonal normalization')
t, u, At, Au = s.symbols('t u At Au', real=True)
bt, bu = s.sqrt(1 - t ** 2), s.sqrt(1 - u ** 2)
kernel_disk = ((1 - t ** 2) * At / t + (1 - u ** 2) * Au / u - lam * bt * bu) / (1 - t * u)
T_in_disk = (2 * At) * 2 * u / (1 - u ** 2) \
            + (2 * Au) * 2 * t / (1 - t ** 2) - 4 * lam * t * u / (bt * bu)
hyperbolic_cos_difference = (1 - t * u) / (bt * bu)
equal(T_in_disk / (2 * hyperbolic_cos_difference),
      2 * t * u * kernel_disk / (bt * bu),
      'exact Hardy-to-hyperbolic signed congruence')

Q = s.Rational
I = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
Y = s.Matrix([[0, -s.I], [s.I, 0]])
Z = s.diag(1, -1)
sigma = s.diag(Q(9, 10), Q(1, 10))
stationary_root = s.diag(3, 1) / s.sqrt(10)
noise = X + 9 * Z
potential = s.Matrix([[Q(244, 3), 9], [9, 84]])
equal((potential * stationary_root + stationary_root * potential) / 2,
      noise * stationary_root * noise, 'upper witness exact Lyapunov stationarity')


def H(a):
    return (potential * a + a * potential) / 2 - noise * a * noise


S = s.diag(s.sqrt(3), 1) / 10 ** Q(1, 4)
physical_noise = S * noise * S.inv()
physical_left = S * potential * S.inv()
hamiltonian_correction = 3 * s.sqrt(3) * Y
equal(physical_noise, s.Matrix([[9, s.sqrt(3)], [1 / s.sqrt(3), -9]]),
      'upper physical jump orientation')
equal(physical_left, physical_noise.conjugate().T * physical_noise
      + s.I * hamiltonian_correction, 'upper physical Hamiltonian retained')


def LS(a):
    return (physical_left * a + a * physical_left.conjugate().T) / 2 \
           - physical_noise * a * physical_noise.conjugate().T


equal(LS(sigma), s.zeros(2), 'upper physical stationary reference')
for i in range(2):
    for j in range(2):
        unit = s.zeros(2)
        unit[i, j] = 1
        equal(s.trace(LS(unit)), 0, f'upper full physical trace conservation {i}{j}')
        equal(S.inv() * LS(S * unit * S) * S.inv(), H(unit),
              f'upper full physical KMS similarity {i}{j}')
basis = [I / s.sqrt(2), X / s.sqrt(2), Y / s.sqrt(2), Z / s.sqrt(2)]
matrix = s.Matrix([[s.trace(a * H(b)) for b in basis] for a in basis])
equal(matrix, s.Matrix([[Q(2, 3), 9, 0, -Q(4, 3)],
                        [9, Q(488, 3), 0, -18], [0, 0, Q(494, 3), 0],
                        [-Q(4, 3), -18, 0, Q(8, 3)]]), 'upper exact transformed Pauli matrix')
spectral_variable = s.symbols('spectral_variable')
equal(matrix.charpoly(spectral_variable).as_expr(),
      spectral_variable * (spectral_variable - Q(494, 3))
      * ((spectral_variable - 83) ** 2 - Q(60766, 9)),
      'upper primitive spectrum characteristic polynomial')
assert 60766 < 249 ** 2
checks.append('upper all nonzero eigenvalues strictly positive')
equal(H(2 * I + Z), s.zeros(2), 'upper fixed root direction')

rad = Q(364, 365)
rho = (I + rad * (s.sqrt(1999) * X + 999 * Z) / 1000) / 2
equal(s.trace(rho), 1, 'upper actual density trace one')
equal(rho.det(), Q(729, 532900), 'upper actual faithful determinant')
root_rho = (rho + Q(27, 730) * I) / s.sqrt(Q(784, 730))
equal(root_rho * root_rho, rho, 'upper actual physical root')
delta = LS(rho)
equal(s.trace(delta), 0, 'upper actual defect trace zero')
# Scalar log determinants cancel against trace-zero delta. beta=ln27=3ln3.
J_over_log3 = s.simplify(s.trace(delta * (3 * (2 * rho - I) / rad - Z)))
E = s.simplify(s.trace(root_rho * H(root_rho)))
equal(E, Q(2822593, 6843750) - Q(700479, 91250000) * s.sqrt(1999),
      'upper E independently from full physical root')
equal(J_over_log3, Q(311978753, 136875000) - Q(305181, 11406250) * s.sqrt(5997),
      'upper J independently from full physical generator and log')

folder = Path(__file__).resolve().parent
workspace = folder.parents[3]
origin_folder = workspace / 'work/agents/complexity_proof_recon/cycle07_qubit_constant'
source = origin_folder / 'check_exact_upper.py'
copy = folder / 'authorized_upper_replay_copy.py'
copy.write_bytes(source.read_bytes())
started = time.perf_counter()
completed = subprocess.run([sys.executable, str(copy)], capture_output=True, text=True, check=True)
child_wall = time.perf_counter() - started
copied_result = json.loads(completed.stdout)
assert copied_result['status'] == 'PASS_EXACT_SINGLE_CERTIFICATE'
assert copied_result['ratio_interval'] == ['82271/25000', '32908401/10000000']
checks.append('authorized owned-copy exact integer rational ratio replay passes')

print(json.dumps({
    'status': 'PASS_EXPOSED_EXACT_AUDIT',
    'checks': len(checks),
    'assertions': checks,
    'origin_script_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'origin_replay_assertions': copied_result['checks_passed'],
    'origin_replay_child_wall_seconds': child_wall,
    'upper_ratio_interval': copied_result['ratio_interval'],
    'scope': 'Post-exposure factorization identities plus one supplied analytic witness; no scan, and no universal theorem by replay',
    'floating_point_used_for_certificate': False,
    'source_proof_edits': False
}, indent=2))
