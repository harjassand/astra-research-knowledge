"""Exact bounded-treewidth counter for onsite-filtered determinant-pair norms.

Input entries and onsite weights are exact rationals (complex entries are
represented by a pair of Fractions). Four Grassmann generators live at each
site. Eliminating sites in a supplied order contracts the pair-norm tensor
network without constructing the full Fock-space vector.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations
from math import lcm
import random
from typing import Dict, Iterable, List, Sequence, Tuple

QC = Tuple[Q, Q]
ZPOLY = List[QC]
EPOLY = Dict[int, ZPOLY]
ZERO: QC = (Q(0), Q(0))
ONE: QC = (Q(1), Q(0))
LOCAL_STATES = ("0", "u", "d", "ud")


def qc(a=0, b=0) -> QC:
    return Q(a), Q(b)


def qadd(a: QC, b: QC) -> QC:
    return a[0] + b[0], a[1] + b[1]


def qneg(a: QC) -> QC:
    return -a[0], -a[1]


def qmul(a: QC, b: QC) -> QC:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def qconj(a: QC) -> QC:
    return a[0], -a[1]


def ptrim(p: ZPOLY) -> ZPOLY:
    while len(p) > 1 and p[-1] == ZERO:
        p.pop()
    return p


def padd(a: ZPOLY, b: ZPOLY) -> ZPOLY:
    out = [ZERO] * max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] = qadd(out[i], x)
    for i, x in enumerate(b):
        out[i] = qadd(out[i], x)
    return ptrim(out)


def pmul(a: ZPOLY, b: ZPOLY) -> ZPOLY:
    out = [ZERO] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = qadd(out[i + j], qmul(x, y))
    return ptrim(out)


def pscale(a: ZPOLY, scale: QC) -> ZPOLY:
    return ptrim([qmul(scale, x) for x in a])


def pshift(a: ZPOLY, shift: int = 1) -> ZPOLY:
    return [ZERO] * shift + list(a)


def ext_sign(mask_a: int, mask_b: int) -> int:
    """Sign when canonical exterior monomial A is followed by B."""
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
            product = pmul(pa, pb)
            if ext_sign(ma, mb) < 0:
                product = [qneg(x) for x in product]
            key = ma | mb
            out[key] = padd(out[key], product) if key in out else product
    return {m: p for m, p in out.items() if any(x != ZERO for x in p)}


def monomial(vars_in_order: Sequence[int], coeff: QC = ONE) -> EPOLY:
    inversions = sum(
        vars_in_order[i] > vars_in_order[j]
        for i in range(len(vars_in_order))
        for j in range(i + 1, len(vars_in_order))
    )
    mask = 0
    for v in vars_in_order:
        mask |= 1 << v
    if inversions & 1:
        coeff = qneg(coeff)
    return {mask: [coeff]}


def edge_factor(i: int, j: int, value: QC) -> EPOLY:
    """(1+F_ij x_i y_j)(1+conj(F_ij) u_i v_j), including i=j."""
    f = epadd({0: [ONE]}, monomial([4 * i, 4 * j + 1], value))
    g = epadd({0: [ONE]}, monomial([4 * i + 2, 4 * j + 3], qconj(value)))
    return epmul(f, g)


def support_adjacency(F: Sequence[Sequence[QC]]) -> List[set[int]]:
    n = len(F)
    adj = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i):
            if F[i][j] != ZERO or F[j][i] != ZERO:
                adj[i].add(j)
                adj[j].add(i)
    return adj


def elimination_width(F: Sequence[Sequence[QC]], order: Sequence[int]) -> int:
    n = len(F)
    if sorted(order) != list(range(n)):
        raise ValueError("order must be a permutation of site indices")
    adj = support_adjacency(F)
    live = set(range(n))
    width = 0
    for v in order:
        neighbors = adj[v] & live
        width = max(width, len(neighbors))
        for a, b in combinations(neighbors, 2):
            adj[a].add(b)
            adj[b].add(a)
        live.remove(v)
    return width


def min_degree_order(F: Sequence[Sequence[QC]]) -> List[int]:
    """Deterministic heuristic; the returned width is reported, not promised."""
    adj = support_adjacency(F)
    live = set(range(len(F)))
    order: List[int] = []
    while live:
        v = min(live, key=lambda u: (len(adj[u] & live), u))
        neighbors = adj[v] & live
        for a, b in combinations(neighbors, 2):
            adj[a].add(b)
            adj[b].add(a)
        live.remove(v)
        order.append(v)
    return order


def contract_site(poly: EPOLY, site: int, allowed: Iterable[str], t: Q) -> EPOLY:
    """Apply ell_i(1)=1, ell_i(xu)=-z, ell_i(yv)=1, ell_i(xyuv)=zt."""
    allowed = set(allowed)
    invalid = allowed - set(LOCAL_STATES)
    if invalid:
        raise ValueError(f"invalid local state(s): {sorted(invalid)}")
    row = (1 << (4 * site)) | (1 << (4 * site + 2))
    col = (1 << (4 * site + 1)) | (1 << (4 * site + 3))
    full = 15 << (4 * site)
    local_mask = full
    out: EPOLY = {}
    for mask, p in poly.items():
        local = mask & local_mask
        if local == 0 and "0" in allowed:
            q = p
        elif local == row and "u" in allowed:
            q = [qneg(x) for x in pshift(p)]
        elif local == col and "d" in allowed:
            q = p
        elif local == full and "ud" in allowed and t:
            q = pshift(pscale(p, qc(t)))
        else:
            continue
        reduced = mask ^ local
        out[reduced] = padd(out[reduced], q) if reduced in out else q
    return {m: p for m, p in out.items() if any(x != ZERO for x in p)}


def counts(
    F: Sequence[Sequence[QC]],
    t: Sequence[Q],
    allowed: Sequence[Iterable[str]] | None = None,
    order: Sequence[int] | None = None,
) -> List[Q]:
    """Return exact c_0,...,c_n under onsite weights and local restrictions.

    c_k = sum_{|I|=|J|=k} |det F[I,J]|^2 prod_{i in I cap J} t_i,
    omitting terms whose per-site state is disallowed by ``allowed``.
    """
    n = len(F)
    if any(len(row) != n for row in F) or len(t) != n:
        raise ValueError("F must be square and t must have one entry per site")
    if any(x < 0 for x in t):
        raise ValueError("onsite squared weights must be nonnegative")
    if allowed is None:
        allowed = [LOCAL_STATES for _ in range(n)]
    if len(allowed) != n:
        raise ValueError("allowed must have one local state set per site")
    if order is None:
        order = min_degree_order(F)
    if sorted(order) != list(range(n)):
        raise ValueError("order must be a permutation of site indices")

    factors: List[Tuple[frozenset[int], EPOLY]] = []
    for i in range(n):
        for j in range(n):
            if F[i][j] != ZERO:
                factors.append((frozenset((i, j)), edge_factor(i, j, F[i][j])))

    for site in order:
        bucket = [(s, p) for s, p in factors if site in s]
        factors = [(s, p) for s, p in factors if site not in s]
        merged: EPOLY = {0: [ONE]}
        union_scope: set[int] = set()
        for scope, factor in sorted(bucket, key=lambda q: len(q[1])):
            union_scope.update(scope)
            merged = epmul(merged, factor)
        msg = contract_site(merged, site, allowed[site], Q(t[site]))
        union_scope.discard(site)
        factors.append((frozenset(union_scope), msg))

    final: EPOLY = {0: [ONE]}
    for scope, factor in factors:
        if scope:
            raise ValueError("order did not eliminate every site")
        final = epmul(final, factor)
    coeffs = final.get(0, [ZERO])
    out = [coeffs[k][0] if k < len(coeffs) else Q(0) for k in range(n + 1)]
    for k in range(n + 1):
        im = coeffs[k][1] if k < len(coeffs) else Q(0)
        if im or out[k] < 0:
            raise ArithmeticError("contraction failed the real nonnegative invariant")
    return out


def _randbelow(total: int, rng) -> int:
    if total <= 0:
        raise ValueError("total must be positive")
    bits = total.bit_length()
    while True:
        value = rng.getrandbits(bits)
        if value < total:
            return value


def _choose_rational(masses: Sequence[Q], rng) -> int:
    den = 1
    for mass in masses:
        den = lcm(den, mass.denominator)
    weights = [mass.numerator * (den // mass.denominator) for mass in masses]
    total = sum(weights)
    if total <= 0:
        raise ValueError("zero-mass conditional branch")
    ticket = _randbelow(total, rng)
    acc = 0
    for index, weight in enumerate(weights):
        acc += weight
        if ticket < acc:
            return index
    raise AssertionError("unreachable exact integer choice")


def sample_sector(
    F: Sequence[Sequence[QC]],
    t: Sequence[Q],
    k: int,
    allowed: Sequence[Iterable[str]] | None = None,
    order: Sequence[int] | None = None,
    rng=None,
) -> List[str]:
    """Exact random-bit self-reduction for a nonzero canonical sector."""
    n = len(F)
    if not 0 <= k <= n:
        raise ValueError("sector k must be in 0..n")
    if allowed is None:
        current = [set(LOCAL_STATES) for _ in range(n)]
    else:
        current = [set(a) for a in allowed]
    if rng is None:
        rng = random.SystemRandom()
    if order is None:
        order = min_degree_order(F)
    current_total = counts(F, t, current, order)[k]
    if not current_total:
        raise ValueError("requested sector has exact zero norm")
    selected = ["0"] * n
    for site in range(n):
        choices = [state for state in LOCAL_STATES if state in current[site]]
        masses = []
        for state in choices:
            restricted = list(current)
            restricted[site] = {state}
            masses.append(counts(F, t, restricted, order)[k])
        if sum(masses) != current_total:
            raise ArithmeticError("local completion masses do not partition total")
        chosen_index = _choose_rational(masses, rng)
        chosen = choices[chosen_index]
        selected[site] = chosen
        current[site] = {chosen}
        current_total = masses[chosen_index]
    return selected
