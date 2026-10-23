#!/usr/bin/env python3
"""Independent exact receiving checker for the Cycle5 cut-balance fixture.

This file does not import or read producer source.  It uses Fraction arithmetic,
leaf elimination for the decoder, and integer/rational Gram identities for the
all-noise certificate.  No floating eigensolver is used.
"""

import argparse
from collections import deque
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import resource
import sys
import time


EXPECTED_BYTES = 178207
EXPECTED_SHA256 = "b613d5621d5d1122fd52c382603bfbfb8bde6d68cb77171f4a4f613d9ef02912"
STRIP_BYTES = 47466
STRIP_SHA256 = "7cfc8edd7e7f6de69fa56eb675e41cb7637a50ee52bb41a044b44f8bc42bc758"


def check(condition, description):
    if not condition:
        raise AssertionError(description)


def fraction_strings(xs):
    return [str(x) for x in xs]


def edge_map(rows, expected):
    out = {}
    for u, v, value in rows:
        check(u < v, "edge-value endpoints must be canonical")
        check((u, v) not in out, "duplicate edge-value entry")
        out[u, v] = Q(value)
    check(set(out) == set(expected), "edge-value support must match graph")
    return out


def graph_structure(n, q, edges, colors):
    check(n >= 1 and q >= 1, "nonempty matrix and nonzero query count")
    check(len(colors) == n, "one color per row")
    check(all(isinstance(c, int) and 0 <= c < q for c in colors), "colors in range")
    es = set()
    adj = [set() for _ in range(n)]
    pair_edges = {}
    for u, v in edges:
        check(isinstance(u, int) and isinstance(v, int) and 0 <= u < v < n,
              "canonical simple graph labels")
        check((u, v) not in es, "no duplicate graph edge")
        es.add((u, v))
        adj[u].add(v)
        adj[v].add(u)
        check(colors[u] != colors[v], "coordinate coloring proper")
        pair = tuple(sorted((colors[u], colors[v])))
        pair_edges.setdefault(pair, []).append((u, v))

    trees = []
    incoming = [0] * n
    max_component = 1
    max_branch = 0
    gamma = Q(0)
    for pair, pe in sorted(pair_edges.items()):
        pa = {}
        for u, v in pe:
            pa.setdefault(u, set()).add(v)
            pa.setdefault(v, set()).add(u)
        unseen = set(pa)
        while unseen:
            seed = min(unseen)
            vs = set([seed])
            todo = [seed]
            for u in todo:
                for v in pa[u]:
                    if v not in vs:
                        vs.add(v)
                        todo.append(v)
            unseen.difference_update(vs)
            te = sorted((u, v) for u in vs for v in pa[u] if u < v)
            check(len(te) == len(vs) - 1, "every bichromatic component is a tree")
            N = len(vs)

            # Find every centroid directly by deleting each candidate vertex.
            # This independent verifier deliberately does not share the producer's
            # linear-time representation construction.
            centroids = []
            for candidate in sorted(vs):
                seen = {candidate}
                largest = 0
                for start in sorted(pa[candidate]):
                    if start in seen:
                        continue
                    branch = [start]
                    seen.add(start)
                    for u in branch:
                        for v in pa[u]:
                            if v not in seen:
                                seen.add(v)
                                branch.append(v)
                    largest = max(largest, len(branch))
                if 2 * largest <= N:
                    centroids.append(candidate)
            check(centroids, "a tree centroid exists")
            root = min(centroids)
            parent = {root: None}
            order = [root]
            for u in order:
                for v in sorted(pa[u]):
                    if v != parent[u]:
                        check(v not in parent, "centroid traversal has no cycle")
                        parent[v] = u
                        order.append(v)
            check(set(order) == vs, "centroid traversal covers component")
            subtree = {u: {u} for u in vs}
            for u in reversed(order[1:]):
                subtree[parent[u]].update(subtree[u])
            children = {u: [] for u in vs}
            for child in order[1:]:
                p = parent[child]
                children[p].append(child)
                incoming[child] += 1
                a = len(subtree[child])
                check(2 * a <= N, "centroid orientation always picks smaller cut side")
                max_branch = max(max_branch, a)
                gamma = max(gamma, Q(a * (N - a), N))
            max_component = max(max_component, N)
            trees.append(dict(pair=pair, vertices=sorted(vs), edges=te, adjacency=pa,
                              N=N, root=root, centroids=centroids, parent=parent,
                              order=order, subtree=subtree, children=children))
    r = max((len({colors[v] for v in adj[u]}) for u in range(n)), default=0)
    r0 = max(incoming, default=0)
    row_mass = [0] * n
    for tree in trees:
        for v in tree["vertices"]:
            row_mass[v] += tree["N"] - 1
    isometry = all(len({colors[v] for v in adj[u]}) == len(adj[u]) for u in range(n))
    all_stars = all(any(len(t["adjacency"][v]) == t["N"] - 1 for v in t["vertices"]) for t in trees)
    return dict(n=n, q=q, colors=colors, edges=sorted(es), adjacency=adj,
                trees=trees, maximum_degree=max(map(len, adj), default=0),
                maximum_component_size=max_component, gamma=gamma, M=max_branch,
                r=r, r0=r0, incoming=incoming, row_mass=row_mass,
                old_row_constant_sq=1 + max(row_mass, default=0),
                isometry=isometry, all_stars=all_stars)


def check_plan(g, plan):
    expected = {
        "n": g["n"], "q": g["q"], "edges": len(g["edges"]),
        "maximum_degree": g["maximum_degree"],
        "maximum_component_size": g["maximum_component_size"],
        "gamma": str(g["gamma"]), "centroid_branch_maximum": g["M"],
        "maximum_incoming": g["r0"], "neighbour_color_count": g["r"],
        "cut_operator_constant_sq": str(1 + 4 * g["r0"] * g["M"]),
        "best_supplied_operator_constant_sq": str(min(
            1 + 4 * g["r0"] * g["M"],
            g["old_row_constant_sq"],
            1 if g["isometry"] else 2 if g["all_stars"] else g["old_row_constant_sq"]))
    }
    check(plan == expected, "all plan fields reconstructed exactly")
    return expected


def action(g, diagonal, weights):
    """Multiply the exact sparse symmetric matrix by the coordinate design."""
    n, q, colors = g["n"], g["q"], g["colors"]
    check(len(diagonal) == n, "diagonal length")
    y = [[Q(0) for _ in range(q)] for _ in range(n)]
    for i in range(n):
        y[i][colors[i]] = diagonal[i]
    for (u, v), w in weights.items():
        y[u][colors[v]] += w
        y[v][colors[u]] += w
    return y


def leaf_decode(g, y):
    """Mean-project each signed incidence channel, then eliminate leaves.

    No centroid, cut-vector, or producer decoder is used in this routine.
    """
    colors = g["colors"]
    diagonal = [y[i][colors[i]] for i in range(g["n"])]
    weights = {}
    for tree in g["trees"]:
        lo, hi = tree["pair"]
        vs = tree["vertices"]
        sigma = {v: 1 if colors[v] == lo else -1 for v in vs}
        f = {v: sigma[v] * y[v][hi if colors[v] == lo else lo] for v in vs}
        mean = sum(f.values(), Q(0)) / tree["N"]
        f = {v: f[v] - mean for v in vs}
        adj = {v: set(tree["adjacency"][v]) for v in vs}
        queue = deque(v for v in vs if len(adj[v]) == 1)
        remaining = set(vs)
        while len(remaining) > 1:
            check(queue, "tree leaf elimination cannot stall")
            u = queue.popleft()
            if u not in remaining or len(adj[u]) != 1:
                continue
            v = next(iter(adj[u]))
            e = tuple(sorted((u, v)))
            weights[e] = sigma[u] * f[u]
            f[v] += f[u]
            adj[v].remove(u)
            adj[u].clear()
            remaining.remove(u)
            if len(adj[v]) == 1:
                queue.append(v)
        check(f[next(iter(remaining))] == 0, "projected final divergence vanishes exactly")
    check(set(weights) == set(g["edges"]), "decoder recovers one value per edge")
    return diagonal, weights


def norm_sq(rows):
    return sum((a * a for row in rows for a in row), Q(0))


def matrix_frobenius_sq(diagonal, weights):
    return sum((a * a for a in diagonal), Q(0)) + 2 * sum((a * a for a in weights.values()), Q(0))


def exact_covariance_certificate(g, noise=None, error_weights=None):
    """Verify every local Gram and a symbolic PSD decomposition exactly.

    For group subtree sizes a, M I - H H^T equals
        diag(M-a) + a a^T/N.
    Nonnegative diagonal plus one outer product is an all-real-vector PSD proof.
    Direct integer dot products verify that H is the actual centered-cut matrix.
    """
    groups = []
    all_component_cells = set()
    checked_gram_entries = 0
    outgoing = [Q(0) for _ in range(g["n"])]
    colors = g["colors"]
    for tree in g["trees"]:
        N = tree["N"]
        lo, hi = tree["pair"]
        vs = tree["vertices"]
        cells = {(v, hi if colors[v] == lo else lo) for v in vs}
        check(not (cells & all_component_cells), "bichromatic noise channels disjoint globally")
        all_component_cells.update(cells)
        sigma = {v: 1 if colors[v] == lo else -1 for v in vs}
        signed_noise = None
        if noise is not None:
            signed_noise = {v: sigma[v] * noise[v][hi if colors[v] == lo else lo] for v in vs}
        component_M = max((len(tree["subtree"][u]) for u in tree["order"][1:]), default=0)
        for parent in vs:
            children = sorted(tree["children"][parent])
            if not children:
                continue
            subtrees = [tree["subtree"][u] for u in children]
            a = [len(s) for s in subtrees]
            check(max(a) <= component_M <= g["M"], "local branch cap")
            for i, s in enumerate(subtrees):
                for t in subtrees[i + 1:]:
                    check(not (s & t), "child subtrees are pairwise disjoint")
            # Each H row is stored as the integer numerator N*1_S-a.
            Hn = [[N * int(v in s) - size for v in vs] for s, size in zip(subtrees, a)]
            for row in Hn:
                check(sum(row) == 0, "centered cut coefficient sums to zero")
            for i, row in enumerate(Hn):
                for j, other in enumerate(Hn):
                    gram = Q(sum(x * y for x, y in zip(row, other)), N * N)
                    expected = (Q(a[i]) if i == j else Q(0)) - Q(a[i] * a[j], N)
                    check(gram == expected, "direct exact local Gram formula")
                    psd_rhs = (Q(component_M - a[i]) if i == j else Q(0)) + Q(a[i] * a[j], N)
                    check((Q(component_M) if i == j else Q(0)) - gram == psd_rhs,
                          "exact PSD decomposition of M I minus Gram")
                    checked_gram_entries += 1
            if signed_noise is not None:
                for child, row in zip(children, Hn):
                    predicted = sigma[child] * sum((Q(h, N) * signed_noise[v] for h, v in zip(row, vs)), Q(0))
                    e = tuple(sorted((parent, child)))
                    check(predicted == error_weights[e], "cut-map noise equals independent leaf decoder error")
                    outgoing[parent] += predicted * predicted
            groups.append(dict(pair=list(tree["pair"]), centroid=tree["root"],
                               parent=parent, N=N, child_sizes=a, M=component_M,
                               psd_diagonal=[component_M - z for z in a],
                               psd_rank_one_scale="1/" + str(N)))
    diagonal_cells = {(v, colors[v]) for v in range(g["n"])}
    check(not (all_component_cells & diagonal_cells), "diagonal/off-diagonal noise orthogonality")
    check(max(g["incoming"], default=0) == g["r0"] <= g["r"], "global sparse-column bound")
    if noise is not None:
        used_off = sum((noise[v][c] ** 2 for v, c in all_component_cells), Q(0))
        check(max(outgoing, default=Q(0)) <= g["M"] * used_off, "observed outgoing bound")
    return dict(status="PASS", components=len(g["trees"]), nonempty_parent_groups=len(groups),
                exact_gram_entries_checked=checked_gram_entries,
                symbolic_psd_decomposition="diag(M-a) + a*a^T/N, M-a >= 0, N > 0",
                r0=g["r0"], M=g["M"], all_noise_operator_constant_sq=str(1 + 4 * g["r0"] * g["M"]),
                maximum_observed_outgoing_error_sq=str(max(outgoing, default=Q(0))) if noise is not None else None,
                groups=groups)


def edge_sides(g, edge):
    u, v = edge
    check(tuple(sorted(edge)) in set(g["edges"]), "cut edge exists")
    seen = {v}
    todo = [v]
    for a in todo:
        for b in g["adjacency"][a]:
            if (a == u and b == v) or (a == v and b == u):
                continue
            if b not in seen:
                seen.add(b)
                todo.append(b)
    check(u not in seen, "edge really separates tree")
    other = set(range(g["n"])) - seen
    return seen, other


def verify_star_comparator(g, data):
    q = data["q"]
    check(q == 3, "ordinary comparator uses three queries")
    h = graph_structure(g["n"], q, g["edges"], data["colors"])
    checked = 0
    for tree in h["trees"]:
        N = tree["N"]
        centers = [u for u in tree["vertices"] if len(tree["adjacency"][u]) == N - 1]
        check(centers, "every comparator bichromatic component is a star")
        edges = tree["edges"]
        for i, e in enumerate(edges):
            for j, f in enumerate(edges):
                gram = len(set(e) & set(f))
                check(gram == 1 + int(i == j), "star unsigned-incidence B^T B = I + 11^T")
                checked += 1
    check(data["all_bichromatic_components_are_stars"] is True, "saved star assertion")
    check(Q(data["frobenius_and_operator_constant_sq"]) == 2, "ordinary constant squared is two")
    return dict(status="PASS", q=q, star_components=len(h["trees"]),
                exact_incidence_gram_entries_checked=checked,
                frobenius_and_operator_constant_sq="2",
                proof="B^T B = I + 11^T >= I; symmetric off-diagonal entries count twice; diagonal channels disjoint")


def exact_row_bound_certificate(g):
    """Check the old row-bound geometry without enumerating sign vectors.

    Around any vertex, the incident cut sides partition the other N-1 vertices.
    Their Gram is diag(a)-aa^T/N.  For arbitrary signs epsilon, therefore,
       ||sum epsilon_j h_j||^2 = (N-1) - (sum epsilon_j a_j)^2/N <= N-1.
    This proves the l2-to-l1 row estimate for all noise, then Gershgorin and
    disjoint channel Cauchy-Schwarz give 1 + max_v sum_T (N_T-1).
    """
    checked_entries = 0
    groups = 0
    masses = [0] * g["n"]
    for tree in g["trees"]:
        vs = tree["vertices"]
        vset = set(vs)
        N = tree["N"]
        for v in vs:
            sides = []
            for u in sorted(tree["adjacency"][v]):
                if tree["parent"].get(u) == v:
                    s = tree["subtree"][u]
                else:
                    check(tree["parent"].get(v) == u, "incident edge orientation consistent")
                    s = vset - tree["subtree"][v]
                sides.append(s)
            a = [len(s) for s in sides]
            check(sum(a) == N - 1, "incident cut sizes sum to N-1")
            check(set().union(*sides) == vset - {v}, "incident cut sides cover all other vertices")
            for i, s in enumerate(sides):
                check(all(not (s & t) for t in sides[i + 1:]), "incident cut sides disjoint")
            Hn = [[N * int(u in s) - size for u in vs] for s, size in zip(sides, a)]
            for i, h in enumerate(Hn):
                for j, k in enumerate(Hn):
                    gram = Q(sum(x * y for x, y in zip(h, k)), N * N)
                    check(gram == (Q(a[i]) if i == j else Q(0)) - Q(a[i] * a[j], N),
                          "old row-bound exact incident Gram")
                    checked_entries += 1
            masses[v] += N - 1
            groups += 1
    check(masses == g["row_mass"], "row mass recomputed from exact incident cuts")
    return dict(status="PASS", per_vertex_component_mass=masses,
                all_noise_operator_constant_sq=str(1 + max(masses, default=0)),
                incident_groups=groups, exact_incident_gram_entries_checked=checked_entries,
                symbolic_all_sign_identity="epsilon^T Gram epsilon = N-1 - (a^T epsilon)^2/N <= N-1")


def verify_received_strip(data, source_data):
    fixture = source_data["fixture"]
    op = data["original_operation"]
    check(fixture["vertices"] == list(range(99)), "pinned original graph labels")
    check(sorted(map(tuple, fixture["edges"])) == sorted(map(tuple, op["edges"])), "received graph binds to pinned structural output")
    source_colors = dict(fixture["colors"])
    check(op["colors"] == [source_colors[v] for v in range(99)], "received coloring binds to pinned structural output")
    g = graph_structure(99, 4, op["edges"], op["colors"])
    plan = check_plan(g, op["plan"])
    check(len(g["edges"]) == 194 and g["maximum_degree"] == 4, "received original support size and degree")
    check(g["gamma"] == Q(20, 9) and g["M"] == 4 and g["r0"] == 3, "received cut parameters exact")
    check(Q(plan["cut_operator_constant_sq"]) == 49 and Q(plan["best_supplied_operator_constant_sq"]) == 20,
          "received new and stronger inherited constants preserved")
    diagonal = list(map(Q, op["diagonal"]))
    weights = edge_map(op["edge_values"], g["edges"])
    noise = [list(map(Q, row)) for row in op["noise"]]
    check(len(noise) == 99 and all(len(row) == 4 for row in noise), "received noise shape")
    ay = action(g, diagonal, weights)
    nd, nw = leaf_decode(g, ay)
    check(nd == diagonal and nw == weights, "received exact noiseless inverse")
    y = [[a + b for a, b in zip(row, erow)] for row, erow in zip(ay, noise)]
    dd, dw = leaf_decode(g, y)
    check(dd == list(map(Q, op["decoded"]["diagonal"])), "received all noisy diagonal entries")
    check(dw == edge_map(op["decoded"]["edge_values"], g["edges"]), "received all noisy edge entries")
    ed = [a - b for a, b in zip(dd, diagonal)]
    ew = {e: dw[e] - weights[e] for e in weights}
    nn, ff = norm_sq(noise), matrix_frobenius_sq(ed, ew)
    diagonal_noise = sum((noise[v][g["colors"][v]] ** 2 for v in range(99)), Q(0))
    cells = set()
    for tree in g["trees"]:
        lo, hi = tree["pair"]
        cells.update((v, hi if g["colors"][v] == lo else lo) for v in tree["vertices"])
    off_noise = sum((noise[v][c] ** 2 for v, c in cells), Q(0))
    check(nn == Q(op["noise_norm_sq"]) and ff == Q(op["error_frobenius_sq"]), "received exact norms")
    check(diagonal_noise == Q(op["diagonal_noise_sq"]) and off_noise == Q(op["used_off_noise_sq"]), "received channel accounting")
    unused_noise = nn - diagonal_noise - off_noise
    check(unused_noise >= 0, "unused action noise is charged in total")
    covariance = exact_covariance_certificate(g, noise, ew)
    check(Q(covariance["maximum_observed_outgoing_error_sq"]) == Q(op["maximum_outgoing_error_sq"]), "received maximum outgoing error")
    row_bound = exact_row_bound_certificate(g)
    check(Q(row_bound["all_noise_operator_constant_sq"]) == 20, "inherited row bound exactly twenty")

    old = fixture["reduced_vertices"]
    index = {v: i for i, v in enumerate(old)}
    old_edges = {tuple(sorted(e)) for e in fixture["reduced_edges"]}
    check(old_edges <= set(g["edges"]), "all reduced edges retained")
    check({e for e in g["edges"] if e[0] in index and e[1] in index} == old_edges, "no unaccounted edge between old vertices")
    rc = dict(fixture["reduced_colors"])
    check(all(rc[v] == source_colors[v] for v in old), "reduced colors retained")
    rg = graph_structure(len(old), 4,
                         [sorted((index[u], index[v])) for u, v in old_edges],
                         [rc[v] for v in old])
    reduced_plan = check_plan(rg, data["reduced_plan"])
    check(len(old) == 8 and len(old_edges) == 6 and rg["gamma"] == Q(1, 2), "reduced cut inputs exact")
    check(rg["isometry"] and Q(reduced_plan["best_supplied_operator_constant_sq"]) == 1, "reduced design Frobenius isometry")

    # Check only the supplied receiving fixture's attachment operation.  No
    # strip-transition construction, search, or earlier experiment is replayed.
    old_set = set(old)
    maximum_attached = 0
    maximum_detached = 0
    attachment_groups = []
    for lo in range(4):
        for hi in range(lo + 1, 4):
            vertices = {v for v in range(99) if g["colors"][v] in (lo, hi)}
            adj = {v: set() for v in vertices}
            for u, v in g["edges"]:
                if u in vertices and v in vertices and (u, v) not in old_edges:
                    adj[u].add(v)
                    adj[v].add(u)
            unseen = set(vertices)
            attached_counts = {}
            while unseen:
                start = min(unseen)
                comp = {start}
                todo = [start]
                for u in todo:
                    for v in adj[u]:
                        if v not in comp:
                            comp.add(v)
                            todo.append(v)
                unseen.difference_update(comp)
                roots = comp & old_set
                check(len(roots) <= 1, "after removing old edges no attachment meets two old vertices")
                if roots:
                    root = next(iter(roots))
                    attached_counts[root] = attached_counts.get(root, 0) + len(comp) - 1
                else:
                    maximum_detached = max(maximum_detached, len(comp))
            maximum_attached = max(maximum_attached, max(attached_counts.values(), default=0))
            attachment_groups.append(dict(pair=[lo, hi], added_vertices_by_old_root=attached_counts))
    check(maximum_attached == 7 and maximum_detached == 5, "actual receiving attachment masses")
    bound = max((1 + maximum_attached) * rg["gamma"], Q(maximum_attached), Q(maximum_detached, 4))
    expected_attachment = {
        "maximum_added_vertices_per_old_vertex_and_pair": maximum_attached,
        "maximum_detached_tree_size": maximum_detached,
        "certified_gamma_upper": str(bound), "actual_gamma": str(g["gamma"]),
        "no_attachment_meets_two_old_vertices_after_old_edges_removed": True
    }
    check(expected_attachment == data["attachment_check"], "all saved attachment claims checked")
    check(g["gamma"] <= bound == 7, "actual Gamma below transfer certificate")
    return dict(status="PASS", original_plan=plan, reduced_plan=reduced_plan,
                noisy_verification=dict(noise_norm_sq=str(nn), error_frobenius_sq=str(ff),
                    diagonal_noise_sq=str(diagonal_noise), used_off_noise_sq=str(off_noise),
                    unused_noise_sq=str(unused_noise), all_decoded_entries="PASS"),
                all_noise_new_covariance=covariance, all_noise_inherited_row_bound=row_bound,
                attachments=expected_attachment, attachment_groups=attachment_groups,
                receiving_scope="Only pinned original/reduced graph and color data received; no transition diagnostic replay or generic coloring algorithm.")


def verify_fixture(data):
    op = data["arm_operation"]
    g = graph_structure(op["plan"]["n"], op["plan"]["q"], op["edges"], op["colors"])
    plan = check_plan(g, op["plan"])
    check(g["n"] == 397 and g["q"] == 2 and len(g["edges"]) == 396, "arm fixture size and query count")
    check(data["arm_lengths"] == [12] * 33, "33 equal length-12 arms declared")
    hubs = [v for v in range(g["n"]) if len(g["adjacency"][v]) == 33]
    check(hubs == [0], "unique degree-33 hub at vertex zero")
    check(all(len(g["adjacency"][v]) <= 2 for v in range(1, g["n"])), "non-hub degrees at most two")
    observed_lengths = []
    for start in sorted(g["adjacency"][0]):
        previous, current, count = 0, start, 1
        while len(g["adjacency"][current]) == 2:
            nxt = next(v for v in g["adjacency"][current] if v != previous)
            previous, current, count = current, nxt, count + 1
        check(len(g["adjacency"][current]) == 1, "arm ends in leaf")
        observed_lengths.append(count)
    check(observed_lengths == [12] * 33, "graph itself has the declared arms")
    check(g["gamma"] == Q(4620, 397) and g["M"] == 12 and g["r0"] == 1,
          "arm exact cut parameters")
    check(Q(plan["cut_operator_constant_sq"]) == 49, "arm all-noise constant squared")

    diagonal = list(map(Q, op["diagonal"]))
    weights = edge_map(op["edge_values"], g["edges"])
    noise = [list(map(Q, row)) for row in op["noise"]]
    check(len(noise) == g["n"] and all(len(row) == g["q"] for row in noise), "noise dimensions")
    exact_y = action(g, diagonal, weights)
    nd, nw = leaf_decode(g, exact_y)
    check(nd == diagonal and nw == weights, "exact noiseless reconstruction")
    y = [[a + b for a, b in zip(row, erow)] for row, erow in zip(exact_y, noise)]
    dd, dw = leaf_decode(g, y)
    check(dd == list(map(Q, op["decoded"]["diagonal"])), "all noisy decoded diagonal entries match")
    check(dw == edge_map(op["decoded"]["edge_values"], g["edges"]), "all noisy decoded edge entries match")
    diag_error = [a - b for a, b in zip(dd, diagonal)]
    edge_error = {e: dw[e] - weights[e] for e in weights}
    noise_norm = norm_sq(noise)
    error_frob = matrix_frobenius_sq(diag_error, edge_error)
    diagonal_noise = sum((noise[v][g["colors"][v]] ** 2 for v in range(g["n"])), Q(0))
    off_noise = noise_norm - diagonal_noise
    check(noise_norm == Q(op["noise_norm_sq"]), "noise norm squared")
    check(error_frob == Q(op["error_frobenius_sq"]), "decoded error Frobenius norm squared")
    check(diagonal_noise == Q(op["diagonal_noise_sq"]), "diagonal noise allocation")
    check(off_noise == Q(op["used_off_noise_sq"]), "off-diagonal noise allocation")
    covariance = exact_covariance_certificate(g, noise, edge_error)
    check(Q(covariance["maximum_observed_outgoing_error_sq"]) == Q(op["maximum_outgoing_error_sq"]),
          "maximum outgoing noisy error agrees")

    cut = data["cut_adversary"]
    cd = list(map(Q, cut["diagonal"]))
    cw = edge_map(cut["edge_values"], g["edges"])
    check(all(z == 0 for z in cd), "cut witness diagonal zero")
    A, B = edge_sides(g, cut["edge"])
    check((len(A), len(B)) == (cut["a"], cut["b"]) == (12, 385), "cut witness split sizes")
    check(abs(cw[tuple(sorted(cut["edge"]))]) == 1, "cut witness has unit boundary edge")
    cy = action(g, cd, cw)
    sigma = [1 if c == 0 else -1 for c in g["colors"]]
    signed = [sigma[v] * cy[v][1 - g["colors"][v]] for v in range(g["n"])]
    check(all(signed[v] == Q(1, len(A)) for v in A), "cut divergence constant +1/a on one side")
    check(all(signed[v] == -Q(1, len(B)) for v in B), "cut divergence constant -1/b on other side")
    cut_action = norm_sq(cy)
    check(cut_action == Q(397, 4620) == Q(cut["action_norm_sq"]), "cut action squared exact")
    check(1 / cut_action == Q(cut["inverse_lower_sq"]) == g["gamma"], "cut inverse lower equals Gamma")

    ramp = data["operator_vs_frobenius_witness"]
    rd = list(map(Q, ramp["diagonal"]))
    rw = edge_map(ramp["edge_values"], g["edges"])
    path = ramp["selected_path"]
    check(len(path) == 25 and len(set(path)) == 25, "ramp path has 25 distinct vertices")
    pe = [tuple(sorted((u, v))) for u, v in zip(path, path[1:])]
    check(all(e in rw for e in pe), "ramp path follows actual edges")
    for j, e in enumerate(pe, 1):
        check(rw[e] == (-1) ** (j - 1) * min(j, 25 - j), "ramp edge formula exact")
    check(all(w == 0 for e, w in rw.items() if e not in pe), "ramp has no off-path entries")
    check(all(x == 0 for x in rd), "ramp diagonal zero")
    ry = action(g, rd, rw)
    ra, rf = norm_sq(ry), matrix_frobenius_sq(rd, rw)
    check(ra == 24 == Q(ramp["action_norm_sq"]), "ramp exact action norm")
    check(rf == 2600 == Q(ramp["matrix_frobenius_sq"]), "ramp exact Frobenius norm")
    check(rf / ra == Q(325, 3) == Q(ramp["frobenius_inverse_lower_sq"]), "ramp Frobenius ratio")
    check(Q(ramp["operator_inverse_upper_sq"]) == 49 == Q(plan["cut_operator_constant_sq"]),
          "ramp uses the same design's all-noise operator upper")
    check(rf / ra > 49, "strict separation between Frobenius lower and operator upper")

    comparator = verify_star_comparator(g, data["same_graph_ordinary_comparator"])

    ds = data["double_star_failure"]
    h = graph_structure(ds["plan"]["n"], ds["plan"]["q"], ds["edges"], ds["colors"])
    dplan = check_plan(h, ds["plan"])
    check(h["n"] == 66 and h["q"] == 2 and ds["leaves_each"] == 32, "double-star size")
    check(h["adjacency"][0] == set(range(1, 34)) and h["adjacency"][1] == {0} | set(range(34, 66)),
          "double-star exact hub neighborhoods")
    check(all(len(h["adjacency"][v]) == 1 for v in range(2, 66)), "double-star all other vertices leaves")
    check(ds["diameter"] == 3, "double-star diameter is three by hub/leaves structure")
    hd = list(map(Q, ds["diagonal"]))
    hw = edge_map(ds["edge_values"], h["edges"])
    check(all(x == 0 for x in hd), "double-star diagonal zero")
    check(ds["unit_central_edge"] == [0, 1] and hw[0, 1] == 1, "double-star central edge unit")
    check(all(w == -Q(1, 33) for e, w in hw.items() if e != (0, 1)), "double-star leaf values exact")
    hy = action(h, hd, hw)
    check(hy == [list(map(Q, row)) for row in ds["action"]], "double-star full action matches")
    ha = norm_sq(hy)
    check(ha == Q(2, 33) == Q(ds["action_norm_sq"]), "double-star action norm exact")
    check(h["gamma"] == Q(33, 2) == Q(ds["operator_inverse_lower_sq"]) == 1 / ha,
          "double-star cut lower exact")
    hnd, hnw = leaf_decode(h, hy)
    check(hnd == hd and hnw == hw, "double-star witness exact independent inversion")
    double_covariance = exact_covariance_certificate(h)

    return {
        "status": "PASS",
        "arm_plan": plan,
        "arm_noisy_verification": {
            "all_diagonal_and_edge_entries": "PASS", "noise_norm_sq": str(noise_norm),
            "error_frobenius_sq": str(error_frob), "diagonal_noise_sq": str(diagonal_noise),
            "used_off_noise_sq": str(off_noise)
        },
        "arm_all_noise_certificate": covariance,
        "cut_witness": {"a": len(A), "b": len(B), "action_norm_sq": str(cut_action),
                        "operator_inverse_lower_sq": str(1 / cut_action)},
        "ramp_norm_separation": {"action_norm_sq": str(ra), "matrix_frobenius_sq": str(rf),
                                 "frobenius_inverse_lower_sq": str(rf / ra), "operator_inverse_upper_sq": "49"},
        "same_graph_comparator": comparator,
        "double_star": {"plan": dplan, "action_norm_sq": str(ha), "operator_inverse_lower_sq": str(1 / ha),
                        "all_noise_certificate": double_covariance},
        "scope": "Exact receiving verification of saved operations and all-noise covariance; no full-class four-query theorem or runtime superiority.",
        "independence": "Producer source and experiment never read/imported; decoder uses rational leaf elimination; all-noise check uses exact integer/rational Gram identities, no floating eigenvalues."
    }


def main():
    started_wall = time.perf_counter()
    started_cpu = time.process_time()
    started_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=Path(__file__).resolve().parents[1] / "results" / "cut_balance_operations.json")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("cut_balance_independent_result.json"))
    args = parser.parse_args()
    raw = args.fixture.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    check(len(raw) == EXPECTED_BYTES, "exact fixture byte count")
    check(digest == EXPECTED_SHA256, "exact fixture hash")
    data = json.loads(raw)
    result = verify_fixture(data)
    result["input"] = dict(filename=args.fixture.name, bytes=len(raw), sha256=digest)
    strip_path = args.fixture.with_name("received_strip_operation.json")
    strip_raw = strip_path.read_bytes()
    check(len(strip_raw) == STRIP_BYTES and hashlib.sha256(strip_raw).hexdigest() == STRIP_SHA256,
          "exact received-strip fixture identity")
    strip_data = json.loads(strip_raw)
    source_path = args.fixture.parents[1] / strip_data["source_relative"]
    source_raw = source_path.read_bytes()
    check(len(source_raw) == strip_data["source_bytes"] and hashlib.sha256(source_raw).hexdigest() == strip_data["source_sha256"],
          "received-strip source provenance binds to exact structural result")
    result["received_strip"] = verify_received_strip(strip_data, json.loads(source_raw))
    result["received_strip_input"] = dict(filename=strip_path.name, bytes=len(strip_raw), sha256=STRIP_SHA256,
                                          pinned_source_sha256=strip_data["source_sha256"])
    result["costs"] = dict(started_utc=started_utc,
        verification_body_wall_seconds=time.perf_counter() - started_wall,
        verification_body_cpu_seconds=time.process_time() - started_cpu,
        peak_process_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == "darwin" else 1024),
        excluded="Python startup/imports, report serialization, authoring, reasoning and prior read-only inspection; no producer timing comparison.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    log = args.output.with_name("cut_balance_independent_runs.jsonl")
    with log.open("a") as f:
        f.write(json.dumps(dict(status="PASS", input_sha256=digest, output=args.output.name, **result["costs"]), sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "output": str(args.output), "input_sha256": digest,
                      "arm_constant_sq": "49", "arm_gamma": "4620/397", "ramp_frobenius_ratio_sq": "325/3",
                      "double_star_action_norm_sq": "2/33", "costs": result["costs"]}, indent=2))


if __name__ == "__main__":
    main()
