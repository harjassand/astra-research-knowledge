"""Count-only physical gauge proposal, boundary-safe CP repair, and law debit.

The scientific theorem is in CONSTRUCTION.md.  This numerical implementation
uses floating point, not directed interval arithmetic; it is a reproducible
diagnostic, not an implementation of the finite-arithmetic certification gate.
No fixture or truth data are imported here.
"""
from __future__ import annotations
from itertools import product
import numpy as np
from scipy.linalg import null_space, polar
from scipy.optimize import minimize_scalar

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
P = np.array([I, X, Y, Z])


def herm(a):
    return (a + a.conj().T) / 2


def root(a, inverse=False):
    w, v = np.linalg.eigh(herm(a))
    if w.min() <= 0:
        raise ValueError('nonpositive matrix at a square-root gate')
    return (v * (1 / np.sqrt(w) if inverse else np.sqrt(w))) @ v.conj().T


def to_choi(f):
    # Input-first convention: J = sum_ij |i><j| tensor Phi(|i><j|).
    ans = np.zeros((4, 4), complex)
    for i in range(2):
        for j in range(2):
            e = np.zeros((2, 2), complex)
            e[i, j] = 1
            coeff = np.array([np.trace(p @ e) for p in P])
            image = sum((v * p for v, p in zip(f @ coeff, P)),
                        np.zeros((2, 2), complex)) / 2
            ans[2 * i:2 * i + 2, 2 * j:2 * j + 2] = image
    return herm(ans)


def from_choi(j):
    ans = np.zeros((4, 4))
    for k, p in enumerate(P):
        out = sum((p[i, l] * j[2 * i:2 * i + 2, 2 * l:2 * l + 2]
                   for i in range(2) for l in range(2)), np.zeros((2, 2), complex))
        ans[:, k] = [np.trace(q @ out).real / 2 for q in P]
    return ans


def partial_trace_output(j):
    return np.array([[np.trace(j[2 * i:2 * i + 2, 2 * k:2 * k + 2])
                      for k in range(2)] for i in range(2)])


def repair_instrument(raw_fs):
    positive, raw_min = [], []
    for f in raw_fs:
        j = to_choi(f)
        w, v = np.linalg.eigh(j)
        raw_min.append(float(w.min()))
        positive.append((v * np.maximum(w, 0)) @ v.conj().T)
    t = sum((partial_trace_output(j) for j in positive), np.zeros((2, 2), complex))
    inv = root(t, inverse=True)
    d = np.kron(inv, I)
    js = [herm(d @ j @ d) for j in positive]
    fs = [from_choi(j) for j in js]
    return fs, dict(raw_choi_min=raw_min, normalization_eigenvalues=np.linalg.eigvalsh(t).tolist(),
                    repaired_choi_min=[float(np.linalg.eigvalsh(j).min()) for j in js],
                    tp_residual=float(np.linalg.norm(sum(fs)[0] - np.array([1, 0, 0, 0]))))


def symmetric_basis(d):
    b = []
    for i in range(d):
        a = np.zeros((d, d)); a[i, i] = 1; b.append(a)
    for i in range(d):
        for j in range(i + 1, d):
            a = np.zeros((d, d)); a[i, j] = a[j, i] = 1 / np.sqrt(2); b.append(a)
    return b


def acquire_gauge(chat, reversible, initial_index, pure_anchor=False):
    r = 4
    trace = np.ones(r)
    v = null_space(trace[None, :])
    e = np.eye(r)[:, initial_index]
    # Exact trace repair for the deterministic calibration operations.
    cc = []
    for a in reversible:
        c = chat[a][0].copy()
        c += np.outer(trace / (trace @ trace), trace - trace @ c)
        cc.append(c)
    bs = [v.T @ c @ v for c in cc]
    rhs = np.concatenate([v.T @ (c @ e - e) for c in cc])
    center_matrix = np.vstack([np.eye(3) - b for b in bs])
    center_coeff, *_ = np.linalg.lstsq(center_matrix, rhs, rcond=None)
    center = e + v @ center_coeff
    anchor = v.T @ (e - center)
    sb = symmetric_basis(3)
    rows = [np.column_stack([(b.T @ s @ b - s).reshape(-1) for s in sb]) for b in bs]
    rows.append(np.array([[anchor @ s @ anchor if pure_anchor else np.trace(s)
                           for s in sb]]))
    fm = np.vstack(rows)
    target = np.zeros(len(fm)); target[-1] = 1 if pure_anchor else 3
    coeff, *_ = np.linalg.lstsq(fm, target, rcond=None)
    g = sum(c * s for c, s in zip(coeff, sb))
    l = root(g).real
    sphere = l @ v.T @ (np.eye(r) - center[:, None])
    raw_norms = np.linalg.norm(sphere, axis=0)
    s = np.vstack([trace, sphere])
    if np.linalg.svd(s, compute_uv=False)[-1] < 1e-10:
        raise ValueError('repaired density-state basis is nearly singular')
    return s, dict(center=center.tolist(), center_gap=float(np.linalg.svd(center_matrix, compute_uv=False)[-1]),
                   metric_gap=float(np.linalg.svd(fm, compute_uv=False)[-1]),
                   metric=g.tolist(), metric_eigenvalues=np.linalg.eigvalsh(g).tolist(),
                   raw_state_radii=raw_norms.tolist(), normalization='pure anchor' if pure_anchor else 'trace(G)=3',
                   basis_min_singular=float(np.linalg.svd(s, compute_uv=False)[-1]),
                   center_residual=float(np.linalg.norm(center_matrix @ center_coeff - rhs)),
                   metric_residual=float(np.linalg.norm(fm @ coeff - target)))


def count_bands(data, alpha):
    slots = int(np.count_nonzero(data['n_H']) +
                sum(np.count_nonzero(n) for ns in data['n_shifted'].values() for n in ns))
    def width(n):
        out = np.zeros(n.shape)
        selected = n > 0
        out[selected] = np.sqrt(np.log(2 * slots / alpha) / (2 * n[selected]))
        return np.nextafter(out, np.inf) * selected
    return width(data['n_H']), {a: [width(n) for n in ns]
                                 for a, ns in data['n_shifted'].items()}, slots


def law_debit(data, fitted_c, alpha=0.01):
    h = data['H']
    dh, dz, slots = count_bands(data, alpha)
    u = np.linalg.inv(h)
    a = np.abs(u) @ dh
    if np.max(a.sum(axis=1)) >= 1:
        raise ValueError('inverse confidence gate fails')
    majorant = np.linalg.solve(np.eye(4) - a, np.abs(u))
    rem = majorant - np.abs(u)
    kcore = max(np.linalg.norm(u @ np.array((1,) + bits), 1) +
                np.ones(4) @ rem @ np.array((1,) + bits) for bits in product([0, 1], repeat=3))
    es, gas = {}, {}
    for a, cs in fitted_c.items():
        es[a] = [majorant @ (d + dh @ np.abs(c) + np.abs(h @ c - hz))
                 for c, hz, d in zip(cs, data['shifted'][a], dz[a])]
        gas[a] = float(max(sum(es[a]).sum(axis=0)))
    b = kcore * max(gas.values()) / 2
    return dict(alpha=alpha, uncertain_probability_slots=slots,
                maximum_width=float(max(dh.max(), max(d.max() for ds in dz.values() for d in ds))),
                K_core=float(kcore), per_action_g=gas, b=float(b),
                inverse_neumann_gate=float(np.max((np.abs(u) @ dh).sum(axis=1)))), es


def learn(data, alpha=0.01, use_unitary_promise=True, pure_anchor=False, scale_points=65):
    h = data['H']
    chat = {a: [np.linalg.solve(h, hz) for hz in hzs] for a, hzs in data['shifted'].items()}
    base, gauge_info = acquire_gauge(chat, data['reversible_actions'], data['initial_index'], pure_anchor)
    evaluations = []
    def objective(scale):
        s = base.copy()
        rr = scale * s[1:]
        s[1:] = rr / np.maximum(1, np.linalg.norm(rr, axis=0))[None, :]
        fitted = fit_in_gauge(data, chat, s, alpha, use_unitary_promise)
        evaluations.append((float(fitted['diagnostics']['law']['b']), float(scale), fitted))
        return evaluations[-1][0]
    if pure_anchor:
        objective(1.)
        search_info = dict(method='pure anchor, no scalar search', evaluations=1, scale=1.)
    else:
        effects = h @ np.linalg.inv(base)
        beta = max(np.linalg.norm(effects[i, 1:]) for i in range(1, 4))
        upper = 1 / max(np.linalg.norm(base[1:, j]) for j in range(4))
        lower = min(upper / 4, beta / 2)
        if lower <= 1e-12:
            raise ValueError('no scale range from nonzero acquired test contrasts')
        # A practical proposal heuristic. The theorem's complete version uses
        # a global mesh tending to zero, with its evaluations charged.
        grid = np.geomspace(lower, 1.2 * upper, scale_points)
        vals = np.array([objective(s) for s in grid])
        for j in np.argsort(vals)[:5]:
            lo, hi = grid[max(0,j-1)], grid[min(len(grid)-1,j+1)]
            if hi > lo:
                minimize_scalar(objective, bounds=(lo,hi), method='bounded',
                                options=dict(xatol=1e-12,maxiter=80))
        _, chosen_scale, _ = min(evaluations, key=lambda x:x[0])
        search_info = dict(method='65-point geometric proposal plus five local scalar refinements; not a proof of global optimality',
                           evaluations=len(evaluations), lower=float(lower), upper=float(1.2*upper), scale=chosen_scale)
    _, _, best = min(evaluations, key=lambda x:x[0])
    best['diagnostics']['gauge'] = gauge_info
    best['diagnostics']['scale_search'] = search_info
    best['diagnostics']['gauge']['repaired_state_radii'] = np.linalg.norm(best['S'][1:],axis=0).tolist()
    return best


def fit_in_gauge(data, chat, s, alpha=0.01, use_unitary_promise=True):
    si = np.linalg.inv(s)
    model, repairs = {}, {}
    for a, cs in chat.items():
        raw = [s @ c @ si for c in cs]
        if use_unitary_promise and a in data['reversible_actions']:
            b = raw[0][1:, 1:]
            q, _ = polar(b)
            if np.linalg.det(q) < 0:
                uu, _, vv = np.linalg.svd(b)
                uu[:, -1] *= -1
                q = uu @ vv
            f = np.zeros((4, 4)); f[0, 0] = 1; f[1:, 1:] = q
            model[a] = [f]
            repairs[a] = dict(unitary_polar=True, raw_error=float(np.linalg.norm(raw[0] - f)),
                              repaired_choi_min=[float(np.linalg.eigvalsh(to_choi(f)).min())],
                              tp_residual=float(np.linalg.norm(f[0] - [1, 0, 0, 0])))
        else:
            model[a], repairs[a] = repair_instrument(raw)
    fitted_c = {a: [si @ f @ s for f in fs] for a, fs in model.items()}
    debit, residual = law_debit(data, fitted_c, alpha)
    initial = s[:, data['initial_index']].copy()
    return dict(actions=model, initial=initial, S=s, C=fitted_c,
                diagnostics=dict(repairs=repairs, law=debit),
                residual_bands=residual, raw_C=chat)


def optimal_policy(actions, state, horizon, terminal_action='M', target_outcome=1):
    """Exhaustive exact-model finite-horizon planning; not polynomial-time planning."""
    nodes = 1
    if horizon == 0:
        return float((actions[terminal_action][target_outcome] @ state)[0]), dict(action=terminal_action, children=None), nodes
    best_value, best = -np.inf, None
    for a, maps in actions.items():
        val, children = 0., []
        for f in maps:
            x = f @ state
            p = float(np.clip(x[0], 0, 1))
            nxt = x / p if p > 1e-13 else np.array([1., 0., 0., 0.])
            v, tree, n = optimal_policy(actions, nxt, horizon - 1, terminal_action, target_outcome)
            val += p * v
            children.append(tree)
            nodes += n
        if val > best_value:
            best_value, best = val, dict(action=a, children=children)
    return best_value, best, nodes


def policy_law(actions, state, tree, prefix=()):
    a = tree['action']
    result = {}
    for o, f in enumerate(actions[a]):
        x = f @ state
        key = prefix + ((a, o),)
        if tree['children'] is None:
            result[key] = float(x[0])
        else:
            result.update(policy_law(actions, x, tree['children'][o], key))
    return result
