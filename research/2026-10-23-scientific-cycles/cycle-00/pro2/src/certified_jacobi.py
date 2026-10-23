"""Exact-input Jacobi node and weight certification, using Python's standard library.

The matrix entries are integer diagonal/off-diagonal coefficients divided by one
positive power-of-two denominator. Off-diagonal entries must be strictly positive.
No numerical eigenvalues/eigenvectors are used by this module.

Roots are isolated in the *scaled integer matrix* coordinate with integer Sturm
recurrences. Spectral weights for e_1 are enclosed using outward-rounded Decimal
interval recurrences for the normalized orthogonal polynomials. `cms_bounds`
implements conservative Chebyshev--Markov--Stieltjes lag/lead envelopes for any
positive probability measure having this leading Jacobi matrix. The small
matrix's Gershgorin interval is used only for root isolation; it is not asserted
to contain the support of that underlying measure.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction
import math
import operator
import time
from typing import Any


DEFAULT_DENOMINATOR = 1 << 32
SCHEMA = "astra-certified-integer-jacobi-v1"


def _integer(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name}: bool is not an integer coefficient")
    if isinstance(value, str):
        try:
            result = int(value, 10)
        except ValueError as exc:
            raise ValueError(f"{name}: expected a base-10 integer") from exc
        if str(result) != value.strip() and not (value.strip().startswith("+") and str(result) == value.strip()[1:]):
            raise ValueError(f"{name}: noncanonical integer")
        return result
    try:
        return operator.index(value)
    except TypeError as exc:
        raise ValueError(f"{name}: exact integer required") from exc


def _validate_inputs(diagonal_int, offdiagonal_int, denominator):
    a = tuple(_integer(x, "diagonal") for x in diagonal_int)
    b = tuple(_integer(x, "offdiagonal") for x in offdiagonal_int)
    den = _integer(denominator, "denominator")
    if not a or len(b) != len(a)-1:
        raise ValueError("Need n>=1 diagonal entries and n-1 off-diagonal entries")
    if any(x <= 0 for x in b):
        raise ValueError("Irreducible Jacobi input requires positive off-diagonal entries")
    if den <= 0 or den & (den-1):
        raise ValueError("The common denominator must be a positive power of two")
    return a, b, den


def _fraction(value: Any) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError("Finite threshold required")
        return Fraction(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("Finite threshold required")
        # A supplied float means exactly that binary rational, not a decimal intent.
        return Fraction.from_float(value)
    return Fraction(value)


def _fraction_json(value: Fraction) -> dict[str, str]:
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def _read_fraction(value: dict[str, str]) -> Fraction:
    n = _integer(value["numerator"], "fraction numerator")
    d = _integer(value["denominator"], "fraction denominator")
    if d <= 0:
        raise ValueError("Positive fraction denominator required")
    return Fraction(n, d)


def sturm_count_scaled(diagonal_int, offdiagonal_int, x) -> tuple[int, bool]:
    """Return (# eigenvalues strictly below x, full determinant is zero).

    x is in the integer coefficient coordinate. With x=m/q, the recurrence
    r_j=q**j det(J_j-x I) uses integers only. Zero sequence values are omitted
    from sign-variation counting. Irreducibility prevents adjacent zeros; strict
    interlacing makes a terminal zero yield the strict, not non-strict, count.
    """
    a = diagonal_int
    b = offdiagonal_int
    if not a or len(b) != len(a)-1 or any(v <= 0 for v in b):
        raise ValueError("Invalid irreducible Jacobi coefficients")
    x = _fraction(x)
    m, q = x.numerator, x.denominator
    q2 = q*q
    previous = 1
    current = a[0]*q-m
    last_sign = 1
    variations = 0
    if current:
        sign = 1 if current > 0 else -1
        variations += sign != last_sign
        last_sign = sign
    for j in range(1, len(a)):
        following = (a[j]*q-m)*current - b[j-1]*b[j-1]*q2*previous
        previous, current = current, following
        if current:
            sign = 1 if current > 0 else -1
            variations += sign != last_sign
            last_sign = sign
    return int(variations), current == 0


class _Counter:
    def __init__(self, a, b):
        self.a, self.b = a, b
        self.cache: dict[Fraction, tuple[int, bool]] = {}
        self.hits = 0

    def __call__(self, x):
        x = _fraction(x)
        if x in self.cache:
            self.hits += 1
            return self.cache[x]
        out = sturm_count_scaled(self.a, self.b, x)
        self.cache[x] = out
        return out


def _gershgorin(a, b) -> tuple[int, int]:
    lows, highs = [], []
    for j, aj in enumerate(a):
        radius = (b[j-1] if j else 0)+(b[j] if j < len(b) else 0)
        lows.append(aj-radius)
        highs.append(aj+radius)
    # Enlarge the Gershgorin enclosure to symmetric dyadic integer endpoints.
    # Its power-of-two width makes all dyadic roots reachable by bisection.
    radius = max(abs(min(lows)-1), abs(max(highs)+1))
    power = 1 << radius.bit_length()
    return -power, power


def _isolate_roots(a, b, fractional_bits, max_fractional_bits, counter):
    lower0, upper0 = _gershgorin(a, b)
    if counter(Fraction(lower0))[0] != 0 or counter(Fraction(upper0))[0] != len(a):
        raise ArithmeticError("Initial exact Gershgorin/Sturm check failed")
    target_width = Fraction(1, 1 << fractional_bits)
    max_steps = max_fractional_bits+(upper0-lower0).bit_length()+4
    roots = []
    for index in range(len(a)):
        lo, hi = Fraction(lower0), Fraction(upper0)
        lc, hc = 0, len(a)
        steps = 0
        exact = False
        while True:
            if hi-lo <= target_width and lc == index and hc == index+1:
                break
            if steps >= max_steps:
                raise ArithmeticError(f"Root {index+1} was not isolated within the refinement cap")
            mid = (lo+hi)/2
            count, is_root = counter(mid)
            steps += 1
            if is_root and count == index:
                lo = hi = mid
                lc = hc = index
                exact = True
                break
            if count <= index:
                lo, lc = mid, count
            else:
                hi, hc = mid, count
        roots.append({"lo": lo, "hi": hi, "lower_count": lc,
                      "upper_count": hc, "exact": exact, "steps": steps})
    for left, right in zip(roots, roots[1:]):
        if left["hi"] > right["lo"]:
            raise ArithmeticError("Ordered isolating intervals overlap")
    return roots, (lower0, upper0)


@dataclass(frozen=True)
class _Interval:
    lo: Decimal
    hi: Decimal


class _IntervalArithmetic:
    """Small directed-rounding interval engine; all endpoints are Decimal."""
    def __init__(self, precision):
        self.precision = int(precision)
        if self.precision < 32:
            raise ValueError("At least 32 Decimal significant digits are required")

    def _op(self, rounding, operation):
        with localcontext() as context:
            context.prec = self.precision
            context.rounding = rounding
            context.Emax = 999999999
            context.Emin = -999999999
            return operation()

    def rational(self, x: Fraction) -> _Interval:
        n, d = Decimal(x.numerator), Decimal(x.denominator)
        return _Interval(self._op(ROUND_FLOOR, lambda: n/d),
                         self._op(ROUND_CEILING, lambda: n/d))

    def enclosure(self, lo: Fraction, hi: Fraction) -> _Interval:
        return _Interval(self.rational(lo).lo, self.rational(hi).hi)

    def integer(self, value: int) -> _Interval:
        x = Decimal(value)
        return _Interval(x, x)

    def add(self, a, b):
        return _Interval(self._op(ROUND_FLOOR, lambda: a.lo+b.lo),
                         self._op(ROUND_CEILING, lambda: a.hi+b.hi))

    def sub(self, a, b):
        return _Interval(self._op(ROUND_FLOOR, lambda: a.lo-b.hi),
                         self._op(ROUND_CEILING, lambda: a.hi-b.lo))

    def mul(self, a, b):
        pairs = [(a.lo, b.lo), (a.lo, b.hi), (a.hi, b.lo), (a.hi, b.hi)]
        lows = [self._op(ROUND_FLOOR, lambda x=x, y=y: x*y) for x, y in pairs]
        highs = [self._op(ROUND_CEILING, lambda x=x, y=y: x*y) for x, y in pairs]
        return _Interval(min(lows), max(highs))

    def divide_positive_integer(self, a, value):
        if value <= 0:
            raise ValueError("Positive recurrence divisor required")
        d = Decimal(value)
        return _Interval(self._op(ROUND_FLOOR, lambda: a.lo/d),
                         self._op(ROUND_CEILING, lambda: a.hi/d))

    def square(self, a):
        if a.lo <= 0 <= a.hi:
            lo = Decimal(0)
        else:
            # Decimal.__abs__ applies the ambient context and can round inward.
            # copy_abs is exact, independent of the ambient precision.
            endpoint = min(a.lo.copy_abs(), a.hi.copy_abs())
            lo = self._op(ROUND_FLOOR, lambda: endpoint*endpoint)
        endpoint = max(a.lo.copy_abs(), a.hi.copy_abs())
        hi = self._op(ROUND_CEILING, lambda: endpoint*endpoint)
        return _Interval(lo, hi)

    def reciprocal_positive(self, a):
        if a.lo <= 0:
            raise ArithmeticError("Positive interval required for reciprocal")
        return _Interval(self._op(ROUND_FLOOR, lambda: Decimal(1)/a.hi),
                         self._op(ROUND_CEILING, lambda: Decimal(1)/a.lo))


def _weight_interval(a, b, lo, hi, arithmetic):
    ar = arithmetic
    x = ar.enclosure(lo, hi)
    previous = ar.integer(1)
    squared_sum = ar.integer(1)
    if len(a) > 1:
        current = ar.divide_positive_integer(ar.sub(x, ar.integer(a[0])), b[0])
        squared_sum = ar.add(squared_sum, ar.square(current))
        for j in range(1, len(a)-1):
            numerator = ar.sub(ar.mul(ar.sub(x, ar.integer(a[j])), current),
                               ar.mul(ar.integer(b[j-1]), previous))
            following = ar.divide_positive_integer(numerator, b[j])
            squared_sum = ar.add(squared_sum, ar.square(following))
            previous, current = current, following
    out = ar.reciprocal_positive(squared_sum)
    return _Interval(max(Decimal(0), out.lo), min(Decimal(1), out.hi))


def certify_jacobi(diagonal_int, offdiagonal_int, denominator=DEFAULT_DENOMINATOR,
                   *, root_fractional_bits=140, decimal_precision=100,
                   max_root_fractional_bits=4096, max_decimal_precision=512,
                   target_weight_width="1e-28"):
    """Return JSON-safe exact root brackets and rigorous Decimal weight intervals.

    Root widths refer to the scaled integer matrix, before division by D.
    A target weight width requests bounded adaptive refinement; use None to
    accept the first rigorous enclosure regardless of its width. All attempts
    are charged in the returned timing/counter fields. The function raises on
    unachieved isolation/tightness instead of silently returning a success flag.
    """
    wall_start, cpu_start = time.perf_counter(), time.process_time()
    a, b, den = _validate_inputs(diagonal_int, offdiagonal_int, denominator)
    bits, precision = int(root_fractional_bits), int(decimal_precision)
    if bits < 0 or max_root_fractional_bits < bits:
        raise ValueError("Invalid root refinement limits")
    if max_decimal_precision < precision:
        raise ValueError("Invalid Decimal refinement limits")
    target = None if target_weight_width is None else Decimal(str(target_weight_width))
    if target is not None and (not target.is_finite() or target <= 0):
        raise ValueError("Positive finite weight-width target required")
    counter = _Counter(a, b)
    attempts = []
    while True:
        attempt_start = time.perf_counter()
        roots, outer = _isolate_roots(a, b, bits, max_root_fractional_bits, counter)
        ar = _IntervalArithmetic(precision)
        weights = [_weight_interval(a, b, r["lo"], r["hi"], ar) for r in roots]
        maximum_width = max(ar._op(ROUND_CEILING, lambda w=w: w.hi-w.lo) for w in weights)
        attempts.append({"root_fractional_bits": bits, "decimal_precision": precision,
                         "maximum_weight_interval_width": str(maximum_width),
                         "wall_seconds": time.perf_counter()-attempt_start})
        if target is None or maximum_width <= target:
            break
        new_bits, new_precision = min(max_root_fractional_bits, bits+32), min(max_decimal_precision, precision+32)
        if new_bits == bits and new_precision == precision:
            raise ArithmeticError("Weight interval target not reached within refinement caps")
        bits, precision = new_bits, new_precision
    total = ar.integer(0)
    for weight in weights:
        total = ar.add(total, weight)
    if not (total.lo <= 1 <= total.hi):
        raise ArithmeticError("Certified weight sum does not enclose one")
    nodes = []
    for index, (root, weight) in enumerate(zip(roots, weights)):
        nodes.append({"index": index+1,
                      "scaled_lower": _fraction_json(root["lo"]),
                      "scaled_upper": _fraction_json(root["hi"]),
                      "lower": _fraction_json(root["lo"]/den),
                      "upper": _fraction_json(root["hi"]/den),
                      "exact_dyadic_root": root["exact"],
                      "lower_strict_sturm_count": root["lower_count"],
                      "upper_strict_sturm_count": root["upper_count"],
                      "bisections": root["steps"],
                      "weight_lower": str(weight.lo), "weight_upper": str(weight.hi)})
    return {"schema": SCHEMA, "dimension": len(a),
            "diagonal_int": [str(x) for x in a],
            "offdiagonal_int": [str(x) for x in b], "denominator": str(den),
            "coordinate_convention": "scaled roots are eigenvalues of denominator * J",
            "root_fractional_bits": bits, "decimal_precision": precision,
            "gershgorin_strict_scaled": {"lower": str(outer[0]), "upper": str(outer[1])},
            "nodes": nodes,
            "weight_sum_interval": {"lower": str(total.lo), "upper": str(total.hi)},
            "maximum_weight_interval_width": str(maximum_width),
            "order_check": "nonoverlapping ordered brackets; exact Sturm index for every root",
            "rounding": "Decimal ROUND_FLOOR for lower endpoints; ROUND_CEILING for upper endpoints",
            "resource": {"wall_seconds": time.perf_counter()-wall_start,
                         "cpu_seconds": time.process_time()-cpu_start,
                         "sturm_unique_evaluations": len(counter.cache),
                         "sturm_cache_hits": counter.hits, "attempts": attempts}}


def verify_certificate(certificate, diagonal_int, offdiagonal_int,
                       denominator=DEFAULT_DENOMINATOR, *, minimum_root_fractional_bits=140):
    """Recheck exact root indices and directed weights against separate input.

    Expected coefficients are mandatory: internal consistency alone is not
    input identity. This function uses no numerical eigensolver and no assert.
    """
    wall_start, cpu_start = time.perf_counter(), time.process_time()
    a, b, den = _validate_inputs(diagonal_int, offdiagonal_int, denominator)
    cert = certificate
    if cert.get("schema") != SCHEMA or cert.get("dimension") != len(a):
        raise ValueError("Certificate schema/dimension mismatch")
    if cert.get("diagonal_int") != [str(x) for x in a] or cert.get("offdiagonal_int") != [str(x) for x in b] or cert.get("denominator") != str(den):
        raise ValueError("Certificate is not bound to the supplied expected coefficients")
    bits = _integer(cert["root_fractional_bits"], "root bits")
    if bits < minimum_root_fractional_bits:
        raise ValueError("Root precision below the receiving contract")
    precision = _integer(cert["decimal_precision"], "Decimal precision")
    ar = _IntervalArithmetic(precision)
    nodes = cert["nodes"]
    if len(nodes) != len(a):
        raise ValueError("Wrong node count")
    last_upper = None
    total = ar.integer(0)
    for i, node in enumerate(nodes):
        if node["index"] != i+1:
            raise ValueError("Wrong ordered node index")
        lo, hi = _read_fraction(node["scaled_lower"]), _read_fraction(node["scaled_upper"])
        if lo > hi or hi-lo > Fraction(1, 1 << bits):
            raise ValueError("Invalid root interval or width")
        if any(x.denominator & (x.denominator-1) for x in (lo, hi)):
            raise ValueError("Root brackets must be dyadic")
        if _read_fraction(node["lower"]) != lo/den or _read_fraction(node["upper"]) != hi/den:
            raise ValueError("Physical/scaled root coordinate mismatch")
        lc, lzero = sturm_count_scaled(a, b, lo)
        hc, hzero = sturm_count_scaled(a, b, hi)
        if lo == hi:
            if not (lzero and hzero and lc == i and hc == i and node["exact_dyadic_root"] is True):
                raise ValueError("Invalid exact-root claim")
        else:
            if not (lc == i and hc == i+1 and node["exact_dyadic_root"] is False):
                raise ValueError("Root interval does not have the required Sturm index")
        if node["lower_strict_sturm_count"] != lc or node["upper_strict_sturm_count"] != hc:
            raise ValueError("Recorded Sturm counts differ")
        if last_upper is not None and last_upper > lo:
            raise ValueError("Root order check failed")
        last_upper = hi
        actual = _weight_interval(a, b, lo, hi, ar)
        supplied = _Interval(Decimal(node["weight_lower"]), Decimal(node["weight_upper"]))
        if not (supplied.lo.is_finite() and supplied.hi.is_finite() and
                Decimal(0) <= supplied.lo <= actual.lo <= actual.hi <= supplied.hi <= Decimal(1)):
            raise ValueError("Supplied weight interval is not a valid directed enclosure")
        total = ar.add(total, supplied)
    if not total.lo <= 1 <= total.hi:
        raise ValueError("Weight sum does not enclose one")
    return {"verified": True, "input_binding": "separately supplied exact coefficients",
            "nodes_verified": len(nodes), "no_numerical_eigensolver": True,
            "wall_seconds": time.perf_counter()-wall_start,
            "cpu_seconds": time.process_time()-cpu_start}


def cms_bounds(certificate, threshold) -> dict[str, str]:
    """Conservative CMS bounds at an exact threshold.

    With 1-based indices:
      lower = sum_{i=1}^{k-1} w_i,low * 1{theta_{i+1},upper <= t};
      upper = w_1,high + sum_{i=2}^{k} w_i,high * 1{theta_{i-1},lower <= t}.
    The extra inclusion at equality in the upper envelope is intentional and
    conservative. A Python float denotes its exact binary-rational value.
    Call verify_certificate first when accepting an untrusted certificate.
    """
    if certificate.get("schema") != SCHEMA:
        raise ValueError("Wrong certificate schema")
    t = _fraction(threshold)
    nodes = certificate["nodes"]
    if not nodes:
        raise ValueError("No quadrature nodes")
    ar = _IntervalArithmetic(certificate["decimal_precision"])
    lo = Decimal(0)
    hi = Decimal(nodes[0]["weight_upper"])
    for i in range(len(nodes)-1):
        if _read_fraction(nodes[i+1]["upper"]) <= t:
            wi = Decimal(nodes[i]["weight_lower"])
            lo = ar._op(ROUND_FLOOR, lambda lo=lo, wi=wi: lo+wi)
    for i in range(1, len(nodes)):
        if _read_fraction(nodes[i-1]["lower"]) <= t:
            wi = Decimal(nodes[i]["weight_upper"])
            hi = ar._op(ROUND_CEILING, lambda hi=hi, wi=wi: hi+wi)
    lo, hi = max(Decimal(0), lo), min(Decimal(1), hi)
    if lo > hi:
        raise ArithmeticError("Invalid CMS enclosure")
    return {"lower": str(lo), "upper": str(hi), "threshold": _fraction_json(t)}
