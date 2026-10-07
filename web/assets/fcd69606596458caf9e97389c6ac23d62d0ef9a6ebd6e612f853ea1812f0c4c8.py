"""Exact finite identities; does not implement Chen--Liu or quantum compilation."""
import importlib.util
import itertools
import json
import random
from fractions import Fraction as Q
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "cycle3" / "paired_fermion_checks.py"
spec = importlib.util.spec_from_file_location("paired_checks", path)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
GQ, det, abs2 = base.GQ, base.det, base.abs2


def conj(x):
    x = GQ(x)
    return GQ(x.real, -x.imag)


def rank(matrix):
    a = [[GQ(x) for x in row] for row in matrix]
    if not a:
        return 0
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][j]
        a[r] = [x / v for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                v = a[i][j]
                a[i] = [x + (-1) * v * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def skew(F, z):
    return [[z[i] * F[i][j] + (-1) * z[j] * F[j][i]
             for j in range(len(F))] for i in range(len(F))]


def pf(a):
    if not a:
        return 1
    total = 0
    for j in range(1, len(a)):
        rem = [i for i in range(len(a)) if i not in (0, j)]
        total += (-1) ** (j + 1) * a[0][j] * pf([[a[i][k] for k in rem] for i in rem])
    return total


def random_F(n, rng):
    return [[GQ(Q(rng.randrange(-2, 3), rng.randrange(1, 4)),
                Q(rng.randrange(-2, 3), rng.randrange(1, 4)))
             for j in range(n)] for i in range(n)]


def gram(F, I):
    n = len(F)
    cols = []
    for i in I:
        cols += [[GQ(j == i) for j in range(n)], [F[i][j] for j in range(n)]]
    return [[sum(conj(x) * y for x, y in zip(v, w)) for w in cols] for v in cols]


def disjoint_norm(F, k):
    n = len(F)
    total = Q(0)
    for I in itertools.combinations(range(n), k):
        rest = [i for i in range(n) if i not in I]
        for J in itertools.combinations(rest, k):
            total += abs2(det([[F[i][j] for j in J] for i in I]))
    return total


def parity_identities():
    rng = random.Random(811764)
    cases = gram_checks = pf_checks = phase_checks = 0
    for n in range(2, 7):
        for trial in range(3):
            F = random_F(n, rng)
            if trial == 1:
                F = [[F[i][j] if i < j else GQ(0) for j in range(n)] for i in range(n)]
            if trial == 2:
                F = [[F[0][j] * (i + 1) for j in range(n)] for i in range(n)]
            z = [Q(rng.randrange(1, 11), 3) for _ in range(n)]
            K = skew(F, z)
            d = 0
            for k in range(n // 2 + 1):
                c = disjoint_norm(F, k)
                if c:
                    d = k
                gr = 0
                for I in itertools.combinations(range(n), k):
                    lhs = det(gram(F, I))
                    rhs = sum(abs2(det([[F[i][j] for j in J] for i in I]))
                              for J in itertools.combinations([j for j in range(n) if j not in I], k))
                    assert lhs == rhs
                    gr += lhs
                    gram_checks += 1
                assert gr == c
                for T in itertools.combinations(range(n), 2 * k):
                    lhs = pf([[K[i][j] for j in T] for i in T])
                    rhs = 0
                    for positions in itertools.combinations(range(2 * k), k):
                        I = [T[i] for i in positions]
                        J = [j for j in T if j not in I]
                        term = (-1) ** sum(positions) * det([[F[i][j] for j in J] for i in I])
                        for i in I:
                            term *= z[i]
                        rhs += term
                    assert lhs == rhs
                    pf_checks += 1
                # Orthogonality of all multilinear +/-1 characters, checked exactly.
                phase_sum = Q(0)
                for signs in itertools.product((-1, 1), repeat=n):
                    Ks = skew(F, signs)
                    phase_sum += sum(abs2(pf([[Ks[i][j] for j in T] for i in T]))
                                     for T in itertools.combinations(range(n), 2 * k))
                assert phase_sum / (2 ** n) == c
                phase_checks += 1
            # Specialization can only reduce symbolic rank; sample several exact points.
            ranks = [rank(skew(F, [rng.randrange(101) for _ in range(n)])) for _ in range(4)]
            assert max(ranks) == 2 * d, (n, trial, ranks, d)
            cases += 1
    return {"matrix_cases": cases, "Gram_identities": gram_checks,
            "Pfaffian_identities": pf_checks, "exact_sign_average_sector_identities": phase_checks,
            "generic_rank_tests": 4 * cases, "pass": True}


def bipartite_transfer():
    rng = random.Random(646443)
    cases = configurations = coeffs = phase_signs = 0
    for a, b in [(1, 1), (1, 2), (2, 1), (2, 2), (3, 2), (1, 3)]:
        for trial in range(2):
            n = a + b
            F = random_F(n, rng)
            F = [[F[i][j] if (i < a) != (j < a) else GQ(0) for j in range(n)] for i in range(n)]
            if trial:
                # Include complete hard projection and nonuniform partial factors.
                t = [Q(0) if i % 3 == 0 else Q(i % 3, 3) for i in range(n)]
            else:
                t = [Q(2) if i % 2 else Q(1, 7) for i in range(n)]
            for x in t:
                assert 2 >= x
            M = [[GQ(0) for _ in range(2 * b)] for _ in range(2 * a)]
            for i in range(a):
                for j in range(b):
                    M[i][b + j] = F[i][a + j]
                    M[a + i][j] = (-1) * F[a + j][i]
            A = M + [[GQ(i == j) for j in range(2 * b)] for i in range(2 * b)]
            # Row order u_A,d_A,h_uB,h_dB, mapped to physical canonical modes.
            orig = list(range(a)) + list(range(n, n + a)) + list(range(a, n)) + list(range(n + a, 2 * n))
            Bmodes = list(range(a, n)) + list(range(n + a, 2 * n))
            norm_graph = [Q(0) for _ in range(n + 1)]
            norm_physical = [Q(0) for _ in range(n + 1)]
            for S in itertools.combinations(range(2 * n), 2 * b):
                selected = set(S)
                U = [i for i in range(a) if i in selected] + [a + j for j in range(b) if 2 * a + j not in selected]
                D = [i for i in range(a) if a + i in selected] + [a + j for j in range(b) if 2 * a + b + j not in selected]
                minor = det([A[i] for i in S])
                if len(U) == len(D):
                    k = len(U)
                    amp = (-1) ** (k * (k - 1) // 2) * det([[F[i][j] for j in D] for i in U])
                else:
                    amp = GQ(0)
                assert abs2(minor) == abs2(amp)
                original_occupied = set(U) | {n + j for j in D}
                exponent = sum(sum(l < j for l in original_occupied) for j in Bmodes)
                exponent += sum(j in original_occupied for j in Bmodes)
                permutation = sum(orig[S[i]] > orig[S[j]] for i in range(len(S)) for j in range(i + 1, len(S)))
                assert (-1) ** (exponent + permutation) * minor == amp
                phase_signs += bool(amp)
                graph_weight = abs2(minor)
                for i in range(a):
                    if i in selected and a + i in selected:
                        graph_weight *= t[i]
                for j in range(b):
                    if 2 * a + j not in selected and 2 * a + b + j not in selected:
                        graph_weight *= t[a + j]
                phys_weight = abs2(amp)
                for i in set(U).intersection(D):
                    phys_weight *= t[i]
                assert graph_weight == phys_weight
                if amp:
                    k = len(U)
                    assert k == sum(i < 2 * a for i in S)
                    norm_graph[k] += graph_weight
                configurations += 1
            for k in range(n + 1):
                for U in itertools.combinations(range(n), k):
                    for D in itertools.combinations(range(n), k):
                        w = abs2(det([[F[i][j] for j in D] for i in U]))
                        for i in set(U).intersection(D):
                            w *= t[i]
                        norm_physical[k] += w
                assert norm_physical[k] == norm_graph[k]
                coeffs += 1
            cases += 1
    return {"complex_rational_bipartite_matrices": cases,
            "configuration_sign_and_weight_checks": configurations,
            "nonzero_sign_checks": phase_signs, "canonical_norm_identities": coeffs, "pass": True}


def exponential_variance():
    out = []
    for q in range(1, 9):
        vals = []
        grand = []
        for bits in itertools.product((0, 1), repeat=2 * q):
            splits = sum(bits[2 * j] != bits[2 * j + 1] for j in range(q))
            vals.append(4 ** q if splits == q else 0)
            grand.append(5 ** splits)
        N = 2 ** (2 * q)
        mean = Q(sum(vals), N)
        second = Q(sum(x * x for x in vals), N)
        assert mean == 2 ** q and second / (mean * mean) == 2 ** q
        mg = Q(sum(grand), N)
        sg = Q(sum(x * x for x in grand), N)
        assert mg == 3 ** q and sg / (mg * mg) == Q(13, 9) ** q
        out.append({"swap_blocks": q, "top_sector_relative_variance": str(second / mean ** 2 - 1),
                    "grand_norm_relative_second_moment_at_s1": str(sg / mg ** 2)})
    return {"exact_independent_block_cases": out, "pass": True}


def poly_add(a, b):
    out = [Q(0) for _ in range(max(len(a), len(b)))]
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += x
    return out


def poly_mul(a, b):
    out = [Q(0) for _ in range(len(a) + len(b) - 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def poly_matmul(A, B):
    return [[poly_add(poly_mul(A[i][0], B[0][j]), poly_mul(A[i][1], B[1][j]))
             for j in range(2)] for i in range(2)]


def monomial_dp(p, w, t, fixed):
    seen = set()
    ans = [Q(1)]
    for start in range(len(p)):
        if start in seen:
            continue
        cyc = []
        i = start
        while i not in seen:
            seen.add(i)
            cyc.append(i)
            i = p[i]
        M = [[[Q(1)], [Q(0)]], [[Q(0)], [Q(1)]]]
        for i in cyc:
            T = [[[Q(1)], [Q(0), w[i]]], [[Q(1)], [Q(0), w[i] * t[i]]]]
            if i in fixed:
                for a in range(2):
                    T[a][1 - fixed[i]] = [Q(0)]
            M = poly_matmul(M, T)
        ans = poly_mul(ans, poly_add(M[0][0], M[1][1]))
    return ans + [Q(0)] * (len(p) + 1 - len(ans))


def monomial_checks():
    rng = random.Random(928017)
    cases = queries = minor_checks = 0
    for n in range(1, 9):
        for trial in range(3):
            p = list(range(n))
            rng.shuffle(p)
            f = [GQ(Q(rng.randrange(1, 4), 3), Q(rng.randrange(-2, 3), 4)) for i in range(n)]
            w = [abs2(x) for x in f]
            t = [Q(rng.randrange(0, 6), 3) for i in range(n)]
            for query in range(5):
                fixed = {i: rng.randrange(2) for i in range(n) if query and rng.randrange(3) == 0}
                exact = [Q(0) for i in range(n + 1)]
                for bits in itertools.product((0, 1), repeat=n):
                    if any(bits[i] != b for i, b in fixed.items()):
                        continue
                    I = {i for i in range(n) if bits[i]}
                    J = {p[i] for i in I}
                    val = Q(1)
                    for i in I:
                        val *= w[i]
                    for i in I.intersection(J):
                        val *= t[i]
                    exact[len(I)] += val
                    if n <= 5 and query == 0:
                        F = [[f[i] if j == p[i] else GQ(0) for j in range(n)] for i in range(n)]
                        expected = Q(1)
                        for i in I:
                            expected *= w[i]
                        assert abs2(det([[F[i][j] for j in sorted(J)] for i in sorted(I)])) == expected
                        minor_checks += 1
                assert monomial_dp(p, w, t, fixed) == exact
                queries += 1
            cases += 1
    return {"weighted_permutation_matrices": cases, "exact_prefix_polynomial_DP_queries": queries,
            "monomial_minor_magnitudes": minor_checks, "pass": True}


if __name__ == "__main__":
    result = {"parity": parity_identities(), "bipartite": bipartite_transfer(),
              "variance": exponential_variance(), "monomial": monomial_checks()}
    target = Path(__file__).with_name("hard_bcs_transfer_checks_result.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
