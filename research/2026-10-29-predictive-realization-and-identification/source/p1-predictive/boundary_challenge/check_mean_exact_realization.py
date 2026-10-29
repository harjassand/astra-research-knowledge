#!/usr/bin/env python3
"""Independent exact controls of root's mean-exact positive realization."""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import time

from check_passive_equivalence import (
    F, sp, matrix_block, laplacian, record, killed_mean, passive_mean, encode,
)


def realize(S, b, c, wb):
    m = len(wb)
    assert S.rows == S.cols == m and len(b) == m
    assert S == S.T and S * sp.ones(m, 1) == sp.zeros(m, 1)
    assert all(wi > 0 for wi in wb)
    v = b - wb
    assert all(x >= 0 for x in v)
    V = sum(v)
    assert (V == 0 and c == 0) or (V > 0 and c > 0)
    gamma = V / c if V else None
    edges = []
    for i in range(m):
        for j in range(i + 1, m):
            assert S[i, j] <= 0
            if S[i, j]:
                edges.append((i, j, -S[i, j]))
    masses = list(wb)
    for i in range(m):
        if v[i]:
            leaf = len(masses)
            masses.append(v[i])
            edges.append((i, leaf, gamma * v[i]))
    L = laplacian(len(masses), edges)
    w = sp.Matrix(masses)
    assert len(w) <= 2 * m
    return L, w, gamma


def ground_mean(L, w, B, hazards):
    A = L.copy()
    for i, kappa in zip(B, hazards):
        A[i, i] += w[i] * kappa
    h = A.inv() * w
    return (w.T * h)[0] / sum(w)


def killing_field(L, w, target):
    live = [i for i in range(len(w)) if i not in target]
    wc = matrix_block(w, live, [0])
    A = matrix_block(L, live, live)
    h = A.inv() * wc
    assert A * h == wc
    return {i: h[j] for j, i in enumerate(live)}


def assemble(modules, cross):
    offsets = []
    total = 0
    for L, w in modules:
        offsets.append(total)
        total += len(w)
    Lg, wg = sp.zeros(total), sp.zeros(total, 1)
    for off, (L, w) in zip(offsets, modules):
        n = len(w)
        Lg[off:off + n, off:off + n] = L
        wg[off:off + n, 0] = w
    for (j, p), (k, q), g in cross:
        u, v = offsets[j] + p, offsets[k] + q
        Lg[u, u] += g
        Lg[v, v] += g
        Lg[u, v] -= g
        Lg[v, u] -= g
    return Lg, wg, offsets


def main():
    start = time.perf_counter()
    cases = []
    subset_checks = boundary_start_checks = hazard_checks = passive_checks = 0
    # Dense internal mixing and varying port counts; n=port count+7.
    originals = []
    for m in [1, 2, 3, 4, 5]:
        n = m + 7
        edges = [(i, i + 1, F(i + 1, m + 2)) for i in range(n - 1)]
        edges += [(0, n - 1, F(2, 5)), (1, n - 2, F(3, 7)), (2, n - 3, F(5, 11))]
        L = laplacian(n, edges)
        w = sp.Matrix([F(2 * i + 1, n + 1) for i in range(n)])
        originals.append((L, w, list(range(m))))
    # c=V=0 corner; no private leaves should be introduced.
    originals.append((laplacian(3, [(0, 1, 1), (1, 2, F(2, 3))]), sp.Matrix([1, 2, 3]), [0, 1, 2]))
    # Some v_i=0: only the third port owns interior mass.
    originals.append((laplacian(4, [(0, 1, 1), (1, 2, 1), (2, 3, F(1, 2))]), sp.Matrix([1, 1, 1, 2]), [0, 1, 2]))

    for L, w, B in originals:
        m = len(B)
        S, b, c, mu, _ = record(L, w, B)
        wb = matrix_block(w, B, [0])
        Lh, wh, gamma = realize(S, b, c, wb)
        Sh, bh, ch, muh, _ = record(Lh, wh, list(range(m)))
        assert (Sh, bh, ch, muh) == (S, b, c, mu)
        assert matrix_block(wh, range(m), [0]) == wb
        for size in range(1, m + 1):
            for positions in itertools.combinations(range(m), size):
                target = {B[i] for i in positions}
                target_h = set(positions)
                if len(target) == len(w):
                    continue
                assert killed_mean(L, w, target) == killed_mean(Lh, wh, target_h)
                subset_checks += 1
                f = killing_field(L, w, target)
                fh = killing_field(Lh, wh, target_h)
                for i in range(m):
                    if i not in target_h:
                        assert f[B[i]] == fh[i]
                        boundary_start_checks += 1
        for scale in [F(1, 5), F(1), F(7, 3)]:
            hazards = [scale * (i + 1) for i in range(m)]
            assert ground_mean(L, w, B, hazards) == ground_mean(Lh, wh, list(range(m)), hazards)
            hazard_checks += 1
        for t in [F(1, 3), F(2)]:
            z = [F(i + 1, 4) for i in range(m)]
            g = [F(i + 2, 3) for i in range(m)]
            assert passive_mean(L, w, B, t, z, g) == passive_mean(Lh, wh, list(range(m)), t, z, g)
            passive_checks += 1
        original_exit = [L[i, i] / w[i] for i in B]
        replaced_exit = [Lh[i, i] / wh[i] for i in range(m)]
        cases.append({"original_states": len(w), "ports": m, "realized_states": len(wh), "gamma": gamma, "v": b - wb, "original_port_exit_rates": original_exit, "realized_port_exit_rates": replaced_exit, "port_exit_rates_preserved": original_exit == replaced_exit})

    # Memory is deliberately not preserved.
    L = laplacian(3, [(0, 1, 1), (0, 2, F(1, 3))])
    w = sp.Matrix([1, F(1, 2), F(1, 2)])
    S, b, c, _, _ = record(L, w, [0])
    Lh, wh, _ = realize(S, b, c, sp.Matrix([1]))
    second_moments = []
    for LL, ww in [(L, w), (Lh, wh)]:
        A = LL.copy()
        A[0, 0] += 1
        h = A.inv() * ww
        D = sp.diag(*list(ww))
        second_moments.append(2 * (h.T * D * h)[0] / sum(ww))
    assert second_moments == [F(53, 4), F(13)]

    # Exact worst-case family and its strict rank-forcing inequalities.
    sharpness = []
    for m in range(1, 7):
        epsilon = F(1, 2 * m * (m - 1)) if m > 1 else None
        S = laplacian(m, [(i, j, epsilon) for i in range(m) for j in range(i + 1, m)])
        wb, v, c = sp.ones(m, 1), sp.ones(m, 1), F(m)
        L, w, gamma = realize(S, wb + v, c, wb)
        assert len(w) == 2 * m and gamma == 1
        I, B = list(range(m, 2 * m)), list(range(m))
        J = matrix_block(L, I, B)
        G = matrix_block(L, I, I)
        C = J.T * G.inv() * J
        assert C == sp.eye(m)
        margins = []
        for i in range(m):
            margin = v[i] * v[i] / c - sum(-S[i, j] for j in range(m) if j != i)
            assert margin > 0
            margins.append(margin)
        sharpness.append({"ports": m, "required_hidden_states_at_least": m, "constructed_total_states": len(w), "S_edge_conductance": epsilon, "rank_forcing_margins": margins})

    # Four modules: preserve actual means between all disjoint nonempty unions.
    original_modules, compiled_modules, records = [], [], []
    for j in range(4):
        edges = [(0, 2, F(j + 2, 3)), (2, 3, F(j + 1, 5)), (3, 4, F(j + 3, 7)), (4, 1, F(j + 1, 2)), (0, 1, F(1, j + 6)), (2, 4, F(2, j + 7))]
        L = laplacian(5, edges)
        w = sp.Matrix([F(j + i + 1, 7) for i in range(5)])
        S, b, c, mu, _ = record(L, w, [0, 1])
        Lh, wh, _ = realize(S, b, c, sp.Matrix([w[0], w[1]]))
        original_modules.append((L, w))
        compiled_modules.append((Lh, wh))
        records.append((S, b, c, mu))
    cross = [((j, 1), ((j + 1) % 4, 0), F(j + 1, 11)) for j in range(4)]
    cross += [((0, 0), (2, 1), F(1, 9)), ((1, 1), (3, 0), F(2, 13))]
    Lg, wg, offsets = assemble(original_modules, cross)
    Lgh, wgh, offsetsh = assemble(compiled_modules, cross)
    directional = []
    all_live_checks = 0
    for target_size in range(1, 4):
        for target_modules in itertools.combinations(range(4), target_size):
            target = {offsets[j] + k for j in target_modules for k in range(len(original_modules[j][1]))}
            target_h = {offsetsh[j] + k for j in target_modules for k in range(len(compiled_modules[j][1]))}
            field = killing_field(Lg, wg, target)
            field_h = killing_field(Lgh, wgh, target_h)
            assert killed_mean(Lg, wg, target) == killed_mean(Lgh, wgh, target_h)
            all_live_checks += 1
            live_modules = [j for j in range(4) if j not in target_modules]
            for source_size in range(1, len(live_modules) + 1):
                for source_modules in itertools.combinations(live_modules, source_size):
                    source = [offsets[j] + k for j in source_modules for k in range(len(original_modules[j][1]))]
                    source_h = [offsetsh[j] + k for j in source_modules for k in range(len(compiled_modules[j][1]))]
                    truth = sum(wg[i] * field[i] for i in source) / sum(wg[i] for i in source)
                    replacement = sum(wgh[i] * field_h[i] for i in source_h) / sum(wgh[i] for i in source_h)
                    numerator = F(0)
                    source_mass = F(0)
                    for j in source_modules:
                        S, b, c, mu = records[j]
                        numerator += c + sum(b[p] * field[offsets[j] + p] for p in [0, 1])
                        source_mass += mu
                    compiled_formula = numerator / source_mass
                    assert truth == replacement == compiled_formula
                    directional.append({"source_modules": list(source_modules), "target_modules": list(target_modules), "mean": truth})
    assert len(directional) == 50 and all_live_checks == 14
    result = {
        "status": "PASS",
        "scope": "independent exact supplied-record realization and finite macro-transition controls",
        "arithmetic": "fractions.Fraction; no floating assertions",
        "source_observations": 0,
        "physical_preparations": 0,
        "record_and_realization_cases": cases,
        "boundary_target_mean_checks": subset_checks,
        "boundary_start_mean_checks": boundary_start_checks,
        "native_hazard_checks": hazard_checks,
        "passive_attachment_checks": passive_checks,
        "unpreserved_second_moments_original_then_realized": second_moments,
        "worst_case_state_count_family": sharpness,
        "macro_original_states": len(wg),
        "macro_realized_states": len(wgh),
        "macro_equilibrium_outside_target_checks": all_live_checks,
        "macro_directional_union_checks": len(directional),
        "macro_directional_results": directional,
        "wall_seconds": time.perf_counter() - start,
        "not_claimed": ["free record acquisition", "full trajectory or memory equivalence", "preserved total port exit clocks", "same binary heat-bath/geometry class", "historical novelty", "runtime advantage over direct Schur evaluation"],
    }
    out = Path(__file__).with_name("MEAN_EXACT_REALIZATION_CHECKS.json")
    out.write_text(json.dumps(encode(result), indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["status", "boundary_target_mean_checks", "boundary_start_mean_checks", "native_hazard_checks", "passive_attachment_checks", "macro_original_states", "macro_realized_states", "macro_directional_union_checks", "wall_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
