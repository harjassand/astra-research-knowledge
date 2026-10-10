"""Exact coefficient extraction in P(x)^K over a prime field.

The input polynomial is an explicit list of (nonnegative exponent, coefficient)
pairs.  Powers are never expanded: Frobenius splits K into base-p digits, and
a carry DP sums all contributions exactly modulo p.
"""

from __future__ import annotations

from typing import Iterable


Poly = dict[int, int]  # exponent -> coefficient; zero coefficients are omitted


def _mul(a: Poly, b: Poly, p: int) -> Poly:
    out: Poly = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = ea + eb
            value = (out.get(e, 0) + ca * cb) % p
            if value:
                out[e] = value
            else:
                out.pop(e, None)
    return out


def _digit_length(n: int, p: int) -> int:
    if n == 0:
        return 1
    length = 0
    while n:
        length += 1
        n //= p
    return length


def coefficient_of_power(
    terms: Iterable[tuple[int, int]], p: int, K: int, N: int
) -> tuple[int, dict[str, int]]:
    """Return [x^N]P(x)^K in F_p plus compact run diagnostics.

    p must be prime; K,N and exponents must be nonnegative.  The algorithm is
    deterministic and handles cancellations by reducing every local product
    and carry-state sum in F_p.
    """
    if p < 2 or K < 0 or N < 0:
        raise ValueError("require p >= 2 and nonnegative K,N")

    P: Poly = {}
    for exponent, coefficient in terms:
        if exponent < 0:
            raise ValueError("polynomial exponents must be nonnegative")
        value = (P.get(exponent, 0) + coefficient) % p
        if value:
            P[exponent] = value
        else:
            P.pop(exponent, None)

    if K == 0:
        return int(N == 0), {"degree": max(P, default=-1), "digits": 0, "peak_carries": 1}
    if not P:
        return 0, {"degree": -1, "digits": 0, "peak_carries": 0}

    degree = max(P)
    if degree == 0:
        answer = pow(P[0], K, p) if N == 0 else 0
        return answer, {"degree": 0, "digits": 1, "peak_carries": 1}
    if N > degree * K:
        return 0, {"degree": degree, "digits": 0, "peak_carries": 0}

    # Q_r=P^r for r=0,...,p-1.  These are all the local factors needed by
    # P(x)^K = product_j Q_{k_j}(x^(p^j)), where k_j is digit j of K.
    local_powers: list[Poly] = [{0: 1}]
    for _ in range(1, p):
        local_powers.append(_mul(local_powers[-1], P, p))

    digit_count = _digit_length(degree * K, p)
    carries: Poly = {0: 1}
    peak_carries = 1
    transition_attempts = 0
    current_K, current_N = K, N
    for _ in range(digit_count):
        k_digit = current_K % p
        n_digit = current_N % p
        q = local_powers[k_digit]
        following: Poly = {}
        for carry, prefix_weight in carries.items():
            for exponent, local_weight in q.items():
                transition_attempts += 1
                remainder = carry + exponent - n_digit
                if remainder < 0 or remainder % p:
                    continue
                next_carry = remainder // p
                # The invariant 0 <= carry <= degree implies the same bound
                # after this transition because exponent <= (p-1)*degree.
                if next_carry > degree:
                    raise ArithmeticError("carry bound violated")
                value = (following.get(next_carry, 0) + prefix_weight * local_weight) % p
                if value:
                    following[next_carry] = value
                else:
                    following.pop(next_carry, None)
        carries = following
        peak_carries = max(peak_carries, len(carries))
        current_K //= p
        current_N //= p
        if not carries:
            break

    return carries.get(0, 0), {
        "degree": degree,
        "digits": digit_count,
        "peak_carries": peak_carries,
        "local_support_total": sum(len(q) for q in local_powers),
        "transition_attempts": transition_attempts,
    }

