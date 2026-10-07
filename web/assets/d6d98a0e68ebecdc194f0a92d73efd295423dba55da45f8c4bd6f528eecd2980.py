"""Exact building blocks for BIT_COMPILER.md (not a complete sampler).

Uses only Python's standard library. Parameters may be extremely conservative.
These routines do not establish the statistical theorem or certify sampler.py.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import isqrt
from typing import Sequence

Matrix = list[list[F]]

def matrix(a: Sequence[Sequence[int | F]]) -> Matrix:
    """Copy a square rational matrix, checking its shape."""
    out = [[F(x) for x in row] for row in a]
    n = len(out)
    if not n or any(len(row) != n for row in out):
        raise ValueError("A nonempty square matrix is required")
    return out

def ceil_log2(x: int | F) -> int:
    """Smallest integer k such that x <= 2**k; no floating logarithm."""
    x = F(x)
    if x <= 0:
        raise ValueError("Logarithm argument must be positive")
    k = x.numerator.bit_length() - x.denominator.bit_length()
    power = F(1 << k) if k >= 0 else F(1, 1 << (-k))
    return k + int(x > power)

def determinant(a: Sequence[Sequence[int | F]]) -> F:
    """Exact determinant by rational Gaussian elimination with row pivoting."""
    a = matrix(a)
    n = len(a)
    out = F(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            out = -out
        p = a[j][j]
        out *= p
        for i in range(j + 1, n):
            c = a[i][j] / p
            for k in range(j + 1, n):
                a[i][k] -= c * a[j][k]
            a[i][j] = F(0)
    return out

def is_psd(a: Sequence[Sequence[int | F]]) -> bool:
    """Exact PSD test for a symmetric rational matrix using Schur elimination."""
    a = matrix(a)
    n = len(a)
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        raise ValueError("PSD test requires a symmetric matrix")
    for j in range(n):
        p = a[j][j]
        if p < 0:
            return False
        if p == 0:
            if any(a[j][k] for k in range(j + 1, n)):
                return False
            continue
        for i in range(j + 1, n):
            for k in range(i, n):
                v = a[i][k] - a[i][j] * a[j][k] / p
                a[i][k] = a[k][i] = v
    return True

def physical_round(a: Sequence[Sequence[int | F]], bits: int) -> Matrix:
    """Round a symmetric covariance, adding PSD noise of norm <= 2*d*2^-bits.

If the input covariance is physical, the output is physical. No attempt to
validate the quantum uncertainty relation is made inside this function.
"""
    if not isinstance(bits, int) or bits < 1:
        raise ValueError("bits must be a positive integer")
    a = matrix(a)
    n = len(a)
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        raise ValueError("Rounding requires a symmetric matrix")
    scale = 1 << bits
    out = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            x = a[i][j] * scale + F(1, 2)
            out[i][j] = out[j][i] = F(x.numerator // x.denominator, scale)
        out[i][i] += F(n, scale)
    return out

def survival_bracket(k: Sequence[Sequence[int | F]], v: int | F,
                     bits: int) -> tuple[F, F]:
    """Enclose det[I+(1-v)K]^(-1/2) in a dyadic interval of width 2^-bits."""
    if not isinstance(bits, int) or bits < 1:
        raise ValueError("bits must be a positive integer")
    v = F(v)
    if not 0 <= v <= 1:
        raise ValueError("v must lie in [0,1]")
    k = matrix(k)
    n = len(k)
    a = [[F(i == j) + (1-v)*k[i][j] for j in range(n)] for i in range(n)]
    det = determinant(a)
    if det <= 0:
        raise ValueError("Survival determinant must be positive")
    scale = 1 << bits
    z = isqrt((det.denominator * scale * scale) // det.numerator)
    return F(z, scale), F(z+1, scale)

def compiler_parameters(m: int, energy: int | F, epsilon: int | F) -> dict:
    """Explicit proof-level schedule; computes parameters, not a sampled record."""
    energy, epsilon = F(energy), F(epsilon)
    if not isinstance(m, int) or m < 1 or energy < 0 or not 0 < epsilon < F(1, 2):
        raise ValueError("Require M>=1, energy>=0, and 0<epsilon<1/2")
    d = 2*m
    cap = F(100)*(energy+1)/epsilon
    j = -(-cap.numerator // cap.denominator)
    k = ceil_log2(F(100*j*(m+1))/epsilon)
    vmin = F(1, 1 << k)
    gamma = min(vmin/100, epsilon/F(100*m*j*(k+1)))
    growth = F((1 << (4*d+100)) * (d+1)**10) / (gamma**10 * vmin**4)
    delta = epsilon/(10000*j*growth**2)
    lg = ceil_log2(growth)
    # This upper choice implies Eq. B8 without constructing growth**(J+2).
    b = ceil_log2(1/delta) + (j+2)*(2+lg) + ceil_log2(4*d)
    return {"m": m, "quadrature_dimension": d, "energy": str(energy),
            "epsilon": str(epsilon), "count_cap": j, "k": k,
            "v_min": str(vmin), "gamma": str(gamma),
            "ceil_log2_L": lg, "precision_bits": b,
            "bisection_iteration_cap": b+ceil_log2(F(m+1)/vmin)+8,
            "status": "parameters only; full theorem-schedule engine not executed"}
