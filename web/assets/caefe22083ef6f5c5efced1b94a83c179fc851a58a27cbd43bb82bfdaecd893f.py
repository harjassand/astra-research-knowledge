#!/usr/bin/env python3
"""Small exact mechanism replay, not a generic quantum-channel compiler.

Uses one depth of a rational qubit copy/cloning mixture. Every mathematical
comparison below is exact over rational complex entries; floats are display
only. A seeded pseudorandom source makes the sampler diagnostic reproducible.
The theorem's Las Vegas algorithm instead assumes independent unbiased bits.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import time

import sympy as sp


HERE = Path(__file__).resolve().parent
R = sp.Rational
I = sp.I
d = 2
ID = sp.eye(d)
PAULI = [ID, sp.Matrix([[0, 1], [1, 0]]),
         sp.Matrix([[0, -I], [I, 0]]), sp.diag(1, -1)]
DELTA = R(1, 100)
# Optional warm start: the final exact certificate, not concentration, decides.
WARM_T = 40
WARM_EPSILON = R(1, 20)
SEED = 20261009


def clean(matrix):
    return matrix.applyfunc(sp.expand)


def tr(matrix):
    return sp.expand(sp.trace(matrix))


def psd_factors(matrix):
    """Exact pivoted LDL rank-one factors, including zero-pivot decisions."""
    residual = clean(matrix)
    assert residual == residual.H
    factors = []
    pivots = []
    while residual != sp.zeros(residual.rows):
        diagonal = [residual[i, i] for i in range(residual.rows)]
        if any(x < 0 for x in diagonal):
            return None
        positive = [i for i, x in enumerate(diagonal) if x > 0]
        if not positive:
            return None  # zero diagonals with a nonzero row cannot be PSD
        pivot = positive[0]
        q = residual[pivot, pivot]
        v = residual[:, pivot] / q
        factors.append((q, v))
        pivots.append(q)
        residual = clean(residual - q * v * v.H)
    return factors, pivots


def require_psd(matrix, label):
    result = psd_factors(matrix)
    assert result is not None, label
    factors, pivots = result
    rebuilt = sp.zeros(matrix.rows)
    for q, v in factors:
        rebuilt += q * v * v.H
    assert clean(rebuilt) == matrix, label + " reconstruction"
    return pivots


def adjoint(branch, output_effect):
    q, w = branch
    return clean(q * w.H * output_effect * w)


def channel(branches, state):
    result = sp.zeros(4)
    for q, w in branches:
        result += q * w * state * w.H
    return clean(result)


def partial_trace_left(state):
    return sp.Matrix(2, 2,
                     lambda i, j: sum(state[2*i+k, 2*j+k] for k in range(2)))


def partial_trace_right(state):
    return sp.Matrix(2, 2,
                     lambda i, j: sum(state[2*k+i, 2*k+j] for k in range(2)))


def pauli_vector(posterior):
    return sp.Matrix([tr(e * posterior) for e in PAULI])


def canonical_matrix(effects):
    result = sp.zeros(4)
    for effect in effects:
        mass = tr(effect)
        if mass == 0:
            continue
        posterior = effect / mass
        a = pauli_vector(posterior)
        result += (mass / d) * a * a.T
    return clean(result)


def rational_json(x):
    x = sp.expand(x)
    real, imag = x.as_real_imag()
    return {"real": str(real), "imag": str(imag)}


def matrix_json(matrix):
    return [[rational_json(matrix[i, j]) for j in range(matrix.cols)]
            for i in range(matrix.rows)]


def input_height(matrix):
    bit_height = 0
    for z in matrix:
        for x in z.as_real_imag():
            numerator, denominator = sp.fraction(x)
            bit_height = max(bit_height, abs(int(numerator)).bit_length(),
                             int(denominator).bit_length())
    return bit_height


def scalar_depth_certificate(r, delta_tree):
    """Exact Sturm certificate for a uniform, spectrum-independent depth."""
    lam = sp.Symbol("lambda")
    lo = (3 + delta_tree) / 4
    m = 0
    while R(r) * R(8, 9)**m > delta_tree:
        m += 1
    safe_m = m
    attempts = []
    for m in range(safe_m + 1):
        polynomial = sp.Poly(
            (2*(1-lam)**2+delta_tree)*(2*lam**2)**m
            -(4*lam-3-delta_tree)*(r*(2*lam**2-1)-1), lam)
        endpoints_positive = polynomial.eval(lo) > 0 and polynomial.eval(1) > 0
        roots = int(polynomial.count_roots(lo, 1))
        attempts.append({"depth": m, "roots_on_interval": roots,
                         "positive_endpoints": bool(endpoints_positive)})
        if endpoints_positive and roots == 0:
            return {"r": r, "delta_tree": str(delta_tree),
                    "certified_depth": m, "safe_depth": safe_m,
                    "leaves": 2**m, "safe_leaves": 2**safe_m,
                    "interval": [str(lo), "1"],
                    "polynomial": str(polynomial.as_expr()),
                    "attempts": attempts}
    raise AssertionError("safe depth failed exact uniform scalar certificate")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None,
                        help="Optional evidence JSON destination; default does not edit frozen evidence.")
    args = parser.parse_args()
    started = time.monotonic()
    checks = []

    def checked(label, condition=True):
        assert condition, label
        checks.append(label)

    sym = sp.Matrix([[1, 0, 0, 0], [0, R(1, 2), R(1, 2), 0],
                     [0, R(1, 2), R(1, 2), 0], [0, 0, 0, 1]])
    hand_branches = []
    for j in range(2):
        copied = sp.zeros(4, 2)
        copied[3*j, j] = 1
        hand_branches.append((R(9, 10), copied))
        embedded = sp.zeros(4, 2)
        for k in range(2):
            embedded[2*k+j, k] = 1
        hand_branches.append((R(1, 15), sym * embedded))

    choi = sp.zeros(8)
    for q, w in hand_branches:
        v = sp.Matrix([w[alpha, i] for i in range(2) for alpha in range(4)])
        choi += q * v * v.H
    choi = clean(choi)
    factors, _ = psd_factors(choi)
    branches = [(q, sp.Matrix(4, 2, lambda alpha, i: v[4*i+alpha]))
                for q, v in factors]
    checked("rational Choi PSD and LDL reconstruction",
            clean(sum((q*v*v.H for q, v in factors), sp.zeros(8))) == choi)
    checked("LDL Kraus orientation and TP",
            clean(sum((q*w.H*w for q, w in branches), sp.zeros(2))) == ID)
    for e in PAULI:
        checked("LDL and supplied broadcaster agree on " + str(PAULI.index(e)),
                channel(branches, e) == channel(hand_branches, e))

    phi_matrix = sp.zeros(4)
    for j, e in enumerate(PAULI):
        output = channel(branches, e)
        left, right = partial_trace_left(output), partial_trace_right(output)
        checked("both marginals agree on Pauli " + str(j), left == right)
        for i, f in enumerate(PAULI):
            phi_matrix[i, j] = tr(f * left) / 2
    expected_phi = sp.diag(1, R(1, 15), R(1, 15), R(29, 30))
    checked("marginal bistochastic HS-self-adjoint and exact eigenvalues",
            phi_matrix == expected_phi)

    vectors = [sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([1, 1]),
               sp.Matrix([1, -1]), sp.Matrix([1, I]), sp.Matrix([1, -I])]
    leaves = [v*v.H / (3*(v.H*v)[0]) for v in vectors]
    checked("fixed rational rank-one leaf sums to I", sum(leaves, sp.zeros(2)) == ID)
    leaf_canonical = canonical_matrix(leaves)
    checked("fixed IC leaf spectrum", leaf_canonical == sp.diag(1, R(1, 3), R(1, 3), R(1, 3)))
    leaf_target = (3 + DELTA)*sp.eye(4) - 4*phi_matrix + leaf_canonical
    checked("leaf comparator fails target on nontrivial slow Z mode",
            leaf_target[3, 3] < 0)

    records = {}
    for j, zl, zr in itertools.product(range(len(branches)), range(6), range(6)):
        effect = adjoint(branches[j], sp.kronecker_product(leaves[zl], leaves[zr]))
        records[(j, zl, zr)] = effect
        checked("fine record rank <=1: " + str((j, zl, zr)), effect.det() == 0)
    checked("fine effects sum exactly to I", sum(records.values(), sp.zeros(2)) == ID)
    fine_cov = canonical_matrix(records.values())
    checked("fine common comparator fixes identity", fine_cov[:, 0] == sp.Matrix([1, 0, 0, 0]))
    checked("fine common comparator full C4 certificate",
            psd_factors((3 + DELTA)*sp.eye(4)-4*phi_matrix+fine_cov) is not None)

    coarse_effects = [sum((records[(j, zl, zr)] for j in range(len(branches))),
                          sp.zeros(2)) for zl in range(6) for zr in range(6)]
    coarse_cov = canonical_matrix(coarse_effects)
    coarse_target = (3+DELTA)*sp.eye(4)-4*phi_matrix+coarse_cov
    checked("one-depth COARSE comparator also fails on slow Z mode",
            coarse_target[3, 3] < 0)
    fine_minus_coarse_pivots = require_psd(fine_cov-coarse_cov, "refinement full Schur order")
    checked("fine >= coarse canonical channel on FULL Hermitian space")

    contraction_cache = {}

    def partial_effect(h):
        if h not in contraction_cache:
            j, zl, zr = h
            left = ID if zl is None else leaves[zl]
            right = ID if zr is None else leaves[zr]
            output_effect = sp.kronecker_product(left, right)
            active = branches if j is None else [branches[j]]
            contraction_cache[h] = clean(sum(
                (adjoint(branch, output_effect) for branch in active), sp.zeros(2)))
        return contraction_cache[h]

    def probability(h):
        return tr(partial_effect(h)) / 2

    domains = [range(len(branches)), range(6), range(6)]
    partial_count = 0
    for h in itertools.product(*[[None, *domain] for domain in domains]):
        enumerated = sp.zeros(2)
        for w, effect in records.items():
            if all(v is None or v == w[i] for i, v in enumerate(h)):
                enumerated += effect
        checked("partial contraction equals exact enumeration: " + str(h),
                partial_effect(h) == clean(enumerated))
        require_psd(partial_effect(h), "partial effect")
        require_psd(ID-partial_effect(h), "partial complement")
        partial_count += 1
        for i, domain in enumerate(domains):
            if h[i] is None:
                children = []
                for v in domain:
                    child = list(h)
                    child[i] = v
                    children.append(probability(tuple(child)))
                checked("conditional integer normalization: " + str((h, i)),
                        sum(children) == probability(h))

    # Specifically exhibits correlated siblings, so independent sampling is wrong.
    p_both = probability((None, 0, 0))
    p_left = probability((None, 0, None))
    p_right = probability((None, None, 0))
    checked("sibling outcomes are NOT independent", p_both != p_left*p_right)

    # Verify every positive complete-record chain, with a deliberately noncausal order.
    order = [1, 0, 2]  # left leaf, internal Kraus, right leaf
    for w, effect in records.items():
        if tr(effect) == 0:
            continue
        h = [None, None, None]
        product_probability = R(1)
        for variable in order:
            old_probability = probability(tuple(h))
            h[variable] = w[variable]
            product_probability *= probability(tuple(h)) / old_probability
        checked("exact sampled chain law: " + str(w), product_probability == tr(effect)/2)

    # First moment and sibling second moment for the slow mode.
    lam_z = R(29, 30)
    c_zz = tr(channel(branches, ID/2) * sp.kronecker_product(PAULI[3], PAULI[3]))
    cross = sp.zeros(4, 1)
    moment = R(0)
    mean = R(0)
    for (j, zl, zr), effect in records.items():
        mass = tr(effect)
        if mass == 0:
            continue
        a = pauli_vector(effect/mass)
        az_left = tr((3*leaves[zl])*PAULI[3])
        az_right = tr((3*leaves[zr])*PAULI[3])
        estimator = 3*(az_left+az_right)/(2*lam_z)
        p = mass/2
        mean += p*estimator
        moment += p*estimator**2
        cross += p*a*estimator
    checked("unbiased coarse estimator retained after fine refinement",
            mean == 0 and cross == sp.Matrix([0, 0, 0, 1]))
    checked("correlated exact sibling moment recursion",
            moment == (3+c_zz)/(2*lam_z**2) and c_zz == R(14, 15))
    full_moment = fine_cov.row_join(cross).col_join(cross.T.row_join(sp.Matrix([[moment]])))
    require_psd(full_moment, "full posterior-estimator crossmoment")
    require_psd(fine_cov-cross*cross.T/moment, "full Schur comparator")
    checked("FULL crossmoment PSD and common-channel Schur complement")

    rng = random.Random(SEED)
    random_bits = 0
    rejections = 0

    def exact_integer_below(n):
        nonlocal random_bits, rejections
        assert n > 0
        bits = (n-1).bit_length()
        while True:
            random_bits += bits
            value = rng.getrandbits(bits)
            if value < n:
                return value
            rejections += 1

    def sample_record():
        h = [None, None, None]
        for variable in order:
            weights = []
            for value in domains[variable]:
                child = h.copy()
                child[variable] = value
                weights.append(probability(tuple(child)))
            denominator = math.lcm(*(int(sp.denom(x)) for x in weights))
            integers = [int(x*denominator) for x in weights]
            total = sum(integers)
            assert R(total, denominator) == probability(tuple(h))
            draw = exact_integer_below(total)
            accumulated = 0
            for value, weight in enumerate(integers):
                accumulated += weight
                if draw < accumulated:
                    h[variable] = value
                    break
            else:
                raise AssertionError("categorical integer sample failed")
        return tuple(h)

    rejected_first = 0
    rejected_second = 0
    for batch_number in range(1, 513):
        sampled_records = [sample_record() for _ in range(WARM_T)]
        sampled_posteriors = [records[w]/tr(records[w]) for w in sampled_records]
        s_matrix = clean((R(2, WARM_T))*sum(sampled_posteriors, sp.zeros(2)))
        residual = clean(ID-s_matrix/(1+WARM_EPSILON))
        residual_decomposition = psd_factors(residual)
        if residual_decomposition is None:
            rejected_first += 1
            continue
        effects = [clean(R(2, WARM_T)/(1+WARM_EPSILON)*pi)
                   for pi in sampled_posteriors]
        residual_factors, _ = residual_decomposition
        effects += [clean(q*v*v.H) for q, v in residual_factors]
        candidate = canonical_matrix(effects)
        qform = clean((3+DELTA)*sp.eye(4)-4*phi_matrix+candidate)
        q_factors = psd_factors(qform)
        if q_factors is None:
            rejected_second += 1
            continue
        break
    else:
        raise AssertionError("bounded warm-start diagnostic found no certified batch")

    checked("sampled/residual POVM sums exactly to I", sum(effects, sp.zeros(2)) == ID)
    for effect in effects:
        checked("returned effect rank-one or zero", effect.det() == 0)
        require_psd(effect, "returned effect PSD")
    checked("returned canonical channel fixes identity", candidate[:, 0] == sp.Matrix([1, 0, 0, 0]))
    checked("returned channel is full HS-self-adjoint", candidate == candidate.T)
    require_psd(candidate, "returned canonical HS PSD")
    require_psd(sp.eye(4)-candidate, "returned canonical HS contraction")
    final_pivots = require_psd(qform, "FULL exact target certificate")
    checked("returned FULL C4+delta certificate")

    # Preserve a concrete negative control: direct empirical covariance is not TP.
    unbalanced = [vectors[0]*vectors[0].H]*7 + [vectors[1]*vectors[1].H]*3
    bad_effects = [R(2, 10)*pi for pi in unbalanced]
    bad_mean = sum(bad_effects, sp.zeros(2))
    checked("direct empirical candidate is NOT unital/TP", bad_mean != ID)
    checked("unbalanced sample rejected by first structural test",
            psd_factors((1+WARM_EPSILON)*ID-bad_mean) is None)

    # These are uniform scalar certificates, not tests on this one Phi spectrum.
    scalar_certificates = [scalar_depth_certificate(r, DELTA/8) for r in [3, 5]]
    checked("two exact Sturm uniform depth certificates")

    atoms = []
    for effect in effects:
        mass = tr(effect)
        if mass:
            atoms.append({"effect": matrix_json(effect),
                          "posterior": matrix_json(effect/mass),
                          "mass": str(mass)})
    output = {
        "status": "EXACT_FINITE_DIAGNOSTICS_PASS",
        "scope": "one-depth rational qubit control and two uniform scalar depth certificates; not a generic compiler",
        "matrix_input": "B=(9/10) computational dephase-and-copy+(1/10) universal 1->2 cloner",
        "choi": matrix_json(choi), "choi_max_coefficient_bits": input_height(choi),
        "phi_pauli_matrix": matrix_json(phi_matrix),
        "fine_kraus_count": len(branches), "raw_fine_record_count": len(records),
        "nonzero_fine_record_count": sum(bool(tr(m)>0) for m in records.values()),
        "partial_events_checked": partial_count,
        "conditional_variable_order": order,
        "leaf_Z_certificate_slack": str(leaf_target[3, 3]),
        "coarse_Z_certificate_slack": str(coarse_target[3, 3]),
        "fine_canonical_pauli_matrix": matrix_json(fine_cov),
        "coarse_canonical_pauli_matrix": matrix_json(coarse_cov),
        "fine_minus_coarse_PSD_pivots": [str(x) for x in fine_minus_coarse_pivots],
        "sibling_joint_probability": str(p_both),
        "sibling_product_probability": str(p_left*p_right),
        "sibling_correlation_C_ZZ": str(c_zz),
        "estimator_second_moment": str(moment),
        "warm_delta": str(DELTA), "warm_epsilon": str(WARM_EPSILON),
        "warm_T": WARM_T, "seed": SEED, "accepted_batch": batch_number,
        "rejected_first_test": rejected_first, "rejected_second_test": rejected_second,
        "seeded_random_bits": random_bits, "integer_rejections": rejections,
        "accepted_fine_records": [list(w) for w in sampled_records],
        "returned_support": len(atoms), "returned_atoms": atoms,
        "returned_pauli_matrix": matrix_json(candidate),
        "full_certificate_pauli_matrix": matrix_json(qform),
        "full_certificate_PSD_pivots": [str(x) for x in final_pivots],
        "returned_max_coefficient_bits": max(input_height(m) for m in effects),
        "scalar_depth_certificates": scalar_certificates,
        "exact_assertions": len(checks), "checks": checks,
        "elapsed_seconds": round(time.monotonic()-started, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    target = args.output
    if target is not None:
        target.write_text(json.dumps(output, indent=2, sort_keys=True)+"\n")
    print(json.dumps({k: output[k] for k in [
        "status", "scope", "partial_events_checked", "exact_assertions",
        "leaf_Z_certificate_slack", "fine_kraus_count", "accepted_batch",
        "rejected_first_test", "rejected_second_test", "returned_support",
        "returned_max_coefficient_bits", "seeded_random_bits", "elapsed_seconds"]}, indent=2))
    print("Exact scalar uniform depths:", [(c["r"], c["certified_depth"], c["safe_depth"])
                                           for c in scalar_certificates])
    print("Full certificate pivots positive:", all(x>0 for x in final_pivots))
    print("Evidence:", target if target is not None else "not saved; supplied frozen evidence unchanged")


if __name__ == "__main__":
    main()
