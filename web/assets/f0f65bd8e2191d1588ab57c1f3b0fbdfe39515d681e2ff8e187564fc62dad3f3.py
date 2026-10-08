"""Exact feature rounding for centered disjoint K_{2,2} matching polytopes.

Input weights are rational scalars a_i in [-1, 1].  The feature row assigns
value +a_i/2 to each edge of the diagonal matching in block i and -a_i/2 to
each edge of the off-diagonal matching.  The returned two perfect matchings,
with probability 1/2 each, have exact edge marginals 1/2 and feature error at
most max_i |a_i| <= 1 in every atom.
"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence


Edge = tuple[int, int, int]  # (component, left endpoint, right endpoint)
Matching = tuple[Edge, ...]


@dataclass(frozen=True)
class RoundingLaw:
    probabilities: tuple[Fraction, Fraction]
    matchings: tuple[Matching, Matching]
    signs: tuple[int, ...]
    feature_error: Fraction


def _matching(signs: Sequence[int]) -> Matching:
    edges: list[Edge] = []
    for i, sign in enumerate(signs):
        if sign == 1:
            edges.extend(((i, 0, 0), (i, 1, 1)))
        elif sign == -1:
            edges.extend(((i, 0, 1), (i, 1, 0)))
        else:
            raise ValueError("signs must be +1 or -1")
    return tuple(edges)


def round_centered_k22_scalar(weights: Sequence[Fraction]) -> RoundingLaw:
    """Return a two-atom exact-marginal law with scalar feature error at most 1.

    The two-bin greedy signing maintains the absolute load difference at most
    the largest weight seen so far.  All calculations use exact fractions.
    """
    exact = tuple(Fraction(a) for a in weights)
    if any(abs(a) > 1 for a in exact):
        raise ValueError("each feature weight must lie in [-1, 1]")

    loads = [Fraction(0), Fraction(0)]
    signs: list[int] = []
    for a in exact:
        side = 0 if loads[0] <= loads[1] else 1
        orientation = 1 if side == 0 else -1
        loads[side] += abs(a)
        signs.append(orientation * (1 if a >= 0 else -1))

    sigma = tuple(signs)
    antipode = tuple(-s for s in sigma)
    error = abs(sum((s * a for s, a in zip(sigma, exact)), Fraction(0)))
    law = RoundingLaw(
        probabilities=(Fraction(1, 2), Fraction(1, 2)),
        matchings=(_matching(sigma), _matching(antipode)),
        signs=sigma,
        feature_error=error,
    )
    return law
