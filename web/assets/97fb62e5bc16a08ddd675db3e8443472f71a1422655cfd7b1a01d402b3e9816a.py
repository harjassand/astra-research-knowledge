#!/usr/bin/env python3
"""Finite arithmetic checks for the occupation-cap formulas in RESULT.txt."""

from math import comb


def layer_size(s: int, d: int) -> int:
    return comb(s + d - 1, d - 1)


def check() -> None:
    cases = 0
    for d in range(1, 8):
        for R in range(20):
            g = lambda s: layer_size(s, d)
            z = sum(g(s) * (R + 1 - s) ** 2 for s in range(R + 1))
            z_closed = comb(R + d + 2, d + 2) + comb(R + d + 1, d + 2)
            assert z == z_closed, (d, R, z, z_closed)

            rank = sum(g(s) for s in range(R + 1))
            assert rank == comb(R + d, d), (d, R, rank)

            for N in range(R, R + 8):
                w = sum((N - s) * (s + d) * g(s) for s in range(R + 1))
                w_closed = (
                    N * d * comb(R + d + 1, d + 1)
                    - d * (d + 1) * comb(R + d + 1, d + 2)
                )
                assert w == w_closed, (d, R, N, w, w_closed)
                cases += 1

    print(
        "Exact integer identities passed for d=1..7, R=0..19, "
        f"N=R..R+7 ({cases} energy-sum cases)."
    )
    print("These checks verify the displayed binomial sums only; they are not a proof of the representation decomposition or theorem.")


if __name__ == "__main__":
    check()
