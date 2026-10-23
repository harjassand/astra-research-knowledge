#!/usr/bin/env python3
"""Independent exact checker of Cycle11 native original-action receiving data.

Only Python's standard library is imported. No producer code or old closure
certificate is imported or executed. This checks saved receiving instances,
not the universal existence theorem for every admitted graph.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import resource
import time


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def canon(e):
    u, v = e
    require(u != v, "loop in simple original graph")
    return min(u, v), max(u, v)


def adjacency(n, edges):
    a = [set() for _ in range(n)]
    for u, v in edges:
        require(0 <= u < n and 0 <= v < n, "out-of-range endpoint")
        a[u].add(v)
        a[v].add(u)
    return a


def components(vertices, adj):
    remaining = set(vertices)
    out = []
    while remaining:
        root = min(remaining)
        stack, found = [root], {root}
        remaining.remove(root)
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v in remaining:
                    remaining.remove(v)
                    found.add(v)
                    stack.append(v)
        out.append(frozenset(found))
    return out


def find_bridges(n, adj):
    tin, low, counter, ans = [-1] * n, [0] * n, 0, set()

    def dfs(u, parent):
        nonlocal counter
        tin[u] = low[u] = counter
        counter += 1
        for v in sorted(adj[u]):
            if v == parent:
                continue
            if tin[v] < 0:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    ans.add(canon((u, v)))
            else:
                low[u] = min(low[u], tin[v])

    for u in range(n):
        if tin[u] < 0:
            dfs(u, -1)
    return ans


def biconnected_edge_blocks(n, adj):
    tin, low, clock, stack, blocks = [-1] * n, [0] * n, 0, [], []

    def dfs(u, parent):
        nonlocal clock
        tin[u] = low[u] = clock
        clock += 1
        for v in sorted(adj[u]):
            e = canon((u, v))
            if v == parent:
                continue
            if tin[v] < 0:
                stack.append(e)
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] >= tin[u]:
                    block = set()
                    while True:
                        popped = stack.pop()
                        block.add(popped)
                        if popped == e:
                            break
                    blocks.append(frozenset(block))
            elif tin[v] < tin[u]:
                stack.append(e)
                low[u] = min(low[u], tin[v])

    for u in range(n):
        if tin[u] < 0:
            dfs(u, -1)
    return blocks


def width_two_order(n, adj):
    work = [set(x) for x in adj]
    active, order = set(range(n)), []
    while active:
        choices = [u for u in active if len(work[u]) <= 2]
        require(choices, "degree-two elimination with fill stuck")
        u = min(choices)
        ns = sorted(work[u])
        fill = None
        if len(ns) == 2 and ns[1] not in work[ns[0]]:
            x, y = ns
            work[x].add(y)
            work[y].add(x)
            fill = [x, y]
        order.append({"vertex": u, "later_neighbors": ns, "fill_edge": fill})
        for v in ns:
            work[v].remove(u)
        active.remove(u)
        work[u].clear()
    return order


def disjoint_paths_after_edge_removal(n, edges, removed):
    """Vertex-capacitated integral maxflow, stopped after two units."""
    s, t = removed
    cap = [dict() for _ in range(2 * n)]

    def add(u, v, value):
        cap[u][v] = cap[u].get(v, 0) + value
        cap[v].setdefault(u, 0)

    for v in range(n):
        add(2 * v, 2 * v + 1, 2 if v in (s, t) else 1)
    for u, v in edges:
        if (u, v) != removed:
            add(2 * u + 1, 2 * v, 2)
            add(2 * v + 1, 2 * u, 2)
    source, sink, value = 2 * s + 1, 2 * t, 0
    while value < 2:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v, c in cap[u].items():
                if c > 0 and v not in parent:
                    parent[v] = u
                    queue.append(v)
        if sink not in parent:
            break
        v = sink
        while v != source:
            u = parent[v]
            cap[u][v] -= 1
            cap[v][u] += 1
            v = u
        value += 1
    return value


def check_chordless(n, edges, adj, bridges):
    flow_checked, endpoint_shortcuts, bridge_shortcuts = [], 0, 0
    for e in sorted(edges):
        u, v = e
        if e in bridges:
            bridge_shortcuts += 1
        elif min(len(adj[u]), len(adj[v])) <= 2:
            endpoint_shortcuts += 1
        else:
            value = disjoint_paths_after_edge_removal(n, edges, e)
            require(value < 2, f"original edge {e} is a chord")
            flow_checked.append({"edge": list(e), "maximum_disjoint_paths": value})
    return {
        "edge_flow_checks": flow_checked,
        "degree_endpoint_shortcuts": endpoint_shortcuts,
        "bridge_shortcuts": bridge_shortcuts,
        "criterion": "G-e has no two internally vertex-disjoint endpoint paths for every original edge e",
    }


def pair_components(n, edges, colors, q):
    out = []
    for a in range(q):
        for b in range(a + 1, q):
            es = [e for e in edges if {colors[e[0]], colors[e[1]]} == {a, b}]
            ad = adjacency(n, es)
            vertices = {v for e in es for v in e}
            for vs in components(vertices, ad):
                ces = sorted(e for e in es if e[0] in vs)
                require(len(ces) == len(vs) - 1, "bichromatic cycle")
                out.append({"pair": (a, b), "vertices": vs, "edges": ces, "adj": ad})
    return out


def short_spider_center(vertices, adj):
    """Direct shape check: all off-center degrees <=2 and all distances <=2."""
    vs = set(vertices)
    for center in sorted(vs):
        if any(len(adj[u] & vs) > 2 for u in vs if u != center):
            continue
        dist = {center: 0}
        queue = deque([center])
        while queue:
            u = queue.popleft()
            for v in adj[u] & vs:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        if set(dist) == vs and max(dist.values()) <= 2:
            return center
    raise AssertionError("non-short-spider module core")


def atom_profile(n, edges, colors, mark, q):
    ad = adjacency(n, edges)
    mult = [0] * q
    flags = set()
    for u in ad[mark]:
        mult[colors[u]] += 1
        if any(v != mark and colors[v] == colors[mark] for v in ad[u]):
            flags.add(colors[u])
    return {
        "color": colors[mark], "degree": len(ad[mark]),
        "neighbor_colors": [c for c in range(q) if mult[c]],
        "neighbor_color_multiplicities": mult,
        "far_flags": sorted(flags),
    }


def exact_positive_gram(component):
    """Exact LDL certificate of 9 Q^T Q - I >0, for unsigned incidence Q.

    Thus sigma_min(Q)^2>=1/9, and the pair LS Frobenius-output
    noise norm squared is at most 2/(1/9)=18.
    """
    es = component["edges"]
    k = len(es)
    mat = [[F(17 if i == j else 9 * len(set(es[i]) & set(es[j])))
            for j in range(k)] for i in range(k)]
    pivots = []
    for i in range(k):
        p = mat[i][i]
        require(p > 0, "exact incidence Gram lower-bound failed")
        pivots.append(str(p))
        for j in range(i + 1, k):
            for l in range(j, k):
                mat[j][l] -= mat[j][i] * mat[l][i] / p
                mat[l][j] = mat[j][l]
    return {"pair": list(component["pair"]),
            "vertices": sorted(component["vertices"]),
            "ordered_edges": [list(e) for e in es], "ldl_pivots": pivots}


def decode(n, edges, colors, q, observation, pcs):
    diagonal = [observation[u][colors[u]] for u in range(n)]
    output = {}
    projection = [[F(0) for _ in range(q)] for _ in range(n)]
    for u in range(n):
        projection[u][colors[u]] = diagonal[u]
    for pc in pcs:
        a, b = pc["pair"]
        vs = pc["vertices"]
        sign = {u: (1 if colors[u] == a else -1) for u in vs}
        other = {u: (b if colors[u] == a else a) for u in vs}
        signed = {u: sign[u] * observation[u][other[u]] for u in vs}
        mean = sum(signed.values(), F(0)) / len(vs)
        balance = {u: signed[u] - mean for u in vs}
        for u in vs:
            projection[u][other[u]] = sign[u] * balance[u]
        work = {u: set(pc["adj"][u]) for u in vs}
        queue = deque(sorted(u for u in vs if len(work[u]) == 1))
        while queue:
            u = queue.popleft()
            if len(work[u]) != 1:
                continue
            v = next(iter(work[u]))
            value = sign[u] * balance[u]
            output[canon((u, v))] = value
            balance[v] -= sign[v] * value
            balance[u] = F(0)
            work[v].remove(u)
            work[u].clear()
            if len(work[v]) == 1:
                queue.append(v)
        require(all(x == 0 for x in balance.values()), "leaf-incidence terminal imbalance")
    require(set(output) == set(edges), "incomplete sparse inverse")
    return diagonal, output, projection


def action(n, colors, q, diagonal, coefficients):
    out = [[F(0) for _ in range(q)] for _ in range(n)]
    for u, d in enumerate(diagonal):
        out[u][colors[u]] += d
    for (u, v), d in coefficients.items():
        out[u][colors[v]] += d
        out[v][colors[u]] += d
    return out


def matrix(x, n, q):
    require(len(x) == n and all(len(row) == q for row in x), "wrong action dimensions")
    return [[F(v) for v in row] for row in x]


def coeffs(x, n, edges):
    d = [F(v) for v in x["diagonal"]]
    require(len(d) == n, "wrong diagonal dimension")
    es = [canon(v["edge"]) for v in x["edges"]]
    require(len(es) == len(set(es)) and set(es) == set(edges), "coefficients change original support")
    return d, {canon(v["edge"]): F(v["value"]) for v in x["edges"]}


def norm_sq(x):
    return sum((v * v for row in x for v in row), F(0))


def cut_gamma(pcs):
    answer = F(0)
    for pc in pcs:
        size = len(pc["vertices"])
        for u, v in pc["edges"]:
            seen, stack = {u}, [u]
            while stack:
                x = stack.pop()
                for y in pc["adj"][x]:
                    if canon((x, y)) == canon((u, v)) or y in seen:
                        continue
                    seen.add(y)
                    stack.append(y)
            a = len(seen)
            answer = max(answer, F(a * (size - a), size))
    return answer


def verify_structure(native, saved):
    n = native["n"]
    raw_edges = [canon(e) for e in native["edges"]]
    require(len(raw_edges) == len(set(raw_edges)), "duplicate original edge")
    edges = sorted(raw_edges)
    ad = adjacency(n, edges)
    require(max(map(len, ad), default=0) <= 4, "degree exceeds four")
    require(saved["n"] == n and saved["m"] == len(edges), "input n,m binding mismatch")
    des, q = saved["design"], saved["q"]
    colors = des["colors"]
    require(q == 4 and des["q"] == q, "query count mismatch")
    require(len(colors) == n and all(isinstance(c, int) and 0 <= c < q for c in colors), "invalid query rows")
    require(all(colors[u] != colors[v] for u, v in edges), "improper coordinate design")
    bridges = find_bridges(n, ad)
    require({canon(b["edge"]) for b in des["bridges"]} == bridges, "bridge inventory mismatch")
    core_ad = adjacency(n, [e for e in edges if e not in bridges])
    modules = components(range(n), core_ad)
    require({frozenset(m["original_vertex_ids"]) for m in des["modules"]} == set(modules), "native module mismatch")
    require(sum(len(m["original_vertex_ids"]) for m in des["modules"]) == n, "overlapping modules")
    module_by_id = {m["module"]: m for m in des["modules"]}
    require(len(module_by_id) == len(modules), "duplicate module IDs")
    module_of = {v: m["module"] for m in des["modules"] for v in m["original_vertex_ids"]}
    actual_blocks = biconnected_edge_blocks(n, core_ad)
    recorded_blocks = []
    degree_three_entries, family_ids, stop_messages = [], [], 0
    for m in des["modules"]:
        ids, cert = m["original_vertex_ids"], m["certificate"]
        require(cert["colors"] == [colors[v] for v in ids], "module colors differ from full X")
        for block in cert["blocks"]:
            vids = [ids[i] for i in block["vertex_ids"]]
            atom = block["atom_certificate"]
            aes = [canon(e) for e in atom["edges"]]
            mapped = frozenset(canon((vids[u], vids[v])) for u, v in aes)
            recorded_blocks.append(mapped)
            require(mapped <= set(edges), "normalizer-only edge leaked into block")
            ac = atom["colors"]
            require([block["permutation"][c] for c in ac] == block["colors"] == [colors[v] for v in vids], "atom color transfer mismatch")
            require(all(ac[u] != ac[v] for u, v in aes), "atom improper")
            apcs = pair_components(len(vids), aes, ac, q)
            for pc in apcs:
                require(sum(len(pc["adj"][u]) > 1 for u in pc["vertices"]) <= 1, "recorded atom coloring is not star")
            profile = atom_profile(len(vids), aes, ac, atom["mark"], q)
            for key in ("color", "degree", "neighbor_colors", "neighbor_color_multiplicities", "far_flags"):
                require(atom["profile"][key] == profile[key], f"actual atom profile mismatch: {key}")
            if profile["degree"] == 3:
                family_ids.append(atom["root_family"])
                require(len(profile["neighbor_colors"]) <= 2, "degree-three atom root lacks a missing channel")
            if block.get("outgoing_stop_message") is not None:
                stop_messages += 1
        entry, parent = m["original_entry"], m["original_parent_endpoint"]
        if entry is not None and len(ids) > 1:
            require(entry in ids and parent not in ids, "invalid original module entry")
            ns = core_ad[entry]
            mult = [sum(colors[u] == c for u in ns) for c in range(q)]
            eq = cert["entry_qualification"]
            require(eq["vertex"] == ids.index(entry) and eq["color"] == colors[entry], "entry identity mismatch")
            require(eq["incoming_color"] == colors[parent] and eq["actual_degree"] == len(ns), "entry degree/channel mismatch")
            require(eq["neighbor_color_multiplicities"] == mult, "entry actual multiplicity mismatch")
            require(mult[colors[parent]] == 0, "incoming bridge color occurs inside child module")
            if len(ns) == 3:
                degree_three_entries.append({"vertex": entry, "parent": parent, "internal_neighbors": sorted(ns), "multiplicities": mult})
    require(Counter(recorded_blocks) == Counter(actual_blocks), "native biconnected block mismatch")
    indegree, reset_count, oriented = Counter(), 0, []
    for br in des["bridges"]:
        u, v = br["edge"]
        pm, cm = br["parent_module"], br["child_module"]
        require(module_of[u] == pm and module_of[v] == cm, "oriented bridge/module mismatch")
        require(module_by_id[cm]["original_entry"] == v and module_by_id[cm]["original_parent_endpoint"] == u, "child entry binding mismatch")
        require(br["parent_color"] == colors[u] and br["child_color"] == colors[v], "bridge colors mismatch")
        indegree[cm] += 1
        require(indegree[cm] == 1, "module has two incoming bridges")
        par = module_by_id[pm]
        reset = u == par["original_entry"]
        forbidden = {colors[u]}
        if reset:
            forbidden.add(colors[par["original_parent_endpoint"]])
            reset_count += 1
        require(br["entry_vertex_reset"] == reset and set(br["forbidden_colors"]) == forbidden, "same-entry reset metadata mismatch")
        require(colors[v] not in forbidden, "same-entry outgoing bridge reused incoming channel")
        require([w for w in ad[v] if colors[w] == colors[u]] == [u], "child endpoint is not a leaf in incoming pair")
        oriented.append({"parent_module": pm, "child_module": cm, "edge": [u, v]})
    pcs = pair_components(n, edges, colors, q)
    recorded = {(tuple(c["pair"]), frozenset(c["vertices"])): c for c in des["components"]}
    require(len(recorded) == len(des["components"]), "duplicate component certificates")
    require(set(recorded) == {(c["pair"], c["vertices"]) for c in pcs}, "component inventory mismatch")
    core_records, gram_records = [], []
    for pc in pcs:
        ces = [e for e in pc["edges"] if e not in bridges]
        bes = [e for e in pc["edges"] if e in bridges]
        rec = recorded[(pc["pair"], pc["vertices"])]
        require({canon(e) for e in rec["core_edges"]} == set(ces), "component core edge mismatch")
        require({canon(e) for e in rec["bridges"]} == set(bes), "component bridge edge mismatch")
        if ces:
            cvs = {v for e in ces for v in e}
            require(len({module_of[v] for v in cvs}) == 1, "two module cores in one pair component")
            require(len(components(cvs, pc["adj"])) == 1, "disconnected core")
            cad = adjacency(n, ces)
            center = short_spider_center(cvs, cad)
            for v in pc["vertices"] - cvs:
                require(len(pc["adj"][v]) == 1, "nonpendant vertex outside module core")
                require(next(iter(pc["adj"][v])) in cvs, "pendant does not meet core")
            require(rec["kind"] == "one_spider_plus_pendants" and set(rec["core_vertices"]) == cvs, "saved one-core shape mismatch")
            core_records.append({"pair": list(pc["pair"]), "vertices": sorted(pc["vertices"]), "core_vertices": sorted(cvs), "independent_center": center})
        else:
            center = max(pc["vertices"], key=lambda u: len(pc["adj"][u]))
            require(all(u == center or len(pc["adj"][u]) == 1 for u in pc["vertices"]), "bridge-only pair component is not a star")
            require(rec["kind"] == "bridge_star", "saved bridge-star kind mismatch")
        gram_records.append(exact_positive_gram(pc))
    summary = saved["summary"]
    require(summary["internal_stop_messages"] == stop_messages, "internal-stop count mismatch")
    require(summary["entry_vertex_bridge_resets"] == reset_count, "bridge-reset count mismatch")
    require(summary["degree3_families"] == family_ids, "observed family label mismatch")
    require(saved["largest_component_vertices"] == max(map(lambda pc: len(pc["vertices"]), pcs), default=1), "largest component mismatch")
    gamma = cut_gamma(pcs)
    require(F(saved["actual_cut_gamma"]) == gamma, "cut balance mismatch")
    report = {
        "n": n, "m": len(edges), "q": q, "maximum_degree": max(map(len, ad)),
        "whole_row_norm_squared": 1,
        "original_bridge_count": len(bridges), "native_module_count": len(modules),
        "native_atom_count": len(actual_blocks), "bridge_reset_count": reset_count,
        "degree_three_entries": degree_three_entries, "observed_family_labels": family_ids,
        "internal_stop_messages": stop_messages,
        "bichromatic_tree_components": len(pcs), "cut_gamma": str(gamma),
        "width_two_elimination": width_two_order(n, ad),
        "chordless_check": check_chordless(n, edges, ad, bridges),
        "direct_component_structure": core_records,
        "exact_gram_certificates": gram_records,
    }
    return edges, colors, pcs, report


def verify_operation(native, saved):
    started, cpu = time.perf_counter(), time.process_time()
    edges, colors, pcs, report = verify_structure(native, saved)
    n, q = native["n"], saved["q"]
    d, es = coeffs(saved["original_coefficients"], n, edges)
    e = matrix(saved["noise"], n, q)
    full = action(n, colors, q, d, es)
    require(full == matrix(saved["full_noiseless_actions"], n, q), "not the full original D X")
    obs = [[full[i][j] + e[i][j] for j in range(q)] for i in range(n)]
    require(obs == matrix(saved["observations"], n, q), "original action plus noise mismatch")
    d0, es0, _ = decode(n, edges, colors, q, full, pcs)
    require(d0 == d and es0 == es, "independent noiseless recovery failed")
    dh, eh, proj = decode(n, edges, colors, q, obs, pcs)
    ds, ets = coeffs(saved["output"], n, edges)
    require(dh == ds and eh == ets, "independent LS inverse differs from saved output")
    predicted = action(n, colors, q, dh, eh)
    require(predicted == proj == matrix(saved["projected_actions"], n, q), "exact projected-action residual is nonzero")
    residual = [[obs[i][j] - predicted[i][j] for j in range(q)] for i in range(n)]
    require(residual == matrix(saved["raw_residual"], n, q), "raw residual mismatch")
    require(all(residual[u][colors[u]] == 0 for u in range(n)), "diagonal normal equation failed")
    require(all(residual[u][colors[v]] + residual[v][colors[u]] == 0 for u, v in edges), "edge normal equation failed")
    err_sq = sum(((dh[u] - d[u]) ** 2 for u in range(n)), F(0)) + 2 * sum(((eh[t] - es[t]) ** 2 for t in edges), F(0))
    noise_sq = norm_sq(e)
    raw_sq = norm_sq(residual)
    require(err_sq <= 18 * noise_sq, "squared Frobenius error bound 18 failed")
    for key, value in (("error_frobenius_sq", err_sq), ("noise_frobenius_sq", noise_sq), ("raw_residual_norm_sq", raw_sq), ("projected_numerical_residual_norm_sq", F(0))):
        require(F(saved[key]) == value, "saved norm mismatch: " + key)
    require(F(saved["ratio_frobenius_sq"]) == err_sq / noise_sq, "error/noise ratio mismatch")
    report.update({
        "name": saved["name"], "status": "PASS",
        "exact_original_actions": True, "independent_exact_LS_output": True,
        "normal_equations": True, "exact_noiseless_recovery": True,
        "projected_action_residual_norm_squared": "0",
        "raw_residual_norm_squared": str(raw_sq),
        "noise_frobenius_squared": str(noise_sq),
        "error_frobenius_squared": str(err_sq),
        "actual_squared_error_ratio": str(err_sq / noise_sq),
        "certified_squared_Frobenius_and_operator_inverse_upper": 18,
        "checking_body_wall_seconds": time.perf_counter() - started,
        "checking_body_cpu_seconds": time.process_time() - cpu,
    })
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started, cpu = time.perf_counter(), time.process_time()
    receiving_path = args.root / "results" / "RECEIVING.json"
    receiving_bytes = receiving_path.read_bytes()
    payload = json.loads(receiving_bytes)
    require(payload["schema"] == "astra-cycle11-original-actions/v1", "unknown receiving schema")
    inputs = {}
    bindings = []
    for item in payload["input_bindings"]:
        path = args.root / item["path"]
        data = path.read_bytes()
        require(len(data) == item["bytes"] and hashlib.sha256(data).hexdigest() == item["sha256"], "input bytes/hash binding failed")
        native = json.loads(data)
        require(native["name"] not in inputs, "duplicate native input name")
        inputs[native["name"]] = native
        bindings.append(item)
    checked_source_hashes = {}
    for name, digest in payload["source_hashes"].items():
        data = (args.root / "src" / name).read_bytes()
        require(hashlib.sha256(data).hexdigest() == digest, "saved producer source hash mismatch: " + name)
        checked_source_hashes[name] = digest
    reports = [verify_operation(inputs[op["name"]], op) for op in payload["operations"]]
    require(set(inputs) == {op["name"] for op in payload["operations"]}, "unused or unbound original graph")
    iso = payload["isolated_direct_sum_check"]
    require(iso["n"] == 3 and iso["edges"] == [] and iso["colors"] == [0, 0, 0], "isolated direct-sum schema mismatch")
    io = matrix(iso["observations"], 3, 4)
    idh, ies, ip = decode(3, [], iso["colors"], 4, io, [])
    require(idh == list(map(F, iso["recovered_diagonal"])) and not ies, "isolated direct-sum inverse failed")
    require(action(3, iso["colors"], 4, idh, ies) == ip, "isolated projection residual")
    result = {
        "schema": "astra-cycle11-independent-receiving/v1", "status": "PASS",
        "receiving_bytes": len(receiving_bytes),
        "receiving_sha256": hashlib.sha256(receiving_bytes).hexdigest(),
        "input_bindings": bindings, "checked_source_hashes": checked_source_hashes,
        "operations": reports, "isolated_direct_sum": "PASS",
        "no_producer_imports": True,
        "scope": "Exact receiving instances, original graph properties and all-noise inverse bound for their saved coordinate designs; not a universal graph-coloring existence theorem.",
        "unexercised_inherited_branch": "Nonzero internal block stop messages: observed count is zero in both native receivers.",
        "checking_body_wall_seconds_before_serialization": time.perf_counter() - started,
        "checking_body_cpu_seconds_before_serialization": time.process_time() - cpu,
        "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
        "authoring_and_discovery_cost_seconds": None,
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(json.dumps({k: result[k] for k in ("status", "receiving_sha256", "checking_body_wall_seconds_before_serialization", "checking_body_cpu_seconds_before_serialization", "peak_rss_bytes")}, indent=2))
    for op in reports:
        print(json.dumps({k: op[k] for k in ("name", "n", "m", "status", "actual_squared_error_ratio", "internal_stop_messages", "bridge_reset_count")}))


if __name__ == "__main__":
    main()
