"""Conditional competing-hazard selectivity threshold; no experimental rates."""

from math import prod


def exact_clean_repair_probability(defects: int, intact: int, repair_to_harm: float) -> float:
    """All defects repair before any harm, under independent constant hazards."""
    return prod(
        j * repair_to_harm / (j * repair_to_harm + intact)
        for j in range(1, defects + 1)
    )


def threshold(defects: int, intact: int, target: float) -> float:
    low, high = 0.0, 1.0
    while exact_clean_repair_probability(defects, intact, high) < target:
        high *= 2
    for _ in range(100):
        midpoint = (low + high) / 2
        if exact_clean_repair_probability(defects, intact, midpoint) < target:
            low = midpoint
        else:
            high = midpoint
    return high


if __name__ == "__main__":
    for defects in (1, 9):
        ratio = threshold(defects, 100, 0.9)
        print(f"K={defects} N=100 target=0.9 a/b={ratio:.9f} "
              f"P={exact_clean_repair_probability(defects, 100, ratio):.9f}")
