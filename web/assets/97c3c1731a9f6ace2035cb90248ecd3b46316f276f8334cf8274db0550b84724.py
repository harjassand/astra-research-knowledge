#!/usr/bin/env python3
"""Exact audit: Pluecker cross-swaps versus pair-closed states on a cycle."""
from collections import deque
from itertools import combinations
from json import dump
from pathlib import Path


def det_int(a):
    a = [list(map(int, row)) for row in a]
    n = len(a)
    if n == 0:
        return 1
    sign, prev = 1, 1
    for k in range(n - 1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                assert (a[i][j] * p - a[i][k] * a[k][j]) % prev == 0
                a[i][j] = (a[i][j] * p - a[i][k] * a[k][j]) // prev
        for i in range(k + 1, n):
            a[i][k] = 0
        prev = p
    return sign * a[n - 1][n - 1]


def ordered_det(V, cols):
    return det_int([[row[j] for j in cols] for row in V])


def run(n):
    assert n % 2 == 0
    F = [[int(j == (i + 1) % n) for j in range(n)] for i in range(n)]
    # V=[I,F^T]
    V = [[int(i == j) for j in range(n)] + [F[j][i] for j in range(n)] for i in range(n)]
    m = 2 * n
    all_bases = list(combinations(range(m), n))
    det = {A: det_int([[row[j] for j in A] for row in V]) for A in all_bases}
    full = frozenset(range(m))
    comp = {A: tuple(sorted(full - set(A))) for A in all_bases}
    # Set of nonzero paired bases P(I), where P(I) contains e_i and f_i for i in I.
    paired = {}
    for I in combinations(range(n), n // 2):
        A = tuple(sorted((*I, *(n + i for i in I))) )
        paired[A] = det[A]
    supported = [A for A, x in paired.items() if x]
    assert len(supported) == 2, (n, supported, paired)
    A, B = sorted(supported)
    assert set(comp[A]) == set(B)  # two alternating paired bases complement all columns
    # GP expansion with a first column in A\B; report nonzero split exchanges.
    a = next(x for x in A if x not in B)
    X = [x for x in A if x != a]
    Y = [a, *B]
    gp_terms = []
    for t, y in enumerate(Y):
        c1_order = (*X, y)
        c2_order = tuple(z for k, z in enumerate(Y) if k != t)
        c1 = tuple(sorted(c1_order))
        c2 = tuple(sorted(c2_order))
        d1 = ordered_det(V, c1_order)
        d2 = ordered_det(V, c2_order)
        value = (-1) ** t * d1 * d2
        gp_terms.append({"t": t, "y": y, "first": c1, "second": c2,
                         "first_order": c1_order, "second_order": c2_order,
                         "first_det": d1, "second_det": d2, "signed_product": value,
                         "both_pair_closed": c1 in paired and c2 in paired})
    assert sum(z["signed_product"] for z in gp_terms) == 0
    # The endpoint term t=0 has magnitude |det(A) det(B)|; terms with y in A∩B vanish.
    assert abs(gp_terms[0]["signed_product"]) == abs(det[A] * det[B])
    # Graph on complementary ordered basis pairs, encoded by A only.
    valid = {A0 for A0 in all_bases if det[A0] and det[comp[A0]]}
    adj = {A0: [] for A0 in valid}
    for A0 in valid:
        aset = set(A0)
        for x in A0:
            for y in comp[A0]:
                A1 = tuple(sorted((aset - {x}) | {y}))
                if A1 in valid:
                    adj[A0].append((A1, x, y))
    q = deque([A])
    dist = {A: 0}
    prev = {}
    while q:
        u = q.popleft()
        if u == B:
            break
        for v, x, y in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                prev[v] = (u, x, y)
                q.append(v)
    path = None
    if B in dist:
        path = [B]
        while path[-1] != A:
            path.append(prev[path[-1]][0])
        path.reverse()
    # Connected components of the unrestricted complementary-basis graph.
    unseen = set(valid)
    component_sizes = []
    while unseen:
        root = next(iter(unseen))
        todo = [root]
        unseen.remove(root)
        size = 0
        while todo:
            u = todo.pop()
            size += 1
            for v, _, _ in adj[u]:
                if v in unseen:
                    unseen.remove(v)
                    todo.append(v)
        component_sizes.append(size)
    component_sizes.sort(reverse=True)
    path_state_data = []
    for u in path or []:
        occupied = [sum((i in u, n + i in u)) for i in range(n)]
        path_state_data.append({
            "A_columns": list(u),
            "det_A": det[u],
            "det_complement": det[comp[u]],
            "absolute_product_weight": abs(det[u] * det[comp[u]]),
            "split_pair_count": sum(x == 1 for x in occupied),
        })
    assert len(component_sizes) == 1
    assert dist[B] == n
    assert all(z["absolute_product_weight"] == 1 for z in path_state_data)
    assert sum(z["signed_product"] != 0 for z in gp_terms[1:]) == 1
    # Pair-closed endpoint neighbor support for exchanging s site-pairs (s=1..q-1).
    I_A = tuple(i for i in range(n) if i % 2 == 0)
    pair_swap = {}
    for s in range(1, n // 2):
        count = total = 0
        for rem in combinations(I_A, s):
            for add in combinations([i for i in range(n) if i not in I_A], s):
                I1 = tuple(sorted((set(I_A) - set(rem)) | set(add)))
                C = tuple(sorted((*I1, *(n + i for i in I1))))
                total += 1
                count += bool(det.get(C, 0))
        pair_swap[str(s)] = {"candidate_pair_closed_replacements": total,
                              "nonzero_destinations": count}
    assert all(v["nonzero_destinations"] == 0 for v in pair_swap.values())
    return {
        "n": n, "q": n // 2, "rank": n, "column_count": 2 * n,
        "pair_closed_basis_count": len(paired), "pair_closed_nonzero_count": len(supported),
        "supported_pair_closed": [{"columns": x, "det": paired[x]} for x in supported],
        "gp_distinguished_column": a,
        "gp_terms": gp_terms,
        "gp_endpoint_abs_product": abs(det[A] * det[B]),
        "gp_nonzero_exchange_terms": sum(z["signed_product"] != 0 for z in gp_terms[1:]),
        "complementary_ordinary_basis_pair_states": len(valid),
        "cross_swap_graph_component_count": len(component_sizes),
        "cross_swap_graph_component_sizes": component_sizes,
        "reverse_endpoint_distance": dist.get(B),
        "reverse_endpoint_path": path,
        "reverse_endpoint_path_state_data": path_state_data,
        "pair_closed_one_step_replacements": pair_swap,
        "exact_arithmetic": "Bareiss integer determinants"
    }


def block_dpp_character_audit(q):
    """Exact ordinary-DPP versus pair-closed mass and character sectors."""
    n = 2 * q
    F = [[0] * n for _ in range(n)]
    for b in range(q):
        i, j = 2 * b, 2 * b + 1
        F[i][j] = F[j][i] = 1
    V = [[int(i == j) for j in range(n)] + [F[j][i] for j in range(n)] for i in range(n)]
    all_bases = list(combinations(range(2 * n), n))
    total_mass = 0
    sectors = {}
    for S in all_bases:
        p = ordered_det(V, S)
        w = p * p
        total_mass += w
        split = 0
        selected = set(S)
        for i in range(n):
            if (i in selected) != (n + i in selected):
                split |= 1 << i
        sectors[split] = sectors.get(split, 0) + w
    pair_mass = 0
    pair_support = 0
    for I in combinations(range(n), q):
        S = tuple(sorted((*I, *(n + i for i in I))))
        p = ordered_det(V, S)
        pair_mass += p * p
        pair_support += p != 0
    nonzero = {str(mask): value for mask, value in sorted(sectors.items()) if value}
    assert total_mass == 4 ** q
    assert pair_mass == 2 ** q
    assert pair_support == 2 ** q
    assert len(nonzero) == 2 ** q
    assert {v for v in sectors.values() if v} == {2 ** q}
    return {
        "independent_two_site_blocks": q,
        "n_rows": n,
        "ordinary_full_basis_partition": total_mass,
        "pair_closed_partition": pair_mass,
        "pair_closed_support_size": pair_support,
        "parity_event_probability_in_ordinary_volume_sample": f"1/{2**q}",
        "nonzero_character_sectors": len(nonzero),
        "each_nonzero_character_sector_mass": 2 ** q,
        "character_sector_masses_hex_mask_to_integer": nonzero,
        "independent_two_replica_total_product_mass": total_mass ** 2,
        "diagonal_character_projection_mass": sum(x * x for x in sectors.values()),
        "diagonal_projection_fraction": f"1/{2**q}",
        "exact_arithmetic": "Bareiss integer determinants"
    }


def main():
    result = {"cycle_pair_closure": [run(4), run(6)],
              "block_dpp_character_audit": [block_dpp_character_audit(q) for q in (1, 2, 3)]}
    out = Path(__file__).with_name("plucker_pair_closure_audit_result.json")
    out.write_text(__import__("json").dumps(result, indent=2) + "\n")
    print(__import__("json").dumps(result, indent=2))

if __name__ == "__main__":
    main()
