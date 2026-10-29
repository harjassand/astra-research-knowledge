"""Exact new-scope control: locally nonstationary modules, stationary assembly.

No producer imports or source observations. All assertions use Fraction.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def solve(a, b):
    n = len(a)
    if not n:
        return []
    vector = not isinstance(b[0], list)
    rhs = [[F(x)] for x in b] if vector else [[F(x) for x in r] for r in b]
    q = len(rhs[0])
    z = [[F(x) for x in a[i]] + rhs[i] for i in range(n)]
    for j in range(n):
        p = next(i for i in range(j, n) if z[i][j])
        z[j], z[p] = z[p], z[j]
        aij = z[j][j]
        z[j] = [x / aij for x in z[j]]
        for i in range(n):
            if i != j and z[i][j]:
                v = z[i][j]
                z[i] = [z[i][k] - v * z[j][k] for k in range(n + q)]
    ans = [r[n:] for r in z]
    return [r[0] for r in ans] if vector else ans


def laplacian(size, edges):
    L = [[F(0) for _ in range(size)] for _ in range(size)]
    for i, j, f in edges:
        f = F(f)
        assert f > 0 and i != j
        L[i][i] += f
        L[i][j] -= f
    assert all(sum(r) == 0 for r in L)
    return L


def local_record(ports, hidden, edges, weights):
    ids = ports + hidden
    index = {x: i for i, x in enumerate(ids)}
    local_edges = [(index[i], index[j], f) for i, j, f in edges]
    L = laplacian(len(ids), local_edges)
    m, k = len(ports), len(hidden)
    wB, wI = [weights[x] for x in ports], [weights[x] for x in hidden]
    column_sums = [sum(L[i][j] for i in range(m + k)) for j in range(m + k)]
    assert all(v == 0 for v in column_sums[m:])
    assert column_sums[:m] != [0] * m
    G = [r[m:] for r in L[m:]]
    BI = [r[m:] for r in L[:m]]
    IB = [r[:m] for r in L[m:]]
    X = solve(G, IB)
    t = solve(G, wI)
    S = [[L[i][j] - dot(BI[i], [r[j] for r in X]) for j in range(m)]
         for i in range(m)]
    bR = [wB[i] - dot(BI[i], t) for i in range(m)]
    bL = [wB[j] - sum(wI[i] * X[i][j] for i in range(k)) for j in range(m)]
    Y = solve(G, [[wI[i] * X[i][j] for j in range(m)] for i in range(k)])
    M = [[dot(BI[i], [r[j] for r in Y]) for j in range(m)] for i in range(m)]
    c = dot(wI, t)
    assert [sum(r) for r in M] == [bR[i] - wB[i] for i in range(m)]
    assert [sum(M[i][j] for i in range(m)) for j in range(m)] == [bL[j] - wB[j] for j in range(m)]
    assert sum(bR) == sum(bL) == sum(wB) + sum(wI)
    assert [sum(S[i][j] for i in range(m)) for j in range(m)] == column_sums[:m]
    assert all(sum(r) == 0 for r in S)
    return {"S": S, "bR": bR, "bL": bL, "c": c, "M": M,
            "port_divergence": column_sums[:m], "mass": sum(bR)}


def make_network(replacement):
    cross = [(1, 2, F(1)), (3, 0, F(1))]
    if not replacement:
        weights = list(map(F, [1, 1, 1, 1, 1, 2, 1, 1, 1]))
        localA = [(0, 4, 1), (4, 5, 1), (5, 1, 1)]
        localB = [(2, 6, 1), (6, 7, 1), (7, 8, 1), (8, 3, 1)]
        hidden = [[4, 5], [6, 7, 8]]
    else:
        weights = list(map(F, [1, 1, 1, 1])) + [F(5, 6)] * 3 + [F(1, 2)] + [F(1)] * 3
        localA = [(0, 1, F(1, 6)), (0, 4, F(5, 6)),
                  (4, 5, F(5, 6)), (5, 6, F(5, 6)),
                  (6, 1, F(1, 3)), (6, 7, F(1, 2)), (7, 1, F(1, 2))]
        localB = [(2, 8, 1), (8, 9, 1), (9, 10, 1), (10, 3, 1)]
        hidden = [[4, 5, 6, 7], [8, 9, 10]]
    edges = localA + localB + cross
    L = laplacian(len(weights), edges)
    assert all(sum(L[i][j] for i in range(len(weights))) == 0 for j in range(len(weights)))
    for reverse in [False, True]:
        seen, todo = {0}, [0]
        while todo:
            x = todo.pop()
            for i, j, f in edges:
                if reverse:
                    i, j = j, i
                if i == x and j not in seen:
                    seen.add(j)
                    todo.append(j)
        assert seen == set(range(len(weights)))
    rates = [L[i][i] / weights[i] for i in range(len(weights))]
    assert rates[:4] == [1] * 4
    assert all(r <= 1 for r in rates[4:])
    if replacement:
        assert all(r == 1 for r in rates[4:])
    local = [local_record([0, 1], hidden[0], localA, weights),
             local_record([2, 3], hidden[1], localB, weights)]
    for r in local:
        assert r["S"] == [[1, -1], [0, 0]]
        assert r["bR"] == [4, 1]
        assert r["bL"] == [1, 4]
        assert r["M"] == [[0, 3], [0, 0]]
        assert r["port_divergence"] == [1, -1]
    assert [r["c"] for r in local] == [7, 6]
    trace_edges = [(0, 1, 1), (2, 3, 1)] + cross
    K = laplacian(4, trace_edges)
    budgets = [weights[i] - K[i][i] for i in range(4)]
    assert budgets == [0] * 4
    return {"weights": weights, "L": L, "local": local, "K": K,
            "rates": rates, "budgets": budgets,
            "regions": [[0, 1] + hidden[0], [2, 3] + hidden[1]],
            "cross_edges": cross}


def full_mean(net, target, source=None):
    L, w = net["L"], net["weights"]
    live = [i for i in range(len(w)) if i not in target]
    h = solve([[L[i][j] for j in live] for i in live], [w[i] for i in live])
    field = dict(zip(live, h))
    source = live if source is None else source
    assert all(i in field for i in source)
    return sum(w[i] * field[i] for i in source) / sum(w[i] for i in source)


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


def main():
    original, prepared = make_network(False), make_network(True)
    assert original["local"] == prepared["local"]
    assert original["K"] == prepared["K"]
    assert original["cross_edges"] == prepared["cross_edges"]
    K = original["K"]
    bR, bL = [F(4), F(1), F(4), F(1)], [F(1), F(4), F(1), F(4)]
    c, W = F(13), F(10)
    means = []
    for k in range(1, 5):
        for A in combinations(range(4), k):
            expected = full_mean(original, A)
            assert full_mean(prepared, A) == expected
            live = [i for i in range(4) if i not in A]
            h = solve([[K[i][j] for j in live] for i in live], [bR[i] for i in live])
            compressed = (c + dot([bL[i] for i in live], h)) / (W - len(A))
            assert compressed == expected
            means.append({"port_target": A, "mean": expected})
    whole = []
    for j, expected in [(0, F(16, 5)), (1, F(3))]:
        t = 1 - j
        value = full_mean(original, original["regions"][t], original["regions"][j])
        assert value == expected
        assert full_mean(prepared, prepared["regions"][t], prepared["regions"][j]) == expected
        live_ports = [2 * j, 2 * j + 1]
        h = solve([[K[i][l] for l in live_ports] for i in live_ports],
                  [bR[i] for i in live_ports])
        r = original["local"][j]
        compressed = (r["c"] + dot(r["bL"], h)) / r["mass"]
        assert compressed == expected
        whole.append({"source_region": j, "target_region": t, "mean": expected})
    out = {"status": "PASS", "scope": "new non-Eulerian-module composition control",
           "original_states": len(original["weights"]),
           "prepared_states": len(prepared["weights"]),
           "local_records": original["local"], "assembled_trace": K,
           "cross_edges": original["cross_edges"], "port_spare_budgets": prepared["budgets"],
           "original_rates": original["rates"], "prepared_rates": prepared["rates"],
           "original_laplacian": original["L"], "prepared_laplacian": prepared["L"],
           "original_weights": original["weights"], "prepared_weights": prepared["weights"],
           "port_target_means": means, "whole_region_means": whole,
           "new_observations": 0}
    path = Path(__file__).with_name("NON_EULERIAN_MODULE_COMPOSITION_CHECKS.json")
    path.write_text(json.dumps(encode(out), indent=2) + "\n")
    print(json.dumps({"status": "PASS", "states": [out["original_states"], out["prepared_states"]],
                      "port_target_means": len(means), "whole_region_means": encode(whole),
                      "local_column_sums": encode([r["port_divergence"] for r in original["local"]]),
                      "path": str(path)}, indent=2))


if __name__ == "__main__":
    main()
