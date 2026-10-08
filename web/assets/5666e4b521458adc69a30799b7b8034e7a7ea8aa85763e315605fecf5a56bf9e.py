"""Small model-conditional rate-CI and box-margin checker.

This file checks arithmetic only. It does not validate a mass-action/RDME model,
reciprocal transport, or a physical material.
"""

from __future__ import annotations

from math import exp, inf, lgamma, log
from typing import Iterable, Sequence


def log_gamma_mixture_evalue(theta: float, count: int, exposure: float,
                             shape: float = 1.0, rate: float = 1.0) -> float:
    """Log of Gamma(shape, rate)-mixture LR against candidate rate theta.

    The counting-process intensity must be theta * h(t), with known predictable
    h and integrated exposure ``exposure = integral h(t) dt``.
    """
    if count < 0 or exposure < 0 or shape <= 0 or rate <= 0 or theta < 0:
        raise ValueError("count/exposure/rate/shape/theta outside domain")
    if theta == 0:
        if count:
            return inf
        return shape * log(rate) - shape * log(rate + exposure)
    return (
        shape * log(rate)
        + lgamma(shape + count) - lgamma(shape)
        - (shape + count) * log(rate + exposure)
        - count * log(theta)
        + theta * exposure
    )


def poisson_rate_confidence_interval(count: int, exposure: float, delta: float,
                                     cap: float, shape: float = 1.0,
                                     prior_rate: float = 1.0,
                                     iterations: int = 100) -> tuple[float, float] | None:
    """Invert the mixture e-process to get a time-uniform CS at one look.

    Return the closure of {theta in [0, cap]: e(theta) < 1/delta}.
    ``None`` means the data are inconsistent with every capped rate at this
    confidence level. Repeated calls at optional stopping times retain coverage.
    """
    if not 0 < delta < 1 or cap < 0:
        raise ValueError("delta must be in (0,1) and cap nonnegative")
    cutoff = log(1.0 / delta)

    def f(theta: float) -> float:
        return log_gamma_mixture_evalue(theta, count, exposure, shape, prior_rate)

    if count and exposure == 0:
        return None  # zero exposure cannot produce a count under this model
    minimizer = min(cap, count / exposure) if count and exposure else 0.0
    if f(minimizer) >= cutoff:
        return None

    if f(0.0) < cutoff:
        lower = 0.0
    else:
        left, right = 0.0, minimizer
        for _ in range(iterations):
            mid = (left + right) / 2
            if f(mid) < cutoff:
                right = mid
            else:
                left = mid
        lower = right

    if f(cap) < cutoff:
        upper = cap
    else:
        left, right = minimizer, cap
        for _ in range(iterations):
            mid = (left + right) / 2
            if f(mid) < cutoff:
                left = mid
            else:
                right = mid
        upper = left
    return lower, upper


def _monomial(point: Sequence[float], complex_: Sequence[int]) -> float:
    value = 1.0
    for x, power in zip(point, complex_):
        value *= x ** power
    return value


def reaction_face_margin(reactions: Iterable[dict], lower: Sequence[float],
                         upper: Sequence[float], species: int,
                         collar: float, side: str) -> float:
    """Worst deterministic reaction drift toward one box face.

    Each reaction dict has ``y`` (reactant exponents), ``nu`` (jump vector),
    ``k_lo`` and ``k_hi``. Rate intervals are treated independently, so the
    result remains conservative when their actual confidence set is narrower.
    """
    if side not in {"lower", "upper"}:
        raise ValueError("side must be 'lower' or 'upper'")
    if not 0 <= species < len(lower) or len(lower) != len(upper):
        raise ValueError("invalid species/bounds")
    if not 0 < collar <= upper[species] - lower[species]:
        raise ValueError("collar outside box")
    low_point = list(lower)
    high_point = list(upper)
    if side == "lower":
        high_point[species] = lower[species] + collar
    else:
        low_point[species] = upper[species] - collar

    margin = 0.0
    for reaction in reactions:
        nu = reaction["nu"][species]
        if nu == 0:
            continue
        if side == "lower":
            if nu > 0:
                margin += nu * reaction["k_lo"] * _monomial(low_point, reaction["y"])
            else:
                margin -= abs(nu) * reaction["k_hi"] * _monomial(high_point, reaction["y"])
        else:
            if nu < 0:
                margin += abs(nu) * reaction["k_lo"] * _monomial(low_point, reaction["y"])
            else:
                margin -= nu * reaction["k_hi"] * _monomial(high_point, reaction["y"])
    return margin


def effective_face_margin(reaction_margin: float, alpha: float,
                          incident_transport_caps: Iterable[float],
                          collar: float) -> float:
    """Subtract the symmetric-transport box-collar loss from PROOF.md."""
    if alpha <= 0 or collar < 0:
        raise ValueError("alpha must be positive and collar nonnegative")
    return reaction_margin - collar * sum(incident_transport_caps) / alpha


if __name__ == "__main__":
    # Synthetic arithmetic fixture only: two one-species adsorption/removal
    # channels, confidence intervals supplied as if returned by an assay.
    reactions = [
        {"y": (0,), "nu": (1,), "k_lo": 0.95, "k_hi": 1.05},
        {"y": (1,), "nu": (-1,), "k_lo": 0.95, "k_hi": 1.05},
    ]
    box, collar = (0.5,), (1.5,)
    low = reaction_face_margin(reactions, box, collar, 0, 0.25, "lower")
    high = reaction_face_margin(reactions, box, collar, 0, 0.25, "upper")
    ci = poisson_rate_confidence_interval(100, 100.0, 0.01, 2.0)
    print({"synthetic_only": True, "reaction_margins": [low, high], "rate_cs": ci})
