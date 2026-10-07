"""Exact rational recognition of a fixed-rank complementary filter source.

Input: strictly positive rational tables b_j(0),...,b_j(q_j), q_j>=1,
and physical particle rank r. Recognizes whether
  g_(m-r)(x) = sum_|T|=m-r prod_j b_j(q_j-|T intersect E_j|) x^T
is Lorentzian. A rejected input includes residual block counts defining a
quadratic derivative with at least two positive Hessian eigenvalues.

The dynamic program uses O(m^2) rational operations. Rational bit complexity
is polynomial in the explicitly supplied table length. This is coefficient
recognition, not execution of an approximate counting or quantum compiler.
"""
from fractions import Fraction


def recognize_complementary(tables, rank):
    tables = tuple(tuple(Fraction(v) for v in b) for b in tables)
    if any(len(b) < 2 or any(v <= 0 for v in b) for b in tables):
        raise ValueError("Tables must have q>=1 and strictly positive rational entries.")
    sizes = tuple(len(b) - 1 for b in tables)
    m = sum(sizes)
    if not isinstance(rank, int) or not 0 <= rank <= m:
        raise ValueError("Particle rank must be an integer in [0,m].")
    degree = m - rank
    if degree <= 1:
        return {"accepted": True, "reason": "degree at most one", "m": m,
                "rank": rank, "degree": degree, "states": 1, "transitions": 0}

    target = rank + 2
    option_lists = []
    for b, q in zip(tables, sizes):
        options = [(0, 0, False, Fraction(0), None)]
        for n in range(1, min(q, target) + 1):
            delta = (Fraction(-1) if n == 1 else
                     (n - 1) * b[n] * b[n - 2] / b[n - 1] ** 2 - n)
            options.append((n, int(delta > 0), delta == 0,
                            Fraction(0) if delta == 0 else Fraction(n) / delta,
                            delta))
        option_lists.append(options)

    # State = (total residual modes, positive diagonal count capped at 2,
    #          presence of an active zero diagonal).
    current = {(0, 0, False): Fraction(0)}
    predecessors = []
    states = 1
    transitions = 0
    max_fraction_bits = 1
    for options in option_lists:
        following = {}
        pred = {}
        for key, cost in current.items():
            total, positives, has_zero = key
            for n, p, z, add, unused_delta in options:
                if total + n > target:
                    continue
                transitions += 1
                next_key = (total + n, min(2, positives + p), has_zero or z)
                next_cost = cost + add
                if next_key not in following or next_cost < following[next_key]:
                    following[next_key] = next_cost
                    pred[next_key] = (key, n)
                    max_fraction_bits = max(max_fraction_bits,
                                            next_cost.numerator.bit_length(),
                                            next_cost.denominator.bit_length())
        current = following
        predecessors.append(pred)
        states += len(current)

    rejected_key = next((key for key in current if key[0] == target and key[1] == 2), None)
    reason = "at least two positive diagonal entries"
    if rejected_key is None:
        key = (target, 1, True)
        if key in current:
            rejected_key = key
            reason = "one positive and an active zero diagonal entry"
    if rejected_key is None:
        key = (target, 1, False)
        if key in current and current[key] < -1:
            rejected_key = key
            reason = "one positive diagonal and negative Schur-complement scalar"

    common = {"m": m, "rank": rank, "degree": degree, "states": states,
              "transitions": transitions, "maximum_fraction_bits": max_fraction_bits}
    if rejected_key is None:
        return {"accepted": True, "reason": "every quadratic derivative passes", **common}

    residual = []
    key = rejected_key
    for pred in reversed(predecessors):
        key, n = pred[key]
        residual.append(n)
    residual.reverse()
    deltas = []
    for b, n in zip(tables, residual):
        deltas.append(None if n == 0 else
                      Fraction(-1) if n == 1 else
                      (n - 1) * b[n] * b[n - 2] / b[n - 1] ** 2 - n)
    result = {"accepted": False, "reason": reason, "residual_counts": residual,
              "forced_hole_counts": [q - n for q, n in zip(sizes, residual)],
              "diagonal_entries": [None if v is None else str(v) for v in deltas],
              **common}
    if rejected_key == (target, 1, False):
        result["schur_scalar"] = str(1 + current[rejected_key])
    return result


def recognize_direct(tables, rank):
    """Recognize h_r=sum_|S|r prod b_j(|S_j|)x^S via table reversal."""
    m = sum(len(b) - 1 for b in tables)
    result = recognize_complementary([list(reversed(b)) for b in tables], m - rank)
    return {**result, "orientation": "direct", "physical_rank": rank}


def recognize_counting_pair(tables, rank):
    """Admit the filter if either global complement orientation is log-concave."""
    complementary = recognize_complementary(tables, rank)
    if complementary["accepted"]:
        return {"accepted": True, "orientation": "complementary", "certificate": complementary}
    direct = recognize_direct(tables, rank)
    if direct["accepted"]:
        return {"accepted": True, "orientation": "direct", "certificate": direct}
    return {"accepted": False, "complementary": complementary, "direct": direct}
