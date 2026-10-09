"""Portable read-only replay of the frozen finite observable witness.

All arithmetic is preserved from build_and_verify_witness_v1.py. The recorded
absolute source path is historical metadata. The actual relative source SHA256
and every other JSON payload field are checked. Frozen coefficient bytes are
never regenerated or changed; their original SHA256 is independently pinned.
The universal conditional-Markov/geometric proof still requires mathematical
audit. No third-party package or assert statement is used.
"""
from fractions import Fraction as F
from pathlib import Path
from math import factorial, log
import hashlib
import json

FOLDER = Path(__file__).parent
SOURCE = FOLDER.parent / 'hidden_realization' / 'exact_certificate_v1.json'
DATA = json.loads(SOURCE.read_text())


def require(test, label):
    if not test:
        raise RuntimeError(label)


def matrix(name):
    return [[F(x) for x in row] for row in DATA[name]]


def transpose(a):
    return [list(x) for x in zip(*a)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mul(a, b):
    return [[sum(x * y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def scale(a, s):
    return [[s * x for x in row] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)]
            for ar, br in zip(a, b)]


def inv(a):
    n = len(a)
    b = [ar[:] + ir for ar, ir in zip(a, eye(n))]
    for i in range(n):
        pivot = next((j for j in range(i, n) if b[j][i]), None)
        require(pivot is not None, 'invertible matrix')
        b[i], b[pivot] = b[pivot], b[i]
        q = b[i][i]
        b[i] = [x / q for x in b[i]]
        for j in range(n):
            if j != i:
                q = b[j][i]
                b[j] = [x - q * y for x, y in zip(b[j], b[i])]
    return [row[n:] for row in b]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def mv(a, b):
    return [dot(row, b) for row in a]


def frob2(a):
    return sum(x * x for row in a for x in row)


def inf_norm(a):
    return max(sum(abs(x) for x in row) for row in a)


def polynomial_exponential(a, time, degree):
    n = len(a)
    total = eye(n)
    term = eye(n)
    for k in range(1, degree + 1):
        term = scale(mul(term, a), time / k)
        total = add(total, term)
    return total


def strings(a):
    return [[str(x) for x in row] for row in a]


def scalar_row(a):
    return [str(x) for x in a]


Q = matrix('Q')
L = matrix('L')
H = matrix('H')
points = matrix('points')
facets = matrix('facets')
z = matrix('farkas_z')

Z = [[F(0)] + zi + [dot(zi, vi)] * 5
     for zi, vi in zip(z, points)] + [[F(0)] * 8 for _ in range(5)]
require(frob2(L) < 9, 'generator feature norm <3')
require(inf_norm(Q) <= 2, 'hidden generator infinity norm <=2')
require(all(dot(zi, zi) < 9 for zi in Z), 'Farkas field norm <3')
beta = sum(sum(abs(x) for x in zi) for zi in Z[:5]) / 10
require(beta < 2, 'weighted Farkas l1 beta <2')
derivative = sum(dot(zi, mv(scale(transpose(L), F(-1)), xi))
                 for zi, xi in zip(Z, H)) / 10
gamma = -derivative
require(gamma == -F(DATA['farkas_drift_pairing']) / 2,
        'full negative Farkas pairing matches internal seed')
require(gamma > F(59, 10000), 'gamma > .0059')
for i in range(10):
    for j in range(i + 1, 10):
        mono = dot([x - y for x, y in zip(Z[i], Z[j])],
                   [x - y for x, y in zip(H[i], H[j])])
        require(mono >= 0, 'all ten-frame monotonicities')
minimum_separation2 = min(sum((a - b) ** 2 for a, b in zip(x, y))
                          for i, x in enumerate(points)
                          for j, y in enumerate(points) if i < j)
require(minimum_separation2 > F(25, 64), 'vertex separation >5/8')

V = [[F(1), x, y, x * x, x * y] for x, y in points]
V_inverse = inv(V)
require(inf_norm(V_inverse) < 5, 'quadratic interpolation norm <5')
for i in range(5):
    normals = [facets[i][1:], facets[(i + 1) % 5][1:]]
    require(frob2(inv(normals)) < 9, 'adjacent Hoffman inverse norm <3')
    require(dot(facets[i][1:], facets[i][1:]) > F(1, 9),
            'single-normal Hoffman inverse norm <3')

h = F(1, 10 ** 12)
t = F(1, 1000)
tau = F(1, 2_000_000)
eta = F(1, 10)
Eh = polynomial_exponential(L, h, 4)
Et = polynomial_exponential(L, t, 16)
K = transpose(Et)
ak = [Eh[0][3 + k] for k in range(5)]
bk = [[Eh[1][3 + k], Eh[2][3 + k]] for k in range(5)]
Bh = [bk[4], bk[0]]
Bh_inverse = inv(Bh)
require(inf_norm(Bh_inverse) < 12 / h, 'basis inversion bound')
require(all(abs(a) < h for a in ak), 'finite marker constant bound')
require(all(sum(abs(x) for x in b) < h / 4 for b in bk),
        'finite marker gradient bound')
require(sum((3 * h) ** n / factorial(n) for n in range(2, 5)) < 5 * h * h,
        'facet Taylor remainder bound')
rh = (3 * h) ** 5 / (factorial(5) * (1 - 3 * h))
rt = (3 * t) ** 17 / (factorial(17) * (1 - 3 * t))
require(rh < 3 * h ** 5, 'target degree4 Taylor remainder')
require(rt < F(1, 10 ** 55), 'target degree16 Taylor remainder')
require(1 / (1 - 3 * t) < F(101, 100), 'transition norm <1.01')
require(3 * (3 * t) / (1 - 3 * t) < 1, 'rounded-drift Lipschitz constant <=1')

# Raw function basis: I0, psi0,...,psi4, I1,...,I5.
F_coeff = [[F(0)] * 11 for _ in range(8)]
F_coeff[0][0] = 1
for coordinate in range(2):
    row = coordinate + 1
    F_coeff[row][0] = -Bh_inverse[coordinate][0] * ak[4] - Bh_inverse[coordinate][1] * ak[0]
    F_coeff[row][5] = Bh_inverse[coordinate][0]
    F_coeff[row][1] = Bh_inverse[coordinate][1]
for k in range(5):
    F_coeff[3 + k][6 + k] = 1
D_coeff = [[F(0)] * 11 for _ in range(5)]
for k in range(5):
    D_coeff[k][1 + k] = 1
    D_coeff[k] = [x - ak[k] * f0 - bk[k][0] * fx - bk[k][1] * fy
                  for x, f0, fx, fy in zip(D_coeff[k], F_coeff[0], F_coeff[1], F_coeff[2])]
require(all(sum(abs(x) for x in row) < 20 / h for row in F_coeff[1:3]),
        'feature sup norm bound')
feature_sup2 = sum(sum(abs(x) for x in row) ** 2 for row in F_coeff)
require(feature_sup2 < 900 / (h * h), 'feature vector sup norm <30/h')
require(all(sum(abs(x) for x in row) < 7 for row in D_coeff), 'facet residual sup norm <7')
require(all(x == 0 for x in D_coeff[0] + D_coeff[4]), 'selected facet residuals identically zero')

I_minus_K = add(eye(8), scale(K, F(-1)))
vertex_costs = [dot(zi, mv(I_minus_K, xi))
                for zi, xi in zip(Z[:5], H[:5])]
alpha = mv(V_inverse, vertex_costs)
require(all(abs(x) < F(1, 10) for x in alpha), 'quadratic coefficient bounds')
require(mv(V, alpha) == vertex_costs, 'exact quadratic interpolation')

Lambda = F(150 ** 2 * 3 ** 2, 1) / (2 * eta ** 2 * h ** 2 * tau)
Mu = F(9, 1) / (4 * tau)
require(Lambda == F(20_250_000_000_000, 1) / (h * h), 'facet Young coefficient')
require(Mu == 4_500_000, 'regression Young coefficient')
require(8 ** 2 + 145 ** 2 < 150 ** 2, 'rounding Cauchy constant')
target_F_bound = -gamma * t + 4 * t * t / (1 - 2 * t)
require(target_F_bound < -F(18, 10 ** 7), 'finite-time negative drift margin')
moment_error = 200 * h ** 4
target_W_bound = (target_F_bound + 200 * h ** 4 + 3 * F(1, 10 ** 55)
                  + 72 * moment_error
                  + (45000 * h + tau) * (1 + moment_error) + tau / 2
                  + Lambda * 1000 * h ** 10 + Mu * 90000 * h ** 8)
require(target_W_bound < -F(1, 10 ** 6), 'strict target observable witness')
M = F(6 * 10 ** 39)
stat_sup_bound = (100 / (h * h) + 72 * (1 + 800 / (h * h))
                  + (45000 * h + tau) * (1 + 800 / (h * h)) + tau
                  + Lambda * 245 + Mu * 4000 / (h * h))
require(stat_sup_bound < M, 'observed statistic normalization')
T = 2 * (t + h)
require(T < F(1, 400), 'finite observation span')
delta = F(1, 10 ** 6) / M
sigma_floor = 2 * delta * delta / T
require(sigma_floor > F(2, 10 ** 89), 'dimension-free entropy floor')

payload = {
    'status': 'internally derived rational certificate; proof in v1.txt and clarifications in v2.txt',
    'source': str(SOURCE),
    'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'alphabet': list(range(6)),
    'observation_times': scalar_row([-t-h, -t, -h, F(0), h, t, t+h]),
    'raw_function_basis': ['I0'] + ['psi' + str(k) for k in range(5)] + ['I' + str(k) for k in range(1,6)],
    'raw_function_definition': 'I0=1(Y0=0); psik=1(Y0=0,Yh=k+1); Ik=1(Y0=k)',
    'feature_matrix': strings(F_coeff),
    'facet_residual_matrix': strings(D_coeff),
    'K': strings(K),
    'quadratic_coefficients': scalar_row(alpha),
    'quadratic_monomials': ['1','x','y','x^2','xy'],
    'constants': {name: str(value) for name, value in {
        'h':h, 't':t, 'tau':tau, 'eta':eta, 'circle_coefficient':F(72),
        'finite_facet_coefficient':45000*h, 'Lambda':Lambda, 'Mu':Mu,
        'M':M, 'raw_target_gap':F(1,10**6), 'normalized_gap':delta,
        'span':T, 'entropy_floor':sigma_floor}.items()},
    'statistic_formula': 'Sq +72(p0-s2)+(45000*h+tau)*(p0+s2)+tau*p0+Lambda*Rh+Mu*Rt, divided by M',
    'verification': {
        'gamma':str(gamma), 'beta':str(beta),
        'minimum_vertex_distance_squared':str(minimum_separation2),
        'target_drift_upper_bound':str(target_F_bound),
        'target_witness_upper_bound':str(target_W_bound),
        'statistic_sup_bound':str(stat_sup_bound),
        'arithmetic':'fractions.Fraction', 'Taylor_degrees':[4,16]
    }
}
output = FOLDER / 'witness_rational_v1.json'
require(output.is_file(), 'frozen coefficient artifact exists')
frozen_bytes = output.read_bytes()
recorded = json.loads(frozen_bytes)
require(isinstance(recorded, dict), 'frozen coefficient JSON object')
require(isinstance(recorded.get('source'), str), 'historical source path is metadata')
require(set(recorded) == set(payload), 'all frozen payload fields are present')
require(recorded['source_sha256'] == hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'actual relative source SHA256 matches frozen provenance')
# Ignore only the old checkout location, never any mathematical payload field.
expected_fields = {key: value for key, value in payload.items() if key != 'source'}
recorded_fields = {key: value for key, value in recorded.items() if key != 'source'}
require(recorded_fields == expected_fields,
        'every mathematical and non-path metadata field agrees on portable replay')
frozen_sha256 = hashlib.sha256(frozen_bytes).hexdigest()
require(frozen_sha256 == '2e9f7eb0e67839b60c5345f42b4bb6b764053bae32f72aeabbaa960b89fd0123',
        'original frozen coefficient bytes and SHA256 are preserved')

print(json.dumps({
    'status':'PASS', 'arithmetic':'fractions.Fraction',
    'certificate_file':str(output), 'certificate_bytes':len(frozen_bytes),
    'certificate_sha256':frozen_sha256,
    'portable_validation':'actual relative source SHA256 and every payload field except historical source path',
    'historical_source_path':recorded['source'],
    'actual_source_sha256':recorded['source_sha256'],
    'finite_drift_upper_bound':float(target_F_bound),
    'witness_upper_bound':float(target_W_bound),
    'statistic_sup_bound':float(stat_sup_bound), 'normalization':float(M),
    'normalized_gap':float(delta), 'entropy_floor':float(sigma_floor),
    'h':float(h), 't':float(t), 'span':float(T),
    'N_independent_windows_95_percent':float(8/(delta*delta))*log(40),
    'interpretation':'finite algebra and constants replayed; universal proof requires mathematical audit'
}, indent=2))
