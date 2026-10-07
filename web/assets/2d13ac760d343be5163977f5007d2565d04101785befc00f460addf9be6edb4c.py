"""Exact fermionic variable-elimination prototype for determinant-pair norms.

The full state space is exponential in induced width, not in the number of
sites.  Coefficients are Gaussian integers, represented as (real, imag).
This prototype accepts an elimination order; callers can supply an order from
a tree decomposition.  It is intended for exact small-instance verification.
"""
from __future__ import annotations

from itertools import combinations, permutations, product
from math import lcm
from random import Random
from fractions import Fraction
from typing import Dict, Iterable, List, Sequence, Tuple

GI = Tuple[int, int]
ZPOLY = List[GI]  # coefficient of z^d at index d
EPOLY = Dict[int, ZPOLY]  # exterior monomial bitmask -> z polynomial


def gadd(a: GI, b: GI) -> GI:
    return a[0] + b[0], a[1] + b[1]


def gmul(a: GI, b: GI) -> GI:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def gconj(a: GI) -> GI:
    return a[0], -a[1]


def gdiv(a: GI, b: GI) -> GI:
    den = b[0] * b[0] + b[1] * b[1]
    if den == 0:
        raise ZeroDivisionError
    num = gmul(a, gconj(b))
    return Fraction(num[0], den), Fraction(num[1], den)


ONE: GI = (1, 0)
ZERO: GI = (0, 0)


def ptrim(p: ZPOLY) -> ZPOLY:
    while len(p) > 1 and p[-1] == ZERO:
        p.pop()
    return p


def padd(a: ZPOLY, b: ZPOLY) -> ZPOLY:
    out = [ZERO] * max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] = gadd(out[i], x)
    for i, x in enumerate(b):
        out[i] = gadd(out[i], x)
    return ptrim(out)


def pmul(a: ZPOLY, b: ZPOLY) -> ZPOLY:
    out = [ZERO] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = gadd(out[i + j], gmul(x, y))
    return ptrim(out)


def pshift(a: ZPOLY, shift: int) -> ZPOLY:
    if shift == 0:
        return list(a)
    return [ZERO] * shift + list(a)


def ext_sign(mask_a: int, mask_b: int) -> int:
    """Sign for canonical exterior monomials A wedge B."""
    inversions = 0
    bits = mask_a
    while bits:
        low = bits & -bits
        idx = low.bit_length() - 1
        inversions += (mask_b & ((1 << idx) - 1)).bit_count()
        bits ^= low
    return -1 if inversions & 1 else 1


def epadd(a: EPOLY, b: EPOLY) -> EPOLY:
    out = {m: list(p) for m, p in a.items()}
    for m, p in b.items():
        out[m] = padd(out[m], p) if m in out else list(p)
    return {m: p for m, p in out.items() if any(x != ZERO for x in p)}


def epmul(a: EPOLY, b: EPOLY) -> EPOLY:
    out: EPOLY = {}
    for ma, pa in a.items():
        for mb, pb in b.items():
            if ma & mb:
                continue
            p = pmul(pa, pb)
            if ext_sign(ma, mb) < 0:
                p = [(-x[0], -x[1]) for x in p]
            out[ma | mb] = padd(out[ma | mb], p) if (ma | mb) in out else p
    return {m: p for m, p in out.items() if any(x != ZERO for x in p)}


def monomial(mask_vars: Sequence[int], coeff: GI = ONE) -> EPOLY:
    mask = 0
    inversions = 0
    for i, a in enumerate(mask_vars):
        for b in mask_vars[i + 1 :]:
            if a > b:
                inversions += 1
        mask |= 1 << a
    if inversions & 1:
        coeff = (-coeff[0], -coeff[1])
    return {mask: [coeff]}


def edge_factor(i: int, j: int, value: GI) -> EPOLY:
    # Modes at site i are x_i,y_i,u_i,v_i.  The two even bilinears encode
    # one determinant amplitude and its conjugate.
    f1 = epadd({0: [ONE]}, monomial([4 * i, 4 * j + 1], value))
    f2 = epadd({0: [ONE]}, monomial([4 * i + 2, 4 * j + 3], gconj(value)))
    return epmul(f1, f2)


def local_empty_factor(site: int) -> EPOLY:
    return {0: [ONE]}


def apply_site_pairing(poly: EPOLY, site: int, allowed: Iterable[str] = ("empty", "row", "col")) -> EPOLY:
    """Apply L_i: identify replica occupations and forbid row+column."""
    row_local = (1 << (4 * site)) | (1 << (4 * site + 2))
    col_local = (1 << (4 * site + 1)) | (1 << (4 * site + 3))
    local_mask = 0b1111 << (4 * site)
    allowed = set(allowed)
    local_states = {0: "empty", row_local: "row", col_local: "col"}
    out: EPOLY = {}
    for mask, p in poly.items():
        local = mask & local_mask
        if local not in local_states or local_states[local] not in allowed:
            continue
        reduced = mask ^ local
        if local == row_local:
            # The replica contraction crosses one y/u pair per selected row;
            # this Koszul sign cancels the determinant convention's global
            # (-1)^k factor in the product of amplitude and conjugate.
            q = [(-x[0], -x[1]) for x in pshift(p, 1)]
        else:
            q = p
        out[reduced] = padd(out[reduced], q) if reduced in out else q
    return {m: p for m, p in out.items() if any(x != ZERO for x in p)}


def exact_elimination(F: Sequence[Sequence[GI]], order: Sequence[int],
                      domains: Dict[int, Iterable[str]] | None = None) -> List[GI]:
    """Return [c_0,...,c_n] for integer Gaussian-rational F."""
    n = len(F)
    factors: List[Tuple[frozenset[int], EPOLY]] = []
    for i in range(n):
        factors.append((frozenset((i,)), local_empty_factor(i)))
    for i in range(n):
        for j in range(n):
            if F[i][j] != ZERO:
                factors.append((frozenset((i, j)), edge_factor(i, j, F[i][j])))

    for site in order:
        touched = [(scope, p) for scope, p in factors if site in scope]
        factors = [(scope, p) for scope, p in factors if site not in scope]
        union_scope: set[int] = set()
        merged: EPOLY = {0: [ONE]}
        for scope, p in touched:
            union_scope.update(scope)
            merged = epmul(merged, p)
        msg = apply_site_pairing(merged, site,
                                 ("empty", "row", "col") if domains is None else domains.get(site, ("empty", "row", "col")))
        factors.append((frozenset(union_scope - {site}), msg))

    final: EPOLY = {0: [ONE]}
    for scope, p in factors:
        if scope:
            raise ValueError("elimination order did not eliminate every site")
        final = epmul(final, p)
    coeffs = final.get(0, [ZERO])
    return coeffs + [ZERO] * (n + 1 - len(coeffs))


def det_perm(A: Sequence[Sequence[GI]]) -> GI:
    n = len(A)
    if n == 0:
        return ONE
    total = ZERO
    for perm in permutations(range(n)):
        inv = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = ONE
        for i, j in enumerate(perm):
            term = gmul(term, A[i][j])
        total = gadd(total, (-term[0], -term[1]) if inv & 1 else term)
    return total


def direct_coefficients(F: Sequence[Sequence[GI]]) -> List[int]:
    n = len(F)
    out = [0] * (n + 1)
    ids = range(n)
    for k in range(n + 1):
        for I in combinations(ids, k):
            for J in combinations(ids, k):
                if set(I) & set(J):
                    continue
                d = det_perm([[F[i][j] for j in J] for i in I])
                out[k] += d[0] * d[0] + d[1] * d[1]
    return out


def direct_branch_masses(F: Sequence[Sequence[GI]], k: int,
                         prefix: Sequence[str]) -> Tuple[GI, GI, GI]:
    names = ("empty", "row", "col")
    masses = [ZERO, ZERO, ZERO]
    n = len(F)
    for config in product(names, repeat=n):
        if config[:len(prefix)] != tuple(prefix):
            continue
        I = [i for i, x in enumerate(config) if x == "row"]
        J = [i for i, x in enumerate(config) if x == "col"]
        if len(I) != k or len(J) != k:
            continue
        d = det_perm([[F[i][j] for j in J] for i in I])
        weight_real = d[0] * d[0] + d[1] * d[1]
        branch = names.index(config[len(prefix)]) if len(prefix) < n else 0
        masses[branch] = gadd(masses[branch], (weight_real, 0))
    return tuple(masses)  # type: ignore[return-value]


def wedge_sign(mask: int, coordinate: int) -> int:
    # e_mask wedge e_coordinate, reordered into increasing basis order.
    higher = mask >> (coordinate + 1)
    return -1 if higher.bit_count() & 1 else 1


def rank_transfer(A: Sequence[Sequence[GI]], B: Sequence[Sequence[GI]]) -> List[int]:
    """FPT-in-rank transfer for F=A B; state is four exterior powers."""
    n, r = len(A), len(A[0]) if A else len(B)
    if len(B) != r or any(len(row) != r for row in A) or any(len(row) != n for row in B):
        raise ValueError("incompatible rank factorization")
    # (S_A, S_B, T_A, T_B) -> exact Gaussian-integer coefficient.
    state: Dict[Tuple[int, int, int, int], GI] = {(0, 0, 0, 0): ONE}
    for i in range(n):
        nxt = dict(state)  # site i is empty
        for (sa, sb, ta, tb), coeff in state.items():
            # Occupy site i on the row/up side, simultaneously in the bra.
            for p in range(r):
                if sa >> p & 1:
                    continue
                sp = wedge_sign(sa, p)
                for q in range(r):
                    if ta >> q & 1:
                        continue
                    factor = gmul(A[i][p], gconj(A[i][q]))
                    if factor == ZERO:
                        continue
                    factor = (factor[0] * sp * wedge_sign(ta, q),
                              factor[1] * sp * wedge_sign(ta, q))
                    key = (sa | (1 << p), sb, ta | (1 << q), tb)
                    term = gmul(coeff, factor)
                    nxt[key] = gadd(nxt.get(key, ZERO), term)
            # Occupy site i on the column/down side, simultaneously in bra.
            for p in range(r):
                if sb >> p & 1:
                    continue
                sp = wedge_sign(sb, p)
                for q in range(r):
                    if tb >> q & 1:
                        continue
                    factor = gmul(B[p][i], gconj(B[q][i]))
                    if factor == ZERO:
                        continue
                    factor = (factor[0] * sp * wedge_sign(tb, q),
                              factor[1] * sp * wedge_sign(tb, q))
                    key = (sa, sb | (1 << p), ta, tb | (1 << q))
                    term = gmul(coeff, factor)
                    nxt[key] = gadd(nxt.get(key, ZERO), term)
        state = {key: value for key, value in nxt.items() if value != ZERO}
    out = [ZERO] * (r + 1)
    for (sa, sb, ta, tb), value in state.items():
        k = sa.bit_count()
        if sa == sb and ta == tb and k == ta.bit_count() and k <= r:
            out[k] = gadd(out[k], value)
    if any(value[1] != 0 for value in out):
        raise AssertionError(("nonreal final partition", out))
    return [value[0] for value in out]


def rank_transfer_sector(A: Sequence[Sequence[GI]], B: Sequence[Sequence[GI]],
                         k: int) -> GI:
    """Compute one coefficient, pruning exterior degrees above k."""
    n, r = len(A), len(A[0]) if A else len(B)
    state: Dict[Tuple[int, int, int, int], GI] = {(0, 0, 0, 0): ONE}
    for i in range(n):
        a = A[i]
        b = [B[s][i] for s in range(r)]
        nxt = dict(state)
        for branch in ("row", "col"):
            part = rank_forward_branch(state, a, b, branch, max_degree=k)
            for key, value in part.items():
                nxt[key] = gadd(nxt.get(key, ZERO), value)
        state = {key: value for key, value in nxt.items()
                 if value != ZERO and key[0].bit_count() <= k and key[1].bit_count() <= k}
    total = sum_gaussian(value for (sa, sb, ta, tb), value in state.items()
                         if sa == sb and ta == tb and sa.bit_count() == k
                         and ta.bit_count() == k)
    if total[1] != 0:
        raise AssertionError(("nonreal sector", k, total))
    return total


def rank_forward_branch(state: Dict[Tuple[int, int, int, int], GI],
                        a: Sequence[GI], b: Sequence[GI], branch: str,
                        max_degree: int | None = None) -> Dict[Tuple[int, int, int, int], GI]:
    """Apply one local occupancy branch: empty, row, or col."""
    if branch == "empty":
        out = dict(state)
        if max_degree is not None:
            out = {key: value for key, value in out.items()
                   if key[0].bit_count() <= max_degree and key[1].bit_count() <= max_degree}
        return out
    r = len(a)
    out: Dict[Tuple[int, int, int, int], GI] = {}
    for (sa, sb, ta, tb), coeff in state.items():
        if branch == "row":
            for p in range(r):
                if sa >> p & 1:
                    continue
                sp = wedge_sign(sa, p)
                for q in range(r):
                    if ta >> q & 1:
                        continue
                    factor = gmul(a[p], gconj(a[q]))
                    factor = (factor[0] * sp * wedge_sign(ta, q),
                              factor[1] * sp * wedge_sign(ta, q))
                    key = (sa | (1 << p), sb, ta | (1 << q), tb)
                    out[key] = gadd(out.get(key, ZERO), gmul(coeff, factor))
        elif branch == "col":
            for p in range(r):
                if sb >> p & 1:
                    continue
                sp = wedge_sign(sb, p)
                for q in range(r):
                    if tb >> q & 1:
                        continue
                    factor = gmul(b[p], gconj(b[q]))
                    factor = (factor[0] * sp * wedge_sign(tb, q),
                              factor[1] * sp * wedge_sign(tb, q))
                    key = (sa, sb | (1 << p), ta, tb | (1 << q))
                    out[key] = gadd(out.get(key, ZERO), gmul(coeff, factor))
        else:
            raise ValueError("branch must be empty, row, or col")
    return {key: value for key, value in out.items()
            if value != ZERO and (max_degree is None or
                                  (key[0].bit_count() <= max_degree and
                                   key[1].bit_count() <= max_degree))}


def rank_cov_branch(cov: Dict[Tuple[int, int, int, int], GI],
                    a: Sequence[GI], b: Sequence[GI], branch: str) -> Dict[Tuple[int, int, int, int], GI]:
    """Apply the transpose of one local branch to a final contraction covector."""
    if branch == "empty":
        return dict(cov)
    out: Dict[Tuple[int, int, int, int], GI] = {}
    for (sa, sb, ta, tb), coeff in cov.items():
        if branch == "row":
            ps = [p for p in range(len(a)) if sa >> p & 1]
            qs = [q for q in range(len(a)) if ta >> q & 1]
            for p in ps:
                pred_a = sa ^ (1 << p)
                sp = wedge_sign(pred_a, p)
                for q in qs:
                    pred_t = ta ^ (1 << q)
                    factor = gmul(a[p], gconj(a[q]))
                    sign = sp * wedge_sign(pred_t, q)
                    factor = (factor[0] * sign, factor[1] * sign)
                    key = (pred_a, sb, pred_t, tb)
                    out[key] = gadd(out.get(key, ZERO), gmul(coeff, factor))
        elif branch == "col":
            ps = [p for p in range(len(b)) if sb >> p & 1]
            qs = [q for q in range(len(b)) if tb >> q & 1]
            for p in ps:
                pred_b = sb ^ (1 << p)
                sp = wedge_sign(pred_b, p)
                for q in qs:
                    pred_t = tb ^ (1 << q)
                    factor = gmul(b[p], gconj(b[q]))
                    sign = sp * wedge_sign(pred_t, q)
                    factor = (factor[0] * sign, factor[1] * sign)
                    key = (sa, pred_b, ta, pred_t)
                    out[key] = gadd(out.get(key, ZERO), gmul(coeff, factor))
        else:
            raise ValueError("branch must be empty, row, or col")
    return {key: value for key, value in out.items() if value != ZERO}


def rank_dot(cov: Dict[Tuple[int, int, int, int], GI],
             state: Dict[Tuple[int, int, int, int], GI]) -> GI:
    return sum_gaussian(gmul(value, state.get(key, ZERO)) for key, value in cov.items())


def rank_suffix_covectors(A: Sequence[Sequence[GI]], B: Sequence[Sequence[GI]],
                          k: int) -> List[Dict[Tuple[int, int, int, int], GI]]:
    """Backward messages for the exact k-sector terminal contraction."""
    n, r = len(A), len(A[0]) if A else len(B)
    terminal: Dict[Tuple[int, int, int, int], GI] = {}
    for sa in range(1 << r):
        if sa.bit_count() != k:
            continue
        for ta in range(1 << r):
            if ta.bit_count() == k:
                terminal[(sa, sa, ta, ta)] = ONE
    suffix: List[Dict[Tuple[int, int, int, int], GI]] = [dict() for _ in range(n + 1)]
    suffix[n] = terminal
    for i in range(n - 1, -1, -1):
        a = A[i]
        b = [B[s][i] for s in range(r)]
        current = rank_cov_branch(suffix[i + 1], a, b, "empty")
        for branch in ("row", "col"):
            part = rank_cov_branch(suffix[i + 1], a, b, branch)
            for key, value in part.items():
                current[key] = gadd(current.get(key, ZERO), value)
        suffix[i] = {key: value for key, value in current.items() if value != ZERO}
    return suffix


def rank_prefix_state(A: Sequence[Sequence[GI]], B: Sequence[Sequence[GI]],
                      prefix: Sequence[str], max_degree: int | None = None) -> Dict[Tuple[int, int, int, int], GI]:
    """Forward message after a fixed local occupancy prefix."""
    r = len(A[0]) if A else len(B)
    forward: Dict[Tuple[int, int, int, int], GI] = {(0, 0, 0, 0): ONE}
    for i, branch in enumerate(prefix):
        a = A[i]
        b = [B[s][i] for s in range(r)]
        forward = rank_forward_branch(forward, a, b, branch, max_degree=max_degree)
    return forward


def rank_prefix_branch_masses(A: Sequence[Sequence[GI]], B: Sequence[Sequence[GI]],
                              k: int, prefix: Sequence[str]) -> Tuple[GI, GI, GI]:
    """Exact completion masses for the three next-site choices."""
    i = len(prefix)
    if i >= len(A):
        raise ValueError("prefix already covers every site")
    r = len(A[0]) if A else len(B)
    forward = rank_prefix_state(A, B, prefix, max_degree=k)
    suffix = rank_suffix_covectors(A, B, k)[i + 1]
    a = A[i]
    b = [B[s][i] for s in range(r)]
    return tuple(rank_dot(suffix, rank_forward_branch(forward, a, b, branch, max_degree=k))
                 for branch in ("empty", "row", "col"))  # type: ignore[return-value]


def rank_sample(A: Sequence[Sequence[GI]], B: Sequence[Sequence[GI]], k: int,
                rng: Random | None = None) -> Tuple[List[str], List[Tuple[GI, GI, GI]]]:
    """Exact sequential sample and conditional masses using suffix covectors."""
    rng = rng or Random()
    n, r = len(A), len(A[0]) if A else len(B)
    suffix = rank_suffix_covectors(A, B, k)
    terminal = suffix[n]

    forward: Dict[Tuple[int, int, int, int], GI] = {(0, 0, 0, 0): ONE}
    result: List[Tuple[GI, GI, GI]] = []
    path: List[str] = []
    branch_names = ("empty", "row", "col")
    for i in range(n):
        a = A[i]
        b = [B[s][i] for s in range(r)]
        branch_vectors = [rank_forward_branch(forward, a, b, branch, max_degree=k)
                          for branch in branch_names]
        masses = tuple(rank_dot(suffix[i + 1], vec) for vec in branch_vectors)
        if any(m[1] != 0 or m[0] < 0 for m in masses):
            raise AssertionError(("invalid conditional mass", i, masses))
        if sum(m[0] for m in masses) != rank_dot(suffix[i], forward)[0]:
            raise AssertionError(("branch masses fail to partition", i, masses))
        result.append(masses)
        den = 1
        for mass in masses:
            den = lcm(den, Fraction(mass[0]).denominator)
        weights = [int(Fraction(mass[0]) * den) for mass in masses]
        total = sum(weights)
        if total <= 0:
            raise ValueError("requested canonical sector is zero")
        draw = rng.randrange(total)
        chosen = 0
        for j, weight in enumerate(weights):
            if draw < weight:
                chosen = j
                break
            draw -= weight
        path.append(branch_names[chosen])
        forward = branch_vectors[chosen]
    final_mass = rank_dot(terminal, forward)
    if final_mass[1] != 0 or final_mass[0] <= 0:
        raise AssertionError(("sampled path has invalid final weight", final_mass))
    return path, result


def checks() -> dict:
    rng = Random(271828)
    cases = 0
    for n in range(1, 6):
        # The identity order has small induced width on the path-supported
        # cases below; arbitrary complex entries also check conjugation signs.
        for trial in range(8):
            F = []
            for i in range(n):
                row = []
                for j in range(n):
                    if abs(i - j) <= 1 or trial % 3 == 0:
                        row.append((rng.randrange(-1, 2), rng.randrange(-1, 2)))
                    else:
                        row.append(ZERO)
                F.append(row)
            got = exact_elimination(F, list(range(n)))
            want = direct_coefficients(F)
            got_int = [a if b == 0 else None for a, b in got]
            assert got_int == want, (n, trial, got_int, want)
            cases += 1
    # Forced/excluded prefix partitions add exactly, so the same DP supplies
    # the conditional masses needed for exact sequential sampling.
    F = [[(0, 0), (2, -1), (0, 0), (0, 0)],
         [(0, 0), (0, 0), (1, 1), (0, 0)],
         [(0, 0), (0, 0), (0, 0), (1, 0)],
         [(0, 0), (0, 0), (0, 0), (0, 0)]]
    base = exact_elimination(F, list(range(4)))
    for site in range(4):
        parts = []
        for state in ("empty", "row", "col"):
            constrained = exact_elimination(F, list(range(4)), {site: (state,)})
            parts.append(constrained)
        for degree in range(5):
            assert sum(p[degree][0] if degree < len(p) else 0 for p in parts) == base[degree][0]
            assert sum(p[degree][1] if degree < len(p) else 0 for p in parts) == base[degree][1]
    # Rank-only algorithm test: dense matrices F=A B with rank at most r.
    rank_cases = 0
    for n, r in ((3, 1), (4, 2), (5, 2), (5, 3)):
        for _ in range(6):
            A = [[(rng.randrange(-1, 2), rng.randrange(-1, 2)) for _ in range(r)] for _ in range(n)]
            B = [[(rng.randrange(-1, 2), rng.randrange(-1, 2)) for _ in range(n)] for _ in range(r)]
            F = [[sum_gaussian(gmul(A[i][s], B[s][j]) for s in range(r)) for j in range(n)] for i in range(n)]
            got = rank_transfer(A, B)
            want = direct_coefficients(F)[:r + 1]
            assert got == want, (n, r, got, want)
            A2, B2 = rank_factorization(F)
            got2 = rank_transfer(A2, B2)
            assert got2 == direct_coefficients(F)[:len(A2[0]) + 1], (n, r, got2, A2, B2)
            for k, total in enumerate(direct_coefficients(F)[:len(A2[0]) + 1]):
                sector = rank_transfer_sector(A2, B2, k)
                assert sector == (total, 0), (n, r, k, sector, total)
                if total <= 0:
                    continue
                path, branch_masses = rank_sample(A2, B2, k, rng)
                for i, masses in enumerate(branch_masses):
                    exact = direct_branch_masses(F, k, path[:i])
                    assert masses == exact, (n, r, k, path, i, masses, exact)
                # Audit every possible short prefix, including prefixes that a
                # single random path would not visit.
                if n <= 4:
                    for depth in range(n):
                        for prefix in product(("empty", "row", "col"), repeat=depth):
                            exact = direct_branch_masses(F, k, prefix)
                            got_prefix = rank_prefix_branch_masses(A2, B2, k, prefix)
                            assert got_prefix == exact, (n, r, k, prefix, got_prefix, exact)
            rank_cases += 1
    # Rational-complex full-rank acquisition also exercises division and
    # denominator growth rather than only integer factors.
    rational_cases = 0
    for n in (2, 3):
        for _ in range(4):
            F = [[(Fraction(rng.randrange(-2, 3), rng.randrange(1, 4)),
                   Fraction(rng.randrange(-2, 3), rng.randrange(1, 4))) for _ in range(n)] for _ in range(n)]
            A, B = rank_factorization(F)
            got = rank_transfer(A, B)
            want = direct_coefficients(F)[:len(A[0]) + 1]
            assert got == want, (n, got, want)
            for k, total in enumerate(want):
                assert rank_transfer_sector(A, B, k) == (total, 0), (n, k, total)
            rational_cases += 1
    return {"status": "PASS", "exact_cases": cases, "rank_cases": rank_cases,
            "rational_factorization_cases": rational_cases,
            "max_n": 5, "max_rank": 3,
            "checks": "treewidth DP equals direct determinants; all-coefficient and k-pruned rank transfers plus every n<=4 prefix mass equal direct determinants; constrained sectors add"}


def sum_gaussian(values: Iterable[GI]) -> GI:
    total = ZERO
    for value in values:
        total = gadd(total, value)
    return total


def matrix_rank_pivots(matrix: Sequence[Sequence[GI]]) -> List[int]:
    """Exact row-rank pivot columns over Q(i), returning original column ids."""
    if not matrix:
        return []
    work = [[(Fraction(x[0]), Fraction(x[1])) for x in row] for row in matrix]
    m, n = len(work), len(work[0])
    pivot_cols: List[int] = []
    row = 0
    for col in range(n):
        pivot = next((i for i in range(row, m) if work[i][col] != ZERO), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        p = work[row][col]
        work[row] = [gdiv(x, p) for x in work[row]]
        for i in range(row + 1, m):
            q = work[i][col]
            if q != ZERO:
                work[i] = [gadd(x, (-y[0], -y[1])) for x, y in zip(work[i], [gmul(q, z) for z in work[row]])]
        pivot_cols.append(col)
        row += 1
        if row == m:
            break
    return pivot_cols


def matrix_inverse(matrix: Sequence[Sequence[GI]]) -> List[List[GI]]:
    n = len(matrix)
    aug = [[(Fraction(x[0]), Fraction(x[1])) for x in row] +
           [(ONE if i == j else ZERO) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if aug[i][col] != ZERO), None)
        if pivot is None:
            raise ValueError("singular pivot minor")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        p = aug[col][col]
        aug[col] = [gdiv(x, p) for x in aug[col]]
        for i in range(n):
            if i == col:
                continue
            q = aug[i][col]
            if q != ZERO:
                aug[i] = [gadd(x, (-y[0], -y[1])) for x, y in zip(aug[i], [gmul(q, z) for z in aug[col]])]
    return [row[n:] for row in aug]


def rank_factorization(F: Sequence[Sequence[GI]]) -> Tuple[List[List[GI]], List[List[GI]]]:
    """Acquire F=A B exactly over Q(i) using pivot rows and columns."""
    n = len(F)
    if any(len(row) != n for row in F):
        raise ValueError("F must be square")
    col_ids = matrix_rank_pivots(F)
    r = len(col_ids)
    A = [[F[i][j] for j in col_ids] for i in range(n)]
    if r == 0:
        return A, []
    row_ids = matrix_rank_pivots([list(row) for row in zip(*A)])
    pivot = [[A[i][j] for j in range(r)] for i in row_ids]
    inv = matrix_inverse(pivot)
    B = [[sum_gaussian(gmul(inv[i][s], F[row_ids[s]][j]) for s in range(r))
          for j in range(n)] for i in range(r)]
    reconstructed = [[sum_gaussian(gmul(A[i][s], B[s][j]) for s in range(r))
                      for j in range(n)] for i in range(n)]
    if reconstructed != [[(Fraction(x[0]), Fraction(x[1])) for x in row] for row in F]:
        raise AssertionError("rank factorization did not reconstruct input")
    return A, B


if __name__ == "__main__":
    import json
    print(json.dumps(checks(), indent=2))
