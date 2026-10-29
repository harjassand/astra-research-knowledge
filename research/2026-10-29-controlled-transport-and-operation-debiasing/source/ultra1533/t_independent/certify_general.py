"""Symbolic/scalar/general-law consumer; no new sampler or source run."""
import itertools
import json
from pathlib import Path
import time
import sympy as sp
from flint import fmpq, arb, ctx
from exact_conductance import Frame, cycle, torus
from ordinary import proved_burnin

HERE = Path(__file__).resolve().parent


def main():
    start = time.perf_counter()
    s, t, rho, R, current = sp.symbols("s t rho R current", real=True)
    # Scalar maximum is an exact nonnegative-square identity, not a mesh.
    maximum_identity = sp.expand(1 + (t ** 2 - 1) * s - (t + 1) ** 2 * s * (1 - s) - ((t + 1) * s - 1) ** 2)
    assert maximum_identity == 0
    R0 = R / (1 - rho * R)
    r0 = current / (1 - rho * R)
    removal_identity = sp.factor(r0 ** 2 / (1 + rho * R0) - current ** 2 / (1 - rho * R))
    assert removal_identity == 0

    # Recover the q=1 independent conditional law at every six-cycle state.
    independent = Frame(6, cycle(6), contrast=fmpq(1))
    independent_checks = 0
    for state in itertools.product((0, 1), repeat=6):
        inverse = independent.inverse_for(state)
        assert inverse == independent.base_inverse
        for e in range(6):
            assert independent.low_ratio(inverse, state, e)[0] == 1
            independent_checks += 1

    # A second positive representation must preserve the SAME law, not just moments.
    frame = Frame(6, cycle(6))
    ctx.prec = 256
    tau = [(b.transpose() * frame.base_inverse * b)[0, 0] for b in frame.columns]
    assert sum(tau, fmpq(0)) == 5
    shifted = [1 / (1 + (arb(2).log() * arb(x) / 2).exp()) for x in tau]
    normalization = arb(1)
    for x in tau:
        normalization *= (1 + (-arb(2).log() * arb(x) / 2).exp()) / 2
    max_error = 0.0
    representation_checks = 0
    for state in itertools.product((0, 1), repeat=6):
        ratio = frame.determinant_for(state) / frame.base.det()
        leverage_sum = sum((x * b for x, b in zip(tau, state)), fmpq(0))
        accept = ((arb(2).log() * arb(leverage_sum) - arb(ratio).log()) / 2).exp()
        assert accept > 0 and accept < 1 + arb(2) ** -180
        proposal = arb(1)
        for b, p in zip(state, shifted):
            proposal *= p if b else 1 - p
        target = arb(fmpq(1, 64)) / arb(ratio).sqrt()
        difference = proposal * accept * normalization / target - 1
        assert abs(difference) < arb(2) ** -180
        max_error = max(max_error, float(abs(difference).upper()))
        representation_checks += 1

    # Both algorithms receive the sharpened constant; no performance rerun.
    sharp = Frame(16, torus(4), contraction_bound=fmpq(43, 1000))
    q4 = Frame(16, torus(4), contrast=fmpq(4), contraction_bound=fmpq(1, 2))
    vector_sharp = Frame(16, torus(4), components=3, contraction_bound=fmpq(13, 100))
    delta = (1 / arb(2).log()).log() - 1 + arb(2).log()
    proposal_lower = (-arb(63) * delta / 2).exp()
    base_rejection_upper = ((1 + 1 / arb(2).sqrt()) / 2) ** 63
    record = {"maximum_square_identity": str(maximum_identity), "rank_one_removal_identity": str(removal_identity),
              "q1_exact_checks": independent_checks, "leverage_law_checks": representation_checks,
              "leverage_law_max_error_upper_display": max_error, "leverage_law_error_certified_upper": "2^-180",
              "sharpened_q2_scalar": {"constant_upper": str(sharp.c), "cftp_initial_window": sharp.initial_window,
                                        "ordinary_tv_1percent_steps": proved_burnin(sharp)},
              "sharpened_q2_vector": {"constant_upper": str(vector_sharp.c), "cftp_initial_window": vector_sharp.initial_window},
              "q4_scalar_constant": str(q4.c), "q2_logdet_chord_error_ball": str(delta),
              "64site_leverage_acceptance_uniform_lower_ball": str(proposal_lower),
              "64site_ordinary_gaussian_acceptance_upper_ball": str(base_rejection_upper),
              "seconds": time.perf_counter() - start,
              "scope": "algebra and finite same-law receiver; no independent audit, new source, stochastic run or general CPU-complexity claim"}
    (HERE / "GENERAL_CERTIFICATE.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
