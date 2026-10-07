"""Exact finite checks for the soft-intersection transfer; no FPRAS implementation."""
from fractions import Fraction as F
from itertools import combinations, product
import json


def det(a):
    if not a:
        return F(1)
    a = [list(map(F, row)) for row in a]
    ans = F(1)
    for j in range(len(a)):
        p = next((i for i in range(j, len(a)) if a[i][j]), None)
        if p is None:
            return F(0)
        if p != j:
            a[j], a[p] = a[p], a[j]
            ans = -ans
        q = a[j][j]
        ans *= q
        for i in range(j + 1, len(a)):
            r = a[i][j] / q
            for k in range(j + 1, len(a)):
                a[i][k] -= r * a[j][k]
    return ans


def tensor_check(n):
    # K_{n,n}, rank-one weighted signatures at every vertex.
    edges = list(product(range(n), range(n)))
    inc = {("L", i): [j for j, e in enumerate(edges) if e[0] == i]
           for i in range(n)}
    inc.update({("R", i): [j for j, e in enumerate(edges) if e[1] == i]
                for i in range(n)})
    weights = {(v, e): F(1 + (i + 2 * e) % 7, 1 + (3 * i + e) % 5)
               for i, v in enumerate(inc) for e in inc[v]}
    direct = {}
    for bits in product((0, 1), repeat=len(edges)):
        val = F(1)
        for v, inds in inc.items():
            chosen = [e for e in inds if bits[e]]
            if len(chosen) != 1:
                val = F(0)
                break
            val *= weights[(v, chosen[0])]
        if val:
            direct[bits] = val

    # Multiply local polynomials on halfedges, using full complement on R.
    expanded = {}
    for choices in product(range(n), repeat=2 * n):
        selected, val = set(), F(1)
        for choice, (v, inds) in zip(choices, inc.items()):
            e = inds[choice]
            val *= weights[(v, e)]
            chosen = {e} if v[0] == "L" else set(inds) - {e}
            selected |= {(v, a) for a in chosen}
        if not all(sum((v, e) in selected for v in (("L", i), ("R", j))) == 1
                   for e, (i, j) in enumerate(edges)):
            continue
        bits = tuple(int((("L", i), e) in selected)
                     for e, (i, _) in enumerate(edges))
        expanded[bits] = expanded.get(bits, F(0)) + val
    assert direct == expanded
    pin_checks = 0
    for pins in product((-1, 0, 1), repeat=len(edges)):
        # -1 is unobserved. This is a loop/singleton-block matroid restriction.
        a = sum((w for b, w in direct.items()
                 if all(p == -1 or b[e] == p for e, p in enumerate(pins))), F(0))
        c = sum((w for b, w in expanded.items()
                 if all(p == -1 or b[e] == p for e, p in enumerate(pins))), F(0))
        assert a == c
        pin_checks += 1
    return {"n": n, "positive_configurations": len(direct),
            "pinnings_checked": pin_checks,
            "partition_function": str(sum(direct.values()))}


def parity_check():
    triples = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
    all_sets = list(combinations(range(4), 2))
    bases = [list(map(frozenset, (s for s in all_sets
                    if len({triples[e][axis] for e in s}) == 2)))
             for axis in range(3)]
    common = set(bases[0]) & set(bases[1]) & set(bases[2])
    assert not common
    results = []
    for t in (F(1, 2), F(1, 4), F(1, 16), F(1, 100)):
        laws = [(s, t ** (len(s[0] ^ s[1]) + len(s[0] ^ s[2])))
                for s in product(*bases)]
        z = sum(w for _, w in laws)
        marg = [[sum(w for s, w in laws if e in s[k]) / z
                 for e in range(4)] for k in range(3)]
        assert all(x == F(1, 2) for row in marg for x in row)
        results.append({"t": str(t), "means": [[str(x) for x in r] for r in marg],
                        "hard_agreement_probability": "0"})
    return {"bases_per_matroid": [len(b) for b in bases],
            "common_bases": len(common), "softened_laws": results}


def curvature_check():
    # psi on k copies penalizes all but the first copy. Its dual has curvature1.
    psd_matrices = 0
    for k in range(2, 7):
        for t in (F(1, 2), F(1, 10), F(1)):
            def w(y):
                return t ** max(k - len(y) - 1, 0)
            for mask in range(1 << k):
                s = {i for i in range(k) if mask >> i & 1}
                free = [i for i in range(k) if i not in s]
                rates = {i: w(s | {i}) / w(s) for i in free}
                a = [[(rates[i] ** 2 - rates[i] if i == j
                       else rates[i] * rates[j] - w(s | {i, j}) / w(s))
                      for j in free] for i in free]
                for r in range(1, len(free) + 1):
                    for inds in combinations(range(len(free)), r):
                        assert det([[a[i][j] for j in inds] for i in inds]) >= 0
                psd_matrices += 1
    # A ferromagnetic agreement factor has negative zero-curvature.
    t = F(1, 2)
    agreement_curvature = [[t * t, t * t - 1], [t * t - 1, t * t]]
    assert agreement_curvature[0][0] + agreement_curvature[0][1] == F(-1, 2)
    # Exact log-Hessian for p=1+xy at x=y=1/2.
    partial_flip_hessian = [[F(-4, 25), F(16, 25)],
                            [F(16, 25), F(-4, 25)]]
    assert sum(partial_flip_hessian[0]) == F(12, 25)
    # The quadratic coefficient-square obstruction, using four explicit eigenvectors.
    vectors = [(1, 1, 1, 1), (1, 1, -1, -1),
               (1, -1, 1, -1), (1, -1, -1, 1)]
    spectra = []
    for a, b, c in ((3, 2, 2), (9, 4, 4)):
        h = [[0, a, b, c], [a, 0, c, b], [b, c, 0, a], [c, b, a, 0]]
        eigs = []
        for v in vectors:
            hv = [sum(h[i][j] * v[j] for j in range(4)) for i in range(4)]
            lam = hv[0] // v[0]
            assert hv == [lam * x for x in v]
            eigs.append(lam)
        spectra.append(eigs)
    assert spectra == [[7, -1, -3, -3], [17, 1, -9, -9]]
    return {"rank_penalty_dual_psd_matrices": psd_matrices,
            "agreement_curvature_positive_vector_eigenvalue": "-1/2",
            "partial_flip_log_hessian_positive_eigenvalue": "12/25",
            "quadratic_original_and_squared_Hessian_spectra": spectra}


if __name__ == "__main__":
    print(json.dumps({"tensor_checks": [tensor_check(2), tensor_check(3)],
                      "triple_intersection": parity_check(),
                      "curvature_checks": curvature_check()}, indent=2))
