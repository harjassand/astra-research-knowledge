"""Independent exact arithmetic audit of Sol7's finite-word coefficient bounds.

Standard library only; this is scoped checking, not a proof assistant.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from math import factorial

record = json.loads((Path(__file__).parent / "exact_certificate_v1.json").read_text())


def mat(key):
    return [[F(s) for s in row] for row in record[key]]


def require(condition, name):
    if not condition:
        raise RuntimeError(name)


def trans(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def inv(a):
    n = len(a)
    aug = [row[:] + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if aug[i][j]), None)
        require(pivot is not None, "matrix invertible")
        aug[j], aug[pivot] = aug[pivot], aug[j]
        scale = aug[j][j]
        aug[j] = [x / scale for x in aug[j]]
        for i in range(n):
            if i != j:
                scale = aug[i][j]
                aug[i] = [x - scale * y for x, y in zip(aug[i], aug[j])]
    return [row[n:] for row in aug]


def norminf(a):
    return max(sum(abs(x) for x in row) for row in a)


def frobsq(a):
    return sum(x * x for row in a for x in row)


def exponential_polynomial(a, s, degree):
    n = len(a)
    power = [[F(i == j) for j in range(n)] for i in range(n)]
    result = [row[:] for row in power]
    for k in range(1, degree + 1):
        power = mul(power, a)
        coefficient = s**k / factorial(k)
        result = [[x + coefficient * y for x, y in zip(row, prow)] for row, prow in zip(result, power)]
    return result


L, Q, H = mat("L"), mat("Q"), mat("H")
vertices, z, facets = mat("points"), mat("farkas_z"), mat("facets")
Z = [[F(0), *z[i], *[sum(x * y for x, y in zip(z[i], vertices[i]))] * 5] for i in range(5)] + [[F(0)] * 8 for _ in range(5)]
h, t, tau, eta = F(1, 10**12), F(1, 1000), F(1, 2_000_000), F(1, 10)
Eh = exponential_polynomial(L, h, 4)
Et = exponential_polynomial(L, t, 16)
K = trans(Et)
require(frobsq(L) < 9, "L Frobenius norm <3")
require(norminf(Q) <= 2, "Q infinity norm <=2")
require(max(sum(x*x for x in row) for row in Z) < 9, "field Euclidean norm <3")
require(sum(sum(abs(x) for x in row) for row in Z) / 10 < 2, "field L1 average <2")
require(min(sum((x-y)**2 for x, y in zip(vertices[i], vertices[j])) for i in range(5) for j in range(i)) > F(25,64), "vertex distances >5/8")

V = [[F(1), x, y, x*x, x*y] for x, y in vertices]
require(norminf(inv(V)) < 5, "V inverse infinity norm <5")
for i in range(5):
    normals = [facets[i][1:], facets[(i+1) % 5][1:]]
    require(frobsq(inv(normals)) < 9, "adjacent normal inverse Frobenius norm <3")
    require(sum(x*x for x in facets[i][1:]) > F(1,9), "single normal reciprocal <3")

a = [Eh[0][3+k] for k in range(5)]
b = [[Eh[1][3+k], Eh[2][3+k]] for k in range(5)]
Bhinv = inv([b[4], b[0]])
require(norminf(Bhinv) < 12 / h, "B_h inverse infinity norm <12/h")
require(frobsq(b) < (F(9,20)*h)**2, "all marker coordinate coefficients Frobenius norm <.45h")

f_values, d_values = [], []
for output0 in range(6):
    for outputh in range(6):
        internal = F(output0 == 0)
        psi = [F(output0 == 0 and outputh == k+1) for k in range(5)]
        xy = mul(Bhinv, [[psi[4] - a[4]*internal], [psi[0] - a[0]*internal]])
        features = [internal, xy[0][0], xy[1][0]] + [F(output0 == k+1) for k in range(5)]
        residuals = [psi[k] - a[k]*internal - sum(b[k][j]*features[j+1] for j in range(2)) for k in range(5)]
        f_values.append(features)
        d_values.append(residuals)
require(max(abs(row[j]) for row in f_values for j in (1,2)) < 20/h, "pointwise F_x,F_y <20/h")
require(max(sum(x*x for x in row) for row in f_values) < (30/h)**2, "pointwise F Euclidean norm <30/h")
require(max(abs(x) for row in d_values for x in row) < 7, "pointwise D_k <7")
require(all(row[0] == row[4] == 0 for row in d_values), "D_0,D_4 identically zero")

bvertex = [[sum(Z[i][k] * (H[i][k] - sum(K[k][j]*H[i][j] for j in range(8))) for k in range(8))] for i in range(5)]
alpha = [row[0] for row in mul(inv(V), bvertex)]
require(max(abs(x) for x in alpha) < F(1,10), "quadratic coefficients <1/10")

# Exact bounds used in the analytic target-error argument. The better 72 h^4
# feature error follows from ||B^-1||_2 <=sqrt(2)||B^-1||_infinity.
remainder_h = (3*h)**5 / (factorial(5)*(1-3*h))
remainder_t = (3*t)**17 / (factorial(17)*(1-3*t))
require(remainder_h < 3*h**5, "degree-4 exponential remainder <3h^5")
require(remainder_t < F(1,10**55), "degree-16 exponential remainder <1e-55")
require(F(1,2) * 37**2 < 1000, "R_h bound from 72h^4 feature error and .45h coefficient norm")

gamma = -F(record["farkas_drift_pairing"]) / 2
require(gamma > F(59,10000), "negative drift magnitude >59/10000")
Lambda = F(202500) / (2*eta**2*h**2*tau)
Mu = F(9) / (4*tau)
W_target_upper = -gamma*t + 4*t*t/(1-2*t) + 200*h**4 + 3*F(1,10**55)
W_target_upper += 14400*h**4 + (45000*h+tau)*(1+200*h**4) + tau/2
W_target_upper += Lambda * 1000*h**10 + Mu * 90000*h**8
require(W_target_upper < -F(1,10**6), "strict target witness <-1e-6")

summand_bound = 100/h**2 + 72*(1+800/h**2)
summand_bound += (45000*h+tau)*(1+800/h**2) + tau
summand_bound += Lambda*245 + Mu*4000/h**2
M = F(6*10**39)
require(summand_bound < M, "pointwise witness normalization <6e39")
delta = F(1,6*10**45)
T = 2*(t+h)
require(2*delta**2/T > F(2,10**89), "EP floor >2e-89")

print(json.dumps({
    "status": "PASS",
    "checks": "independent exact arithmetic audit of coefficient/normalization bounds",
    "target_upper_bound_decimal": float(W_target_upper),
    "summand_bound_decimal": float(summand_bound),
    "EP_floor_lower_decimal": float(2*delta**2/T),
    "arithmetic": "fractions.Fraction; decimals only for presentation",
}, indent=2))
