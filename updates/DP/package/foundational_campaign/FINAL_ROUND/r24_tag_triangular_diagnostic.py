"""Exact finite checks of R24 section 5; not a preparation algorithm."""
from itertools import combinations, product
import json
import sympy as sp


def subsets(s):
    s = tuple(sorted(s))
    return [frozenset(x) for j in range(len(s) + 1) for x in combinations(s, j)]


def tuples(sets):
    return list(product(*sets))


def run_case(name, n, d, raw_clauses):
    sites = frozenset(range(n))
    counts = [0] * n
    clauses = []
    for support, row in raw_clauses:
        support = tuple(support)
        q = tuple(counts[i] for i in support)
        for i in support:
            counts[i] += 1
        assert all(counts[i] < d for i in range(n))
        local = tuples([range(d)] * len(support))
        coeff = {v: sp.Rational(row.get(v, 0)) for v in local}
        assert coeff[q] != 0
        clauses.append((frozenset(support), support, q, coeff, coeff[q]))
    cb = {i: tuple(range(counts[i])) for i in range(n)}
    tb = {i: tuple(range(counts[i], d)) for i in range(n)}
    ctuples = {u: tuples([cb[i] for i in sorted(u)]) for u in subsets(sites)}
    ttuples = {u: tuples([tb[i] for i in sorted(u)]) for u in subsets(sites)}
    M = {frozenset(): sp.ones(1, 1)}
    E = {}

    for u in subsets(sites)[1:]:
        us = tuple(sorted(u))
        ca = [a for a in clauses if a[0] <= u]
        cu = ctuples[u]
        tu = ttuples[u]
        cindex = {v: j for j, v in enumerate(cu)}
        du = sp.zeros(len(ca) * len(cu), len(cu))
        bu = sp.zeros(len(ca) * len(cu), len(tu))
        for ai, (x, xs, q, coeff, denominator) in enumerate(ca):
            for col, c in enumerate(cu):
                state = dict(zip(us, c))
                out = dict(state)
                out.update(zip(xs, q))
                row = ai * len(cu) + cindex[tuple(out[i] for i in us)]
                du[row, col] += coeff[tuple(state[i] for i in xs)] / denominator
            for s in subsets(u)[:-1]:
                if s | x != u:
                    continue
                ss = tuple(sorted(s))
                tsindex = {v: j for j, v in enumerate(ttuples[s])}
                for col, t in enumerate(tu):
                    logical = dict(zip(us, t))
                    mcol = tsindex[tuple(logical[i] for i in ss)]
                    for mrow, c in enumerate(ctuples[s]):
                        weight = M[s][mrow, mcol]
                        if weight == 0:
                            continue
                        state = dict(logical)
                        state.update(zip(ss, c))
                        out = dict(state)
                        out.update(zip(xs, q))
                        row = ai * len(cu) + cindex[tuple(out[i] for i in us)]
                        bu[row, col] += weight * coeff[tuple(state[i] for i in xs)] / denominator
        if du.rows:
            dpi = du.pinv()
            M[u] = -dpi * bu
            E[u] = (sp.eye(du.rows) - du * dpi) * bu
            assert du * M[u] + bu == E[u]
        else:
            M[u] = sp.zeros(len(cu), len(tu))
            E[u] = sp.zeros(0, len(tu))
        assert M[u].rank() <= len(cu)
        ru = sum(len(ctuples[u - a[0]]) for a in ca)
        assert E[u].rank() <= ru

    # Lift a local map with the logical identity on exterior factors.
    all_logical = ttuples[sites]
    logical_index = {t: j for j, t in enumerate(all_logical)}

    def lift_rows(a, u):
        us = tuple(sorted(u))
        outside = tuple(sorted(sites - u))
        outs = ttuples[sites - u]
        mat = sp.zeros(a.rows * len(outs), len(all_logical))
        for oi, ot in enumerate(outs):
            for ti, ut in enumerate(ttuples[u]):
                t = dict(zip(outside, ot))
                t.update(zip(us, ut))
                j = logical_index[tuple(t[i] for i in range(n))]
                for r in range(a.rows):
                    mat[oi * a.rows + r, j] = a[r, ti]
        return mat

    eglobal = {u: lift_rows(e, u) for u, e in E.items()}
    stacked = sp.Matrix.vstack(*eglobal.values())
    basis = stacked.nullspace()
    code = sp.Matrix.hstack(*basis) if basis else sp.zeros(len(all_logical), 0)
    full_states = tuples([range(d)] * n)
    state_index = {t: j for j, t in enumerate(full_states)}
    mg = sp.zeros(len(full_states), len(all_logical))
    for u, mu in M.items():
        us = tuple(sorted(u))
        tindex = {t: j for j, t in enumerate(ttuples[u])}
        for j, t in enumerate(all_logical):
            state = dict(enumerate(t))
            col = tindex[tuple(t[i] for i in us)]
            for r, c in enumerate(ctuples[u]):
                out = dict(state)
                out.update(zip(us, c))
                mg[state_index[tuple(out[i] for i in range(n))], j] = mu[r, col]
    for _, xs, q, coeff, denominator in clauses:
        gm = sp.zeros(len(full_states), len(all_logical))
        for j, state in enumerate(full_states):
            weight = coeff[tuple(state[i] for i in xs)] / denominator
            if not weight:
                continue
            out = dict(enumerate(state))
            out.update(zip(xs, q))
            gm[state_index[tuple(out[i] for i in range(n))], :] += weight * mg[j, :]
        assert gm * code == sp.zeros(gm.rows, code.cols)
    assert mg * code != sp.zeros(mg.rows, code.cols) or code.cols == 0

    # Every disconnected E_U is redundant modulo all proper E_V in U.
    disconnected_checks = 0
    for u in subsets(sites)[1:]:
        components = [{i} for i in u]
        for x, *_ in clauses:
            if x <= u:
                hit = [c for c in components if c & x]
                components = [c for c in components if not c & x]
                components.append(set().union(*hit))
        if len(components) <= 1:
            continue
        proper = [eglobal[v] for v in E if v < u]
        ep = sp.Matrix.vstack(*proper) if proper else sp.zeros(0, len(all_logical))
        bp = ep.nullspace()
        kp = sp.Matrix.hstack(*bp) if bp else sp.zeros(len(all_logical), 0)
        assert eglobal[u] * kp == sp.zeros(eglobal[u].rows, kp.cols)
        disconnected_checks += 1
    return {
        "case": name,
        "n": n,
        "d": d,
        "logical_dimension": len(all_logical),
        "selected_consistency_dimension": code.cols,
        "nonzero_local_consistency_ranks": {
            ",".join(map(str, sorted(u))): int(e.rank()) for u, e in E.items() if e.rank()
        },
        "disconnected_redundancy_checks": disconnected_checks,
        "exact_kernel_check": True,
    }


if __name__ == "__main__":
    dense = {x: 1 + ((3 * x[0] + 5 * x[1]) % 7) for x in product(range(4), repeat=2)}
    row_a = {(0, 0): 1, (1, 1): 1, (2, 2): 1}
    row_b = {(0, 0): 1, (1, 1): 1, (2, 2): 2}
    free_old = {(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 1}
    free_new = {(0, 0): 1, (1, 0): 1, (0, 1): 1, (1, 1): -1, (2, 2): 1}
    free_new_rotated = {
        (0, 0): sp.Rational(7, 5),
        (1, 0): sp.Rational(-1, 5),
        (0, 1): sp.Rational(-1, 5),
        (1, 1): sp.Rational(-7, 5),
        (2, 2): 1,
    }
    cases = [
        ("two_disjoint_rows", 4, 4, [((0, 1), dense), ((2, 3), dense)]),
        ("syzygy_and_disjoint_row", 4, 4, [((0, 1), row_a), ((0, 1), row_b), ((2, 3), dense)]),
        ("generic_three_edge_path", 4, 4, [((0, 1), dense), ((1, 2), dense), ((2, 3), dense)]),
        ("global_chart_needs_free_transport", 3, 4, [((0, 2), free_old), ((0, 1), free_new)]),
        ("free_transport_after_rational_B_rotation", 3, 4,
         [((0, 2), free_old), ((0, 1), free_new_rotated)]),
    ]
    for case in cases:
        print(json.dumps(run_case(*case), sort_keys=True), flush=True)
