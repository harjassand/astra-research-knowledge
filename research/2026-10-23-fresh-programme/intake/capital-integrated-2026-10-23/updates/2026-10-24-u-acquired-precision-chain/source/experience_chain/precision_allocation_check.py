"""Exact identities and bounded numerical falsification of the allocation note."""
from fractions import Fraction as F
import json
from pathlib import Path
import math
import numpy as np


def exact_checks():
    # A=9, B=4, T=16 gives square roots 3, 8 and sqrt(TAB)=24.
    A, B, T, e = F(9), F(4), 16, F(1, 25)
    E, m = F(33) / e, F(11, 2) / e
    assert A / E + B / m == e
    assert E + T * m == F(121) / e
    assert sum(A * B / (e * E - A) ** 2 for _ in range(T)) == 1
    # A strict convex derivative zero proves the unique minimum, without grids.
    assert -1 + sum(A * B / (e * (E / 2) - A) ** 2 for _ in range(T)) > 0
    assert -1 + sum(A * B / (e * (2 * E) - A) ** 2 for _ in range(T)) < 0

    bo, bn, de, Bt, et = F(1, 100), F(1, 400), F(100), F(2), F(1, 25)
    threshold = de * (et - bo) * (et - bn) / (Bt * (bo - bn))
    assert threshold == F(15, 2)
    saving = Bt / (et - bo) - Bt / (et - bn)
    assert threshold * saving == de
    return {"E_star": str(E), "m_star": str(m), "minimum_cost": str(E + T*m),
            "break_even_task_count": str(threshold)}


def prefix_optimum(A, e, B):
    boundary = float(np.max(A / e))
    low = np.nextafter(boundary, math.inf)
    high = max(1.0, 2 * boundary)
    def left(x):
        return float(np.sum(A * B / (e * x - A) ** 2))
    while left(high) > 1:
        high *= 2
    for _ in range(110):
        mid = (low + high) / 2
        if left(mid) > 1:
            low = mid
        else:
            high = mid
    E = (low + high) / 2
    rents = B * E / (e * E - A)
    return E, float(E + np.sum(rents)), left(E)


def chain_check(name, eps, B, A=7.0):
    e = np.asarray(eps, float) ** 2
    B = np.asarray(B, float)
    previous = 0.0
    rent = rent_grid = 0.0
    maximum_ratio = maximum_grid_ratio = 0.0
    max_derivative_residual = 0.0
    rows = []
    for t in range(1, len(e) + 1):
        E, Fopt, derivative = prefix_optimum(A, e[:t], B[:t])
        assert E >= previous * (1 - 2e-13)
        previous = E
        rent += B[t-1] * E / (e[t-1] * E - A)
        # For this check the grid has a sufficiently small initial level.
        Egrid = 2.0 ** math.ceil(math.log2(E))
        assert Egrid >= E and Egrid <= 2 * E * (1 + 1e-13)
        rent_grid += B[t-1] * Egrid / (e[t-1] * Egrid - A)
        actual, grid_actual = E + rent, Egrid + rent_grid
        assert rent <= Fopt * (1 + 3e-13)
        assert actual <= 2 * Fopt * (1 + 3e-13)
        assert grid_actual <= 3 * Fopt * (1 + 3e-13)
        maximum_ratio = max(maximum_ratio, actual / Fopt)
        maximum_grid_ratio = max(maximum_grid_ratio, grid_actual / Fopt)
        max_derivative_residual = max(max_derivative_residual, abs(derivative - 1))
        rows.append({"t":t, "E":E, "offline_cost":Fopt, "online_cost":actual,
                     "doubling_cost":grid_actual})
    return {"name":name, "tasks":len(e), "max_online_ratio":maximum_ratio,
            "max_doubling_ratio":maximum_grid_ratio,
            "max_derivative_residual":max_derivative_residual,
            "final":rows[-1]}


def main():
    rng = np.random.default_rng(20261024)
    results = [
        chain_check("same_precision", np.full(128, .1), np.ones(128)),
        chain_check("increasing_precision", np.repeat([.2,.1,.05,.025],32),
                    np.linspace(1,3,128)),
        chain_check("nonmonotone_requests", rng.uniform(.04,.25,128),
                    rng.uniform(.2,4,128)),
    ]
    out = {"status":"PASS", "exact":exact_checks(), "chains":results,
           "scope":"Conditional exposure-envelope allocation, not an acquired-envelope claim."}
    target = Path(__file__).with_suffix(".json")
    target.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__ == "__main__":
    main()
