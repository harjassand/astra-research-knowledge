#!/usr/bin/env python3
"""Population checks of the actual continuous-observation lower-bound source.

Checks the generator, exact echo/density identities, killed-path filter,
and backwards information bound on noncommuting transcript products.
These are mathematical model checks, not samples certifying a device.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent


def main():
    states = np.asarray(list(itertools.product([-1.0, 1.0], repeat=2)))
    a, b = states[:, 0], states[:, 1]
    mu = np.full(4, 0.25)
    f = 1 + a
    base = np.full((4, 4), 0.25) - np.eye(4)
    b2 = np.asarray([1.0, -1.0])
    ones = np.ones(2)
    rng = np.random.default_rng(2026103001203)
    theta_values = [0.25, 0.125, 0.0625, 0.03125, 0.015625]
    errors = {k: 0.0 for k in (
        "generator_rate", "density", "echo_identity", "full_state_TV",
        "filter_derivative", "filter_jump", "transcript_transpose",
        "backwards_posterior")}
    cases = []
    posterior_bound_ratio = 0.0
    filter_bound_ratio = 0.0
    compensator_bound_ratio = 0.0
    transcript_count = 0

    def waiting(aa, q):
        return np.asarray([[-0.75 + q * aa / 2, 0.25],
                           [0.25, -0.75 - q * aa / 2]])

    def jump(aa, q):
        return np.asarray([[0.25, 0.25 - q * aa / 2],
                           [0.25 + q * aa / 2, 0.25]])

    for theta in theta_values:
        gen = base + theta * (np.outer(a, b) + np.outer(b, a)) / 4
        assert np.max(np.abs(gen.sum(axis=1))) < 1e-14
        assert np.array_equal(gen, gen.T)
        for i, (aa, bb) in enumerate(states):
            for j, (cc, dd) in enumerate(states):
                if i == j:
                    continue
                expected = (0.25 - theta * aa * bb / 2
                            if aa != cc and bb != dd else 0.25)
                errors["generator_rate"] = max(errors["generator_rate"],
                                                abs(gen[i, j] - expected))
                assert 0.125 <= gen[i, j] <= 0.375
        gap = float(np.linalg.eigvalsh(-gen)[1])
        assert gap >= 0.75 - 1e-14
        p, p0 = expm(gen), expm(base)
        rho, rho0 = p.T @ f, p0.T @ f
        formula = 1 + math.exp(-1) * (math.cosh(theta) * a + math.sinh(theta) * b)
        errors["density"] = max(errors["density"], float(np.max(np.abs(rho - formula))))
        delta = rho - rho0
        distance = float(mu @ delta**2)
        echo = float(mu @ (f * (p @ p.T @ f + p0 @ p0.T @ f - 2 * p @ p0.T @ f)))
        errors["echo_identity"] = max(errors["echo_identity"], abs(distance - echo))
        hidden_tv = float(mu @ np.abs(delta) / 2)
        formula_tv = math.exp(-1) * math.sinh(theta) / 2
        errors["full_state_TV"] = max(errors["full_state_TV"], abs(hidden_tv - formula_tv))
        visible_gap = math.exp(-1) * (math.cosh(theta) - 1) / 2
        menu_upper = math.exp(-1) * (math.cosh(theta) - 1 + 2 * theta * math.sinh(theta)) / 2

        # Check both filter formulae against the normalized exact hidden
        # posterior update, including interval endpoints and interior means.
        for aa in (-1.0, 1.0):
            for q in (0.0, theta):
                k, j = waiting(aa, q), jump(aa, q)
                assert np.array_equal(k, k.T)
                assert np.array_equal(j.T, jump(-aa, q))
                for h in np.linspace(-2 * theta, 2 * theta, 101):
                    pr = np.asarray([(1 + h) / 2, (1 - h) / 2])
                    derivative = float(pr @ k @ b2 - (pr @ k @ ones) * h)
                    formula_derivative = -h / 2 + q * aa * (1 - h * h) / 2
                    hnext = float(pr @ j @ b2 / (pr @ j @ ones))
                    formula_jump = q * aa / (1 - q * aa * h)
                    errors["filter_derivative"] = max(errors["filter_derivative"], abs(derivative - formula_derivative))
                    errors["filter_jump"] = max(errors["filter_jump"], abs(hnext - formula_jump))
                    assert abs(hnext) <= 2 * theta + 1e-14
                    lam_delta = -q * aa * h / 2
                    phi = (0.5 + lam_delta) * math.log1p(2 * lam_delta) - lam_delta
                    assert phi >= -1e-15
                    bound = 2 * theta**4 if q else 0.0
                    assert phi <= bound + 1e-15
                    if q:
                        compensator_bound_ratio = max(compensator_bound_ratio, phi / bound)

        # Arbitrary finite transcripts use noncommuting killed propagators,
        # with independent allowed pre-jump and post-jump controls. No claim
        # that the transposed feedback schedule is causally executable.
        for _ in range(120):
            aa = float(rng.choice([-1, 1]))
            ops = []
            for stage in range(int(rng.integers(2, 12))):
                for _ in range(int(rng.integers(1, 4))):
                    q = theta * int(rng.integers(0, 2))
                    dt = float(rng.uniform(0.01, 0.8))
                    ops.append(("wait", aa, q, dt))
                q = theta * int(rng.integers(0, 2))
                ops.append(("jump", aa, q, 0.0))
                aa = -aa
            ops.append(("wait", aa, theta * int(rng.integers(0, 2)), 0.3))
            mat = np.eye(2)
            pr = np.full(2, 0.5)
            for kind, aa, q, dt in ops:
                factor = expm(waiting(aa, q) * dt) if kind == "wait" else jump(aa, q)
                mat = mat @ factor
                pr = pr @ factor
                pr /= pr.sum()
                filter_bound_ratio = max(filter_bound_ratio, abs(float(pr @ b2)) / (2 * theta))
            reverse = np.eye(2)
            reverse_pr = np.full(2, 0.5)
            for kind, aa, q, dt in reversed(ops):
                factor = expm(waiting(aa, q) * dt) if kind == "wait" else jump(-aa, q)
                reverse = reverse @ factor
                reverse_pr = reverse_pr @ factor
                reverse_pr /= reverse_pr.sum()
                filter_bound_ratio = max(filter_bound_ratio, abs(float(reverse_pr @ b2)) / (2 * theta))
            normalized = mat / mat.sum()
            reversed_normalized = reverse / reverse.sum()
            errors["transcript_transpose"] = max(errors["transcript_transpose"], float(np.max(np.abs(normalized.T - reversed_normalized))))
            posterior_initial = float(b2 @ mat @ ones / (ones @ mat @ ones))
            posterior_reversed = float(reverse_pr @ b2)
            errors["backwards_posterior"] = max(errors["backwards_posterior"], abs(posterior_initial - posterior_reversed))
            posterior_bound_ratio = max(posterior_bound_ratio, abs(posterior_initial) / (2 * theta))
            assert abs(posterior_initial) <= 2 * theta + 1e-13
            transcript_count += 1

        alpha = 0.05
        lower_time = (1 - 2 * alpha) * math.log((1 - alpha) / alpha) / (2 * theta**4)
        cases.append({"theta": theta, "spectral_gap": gap,
                      "full_hidden_TV": hidden_tv, "squared_echo_distance": distance,
                      "available_menu_lower": visible_gap,
                      "available_menu_upper": menu_upper,
                      "active_time_lower_at_alpha_0_05": lower_time})

    # A concrete failure of substituting a post-jump command in a reversed
    # transcript. This is exactly the distinction needed in the proof.
    theta = 0.25
    before = expm(waiting(1.0, theta) * 0.4)
    after = expm(waiting(-1.0, 0.0) * 0.7)
    forward = before @ jump(1.0, theta) @ after
    correct = after @ jump(-1.0, theta) @ before
    wrong = after @ jump(-1.0, 0.0) @ before
    assert np.max(np.abs(forward.T - correct)) < 1e-15
    wrong_gap = float(np.max(np.abs(forward.T / forward.sum() - wrong / wrong.sum())))
    assert wrong_gap > 0.01
    assert max(errors.values()) < 2e-13
    assert posterior_bound_ratio <= 1 + 1e-12
    assert filter_bound_ratio <= 1 + 1e-12
    result = {
        "scope": "Executed population algebra and finite transcript checks, not finite-data confidence or physical apparatus verification.",
        "seed": 2026103001203, "theta_cases": cases,
        "finite_transcripts_checked": transcript_count,
        "maximum_residuals": errors,
        "max_initial_hidden_posterior_over_bound": posterior_bound_ratio,
        "max_filter_mean_over_bound": filter_bound_ratio,
        "max_KL_compensator_over_conservative_bound": compensator_bound_ratio,
        "wrong_post_jump_reversal_normalized_matrix_error": wrong_gap,
        "proof_only_scope": "Uniformity over all adaptive policies, stopping and infinite records follows from the analytic invariant and likelihood proofs, not enumeration of these transcripts.",
        "initializer_contract": "Entire exposed initializer records and timing are theta-independent; b seeds and hidden marks are unobserved. Independent copies if parallel specimens are used.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (ROOT / "HIDDEN_ENSEMBLE_INFORMATION_COST_CHECK_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
