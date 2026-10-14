#!/usr/bin/env python3
"""Float prototype of the root source-leaf control variate."""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np

from nonlinear_query_reference import base_and_residual, certificate


def sample_with_root_control(x, n, seed, h, R, rate, B2, B3, B4):
    np.random.seed(seed)
    zvals = np.empty(n)
    root_controls = np.zeros(n)
    nodes = np.empty(n, dtype=np.int64)
    p0 = R / (rate * h)
    p2, p3, p4 = B2 * h / rate, B3 * h * h / rate, B4 * h**3 / rate
    max_nodes = 0
    for sample in range(n):
        pending = [x]
        weight = 1.0
        count = 0
        root_control = 0.0
        while len(pending):
            xx = pending.pop()
            tau = np.random.exponential(1.0 / rate)
            y = (xx + math.sqrt(2.0 * tau) * np.random.normal()) % (2.0 * math.pi)
            v, residual = base_and_residual(y, 1)
            tangent = 1.0 + 100.0 * v**3
            p1_local = 1.0 - tangent / rate
            total = p0 + p1_local + p2 + p3 + p4
            if p1_local < -1.e-12 or total > 1.0 + 1.e-12:
                raise ValueError("local probabilities violate supplied certificate")
            draw = np.random.random()
            count += 1
            if draw < p0:
                leaf = residual / R
                weight *= leaf
                if count == 1:
                    root_control = leaf
            elif draw < p0 + p1_local:
                pending.append(y)
            elif draw < p0 + p1_local + p2:
                weight *= -(150.0 * v * v) / B2
                pending.append(y)
                pending.append(y)
            elif draw < p0 + p1_local + p2 + p3:
                weight *= -(100.0 * v) / B3
                pending.append(y)
                pending.append(y)
                pending.append(y)
            elif draw < total:
                weight *= -25.0 / B4
                pending.append(y)
                pending.append(y)
                pending.append(y)
                pending.append(y)
            else:
                weight = 0.0
                break
        zvals[sample] = weight
        root_controls[sample] = root_control
        nodes[sample] = count
        if count > max_nodes:
            max_nodes = count
    return zvals, root_controls, nodes, max_nodes


def q_at_x_from_receipt(x: float) -> float:
    receipt = json.loads(Path(__file__).with_name("source_control_certificate.json").read_text())
    coeffs = receipt["weak_source_control"]["fourier_coefficients"]
    return math.fsum(
        (entry["real"]["numerator"] / entry["real"]["denominator"]) * math.cos(entry["k"] * x)
        - (entry["imag"]["numerator"] / entry["imag"]["denominator"]) * math.sin(entry["k"] * x)
        for entry in coeffs)


def main():
    n = 200_000
    x = 0.5
    h = 0.011
    cert = certificate(1)
    start = time.perf_counter()
    z, c, nodes, max_nodes = sample_with_root_control(
        x, n, 20261015, h, cert.residual_bound,
        cert.proposal_rate, cert.b2, cert.b3, cert.b4)
    seconds = time.perf_counter() - start
    w = z - c
    v, _ = base_and_residual(x, 1)
    q = q_at_x_from_receipt(x)
    old_est = v + h * float(np.mean(z))
    new_est = v + q + h * float(np.mean(w))
    p0 = cert.residual_bound / (cert.proposal_rate * h)
    result = {
        "samples": n,
        "seed": 20261015,
        "target_x": x,
        "compile_seconds_excluded": True,
        "sample_seconds": seconds,
        "tree_nodes_mean": float(np.mean(nodes)),
        "tree_nodes_max": int(max_nodes),
        "root_source_probability_theory": p0,
        "root_source_probability_observed": float(np.mean(c != 0.0)),
        "q_lambda_at_x_float": q,
        "q_over_h": q / h,
        "root_control_mean": float(np.mean(c)),
        "ordinary_normalized_variance": float(np.var(z, ddof=1)),
        "controlled_normalized_variance": float(np.var(w, ddof=1)),
        "controlled_to_ordinary_variance_ratio": float(np.var(w, ddof=1) / np.var(z, ddof=1)),
        "ordinary_standard_error": float(h * np.std(z, ddof=1) / math.sqrt(n)),
        "controlled_standard_error": float(h * np.std(w, ddof=1) / math.sqrt(n)),
        "ordinary_estimate": old_est,
        "controlled_estimate": new_est,
        "paired_difference_due_to_C": new_est - old_est,
        "numerical_fft_reference_from_source": 1.0208709917983396,
        "scope": "Floating-point ideal-law replay only; this does not interval-validate the source or transcendental control evaluation.",
    }
    Path(__file__).with_name("source_control_run.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
