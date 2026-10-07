"""Finite algebra and falsification checks, not a counting/preparation algorithm."""
import itertools
import json
import math
from fractions import Fraction as Q
from pathlib import Path

import numpy as np


class GQ:
    """Gaussian rationals with no floating-point arithmetic."""
    def __init__(self, real=0, imag=0):
        if isinstance(real, GQ):
            self.real, self.imag = real.real, real.imag
        else:
            self.real, self.imag = Q(real), Q(imag)

    def __add__(self, other):
        other = GQ(other)
        return GQ(self.real + other.real, self.imag + other.imag)

    __radd__ = __add__

    def __mul__(self, other):
        other = GQ(other)
        return GQ(self.real * other.real - self.imag * other.imag,
                  self.real * other.imag + self.imag * other.real)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = GQ(other)
        norm = other.real ** 2 + other.imag ** 2
        return GQ((self.real * other.real + self.imag * other.imag) / norm,
                  (self.imag * other.real - self.real * other.imag) / norm)

    def __eq__(self, other):
        other = GQ(other)
        return self.real == other.real and self.imag == other.imag

    def __bool__(self):
        return bool(self.real or self.imag)


def abs2(value):
    if isinstance(value, GQ):
        return value.real ** 2 + value.imag ** 2
    return value ** 2


def subsets(n, k):
    return itertools.combinations(range(n), k)


def det(M):
    n = len(M)
    if not n:
        return 1
    ans = 0
    for p in itertools.permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        val = (-1) ** inv
        for i, j in enumerate(p):
            val *= M[i][j]
        ans += val
    return ans


def creation(state, mode):
    out = {}
    for mask, amplitude in state.items():
        if mask & (1 << mode):
            continue
        sign = (-1) ** (mask & ((1 << mode) - 1)).bit_count()
        new = mask | (1 << mode)
        out[new] = out.get(new, 0) + sign * amplitude
    return out


def pair_operator(state, F):
    n = len(F)
    out = {}
    for i in range(n):
        for j in range(n):
            # Rightmost d_j^dagger acts first.
            term = creation(creation(state, n + j), i)
            for mask, amplitude in term.items():
                out[mask] = out.get(mask, 0) + F[i][j] * amplitude
    return {mask: amp for mask, amp in out.items() if amp}


def exp_pair(F):
    n = len(F)
    term = {0: Q(1)}
    out = dict(term)
    for k in range(1, n + 1):
        term = pair_operator(term, F)
        for mask, amplitude in term.items():
            out[mask] = out.get(mask, 0) + amplitude / math.factorial(k)
    return {mask: amp for mask, amp in out.items() if amp}


def exact_mapping():
    cases = []
    totals = 0
    rng = np.random.default_rng(404071)
    for n in range(1, 5):
        for trial in range(6):
            F = [[GQ(Q(int(rng.integers(-3, 4)), int(rng.integers(1, 5))),
                     Q(int(rng.integers(-3, 4)), int(rng.integers(1, 5))))
                  for _ in range(n)] for _ in range(n)]
            t = [Q(int(rng.integers(1, 17)), 2) for _ in range(n)]
            Fock = exp_pair(F)
            A = F + [[Q(i == j) for j in range(n)] for i in range(n)]
            norm0 = Q(0)
            norm1 = Q(0)
            for k in range(n + 1):
                for U in subsets(n, k):
                    for D in subsets(n, k):
                        H = tuple(i for i in range(n) if i not in D)
                        rows = U + tuple(n + i for i in H)
                        minor = det([A[i] for i in rows])
                        physical_mask = sum(1 << i for i in U) + sum(1 << (n + i) for i in D)
                        # X on all holes, then Z on odd zero-based physical down modes.
                        mapped = (-1) ** sum(D) * minor
                        assert mapped == Fock.get(physical_mask, 0)
                        amplitude = (-1) ** (k * (k - 1) // 2) * det([[F[i][j] for j in D] for i in U])
                        assert mapped == amplitude
                        w_physical = abs2(amplitude)
                        for i in set(U).intersection(D):
                            w_physical *= t[i]
                        w_nambu = abs2(minor)
                        for i in U:
                            w_nambu *= t[i]
                        for i in set(U).intersection(H):
                            w_nambu /= t[i]
                        assert w_physical == w_nambu
                        norm0 += w_physical
                        norm1 += w_nambu
                        totals += 1
            assert norm0 == norm1
            cases.append({"n": n, "trial": trial, "norm": str(norm0)})
    return {"matrix_cases": len(cases), "exact_amplitude_weight_checks": totals, "pass": True}


def exact_clone_identity():
    rng = np.random.default_rng(941115)
    cases = 0
    coeffs = 0
    retained = 0
    for n in range(1, 5):
        for trial in range(3):
            F = [[GQ(Q(int(rng.integers(-2, 3)), 3), Q(int(rng.integers(-2, 3)), 2))
                  for _ in range(n)] for _ in range(n)]
            # Pythagorean weights make both cloned columns Gaussian rational.
            v = [Q(3, 5) if (i + trial) % 2 else Q(5, 13) for i in range(n)]
            w = [Q(4, 5) if (i + trial) % 2 else Q(12, 13) for i in range(n)]
            t = [x * x for x in w]
            augmented = [[F[i][j] * v[j] for j in range(n)] +
                         [F[i][j] * w[j] for j in range(n)] for i in range(n)]
            Z = [Q(0) for _ in range(n + 1)]
            for k in range(n + 1):
                for U in subsets(n, k):
                    for D in subsets(n, k):
                        val = abs2(det([[F[i][j] for j in D] for i in U]))
                        for i in set(U).intersection(D):
                            val *= t[i]
                        Z[k] += val
            # Sum coefficients of principal characteristic polynomials for all
            # fixed-size retained sets: one U_i or V_i plus every W_i.
            avg = [Q(0) for _ in range(n + 1)]
            for choice in itertools.product([0, 1], repeat=n):
                us = [i for i in range(n) if choice[i] == 0]
                ds = [i for i in range(n) if choice[i] == 1] + list(range(n, 2 * n))
                retained += 1
                for k in range(min(len(us), len(ds)) + 1):
                    for U in itertools.combinations(us, k):
                        for D in itertools.combinations(ds, k):
                            val = abs2(det([[augmented[i][j] for j in D] for i in U]))
                            # Vertex sqrt(2) on U and V; W vertex scale 1.
                            val *= 2 ** (k + sum(j < n for j in D))
                            avg[k] += val / (2 ** n)
            assert avg == Z, (n, trial, avg, Z)
            coeffs += n + 1
            cases += 1
    return {"Gaussian_rational_matrix_cases": cases, "exact_coefficient_identities": coeffs, "fixed_size_retained_sets": retained, "pass": True}


def pair_count_weights(F, t):
    n = len(F)
    z = []
    for k in range(n + 1):
        val = 0.0
        for U in subsets(n, k):
            for D in subsets(n, k):
                weight = abs(np.linalg.det(F[np.ix_(U, D)])) ** 2 if k else 1.0
                for i in set(U).intersection(D):
                    weight *= t[i]
                val += weight
        z.append(val)
    return np.array(z)


def charge_search():
    rng = np.random.default_rng(778303)
    failures = []
    realroot_failures = []
    cases = 0
    for n, trials in [(3, 1200), (4, 1000), (5, 500)]:
        for trial in range(trials):
            F = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
            # Entrywise scales test ill-conditioned and nonuniform pair geometry.
            if trial % 3 == 1:
                F *= np.exp(rng.uniform(-3, 3, size=(n, n)))
            elif trial % 3 == 2:
                F = np.diag(np.diag(F)) + 10 ** rng.uniform(-2, 1) * F
            t = rng.uniform(0.5, 1.0, size=n)
            Z = pair_count_weights(F, t)
            cases += 1
            ratios = Z[1:-1] ** 2 / (Z[:-2] * Z[2:])
            if min(ratios) < 1 - 1e-9:
                failures.append({"n": n, "trial": trial, "t": t.tolist(), "Freal": F.real.tolist(), "Fimag": F.imag.tolist(), "Z": Z.tolist(), "ratio": float(min(ratios))})
                return {"numeric_cases": cases, "ordinary_logconcavity_failures": failures, "real_root_failures": realroot_failures[:3]}
            roots = np.roots(Z[::-1])
            if max(abs(roots.imag)) > 1e-7 * max(1, max(abs(roots))):
                realroot_failures.append({"n": n, "trial": trial, "t": t.tolist(), "Freal": F.real.tolist(), "Fimag": F.imag.tolist(), "Z": Z.tolist(), "roots": [[float(z.real), float(z.imag)] for z in roots]})
    return {"numeric_cases": cases, "ordinary_logconcavity_failures": failures, "real_root_failures_count": len(realroot_failures), "real_root_failures": realroot_failures[:3]}


def exact_barriers():
    # n=2 auxiliary charge slice with a=2 (allowed t=1/2).
    M = np.array([[2, 1], [1, 2]], dtype=float)
    H = np.block([[np.zeros((2, 2)), M], [M.T, np.zeros((2, 2))]])
    # On the all-ones point, the two sign-balanced within-side directions
    # give a positive log-Hessian quadratic form.
    v = np.array([1, -1, 1, -1], dtype=float)
    assert v @ H @ v == 4
    assert sum(v) == 0
    # For T>1, Z=1+2z+T^2 z^2, p1 is maximized at z=1/T.
    T = Q(2) ** 80
    pbest = 1 / (T + 1)
    return {"auxiliary_charge_slice_H_eigenvalues": np.linalg.eigvalsh(H).tolist(), "log_hessian_witness_vHv": 4, "fugacity_T": str(T), "fugacity_best_p_k1": str(pbest)}


if __name__ == "__main__":
    result = {"exact_mapping": exact_mapping(), "exact_clone_identity": exact_clone_identity(), "exact_barriers": exact_barriers(), "charge_search": charge_search()}
    target = Path(__file__).with_name("paired_fermion_checks_result.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"exact_mapping": result["exact_mapping"], "exact_clone_identity": result["exact_clone_identity"], "exact_barriers": result["exact_barriers"], "charge_search_cases": result["charge_search"]["numeric_cases"], "charge_LC_failures": len(result["charge_search"]["ordinary_logconcavity_failures"]), "charge_realroot_failures": result["charge_search"].get("real_root_failures_count", "early_exit")}))
