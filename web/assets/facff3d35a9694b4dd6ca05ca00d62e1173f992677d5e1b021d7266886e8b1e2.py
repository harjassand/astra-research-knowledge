#!/usr/bin/env python3
"""Parameter arithmetic for the R06 cost note; not a hitting-list generator."""

def next_power(base: int, threshold: int) -> int:
    value = 1
    while value <= threshold:
        value *= base
    return value


def integral_branch(n: int, B: int) -> dict[str, int]:
    w = n + 1
    delta = 4 * w**3 * B
    M = next_power(2, B * delta)
    rho = M // 2
    d = M * rho
    E0 = 3 * M**2 * (w + M + 1)
    T0 = B * d * (d * E0 + 1)
    K = max(M, B * T0 + 2)
    tuples = (K + 1) ** 5
    dense_integer_positions = tuples * n * d**2
    return {
        "w": w,
        "Delta": delta,
        "M": M,
        "rho": rho,
        "d": d,
        "E0": E0,
        "T0": T0,
        "K": K,
        "tuples": tuples,
        "dense_integer_positions": dense_integer_positions,
    }


if __name__ == "__main__":
    result = integral_branch(1, 1)
    for key, value in result.items():
        print(f"{key}={value}")
