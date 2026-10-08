"""Cost-aware paired intervention design for the two-mechanism model.

This is a small executable implementation of the model-level result in
CAUSAL_DESIGN_LAW.md. It does not validate biological assumptions or acquire
the supplied quantities (effect gap, noise bound, action range, or costs).
"""

from dataclasses import dataclass
from math import log, sqrt
from typing import Iterable, Optional, Tuple


@dataclass(frozen=True)
class Design:
    amplitude: float
    precision: float
    endpoint_noise_proxy: float
    endpoint_cost: float
    information_per_cost: float

    @property
    def pair_cost(self) -> float:
        return 2.0 * self.endpoint_cost


def optimal_design(
    *,
    max_amplitude: float,
    effect_gap: float,
    nonmeasurement_noise_proxy: float,
    intervention_base_cost: float,
    intervention_quadratic_cost: float,
    measurement_setup_cost: float,
    measurement_cost_per_precision: float,
) -> Design:
    """Return the closed-form optimum for symmetric quadratic intervention cost.

    One endpoint call at magnitude ``a`` and precision ``tau`` costs
    ``c0 + kappa*a**2 + m0 + gamma*tau``. The returned symmetric pair uses
    ``do(+a)`` and ``do(-a)`` on independent units.
    """
    values = (
        max_amplitude,
        effect_gap,
        nonmeasurement_noise_proxy,
        intervention_base_cost,
        intervention_quadratic_cost,
        measurement_setup_cost,
        measurement_cost_per_precision,
    )
    if any(x < 0.0 for x in values):
        raise ValueError("design parameters and costs must be nonnegative")
    if max_amplitude == 0.0 or effect_gap == 0.0:
        raise ValueError("positive action range and effect gap are required")
    if nonmeasurement_noise_proxy == 0.0:
        raise ValueError("a positive noise proxy gives a finite precision optimum")
    if intervention_base_cost + measurement_setup_cost <= 0.0:
        raise ValueError("a positive per-call setup cost is required")
    if measurement_cost_per_precision == 0.0:
        raise ValueError("measurement precision must have a positive marginal cost")

    amplitude = max_amplitude
    setup_and_intervention = (
        intervention_base_cost
        + measurement_setup_cost
        + intervention_quadratic_cost * amplitude**2
    )
    precision = sqrt(
        setup_and_intervention
        / (nonmeasurement_noise_proxy * measurement_cost_per_precision)
    )
    endpoint_noise_proxy = nonmeasurement_noise_proxy + 1.0 / precision
    endpoint_cost = (
        intervention_base_cost
        + intervention_quadratic_cost * amplitude**2
        + measurement_setup_cost
        + measurement_cost_per_precision * precision
    )
    information_per_cost = (
        effect_gap**2 * amplitude**2
        / (2.0 * endpoint_noise_proxy * endpoint_cost)
    )
    return Design(
        amplitude=amplitude,
        precision=precision,
        endpoint_noise_proxy=endpoint_noise_proxy,
        endpoint_cost=endpoint_cost,
        information_per_cost=information_per_cost,
    )


@dataclass
class PairedEvidenceTest:
    """Anytime-valid paired e-process test for H0 versus positive H1 effect."""

    design: Design
    effect_gap: float
    nonmeasurement_noise_proxy: float
    error_probability: float
    score: float = 0.0
    pairs_seen: int = 0
    decision: Optional[str] = None

    def __post_init__(self) -> None:
        if self.effect_gap <= 0.0:
            raise ValueError("effect_gap must be positive")
        if self.nonmeasurement_noise_proxy <= 0.0:
            raise ValueError("noise proxy must be positive")
        if not 0.0 < self.error_probability < 0.5:
            raise ValueError("error_probability must lie in (0, 1/2)")

    def update(self, paired_difference: float) -> Tuple[str, int, float]:
        """Add D=(Z_plus-Z_minus)/2 and return (status, pairs, log-evidence).

        Status is ``H0``, ``H1``, or ``continue``. The caller pays for and
        supplies every pair; each pair is two interventions plus two endpoint
        measurements at the selected precision.
        """
        if self.decision in ("H0", "H1"):
            raise RuntimeError("the sequential test has already stopped")

        q = self.effect_gap * self.design.amplitude
        pair_noise_proxy = (
            self.nonmeasurement_noise_proxy + 1.0 / self.design.precision
        ) / 2.0
        increment = (q / pair_noise_proxy) * (paired_difference - q / 2.0)
        self.score += increment
        self.pairs_seen += 1

        threshold = log(1.0 / self.error_probability)
        if self.score >= threshold:
            self.decision = "H1"
        elif self.score <= -threshold:
            self.decision = "H0"
        else:
            self.decision = "continue"
        return self.decision, self.pairs_seen, self.score

    def cost_if_stopped(self) -> float:
        """Return accrued intervention and measurement cost for observed pairs."""
        return self.pairs_seen * self.design.pair_cost


def run_sequential_test(
    differences: Iterable[float],
    *,
    design: Design,
    effect_gap: float,
    nonmeasurement_noise_proxy: float,
    error_probability: float,
) -> Tuple[str, int, float]:
    """Consume a supplied stream of paired differences until decision/exhaustion."""
    test = PairedEvidenceTest(
        design=design,
        effect_gap=effect_gap,
        nonmeasurement_noise_proxy=nonmeasurement_noise_proxy,
        error_probability=error_probability,
    )
    for difference in differences:
        result = test.update(float(difference))
        if result[0] != "continue":
            return result
    return "continue", test.pairs_seen, test.score
