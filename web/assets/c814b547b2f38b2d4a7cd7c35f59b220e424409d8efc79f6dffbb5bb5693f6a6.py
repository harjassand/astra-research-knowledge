"""Scoped diagnostics for the binary-convolution/profile compiler deductions.

This does not implement or validate the released ultraflat construction.
Exact calculations are explicitly separated from floating-point diagnostics.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import numpy as np
import sympy as sp

out = {"scope": "Independent small diagnostics; no ultraflat source theorem replay"}

# Exact continuous-versus-discrete spectrum obstruction.
x = sp.symbols("x", real=True)
a = [1, 1, 1, -1]
N = len(a)
c = [sum(a[j] * a[j+k] for j in range(N-k)) for k in range(N)]
q = sp.expand(N + 2 * sum(c[k] * sp.chebyshevt(k, x) for k in range(1, N)))
assert q == 4 + 8*x - 8*x**3
assert sp.simplify(q.subs(x, 1/sp.sqrt(3)) - (4 + 16/(3*sp.sqrt(3)))) == 0
assert sp.simplify(q.subs(x, -1/sp.sqrt(3)) - (4 - 16/(3*sp.sqrt(3)))) == 0
z = sp.symbols("z")
p = sum(a[k] * z**k for k in range(N))
root_values = [sp.simplify(p.subs(z, t) * sp.conjugate(p.subs(z, t)))
               for t in [1, sp.I, -1, -sp.I]]
assert root_values == [4, 4, 4, 4]
out["exact_four_point_counterexample"] = {
    "signs": a, "aperiodic_autocorrelations": c,
    "squared_modulus_Chebyshev": str(q),
    "squared_moduli_at_N_roots": [str(v) for v in root_values],
    "continuous_squared_modulus_min": "4-16/(3*sqrt(3))",
    "continuous_squared_modulus_max": "4+16/(3*sqrt(3))",
    "normalized_continuous_min": float(sp.sqrt(1-4/(3*sp.sqrt(3)))),
    "normalized_continuous_max": float(sp.sqrt(1+4/(3*sp.sqrt(3)))),
}

# Exact full convolution Gram identity, with finite integer inputs.
identity_checks = 0
for n in range(2, 9):
    for signs in product([-1, 1], repeat=n-1):
        aa = [1, *signs]
        cc = [sum(aa[j]*aa[j+k] for j in range(n-k)) for k in range(n)]
        for length in [1, 3, 7]:
            signal = [((j*j+3*j+2) % 9)-4 for j in range(length)]
            conv = [sum(aa[t-j]*signal[j] for j in range(length) if 0 <= t-j < n)
                    for t in range(n+length-1)]
            energy = sum(t*t for t in conv)
            gram = sum(signal[j]*signal[k] * (cc[abs(j-k)] if abs(j-k)<n else 0)
                       for j in range(length) for k in range(length))
            assert energy == gram
            identity_checks += 1
out["exact_full_convolution_Gram_identity_checks"] = identity_checks

# A square causal truncation has determinant N^{-L/2}, regardless of signs.
truncation_checks = []
for n, length in [(4, 5), (4, 9), (7, 5)]:
    aa = [1 if j % 3 else -1 for j in range(n)]
    mat = sp.Matrix([[aa[t-j] if 0 <= t-j < n else 0
                      for j in range(length)] for t in range(length)])
    assert abs(mat.det()) == 1
    truncation_checks.append({"N": n, "L": length,
                              "unnormalized_abs_determinant": int(abs(mat.det())),
                              "normalized_abs_determinant": f"{n}^(-{length}/2)"})
out["exact_square_causal_truncation_checks"] = truncation_checks

# Exact alias aggregation identity and l1 bound for finite Fourier profiles.
# Conjugate symmetry is equivalent to all Fourier coefficients being real.
alias_checks = 0
alias_ratios = []
for n in range(2, 18):
    coeff = {}
    for k in range(-3*n, 4*n):
        if 0 <= k < n:
            coeff[k] = Fraction((k % 3)-1, 2*n)
        else:
            coeff[k] = Fraction((-1)**abs(k), (n+abs(k))**3)
    tail = sum(abs(v) for k, v in coeff.items() if not 0 <= k < n)
    folded = [sum(v for k, v in coeff.items() if k % n == j) for j in range(n)]
    alias = [folded[j] - coeff[j] for j in range(n)]
    assert sum(abs(v) for v in alias) <= tail
    # Error polynomial Q-B has alias coefficients inside and discarded
    # coefficients outside, so its Fourier l1 norm is at most twice tail.
    error_l1 = sum(abs(v) for v in alias) + tail
    assert error_l1 <= 2*tail
    ts = np.arange(n)/n
    samples = np.zeros(n, dtype=complex)
    for k, value in coeff.items():
        samples += float(value)*np.exp(2j*np.pi*k*ts)
    observed = np.fft.fft(samples)/n
    assert np.max(np.abs(observed - np.array([float(v) for v in folded]))) < 2e-14
    alias_ratios.append(float(error_l1/(2*tail)))
    alias_checks += 1
out["exact_alias_l1_checks"] = alias_checks
out["floating_DFT_alias_checks"] = alias_checks
out["max_exact_error_l1_over_twice_tail"] = max(alias_ratios)

# Finite Toeplitz eigenvalues approach the continuous spectral bounds.
# This floating diagnostic confirms the direction of the four-point failure.
toeplitz = []
for length in [4, 16, 64, 128]:
    gram = np.array([[(c[abs(j-k)]/N) if abs(j-k)<N else 0
                      for k in range(length)] for j in range(length)])
    ev = np.linalg.eigvalsh(gram)
    toeplitz.append({"L": length, "min_Gram_eigenvalue": float(ev[0]),
                     "max_Gram_eigenvalue": float(ev[-1]),
                     "full_convolution_condition_number": float(np.sqrt(ev[-1]/ev[0]))})
out["floating_four_sign_Toeplitz_extrema"] = toeplitz

# A finite dyadic rounding experiment uses exhaustive tiny discrepancy choices.
# It verifies exact defect-mass accounting, not the Lovett-Meka implementation.
rounding = []
for n in range(2, 11):
    defect = [Fraction(((j*7+n) % 8), 16) for j in range(n)]
    mass0 = sum(defect)
    mass_history = [mass0]
    grid = np.arange(40*n)/(40*n)
    fourier = np.exp(2j*np.pi*grid[:, None]*np.arange(n)[None, :])
    for h in range(4, 0, -1):
        active = [j for j in range(n) if int(defect[j]*(2**h)) % 2]
        if not active:
            continue
        best = None
        for choice in product([-1, 1], repeat=len(active)):
            if sum(choice) > 0:
                continue
            val = float(np.max(np.abs(fourier[:, active] @ np.array(choice))))
            if best is None or val < best[0]:
                best = val, choice
        for j, direction in zip(active, best[1]):
            defect[j] += Fraction(direction, 2**h)
        assert all(0 <= p <= 1 for p in defect)
        assert sum(defect) <= mass_history[-1]
        mass_history.append(sum(defect))
    assert all(p in [0, 1] for p in defect)
    rounding.append({"N": n, "initial_mass": str(mass0),
                     "final_mass": str(sum(defect)),
                     "exact_monotone_mass_verified": True})
out["tiny_exhaustive_dyadic_mass_checks"] = rounding

# Exact acceptance test for a rational target distortion. Strict positivity
# makes the test complete for any candidate with a margin to the target.
def certify_strict_binary_bounds(signs, epsilon):
    n = len(signs)
    corr = [sum(signs[j]*signs[j+k] for j in range(n-k)) for k in range(n)]
    energy_poly = sp.expand(n + 2*sum(corr[k]*sp.chebyshevt(k, x)
                                     for k in range(1, n)))
    epsilon = sp.Rational(epsilon.numerator, epsilon.denominator)
    lower = sp.Poly(energy_poly - n*(1-epsilon)**2, x, domain=sp.QQ)
    upper = sp.Poly(n*(1+epsilon)**2 - energy_poly, x, domain=sp.QQ)
    tests = []
    for gap in [lower, upper]:
        endpoint_positive = bool(gap.eval(-1)>0 and gap.eval(1)>0)
        roots = int(gap.count_roots(-1, 1))
        tests.append({"endpoint_positive": endpoint_positive,
                      "number_of_real_gap_roots_on_interval": roots,
                      "strictly_positive": endpoint_positive and roots == 0})
    return {"epsilon": str(epsilon), "signs": signs,
            "certified": all(t["strictly_positive"] for t in tests),
            "lower_upper_exact_tests": tests}

out["exact_Sturm_strict_certificates"] = [
    certify_strict_binary_bounds([1,1,1,-1], Fraction(3,5)),
    certify_strict_binary_bounds([1,1,1,-1], Fraction(1,2)),
    certify_strict_binary_bounds([1,1,1,1,1,-1,-1,1,1,-1,1,-1,1], Fraction(2,5)),
]
assert out["exact_Sturm_strict_certificates"][0]["certified"]
assert not out["exact_Sturm_strict_certificates"][1]["certified"]
assert out["exact_Sturm_strict_certificates"][2]["certified"]

path = Path(__file__).with_name("number_wave_checks.json")
path.write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps(out, indent=2))
