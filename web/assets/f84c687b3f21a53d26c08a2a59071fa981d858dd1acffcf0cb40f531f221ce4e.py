"""Exact rational scalar-feature rounding on a disjoint union of K_{2,2}s.

Each block i has two perfect matchings.  The input p_i is the desired
probability of the diagonal matching, and a_i is a supplied rational scalar
feature weight with |a_i| <= 1.  The returned sampler has exact edge
marginals and every matching it can output has feature error at most
2 max_i |a_i|.

The caller supplies randbelow(q), which must return an exactly uniform integer
in {0,...,q-1}.  A standard rejection sampler from fair bits implements this
with expected fewer than 2 ceil(log2(q)) bits per call.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Sequence


Edge = tuple[int, int, int]  # (component, left endpoint, right endpoint)
Matching = tuple[Edge, ...]
RandBelow = Callable[[int], int]
GetRandBits = Callable[[int], int]


def fair_bit_randbelow(bound: int, getrandbits: GetRandBits) -> int:
    """Exact uniform integer in range(bound), via rejection from fair bits.

    For bound > 1 this uses an expected fewer than 2*ceil(log2(bound)) fair
    bits.  The getrandbits callback must return a uniform k-bit integer.
    """
    if bound < 1:
        raise ValueError("bound must be positive")
    if bound == 1:
        return 0
    bits = (bound - 1).bit_length()
    while True:
        value = getrandbits(bits)
        if 0 <= value < bound:
            return value


@dataclass(frozen=True)
class Sample:
    diagonal_choices: tuple[int, ...]
    matching: Matching
    feature_error: Fraction


def _matching(choices: Sequence[int]) -> Matching:
    edges: list[Edge] = []
    for i, choice in enumerate(choices):
        if choice == 1:
            edges.extend(((i, 0, 0), (i, 1, 1)))
        elif choice == 0:
            edges.extend(((i, 0, 1), (i, 1, 0)))
        else:
            raise ValueError("each matching choice must be 0 or 1")
    return tuple(edges)


def _bernoulli(probability: Fraction, randbelow: RandBelow) -> int:
    """Exact Bernoulli draw for a rational probability."""
    if not 0 <= probability <= 1:
        raise ValueError("probability must lie in [0, 1]")
    draw = randbelow(probability.denominator)
    if not 0 <= draw < probability.denominator:
        raise ValueError("randbelow(q) must return an integer in range(q)")
    return int(draw < probability.numerator)


def _interval(z: Fraction, direction: Fraction) -> tuple[Fraction, Fraction]:
    """t interval for which 0 <= z + t*direction <= 1."""
    if direction == 0:
        raise ValueError("zero direction has no finite interval")
    first = -z / direction
    second = (1 - z) / direction
    return min(first, second), max(first, second)


def sample_k22_scalar_marginals(
    diagonal_marginals: Sequence[Fraction],
    weights: Sequence[Fraction],
    randbelow: RandBelow,
) -> Sample:
    """Sample one perfect matching with prescribed marginals and bounded error.

    For block i, both diagonal edges have marginal p_i and both off-diagonal
    edges have marginal 1-p_i.  The feature puts +a_i/2 on each diagonal
    edge and -a_i/2 on each off-diagonal edge.  Thus the sampled matching's
    feature discrepancy from its mean is 2 sum_i a_i (z_i-p_i).

    Pairwise moves preserve sum_i a_i z_i exactly and preserve each coordinate
    in conditional expectation.  Once at most one z_i remains fractional,
    its final Bernoulli rounding changes the preserved scalar objective by at
    most max_i |a_i|.
    """
    p = tuple(Fraction(value) for value in diagonal_marginals)
    a = tuple(Fraction(value) for value in weights)
    if len(p) != len(a):
        raise ValueError("marginals and weights must have equal length")
    if any(not 0 <= value <= 1 for value in p):
        raise ValueError("each diagonal marginal must lie in [0, 1]")
    if any(abs(value) > 1 for value in a):
        raise ValueError("each feature weight must lie in [-1, 1]")

    z = list(p)
    while True:
        fractional = [i for i, value in enumerate(z) if 0 < value < 1]
        if len(fractional) < 2:
            break
        i, j = fractional[0], fractional[1]

        # A direction in the kernel of the supplied scalar feature.  If both
        # coefficients vanish, rounding z_i alone is already objective-safe.
        if a[i] == 0 and a[j] == 0:
            d_i, d_j = Fraction(1), Fraction(0)
        else:
            d_i, d_j = a[j], -a[i]

        lows: list[Fraction] = []
        highs: list[Fraction] = []
        for coordinate, direction in ((i, d_i), (j, d_j)):
            if direction:
                low, high = _interval(z[coordinate], direction)
                lows.append(low)
                highs.append(high)
        t_minus = max(lows)
        t_plus = min(highs)
        if not t_minus < 0 < t_plus:
            raise ArithmeticError("fractional pair did not yield a two-sided move")

        width = t_plus - t_minus
        probability_minus = t_plus / width
        if _bernoulli(probability_minus, randbelow):
            step = t_minus
        else:
            step = t_plus

        z[i] += step * d_i
        z[j] += step * d_j
        if any(value < 0 or value > 1 for value in (z[i], z[j])):
            raise ArithmeticError("exact update left the unit interval")

    # At most one coordinate remains fractional; finalize it by its exact
    # prescribed Bernoulli probability.
    for i, value in enumerate(z):
        if value not in (0, 1):
            z[i] = Fraction(_bernoulli(value, randbelow))

    choices = tuple(int(value) for value in z)
    error = 2 * sum(
        (a_i * (Fraction(choice) - p_i)
         for a_i, choice, p_i in zip(a, choices, p)),
        Fraction(0),
    )
    bound = 2 * max((abs(value) for value in a), default=Fraction(0))
    if abs(error) > bound:
        raise ArithmeticError("the sampled matching violated the proved bound")
    return Sample(choices, _matching(choices), error)
