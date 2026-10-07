"""Rational Gaussian MPS acquisition from exact off-diagonal cut ranks.

No SVD, spectral gap, approximate low-rank promise, or projected-norm oracle.
The finite executable checks are deliberately tiny. Gaussian transition Wick
moments acquire nonorthogonal Schmidt-basis tensors by exact Gram inversion.
"""
from fractions import Fraction
from random import Random
from pathlib import Path
from time import perf_counter
import json
from near_monomial_dp import G, brute_counts, add
from rank_certificate_sampler import qdiv


def conv(F): return [[x if isinstance(x, G) else G(x) for x in row] for row in F]


def eye(n): return [[G(int(i == j)) for j in range(n)] for i in range(n)]


def transpose(M): return [list(x) for x in zip(*M)]


def adjoint(M): return [[x.conjugate() for x in row] for row in transpose(M)]


def matmul(A, B):
    if not A: return []
    width = len(B[0]) if B else 0
    return [[sum((a * B[k][j] for k, a in enumerate(row)), G())
             for j in range(width)] for row in A]


def inverse(M):
    n = len(M); R = [row[:] + erow for row, erow in zip(M, eye(n))]
    for j in range(n):
        p = next(i for i in range(j, n) if R[i][j])
        R[j], R[p] = R[p], R[j]
        pivot = R[j][j]; R[j] = [qdiv(x, pivot) for x in R[j]]
        for i in range(n):
            if i == j or not R[i][j]: continue
            z = R[i][j]; R[i] = [x - z * y for x, y in zip(R[i], R[j])]
    return [row[n:] for row in R]


def det(M):
    R = [row[:] for row in M]; n = len(R); answer = G(1)
    for j in range(n):
        p = next((i for i in range(j, n) if R[i][j]), None)
        if p is None: return G()
        if p != j: R[j], R[p] = R[p], R[j]; answer = -answer
        pivot = R[j][j]; answer *= pivot
        for i in range(j + 1, n):
            if not R[i][j]: continue
            z = qdiv(R[i][j], pivot)
            R[i] = [x - z * y for x, y in zip(R[i], R[j])]
    return answer


def factor_rect(M, width=None):
    m = len(M); q = len(M[0]) if m else (width or 0)
    R = [row[:] for row in M]; rank = 0; pivots = []
    for j in range(q):
        p = next((i for i in range(rank, m) if R[i][j]), None)
        if p is None: continue
        R[rank], R[p] = R[p], R[rank]
        den = R[rank][j]; R[rank] = [qdiv(x, den) for x in R[rank]]
        for i in range(m):
            if i == rank or not R[i][j]: continue
            z = R[i][j]; R[i] = [x - z * y for x, y in zip(R[i], R[rank])]
        pivots.append(j); rank += 1
    U = [[row[j] for j in pivots] for row in M]
    V = [[R[a][j] for a in range(rank)] for j in range(q)]
    return rank, U, V


def pfaffian(K):
    if len(K) % 2: return G()
    R = [row[:] for row in K]; answer = G(1)
    while R:
        n = len(R)
        p = next((j for j in range(1, n) if R[0][j]), None)
        if p is None: return G()
        if p != 1:
            R[1], R[p] = R[p], R[1]
            for row in R: row[1], row[p] = row[p], row[1]
            answer = -answer
        pivot = R[0][1]; answer *= pivot
        R = [[R[i][j] - qdiv(R[0][i] * R[1][j] - R[0][j] * R[1][i], pivot)
              for j in range(2, n)] for i in range(2, n)]
    return answer


def transition_wick(A, B):
    """Return overlap and CAR two-point table for braA/ketB.

    Matrices use opposite-spin pairing. The call sites use A=B or A equal
    to the preceding principal block of B padded by zeros, so all needed
    inverses are nonsingular without a conditioning promise.
    """
    m = len(A); I = eye(m)
    BA = matmul(B, adjoint(A))
    BTAbar = matmul(transpose(B), [[x.conjugate() for x in row] for row in A])
    Q = inverse([[I[i][j] + BA[i][j] for j in range(m)] for i in range(m)])
    R = inverse([[I[i][j] + BTAbar[i][j] for j in range(m)] for i in range(m)])
    QB = matmul(Q, B)
    AbarR = matmul([[x.conjugate() for x in row] for row in A], R)
    AB = matmul(adjoint(A), B)
    overlap = det([[I[i][j] + AB[i][j] for j in range(m)] for i in range(m)])
    assert overlap
    size = 2 * m
    # Operator kind0 annihilator, kind1 creator; modes interleaved a_i,b_i.
    table = [[[[G() for _ in range(size)] for _ in range(size)] for _ in range(2)] for _ in range(2)]
    for u in range(size):
        i, species = divmod(u, 2)
        for v in range(size):
            j, other = divmod(v, 2)
            if species == other:
                N = Q if species == 0 else R
                table[0][1][u][v] = N[i][j]
                table[1][0][u][v] = G(int(u == v)) - N[j][i]
            elif species == 0:
                table[0][0][u][v] = -QB[i][j]
                table[1][1][u][v] = AbarR[i][j]
            else:
                table[0][0][u][v] = QB[j][i]
                table[1][1][u][v] = -AbarR[j][i]
    return overlap, table


def overlap_forms(wick, left, right):
    norm, table = wick
    operators = [(0, [x.conjugate() for x in row]) for row in reversed(left)]
    operators += [(1, row) for row in right]
    if len(operators) % 2: return G()
    K = [[G() for _ in operators] for _ in operators]
    for i, (kind, x) in enumerate(operators):
        for j in range(i + 1, len(operators)):
            kind2, y = operators[j]
            moment = sum((xx * yy * table[kind][kind2][u][v]
                          for u, xx in enumerate(x) if xx
                          for v, yy in enumerate(y) if yy), G())
            K[i][j], K[j][i] = moment, -moment
    return norm * pfaffian(K)


def left_forms(F, cut):
    n = len(F)
    r1, U1, _ = factor_rect([row[cut:] for row in F[:cut]], n - cut)
    r2, _, V2 = factor_rect([row[:cut] for row in F[cut:]], cut)
    forms = []
    for a in range(r1):
        form = [G() for _ in range(2 * cut)]
        for i in range(cut): form[2 * i] = U1[i][a]
        forms.append(form)
    for a in range(r2):
        form = [G() for _ in range(2 * cut)]
        for i in range(cut): form[2 * i + 1] = V2[i][a]
        forms.append(form)
    return forms


def subsets(forms):
    return [[row for a, row in enumerate(forms) if mask >> a & 1]
            for mask in range(1 << len(forms))]


def acquire_mps(F):
    F = conv(F); n = len(F)
    bases = [subsets(left_forms(F, cut)) for cut in range(n + 1)]
    tensors = []; width = max((len(b).bit_length() - 1 for b in bases), default=0)
    for i in range(1, n + 1):
        previous = [[x + [G(), G()] for x in basis] for basis in bases[i - 1]]
        current = bases[i]
        A = [[F[r][c] if r < i - 1 and c < i - 1 else G() for c in range(i)] for r in range(i)]
        B = [row[:i] for row in F[:i]]
        gram_wick = transition_wick(A, A)
        Gprev = [[overlap_forms(gram_wick, l, r) for r in previous] for l in previous]
        invG = inverse(Gprev)
        trans = transition_wick(A, B)
        site_tensors = []
        for physical in range(4):
            local = []
            if physical & 1:
                x = [G() for _ in range(2 * i)]; x[-2] = G(1); local.append(x)
            if physical >> 1:
                x = [G() for _ in range(2 * i)]; x[-1] = G(1); local.append(x)
            overlaps = [[overlap_forms(trans, left + local, right) for right in current]
                        for left in previous]
            site_tensors.append(matmul(invG, overlaps))
        tensors.append(site_tensors)
    return tensors, {'maximum_cut_rank_sum': width, 'bonds': [len(x) for x in bases]}


def projected_counts(tensors, activities=None, row_constraints=None, col_constraints=None):
    n = len(tensors); maxk = n // 2
    acts = activities if activities is not None else [1] * n
    rc, cc = row_constraints or {}, col_constraints or {}
    state = {(0, 0, 0): G(1)}
    for i, matrices in enumerate(tensors):
        nxt = {}
        for physical in (0, 1, 2):
            row, col = physical & 1, physical >> 1
            if i in rc and rc[i] != row: continue
            if i in cc and cc[i] != col: continue
            M = matrices[physical]
            for (a, b, k), z in state.items():
                if k + row > maxk: continue
                for c, u in enumerate(M[a]):
                    if not u: continue
                    for d, v in enumerate(M[b]):
                        if v: add(nxt, (c, d, k + row), z * u * v.conjugate() * G(acts[i] if row else 1))
        state = nxt
    out = [state.get((0, 0, k), G()) for k in range(maxk + 1)]
    assert all(x.im == 0 and x.re >= 0 for x in out), out
    return [x.re for x in out]


def exact_sample(tensors, k, rng, activities=None):
    from math import lcm
    rc, cc = {}, {}
    choices = ((0, 0), (1, 0), (0, 1))
    for i in range(len(tensors)):
        masses = []
        for row, col in choices:
            rr, c = dict(rc), dict(cc); rr[i], c[i] = row, col
            masses.append(Fraction(projected_counts(tensors, activities, rr, c)[k]))
        if not sum(masses): raise ValueError('zero norm conditional sector')
        den = lcm(*(x.denominator for x in masses))
        weights = [int(x * den) for x in masses]
        draw = rng.randrange(sum(weights))
        for choice, weight in zip(choices, weights):
            if draw < weight:
                rc[i], cc[i] = choice
                break
            draw -= weight
    return tuple(i for i, v in rc.items() if v), tuple(i for i, v in cc.items() if v)


def run_checks():
    rng = Random(61305); t0 = perf_counter(); cases = prefix = 0; bonds = []
    fixtures = []
    for n in (3, 4):
        for _ in range(4):
            fixtures.append([[G(rng.randint(-1, 1), rng.randint(-1, 1)) for _ in range(n)] for _ in range(n)])
    # Growing-size, fixed cut-rank family: cycle monomial plus rank1.
    for n in (6, 8):
        F = [[G(1) for _ in range(n)] for _ in range(n)]
        for i in range(n): F[i][(i + 1) % n] += G(1, i % 2)
        fixtures.append(F)
    # Exact rational entries and activities with a tiny nonzero target norm.
    fixtures.append([[G() if i == j else G(Fraction(i + j + 1, 1024), Fraction(i - j, 2048))
                      for j in range(4)] for i in range(4)])
    samples = []
    for F in fixtures:
        n = len(F)
        tensors, stats = acquire_mps(F)
        acts = [rng.randint(1, 3) for _ in range(n)]
        if isinstance(F[0][-1].re, Fraction): acts = [Fraction(x, 64) for x in acts]
        got = projected_counts(tensors, acts)
        want = brute_counts(F, acts)
        assert got == want, (n, got, want)
        cases += 1; bonds.append(stats)
        for size in (1, 2):
            choices = [rng.choice(((0, 0), (1, 0), (0, 1))) for _ in range(size)]
            rc = {i: x[0] for i, x in enumerate(choices)}
            cc = {i: x[1] for i, x in enumerate(choices)}
            assert projected_counts(tensors, acts, rc, cc) == brute_counts(F, acts, rc, cc)
            prefix += 1
        if n == 8:
            k = max(i for i, x in enumerate(got) if x)
            I, J = exact_sample(tensors, k, rng, acts)
            from near_monomial_dp import determinant
            assert not set(I) & set(J) and determinant([[F[i][j] for j in J] for i in I]).abs2() > 0
            samples.append({'n': n, 'k': k, 'I': I, 'J': J})
    return {'status': 'PASS', 'seed': 61305, 'Gaussian_integer_matrices': cases,
            'exact_prefix_comparisons': prefix, 'acquired_bond_schedules': bonds,
            'support_valid_samples': samples,
            'elapsed_seconds': perf_counter() - t0,
            'scope': 'Tiny exact rational cut-rank/Wick/Gram tensor acquisition against independent determinant sums; no asymptotic performance benchmark.'}


if __name__ == '__main__':
    result = run_checks()
    Path(__file__).with_name('cutrank_checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
