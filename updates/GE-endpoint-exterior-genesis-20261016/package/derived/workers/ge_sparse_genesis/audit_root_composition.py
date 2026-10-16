"""Independent read-only audit of root's saved direct-limit witnesses.

Imports no root implementation. Green systems use integer Bareiss elimination;
original actions and coarse rational histories use exact residual checks.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import math
import time

from check_receipts import independently_build_killed

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent / "root"


def fraction_free_multiple_solve(a, rhs):
    d = len(a)
    cols = len(rhs)
    m = [list(row) + [rhs[j][i] for j in range(cols)] for i, row in enumerate(a)]
    prev = 1
    for k in range(d - 1):
        pivot = m[k][k]
        assert isinstance(pivot, int) and pivot > 0
        for i in range(k + 1, d):
            multiplier = m[i][k]
            for j in range(k + 1, d + cols):
                numerator = m[i][j] * pivot - multiplier * m[k][j]
                quotient, remainder = divmod(numerator, prev)
                assert remainder == 0
                m[i][j] = quotient
            m[i][k] = 0
        prev = pivot
    answers = []
    for col in range(cols):
        x = [F(0)] * d
        for i in range(d - 1, -1, -1):
            x[i] = (F(m[i][d + col]) - sum((m[i][j] * x[j] for j in range(i + 1, d)), F(0))) / m[i][i]
        assert all(sum(F(a[i][j]) * x[j] for j in range(d)) == rhs[col][i] for i in range(d))
        answers.append(x)
    return answers


def check_one(path):
    start = time.perf_counter()
    data = json.loads(path.read_text())
    n, edges, r, fast = data["n"], list(map(tuple, data["edges"])), data["original_rates"], data["fast_design_rates"]
    # Independent union-find rather than the root DFS component builder.
    representative = list(range(n))
    def find(x):
        while representative[x] != x:
            x = representative[x]
        return x
    for (x, y), v in zip(edges, fast):
        if v:
            representative[find(y)] = find(x)
    sets = {}
    for x in range(n):
        sets.setdefault(find(x), []).append(x)
    blocks = sorted(sets.values(), key=lambda c: c[0])
    assert blocks == data["actual_fast_components"]
    owner = {x: j for j, c in enumerate(blocks) for x in c}
    block_pairs = list(combinations(range(len(blocks)), 2))
    bp_index = {p: j for j, p in enumerate(block_pairs)}
    retained = [ri if not ai else 0 for ri, ai in zip(r, fast)]
    conductance = [[0] * len(blocks) for _ in blocks]
    for (x, y), v in zip(edges, retained):
        if owner[x] != owner[y]:
            conductance[owner[x]][owner[y]] += v
            conductance[owner[y]][owner[x]] += v
    beta = [[F(conductance[i][j], len(blocks[i])) for j in range(len(blocks))] for i in range(len(blocks))]
    coarse = [[F(0)] * len(block_pairs) for _ in block_pairs]
    for z, pair in enumerate(block_pairs):
        for moving, other in [pair, pair[::-1]]:
            for destination, v in enumerate(beta[moving]):
                if destination == moving or not v:
                    continue
                coarse[z][z] += v
                if destination != other:
                    target = bp_index[tuple(sorted((destination, other)))]
                    coarse[z][target] -= v
    assert coarse == [[F(x) for x in row] for row in data["coarse_K"]]
    green_h, green_g = {}, {}
    green_equations = 0
    for block_id, c in enumerate(blocks):
        if len(c) < 2:
            continue
        local = {x: i for i, x in enumerate(c)}
        local_edges = [(local[x], local[y]) for (x, y), v in zip(edges, fast) if v and owner[x] == block_id]
        local_rates = [v for (x, y), v in zip(edges, fast) if v and owner[x] == block_id]
        local_h, _ = independently_build_killed(len(c), local_edges, local_rates)
        local_pairs = list(combinations(c, 2))
        local_index = {p: i for i, p in enumerate(local_pairs)}
        a = [[row.get(j, 0) for j in range(len(local_h))] for row in local_h]
        rhs = [[1] * len(local_h)]
        for bp in block_pairs:
            v = [0] * len(local_h)
            if block_id in bp:
                destination = bp[0] if bp[1] == block_id else bp[1]
                for i, (x, y) in enumerate(local_pairs):
                    for (u, w), rate in zip(edges, retained):
                        if u in (x, y) and owner[w] == destination:
                            v[i] += rate
                        if w in (x, y) and owner[u] == destination:
                            v[i] += rate
            rhs.append(v)
        answers = fraction_free_multiple_solve(a, rhs)
        green_equations += len(a) * len(rhs)
        for edge, v in zip(edges, fast):
            if v and owner[edge[0]] == block_id:
                i = local_index[edge]
                green_h[edge] = answers[0][i]
                green_g[edge] = [column[i] for column in answers[1:]]
    assert {str(e): str(v) for e, v in green_h.items()} == data["h"]
    assert {str(e): list(map(str, v)) for e, v in green_g.items()} == data["G"]
    h, _ = independently_build_killed(n, edges, r)
    pair_index = {p: i for i, p in enumerate(combinations(range(n), 2))}
    k, s, p = data["shape"], data["shift"], data["precision"]
    q = 1 << p
    previous = [q] * len(h)
    error = F(0)
    original_upper = []
    fast_ids = [i for i, v in enumerate(fast) if v]
    assert len(data["dyadic_original_solve_witnesses"]) == k - 1
    for j, (vector, receipt) in enumerate(zip(data["dyadic_original_solve_witnesses"], data["residual_receipts"]), 1):
        residual = max(abs(s * previous[i] - s * vector[i] - sum(w * vector[z] for z, w in row.items())) for i, row in enumerate(h))
        assert receipt["power"] == j and residual == receipt["residual_numerator"]
        error += F(residual, s * q)
        assert error == F(receipt["accumulated_error_exact"])
        original_upper.append([min(F(1), F(vector[pair_index[edges[i]]], q) + error) for i in fast_ids])
        previous = vector
    previous = [F(1)] * len(block_pairs)
    coarse_history = []
    for row in data["coarse_resolvent_history"]:
        v = list(map(F, row))
        assert all(0 <= x <= 1 for x in v)
        assert all(v[i] + sum(coarse[i][j] * v[j] for j in range(len(v))) / s == previous[i] for i in range(len(v)))
        coarse_history.append(v)
        previous = v
    assert len(coarse_history) == k - 1
    atom = F(s, k - 1) * sum(F(fast[i]) * green_h[edges[i]] * original_upper[k - 2][j] for j, i in enumerate(fast_ids))
    boundary = F(0)
    for j in range(k - 1):
        v = coarse_history[k - 2 - j]
        boundary += sum(F(fast[i]) * original_upper[j][ii] * sum(g * x for g, x in zip(green_g[edges[i]], v)) for ii, i in enumerate(fast_ids)) / (k - 1)
    m = max(4 * k, 2 * s)
    lower_exp = sum(F(s ** j, math.factorial(j)) for j in range(m + 1))
    tail_poly = sum(F(s ** j, math.factorial(j)) for j in range(k))
    cdf = 1 - tail_poly / lower_exp
    assert atom == F(data["atom_average_upper_exact"])
    assert boundary == F(data["boundary_average_upper_exact"])
    assert cdf == F(data["gamma_cdf_lower_exact"])
    upper = (atom + boundary) / cdf
    assert upper == F(data["direct_average_TV_upper_exact"])
    assert data["direct_average_certified_at_005"] == (upper <= F(1, 20))
    return dict(input=path.name, input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                checked=True, upper_exact=str(upper), upper_float=float(upper),
                green_equations_exactly_rechecked=green_equations,
                original_shifted_residuals_exactly_rechecked=k - 1,
                coarse_shifted_residuals_exactly_rechecked=(k - 1) * len(block_pairs),
                checker_seconds=time.perf_counter() - start)


def main():
    out = [check_one(ROOT / name) for name in ["DIRECT_PATH6.json", "DIRECT_BRANCH6.json", "DIRECT_PATH20.json"]]
    result = dict(scope="independent same-team read-only audit of Erlang composition and saved finite-bit outputs, not external validation of direct-limit theorem",
                  root_code_executed=False, root_sources_modified=False,
                  exact_checks=out,
                  formulas_E_F="correct conditional on direct certificate D; atom coefficient s/(k-1) and positive convolution normalization verified")
    (HERE / "root_composition_audit_receipt.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks": [{k: v[k] for k in ["input", "checked", "upper_float", "checker_seconds"]} for v in out]}), flush=True)


if __name__ == "__main__":
    main()
