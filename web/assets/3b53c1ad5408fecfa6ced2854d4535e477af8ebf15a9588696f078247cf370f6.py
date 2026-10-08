#!/usr/bin/env python3
"""Exact finite check of the labeled-coordinate graph commutator/counting lemma.

This checks only the algebraic graph identity and the endpoint shell/count
used in RESULT.txt. It is finite evidence, not a proof of the Wick or trace
estimates and not a proof of the theorem.
"""

from itertools import product
import json


def site_coords(L):
    return list(product(range(L), repeat=2))


def close(a, b, R):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= R


def allowed(z, coords, R):
    return all(not close(coords[z[i]], coords[z[j]], R)
               for i in range(len(z)) for j in range(i + 1, len(z)))


def neighbors(z, coords, L):
    out = []
    for i, site in enumerate(z):
        x, y = coords[site]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            xx, yy = x + dx, y + dy
            if 0 <= xx < L and 0 <= yy < L:
                target = coords.index((xx, yy))
                zz = list(z)
                zz[i] = target
                out.append(tuple(zz))
    return out


def run_case(L, m, R):
    coords = site_coords(L)
    configs = list(product(range(L * L), repeat=m)) if m else [()]
    P = {z: allowed(z, coords, R) for z in configs}
    shell = {z: not allowed(z, coords, R + 1) for z in configs}
    max_cross = 0
    edge_checks = 0
    diagonal_checks = 0
    for z in configs:
        # Any diagonal part of K cancels identically in the double
        # commutator; include the actual d=2 labeled-sector diagonal here.
        fz = int(P[z])
        k_zz = 4 * m  # J=1, two-dimensional Dirichlet one-body diagonal.
        double_comm_zz = 2 * fz * k_zz * fz - fz * fz * k_zz - k_zz * fz * fz
        assert double_comm_zz == 0
        diagonal_checks += 1
        nb = neighbors(z, coords, L)
        cross = [w for w in nb if P[z] != P[w]]
        max_cross = max(max_cross, len(cross))
        assert len(cross) <= 4 * m
        if cross:
            assert shell[z]
        for w in nb:
            # K_uv=-1 for a coordinate hop. Verify
            # P K P = (P^2 K + K P^2)/2 + [P,[K,P]]/2.
            k_uv = -1
            lhs = int(P[z]) * k_uv * int(P[w])
            double_comm_uv = -k_uv * (int(P[z]) - int(P[w])) ** 2
            rhs = ((int(P[z]) + int(P[w])) * k_uv + double_comm_uv) / 2
            assert lhs == rhs
            if P[z] != P[w]:
                assert shell[w]
            edge_checks += 1
    return {
        "L": L,
        "d": 2,
        "m": m,
        "R": R,
        "configurations": len(configs),
        "directed_coordinate_edges": edge_checks,
        "diagonal_commutator_checks": diagonal_checks,
        "max_crossing_degree": max_cross,
        "crossing_degree_bound": 4 * m,
        "status": "PASS",
    }


def main():
    records = [run_case(L, m, R)
               for L in range(2, 5)
               for m in range(0, 4)
               for R in range(0, 2)]
    print(json.dumps({"cases": len(records), "records": records}, indent=2))


if __name__ == "__main__":
    main()
