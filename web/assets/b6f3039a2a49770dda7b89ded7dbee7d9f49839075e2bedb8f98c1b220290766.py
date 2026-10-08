#!/usr/bin/env python3
"""Exact-integer checks of the SU(2) weight/multiplicity counting identity."""
import json


def coefficients(cap: int, V: int) -> list[int]:
    # Coefficients of (1+z+...+z^cap)^V.
    out = [1]
    for _ in range(V):
        nxt = [0] * (len(out) + cap)
        for i, value in enumerate(out):
            for j in range(cap + 1):
                nxt[i + j] += value
        out = nxt
    return out


def check(twoS: int, V: int) -> dict:
    if twoS <= 0 or V <= 0 or V % 2:
        raise ValueError("require positive integer 2S and even V")
    maxJ = (twoS * V) // 2
    a = coefficients(twoS, V)
    multiplicities = [a[d] - (a[d - 1] if d else 0) for d in range(maxJ + 1)]
    nonnegative = all(g >= 0 for g in multiplicities)
    reconstructed_dimension = sum(
        multiplicities[d] * (2 * (maxJ - d) + 1)
        for d in range(maxJ + 1)
    )
    exact_dimension = (twoS + 1) ** V
    return {
        "2S": twoS,
        "V": V,
        "max_total_spin_SV": maxJ,
        "multiplicities_nonnegative": nonnegative,
        "reconstructed_Hilbert_dimension": reconstructed_dimension,
        "exact_Hilbert_dimension": exact_dimension,
        "dimension_identity_pass": reconstructed_dimension == exact_dimension,
    }


def main() -> None:
    rows = [check(twoS, V) for twoS in (1, 2, 3) for V in (2, 4, 8)]
    print(json.dumps({"rows": rows,
                      "status": "PASS" if all(r["multiplicities_nonnegative"] and r["dimension_identity_pass"] for r in rows) else "FAIL"}, indent=2))


if __name__ == "__main__":
    main()
