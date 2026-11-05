"""Finite-bit geometric clocks with a rational total-variation certificate.

The target is Geom_0(r): P(K=k) = r * (1-r)**k, k >= 0.  Inputs are
exact fractions.  This module never evaluates that exact rational power,
iterates to 1/r, or uses a floating-point logarithm.

The proof assumes independent unbiased random bits.  ``random.Random`` is
accepted for reproducible execution diagnostics, not as a source of literal
independent mathematical bits.

For repeated draws, compile once::

    from fractions import Fraction
    import random
    clock = GeometricClockCompiler(Fraction(1, 2**100), Fraction(1, 2**20))
    value, metadata = clock.sample(random.Random(20261105))

The convenience function ``sample_geometric`` compiles on each invocation.
All accuracy and resource bounds below are deterministic.  The only random
operation in a nontrivial draw is one ``rng.getrandbits(uniform_bits)`` call.
"""

from __future__ import annotations

from fractions import Fraction
import random
from typing import Any


def _ceil_div(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def _ceil_log2_ratio(numerator: int, denominator: int) -> int:
    """Exact ceil(log2(numerator/denominator)); no floating arithmetic."""
    if numerator <= 0 or denominator <= 0:
        raise ValueError("The logarithm arguments must be positive integers.")
    exponent = numerator.bit_length() - denominator.bit_length()
    if exponent >= 0:
        too_small = numerator > (denominator << exponent)
    else:
        too_small = (numerator << -exponent) > denominator
    return exponent + int(too_small)


def _integer_text(value: int) -> str:
    # Hexadecimal fallback avoids Python's decimal-conversion digit limit.
    return str(value) if value.bit_length() <= 4096 else hex(value)


def _fraction_text(value: Fraction) -> str:
    if max(value.numerator.bit_length(), value.denominator.bit_length()) <= 4096:
        return str(value)
    return f"{hex(value.numerator)}/{hex(value.denominator)}"


class GeometricClockCompiler:
    """Compile a capped, finite-bit approximation to ``Geom_0(r)``.

    Parameters
    ----------
    r:
        Exact success probability, ``Fraction`` with 0 < r <= 1.
    epsilon:
        Total-variation budget, ``Fraction`` with 0 < epsilon < 1.

    Construction for r < 1
    ----------------------
    Set t = ceil(log2(1/epsilon)), M = ceil(t/r), D = bit_length(M),
    B = ceil(log2(8*M/epsilon)), A = ceil(log2(16*M*M/epsilon)).
    There are D precomputed fixed-point powers and at most D binary-search
    comparisons per draw.  Each comparison costs at most D fixed-point
    multiplications.  Thus a draw uses at most D**2 multiplications, on
    operands of at most A+1 bits; it consumes exactly B fresh random bits.

    Error certificate
    -----------------
    Tail:       3 / (4 * 2**t).
    Uniform:    M / 2**B.
    Powers:     M*(M+1) / 2**A.
    Their sum is <= epsilon.  These are total-variation bounds, not merely
    CDF bounds.  The implementation rounds powers downward.  Its computed
    survival power for exponent n is between (1-r)**n - 2*n/2**A and
    (1-r)**n.  A coupling union bound over M CDF boundaries proves the
    uniform-plus-power bound even if rounded thresholds are not monotone.

    The integer cap M can be enormous, but its value never controls a loop
    in this class.  Exact rational powers with exponent M are never formed.
    """

    def __init__(self, r: Fraction, epsilon: Fraction):
        if not isinstance(r, Fraction) or not isinstance(epsilon, Fraction):
            raise TypeError("r and epsilon must be fractions.Fraction values.")
        if not 0 < r <= 1:
            raise ValueError("r must satisfy 0 < r <= 1.")
        if not 0 < epsilon < 1:
            raise ValueError("epsilon must satisfy 0 < epsilon < 1.")

        self.r = r
        self.epsilon = epsilon
        self._deterministic = r == 1

        if self._deterministic:
            self.tail_steps = 0
            self.k_max = 0
            self.index_bits = 0
            self.uniform_bits = 0
            self.fixed_point_bits = 0
            self.scale = 1
            self._powers: tuple[int, ...] = ()
            self.tail_tv_bound = Fraction(0)
            self.uniform_tv_bound = Fraction(0)
            self.power_tv_bound = Fraction(0)
        else:
            self.tail_steps = _ceil_log2_ratio(
                epsilon.denominator, epsilon.numerator
            )
            self.k_max = _ceil_div(self.tail_steps * r.denominator, r.numerator)
            self.index_bits = self.k_max.bit_length()
            self.uniform_bits = _ceil_log2_ratio(
                8 * self.k_max * epsilon.denominator, epsilon.numerator
            )
            self.fixed_point_bits = _ceil_log2_ratio(
                16 * self.k_max * self.k_max * epsilon.denominator,
                epsilon.numerator,
            )
            self.scale = 1 << self.fixed_point_bits
            base = (
                (r.denominator - r.numerator) << self.fixed_point_bits
            ) // r.denominator

            powers = [base]
            for _ in range(1, self.index_bits):
                previous = powers[-1]
                powers.append((previous * previous) >> self.fixed_point_bits)
            self._powers = tuple(powers)

            self.tail_tv_bound = Fraction(3, 4 << self.tail_steps)
            self.uniform_tv_bound = Fraction(self.k_max, 1 << self.uniform_bits)
            self.power_tv_bound = Fraction(
                self.k_max * (self.k_max + 1), self.scale
            )

        self.total_tv_bound = (
            self.tail_tv_bound + self.uniform_tv_bound + self.power_tv_bound
        )
        if self.total_tv_bound > epsilon:
            raise ArithmeticError("Internal error: the exact TV budget was exceeded.")
        if self.fixed_point_bits < self.uniform_bits:
            raise ArithmeticError("Internal error: incompatible fixed-point scales.")
        self._certificate = self._make_certificate()

    def _make_certificate(self) -> dict[str, Any]:
        d = self.index_bits
        a = self.fixed_point_bits
        return {
            "algorithm": "finite_bit_geometric_v1",
            "target": "Geom_0(r), number of failures before first success",
            "r": _fraction_text(self.r),
            "epsilon": _fraction_text(self.epsilon),
            "k_max": _integer_text(self.k_max),
            "tail_steps": self.tail_steps,
            "uniform_bits": self.uniform_bits,
            "fixed_point_bits": a,
            "max_output_bits": max(1, d),
            "power_table_entries": len(self._powers),
            "setup_fixed_point_multiplications": max(0, d - 1),
            "max_cdf_evaluations_per_draw": d,
            "max_exponent_bit_steps_per_draw": d * d,
            "max_fixed_point_multiplications_per_draw": d * d,
            "max_fixed_point_operand_bits": a + 1,
            "max_fixed_point_product_bits": 2 * a + 2,
            "power_table_payload_bits_upper_bound": d * (a + 1),
            "tail_tv_bound": _fraction_text(self.tail_tv_bound),
            "uniform_tv_bound": _fraction_text(self.uniform_tv_bound),
            "power_tv_bound": _fraction_text(self.power_tv_bound),
            "total_tv_bound": _fraction_text(self.total_tv_bound),
            "tv_budget_verified_by_exact_rationals": True,
            "proof_randomness_assumption": "independent unbiased random bits",
            "numeric_model": "exact integers with explicit downward fixed-point rounding",
            "large_integer_encoding": "decimal strings, hexadecimal above 4096 bits",
        }

    def certificate(self) -> dict[str, Any]:
        """Return JSON-safe parameter and worst-case resource metadata."""
        return self._certificate.copy()

    def _survival_and_counts(self, exponent: int) -> tuple[int, int, int]:
        """Return fixed-point power, multiplication count, exponent-bit count."""
        if not isinstance(exponent, int) or not 0 <= exponent <= self.k_max:
            raise ValueError("Exponent must be an integer in [0, k_max].")
        value = self.scale
        remaining = exponent
        table_index = 0
        multiplications = 0
        while remaining:
            if remaining & 1:
                value = (value * self._powers[table_index]) >> self.fixed_point_bits
                multiplications += 1
            remaining >>= 1
            table_index += 1
        return value, multiplications, table_index

    def fixed_point_survival(self, exponent: int) -> int:
        """Return an integer representing a downward approximation to (1-r)^n.

        Divide the result by ``scale`` to interpret it.  The method is useful
        for auditing; it does not construct the exact rational target power.
        """
        return self._survival_and_counts(exponent)[0]

    def _draw_from_uniform_integer(self, uniform_integer: int) -> tuple[int, dict[str, int]]:
        """Deterministic inverse transform for one B-bit integer (audit hook)."""
        if not isinstance(uniform_integer, int):
            raise TypeError("The uniform integer must be an integer.")
        if not 0 <= uniform_integer < (1 << self.uniform_bits):
            raise ValueError("The uniform integer lies outside its prescribed bit range.")
        scaled_uniform = uniform_integer << (
            self.fixed_point_bits - self.uniform_bits
        )
        lower, upper = 0, self.k_max
        queries = multiplications = bit_steps = 0
        while lower < upper:
            middle = (lower + upper) // 2
            survival, count, steps = self._survival_and_counts(middle + 1)
            queries += 1
            multiplications += count
            bit_steps += steps
            if scaled_uniform < self.scale - survival:
                upper = middle
            else:
                lower = middle + 1
        return lower, {
            "actual_cdf_evaluations": queries,
            "actual_fixed_point_multiplications": multiplications,
            "actual_exponent_bit_steps": bit_steps,
            "actual_random_bits": self.uniform_bits,
        }

    def sample(self, rng: random.Random) -> tuple[int, dict[str, Any]]:
        """Return one geometric index and the analytic/error resource metadata.

        ``rng`` must provide ``getrandbits(k)``.  Its uniformity and independence
        are assumptions of the mathematical guarantee.  Seeded PRNG draws are
        reproducible diagnostics, and are explicitly labelled as such.
        """
        uniform_integer = 0 if self._deterministic else rng.getrandbits(self.uniform_bits)
        value, counts = self._draw_from_uniform_integer(uniform_integer)
        metadata = self.certificate()
        metadata.update(counts)
        metadata["bit_source"] = f"{type(rng).__module__}.{type(rng).__qualname__}"
        metadata["randomness_note"] = (
            "The theorem assumes ideal independent fair bits; a seeded PRNG is a diagnostic."
        )
        return value, metadata

    def draw(self, rng: random.Random) -> int:
        """Return just the index; reuse the compiled powers without metadata copying."""
        uniform_integer = 0 if self._deterministic else rng.getrandbits(self.uniform_bits)
        return self._draw_from_uniform_integer(uniform_integer)[0]


def sample_geometric(
    r: Fraction, epsilon: Fraction, rng: random.Random
) -> tuple[int, dict[str, Any]]:
    """Compile and draw once; use GeometricClockCompiler for repeated draws."""
    return GeometricClockCompiler(r, epsilon).sample(rng)


__all__ = ["GeometricClockCompiler", "sample_geometric"]
