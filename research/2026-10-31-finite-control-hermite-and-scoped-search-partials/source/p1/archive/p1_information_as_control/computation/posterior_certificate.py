#!/usr/bin/env python3
"""Acquired posterior-curvature certificate; no hidden-feature access by design.

The numerical run verifies acquisition/frame identities and executes a scalar-
value-gradient Langevin kernel. Floating arithmetic/random generation is a
diagnostic implementation, not an outward-rounded machine certificate. See the
proof note for its rigorous oracle and finite-random-bit error budgets.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from pathlib import Path

import numpy as np


class ScalarValueOracle:
    """The algorithms below receive only this value interface and public bounds."""

    def __init__(self, H, features):
        self._H = np.asarray(H, dtype=float)
        self._features = np.asarray(features, dtype=float)
        self.n = self._H.shape[0]
        self.calls = 0
        self.dense_input_scalars = 0
        self.logcosh_evaluations = 0
        self.smallest_requested_absolute_error = math.inf

    def value(self, x, nu=0.0, bounded_error=False):
        x = np.asarray(x, dtype=float)
        singleton = x.ndim == 1
        xx = np.atleast_2d(x)
        z = xx @ self._features.T
        out = 0.5 * np.einsum("bi,ij,bj->b", xx, self._H, xx)
        out -= np.sum(np.logaddexp(z, -z) - math.log(2), axis=1)
        count = len(xx)
        self.calls += count
        self.dense_input_scalars += count * self.n
        self.logcosh_evaluations += count * len(self._features)
        if nu > 0:
            self.smallest_requested_absolute_error = min(
                self.smallest_requested_absolute_error, float(nu)
            )
        if bounded_error and nu > 0:
            # A deterministic error bounded by nu; no zero-mean assumption.
            phase = xx @ (np.arange(self.n, dtype=float) + 1.2345)
            out += nu * np.sin(12345.6789 * phase + 0.7654321)
        return float(out[0]) if singleton else out

    def ledger(self):
        return {
            "scalar_value_calls": self.calls,
            "dense_input_scalars": self.dense_input_scalars,
            "hidden_evaluator_logcosh_calls": self.logcosh_evaluations,
            "smallest_requested_absolute_error": (
                None if math.isinf(self.smallest_requested_absolute_error)
                else self.smallest_requested_absolute_error
            ),
        }


def dyadic_below(x):
    if x <= 0:
        raise ValueError("positive step required")
    return 2.0 ** math.floor(math.log2(x))


def acquire_hessian(value, n, enclosure, fourth_bound):
    h = dyadic_below(math.sqrt(2 * enclosure / (n * fourth_bound)))
    nu = enclosure * h * h / (8 * n)
    points = [np.zeros(n)]
    for i in range(n):
        x = np.zeros(n)
        x[i] = h
        points.extend([x, -x])
    pairs = list(itertools.combinations(range(n), 2))
    for i, j in pairs:
        x = np.zeros(n)
        x[i] = x[j] = h
        points.extend([x, -x])
    vals = value(np.asarray(points), nu=nu, bounded_error=True)
    diagonal = np.array([
        (vals[1 + 2 * i] + vals[2 + 2 * i] - 2 * vals[0]) / h**2
        for i in range(n)
    ])
    estimate = np.diag(diagonal)
    offset = 1 + 2 * n
    for p, (i, j) in enumerate(pairs):
        direction = (vals[offset + 2*p] + vals[offset + 2*p + 1]
                     - 2*vals[0]) / h**2
        estimate[i, j] = estimate[j, i] = (
            direction - diagonal[i] - diagonal[j]
        ) / 2
    bound = n * (fourth_bound * h**2 / 4 + 4 * nu / h**2)
    return estimate, {
        "distinct_values": len(points), "h": h, "nu": nu,
        "operator_error_bound": bound,
    }


def unit_frame(eigenvalues, ell):
    """Classical two-column rotations; F F.T=diag(c), unit columns."""
    c = np.asarray(eigenvalues, dtype=float)
    r = len(c)
    if ell == 0:
        return np.zeros((0, 0))
    if ell < r or abs(c.sum() - ell) > 1e-8:
        raise ValueError("frame trace/rank contract violated")
    F = np.zeros((r, ell))
    F[:, :r] = np.diag(np.sqrt(c))
    d = np.r_[c, np.zeros(ell-r)]
    for i in range(ell-1):
        if abs(d[i] - 1.0) <= 1e-13:
            continue
        if d[i] > 1:
            choices = np.flatnonzero(d[i+1:] < 1)
        else:
            choices = np.flatnonzero(d[i+1:] > 1)
        if not len(choices):
            raise ArithmeticError("frame balancing lost its trace invariant")
        j = i + 1 + int(choices[0])
        a, b = float(d[i]), float(d[j])
        cc = min(1.0, max(0.0, (1-b)/(a-b)))
        co, si = math.sqrt(cc), math.sqrt(1-cc)
        fi, fj = F[:, i].copy(), F[:, j].copy()
        F[:, i], F[:, j] = co*fi+si*fj, -si*fi+co*fj
        d[i], d[j] = 1.0, a+b-1.0
    return F


def sensor_design(hessian, target_curvature, sigma):
    eigen, vectors = np.linalg.eigh(hessian)
    take = eigen < target_curvature
    d = target_curvature - eigen[take]
    r = len(d)
    if not r:
        return np.zeros((0, len(eigen))), {"rank_deficit": 0, "trace_budget": 0,
                                         "reads": 0}
    S = float(sigma**2 * d.sum())
    ell = max(r, math.ceil(S))
    c = sigma**2 * d + (ell-S)/r
    F = unit_frame(c, ell)
    M = F.T @ vectors[:, take].T
    return M, {
        "rank_deficit": r,
        "trace_budget": S,
        "reads": ell,
        "eigenvector_repetition_reads": int(np.ceil(sigma**2*d).sum()),
        "row_power_error": float(np.max(abs(np.sum(M*M, axis=1)-1))),
        "frame_operator_error": float(np.linalg.norm(F@F.T-np.diag(c), 2)),
    }


def central_gradient(value, x, third_bound, norm_error):
    x = np.atleast_2d(np.asarray(x, dtype=float))
    n = x.shape[1]
    t = dyadic_below(math.sqrt(3*norm_error/(math.sqrt(n)*third_bound)))
    nu = norm_error*t/(2*math.sqrt(n))
    queries = []
    for i in range(n):
        shift = np.zeros(n)
        shift[i] = t
        queries.extend([x+shift, x-shift])
    vals = value(np.concatenate(queries), nu=nu, bounded_error=True)
    vals = vals.reshape(2*n, len(x))
    return ((vals[::2]-vals[1::2])/(2*t)).T


def logsumexp(x):
    top = float(np.max(x))
    return top + math.log(float(np.exp(x-top).sum()))


def exact_latent_reference(H, features, M, y, sigma, rng):
    """Strong ordinary baseline: enumerate all 2^m latent signs, fully charged."""
    m, n = features.shape
    signs = np.asarray(list(itertools.product([-1., 1.], repeat=m)))
    prior_linear = signs @ features
    Hinv = np.linalg.inv(H)
    prior_logits = .5*np.einsum("bi,ij,bj->b", prior_linear, Hinv, prior_linear)
    prior_probs = np.exp(prior_logits-logsumexp(prior_logits))
    chosen = rng.choice(len(signs), p=prior_probs)
    prior_x = Hinv@prior_linear[chosen] + rng.multivariate_normal(np.zeros(n), Hinv)
    G = H + M.T@M/sigma**2
    Ginv = np.linalg.inv(G)
    linear = prior_linear + y@M/sigma**2
    logits = .5*np.einsum("bi,ij,bj->b", linear, Ginv, linear)
    probs = np.exp(logits-logsumexp(logits))
    component_means = linear@Ginv
    mean = probs@component_means
    centered = component_means-mean
    covariance = Ginv + np.einsum("b,bi,bj->ij", probs, centered, centered)
    logZ = (n*.5*math.log(2*math.pi)-.5*np.linalg.slogdet(G)[1]
            -m*math.log(2)+logsumexp(logits)-.5*np.dot(y, y)/sigma**2)
    return {"latent_terms": len(signs), "log_conditional_unnormalized_integral": logZ,
            "posterior_mean": mean.tolist(), "posterior_covariance": covariance.tolist(),
            "prior_draw": prior_x.tolist()}


def normalizer_budget(n, kappa, epsilon, alpha):
    a = kappa-1
    M4 = 8*(n+1)**2
    Q = 4*(n+1)+4*a*a*(n+1)**2
    q = math.ceil(4*Q/epsilon)
    R = max(1., (16*M4/epsilon)**(1/3), math.sqrt(8*a*M4/epsilon))
    B, D = R+a*R*R/2, 1+a*R
    delta = epsilon/(8*D)
    h = min(1/kappa, delta*delta/(64*kappa*kappa*n))
    K = math.ceil(math.log(max(1., 4*math.sqrt(2*(n+1))/delta))/h)
    Ns = math.ceil(32*B*B/(epsilon*epsilon)*math.log(2*q/alpha))
    calls = 2*n*q*Ns*K+q*Ns
    return {"temperatures": q, "independent_chains_per_temperature": Ns,
            "steps_per_chain": K, "scalar_value_calls_excluding_center_and_calibration": calls,
            "log10_scalar_value_calls": math.log10(calls),
            "status": "Conservative existence bound computed; this full budget was not executed."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("posterior_results.json"))
    parser.add_argument("--skip-sampling", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()
    rng = np.random.default_rng(20261030)
    n, m = 6, 9
    Qh, _ = np.linalg.qr(rng.normal(size=(n, n)))
    Qc, _ = np.linalg.qr(rng.normal(size=(n, n)))
    left, _ = np.linalg.qr(rng.normal(size=(m, n)))
    H = Qh@np.diag([1.5, 1.8, 2., 2.2, 2.4, 2.6])@Qh.T
    features = left@np.diag(np.sqrt([4.2, 2.7, .8, .4, .2, .1]))@Qc.T
    H0 = H-features.T@features
    fourth = 2*float(np.sum(np.sum(features**2, axis=1)**2))
    oracle = ScalarValueOracle(H, features)
    enclosure, eta, sigma, guard = .002, .35, .8, .004
    estimate, cal = acquire_hessian(oracle.value, n, enclosure, fourth)
    actual_error = float(np.linalg.norm(estimate-H0, 2))
    M, design = sensor_design(estimate, eta+enclosure+guard, sigma)
    minimum = float(np.linalg.eigvalsh(H0+M.T@M/sigma**2)[0])
    assert actual_error <= cal["operator_error_bound"]*(1+1e-5)
    assert design["row_power_error"] < 1e-12
    assert design["frame_operator_error"] < 1e-12
    assert minimum >= eta+guard-1e-10
    # Random global checks are diagnostic; the proof is the sech^2 inequality.
    points = rng.normal(size=(500, n))*rng.lognormal(0, 2, size=(500, 1))
    diagnostic_min = math.inf
    for x in points:
        z = features@x
        sech2 = 1-np.tanh(z)**2
        Hess = H-features.T@(features*sech2[:, None])
        diagnostic_min = min(diagnostic_min, float(np.linalg.eigvalsh(Hess-H0)[0]))
    assert diagnostic_min > -1e-10
    # An exact latent-mixture draw makes the observation a legal fresh-state draw.
    empty = np.zeros((0, n))
    prior = exact_latent_reference(H, features, empty, np.zeros(0), sigma, rng)
    x = np.asarray(prior["prior_draw"])
    y = M@x+sigma*rng.normal(size=len(M))
    reference = exact_latent_reference(H, features, M, y, sigma, rng)
    reference.pop("prior_draw")
    uniform = n*math.ceil(sigma**2*max(0., eta-float(np.linalg.eigvalsh(H0)[0])))
    result = {
        "seed": 20261030,
        "scope": "Numerical certificate/frame validation; no empirical speedup or certified finite-bit sampler claim.",
        "dense_case": {
            "dimension": n, "hidden_components": m,
            "hessian_eigenvalues": np.linalg.eigvalsh(H0).tolist(),
            "calibration": cal, "actual_hessian_error": actual_error,
            "design": design, "certified_target_curvature": eta,
            "actual_minimum_posterior_curvature": minimum,
            "uniform_coordinate_read_baseline": uniform,
            "diagnostic_hessian_points": len(points),
            "minimum_diagnostic_envelope_eigenvalue": diagnostic_min,
            "oracle_ledger": oracle.ledger(),
            "legal_observation": y.tolist(),
            "exact_reference": reference,
            "reference_total_latent_terms": prior["latent_terms"]+reference["latent_terms"],
        }
    }
    # Stress the classical frame construction across fractional/multiple-read cases.
    worst_power = worst_operator = 0.
    for r in range(1, 9):
        for _ in range(20):
            ds = rng.lognormal(0, 2, size=r)
            S = float(ds.sum())
            ell = max(r, math.ceil(S))
            c = ds+(ell-S)/r
            F = unit_frame(c, ell)
            worst_power = max(worst_power, float(np.max(abs(np.sum(F*F, axis=0)-1))))
            worst_operator = max(worst_operator, float(np.linalg.norm(F@F.T-np.diag(c), 2)))
    result["frame_stress"] = {"cases": 160, "max_column_power_error": worst_power,
                              "max_operator_error": worst_operator}
    assert worst_power < 1e-10 and worst_operator < 1e-9

    if not args.skip_sampling:
        sn = 2
        sH = np.diag([1.6, 1.2])
        sf = np.array([[1.3, .2], [.6, .9], [.1, .25]])
        seta, ssigma = .5, .8
        so = ScalarValueOracle(sH, sf)
        sM4 = 2*float(np.sum(np.sum(sf**2, axis=1)**2))
        shat, scal = acquire_hessian(so.value, sn, enclosure, sM4)
        sM, sdesign = sensor_design(shat, seta+enclosure+guard, ssigma)
        sprior = exact_latent_reference(sH, sf, np.zeros((0, sn)), np.zeros(0), ssigma, rng)
        sx = np.asarray(sprior["prior_draw"])
        sy = sM@sx+ssigma*rng.normal(size=len(sM))
        sref = exact_latent_reference(sH, sf, sM, sy, ssigma, rng)
        sref.pop("prior_draw")
        L = 1.6+np.linalg.norm(sM, 2)**2/ssigma**2
        kappa = L/seta
        Q2 = sn*1.6-np.trace(shat)+sn*enclosure
        M3 = math.sqrt(Q2*sM4/2)

        def gradW(xx, accuracy):
            xx = np.atleast_2d(xx)
            return (central_gradient(so.value, xx, M3, accuracy)
                    +(xx@sM.T-sy)@sM/ssigma**2)

        center = np.zeros((1, sn))
        center_accuracy = seta**1.5/(4*L)
        center_steps = 0
        for center_steps in range(10000):
            gg = gradW(center, center_accuracy)
            if np.linalg.norm(gg)+center_accuracy <= math.sqrt(seta):
                break
            center -= gg/L
        else:
            raise ArithmeticError("centering failed")
        delta = 1.0
        step = min(1/kappa, delta**2/(64*kappa*kappa*sn))
        iterations = math.ceil(math.log(4*math.sqrt(2*(sn+1))/delta)/step)
        chains = 16
        zz = np.zeros((chains, sn))
        before = so.calls
        sampling_started = time.perf_counter()
        for _ in range(iterations):
            xx = center+zz/math.sqrt(seta)
            gg = gradW(xx, math.sqrt(seta)*delta/4)/math.sqrt(seta)
            zz += -step*gg+math.sqrt(2*step)*rng.normal(size=zz.shape)
        xx = center+zz/math.sqrt(seta)
        sampling_seconds = time.perf_counter()-sampling_started
        bound = (math.exp(-iterations*step)*math.sqrt(2*(sn+1))
                 +2*kappa*math.sqrt(sn*step)+delta/4)
        result["small_sampling_execution"] = {
            "dimension": sn, "calibration": scal, "design": sdesign,
            "center_iterations": center_steps,
            "center": center[0].tolist(), "condition_number_bound": kappa,
            "chains": chains, "steps_per_chain": iterations,
            "scalar_value_calls_for_sampling": so.calls-before,
            "expected_scalar_value_calls_for_sampling": 2*sn*chains*iterations,
            "ideal_random_and_arithmetic_W2_bound_in_scaled_coordinates": bound,
            "W2_target_in_scaled_coordinates": delta,
            "empirical_sample_mean_diagnostic_only": xx.mean(axis=0).tolist(),
            "exact_reference": sref, "oracle_ledger": so.ledger(),
            "sampling_seconds": sampling_seconds,
            "finite_precision_status": (
                "Value-gradient error budget is explicit; floating roundoff and NumPy "
                "Gaussian generation were not outward certified. This run is a numerical "
                "kernel check, not a machine-certified W2 guarantee."
            ),
        }
        assert so.calls-before == 2*sn*chains*iterations
        result["general_normalizer_bound_for_small_case"] = normalizer_budget(
            sn, kappa, .5, .05
        )
    result["total_seconds"] = time.perf_counter()-started
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({
        "output": str(args.output), "dense_reads": len(M),
        "dense_calibration_calls": cal["distinct_values"],
        "dense_posterior_min_curvature": minimum,
        "frame_stress_cases": 160,
        "sampling_scalar_calls": result.get("small_sampling_execution", {}).get(
            "scalar_value_calls_for_sampling"),
        "total_seconds": result["total_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
