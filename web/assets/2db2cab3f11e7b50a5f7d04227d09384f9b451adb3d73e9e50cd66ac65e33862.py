"""Independent exact Pauli-word trace audit of the Spin(9) three-copy star.

Unlike a highest-weight restriction, this code never constructs a multiplicity
basis. It builds the full 12-qubit Pauli-word operator algebra, projects by the
quadratic Casimir, and extracts each output-swap block's characteristic
coefficients from full-space traces. All arithmetic is exact Gaussian integer
plus Fraction arithmetic.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
from math import comb
import json
from pathlib import Path
import sys

NQ = 12
MASK = (1 << NQ) - 1
DIM = 1 << NQ
ID = 0

# A 12-qubit Hermitian Pauli word is keyed by x | (z << 12),
# representing P(x,z)=i^{x.z} X^x Z^z. Coefficients are Gaussian integers.
GI = tuple[int, int]
ZERO: GI = (0, 0)
ONE: GI = (1, 0)


def gadd(a: GI, b: GI) -> GI:
    return a[0] + b[0], a[1] + b[1]


def gmul(a: GI, b: GI) -> GI:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def grot(a: GI, phase: int) -> GI:
    phase %= 4
    if phase == 0:
        return a
    if phase == 1:
        return -a[1], a[0]
    if phase == 2:
        return -a[0], -a[1]
    return a[1], -a[0]


def pkey_from_word(word: tuple[str, ...]) -> int:
    x = z = 0
    for j, ch in enumerate(word):
        if ch in "XY":
            x |= 1 << j
        if ch in "YZ":
            z |= 1 << j
    # Gamma generators live on four spinor qubits; keep this compact encoding
    # (x | z<<4) until the word is embedded into one of the three factors.
    return x | (z << len(word))


def pkey_mul_n(a: int, b: int, n: int) -> tuple[int, int]:
    mask = (1 << n) - 1
    x, z = a & mask, a >> n
    xp, zp = b & mask, b >> n
    phase = ((x & z).bit_count() + (xp & zp).bit_count()
             - ((x ^ xp) & (z ^ zp)).bit_count()
             + 2 * (z & xp).bit_count()) % 4
    return (x ^ xp) | ((z ^ zp) << n), phase


def pkey_mul(a: int, b: int) -> tuple[int, int]:
    return pkey_mul_n(a, b, NQ)


def pkey_transpose_sign(key: int) -> int:
    return -1 if ((key & MASK) & (key >> NQ)).bit_count() % 2 else 1


def pkey4_transpose_sign(key: int) -> int:
    return -1 if ((key & 15) & (key >> 4)).bit_count() % 2 else 1


def embed4(key4: int, factor: int) -> int:
    x4, z4 = key4 & 15, key4 >> 4
    x, z = x4 << (4 * factor), z4 << (4 * factor)
    return x | (z << NQ)


def add_term(a: dict[int, GI], key: int, value: GI) -> None:
    if value == ZERO:
        return
    nxt = gadd(a.get(key, ZERO), value)
    if nxt == ZERO:
        a.pop(key, None)
    else:
        a[key] = nxt


def clean_real(a: dict[int, GI], label: str) -> dict[int, int]:
    out: dict[int, int] = {}
    for k, (re, im) in a.items():
        if im:
            raise AssertionError(f"{label} has imaginary Hermitian-Pauli coefficient {k}: {(re, im)}")
        if re:
            out[k] = re
    return out


def mul(A: dict[int, int], B: dict[int, int], label: str) -> dict[int, int]:
    acc: dict[int, list[int]] = {}
    for ka, ca in A.items():
        for kb, cb in B.items():
            key, phase = pkey_mul(ka, kb)
            z = ca * cb
            if phase == 1:
                pair = (0, z)
            elif phase == 2:
                pair = (-z, 0)
            elif phase == 3:
                pair = (0, -z)
            else:
                pair = (z, 0)
            old = acc.get(key)
            if old is None:
                acc[key] = [pair[0], pair[1]]
            else:
                old[0] += pair[0]
                old[1] += pair[1]
    out = {}
    for k, (re, im) in acc.items():
        if im:
            raise AssertionError(f"{label} product not real at {k}: {(re, im)}")
        if re:
            out[k] = re
    return out


def mul_gaussian(A: dict[int, GI], B: dict[int, GI], label: str) -> dict[int, GI]:
    acc: dict[int, list[int]] = {}
    for ka, ca in A.items():
        for kb, cb in B.items():
            key, phase = pkey_mul(ka, kb)
            pair = grot(gmul(ca, cb), phase)
            old = acc.get(key)
            if old is None:
                acc[key] = [pair[0], pair[1]]
            else:
                old[0] += pair[0]
                old[1] += pair[1]
    out = {k: (re, im) for k, (re, im) in acc.items() if re or im}
    return out


def gamma_words() -> list[tuple[str, ...]]:
    out = []
    for j in range(4):
        pre, suf = ("Z",) * j, ("I",) * (3 - j)
        out += [pre + ("X",) + suf, pre + ("Y",) + suf]
    out.append(("Z",) * 4)
    return out


GAMMA_WORDS = gamma_words()
GAMMA_KEYS = [pkey_from_word(w) for w in GAMMA_WORDS]


def word_product(keys: list[int]) -> tuple[int, int]:
    key, phase = ID, 0
    for b in keys:
        key, p = pkey_mul_n(key, b, 4)
        phase = (phase + p) % 4
    return key, phase


def clifford_grade_terms() -> dict[int, list[tuple[int, int]]]:
    out: dict[int, list[tuple[int, int]]] = {k: [] for k in range(1, 5)}
    for k in range(1, 5):
        for A in combinations(range(9), k):
            key, phase = word_product([GAMMA_KEYS[j] for j in A])
            phase = (phase + k * (k - 1) // 2) % 4
            if phase not in (0, 2):
                raise AssertionError(("T_A not Hermitian", A, phase))
            # T_A=sign*P_A. Its transpose sign depends only on the Pauli word.
            trans = pkey4_transpose_sign(key)
            out[k].append((key, trans))
    return out


GRADE_TERMS = clifford_grade_terms()


def star_blocks() -> dict[int, dict[int, int]]:
    out = {k: {} for k in range(1, 5)}
    for k, terms in GRADE_TERMS.items():
        for key4, trans in terms:
            # T_A^T on the dual/reference leg, and T_A on either output.
            add_term(out[k], embed4(key4, 0) | embed4(key4, 1), (trans, 0))
            add_term(out[k], embed4(key4, 0) | embed4(key4, 2), (trans, 0))
    return {k: clean_real(v, f"H_{k}") for k, v in out.items()}


def generator_double(i: int, j: int) -> tuple[int, int]:
    """Return key/phase for Gamma_i Gamma_j, i<j."""
    return word_product([GAMMA_KEYS[i], GAMMA_KEYS[j]])


def total_generator2(i: int, j: int) -> dict[int, GI]:
    """Exact 2J_ij on S* tensor S tensor S."""
    k4, phase = generator_double(i, j)
    coef = grot(ONE, phase)
    trsign = pkey4_transpose_sign(k4)
    J2: dict[int, GI] = {}
    # The dual/reference action is -L^T; the two output actions are +L.
    add_term(J2, embed4(k4, 0), grot(coef, 2) if trsign == 1 else coef)
    add_term(J2, embed4(k4, 1), coef)
    add_term(J2, embed4(k4, 2), coef)
    return J2


def casimir4() -> dict[int, int]:
    # On S* tensor S tensor S the Lie generator is -L^T + L + L,
    # where 2L_ij=Gamma_i Gamma_j. C4=4*C2=-sum_{i<j}(2J_ij)^2.
    total: dict[int, GI] = {}
    for i, j in combinations(range(9), 2):
        J2 = total_generator2(i, j)
        sq = mul_gaussian(J2, J2, f"J2^2_{i}_{j}")
        for key, value in sq.items():
            add_term(total, key, (-value[0], -value[1]))
    return clean_real(total, "C4")


def verify_clifford_star_and_casimir(H: dict[int, dict[int, int]], C: dict[int, int]) -> None:
    # Clifford anticommutators in the exact compact four-qubit Pauli algebra.
    for i, j in combinations(range(9), 2):
        ij, pij = pkey_mul_n(GAMMA_KEYS[i], GAMMA_KEYS[j], 4)
        ji, pji = pkey_mul_n(GAMMA_KEYS[j], GAMMA_KEYS[i], 4)
        if ij != ji or ((pij - pji) % 4) != 2:
            raise AssertionError(("Clifford anticommutator", i, j, ij, ji, pij, pji))
    if len({key for grade in GRADE_TERMS.values() for key, _ in grade} | {0}) != 256:
        raise AssertionError("grades 0..4 are not 256 distinct Pauli basis words")
    for k, Hk in H.items():
        expected_terms = 2 * comb(9, k)
        if len(Hk) != expected_terms or any(v not in (-1, 1) for v in Hk.values()):
            raise AssertionError(("star support/transpose signs", k, len(Hk), expected_terms))
        for ell, Hl in H.items():
            inner = DIM * sum(v * Hl.get(key, 0) for key, v in Hk.items())
            expected = DIM * expected_terms if k == ell else 0
            if inner != expected:
                raise AssertionError(("grade-star trace normalization", k, ell, inner, expected))
        for key, value in Hk.items():
            x, z = key & MASK, key >> NQ
            swapped = ((x & 15) | (((x >> 8) & 15) << 4) | (((x >> 4) & 15) << 8))
            swapped |= (((z & 15) | (((z >> 8) & 15) << 4) | (((z >> 4) & 15) << 8)) << NQ)
            if Hk.get(swapped, 0) != value:
                raise AssertionError(("star not output-swap invariant", k, key, swapped))
    # The full tensor Casimir must commute with all 36 diagonal Spin(9) generators.
    Cgi = {key: (value, 0) for key, value in C.items()}
    for i, j in combinations(range(9), 2):
        J = total_generator2(i, j)
        CJ, JC = mul_gaussian(Cgi, J, f"C4J_{i}_{j}"), mul_gaussian(J, Cgi, f"J_C4_{i}_{j}")
        for key in set(CJ) | set(JC):
            if gadd(CJ.get(key, ZERO), (-JC.get(key, ZERO)[0], -JC.get(key, ZERO)[1])) != ZERO:
                raise AssertionError(("quadratic Casimir not central", i, j, key))
        for k, Hk in H.items():
            Hgi = {word: (value, 0) for word, value in Hk.items()}
            JH = mul_gaussian(J, Hgi, f"JH_{i}_{j}_{k}")
            HJ = mul_gaussian(Hgi, J, f"HJ_{i}_{j}_{k}")
            for key in set(JH) | set(HJ):
                if gadd(JH.get(key, ZERO), (-HJ.get(key, ZERO)[0], -HJ.get(key, ZERO)[1])) != ZERO:
                    raise AssertionError(("star not Spin(9)-invariant", k, i, j, key))


def verify_casimir_minimal_polynomial(Cpowers: list[dict[int, int]], mu: list[int]) -> None:
    coeff = [1]
    for root in mu:
        nxt = [0] * (len(coeff) + 1)
        for j, value in enumerate(coeff):
            nxt[j] -= root * value
            nxt[j + 1] += value
        coeff = nxt
    remainder: dict[int, int] = {}
    for degree, scalar in enumerate(coeff):
        for key, value in Cpowers[degree].items():
            z = remainder.get(key, 0) + scalar * value
            if z:
                remainder[key] = z
            else:
                remainder.pop(key, None)
    if remainder:
        raise AssertionError(("Casimir minimal polynomial", coeff, len(remainder), list(remainder.items())[:8]))


def casimir_data() -> tuple[list[int], list[int], list[int], list[list[F]]]:
    rho = [F(7, 2), F(5, 2), F(3, 2), F(1, 2)]
    cas, dims = [], []
    for r in range(5):
        lam = [F(3, 2) if j < r else F(1, 2) for j in range(4)]
        cas.append(int(sum(lam[j] * (lam[j] + 2 * rho[j]) for j in range(4))))
        wd = F(1)
        for i in range(4):
            for j in range(i + 1, 4):
                wd *= (lam[i] + rho[i] - lam[j] - rho[j]) / (rho[i] - rho[j])
                wd *= (lam[i] + rho[i] + lam[j] + rho[j]) / (rho[i] + rho[j])
            wd *= (lam[i] + rho[i]) / rho[i]
        if wd.denominator != 1:
            raise AssertionError(("nonintegral Weyl dimension", r, wd))
        dims.append(wd.numerator)
    mu = [4 * x for x in cas]
    projector_polys = []
    for r in range(5):
        coeff = [F(1)]  # low degree first
        denominator = F(1)
        for s in range(5):
            if s == r:
                continue
            nxt = [F(0)] * (len(coeff) + 1)
            for j, x in enumerate(coeff):
                nxt[j] -= mu[s] * x
                nxt[j + 1] += x
            coeff = nxt
            denominator *= mu[r] - mu[s]
        projector_polys.append([x / denominator for x in coeff])
    return cas, mu, dims, projector_polys


def swap_trace_data(B: dict[int, int]) -> int:
    """Tr(S B), where S swaps the two 16-d output factors."""
    # Swap_16 = (1/16) sum_{P in 4-qubit Pauli basis} I tensor P tensor P.
    acc = 0
    for key, value in B.items():
        x, z = key & MASK, key >> NQ
        # P_ref must be identity, and P_out1 must equal P_out2.
        if (x & 15) or (z & 15):
            continue
        x1, x2 = (x >> 4) & 15, (x >> 8) & 15
        z1, z2 = (z >> 4) & 15, (z >> 8) & 15
        if x1 == x2 and z1 == z2:
            acc += value
    # Tr(P_a P_b)=4096 delta_ab; the swap expansion contributes 1/16.
    return 256 * acc


def trace_identity(B: dict[int, int]) -> int:
    return DIM * B.get(ID, 0)


def projector_trace_moments(Cpowers: list[dict[int, int]], Gpower: dict[int, int]) -> tuple[list[int], list[int]]:
    """Return Tr(C^s G^j) and Tr(S C^s G^j) for all s using exact word algebra.

    Products are Hermitian and C commutes with G. For the no-swap trace,
    Pauli orthogonality reduces the result to a coefficient dot product. For
    the swap trace, expand S against the matching Pauli words directly.
    """
    ordinary = [DIM * sum(Cp.get(k, 0) * v for k, v in Gpower.items())
                for Cp in Cpowers]
    # S B coefficient at u is (1/16) sum_p phase(Q_p B_v), with Q_p=I P P.
    # Instead of materializing S*B, stream over p and v and take its dot with C^s.
    swapped_acc: list[GI] = [(0, 0) for _ in Cpowers]
    swap_keys = []
    for p4 in range(256):
        x4, z4 = p4 & 15, p4 >> 4
        qkey = ((x4 << 4) | (x4 << 8)) | (((z4 << 4) | (z4 << 8)) << NQ)
        swap_keys.append(qkey)
    for vb, cb in Gpower.items():
        for qkey in swap_keys:
            uk, phase = pkey_mul(qkey, vb)
            for s, Cp in enumerate(Cpowers):
                ca = Cp.get(uk, 0)
                if ca:
                    swapped_acc[s] = gadd(swapped_acc[s], grot((ca * cb, 0), phase))
    swapped = []
    for acc in swapped_acc:
        if acc[1]:
            raise AssertionError(("imaginary swapped trace", acc))
        swapped.append(256 * acc[0])
    return ordinary, swapped


def enum_support_rays() -> tuple[list[list[tuple[int, int, int, int]]], list[tuple[int, int, int, int]]]:
    """Enumerate exact rays by intersecting triples of active inequalities."""
    vertices = [
        (1, 0, 0, 14),
        (0, 1, 7, 7),
        (1, 4, 4, 6),
    ]
    rows = [tuple(int(i == j) for j in range(4)) for i in range(4)]
    cones = []
    for winner in range(3):
        active_rows = rows + [tuple(vertices[winner][j] - vertices[s][j] for j in range(4))
                              for s in range(3) if s != winner]
        rays = set()
        # Exact one-dimensional kernels in R^4 via 3x3 cofactors.
        for chosen in combinations(active_rows, 3):
            # Null vector is the signed list of 3x3 minors.
            v = []
            for col in range(4):
                mat = [list(row[:col] + row[col + 1:]) for row in chosen]
                det = (mat[0][0] * (mat[1][1] * mat[2][2] - mat[1][2] * mat[2][1])
                       - mat[0][1] * (mat[1][0] * mat[2][2] - mat[1][2] * mat[2][0])
                       + mat[0][2] * (mat[1][0] * mat[2][1] - mat[1][1] * mat[2][0]))
                v.append((-1 if col % 2 else 1) * det)
            if not any(v):
                continue
            for sign in (1, -1):
                w = tuple(sign * x for x in v)
                if all(sum(a * b for a, b in zip(row, w)) >= 0 for row in active_rows):
                    common = 0
                    from math import gcd
                    for x in w:
                        common = gcd(common, abs(x))
                    rays.add(tuple(x // common for x in w))
                    break
        cones.append(sorted(rays))
    union = sorted(set().union(*map(set, cones)))
    return cones, union


def add_scaled(A: dict[int, int], B: dict[int, int], scale: int) -> dict[int, int]:
    C = dict(A)
    for k, v in B.items():
        z = C.get(k, 0) + scale * v
        if z:
            C[k] = z
        else:
            C.pop(k, None)
    return C


def integer_power(A: dict[int, int], n: int, label: str) -> list[dict[int, int]]:
    out = [{ID: 1}]
    for j in range(n):
        out.append(mul(out[-1], A, f"{label}^{j+1}"))
    return out


def support_bound(alpha: tuple[int, int, int, int]) -> int:
    trace = sum(x * y for x, y in zip((9, 36, 84, 126), alpha))
    score = max(sum(a * b for a, b in zip(v, alpha)) for v in (
        (1, 0, 0, 14), (0, 1, 7, 7), (1, 4, 4, 6)))
    return trace + score


def block_moments(ordinary: list[int], swapped: list[int], polys: list[list[F]],
                  dims: list[int]) -> tuple[list[int], list[int]]:
    plus, minus = [], []
    for r, poly in enumerate(polys):
        for sign, out in ((1, plus), (-1, minus)):
            tr = F(0)
            for s, coef in enumerate(poly):
                tr += coef * (ordinary[s] + sign * swapped[s]) / 2
            block = tr / dims[r]
            if block.denominator != 1:
                raise AssertionError(("nonintegral block trace", r, sign, block))
            out.append(block.numerator)
    return plus, minus


def newton(power_sums: list[F]) -> list[F]:
    """Return e_1,...,e_m from the first m power sums."""
    e = [F(1)]
    for k in range(1, len(power_sums) + 1):
        val = sum(((-1) ** (j - 1)) * e[k - j] * power_sums[j - 1]
                  for j in range(1, k + 1)) / k
        e.append(val)
    return e[1:]


def main() -> None:
    H = star_blocks()
    C = casimir4()
    verify_clifford_star_and_casimir(H, C)
    cas, mu, dims, polys = casimir_data()
    cpowers = integer_power(C, 5, "C4")
    verify_casimir_minimal_polynomial(cpowers, mu)
    projector_cpowers = cpowers[:5]

    # Check the Pauli Casimir eigenvalues and multiplicities by trace projectors.
    cones, rays = enum_support_rays()
    expected_cones = [
        {(0, 0, 0, 1), (0, 0, 1, 1), (0, 2, 0, 1), (0, 7, 5, 6), (1, 0, 0, 0), (7, 0, 2, 1)},
        {(0, 0, 1, 0), (0, 0, 1, 1), (0, 1, 1, 0), (0, 7, 5, 6), (3, 0, 1, 0), (7, 0, 2, 1)},
        {(0, 1, 0, 0), (0, 1, 1, 0), (0, 2, 0, 1), (0, 7, 5, 6), (1, 0, 0, 0), (3, 0, 1, 0), (7, 0, 2, 1)},
    ]
    if [set(x) for x in cones] != expected_cones or len(rays) != 10:
        raise AssertionError(("support cones", cones, rays))

    ident = {ID: 1}
    i_mom, s_mom = projector_trace_moments(projector_cpowers, ident)
    plus_dim, minus_dim = block_moments(i_mom, s_mom, polys, dims)
    expected_plus, expected_minus = [3, 2, 1, 1, 1], [2, 2, 2, 1, 0]
    if plus_dim != expected_plus:
        raise AssertionError(("even multiplicities", plus_dim))
    if minus_dim != expected_minus:
        raise AssertionError(("odd multiplicities", minus_dim))

    all_blocks = []
    max_support = {"C4": len(C), "C4_powers": [len(x) for x in cpowers]}
    for alpha in rays:
        B = support_bound(alpha)
        G = {ID: B}
        for k in range(1, 5):
            G = add_scaled(G, H[k], -alpha[k - 1])
        if G.get(ID, 0) != B:
            raise AssertionError("identity coefficient changed")
        mmax = 3
        gpowers = integer_power(G, mmax, f"G{alpha}")
        max_support[str(alpha)] = [len(x) for x in gpowers]
        moments_by_j = []
        for j in range(mmax + 1):
            moments_by_j.append(projector_trace_moments(projector_cpowers, gpowers[j]))

        ray_cert = {"alpha": alpha, "bound": B, "blocks": []}
        for r in range(5):
            for eps, mult, label in ((1, expected_plus[r], "+"), (-1, expected_minus[r], "-")):
                if not mult:
                    continue
                ps = []
                for j in range(1, mult + 1):
                    ordj, swj = moments_by_j[j]
                    plus, minus = block_moments(ordj, swj, polys, dims)
                    ps.append(F((plus if eps == 1 else minus)[r]))
                elementary = newton(ps)
                if any(x < 0 for x in elementary):
                    raise AssertionError(("negative characteristic coefficient", alpha, r, label, ps, elementary))
                ray_cert["blocks"].append({
                    "r": r,
                    "swap": label,
                    "multiplicity": mult,
                    "power_sums": [str(x) for x in ps],
                    "elementary_symmetric": [str(x) for x in elementary],
                    "psd_certificate": "all exact elementary symmetric coefficients are nonnegative; the block is Hermitian, so its real eigenvalues cannot include a negative one",
                })
        all_blocks.append(ray_cert)
        print(f"certified ray {alpha}: {len(ray_cert['blocks'])} swap blocks", flush=True)

    dims_even = sum(dims[r] * expected_plus[r] for r in range(5))
    dims_odd = sum(dims[r] * expected_minus[r] for r in range(5))
    out = {
        "method": "independent full 12-qubit Pauli-word algebra; quadratic Casimir projectors; output-swap trace functional; Newton characteristic coefficients",
        "exact_prechecks": {
            "clifford_anticommutators_checked": 36,
            "distinct_grade_0_to_4_pauli_words": 256,
            "grade_star_hilbert_schmidt_gram": "Tr(H_k H_l)=4096*2*binom(9,k)*delta_kl",
            "output_swap_invariance_checked_for_grades": [1, 2, 3, 4],
            "casimir_centrality_checks": 36,
            "casimir_minimal_polynomial_exact": True,
            "star_spin9_invariance_checks": 144,
        },
        "normalization": {
            "full_tensor_dimension": DIM,
            "trace_coefficients_grade_1_to_4": [9, 36, 84, 126],
            "spin9_casimir_eigenvalues": cas,
            "casimir4_eigenvalues": mu,
            "irreducible_dimensions_from_B4_weyl_formula": dims,
            "swap_even_dimension": dims_even,
            "swap_odd_dimension": dims_odd,
            "dimension_sum": dims_even + dims_odd,
        },
        "support_cones": [[list(v) for v in cone] for cone in cones],
        "union_rays": [list(v) for v in rays],
        "word_support_sizes": max_support,
        "ray_block_certificates": all_blocks,
        "block_certificates_checked": sum(len(x["blocks"]) for x in all_blocks),
        "arithmetic": "integer and rational exact; all intermediate Hermitian Pauli coefficients checked real",
    }
    dest = Path(__file__).with_name("PAULI_TRACE_CERTIFICATE.json")
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "status": "INDEPENDENT_EXACT_PAULI_TRACE_AUDIT_PASS",
        "full_dimension": DIM,
        "spin9_casimir": cas,
        "irreducible_dimensions": dims,
        "swap_even": dims_even,
        "swap_odd": dims_odd,
        "rays": len(rays),
        "blocks_checked": sum(len(x["blocks"]) for x in all_blocks),
        "exact_prechecks": out["exact_prechecks"],
        "word_support_sizes": max_support,
        "certificate": str(dest),
    }, indent=2))


if __name__ == "__main__":
    main()
