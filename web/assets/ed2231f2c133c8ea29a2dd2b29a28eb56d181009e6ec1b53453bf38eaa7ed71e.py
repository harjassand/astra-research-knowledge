"""Recompute the quadratic field-suppression slopes from preprint Table S1."""

import numpy as np


TABLE = {
    "2ML": ([0, 28, 33, 40], [133.28, 132.9, 132.3, 131.7]),
    "3ML": ([0, 40, 50, 60, 70], [134.3, 133.3, 131.4, 130.2, 129.4]),
    "6ML": (
        [0, 55, 61, 66, 69, 72, 75, 80],
        [139.22, 137.78, 136.68, 135.9, 135.22, 134.7, 134.2, 132.2],
    ),
}


def fit(label, fields_mT, transition_K):
    fields = np.asarray(fields_mT, dtype=float)
    temps = np.asarray(transition_K, dtype=float)
    slope, intercept = np.polyfit(fields**2, temps, 1)
    fitted = intercept + slope * fields**2
    r2 = 1 - np.sum((temps - fitted) ** 2) / np.sum((temps - temps.mean()) ** 2)
    return {"sample": label, "slope_K_per_mT2": slope, "intercept_K": intercept, "R2": r2}


if __name__ == "__main__":
    for name, (fields, temperatures) in TABLE.items():
        print(fit(name, fields, temperatures))
