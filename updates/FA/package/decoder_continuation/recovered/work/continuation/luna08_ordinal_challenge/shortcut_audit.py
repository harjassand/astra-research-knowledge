"""Independent exact check of the deterministic translation shortcut.

The triangular cases use the Sol03 teacher only as a query oracle.  All
subspace, interpolation, candidate-order and equality-witness logic below is
implemented locally.  The final four-bit case is a partial-flag counterexample
to extending the shortcut beyond a complete triangular flag.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOL03 = ROOT / "work/continuation/sol03_learning/ordinal_flag.py"
spec = importlib.util.spec_from_file_location("ordinal_flag", SOL03)
ordinal = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ordinal
spec.loader.exec_module(ordinal)


def rank_rows(rows, n):
    a = [r for r in rows if r]
    pivots = []
    row = 0
    for col in range(n):
        p = next((p for p in range(row, len(a)) if (a[p] >> col) & 1), None)
        if p is None:
            continue
        a[row], a[p] = a[p], a[row]
        for r in range(len(a)):
            if r != row and ((a[r] >> col) & 1):
                a[r] ^= a[row]
        pivots.append(col)
        row += 1
        if row == len(a):
            break
    return a[:row], pivots


def nullspace(rows, n):
    reduced, pivots = rank_rows(rows, n)
    out = []
    for free in range(n):
        if free in pivots:
            continue
        v = 1 << free
        for i, p in enumerate(pivots):
            if (reduced[i] >> free) & 1:
                v |= 1 << p
        out.append(v)
    return out


def combine(basis, mask):
    value = 0
    for i, v in enumerate(basis):
        if (mask >> i) & 1:
            value ^= v
    return value


def prefix_stabilizer(quadratics, n):
    """Basis of directions preserving all acquired coordinates pointwise."""
    radical = nullspace([r for q in quadratics for r in q.polar()], n)
    response_rows = []
    for q in quadratics:
        response_rows.append(sum((q(v) ^ q.constant) << i
                                 for i, v in enumerate(radical)))
    coefficients = nullspace(response_rows, len(radical))
    return [combine(radical, mask) for mask in coefficients]


def interpolation_candidate(v, n, query, points):
    values = {x: int(not query(x, x ^ v)) for x in points}
    return ordinal.interpolate(values, n)


def equal_value_witness(a, b, n):
    """Find x with a(x)=b(x), using balancedness of a+b and its polar."""
    d = ordinal.Quadratic(a.constant ^ b.constant,
                          a.linear ^ b.linear,
                          [x ^ y for x, y in zip(a.upper, b.upper)])
    if d(0) == 0:
        return 0
    radical = nullspace(d.polar(), n)
    for v in radical:
        if (d(v) ^ d.constant) == 1:
            assert d(v) == 0
            return v
    raise AssertionError("balanced quadratic had no radical direction changing its value")


def compare_candidates(a, va, b, vb, n, query):
    if a.body() == b.body():
        return 0
    x = equal_value_witness(a, b, n)
    assert a(x) == b(x)
    answer = query(x ^ va, x ^ vb)
    # If a's coordinate is lexicographically earlier, the queried order bit
    # equals the common coordinate bit; if b is earlier, it is its complement.
    return -1 if answer == a(x) else 1


def acquire_by_translations(n, query):
    points = ordinal.coefficient_points(n)
    learned = []
    per_stage = []
    for k in range(n):
        basis = prefix_stabilizer(learned, n)
        assert len(basis) == n - k
        candidates = []
        for v in basis:
            q = interpolation_candidate(v, n, query, points)
            if not any(q.body() == old[0].body() for old in candidates):
                candidates.append((q, v))
        best_q, best_v = candidates[0]
        tournament_queries = 0
        for q, v in candidates[1:]:
            order = compare_candidates(best_q, best_v, q, v, n, query)
            tournament_queries += 1
            if order > 0:
                best_q, best_v = q, v
        learned.append(best_q)
        per_stage.append({"stage": k, "stabilizer_dimension": len(basis),
                          "distinct_candidate_coordinates": len(candidates),
                          "candidate_queries": len(basis) * len(points),
                          "tournament_queries": tournament_queries,
                          "selected_witness": best_v})
    return learned, per_stage


def test_triangular(n, seed):
    teacher = ordinal.TriangularTeacher(n, seed)
    calls_start = teacher.calls
    learned, stages = acquire_by_translations(n, teacher.query)
    truth = [ordinal.interpolate(
        {x: (teacher.rank(x) >> (n - j - 1)) & 1
         for x in ordinal.coefficient_points(n)}, n)
        for j in range(n)]
    exact = [a.body() == b.body() for a, b in zip(learned, truth)]
    rank_errors = sum(ordinal.learned_rank(learned, x) != teacher.rank(x)
                      for x in range(1 << n))
    assert all(exact) and rank_errors == 0
    toggles = [s["selected_witness"] for s in stages]
    inverse_checks = 0
    for target in range(1 << n):
        x = 0
        for j, (q, v) in enumerate(zip(learned, toggles)):
            desired = (target >> (n - j - 1)) & 1
            if q(x) != desired:
                x ^= v
        assert ordinal.learned_rank(learned, x) == target
        assert teacher.rank(x) == target
        inverse_checks += 1
    prefix_laws = []
    for bits in range(n + 1):
        target_prefix = (1 << bits) - 1
        counts = {}
        for original in range(1 << n):
            x = original
            for j in range(bits):
                desired = (target_prefix >> (bits - j - 1)) & 1
                if learned[j](x) != desired:
                    x ^= toggles[j]
            counts[x] = counts.get(x, 0) + 1
            assert ordinal.learned_rank(learned, x) >> (n - bits) == target_prefix
        assert len(counts) == 1 << (n - bits)
        assert set(counts.values()) == {1 << bits}
        prefix_laws.append({"prefix_bits": bits, "fiber_points": len(counts),
                            "preimages_per_fiber_point": 1 << bits})
    assert teacher.calls - calls_start == sum(
        s["candidate_queries"] + s["tournament_queries"] for s in stages)
    return {"n": n, "seed": seed, "exact_coordinate_bodies": exact,
            "exhaustive_rank_points": 1 << n, "rank_errors": rank_errors,
            "comparison_calls": teacher.calls - calls_start,
            "analytic_upper_bound": (len(ordinal.coefficient_points(n)) * n * (n + 1) // 2
                                     + n * (n - 1) // 2),
            "inverse_targets_checked": inverse_checks,
            "exact_prefix_projection_laws": prefix_laws,
            "stages": stages}


def partial_flag_counterexample():
    n = 4
    q = [ordinal.Quadratic(0, 1, [0, 0, 8, 0]),
         ordinal.Quadratic(0, 2, [0, 0, 8, 0]),
         ordinal.Quadratic(0, 4, [0] * n),
         ordinal.Quadratic(0, 8, [0] * n)]
    ranks = [ordinal.learned_rank(q, x) for x in range(1 << n)]
    assert len(set(ranks)) == 1 << n
    flag_gates = [True, True, False]
    def query(x, y):
        return ordinal.learned_rank(q, x) < ordinal.learned_rank(q, y)
    v = 1 << 2
    f = interpolation_candidate(v, n, query, ordinal.coefficient_points(n))
    bodies = [item.body() for item in q]
    assert f.body() == {"constant": 0, "linear": 4, "upper": [8, 0, 0, 0]}
    assert f.body() not in bodies
    values = [int(not query(x, x ^ v)) for x in range(1 << n)]
    return {"quadratics": bodies, "bijection_exact": True,
            "first_three_flag_gates": flag_gates,
            "translation": v, "candidate_body": f.body(),
            "candidate_is_any_coordinate": False,
            "candidate_truth_table": values,
            "meaning": "A partial flag does not make every direction in F2^n a single-coordinate toggle."}


def main():
    cases = [test_triangular(n, 88000 + 31 * n + seed)
             for n in range(2, 9) for seed in range(3)]
    partial = partial_flag_counterexample()
    result = {"status": "exact_small_audit",
              "triangular_cases": cases,
              "triangular_case_count": len(cases),
              "triangular_all_exact": all(all(c["exact_coordinate_bodies"])
                                           and c["rank_errors"] == 0 for c in cases),
              "partial_flag_counterexample": partial,
              "proof_scope": "The tested shortcut assumes a complete flag / hidden-affine triangular quadratic map."}
    dest = Path(__file__).with_name("shortcut_audit.json")
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"],
                      "triangular_case_count": len(cases),
                      "all_exact": result["triangular_all_exact"],
                      "max_n": max(c["n"] for c in cases),
                      "partial_candidate": partial["candidate_body"]}, indent=2))


if __name__ == "__main__":
    main()
