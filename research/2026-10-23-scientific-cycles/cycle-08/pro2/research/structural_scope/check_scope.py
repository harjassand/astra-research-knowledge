"""Independent structural diagnostics for the new loaded-port grammar.

No producer imports, coloring search, or old scientific replay. The all-size
result is PROOF.md; this checks its exact new expressions and exclusion input.
"""
from pathlib import Path
import json
import time
import resource


def path(k):
    return {"op": "path", "length": k}


def compose(op, *children):
    return {"op": op, "children": list(children)}


def expand(spec):
    op = spec["op"]
    if op == "path":
        k = spec["length"]
        assert isinstance(k, int) and k >= 2
        return k + 1, [(i, i + 1) for i in range(k)], (0, k)
    children = [expand(x) for x in spec["children"]]
    if op in ("left", "right"):
        assert len(children) == 1
        n, es, (s, t) = children[0]
        old = s if op == "left" else t
        assert sum(old in e for e in es) <= 3
        es = es + [(old, n)]
        st = (n, t) if op == "left" else (s, n)
        return n + 1, es, st
    assert op in ("series", "parallel") and len(children) >= 2
    vertices = []
    edges = []
    endpoints = []
    offset = 0
    for n, es, (s, t) in children:
        vertices.extend(range(offset, offset + n))
        edges.extend((u + offset, v + offset) for u, v in es)
        endpoints.append((s + offset, t + offset))
        offset += n
    parent = list(range(offset))

    def find(a):
        while a != parent[a]:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def join(a, b):
        parent[find(b)] = find(a)

    if op == "parallel":
        for s, t in endpoints[1:]:
            join(endpoints[0][0], s)
            join(endpoints[0][1], t)
        st = endpoints[0]
    else:
        for (_, t), (s, _) in zip(endpoints, endpoints[1:]):
            join(t, s)
        st = (endpoints[0][0], endpoints[-1][1])
    ids = {r: i for i, r in enumerate(sorted({find(v) for v in vertices}))}
    out = [tuple(sorted((ids[find(u)], ids[find(v)]))) for u, v in edges]
    assert all(u != v for u, v in out) and len(set(out)) == len(out)
    n = len(ids)
    deg = [0] * n
    for u, v in out:
        deg[u] += 1
        deg[v] += 1
    assert max(deg) <= 4
    st = tuple(ids[find(v)] for v in st)
    assert tuple(sorted(st)) not in out
    return n, out, st


def adjacency(n, es):
    a = [set() for _ in range(n)]
    for u, v in es:
        a[u].add(v)
        a[v].add(u)
    return a


def terminal_paths(a, s, t):
    def visit(p):
        u = p[-1]
        if u == t:
            yield p
        else:
            for v in sorted(a[u] - set(p)):
                yield from visit(p + [v])
    yield from visit([s])


def induced(a, p):
    return all(v not in a[u] for i, u in enumerate(p)
               for v in p[i + 2:])


def connected_after(a, removed):
    allowed = set(range(len(a))) - set(removed)
    if not allowed:
        return True
    seen = {min(allowed)}
    stack = list(seen)
    while stack:
        v = stack.pop()
        for w in a[v] & (allowed - seen):
            seen.add(w)
            stack.append(w)
    return seen == allowed


def atom_expression(length):
    p2 = path(2)
    branch = compose("series", compose("parallel", p2, p2), path(length))
    return compose("parallel", p2, p2, branch)


def main():
    start = time.perf_counter()
    records = []
    for length in (2, 3):
        spec = atom_expression(length)
        n, es, (s, t) = expand(spec)
        a = adjacency(n, es)
        assert (n, len(es)) == (length + 6, length + 8)
        assert (len(a[s]), len(a[t])) == (4, 3)
        assert sorted(map(len, a)) == [2] * (n - 3) + [3, 3, 4]
        ps = list(terminal_paths(a, s, t))
        assert ps and all(induced(a, p) for p in ps)
        assert all(connected_after(a, [v]) for v in range(n))
        assert all(connected_after(a, [u, v]) for u, v in es)
        records.append({"name": f"A_{length}", "spec": spec, "n": n,
                        "edges": es, "terminals": [s, t],
                        "loads": [len(a[s]), len(a[t])],
                        "terminal_path_count": len(ps),
                        "all_terminal_paths_induced": True,
                        "two_connected_and_no_clique_cutset": True})

    # Exact translation of one old stubbed node, showing the retained stubs.
    old = compose("right", compose("left", compose("parallel", path(2), path(2), path(2))))
    n, es, (s, t) = expand(old)
    a = adjacency(n, es)
    assert len(a[s]) == len(a[t]) == 1
    assert len(a[next(iter(a[s]))]) == len(a[next(iter(a[t]))]) == 4
    translation = {"spec": old, "n": n, "edges": es, "terminals": [s, t],
                   "terminal_loads": [1, 1], "stub_neighbor_loads": [4, 4]}

    # Actual graph outside the augmented grammar, by the universal path invariant.
    bad_es = [(0, 1), (1, 2), (2, 3), (0, 3), (0, 4), (1, 5)]
    a = adjacency(6, bad_es)
    bad_path = [4, 0, 3, 2, 1, 5]
    assert not induced(a, bad_path)
    assert [v for v in range(6) if len(a[v]) == 1] == [4, 5]
    bad = {"name": "four_cycle_with_leaves_at_adjacent_vertices", "n": 6,
           "edges": bad_es, "forced_terminals": [4, 5],
           "noninduced_terminal_path": bad_path, "chord": [0, 1]}
    result = {"schema": "astra-cycle8-loaded-port-structural-diagnostic/v1",
              "new_atoms": records, "old_stubbed_node_translation": translation,
              "remaining_scope_exclusion": bad,
              "passed": True, "wall_seconds_body": time.perf_counter() - start,
              "process_max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "scientific_scope": "Finite diagnostics supplement PROOF.md; they are not the all-size proof."}
    out = Path(__file__).with_name("RESULT.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("passed", "wall_seconds_body", "process_max_rss_kib")}))


if __name__ == "__main__":
    main()
