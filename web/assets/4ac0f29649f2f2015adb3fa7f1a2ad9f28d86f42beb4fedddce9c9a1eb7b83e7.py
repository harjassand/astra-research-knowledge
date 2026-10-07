"""Small exact diagnostics for the sparse-observable extension; not an FPRAS."""
from fractions import Fraction as F
from itertools import product, combinations
import json
from pathlib import Path
from time import perf_counter

START = perf_counter()

def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]

def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]

def tr(a):
    return sum((a[i][i] for i in range(len(a))), F(0))

def transpose(a):
    return [list(x) for x in zip(*a)]

def kron(a, b):
    return [[x * y for x in ar for y in br] for ar in a for br in b]

def scale(a, c):
    return [[c * v for v in row] for row in a]

def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]

def embed1(a, q, n=2):
    mats = [a if j == q else eye(2) for j in range(n)]
    out = [[F(1)]]
    for mat in mats:
        out = kron(out, mat)
    return out

X = [[F(0), F(1)], [F(1), F(0)]]
Z = [[F(1), F(0)], [F(0), F(-1)]]
s = F(1, 7)
alpha, gamma = F(3, 4), F(-1, 4)
av = 1 + s * (3 * alpha + gamma)
bv = 1 + s * (3 * alpha - gamma)
cv = 2 * s * alpha
edge = [[av, 0, 0, 0], [0, bv, cv, 0],
        [0, cv, bv, 0], [0, 0, 0, av]]

def field(b, c):
    r = b + abs(c)
    out = [[1 + s * (r + c), s * b],
           [s * b, 1 + s * (r - c)]]
    assert out[0][0] * out[1][1] >= out[0][1] ** 2
    return out

f0 = field(F(2, 3), F(-1, 5))
f1 = field(F(0), F(1, 7))
W = mm(mm(edge, embed1(f0, 0)), embed1(f1, 1))
B = mm(W, transpose(W))
K = mm(mm(B, B), B)
sig = scale(K, 1 / tr(K))
assert K == transpose(K)

# Construct every lifted local monomial directly from the gate matrix.
gates = [(edge, (0, 1)), (f0, (0,)), (f1, (1,))]
legs, row_ids, col_ids, dummy_ids = 0, [], [], []
for mat, qs in gates:
    row_ids.append(list(range(legs, legs + len(qs))))
    legs += len(qs)
    col_ids.append(list(range(legs, legs + len(qs))))
    legs += len(qs)
for mat, qs in gates:
    if len(qs) == 1:
        dummy_ids.append([legs, legs + 1])
        legs += 2
    else:
        dummy_ids.append([])

local = []
for gi, (mat, qs) in enumerate(gates):
    terms = []
    d = len(qs)
    for ri in range(2 ** d):
        rb = tuple((ri >> (d - 1 - j)) & 1 for j in range(d))
        for ci in range(2 ** d):
            val = mat[ri][ci]
            if not val:
                continue
            cb = tuple((ci >> (d - 1 - j)) & 1 for j in range(d))
            chosen = {row_ids[gi][j] for j in range(d) if rb[j]}
            chosen |= {col_ids[gi][j] for j in range(d) if not cb[j]}
            if d == 1:
                options = list(combinations(dummy_ids[gi], 2 - len(chosen)))
                for ds in options:
                    terms.append((chosen | set(ds), F(val) / len(options)))
            else:
                assert len(chosen) == 2
                terms.append((chosen, F(val)))
    local.append(terms)

monomials = []
for combo in product(*local):
    selected, weight = set(), F(1)
    for chosen, val in combo:
        selected |= chosen
        weight *= val
    assert len(selected) == 6
    monomials.append((selected, weight))

wires, boundary = [], []
for q in range(2):
    occ = [(gi, qs.index(q)) for gi, (mat, qs) in enumerate(gates) if q in qs]
    for t, (gi, pos) in enumerate(occ):
        gj, posj = occ[(t + 1) % len(occ)]
        pair = (col_ids[gi][pos], row_ids[gj][posj])
        if t == len(occ) - 1:
            boundary.append((q, pair))
        else:
            wires.append(pair)

all_dummies = {i for ds in dummy_ids for i in ds}
f_count = 2
entries_checked, shifted_nonzero = 0, []
for ai, bi in product(range(4), repeat=2):
    ab = tuple((ai >> (1 - j)) & 1 for j in range(2))
    bb = tuple((bi >> (1 - j)) & 1 for j in range(2))
    delta = sum(ab) - sum(bb)
    out = F(0)
    for chosen, weight in monomials:
        if any((x in chosen) + (y in chosen) != 1 for x, y in wires):
            continue
        if any((row in chosen) != bool(ab[q]) or
               (col in chosen) != bool(1 - bb[q])
               for q, (col, row) in boundary):
            continue
        q_dummy_rank = len(all_dummies - chosen)
        assert q_dummy_rank == f_count + delta
        out += weight
    assert out == W[ai][bi], (ai, bi, out, W[ai][bi])
    entries_checked += 1
    if delta and out:
        shifted_nonzero.append({"a": ai, "b": bi, "delta": delta,
                                "correct_Q_rank": f_count + delta,
                                "entry": str(out), "fixed_f_rank_entry": "0"})

XX, XZ, ZZ = kron(X, X), kron(X, Z), kron(Z, Z)
# Y tensor Y is real despite the imaginary one-qubit Y.
YY = [[F(0), F(0), F(0), F(-1)], [F(0), F(0), F(1), F(0)],
      [F(0), F(1), F(0), F(0)], [F(-1), F(0), F(0), F(0)]]
observables = {"XX": XX, "XZ": XZ, "YY": YY, "ZZ": ZZ,
               "(XX+ZZ)/3": scale(add(XX, ZZ), F(1, 3))}
variance_checks = []
for name, A in observables.items():
    g, u = [], []
    for b in range(4):
        g.append(sum((A[b][a] * sig[a][b] / sig[b][b]
                      for a in range(4)), F(0)))
        u.append(sum((abs(A[b][a]) * sig[a][b] / sig[b][b]
                      for a in range(4)), F(0)))
    mean = sum((sig[b][b] * g[b] for b in range(4)), F(0))
    moment = sum((sig[b][b] * g[b] ** 2 for b in range(4)), F(0))
    trace_bound = tr(mm(mm(A, sig), A))
    assert mean == tr(mm(A, sig))
    assert moment <= trace_bound <= 1
    r = max(sum(v != 0 for v in row) for row in A)
    u_moment = sum((sig[b][b] * u[b] ** 2 for b in range(4)), F(0))
    assert u_moment <= r ** 2
    T = F(5)
    clip_mean = sum((sig[b][b] * max(-T, min(T, g[b]))
                     for b in range(4)), F(0))
    assert abs(mean - clip_mean) <= moment / T <= 1 / T
    variance_checks.append({"observable": name, "mean": str(mean),
                            "second_moment": str(moment),
                            "trace_O_sigma_O": str(trace_bound),
                            "row_sparsity": r, "u_second_moment": str(u_moment)})

# A tiny diagonal need not cause inverse-probability sample complexity.
R = F(2 ** 40)
rare_K = [[F(1), R], [R, R * R + 1]]
rare_sig = scale(rare_K, 1 / tr(rare_K))
rare_g = [rare_sig[1][0] / rare_sig[0][0],
          rare_sig[0][1] / rare_sig[1][1]]
rare_moment = sum((rare_sig[b][b] * rare_g[b] ** 2 for b in range(2)), F(0))
assert rare_g[0] == 2 ** 40 and rare_moment < 1

# Exact Hessian witness for the illegal X boundary insertion 1+x*y.
# At x=y=1/2, Hessian log(1+xy) has diagonal -4/25,
# off-diagonal 16/25; the (1,1) quadratic form is 24/25.
illegal_curvature = 2 * F(-4, 25) + 2 * F(16, 25)
assert illegal_curvature == F(24, 25)

result = {"status": "PASS", "scope": "exact finite diagnostics, no FPRAS executed",
          "lifted_boundary_entries_checked": entries_checked,
          "off_charge_nonzero_entries": shifted_nonzero,
          "variance_checks": variance_checks,
          "rare_diagonal_fixture": {"diagonal_probability": str(rare_sig[0][0]),
                                     "maximum_ratio": str(rare_g[0]),
                                     "second_moment": str(rare_moment)},
          "illegal_X_boundary_curvature": str(illegal_curvature),
          "wall_seconds": perf_counter() - START}
path = Path(__file__).with_name("observable_checks.json")
path.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "entries": entries_checked,
                  "off_charge_nonzero": len(shifted_nonzero),
                  "variance_fixtures": len(variance_checks),
                  "wall_seconds": result["wall_seconds"]}))
