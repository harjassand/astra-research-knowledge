"""Independent source-informed exact check of the three saved Cycle7 uses.

Only Python standard library is imported. No producer module or executable is
imported or called. The graph labels are checked against the documented
allocation convention, and reconstruction uses an analytic star-center formula
rather than the producer's general signed tree-incidence decoder.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import resource
import time
import zipfile

BASE = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PREDECESSOR_NAME = "Astra_Amplification_Cycle6_PRO2_20261022.zip"
PREDECESSOR_BYTES = 168937
PREDECESSOR_HASH = "1c45c5708be5f277f6ae881f3d2e7e0598fe9b79cd943d8afcc42a3e404041cb"
NATIVE_MEMBER = "results/failed_even_series_rotation.json"
NATIVE_BYTES = 136415
NATIVE_HASH = "18dcb6f78241dd5b89c7048b74e3e883cd674db5f75dc12f69d21aa0bd1bba3a"
CERTIFICATE_HASH = "b0ffc8e13badf6faedff7dd821407549e3f4745f7de8a15e6cd765e5163e8fb4"


def identity(path, raw=None):
    if raw is None:
        raw = path.read_bytes()
    return {"filename": path.name, "bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def number(s):
    assert type(s) is str
    q = F(s)
    assert str(q) == s, ("noncanonical rational", s)
    return q


def expression(spec, already_normalized=False):
    """Build immutable syntax trees; repetitions mean fresh copies on expansion.

    Paths are decomposed by their length into one initial length-three block
    when odd and length-two blocks otherwise. All series are left associated.
    This implementation never reads the producer's normalized node indices.
    """
    built = []
    for i, node in enumerate(spec["nodes"]):
        kind = node["kind"]
        if kind == "path":
            length = node["length"]
            assert type(length) is int and length >= 2
            if already_normalized:
                assert length in (2, 3)
            pieces = []
            remaining = length
            if remaining % 2:
                pieces.append(("L", 3))
                remaining -= 3
            while remaining:
                pieces.append(("L", 2))
                remaining -= 2
            value = pieces[0]
            for piece in pieces[1:]:
                value = ("S", value, piece)
        else:
            indices = node["children"]
            assert all(type(j) is int and 0 <= j < i for j in indices)
            children = [built[j] for j in indices]
            if kind == "parallel":
                assert len(children) in (2, 3)
                value = ("P", tuple(children))
            else:
                assert kind in ("series", "series_even_failure")
                assert len(children) >= 2
                if already_normalized:
                    assert kind == "series" and len(children) == 2
                value = children[0]
                for child in children[1:]:
                    value = ("S", value, child)
        built.append(value)
    root = spec["root"]
    assert type(root) is int and 0 <= root < len(built)
    return built[root]


def expand_uncolored(tree, certificate):
    table = {(r["kind"], tuple(r["child_classes"])): r["parent_class"]
             for r in certificate["transitions"]}

    @lru_cache(None)
    def family(t):
        if t[0] == "L":
            return certificate["leaf_classes"][str(t[1])]
        if t[0] == "S":
            return table[("S", (family(t[1]), family(t[2])))]
        return table[("P", tuple(sorted(family(c) for c in t[1])))]

    next_vertex = 2
    edges = []
    counts = Counter()

    def fresh():
        nonlocal next_vertex
        ans = next_vertex
        next_vertex += 1
        return ans

    def edge(u, v):
        edges.append(tuple(sorted((u, v))))

    def visit(t, s, z):
        counts[family(t)] += 1
        if t[0] == "L":
            walk = [s] + [fresh() for _ in range(t[1] - 1)] + [z]
            for a, b in zip(walk, walk[1:]):
                edge(a, b)
        elif t[0] == "S":
            join = fresh()
            visit(t[1], s, join)
            visit(t[2], join, z)
        else:
            a, b = fresh(), fresh()
            edge(s, a)
            edge(b, z)
            for child in t[1]:
                visit(child, a, b)

    visit(tree, 0, 1)
    return next_vertex, edges, family(tree), dict(counts)


def check_graph(record, certificate):
    g = record["graph"]
    tree = expression(record["input_spec"])
    assert tree == expression(g["normalized_spec"], already_normalized=True)
    n, edges, root_family, counts = expand_uncolored(tree, certificate)
    assert n == g["n"] and [list(e) for e in edges] == g["edges"]
    assert g["terminals"] == [0, 1]
    assert root_family == g["root_class"]
    assert counts == g["class_application_counts"]
    assert sum(counts.values()) == g["expanded_applications"]
    assert len(edges) == len(set(edges))
    colors = g["colors"]
    assert len(colors) == n and all(type(c) is int and 0 <= c < 4 for c in colors)
    adj = [set() for _ in range(n)]
    for u, v in edges:
        assert 0 <= u < v < n and colors[u] != colors[v]
        adj[u].add(v)
        adj[v].add(u)
    visited, pending = {0}, [0]
    while pending:
        v = pending.pop()
        for w in adj[v] - visited:
            visited.add(w)
            pending.append(w)
    assert len(visited) == n
    assert len(adj[0]) == len(adj[1]) == 1 and 1 not in adj[0]
    degree = max(map(len, adj))
    assert degree <= 4
    # No edge may be the central edge of a two-colored four-vertex path.
    for u, v in edges:
        left = any(w != v and colors[w] == colors[v] for w in adj[u])
        right = any(w != u and colors[w] == colors[u] for w in adj[v])
        assert not (left and right), ("bichromatic P4", u, v)
    ns, nt = next(iter(adj[0])), next(iter(adj[1]))
    actual_signature = [colors[0], colors[1], colors[ns], colors[nt],
                        int(any(w != 0 and colors[w] == colors[0] for w in adj[ns])),
                        int(any(w != 1 and colors[w] == colors[1] for w in adj[nt]))]
    assert actual_signature == g["root_signature"]
    assert actual_signature in certificate["families"][root_family]
    components = []
    covered = set()
    for a, b in combinations(range(4), 2):
        active = {v for v in range(n) if colors[v] in (a, b)
                  and any(colors[w] in (a, b) for w in adj[v])}
        while active:
            root = min(active)
            nodes, todo = {root}, [root]
            active.remove(root)
            while todo:
                u = todo.pop()
                for v in adj[u]:
                    if colors[v] in (a, b) and v not in nodes:
                        assert v in active
                        active.remove(v)
                        nodes.add(v)
                        todo.append(v)
            induced = {v: adj[v] & nodes for v in nodes}
            centers = [v for v in nodes if len(induced[v]) == len(nodes) - 1]
            assert centers, ("not a star", nodes)
            center = min(centers)
            leaves = sorted(nodes - {center})
            assert all(induced[v] == {center} for v in leaves)
            for leaf in leaves:
                edge = tuple(sorted((center, leaf)))
                assert edge not in covered
                covered.add(edge)
            components.append((center, leaves))
    assert covered == set(edges)
    K = max((1 + len(leaves) for _, leaves in components), default=1)
    assert K == record["maximum_bichromatic_component"]
    assert record["certificate"] == {
        "maximum_degree": degree, "star_verified": True,
        "used_colors": sorted(set(colors)), "all_noise_operator_constant_sq": 2,
        "all_noise_frobenius_constant_sq": 2}
    return n, edges, colors, components, counts, K, degree


def matrix(value, n, support, full=True):
    assert len(value["diagonal"]) == n
    diag = list(map(number, value["diagonal"]))
    edges = {}
    for u, v, x in value["edges"]:
        assert (u, v) in support and (u, v) not in edges
        edges[u, v] = number(x)
    if full:
        assert set(edges) == support
    return diag, edges


def action_rows(value, n):
    assert len(value) == n and all(len(row) == 4 for row in value)
    return [list(map(number, row)) for row in value]


def multiply(colors, diagonal, edge_values):
    ans = [[F(0) for _ in range(4)] for _ in colors]
    for v, d in enumerate(diagonal):
        ans[v][colors[v]] += d
    for (u, v), d in edge_values.items():
        ans[u][colors[v]] += d
        ans[v][colors[u]] += d
    return ans


def inverse_by_star_formula(colors, components, observation):
    diagonal = [observation[v][c] for v, c in enumerate(colors)]
    edge_values = {}
    for center, leaves in components:
        center_color = colors[center]
        leaf_color = colors[leaves[0]]
        leaf_sum = sum((observation[v][center_color] for v in leaves), F(0))
        correction = (observation[center][leaf_color] - leaf_sum) / (len(leaves) + 1)
        for v in leaves:
            edge_values[tuple(sorted((center, v)))] = observation[v][center_color] + correction
    return diagonal, edge_values


def squared_norm(rows):
    return sum((x*x for row in rows for x in row), F(0))


def check_observation(record, n, edges, colors, components):
    support = set(edges)
    diagonal, values = matrix(record["input_matrix"], n, support)
    dh, eh = matrix(record["output_matrix"], n, support)
    E = action_rows(record["noise"], n)
    Y = action_rows(record["full_observed_action"], n)
    # The full explicit inputs are primary; these additional assertions bind the
    # saved deterministic data generator and exclude any silently known diagonal.
    assert diagonal == [F((13*i) % 19 - 9 or 1, 17) for i in range(n)]
    assert values == {(u, v): F((7*u + 11*v) % 23 - 11 or 1, 19) for u, v in edges}
    assert E == [[F((7*(i+3)*(j+5)) % 17 - 8, 1009) for j in range(4)] for i in range(n)]
    assert all(diagonal) and all(values.values())
    Z = multiply(colors, diagonal, values)
    assert Y == [[z + e for z, e in zip(zrow, erow)] for zrow, erow in zip(Z, E)]
    assert inverse_by_star_formula(colors, components, Z) == (diagonal, values)
    assert inverse_by_star_formula(colors, components, Y) == (dh, eh)
    projected = multiply(colors, dh, eh)
    residual = [[p-y for p, y in zip(pr, yr)] for pr, yr in zip(projected, Y)]
    # Independent normal equations characterize the unique Euclidean projection
    # onto the action image. Unused action cells need not have zero noise.
    for v, color in enumerate(colors):
        assert residual[v][color] == 0
    for u, v in edges:
        assert residual[u][colors[v]] + residual[v][colors[u]] == 0
    assert record["noiseless_exact"] is True
    assert number(record["projected_action_residual"]) == 0
    errd = [h-d for h, d in zip(dh, diagonal)]
    erre = {e: eh[e] - values[e] for e in edges}
    nsq = squared_norm(E)
    esq = sum((x*x for x in errd), F(0)) + 2*sum((x*x for x in erre.values()), F(0))
    assert nsq > 0 and nsq == number(record["noise_frobenius_sq"])
    assert esq == number(record["error_frobenius_sq"]) and esq <= 2*nsq
    rowsums = list(map(abs, errd))
    for (u, v), x in erre.items():
        rowsums[u] += abs(x)
        rowsums[v] += abs(x)
    bound = max(rowsums)
    assert bound == number(record["actual_error_absolute_row_sum_upper"])
    return {"noise_frobenius_sq": str(nsq), "error_frobenius_sq": str(esq),
            "actual_error_absolute_row_sum_upper": str(bound),
            "full_action_and_noise_exact": True, "noiseless_inverse_exact": True,
            "saved_output_equals_independent_star_least_squares": True,
            "normal_equations_exact": True, "all_noise_constant_sq": 2}


def bind_predecessor():
    # The sealed return keeps the exact predecessor in sources/. During authoring
    # it was already materialized beside the working tree. Both routes require
    # the identical pinned bytes below; this is a location fallback, not a source
    # or version fallback.
    archive = BASE / "sources" / PREDECESSOR_NAME
    if not archive.is_file():
        archive = BASE.parent / PREDECESSOR_NAME
    raw = archive.read_bytes()
    assert len(raw) == PREDECESSOR_BYTES and sha256(raw).hexdigest() == PREDECESSOR_HASH
    with zipfile.ZipFile(archive) as z:
        native = z.read(NATIVE_MEMBER)
    selected = BASE / "sources/cycle6_selected/failed_even_series_rotation.json"
    assert native == selected.read_bytes()
    assert len(native) == NATIVE_BYTES and sha256(native).hexdigest() == NATIVE_HASH
    return json.loads(native), {"archive": identity(archive, raw),
                               "native_member": NATIVE_MEMBER,
                               "selected_record": identity(selected, native)}


def check_inherited_witness(record, old, n, edges, colors, components, binding):
    assert record["input_spec"] == old["spec"]
    assert n == old["graph"]["n"]
    assert set(edges) == set(map(tuple, old["graph"]["edges"]))
    assert record["inherited_input_identity"] == binding["selected_record"]
    witness = record["inherited_witness_receiving"]
    assert witness["same_original_labeled_support"] is True
    diagonal, values = matrix(witness["matrix"], n, set(edges), full=False)
    assert diagonal == [F(0)] * n
    received = {(u, v): number(x) for u, v, x in old["witness"]["nonzero_matrix_edges"]}
    assert len(received) == len(old["witness"]["nonzero_matrix_edges"])
    assert values == received
    assert values[tuple(old["witness"]["edge"])] == number(old["witness"]["unit_edge_value"]) == 1
    W = multiply(colors, diagonal, values)
    assert W == action_rows(witness["new_four_query_action"], n)
    norm = squared_norm(W)
    assert norm == number(witness["new_action_frobenius_sq"])
    full_values = {edge: values.get(edge, F(0)) for edge in edges}
    assert inverse_by_star_formula(colors, components, W) == (diagonal, full_values)
    assert witness["new_noiseless_reconstruction_exact"] is True
    assert witness["old_three_query_action_frobenius_sq_as_received"] == old["witness"]["action_frobenius_sq"] == "256/16383"
    assert witness["old_design_inverse_lower_sq_as_received"] == old["witness"]["operator_inverse_lower_sq"] == "16383/256"
    assert witness["new_design_uniform_operator_inverse_upper_sq"] == 2
    return {"same_labeled_support": True, "native_cut_matrix_exact": True,
            "native_unit_edge": old["witness"]["edge"],
            "new_full_action_checked": True, "new_action_frobenius_sq": str(norm),
            "new_noiseless_reconstruction_exact": True,
            "old_action_frobenius_sq_received_without_replay": "256/16383",
            "old_inverse_lower_sq_received_without_replay": "16383/256"}


def main():
    start, cpu = time.perf_counter(), time.process_time()
    cert_path = BASE / "results/general_star_certificate.json"
    raw = cert_path.read_bytes()
    assert sha256(raw).hexdigest() == CERTIFICATE_HASH
    certificate = json.loads(raw)
    old, binding = bind_predecessor()
    outputs = []
    names = ("star_three_obstruction_17", "arbitrary_paths_and_both_parities", "same_saved_Q8_support")
    for name in names:
        t = time.perf_counter()
        path = BASE / "results" / (name + ".json")
        raw = path.read_bytes()
        record = json.loads(raw)
        assert record["name"] == name
        n, edges, colors, components, counts, K, degree = check_graph(record, certificate)
        result = {"name": name, "source": identity(path, raw), "n": n, "m": len(edges),
                  "maximum_degree": degree, "maximum_bichromatic_component": K,
                  "class_counts": counts, "status": "PASS"}
        result.update(check_observation(record, n, edges, colors, components))
        if name == "same_saved_Q8_support":
            result["inherited_witness"] = check_inherited_witness(record, old, n, edges, colors, components, binding)
        result["wall_seconds"] = time.perf_counter() - t
        outputs.append(result)
    result = {"status": "PASS", "method": "Source-informed independent standard-library checker; no producer imports or execution",
              "certificate": identity(cert_path), "predecessor_binding": binding,
              "receiving_uses": outputs,
              "cost": {"wall_seconds": time.perf_counter() - start,
                       "cpu_seconds": time.process_time() - cpu,
                       "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
                       "includes": "Exact source reading/hashing, native ZIP binding, independent graph expansion, star checks, full action/noise/LS/norm checks for all three saved uses and inherited witness",
                       "excludes": "Process startup, checker authoring, proof reading/review, final JSON serialization; those totals remain unknown"},
              "scope": "Verifies these concrete saved receiving uses. The general all-depth consequence uses the separately checked 200-witness finite certificate and port proof. No all-real three-query lower, full-class coverage, external acceptance or speedup is inferred."}
    (OUT / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
