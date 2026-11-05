"""Independent exact audit of the ordered-fault, route-collapsed proposal.

No builder code is imported. All error configurations, canonical paths,
distinct-edge tuples and off-tuple completions are enumerated. The *actual*
killed Markov proposal is propagated using rational probabilities.
"""
from fractions import Fraction as Q
from collections import deque
from pathlib import Path
import json, math, time

started = time.perf_counter()
edges = [(0, 1), (1, 2), (2, 3), (1, 3), (3, 4)]
cost = [1, 2, 1, 2, 1]
p = [Q(1, 100), Q(1, 125), Q(1, 80), Q(1, 100), Q(1, 125)]
nv, ne = 5, len(edges)
left, right, checks = {0}, {4}, [1, 2, 3]
adj = [[] for _ in range(nv)]
for e, (u, v) in enumerate(edges):
    adj[u].append((v, e)); adj[v].append((u, e))
dist = [[0 if u == v else 10000 for v in range(nv)] for u in range(nv)]
for e, (u, v) in enumerate(edges):
    dist[u][v] = dist[v][u] = cost[e]
for k in range(nv):
    for u in range(nv):
        for v in range(nv):
            dist[u][v] = min(dist[u][v], dist[u][k] + dist[k][v])
states = [(u, v, e) for e, (u, v) in enumerate(edges) for u, v in [(u, v), (v, u)]]
sid = {s: i for i, s in enumerate(states)}

def syndrome(mask):
    return tuple(sum((mask >> e) & 1 for _, e in adj[v]) % 2 for v in checks)

best = {}
for mask in range(1 << ne):
    key = (sum(c for e, c in enumerate(cost) if (mask >> e) & 1), mask)
    sy = syndrome(mask)
    if sy not in best or key < best[sy]:
        best[sy] = key

def canonical(mask):
    correction = best[syndrome(mask)][1]
    residual = mask ^ correction
    if not (residual & 1):
        return None
    queue = deque([0]); parents = {0: None}; last = None
    while queue:
        u = queue.popleft()
        if u in right:
            last = u; break
        for v, e in adj[u]:
            if (residual >> e) & 1 and v not in parents:
                parents[v] = (u, e); queue.append(v)
    assert last is not None
    path = []
    while parents[last] is not None:
        u, e = parents[last]; path.append(sid[u, last, e]); last = u
    path.reverse()
    assert sum(cost[states[i][2]] * (2 * ((mask >> states[i][2]) & 1) - 1)
               for i in path) >= 0
    faults = tuple(i for i in path if (mask >> states[i][2]) & 1)
    assert faults
    return faults

canon = [canonical(mask) for mask in range(1 << ne)]
prob = [math.prod(p[e] if (mask >> e) & 1 else 1 - p[e] for e in range(ne))
        for mask in range(1 << ne)]
pf = sum(prob[mask] for mask in range(1 << ne) if canon[mask] is not None)

def solve(A, b):
    n = len(b)
    for k in range(n):
        pivot = next(i for i in range(k, n) if A[i][k])
        A[k], A[pivot] = A[pivot], A[k]; b[k], b[pivot] = b[pivot], b[k]
        q = A[k][k]
        for j in range(k, n): A[k][j] /= q
        b[k] /= q
        for i in range(n):
            if i == k or not A[i][k]: continue
            q = A[i][k]
            for j in range(k, n): A[i][j] -= q * A[k][j]
            b[i] -= q * b[k]
    return b

rows = []
for N in [1, 2, 4]:
    for cap in [1, None]:
        # Only interior gaps are capped; boundary distances stay exact.
        gap = lambda a, b: dist[a][b] if cap is None else min(dist[a][b], cap)
        dl = [min(dist[x][u] for x in left) for u, v, e in states]
        dr = [min(dist[v][x] for x in right) for u, v, e in states]
        initial_delta = [cost[e] - dl[i] for i, (u, v, e) in enumerate(states)]
        delta = [[cost[f] - gap(v, x) for x, y, f in states] for u, v, e in states]
        weight = [[p[states[j][2]] * Q(2) ** delta[i][j] for j in range(len(states))]
                  for i in range(len(states))]
        assert all(sum(row) < 1 for row in weight)  # easy exact contraction here
        terminal = [[Q(2) ** (-dr[i] - ((r - dr[i]) % N)) for r in range(N)]
                    for i in range(len(states))]
        M = len(states) * N
        A = [[Q(int(i == j)) for j in range(M)] for i in range(M)]
        rhs = []
        slack = Q(1, 1000)
        for i in range(len(states)):
            for r in range(N):
                rhs.append(terminal[i][r] + slack)
                for j in range(len(states)):
                    A[i*N+r][j*N+(r+delta[i][j]) % N] -= weight[i][j]
        H = solve(A, rhs)
        assert min(H) > 0
        h = lambda i, r: H[i*N+r]
        roots = [p[e] * Q(2) ** initial_delta[i] * h(i, initial_delta[i] % N)
                 for i, (u, v, e) in enumerate(states)]
        Z = sum(roots)
        categories = dict(null=Q(0), repeat_edge=Q(0), terminal=Q(0))
        accepted = Q(0); wrong_vertex_accept = Q(0); terminal_count = 0

        def visit(i, r, S, tup, edge_set, mass):
            global accepted, wrong_vertex_accept, terminal_count
            stop_mass = mass * terminal[i][r] / h(i, r)
            categories['terminal'] += stop_mass
            terminal_count += 1
            final_score = S - dr[i]; final_residue = final_score % N
            qfaults = math.prod(p[states[j][2]] for j in tup)
            assert stop_mass == qfaults * Q(2) ** (final_score - final_residue) / Z
            if final_score >= 0:
                thinned = stop_mass * Q(2) ** (-(final_score - final_residue))
                assert thinned == qfaults / Z
                for mask in range(1 << ne):
                    if canon[mask] != tup: continue
                    assert all((mask >> e) & 1 for e in edge_set)
                    outside = math.prod(p[e] if (mask >> e) & 1 else 1-p[e]
                                        for e in range(ne) if e not in edge_set)
                    accepted += thinned * outside
                    # A tempting but wrong stronger rejection: prohibit any
                    # shared endpoints among fault edges, even adjacent ones.
                    endpoints = [v for j in tup for v in states[j][:2]]
                    if len(set(endpoints)) == len(endpoints):
                        wrong_vertex_accept += thinned * outside
            moves = [(j, weight[i][j] * h(j, (r+delta[i][j]) % N) / h(i, r))
                     for j in range(len(states))]
            null = 1 - terminal[i][r] / h(i, r) - sum(q for j, q in moves)
            assert null > 0
            categories['null'] += mass * null
            for j, q in moves:
                e = states[j][2]
                if e in edge_set:
                    categories['repeat_edge'] += mass * q
                else:
                    visit(j, (r+delta[i][j]) % N, S+delta[i][j],
                          tup+(j,), edge_set | {e}, mass*q)

        for i, root in enumerate(roots):
            visit(i, initial_delta[i] % N, initial_delta[i], (i,), {states[i][2]}, root/Z)
        assert sum(categories.values()) == 1
        assert Z * accepted == pf
        assert Z * wrong_vertex_accept < pf
        # Each independently selected canonical tuple has nonnegative score.
        for tup in canon:
            if tup is None: continue
            score = initial_delta[tup[0]] + sum(delta[i][j] for i, j in zip(tup, tup[1:])) - dr[tup[-1]]
            assert score >= 0
        rows.append(dict(modulus=N, gap_cap=cap, exact_Z=str(Z), failure_probability=str(pf),
                         accepted_mass_times_Z=str(Z*accepted),
                         incorrect_shared_vertex_rejection_result=str(Z*wrong_vertex_accept),
                         tuple_count=terminal_count,
                         categories={k: str(v) for k, v in categories.items()}))

out = dict(status='PASS: exact killed proposal mass, score aliases, boundary shifts, distinct-edge rejection, and canonical law',
           finite_cases=rows, source='Independent five-edge weighted cyclic graph; all 32 physical error patterns',
           elapsed_seconds=time.perf_counter()-started)
Path(__file__).with_name('finite_exact_results.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='finite_cases'}, indent=2))
