"""Validated unnormalized Kubo correlations from untrusted full eigensystems.

Only proposal acquisition uses floating point. All physical entry enclosures,
Gram/residual products, observable products, logarithmic means and output
endpoints are exact rational/integer calculations. No eigenvalue gap is used.
The 25-state spin-two dimer has an independent exact-projector comparator.
See PROOF.md for the error inequalities and the intended thermal interface.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import itertools
import json
import math
import time
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

import numpy as np
import scipy.linalg as la

ROOT = Path(__file__).resolve().parent
HQ = 1 << 40
VQ = 1 << 40
SQ = 1 << 80
BITS = 112
S = 1 << BITS
DEGREE = 28


def floorq(x):
    return x.numerator // x.denominator


def ceilq(x):
    return -((-x.numerator) // x.denominator)


def serial(x):
    x = F(x)
    return f"{x.numerator}/{x.denominator}"


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F

    def __post_init__(self):
        assert self.lo <= self.hi

    def __add__(self, other):
        if not isinstance(other, Interval):
            other = Interval(F(other), F(other))
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if not isinstance(other, Interval):
            other = Interval(F(other), F(other))
        candidates = [x * y for x in (self.lo, self.hi)
                      for y in (other.lo, other.hi)]
        return Interval(min(candidates), max(candidates))

    __rmul__ = __mul__

    def divide_positive(self, denominator):
        assert denominator.lo > 0
        return self * Interval(1 / denominator.hi, 1 / denominator.lo)

    def contains(self, other):
        return self.lo <= other.lo <= other.hi <= self.hi

    def record(self):
        return {"lower": serial(self.lo), "upper": serial(self.hi),
                "display_only": [float(self.lo), float(self.hi)],
                "absolute_width_display_only": float(self.hi - self.lo)}


def fixed_interval(lo, hi):
    assert 0 <= lo <= hi
    return Interval(F(lo, S), F(hi, S))


def mul_fixed(a, b):
    """Nonnegative fixed-point product, rounded outwards."""
    return a[0] * b[0] // S, (a[1] * b[1] + S - 1) // S


@lru_cache(maxsize=None)
def exp_fixed(x):
    """exp(x), with exact rational x; endpoints are integers divided by S."""
    x = F(x)
    if x < 0:
        lo, hi = exp_fixed(-x)
        assert lo > 0
        return S * S // hi, (S * S + lo - 1) // lo
    k = 0
    while x > F(1, 2):
        x /= 2
        k += 1
    term = total = F(1)
    for j in range(1, DEGREE + 1):
        term = term * x / j
        total += term
    next_term = term * x / (DEGREE + 1)
    tail = next_term / (1 - x / (DEGREE + 2))
    lo, hi = floorq(total * S), ceilq((total + tail) * S)
    for _ in range(k):
        lo, hi = mul_fixed((lo, hi), (lo, hi))
    assert 0 < lo <= hi
    return lo, hi


@lru_cache(maxsize=None)
def psi_fixed(x):
    """psi(x)=integral_0^1 exp(-tx)dt, including psi(0)=1 exactly.

    The small-x series is positive, and the doubling step uses no subtraction
    or division by an energy gap. All intermediate intervals stay bounded.
    """
    x = F(x)
    assert x >= 0
    if x == 0:
        return S, S
    k = 0
    while x > F(1, 2):
        x /= 2
        k += 1
    term = total = F(1)  # phi(x)=(exp(x)-1)/x
    for j in range(1, DEGREE + 1):
        term = term * x / (j + 1)
        total += term
    next_term = term * x / (DEGREE + 2)
    tail = next_term / (1 - x / (DEGREE + 3))
    phi = floorq(total * S), ceilq((total + tail) * S)
    decay = exp_fixed(-x)
    psi = mul_fixed(phi, decay)
    for _ in range(k):
        # psi(2x)=psi(x)*(1+exp(-x))/2; use the OLD decay here.
        lo = psi[0] * (S + decay[0]) // (2 * S)
        hi = (psi[1] * (S + decay[1]) + 2 * S - 1) // (2 * S)
        psi = lo, min(S, hi)
        decay = mul_fixed(decay, decay)
    return psi[0], min(S, psi[1])


def exp_interval(x):
    return fixed_interval(*exp_fixed(F(x)))


@lru_cache(maxsize=None)
def logmean_reduced(x, y):
    """L(exp(-x),exp(-y)), for x,y>=0; exact at x=y=0."""
    x, y = F(x), F(y)
    assert min(x, y) >= 0
    return fixed_interval(*mul_fixed(exp_fixed(-min(x, y)),
                                    psi_fixed(abs(x - y))))


def int_array(a):
    """Promote BEFORE multiplying. No fixed-width integer GEMM is trusted."""
    return np.array([[int(x) for x in row] for row in a], dtype=object)


def max_sum(a, axis=1):
    rows = a if axis == 1 else a.T
    return max(sum(abs(int(x)) for x in row) for row in rows)


def assert_hermitian(ar, ai):
    assert np.array_equal(ar, ar.T)
    assert np.array_equal(ai, -ai.T)


def validate_proposal(qr, qi, eta, vr, vi, lam, hq=HQ, vq=VQ, lq=HQ):
    """Exact check of a square proposal; arbitrary eigensolver accuracy allowed."""
    qr, qi, vr, vi = map(int_array, (qr, qi, vr, vi))
    lam = np.array([int(x) for x in lam], dtype=object)
    d = len(qr)
    assert qr.shape == qi.shape == vr.shape == vi.shape == (d, d)
    assert len(lam) == d and eta >= 0 and min(hq, vq, lq) > 0
    assert_hermitian(qr, qi)
    gr = vr.T @ vr + vi.T @ vi - np.eye(d, dtype=object) * (vq * vq)
    gi = vr.T @ vi - vi.T @ vr
    gram_abs = np.abs(gr) + np.abs(gi)
    epsilon = F(max_sum(gram_abs), vq * vq)
    if epsilon > F(1, 2):
        raise ValueError("Gram precondition epsilon <= 1/2 failed")
    # H0 V - V Lambda, common denominator hq*vq*lq.
    rr = (qr @ vr - qi @ vi) * lq - (vr * lam[None, :]) * hq
    ri = (qr @ vi + qi @ vr) * lq - (vi * lam[None, :]) * hq
    res_abs = np.abs(rr) + np.abs(ri)
    residual = F(max(max_sum(res_abs), max_sum(res_abs, axis=0)), hq * vq * lq)
    hn = F(max_sum(np.abs(qr) + np.abs(qi)), hq)
    ln = F(max(abs(int(x)) for x in lam), lq)
    delta_original = eta + residual + F(3, 2) * epsilon * (hn + ln)
    # Hermiticity supplies a sharper polar bound through a positive
    # Sylvester equation; see PROOF.md Section1. This has no energy-offset
    # dependence and requires no eigenvalue gap.
    delta_hermitian = eta + residual / (1 - epsilon)
    delta = min(delta_original, delta_hermitian)
    alpha = epsilon * (4 + epsilon) / (4 - 2 * epsilon)
    return {"vr": vr, "vi": vi, "lam": [F(int(x), lq) for x in lam],
            "vq": vq, "epsilon": epsilon, "eta": F(eta),
            "residual": residual, "delta": delta, "alpha": alpha,
            "delta_original": delta_original, "delta_hermitian": delta_hermitian,
            "H0_norm_bound": hn, "Lambda_norm_bound": ln}


def transformed_observable(record, ar, ai, aq=1):
    """Exact Gaussian-rational V* A V. A=(ar+i ai)/aq is Hermitian."""
    ar, ai = map(int_array, (ar, ai))
    assert_hermitian(ar, ai)
    vr, vi = record["vr"], record["vi"]
    tr, ti = ar @ vr - ai @ vi, ar @ vi + ai @ vr
    re, im = vr.T @ tr + vi.T @ ti, vr.T @ ti - vi.T @ tr
    assert_hermitian(re, im)
    return re, im, aq * record["vq"] ** 2


def spectral_interval(energies, av, bv, beta, shift):
    ar, ai, aq = av
    br, bi, bq = bv
    d = len(energies)
    result = Interval(F(0), F(0))
    for i in range(d):
        for j in range(i, d):
            # Re(A_ij B_ji)=Re(A_ij conj(B_ij)). Hermiticity is checked.
            coefficient = F(int(ar[i, j] * br[i, j] + ai[i, j] * bi[i, j]), aq * bq)
            if i != j:
                coefficient *= 2
            if coefficient:
                weight = logmean_reduced(beta * (energies[i] - shift),
                                         beta * (energies[j] - shift))
                result += weight * coefficient
    return result


def certify_correlations(record, observables, pairs, beta=F(1)):
    """observables[name]=(integer real matrix,imag matrix,denominator,norm bound)."""
    assert beta >= 0
    energies = record["lam"]
    shift = min(energies)
    z_reduced = sum((exp_interval(-beta * (e - shift)) for e in energies),
                    Interval(F(0), F(0)))
    scale = exp_interval(-beta * shift)
    r = beta * record["delta"]
    exponent_error = exp_interval(r).hi - 1
    polar_error = record["alpha"] * (2 + record["epsilon"])
    transformed = {name: transformed_observable(record, *data[:3])
                   for name, data in observables.items()}
    output = {}
    for left, right in pairs:
        central = spectral_interval(energies, transformed[left], transformed[right], beta, shift)
        a, b = observables[left][3], observables[right][3]
        h_error = z_reduced.hi * a * b * exponent_error
        u_error = z_reduced.hi * a * b * polar_error
        total_error = h_error + u_error
        reduced = central + Interval(-total_error, total_error)
        if left == right:
            # Physical C_H(A,A)>=0; observables are Hermitian.
            reduced = Interval(max(F(0), reduced.lo), reduced.hi)
        physical = scale * reduced
        output[left + "," + right] = {
            "physical": physical.record(), "reduced": reduced.record(),
            "proposal_reduced": central.record(),
            "reduced_H_error_upper": serial(h_error),
            "reduced_polar_error_upper": serial(u_error),
            "physical_interval": physical, "reduced_interval": reduced}
    # Weyl bound around the same full diagonal proposal; no physical levels omitted.
    growth = exp_interval(r).hi
    z = scale * Interval(z_reduced.lo / growth, z_reduced.hi * growth)
    return {"correlations": output, "trace": z, "proposal_reduced_trace": z_reduced,
            "energy_shift": shift, "common_scale": scale,
            "dimensionless_H_error": r, "polar_factor": polar_error}


def dimer_exact():
    """h=S_left dot S_right as a+b sqrt(6), with exact integer matrices."""
    states = list(itertools.product(range(-2, 3), repeat=2))
    where = {w: i for i, w in enumerate(states)}
    a = np.zeros((25, 25), dtype=object)
    b = np.zeros_like(a)
    for col, (m, n) in enumerate(states):
        a[col, col] = m * n
        for step in (-1, 1):
            if not (-2 <= m + step <= 2 and -2 <= n - step <= 2):
                continue
            row = where[m + step, n - step]
            rad = (6 - m * (m + step)) * (6 - n * (n - step)) // 4
            if rad == 6:
                b[row, col] += 1
            else:
                root = math.isqrt(rad)
                assert root * root == rad
                a[row, col] += root
    assert np.array_equal(a, a.T) and np.array_equal(b, b.T)
    return states, a, b


def physical_rounding(a, b, multiplier=F(3)):
    sqrt_lo = F(math.isqrt(6 * SQ * SQ), SQ)
    sqrt_hi = sqrt_lo + F(1, SQ)
    assert sqrt_lo * sqrt_lo <= 6 <= sqrt_hi * sqrt_hi
    d = len(a)
    q = np.zeros((d, d), dtype=object)
    errors = [[F(0) for _ in range(d)] for _ in range(d)]
    for i in range(d):
        for j in range(d):
            lo, hi = sorted((multiplier * (a[i, j] + b[i, j] * sqrt_lo),
                             multiplier * (a[i, j] + b[i, j] * sqrt_hi)))
            midpoint = (lo + hi) * HQ / 2
            q[i, j] = (2 * midpoint.numerator + midpoint.denominator) // (2 * midpoint.denominator)
            errors[i][j] = max(abs(F(int(q[i, j]), HQ) - lo),
                               abs(F(int(q[i, j]), HQ) - hi))
    assert np.array_equal(q, q.T)
    return q, max(map(sum, errors))


def algebra_product(x, y):
    a, b = x
    c, d = y
    return a @ c + 6 * (b @ d), a @ d + b @ c


def exact_projectors(a, b):
    """Literal finite-dimensional comparator, without an eigensolver."""
    energies = [-6, -5, -3, 0, 4]
    eye = np.eye(len(a), dtype=object)
    zero = np.zeros_like(eye)
    projectors = []
    for j, e in enumerate(energies):
        numerator = (eye.copy(), zero.copy())
        denominator = 1
        for other in energies:
            if other != e:
                numerator = algebra_product(numerator, (a - other * eye, b))
                denominator *= e - other
        if denominator < 0:
            numerator = (-numerator[0], -numerator[1])
            denominator = -denominator
        pa, pb = numerator
        assert np.array_equal(pa, pa.T) and np.array_equal(pb, pb.T)
        annihilation = algebra_product((a - e * eye, b), numerator)
        assert not np.any(annihilation[0]) and not np.any(annihilation[1])
        squared = algebra_product(numerator, numerator)
        assert np.array_equal(squared[0], denominator * pa)
        assert np.array_equal(squared[1], denominator * pb)
        assert sum(pa[i, i] for i in range(len(a))) == (2 * j + 1) * denominator
        assert sum(pb[i, i] for i in range(len(a))) == 0
        projectors.append((pa, pb, denominator))
    # Completeness is verified entrywise over Q(sqrt(6)).
    for i in range(len(a)):
        for j in range(len(a)):
            assert sum(F(int(pa[i, j]), den) for pa, pb, den in projectors) == (i == j)
            assert sum(F(int(pb[i, j]), den) for pa, pb, den in projectors) == 0
    return energies, projectors


def projector_weights(projectors, left, right):
    rows = []
    for pa, pb, dp in projectors:
        row = []
        for qa, qb, dq in projectors:
            rational = root = 0
            for i in range(len(left)):
                for j in range(len(left)):
                    factor = int(left[j] * right[i])
                    rational += factor * (pa[i, j] * qa[j, i] + 6 * pb[i, j] * qb[j, i])
                    root += factor * (pa[i, j] * qb[j, i] + pb[i, j] * qa[j, i])
            assert root == 0
            row.append(F(int(rational), dp * dq))
        rows.append(row)
    assert rows == list(map(list, zip(*rows)))
    return rows


def projector_correlation(energies, weights, beta=F(1), multiplier=F(3)):
    physical_energies = [multiplier * e for e in energies]
    shift = min(physical_energies)
    reduced = Interval(F(0), F(0))
    for i in range(len(energies)):
        for j in range(len(energies)):
            if weights[i][j]:
                reduced += logmean_reduced(beta * (physical_energies[i] - shift),
                                           beta * (physical_energies[j] - shift)) * weights[i][j]
    return exp_interval(-beta * shift) * reduced


def main():
    start = time.monotonic()
    states, a, b = dimer_exact()
    qr, eta = physical_rounding(a, b)
    qi = np.zeros_like(qr)
    vals, vecs = la.eigh(np.asarray(qr, dtype=float) / HQ, check_finite=False)
    # Eigensolver outputs are only proposals. Round, then certify exactly.
    vr = np.rint(vecs.real * VQ).astype(np.int64)
    vi = np.zeros_like(vr)
    lam = np.rint(vals * HQ).astype(np.int64)
    record = validate_proposal(qr, qi, eta, vr, vi, lam)
    left = np.array([m for m, n in states], dtype=object)
    right = np.array([n for m, n in states], dtype=object)
    total = left + right
    zero = np.zeros((25, 25), dtype=object)
    obs = {"left": (np.diag(left), zero, 1, F(2)),
           "right": (np.diag(right), zero, 1, F(2)),
           "total": (np.diag(total), zero, 1, F(4))}
    pairs = [("left", "right"), ("left", "left"), ("total", "total")]
    certified = certify_correlations(record, obs, pairs)
    generic_seconds = time.monotonic() - start

    reference_start = time.monotonic()
    energies, projectors = exact_projectors(a, b)
    weights = {name: projector_weights(projectors, obs[l][0].diagonal(), obs[r][0].diagonal())
               for l, r in pairs for name in [l + "," + r]}
    reference = {name: projector_correlation(energies, w) for name, w in weights.items()}
    reference_trace = sum((exp_interval(-3 * F(e)) * (2 * j + 1)
                           for j, e in enumerate(energies)), Interval(F(0), F(0)))
    reference_seconds = time.monotonic() - reference_start
    for name, ref in reference.items():
        assert certified["correlations"][name]["physical_interval"].contains(ref)
    assert certified["trace"].contains(reference_trace)

    # Independent commuting-total-Sz rule, not another eigenvector calculation.
    commuting = sum((exp_interval(-3 * F(e)) * F(j * (j + 1) * (2 * j + 1), 3)
                    for j, e in enumerate(energies)), Interval(F(0), F(0)))
    assert commuting.contains(reference["total,total"]) or reference["total,total"].contains(commuting)
    # Exact coefficient identity implies C_LL+C_LR=C_MM/2 at every temperature.
    for i in range(5):
        for j in range(5):
            assert weights["left,left"][i][j] + weights["left,right"][i][j] == weights["total,total"][i][j] / 2
    assert sum(map(sum, weights["left,left"])) == 50
    assert sum(map(sum, weights["left,right"])) == 0
    assert sum(map(sum, weights["total,total"])) == 100
    assert all(weights["total,total"][i][j] == (F(i * (i + 1) * (2 * i + 1), 3) if i == j else 0)
               for i in range(5) for j in range(5))
    assert int(sum(a[i, i] for i in range(25))) == 0
    h2 = algebra_product((a, b), (a, b))
    assert sum(h2[0][i, i] for i in range(25)) == 300
    assert sum(h2[1][i, i] for i in range(25)) == 0

    # Invalid full eigenvector proposals must fail rather than masquerade as complete.
    bad_vr = vr.copy()
    bad_vr[:, 1] = bad_vr[:, 0]
    rejected_duplicate = False
    try:
        validate_proposal(qr, qi, eta, bad_vr, vi, lam)
    except ValueError:
        rejected_duplicate = True
    assert rejected_duplicate

    # A deliberately degraded proposal is still valid, with a wider enclosure.
    degraded_vr = vr.copy()
    degraded_vr[0, 0] += 1 << 15
    degraded_record = validate_proposal(qr, qi, eta, degraded_vr, vi, lam)
    degraded = certify_correlations(degraded_record, {k: obs[k] for k in ("left", "right")},
                                     [("left", "right")])
    assert degraded["correlations"]["left,right"]["physical_interval"].contains(reference["left,right"])

    correlation_records = {}
    for name, item in certified["correlations"].items():
        item = dict(item)
        physical = item.pop("physical_interval")
        item.pop("reduced_interval")
        item["normalized_diagnostic"] = physical.divide_positive(certified["trace"]).record()
        item["exact_projector_comparator"] = reference[name].record()
        item["contains_projector_interval"] = True
        correlation_records[name] = item
    source_moment = -certified["correlations"]["left,right"]["physical_interval"]
    sorted_lam = sorted(set(record["lam"]))
    min_positive_gap = min(y - x for x, y in zip(sorted_lam, sorted_lam[1:]))
    exact_records = {key: serial(record[key]) for key in
                     ("eta", "epsilon", "residual", "delta", "delta_original", "delta_hermitian", "alpha", "H0_norm_bound", "Lambda_norm_bound")}
    output = {
        "status": "VALIDATED_UNNORMALIZED_KUBO_DIMER_WITH_EXACT_PROJECTOR_CONTROL",
        "physical_model": "25-state open spin-two dimer; H_eff=3 S_left dot S_right, beta_eff=1",
        "source_interface": "p=0,r=s=1: source P0 moment is -C_H(Sz_left,Sz_right), with no Gibbs quotient, no extra beta, no 5 factor",
        "all_states": 25, "exact_physical_energies": [-18, -15, -9, 0, 12],
        "exact_energy_multiplicities": [1, 3, 5, 7, 9],
        "beta_eff": "1/1", "proposal_denominators": {"H0": str(HQ), "V": str(VQ), "Lambda": str(HQ)},
        "sqrt6_interval_width": serial(F(1, SQ)), "scalar_fixed_bits": BITS,
        "exact_proposal_bounds": exact_records,
        "display_only_bounds": {key: float(record[key]) for key in ("epsilon", "residual", "delta", "delta_original", "alpha")},
        "proposal_minimum_positive_gap": serial(min_positive_gap),
        "zero_gap_unordered_proposal_pairs": sum(record["lam"][i] == record["lam"][j] for i in range(25) for j in range(i + 1, 25)),
        "gap_assumption": False, "solver_accuracy_assumption": False,
        "energy_shift": serial(certified["energy_shift"]),
        "partition_trace": certified["trace"].record(),
        "exact_projector_trace": reference_trace.record(),
        "correlations": correlation_records,
        "source_P0_p0_moment": source_moment.record(),
        "exact_projector_Kubo_weights": {name: [[serial(x) for x in row] for row in w] for name, w in weights.items()},
        "controls": {"all_projectors_idempotent_complete_correct_energies": True,
                     "projector_trace_ranks": [1, 3, 5, 7, 9],
                     "Tr_h": "0/1", "Tr_h_squared": "300/1", "Tr_H_eff_squared": "2700/1",
                     "total_Sz_commuting_formula": True, "C_LL_plus_C_LR_equals_half_C_MM": True,
                     "beta0_C_LL": "50/1", "beta0_C_LR": "0/1", "beta0_C_MM": "100/1",
                     "duplicate_column_proposal_rejected": rejected_duplicate,
                     "degraded_proposal_still_contains_exact_reference": True,
                     "degraded_delta": serial(degraded_record["delta"]),
                     "degraded_C_LR": degraded["correlations"]["left,right"]["physical"],
                     "psi_zero_exact": psi_fixed(F(0)) == (S, S)},
        "measured_seconds": {"generic_physical_certificate": generic_seconds,
                             "exact_projector_comparator": reference_seconds,
                             "total_with_controls": time.monotonic() - start},
        "scope": "Small physical input and reusable validation operation; no later connected thermal input, gap, six-site cost or general speed advantage acquired."
    }
    (ROOT / "KUBO_CERTIFICATE.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"status": output["status"], "bounds": output["display_only_bounds"],
                      "C_LR": output["correlations"]["left,right"]["physical"]["display_only"],
                      "source_moment": output["source_P0_p0_moment"]["display_only"],
                      "C_LR_normalized_diagnostic": output["correlations"]["left,right"]["normalized_diagnostic"]["display_only"],
                      "C_LR_absolute_width": output["correlations"]["left,right"]["physical"]["absolute_width_display_only"],
                      "seconds": output["measured_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
