"""Finite diagnostics for the sharp centered proof; not theorem validation."""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import json
import numpy as np


exact_checks = 0
g_second_bound = F(105 * 265, 256) * F(128, 119)**6
assert g_second_bound < 180
assert F(9720) * F(9, 2)**3 == 885735
assert F(4) * F(9, 8)**5 < 8
assert 24**2 * 3 < 42**2
exact_checks += 4

# If P(x)(1-2x)^(-a) is differentiated, its new numerator is
# (1-2x)P'(x)+2aP(x), and its denominator exponent is a+1.
def derivative_numerator(coefficients, exponent):
    derivative = [F(i) * coefficients[i] for i in range(1, len(coefficients))]
    result = [F(0)] * len(coefficients)
    for i, coefficient in enumerate(derivative):
        result[i] += coefficient
        result[i+1] -= 2 * coefficient
    for i, coefficient in enumerate(coefficients):
        result[i] += 2 * exponent * coefficient
    return result

first = derivative_numerator([F(1), F(3)], F(7, 2))
second = derivative_numerator(first, F(9, 2))
assert first == [F(10), F(15)]
assert second == [F(105), F(105)]
exact_checks += 2

def rising_coefficient(exponent, degree):
    result = F(1)
    for i in range(degree):
        result *= (exponent+i)*2/F(i+1)
    return result

for k in range(1, 65):
    lhs = F(k*k) * rising_coefficient(F(3, 2), k)
    rhs = 3*rising_coefficient(F(7, 2), k-1)
    if k >= 2:
        rhs += 9*rising_coefficient(F(7, 2), k-2)
    assert lhs == rhs
    exact_checks += 1

extremizer_checks = []
for n in range(1, 129):
    sectors = []
    for twice_j in range(n % 2, n+1, 2):
        lower = (n-twice_j)//2
        multiplicity = comb(n, lower) - (comb(n, lower-1) if lower else 0)
        p = F((twice_j+1)*multiplicity, 2**n)
        sectors.append((F(twice_j, 2), p))
    assert sum(p for j, p in sectors) == 1
    assert sum(p*j*(j+1) for j, p in sectors) == F(3*n, 4)
    mean_j = sum(p*j for j, p in sectors)
    mean_j2 = sum(p*j*j for j, p in sectors)
    assert mean_j2 == F(3*n, 4)-mean_j
    assert mean_j*mean_j <= F(3*n, 4)
    exact_checks += 4
    if n >= 2:
        c_x = (2*mean_j/n-1)/(n-1)
        c_z = (4*mean_j2/n-1)/(n-1)
        coefficient = (1-2*mean_j/n)/(n-1)
        assert c_x == -coefficient
        assert c_z == 2*coefficient
        assert 2*c_x*c_x+c_z*c_z == 6*coefficient**2
        exact_checks += 3
    if n in [3, 4, 31, 32, 127, 128]:
        extremizer_checks.append({"N": n, "mean_spin": float(mean_j),
                                  "scaled_pair_factor": float(1-2*mean_j/n)})

rng = np.random.default_rng(20261008)
covariance_checks = []
for n in range(2, 33):
    for trial in range(3):
        mean = np.zeros(3)
        moments = np.zeros((3, 3))
        for twice_j in range(n % 2, n+1, 2):
            j = twice_j/2
            lower = (n-twice_j)//2
            multiplicity = comb(n, lower)-(comb(n, lower-1) if lower else 0)
            p = (twice_j+1)*multiplicity/2**n
            m = np.arange(-j, j+1)
            raising = np.zeros((twice_j+1, twice_j+1), complex)
            for column in range(twice_j):
                raising[column+1, column] = np.sqrt(j*(j+1)-m[column]*(m[column]+1))
            lowering = raising.conj().T
            spins = [(raising+lowering)/2, (raising-lowering)/(2j), np.diag(m)]
            vector = rng.normal(size=twice_j+1)+1j*rng.normal(size=twice_j+1)
            vector /= np.linalg.norm(vector)
            pure = np.outer(vector, vector.conj())
            rho = 0.83*pure+0.17*np.eye(twice_j+1)/(twice_j+1)
            for a in range(3):
                mean[a] += p*np.trace(rho@spins[a]).real
                for b in range(3):
                    symmetric_product = (spins[a]@spins[b]+spins[b]@spins[a])/2
                    moments[a, b] += p*np.trace(rho@symmetric_product).real
        covariance = moments-np.outer(mean, mean)
        bloch = 2*mean/n
        c = (4*moments-n*np.eye(3))/(n*(n-1))
        centered = c-np.outer(bloch, bloch)
        z = 4*covariance/n+np.outer(bloch, bloch)
        identity_error = np.linalg.norm(centered-(z-np.eye(3))/(n-1))
        trace_error = abs(np.trace(z)-(3-(n-1)*np.dot(bloch, bloch)))
        assert identity_error < 1e-12
        assert trace_error < 1e-12
        assert np.linalg.eigvalsh(covariance)[0] > -1e-12
        assert np.linalg.eigvalsh(z)[0] > -1e-12
        assert np.linalg.norm(centered)**2 <= 6/(n-1)**2+1e-12
        covariance_checks.append({"N": n, "trial": trial,
                                  "identity_error": float(identity_error),
                                  "trace_error": float(trace_error),
                                  "pair_norm_squared": float(np.linalg.norm(centered)**2)})

results = {
    "exact_checks": exact_checks,
    "g_second_rational_upper_bound": str(g_second_bound),
    "g_second_rational_upper_bound_float": float(g_second_bound),
    "higher_degree_constant": 885735,
    "covariance_matrix_cases": len(covariance_checks),
    "max_covariance_identity_error": max(item["identity_error"] for item in covariance_checks),
    "max_trace_error": max(item["trace_error"] for item in covariance_checks),
    "both_parity_extremizer_diagnostics": extremizer_checks,
    "scope": "Finite diagnostics, not theorem validation or external review."
}
Path(__file__).with_name("verification_results.json").write_text(json.dumps(results, indent=2)+"\n")
print(json.dumps(results, indent=2))
