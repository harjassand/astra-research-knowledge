"""Finite coefficient checks for the nonsimply-laced shell audit.

This checks root combinatorics and coefficient recurrences for B2 and G2;
it is not a construction of the corresponding irreducible matrices.
"""
from fractions import Fraction as Q
import numpy as np

CASES = {
    "B2": {
        "cartan": [[2, -2], [-1, 2]],
        "simple_sq": [Q(1), Q(2)],
        "roots": [(1,0), (0,1), (1,1), (2,1)],
    },
    "G2": {
        "cartan": [[2, -3], [-1, 2]],
        "simple_sq": [Q(2,3), Q(2)],
        "roots": [(1,0), (0,1), (1,1), (2,1), (3,1), (3,2)],
    },
}

def dot(v, w, G):
    return sum(v[i] * G[i][j] * w[j] for i in range(len(v)) for j in range(len(v)))

def case_check(name, dat):
    A, sq, roots = dat["cartan"], dat["simple_sq"], dat["roots"]
    r = len(sq); p = len(roots)
    G = [[Q(A[i][j]) * sq[i] / 2 for j in range(r)] for i in range(r)]
    ht = [sum(x) for x in roots]
    norm2 = [dot(a, a, G) for a in roots]
    coroot_coeff = [[Q(a[i]) * sq[i] / n2 for i in range(r)] for a, n2 in zip(roots, norm2)]
    hvee = [sum(c) for c in coroot_coeff]
    kappa = [n2 / 2 for n2 in norm2]
    pair = [[2 * dot(g, a, G) / na for a, na in zip(roots, norm2)] for g in roots]
    assert all(x.denominator == 1 for row in pair for x in row)
    assert all(x.denominator == 1 for row in coroot_coeff for x in row)
    Amax = max(abs(int(x)) for row in pair for x in row)
    H = max(ht)
    K1 = sum(kappa[i] for i, a in enumerate(roots) if sum(a) == 1)
    assert [tuple(x) for x in roots[:r]] == [tuple(1 if i == j else 0 for i in range(r)) for j in range(r)]

    N = 180 if name == "B2" else 360
    M = N // (2 * Amax)
    qmax = M + H
    g = [0] * (qmax + 1); g[0] = 1
    for ell in ht:
        for q in range(ell, qmax + 1):
            g[q] += g[q-ell]
    V = [sum(g[:q+1]) for q in range(qmax+1)]
    s = [[0] * (qmax + 1) for _ in roots]
    c = [[0] * (qmax + 1) for _ in roots]
    for a_idx, (ell, hv) in enumerate(zip(ht, hvee)):
        L = N * hv
        for q in range(qmax + 1):
            val = L * g[q]
            for gi, hgi in enumerate(ht):
                marked = sum(g[q-t*hgi] for t in range(1, q//hgi + 1))
                val -= pair[gi][a_idx] * marked
            s[a_idx][q] = int(val)
        for q in range(ell, qmax + 1):
            c[a_idx][q] = c[a_idx][q-ell] + s[a_idx][q-ell]
        for q in range(qmax + 1):
            direct = sum(s[a_idx][q-t*ell] for t in range(1, q//ell + 1))
            assert c[a_idx][q] == direct
            if q + ell <= qmax:
                assert c[a_idx][q+ell] - c[a_idx][q] == s[a_idx][q]
        assert all(c[a_idx][q] >= 0 for q in range(ell, M+ell))
        for q in range(ell, M+ell):
            assert Q(kappa[a_idx]) * c[a_idx][q] <= Q(5,2)*N*kappa[a_idx]*hv*V[q-ell]
        for q in range(M+1):
            assert Q(N,2)*g[q] <= s[a_idx][q] <= Q(5,2)*N*hv*g[q]

    c1 = [0] * (qmax + 1)
    for i in range(r):
        for q in range(qmax+1):
            c1[q] += kappa[i] * c[i][q]
    for q in range(1, M+1):
        assert Q(N,2)*K1*V[q-1] <= c1[q] <= Q(5,2)*N*K1*V[q-1]

    Gamma = max(Q(__import__('math').comb(2*H+p,p)), Q(2*p*H*(p+1))**p)
    for a_idx, ell in enumerate(ht):
        for q in range(ell, M+ell):
            j = q-ell+1
            assert j <= M
            lhs = kappa[a_idx]*c[a_idx][q]
            rhs = 5*Gamma*kappa[a_idx]*hvee[a_idx]/K1*c1[j]
            assert lhs <= rhs

    print(f"{name}: A={Amax}, p={p}, H={H}, N={N}, M={M}, K1={K1}, Gamma={Gamma}")
    print("  (root coefficients; height, coroot-height, kappa):")
    for a, h, hv, kap in zip(roots, ht, hvee, kappa):
        print(f"   {a}: {h}, {hv}, {kap}")
    print(f"  PBW shell checks: s bounds through q={M}; conductance and simple comparison through q={M+H-1}: PASS")


def root_pair_matrix_check(alpha_sq):
    j = 1.5
    ms = np.arange(-j, j+1, 1)
    E = np.zeros((4,4), dtype=complex)
    for col, m in enumerate(ms):
        if m < j:
            row = col + 1
            E[row,col] = np.sqrt((j-m)*(j+m+1))
    F = E.conj().T
    H = np.diag(2*ms)
    assert np.max(np.abs(E@F-F@E-H)) < 1e-14
    X = np.diag([0.2, -0.7, 1.1, 0.4])
    b = 2/alpha_sq
    Tx = (E+F)/(2*np.sqrt(b))
    Ty = (E-F)/(2j*np.sqrt(b))
    lhs = np.linalg.norm(Tx@X-X@Tx, 'fro')**2 + np.linalg.norm(Ty@X-X@Ty, 'fro')**2
    rhs = (alpha_sq/2)*np.linalg.norm(E@X-X@E, 'fro')**2
    return abs(lhs-rhs)

for name, dat in CASES.items():
    case_check(name, dat)
for sq in [2.0, 1.0, 2.0/3.0]:
    print(f"root-plane factor alpha^2={sq:g}: abs error={root_pair_matrix_check(sq):.3e}")
