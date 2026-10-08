#!/usr/bin/env python3
"""Exact one-magnon lower bound on non-ground thermal weight.

In the M^3=SV-1 sector of the periodic weighted Heisenberg ferromagnet, the
Hamiltonian is S times the weighted graph Laplacian.  The k=0 mode belongs to
the ground multiplet; all nonzero momenta give spin SV-1 multiplets.  Their
contribution lower-bounds Z_excited/Z_ground.
"""
import argparse
import json
import math


def one_magnon_bound(L: int, S: float, J: tuple[float, float, float], beta: float) -> dict:
    if L < 4 or L % 2:
        raise ValueError("L must be even and at least 4")
    if S <= 0 or min(J) <= 0 or beta <= 0:
        raise ValueError("S, all couplings, and beta must be positive")
    V = L**3
    Jmaxspin = S * V
    if Jmaxspin < 1:
        raise ValueError("need SV>=1 for a d=1 spin sector")
    ratio = (2 * Jmaxspin - 1) / (2 * Jmaxspin + 1)
    terms = []
    for k0 in range(L):
        for k1 in range(L):
            for k2 in range(L):
                if (k0, k1, k2) == (0, 0, 0):
                    continue
                ks = (k0, k1, k2)
                energy = 2 * S * sum(
                    J[i] * (1 - math.cos(2 * math.pi * ks[i] / L))
                    for i in range(3)
                )
                terms.append(math.exp(-beta * energy))
    ratio_lower = ratio * sum(terms)
    return {
        "L": L,
        "V": V,
        "S": S,
        "J": list(J),
        "beta": beta,
        "one_magnon_modes": len(terms),
        "multiplet_to_ground_degeneracy_ratio": ratio,
        "Z_exc_over_Z_ground_lower_bound_from_one_magnons": ratio_lower,
        "ground_probability_upper_bound": 1 / (1 + ratio_lower),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=int, default=8)
    parser.add_argument("--S", type=float, default=0.5)
    parser.add_argument("--J", type=float, nargs=3, default=(1.0, 1.0, 1.0))
    parser.add_argument("--beta", type=float, default=1.0)
    args = parser.parse_args()
    print(json.dumps(one_magnon_bound(args.L, args.S, tuple(args.J), args.beta), indent=2))


if __name__ == "__main__":
    main()
