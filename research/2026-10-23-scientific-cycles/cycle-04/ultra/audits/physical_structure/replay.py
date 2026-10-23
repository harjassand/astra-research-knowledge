#!/usr/bin/env python3
"""Exact admission replay for the four-qubit structural boundary.

Standard library only. Signs represent actual amplitudes signs[x]/4.
The replay does not purport to numerically prove the universal classification.
"""
import argparse
import json
import pathlib
import platform
import resource
import time


def parity(x):
    return x.bit_count() & 1


def pack(x, sites):
    return sum(((x >> s) & 1) << a for a, s in enumerate(sites))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path,
                        default=pathlib.Path(__file__).with_name("RESULT.json"))
    args = parser.parse_args()
    wall0, cpu0 = time.perf_counter(), time.process_time()
    n, q = 4, 16
    edges = [(0, 1), (1, 2), (2, 3)]
    base = [(-1) ** (sum(((x >> a) & 1) * ((x >> b) & 1)
                       for a, b in edges) & 1) for x in range(q)]
    vectors = [[base[x] * (-1) ** parity(x & z) for x in range(q)]
               for z in range(q)]
    for z in range(q):
        for w in range(q):
            assert sum(vectors[z][x] * vectors[w][x] for x in range(q)) == (
                q if z == w else 0)

    ranks = {}
    checked_eigenvectors = checked_flat_reductions = 0
    for smask in range(1, q - 1):
        s = [a for a in range(n) if smask >> a & 1]
        c = [a for a in range(n) if not (smask >> a & 1)]
        ds, dc = 1 << len(s), 1 << len(c)
        neighbors = [sum(1 << b for a, b in edges if a == site)
                     + sum(1 << a for a, b in edges if b == site)
                     for site in range(n)]
        subspace = {0}
        for generator in [g for site in s for g in (1 << site, neighbors[site])]:
            subspace |= {v ^ generator for v in list(subspace)}
        assert all((1 << site) in subspace for site in s)
        index = {(pack(x, s), pack(x, c)): x for x in range(q)}
        for z, v in enumerate(vectors):
            # Actual partial state numerator: rho_c = R/16.
            r = [[sum(v[index[(a, b)]] * v[index[(a, d)]]
                      for a in range(ds)) for d in range(dc)]
                 for b in range(dc)]
            purity_numerator = sum(t * t for row in r for t in row)
            assert q * q % purity_numerator == 0
            k = q * q // purity_numerator
            assert q % k == 0
            assert sum(r[a][a] for a in range(dc)) == q
            for b in range(dc):
                for d in range(dc):
                    assert sum(r[b][a] * r[a][d] for a in range(dc)) == (
                        q // k) * r[b][d]
            assert smask not in ranks or ranks[smask] == k
            ranks[smask] = k
            checked_flat_reductions += 1

            # Actual E_s(|v_z><v_z|) numerator is delta_(x_s,y_s) R[x_c,y_c],
            # denominator 16*2^|s|. Every graph-basis vector is an eigenvector
            # iff (M v_w)[x] / v_w[x] is independent of x. All v_w[x] = +/-1/4.
            m = [[r[pack(x, c)][pack(y, c)] if pack(x, s) == pack(y, s)
                  else 0 for y in range(q)] for x in range(q)]
            eigenvalue_numerators = []
            for w in range(q):
                image = [sum(m[x][y] * vectors[w][y] for y in range(q))
                         for x in range(q)]
                ratios = [image[x] * vectors[w][x] for x in range(q)]
                assert len(set(ratios)) == 1
                assert ratios[0] * len(subspace) == (q * ds if w ^ z in subspace else 0)
                eigenvalue_numerators.append(ratios[0])
                checked_eigenvectors += 1
            assert sum(eigenvalue_numerators) == q * ds

    single_ranks = [ranks[1 << a] for a in range(n)]
    balanced = [ranks[0b0011], ranks[0b0101], ranks[0b1001]]
    assert single_ranks == [2] * 4
    assert balanced == [2, 4, 4]
    excluded_ghz_patterns = [[2, 2, 2], [1, 4, 4]]
    assert sorted(balanced) not in excluded_ghz_patterns

    result = {
        "status": "PASS",
        "claim": "Actual four-qubit invariant path-graph basis is outside tensor-GHZ-block normal form",
        "arithmetic": "exact signed integer coefficients with denominators recorded analytically",
        "basis_vectors": q,
        "orthonormality_inner_products": q * q,
        "nonempty_proper_erasures": 14,
        "flat_reductions_checked": checked_flat_reductions,
        "actual_erasure_eigenvectors_checked": checked_eigenvectors,
        "explicit_graph_coordinate_refinement_checked": True,
        "single_site_cut_ranks": single_ranks,
        "balanced_cut_ranks_12_13_14": balanced,
        "tensor_GHZ_patterns_excluded": excluded_ghz_patterns,
        "all_cut_ranks": {str(mask): rank for mask, rank in sorted(ranks.items())},
        "does_not_establish": ["unrestricted entropy witness", "formation improvement",
                               "historical novelty", "efficient state preparation"],
        "cpu_seconds": time.process_time() - cpu0,
        "wall_seconds": time.perf_counter() - wall0,
        "peak_rss_native": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "platform": platform.platform(),
        "total_discovery_cost": "UNKNOWN",
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
