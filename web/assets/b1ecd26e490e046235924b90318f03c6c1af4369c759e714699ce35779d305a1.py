#!/usr/bin/env python3
"""Finite-sample likelihood-ratio policies for rare Poisson signals.

Standard-library reference implementation.  Counts are assumed to be exactly
Poisson and the signal/background model parameters are treated as supplied.
The on/off routine conditions on the total count, so its false-alarm level is
uniform in the unknown common background rate.  It does not account for drift
between on and off regions; that drift must be included in a larger nuisance
model or independently calibrated.
The on/off power sum returns an explicit upper bound on its omitted Poisson
tail mass.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, lgamma, log


@dataclass(frozen=True)
class TestResult:
    threshold: int
    randomize_at_threshold: float
    size: float
    power: float


def _pmf(k: int, mean: float) -> float:
    if k < 0:
        return 0.0
    if mean < 0:
        raise ValueError("Poisson mean must be nonnegative")
    if mean == 0:
        return 1.0 if k == 0 else 0.0
    return exp(-mean + k * log(mean) - lgamma(k + 1))


def _poisson_upper_ge(k: int, mean: float, tol: float = 1e-14) -> float:
    """P[Poisson(mean) >= k], summed upward to avoid 1-CDF cancellation."""
    if k <= 0:
        return 1.0
    if mean == 0:
        return 0.0
    term = _pmf(k, mean)
    total = term
    j = k
    # The recurrence remains stable for the moderate means used in design.
    while j < max(k + 1000, int(mean + 40 * mean**0.5 + 100)):
        j += 1
        term *= mean / j
        total += term
        if term <= tol * total and j > mean:
            break
    return min(1.0, total)


def known_background_test(
    background_rate: float,
    signal_rate: float,
    exposure: float,
    false_alarm: float,
) -> TestResult:
    """Most-powerful size-alpha test for Poi(bT) vs Poi((b+s)T).

    Reject for large counts and randomize at one boundary count when the
    discrete null cannot attain the requested size exactly.
    """
    b, s, t, alpha = background_rate, signal_rate, exposure, false_alarm
    if b <= 0 or s < 0 or t < 0 or not 0 <= alpha <= 1:
        raise ValueError("Require b>0, s>=0, T>=0, and alpha in [0,1]")
    mean0, mean1 = b * t, (b + s) * t
    if alpha == 0:
        return TestResult(threshold=-1, randomize_at_threshold=0.0,
                          size=0.0, power=0.0)
    if alpha == 1:
        return TestResult(threshold=-1, randomize_at_threshold=1.0,
                          size=1.0, power=1.0)

    k = 0
    while _poisson_upper_ge(k + 1, mean0) > alpha:
        k += 1
    upper = _poisson_upper_ge(k + 1, mean0)
    at = _pmf(k, mean0)
    gamma = min(1.0, max(0.0, (alpha - upper) / at)) if at else 0.0
    size = upper + gamma * at
    power = _poisson_upper_ge(k + 1, mean1) + gamma * _pmf(k, mean1)
    return TestResult(k, gamma, size, power)


def _binom_pmf(k: int, n: int, p: float) -> float:
    if k < 0 or k > n:
        return 0.0
    if p == 0:
        return 1.0 if k == 0 else 0.0
    if p == 1:
        return 1.0 if k == n else 0.0
    return exp(lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)
               + k * log(p) + (n - k) * log1p_neg(p))


def log1p_neg(p: float) -> float:
    # log1p(-p) without importing another helper or losing accuracy near zero.
    from math import log1p
    return log1p(-p)


def _binom_upper_ge(k: int, n: int, p: float) -> float:
    if k <= 0:
        return 1.0
    return min(1.0, sum(_binom_pmf(j, n, p) for j in range(k, n + 1)))


def _conditional_binomial_test(n: int, p0: float, alpha: float, p1: float) -> tuple[float, float]:
    """Return exact conditional size and power, randomizing at a boundary."""
    if alpha == 0:
        return 0.0, _binom_upper_ge(n + 1, n, p1)
    if alpha == 1:
        return 1.0, 1.0
    # Build both upper tails in O(n), then randomize at one boundary count.
    masses0 = [_binom_pmf(k, n, p0) for k in range(n + 1)]
    masses1 = [_binom_pmf(k, n, p1) for k in range(n + 1)]
    tails0 = [0.0] * (n + 2)
    tails1 = [0.0] * (n + 2)
    for k in range(n, -1, -1):
        tails0[k] = tails0[k + 1] + masses0[k]
        tails1[k] = tails1[k + 1] + masses1[k]

    # j is the first count at which the test rejects without randomization.
    j = n + 1
    while j > 0 and tails0[j - 1] <= alpha:
        j -= 1
    strict = tails0[j]
    boundary = j - 1
    mass0 = masses0[boundary]
    gamma = min(1.0, max(0.0, (alpha - strict) / mass0)) if mass0 else 0.0
    size = strict + gamma * mass0
    power = tails1[j] + gamma * masses1[boundary]
    return size, power


def unknown_background_on_off_test(
    signal_rate: float,
    on_exposure: float,
    off_exposure: float,
    background_rate: float,
    false_alarm: float,
) -> tuple[float, float]:
    """Exact on/off test size and truncated power at one background value.

    Under H0, X_on~Poi(b*t_on), X_off~Poi(b*t_off).  Conditional on their
    total, X_on is Bin(total, t_on/(t_on+t_off)), eliminating b exactly.
    Under H1, only the on-region receives the added signal.  The reported
    size is analytically alpha up to floating-point summation; power is the
    Poisson mixture of conditional binomial powers. The power sum truncates at
    nmax, and the third return value bounds the omitted Poisson tail.
    """
    s, ton, toff, b, alpha = signal_rate, on_exposure, off_exposure, background_rate, false_alarm
    if s < 0 or ton <= 0 or toff < 0 or b < 0 or not 0 <= alpha <= 1:
        raise ValueError("Require s,b>=0, on exposure>0, off exposure>=0, alpha in [0,1]")
    if toff == 0:
        raise ValueError("No off exposure: the unknown background is not identified")

    p0 = ton / (ton + toff)
    mean_total_alt = (b + s) * ton + b * toff
    p1 = ((b + s) * ton / mean_total_alt) if mean_total_alt else p0
    nmax = max(40, int(mean_total_alt + 14 * mean_total_alt**0.5 + 80))
    power = 0.0
    for n in range(nmax + 1):
        _, conditional_power = _conditional_binomial_test(n, p0, alpha, p1)
        power += _pmf(n, mean_total_alt) * conditional_power
    omitted_tail_bound = _poisson_upper_ge(nmax + 1, mean_total_alt)
    return alpha, min(1.0, power), omitted_tail_bound


def main() -> None:
    b, s, alpha = 3.0, 0.5, 1e-3
    print("Known-background exact NP policy; rates per unit exposure")
    print("T   null size   power   boundary count   boundary randomization")
    for exposure in (2, 5, 10, 20, 40):
        r = known_background_test(b, s, exposure, alpha)
        print(f"{exposure:<3} {r.size:.6g}   {r.power:.6g}   {r.threshold:<15} {r.randomize_at_threshold:.6g}")
    print("\nUnknown common background, on/off conditional policy")
    print("b   on T   off T   total exposure   size   power   omitted-tail bound")
    for bg in (1.0, 3.0, 10.0):
        size, power, tail = unknown_background_on_off_test(s, 20.0, 20.0, bg, alpha)
        print(f"{bg:<3g} 20     20      40               {size:.6g} {power:.6g} {tail:.3g}")


if __name__ == "__main__":
    main()
