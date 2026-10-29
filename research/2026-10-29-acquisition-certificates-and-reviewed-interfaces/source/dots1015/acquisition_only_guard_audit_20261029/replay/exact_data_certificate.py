"""Exact data-only threshold for the acquisition-only protocol.

This evaluates supplied counters, not their provenance or a physical operation.
Only genuinely generated, verified counters satisfy the governing theorem.
"""
from fractions import Fraction as F
from math import isqrt, comb


def root_upper(value, bits=32):
    value = F(value)
    if value < 0 or not isinstance(bits, int) or bits < 0:
        raise ValueError("invalid upper-root input")
    scale = 1 << bits
    numerator = value.numerator * scale * scale
    denominator = value.denominator
    result = isqrt(numerator // denominator)
    if result * result * denominator < numerator:
        result += 1
    return F(result, scale)


def empirical_score(edges, probe_count, p):
    total = F(3 * len(edges) * probe_count, 4) / p
    for edge in edges:
        quaternion = tuple(F(x) for x in edge["quaternion"])
        if len(quaternion) != 4 or sum(x*x for x in quaternion) != 1:
            raise ValueError("candidate is not an exact rational unit quaternion")
        seen = set()
        for exponent, coefficient in edge["coefficients"]:
            exponent = tuple(exponent)
            if len(exponent) != 4 or any(type(x) is not int or x < 0 for x in exponent) or sum(exponent) != 4:
                raise ValueError("malformed degree-four monomial")
            if exponent in seen:
                raise ValueError("duplicate monomial")
            seen.add(exponent)
            monomial = F(1)
            for q, power in zip(quaternion, exponent):
                monomial *= q ** power
            total += F(coefficient) * monomial / 2
    return total


def certify(record):
    T = record["horizon"]
    J = record["service_target"]
    faults = record["correction_radius"]
    services = record["services_completed"]
    probes = record["probe_count"]
    active = record["active_calls"]
    for count in (T, J, faults, services, probes, active):
        if type(count) is not int or count < 0:
            raise ValueError("counts must be nonnegative integers")
    if T < 1 or J < 1 or services > J or active != services + probes or active > T:
        raise ValueError("inconsistent call counts")
    p = F(record["probe_probability"])
    s = 1 - p
    R = F(record["perturbation_amplitude"])
    M = record["midpoint_bank_size"]
    alpha = F(record["raw_transfer_factor"])
    if not 0 < p < 1 or R <= 0 or type(M) is not int or M < 1 or M & (M-1) or alpha <= 0:
        raise ValueError("invalid public parameters")
    exponents = record.get("failure_budget_exponents", [20, 20, 20])
    if len(exponents) != 3 or any(type(k) is not int or k < 1 for k in exponents):
        raise ValueError("invalid dyadic failure budgets")
    ke, km, kf = exponents
    edges = record["edges"]
    m = len(edges)
    if m < 1:
        raise ValueError("no star edges")
    n = m + 1
    if n % 2:
        raise ValueError("full singlet transfer requires an even spin count")
    catalan = comb(n, n//2) // (n//2 + 1)
    if alpha < F(2**n, catalan):
        raise ValueError("understated raw transfer factor")
    d, L = 35, 720
    B = (T-1) * F(L, p) + d*R
    Eobs, Vobs = F(0), F(0)
    for edge in edges:
        gap = F(edge["reported_gap_sum"])
        squared = F(edge["squared_feedback_sum"])
        if gap < 0 or gap > active*B or squared < 0 or squared > probes*F(L, p)**2:
            raise ValueError("counters exceed declared deterministic bounds")
        if sum(abs(F(c)) for _, c in edge["coefficients"]) > probes * F(L, p):
            raise ValueError("feedback exceeds deterministic coefficient bound")
        Eobs += gap
        Vobs += squared
    empirical = empirical_score(edges, probes, p)
    predictable_gap_upper = 2*Eobs + 2*m*B*ke
    bound = (F(m*d, 4)*R + Vobs/(4*R)
             + L*root_upper(F(m*T, R)*predictable_gap_upper + F(m*m*d*T*T, M))
             + m*(1 + F(45, 2*p))*root_upper(2*T*km))
    selected_loss_upper = max(F(0), empirical + bound)
    bad_count_upper = s*alpha*selected_loss_upper + root_upper(F(T*kf, 2))
    ready = (record.get("verified_code") is True
             and record.get("resource_abort") is False
             and services == J)
    accept = ready and bad_count_upper <= faults
    return {
        "accept": accept,
        "empirical_score": str(empirical),
        "reported_gap_sum": str(Eobs),
        "squared_feedback_sum": str(Vobs),
        "predictable_gap_upper": str(predictable_gap_upper),
        "selected_star_loss_upper": str(selected_loss_upper),
        "virtual_bad_count_upper": str(bad_count_upper),
        "accepted_half_diamond_budget": str(sum(F(1, 2**k) for k in exponents)),
        "scope": "Mathematical decision on supplied valid counters. No provenance, physical clock, gate accuracy, or positive-yield claim."
    }
