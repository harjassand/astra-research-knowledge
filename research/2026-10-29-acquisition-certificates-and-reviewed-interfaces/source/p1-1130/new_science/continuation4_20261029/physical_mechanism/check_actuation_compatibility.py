"""Exact population checks for the fixed-clock actuation construction.

Standard library only. No acquired transition probabilities or apparatus data.
The implementation builds the selector from the visible graph and target weights
alone, then tests it on separate complete hidden kernels.
"""

from collections import deque
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json


def max_flow_selector(weights, edges):
    """Integral double-cover max flow, followed by symmetric edge allocation."""
    n = len(weights)
    source, sink = 2*n, 2*n+1
    adj = [[] for _ in range(2*n+2)]
    caps = {}

    def add(u, v, c):
        if (u, v) not in caps:
            adj[u].append(v)
            adj[v].append(u)
            caps[u, v] = 0
            caps[v, u] = 0
        caps[u, v] += c

    for y, w in enumerate(weights):
        add(source, y, w)
        add(n+y, sink, w)
    total = sum(weights)
    for u, v in edges:
        add(u, n+v, total+1)
        add(v, n+u, total+1)
    original = caps.copy()
    value = 0
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v in adj[u]:
                if v not in parent and caps[u, v] > 0:
                    parent[v] = u
                    queue.append(v)
        if sink not in parent:
            break
        path = []
        v = sink
        while parent[v] is not None:
            u = parent[v]
            path.append((u, v))
            v = u
        amount = min(caps[uv] for uv in path)
        for u, v in path:
            caps[u, v] -= amount
            caps[v, u] += amount
        value += amount

    f = {}
    q = [dict() for _ in weights]
    for u, v in edges:
        guv = original[u, n+v] - caps[u, n+v]
        gvu = original[v, n+u] - caps[v, n+u]
        mass = F(guv+gvu, 2)
        f[u, v] = mass
        q[u][v] = mass/weights[u]
        q[v][u] = mass/weights[v]
    q0 = [1-sum(qy.values(), F(0)) for qy in q]
    assert all(qy >= 0 for qy in q0)
    duty = sum(F(w, total)*q0[y] for y, w in enumerate(weights))
    assert duty == F(total-value, total)
    return f, q, q0, duty


def exact_deficiency(weights, edges):
    n = len(weights)
    neighbors = [0]*n
    for u, v in edges:
        neighbors[u] |= 1 << v
        neighbors[v] |= 1 << u
    best = -1
    witness = None
    for mask in range(1 << n):
        hood = 0
        for u in range(n):
            if mask >> u & 1:
                hood |= neighbors[u]
        excess = sum(w for u, w in enumerate(weights) if mask >> u & 1)
        excess -= sum(w for u, w in enumerate(weights) if hood >> u & 1)
        if excess > best:
            best = excess
            witness = mask
    return F(best, sum(weights)), [u for u in range(n) if witness >> u & 1]


def cube(d):
    return [(y, y ^ (1 << i)) for y in range(1 << d)
            for i in range(d) if y < (y ^ (1 << i))]


def zero_matrix(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def row_times(v, a):
    return [sum((v[i]*a[i][j] for i in range(len(v))), F(0))
            for j in range(len(a[0]))]


def make_hidden_menu(d):
    n = 1 << d
    state_count = 2*n
    # Nontrivial label/hidden correlation, but exactly uniform visible marginal.
    mu = []
    for y in range(n):
        a = F(1+(y.bit_count() % 2), 3)
        mu.extend([a/n, (1-a)/n])
    menu = []
    for i in range(d+1):
        p = zero_matrix(state_count)
        for a in range(state_count):
            y = a//2
            for b in range(state_count):
                z = b//2
                allowed = (z == y or (i < d and z == (y ^ (1 << i))))
                if a != b and allowed:
                    # Symmetric, genuinely hidden-state-dependent edge mobility.
                    mobility = F(1+((a+b+3*i) % 7), 9)
                    p[a][b] = mu[b]*mobility
            p[a][a] = 1-sum(p[a], F(0))
        assert row_times(mu, p) == mu
        assert all(mu[a]*p[a][b] == mu[b]*p[b][a]
                   for a in range(state_count) for b in range(state_count))
        menu.append(p)
    return mu, menu


def check_hidden_compilation(weights, d):
    edges = cube(d)
    _, neighbors, q0, duty = max_flow_selector(weights, edges)
    q = [[neighbors[y][y ^ (1 << i)] for i in range(d)] + [q0[y]]
         for y in range(1 << d)]
    mu, menu = make_hidden_menu(d)
    n = len(mu)
    nu = [mu[a]*(1 << d)*F(weights[a//2], sum(weights)) for a in range(n)]
    k = zero_matrix(n)
    for a in range(n):
        for b in range(n):
            k[a][b] = sum((q[a//2][i]*menu[i][a][b]
                           for i in range(d+1)), F(0))
    assert all(sum(row, F(0)) == 1 for row in k)
    assert row_times(nu, k) == nu
    assert all(nu[a]*k[a][b] == nu[b]*k[b][a]
               for a in range(n) for b in range(n))

    # A visible input does not determine the native response: hidden memory matters.
    witnesses = []
    for i in range(d):
        for y in range(1 << d):
            flip = [sum((menu[i][2*y+h][b]
                         for b in range(n) if b//2 == (y ^ (1 << i))), F(0))
                    for h in (0, 1)]
            if flip[0] != flip[1]:
                witnesses.append({"operation": i, "label": y,
                                  "hidden_flip_probabilities": list(map(str, flip))})
    assert witnesses

    # Finite-rate autonomous selector: actual L_i=P_i-I, no instantaneous reset.
    modes = d+1
    joint_n = n*modes
    generator = zero_matrix(joint_n)
    rho = [nu[a]*q[a//2][i] for a in range(n) for i in range(modes)]
    gamma = F(2, 7)
    for a in range(n):
        for i in range(modes):
            src = a*modes+i
            for b in range(n):
                if a != b:
                    generator[src][b*modes+i] += menu[i][a][b]
            for j in range(modes):
                if i != j:
                    generator[src][a*modes+j] += gamma*q[a//2][j]
            generator[src][src] = -sum(generator[src], F(0))
    assert row_times(rho, generator) == [F(0)]*joint_n
    assert all(rho[a]*generator[a][b] == rho[b]*generator[b][a]
               for a in range(joint_n) for b in range(joint_n))
    assert sum(rho[a*modes+d] for a in range(n)) == duty
    return {"weights": weights, "physical_states": n, "controller_modes": modes,
            "joint_states": joint_n, "optimal_preserving_duty": str(duty),
            "hidden_response_witness": witnesses[0],
            "full_state_stationarity": True, "full_state_reversibility": True,
            "finite_rate_joint_stationarity": True,
            "finite_rate_joint_reversibility": True}


def hamming_code_check(r, big_weight):
    d = (1 << r)-1
    # Coordinate columns are the nonzero r-bit vectors.
    def syndrome(y):
        result = 0
        for i in range(d):
            if y >> i & 1:
                result ^= i+1
        return result
    code = [y for y in range(1 << d) if syndrome(y) == 0]
    weights = [big_weight if syndrome(y) == 0 else 1 for y in range(1 << d)]
    assert big_weight >= d
    _, _, _, optimum = max_flow_selector(weights, cube(d))
    q = []
    for y in range(1 << d):
        s = syndrome(y)
        if s == 0:
            q.append([F(1, big_weight)]*d + [1-F(d, big_weight)])
        else:
            q.append([F(i+1 == s) for i in range(d)] + [F(0)])
    for y in range(1 << d):
        for i in range(d):
            z = y ^ (1 << i)
            assert weights[y]*q[y][i] == weights[z]*q[z][i]
    expected = F(big_weight-d, big_weight+d)
    assert optimum == expected
    duty = sum(F(w, sum(weights))*q[y][-1] for y, w in enumerate(weights))
    assert duty == expected
    return {"register_bits": d, "codewords": len(code), "weight": big_weight,
            "code_mass": str(F(big_weight, big_weight+d)),
            "optimal_preserving_duty": str(expected),
            "syndrome_selector_matches_flow_optimum": True,
            "convergence_between_logical_basins_claimed": False}


def main():
    cases = [
        ("triangle_feasible", [2, 3, 4], [(0,1),(1,2),(0,2)]),
        ("triangle_deficient", [8, 1, 2], [(0,1),(1,2),(0,2)]),
        ("path", [1, 4, 2, 1, 3], [(i,i+1) for i in range(4)]),
        ("two_biased_bits", [1, 2, 4, 8], cube(2)),
        ("three_bit_code", [16,1,1,1,1,1,1,16], cube(3)),
        ("four_bit_target", [1,2,4,8,2,1,8,4,4,8,1,2,8,4,2,1], cube(4)),
    ]
    flow_results = []
    for name, weights, edges in cases:
        f, q, q0, duty = max_flow_selector(weights, edges)
        exact, witness = exact_deficiency(weights, edges)
        assert duty == exact
        assert all(sum(q[y].values(), F(0))+q0[y] == 1 for y in range(len(weights)))
        assert all(weights[u]*q[u][v] == weights[v]*q[v][u] for u, v in edges)
        flow_results.append({"name": name, "vertices": len(weights),
                             "edges": len(edges), "minimum_duty": str(duty),
                             "deficiency_witness": witness,
                             "double_cover_equals_all_cut_deficiency": True})
    hidden_results = [check_hidden_compilation([16,1,1,1,1,1,1,16], 3),
                      check_hidden_compilation([1,2,1,2,1,2,1,2], 3)]
    # Strong ordinary prechoice Metropolis comparator on the same target/menu.
    w = [16,1,1,1,1,1,1,16]
    metropolis_duty = sum(F(w[y], sum(w))*(1-sum(
        F(1,3)*min(F(1), F(w[y ^ (1 << i)], w[y])) for i in range(3)))
                          for y in range(8))
    assert metropolis_duty == F(15,19)
    result = {"status": "PASS", "arithmetic": "exact integers and fractions",
              "scope": "population mathematical checks; no apparatus or acquired rates",
              "flow_cases": flow_results, "hidden_physical_menu_cases": hidden_results,
              "perfect_code_family": [hamming_code_check(2,16), hamming_code_check(3,64)],
              "ordinary_prechoice_metropolis": {"duty": str(metropolis_duty),
                  "optimal_flow_duty": str(F(13,19)),
                  "same_physical_menu": True,
                  "general_flow_optimization_is_established": True}}
    here = Path(__file__).resolve().parent
    result["checker_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (here/"ACTUATION_COMPATIBILITY_CHECKS.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
