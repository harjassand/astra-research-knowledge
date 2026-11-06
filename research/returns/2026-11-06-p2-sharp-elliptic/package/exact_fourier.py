#!/usr/bin/env python3
"""Exact rational Fourier demonstration and independently checkable residual.

No numerical quadrature or PDE solver is used.  The analytic L^4 certificate
uses the sharp Hodge-reflection theorem stated and proved in RESEARCH_REPORT.txt.
This is an implementation for encoded finite Fourier data, not a solver for
unencoded measurable functions. Python 3.11+ standard library only.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import json
import time
import resource


@dataclass(frozen=True)
class C:
    re: F = F(0)
    im: F = F(0)

    def __add__(self, other):
        if not isinstance(other, C):
            other = C(F(other))
        return C(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return C(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if not isinstance(other, C):
            other = C(F(other))
        return C(self.re * other.re - self.im * other.im,
                 self.re * other.im + self.im * other.re)

    __rmul__ = __mul__

    def conj(self):
        return C(self.re, -self.im)

    def abs_upper(self):
        return abs(self.re) + abs(self.im)

    def encoded(self):
        return [str(self.re), str(self.im)]


ZERO = C()
N = 2
K = F(3, 10)
EPS = F(1, 256)
CP = F(3)
RHO = K * CP
GRAD_FACTOR = (1 + CP) * CP / (2 * (1 - RHO))
ZMODE = (0,) * N


def clean(a):
    return {m: tuple(v) for m, v in a.items() if any(x != ZERO for x in v)}


def add(a, b, factor=F(1)):
    out = {m: list(v) for m, v in a.items()}
    for m, v in b.items():
        w = out.setdefault(m, [ZERO] * len(v))
        for j, value in enumerate(v):
            w[j] = w[j] + factor * value
    return clean(out)


def scale(a, factor):
    return clean({m: tuple(factor * x for x in v) for m, v in a.items()})


def P(a):
    out = {}
    for m, v in a.items():
        q = sum(i * i for i in m)
        if q:
            dot = sum((i * z for i, z in zip(m, v)), ZERO)
            out[m] = tuple(F(i, q) * dot for i in m)
    return clean(out)


def H(a):
    return add(scale(P(a), F(2)), a, F(-1))


def matvec(a, b):
    out = {}
    for m, mat in a.items():
        for ell, v in b.items():
            mode = tuple(x + y for x, y in zip(m, ell))
            w = out.setdefault(mode, [ZERO] * N)
            for i in range(N):
                for j in range(N):
                    w[i] = w[i] + mat[i * N + j] * v[j]
    return clean(out)


def matmat(a, b):
    out = {}
    for m, left in a.items():
        for ell, right in b.items():
            mode = tuple(x + y for x, y in zip(m, ell))
            w = out.setdefault(mode, [ZERO] * (N * N))
            for i in range(N):
                for j in range(N):
                    for k in range(N):
                        w[i * N + j] = w[i * N + j] + left[i*N+k] * right[k*N+j]
    return clean(out)


def l1_bound(a):
    """Bounds pointwise Euclidean norm, and therefore every finite L^p norm."""
    return sum((x.abs_upper() for v in a.values() for x in v), F(0))


def real_field(a):
    for m, v in a.items():
        other = a.get(tuple(-x for x in m), (ZERO,) * len(v))
        assert other == tuple(x.conj() for x in v)


def divergence_zero(a):
    for m, v in a.items():
        assert sum((i * z for i, z in zip(m, v)), ZERO) == ZERO


def curl_zero(a):
    for m, v in a.items():
        for i in range(N):
            for j in range(N):
                assert m[i] * v[j] == m[j] * v[i]


def max_bits(a):
    return max((max(abs(t.numerator).bit_length(), t.denominator.bit_length())
                for v in a.values() for x in v for t in (x.re, x.im)), default=0)


def encode(a):
    return [{"mode": list(m), "coefficients": [x.encoded() for x in v]}
            for m, v in sorted(a.items())]


def main():
    started = time.perf_counter()
    identity = {ZMODE: (C(F(1)), ZERO, ZERO, C(F(1)))}
    M = {
        (1, 0): (C(K/2), C(F(0), -K/2), C(F(0), -K/2), C(-K/2)),
        (-1, 0): (C(K/2), C(F(0), K/2), C(F(0), K/2), C(-K/2)),
    }
    h = {
        (0, 1): (C(F(1, 2)), ZERO),
        (0, -1): (C(F(1, 2)), ZERO),
        (1, 1): (ZERO, C(F(0), F(-1, 2))),
        (-1, -1): (ZERO, C(F(0), F(1, 2))),
    }
    # A=(I-M)(I+M)^(-1), F=(I+M)^(-1)h.
    inv_plus = scale(add(identity, M, F(-1)), 1/(1-K*K))
    A = scale(add(scale(identity, 1+K*K), M, F(-2)), 1/(1-K*K))
    forcing = matvec(inv_plus, h)
    assert matmat(M, M) == scale(identity, K*K)
    assert matmat(add(identity, M), inv_plus) == identity
    assert matmat(A, add(identity, M)) == add(identity, M, F(-1))
    for field in (M, A, h, forcing):
        real_field(field)

    # A priori cap uses rational arithmetic alone.
    priori = GRAD_FACTOR * l1_bound(h)
    cap = 0
    while priori > EPS:
        priori *= RHO
        cap += 1

    f = {}
    history = []
    maximum_working_bits = 0
    for iteration in range(cap+1):
        residual = add(add(H(f), matvec(M, f), F(-1)), h, F(-1))
        residual_bound = l1_bound(residual)
        certified_error = GRAD_FACTOR * residual_bound
        maximum_working_bits = max(maximum_working_bits, max_bits(f), max_bits(residual))
        history.append({"iteration": iteration, "modes": len(f),
                        "residual_bound": str(residual_bound),
                        "gradient_error_bound": str(certified_error),
                        "gradient_error_bound_float": float(certified_error),
                        "max_coefficient_bits": max_bits(f)})
        if certified_error <= EPS:
            stopping_rule = "exact Fourier residual"
            break
        if iteration == cap:
            # In general the Fourier l1 residual need not decay. The analytic
            # contraction bound is the guaranteed stopping certificate.
            certified_error = priori
            stopping_rule = "a priori contraction bound"
            break
        f = H(add(matvec(M, f), h))

    e = P(f)
    j = add(f, e, F(-1))
    physical_residual = add(add(matvec(A, e), j, F(-1)), forcing, F(-1))
    assert physical_residual == matvec(inv_plus, residual)
    assert H(H(f)) == f
    assert P(e) == e
    curl_zero(e)
    divergence_zero(j)
    assert ZMODE not in e
    for field in (f, e, j, residual, physical_residual):
        real_field(field)
    assert certified_error <= EPS

    data = {
        "format": "Exact rational Fourier coefficients; basis exp(2*pi*i*m.x)",
        "coefficient_encoding": "Each complex coefficient is [real_fraction, imaginary_fraction]",
        "dimension": N, "p": "4", "k": str(K), "rho": str(RHO),
        "requested_gradient_L4_error": str(EPS),
        "M": encode(M), "h": encode(h), "A": encode(A), "forcing": encode(forcing),
        "f": encode(f), "gradient": encode(e), "divergence_free_flux": encode(j),
        "reflection_residual": encode(residual), "physical_residual": encode(physical_residual),
    }
    input_data = {key: data[key] for key in
                  ("format", "coefficient_encoding", "dimension", "p", "k",
                   "requested_gradient_L4_error", "M", "h")}
    input_data["coefficient_bound_certificate"] = "M is real symmetric and M*M=k*k*I; check by exact Fourier convolution"
    input_text = json.dumps(input_data, indent=2)+"\n"
    summary = {
        "iterations": iteration, "a_priori_iteration_cap": cap,
        "stopping_rule": stopping_rule,
        "gradient_modes": len(e), "f_modes": len(f),
        "residual_modes": len(residual),
        "exact_gradient_L4_error_bound": str(certified_error),
        "gradient_L4_error_bound_float": float(certified_error),
        "target": str(EPS), "coefficient_eigenvalues": ["7/13", "13/7"],
        "sharp_p_range": ["13/10", "13/3"],
        "max_output_fraction_bits": max(max_bits(e), max_bits(j)),
        "max_iterate_and_residual_fraction_bits": maximum_working_bits,
        "all_exact_algebraic_checks_passed": True,
        "input_json_utf8_bytes": len(input_text.encode("utf-8")),
        "analytic_certificate_dependency": "The sharp real Hodge-reflection theorem in RESEARCH_REPORT.txt",
        "wall_seconds": time.perf_counter()-started,
        "process_maxrss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "history": history,
    }
    root = Path(__file__).resolve().parent
    (root / "INPUT.json").write_text(input_text)
    (root / "FOURIER_SOLUTION.json").write_text(json.dumps(data, indent=2)+"\n")
    (root / "AUDIT_RESULTS.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps({k: v for k,v in summary.items() if k != "history"}, indent=2))


if __name__ == "__main__":
    main()
