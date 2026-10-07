"""Positive rational quadratic gates, exact LC closure and layer planner.

The generator bound is algebraic and independent of the counting preprint.
The optional count remains conditional on its Lemma 5.5. No source files or
initial evidence are mutated; the original local sampler is reused verbatim.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from xxz_local_chain import LocalFactor, TraceInstance, compile_trace


def quadratic_edge_table(s, alpha, gamma):
    s, alpha, gamma = F(s), F(alpha), F(gamma)
    if s < 0 or alpha < abs(gamma):
        raise ValueError("outside easy-plane cone")
    lam0, diag, off = 3 * alpha + gamma, 3 * alpha - gamma, 2 * alpha
    a = 1 + s * lam0 + s * s * lam0 * lam0 / 2
    b = 1 + s * diag + s * s * (diag * diag + off * off) / 2
    c = s * off + s * s * diag * off
    assert a + b >= c and b + c >= a and a + c >= b
    return {mask: value for mask, value in ((3, a), (12, a), (6, b), (9, b), (5, c), (10, c))
            if value > 0}


def quadratic_field_table(s, b, c):
    s, b, c = F(s), F(b), F(c)
    if s < 0 or b < 0:
        raise ValueError("nonnegative X field required")
    r = b + abs(c)
    upper, lower = r + c, r - c
    v = 1 + s * upper + s * s * (upper * upper + b * b) / 2
    u = 1 + s * lower + s * s * (lower * lower + b * b) / 2
    d = s * b + s * s * r * b
    assert u > 0 and v > 0 and u * v - d * d >= 1
    return {mask: value for mask, value in ((3, d), (12, d), (5, u / 2), (9, u / 2),
                                           (6, v / 2), (10, v / 2)) if value > 0}


def compile_quadratic_trace(qubits, gates):
    original = compile_trace(qubits, gates)
    factors = []
    for old, (kind, _, s, a, g) in zip(original.factors, gates):
        table = quadratic_edge_table(s, a, g) if kind == "edge" else quadratic_field_table(s, a, g)
        factors.append(LocalFactor(old.coordinates, table))
    return TraceInstance(original.n, factors, original.groups, original.inactive_qubits)


def ceil_sqrt_fraction(value):
    value = F(value)
    if value < 0:
        raise ValueError("nonnegative radicand")
    upper_integer = (value.numerator + value.denominator - 1) // value.denominator
    result = isqrt(upper_integer)
    if result * result < upper_integer:
        result += 1
    assert result * result >= value
    return result


def quadratic_plan(qubits, edges, fields, beta, error):
    beta, error = F(beta), F(error)
    if beta < 0 or not 0 < error <= 1:
        raise ValueError("invalid temperature/error")
    if any(F(alpha) < abs(F(gamma)) for _, _, alpha, gamma in edges):
        raise ValueError("outside easy-plane cone")
    if any(F(b) < 0 for _, b, _ in fields):
        raise ValueError("nonnegative X required")
    C = 3 * sum((F(a) for _, _, a, _ in edges), F(0)) + sum(
        (F(b) + abs(F(c)) for _, b, c in fields), F(0))
    tau = 2 * beta * C
    m = max(1, (4 * tau.numerator + tau.denominator - 1) // tau.denominator,
            ceil_sqrt_fraction(4 * tau ** 3 / error))
    p = len(edges) + len(fields)
    return {"qubits": qubits, "C": C, "tau": tau, "m": m, "s": beta / (2 * m),
            "local_terms": p, "gates": 2 * m * p, "ground_size": 8 * m * p,
            "log_generator_error_bound": tau ** 3 / (m * m),
            "complement_symmetric": all(F(c) == 0 for _, _, c in fields)}


def planned_quadratic_circuit(qubits, edges, fields, beta, error, *, max_gates=1000):
    plan = quadratic_plan(qubits, edges, fields, beta, error)
    if plan["gates"] > max_gates:
        raise ValueError(f"explicit circuit admission: {plan['gates']} gates exceeds {max_gates}")
    s = plan["s"]
    forward = ([("edge", (u, v), s, F(a), F(g)) for u, v, a, g in edges] +
               [("field", (v,), s, F(b), F(c)) for v, b, c in fields])
    layer = forward + list(reversed(forward))
    gates = layer * plan["m"]
    return compile_quadratic_trace(qubits, gates), gates, plan
