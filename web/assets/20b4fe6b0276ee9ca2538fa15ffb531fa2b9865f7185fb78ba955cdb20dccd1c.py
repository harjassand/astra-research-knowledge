import math

from certificate_checker import (
    effective_face_margin,
    log_gamma_mixture_evalue,
    poisson_rate_confidence_interval,
    reaction_face_margin,
)


def test_rate_cs_endpoints_and_open_interior():
    n, exposure, delta, cap = 100, 100.0, 0.01, 2.0
    interval = poisson_rate_confidence_interval(n, exposure, delta, cap)
    assert interval is not None
    lo, hi = interval
    cutoff = math.log(1 / delta)
    assert abs(log_gamma_mixture_evalue(lo, n, exposure) - cutoff) < 1e-10
    assert abs(log_gamma_mixture_evalue(hi, n, exposure) - cutoff) < 1e-10
    assert log_gamma_mixture_evalue(1.0, n, exposure) < cutoff
    assert lo < 1.0 < hi


def test_endpoint_box_margins_and_transport_loss():
    reactions = [
        {"y": (0,), "nu": (1,), "k_lo": 0.95, "k_hi": 1.05},
        {"y": (1,), "nu": (-1,), "k_lo": 0.95, "k_hi": 1.05},
    ]
    lo = reaction_face_margin(reactions, (0.5,), (1.5,), 0, 0.25, "lower")
    hi = reaction_face_margin(reactions, (0.5,), (1.5,), 0, 0.25, "upper")
    assert abs(lo - 0.1625) < 1e-12
    assert abs(hi - 0.1375) < 1e-12
    assert abs(effective_face_margin(lo, 1.0, (0.05,), 0.25) - 0.15) < 1e-12
    assert abs(effective_face_margin(hi, 1.0, (0.05,), 0.25) - 0.125) < 1e-12


def test_zero_exposure_does_not_fabricate_positive_rate_evidence():
    assert poisson_rate_confidence_interval(0, 0.0, 0.05, 2.0) == (0.0, 2.0)
    assert poisson_rate_confidence_interval(1, 0.0, 0.05, 2.0) is None


if __name__ == "__main__":
    test_rate_cs_endpoints_and_open_interior()
    test_endpoint_box_margins_and_transport_loss()
    test_zero_exposure_does_not_fabricate_positive_rate_evidence()
    print("3 certificate checker tests passed")
