#!/usr/bin/env python3
"""Numerical check of the Laguerre-chaos frame asymptotic in Appendix C.

Only Python's standard library is used. This is a reproducibility check, not
part of the proof: the proof is the negative-binomial/Laplace-principle
calculation recorded in sliced_marginal_observability.md.
"""
import math


def log_frame_ratio(n: int, beta: float) -> float:
    x = beta * beta / (1.0 + beta) ** 2
    log1mx = math.log1p(-x)
    terms = []
    # The saddle is j/n=beta/2. The broad upper limit safely captures its
    # exponentially relevant neighborhood for fixed beta.
    for j in range(int((beta + 10.0) * n) + 100):
        log_p = (
            math.lgamma(n + j + 1)
            - math.lgamma(j + 1)
            - math.lgamma(n + 1)
            + j * math.log(x)
            + (n + 1) * log1mx
        )
        log_lambda = (
            math.lgamma(n + 2 * j + 1)
            - n * math.log(2.0)
            - 2 * j * math.log(2.0)
            - math.lgamma(j + 1)
            - math.lgamma(n + j + 1)
        )
        terms.append(log_p + log_lambda)
    top = max(terms)
    return top + math.log(sum(math.exp(v - top) for v in terms))


def main() -> None:
    for beta in (0.5, 1.0, 2.0, 10.0):
        target = math.log(2 * (1 + beta) / (1 + 2 * beta))
        print(f"beta={beta:g}; predicted log(frame/norm)/n={-target:.9f}")
        for n in (100, 300, 1000):
            value = log_frame_ratio(n, beta) / n
            print(f"  n={n:4d}: {value:.9f}  (difference {value + target:+.3e})")


if __name__ == "__main__":
    main()
