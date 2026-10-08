#!/usr/bin/env python3
"""Exact log-scale diagnostics for the finite-volume autocatalytic SIS CRN.

Network: A+B -> 2B at beta/V; B -> A at delta; optionally A -> B
at per-A rate eta_V=exp(-alpha*V). The conserved count is A+B=V.

This uses only Python's standard library. It evaluates the exact birth-death
mean-hit-time recurrence and the exact stationary product weights in log space.
"""
from __future__ import annotations
import argparse
import math


def logadd(a: float, b: float) -> float:
    if a < b:
        a, b = b, a
    if a == -math.inf:
        return a
    return a + math.log1p(math.exp(b - a))


def log_mean_absorption(V: int, beta: float = 2.0, delta: float = 1.0,
                        initial: int | None = None) -> tuple[int, float]:
    """Return (initial state, log E_initial[tau_0]) for eta=0.

    Recurrence: D_i=E_i[tau_0]-E_{i-1}[tau_0]
    = 1/mu_i + (lambda_i/mu_i)D_{i+1}, D_{V+1}=0.
    """
    if V < 1 or beta <= delta or delta <= 0:
        raise ValueError("require V>=1 and beta>delta>0")
    if initial is None:
        initial = round(V * (1.0 - delta / beta))
    if not 1 <= initial <= V:
        raise ValueError("initial must lie in 1,...,V")

    log_d = [float("-inf")] * (V + 2)
    for i in range(V, 0, -1):
        mu = delta * i
        term = -math.log(mu)
        if i < V:
            lam = beta * i * (V - i) / V
            if lam > 0:
                term = logadd(term, math.log(lam / mu) + log_d[i + 1])
        log_d[i] = term

    log_tau = float("-inf")
    for i in range(1, initial + 1):
        log_tau = logadd(log_tau, log_d[i])
    return initial, log_tau


def stationary_summary(V: int, alpha: float, beta: float = 2.0,
                       delta: float = 1.0) -> tuple[float, float, float]:
    """For eta_V=exp(-alpha V), return (pi(0), E[I/V], modal I/V).

    Stationary weights satisfy w_0=1 and w_i/w_{i-1}=lambda_{i-1}/mu_i.
    All calculations stay in log space, including exponentially small eta_V.
    """
    if V < 1 or alpha <= 0 or beta <= delta or delta <= 0:
        raise ValueError("require V>=1, alpha>0, and beta>delta>0")
    log_eta = -alpha * V
    log_w = [0.0]
    for k in range(1, V + 1):
        remaining = V - k + 1
        log_immigration = log_eta + math.log(remaining)
        if k == 1:
            log_birth = log_immigration
        else:
            log_infection = (math.log(beta) + math.log(k - 1)
                             + math.log(remaining) - math.log(V))
            log_birth = logadd(log_infection, log_immigration)
        log_death = math.log(delta * k)
        log_w.append(log_w[-1] + log_birth - log_death)

    shift = max(log_w)
    weights = [math.exp(x - shift) for x in log_w]
    normalizer = sum(weights)
    p0 = weights[0] / normalizer
    mean = sum(i * w for i, w in enumerate(weights)) / (V * normalizer)
    mode = max(range(V + 1), key=lambda i: log_w[i]) / V
    return p0, mean, mode


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--volumes", type=int, nargs="+", default=[20, 40, 80, 160, 320, 640, 1280])
    ap.add_argument("--beta", type=float, default=2.0)
    ap.add_argument("--delta", type=float, default=1.0)
    ap.add_argument("--alpha", type=float, nargs="*", default=[],
                    help="optional exponents for eta_V=exp(-alpha*V)")
    args = ap.parse_args()
    xstar = 1.0 - args.delta / args.beta
    R0 = args.beta / args.delta
    barrier = math.log(R0) - 1.0 + 1.0 / R0
    print(f"R0={R0:.12g} x*={xstar:.12g} Delta={barrier:.12g}")
    print("no immigration: V initial log_mean_tau log_mean_tau/V gap_to_Delta")
    for V in args.volumes:
        i, log_tau = log_mean_absorption(V, args.beta, args.delta)
        print(f"{V} {i} {log_tau:.9f} {log_tau/V:.9f} {log_tau/V-barrier:.9f}")
    for alpha in args.alpha:
        print(f"immigration alpha={alpha:.12g}, eta_V=exp(-alpha V)")
        print("V pi0 E[I/V] mode(I/V)")
        for V in args.volumes:
            p0, mean, mode = stationary_summary(V, alpha, args.beta, args.delta)
            print(f"{V} {p0:.9g} {mean:.9g} {mode:.9g}")


if __name__ == "__main__":
    main()
