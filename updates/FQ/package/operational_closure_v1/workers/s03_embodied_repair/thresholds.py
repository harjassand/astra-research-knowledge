"""Hypothetical independent-cavity selectivity thresholds; no physical rates."""

from math import exp, log


def thresholds(cavities: int, frame_yield: float, matchings: int) -> tuple[float, float, float]:
    if cavities < 1 or matchings < 2 or not (0 < frame_yield < 1):
        raise ValueError("invalid hypothetical design target")
    per_cavity_yield = frame_yield ** (1 / cavities)
    max_wrong_to_correct_rate = frame_yield ** (-1 / cavities) - 1
    sufficient_energy_margin_kbt = log((matchings - 1) / max_wrong_to_correct_rate)
    return per_cavity_yield, max_wrong_to_correct_rate, sufficient_energy_margin_kbt


if __name__ == "__main__":
    n, target, m = 100, 0.9, 3
    p, rate_ratio, delta = thresholds(n, target, m)
    check_p = 1 / (1 + (m - 1) * exp(-delta))
    print(f"hypothetical cavities={n}, frame_yield={target}, matchings={m}")
    print(f"minimum per-cavity success={p:.12f}")
    print(f"maximum aggregate wrong/correct lock-rate ratio={rate_ratio:.12f}")
    print(f"sufficient equilibrium Delta/kBT={delta:.12f}")
    print(f"check per-cavity lower bound={check_p:.12f}")
    print(f"check independent-frame lower bound={check_p ** n:.12f}")
