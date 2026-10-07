"""Acquired finite-frontier hard-BCS norm transfer for rational-complex F.

Bandwidth b=max{|i-j| : i!=j and F[i,j]!=0} is acquired directly.
All coefficients: O(n^2 (b+1) 16^(b+1)) exact field operations.
This is an exact admitted-width algorithm, not a general-rank FPRAS.
"""
from low_rank_parity import G, Q, cast, choose_rational
import secrets


def create(bits, mode):
    if bits >> mode & 1:
        return None
    return bits | (1 << mode), (-1) ** ((bits & ((1 << mode) - 1)).bit_count())


def pair_create(bits, up_mode, down_mode):
    # a_up^dagger b_down^dagger acts right to left.
    first = create(bits, down_mode)
    if first is None:
        return None
    second = create(first[0], up_mode)
    if second is None:
        return None
    return second[0], first[1] * second[1]


def gate(D, up_mode, down_mode, amplitude):
    """D -> (1+f K) D (1+f K)^*, K=a_up^dagger b_down^dagger."""
    N = {}

    def add(key, val):
        if val:
            N[key] = N.get(key, G()) + val

    for (ket, bra, k), val in D.items():
        left = pair_create(ket, up_mode, down_mode)
        right = pair_create(bra, up_mode, down_mode)
        add((ket, bra, k), val)
        if left is not None:
            add((left[0], bra, k), val * amplitude * left[1])
        if right is not None:
            add((ket, right[0], k), val * amplitude.conj() * right[1])
        if left is not None and right is not None:
            add((left[0], right[0], k), val * amplitude.norm() * left[1] * right[1])
    return {key: val for key, val in N.items() if val}


def trace_front(D, table, row_weight, col_weight, cap):
    """Trace the first physical site with its hard projection and activity."""
    N = {}
    for (ket, bra, k), val in D.items():
        occupation = ket & 3
        if occupation != bra & 3 or occupation == 3:
            continue
        letter = 'ERC'[occupation]
        if letter not in table:
            continue
        kk = k + int(occupation == 1)
        if kk > cap:
            continue
        weight = Q(1) if occupation == 0 else row_weight if occupation == 1 else col_weight
        key = (ket >> 2, bra >> 2, kk)
        N[key] = N.get(key, G()) + val * weight
    return {key: val for key, val in N.items() if val}


def validate(F, allowed, row_weights, col_weights):
    n = len(F)
    if any(len(row) != n for row in F):
        raise ValueError('F must be square')
    F = [[cast(v) for v in row] for row in F]
    tables = [set('ERC') for _ in range(n)] if allowed is None else [set(t) for t in allowed]
    if len(tables) != n or any(not t <= set('ERC') for t in tables):
        raise ValueError('bad site table')
    rw = [Q(1)] * n if row_weights is None else [Q(v) for v in row_weights]
    cw = [Q(1)] * n if col_weights is None else [Q(v) for v in col_weights]
    if len(rw) != n or len(cw) != n or any(v < 0 for v in rw + cw):
        raise ValueError('bad nonnegative activities')
    return F, tables, rw, cw


def count_band(F, allowed=None, row_weights=None, col_weights=None, max_pairs=None):
    """Return exact disjoint-minor coefficients and acquired-width metadata.

    Optional max_pairs discards only sectors above that number. Entries Fii are
    ignored because disjoint I,J never use them. Site order is the supplied order.
    """
    F, tables, rw, cw = validate(F, allowed, row_weights, col_weights)
    n = len(F)
    if max_pairs is not None and (not isinstance(max_pairs, int) or max_pairs < 0):
        raise ValueError('bad sector cap')
    cap = n // 2 if max_pairs is None else min(max_pairs, n // 2)
    b = max((abs(i-j) for i in range(n) for j in range(n) if i != j and F[i][j]), default=0)
    D = {(0, 0, 0): G(1)}
    max_states = 1
    gate_count = 0
    for a in range(n):
        # Each off-diagonal pair is applied exactly once, before its leftmost
        # physical site is traced. The next unseen rightmost site starts vacuum.
        for j in range(a+1, min(n, a+b+1)):
            if F[a][j]:
                D = gate(D, 0, 2*(j-a)+1, F[a][j])
                gate_count += 1
                max_states = max(max_states, len(D))
            if F[j][a]:
                D = gate(D, 2*(j-a), 1, F[j][a])
                gate_count += 1
                max_states = max(max_states, len(D))
        D = trace_front(D, tables[a], rw[a], cw[a], cap)
        max_states = max(max_states, len(D))
    coefficients = [Q(0)] * (cap+1)
    for (ket, bra, k), val in D.items():
        assert ket == bra == 0
        assert not val.im and val.re >= 0
        coefficients[k] += val.re
    return coefficients, {'bandwidth_acquired': b, 'frontier_sites': min(n, b+1),
                          'max_density_entries': max_states, 'pair_gates': gate_count,
                          'sector_cap': cap}


def sample_band(F, k=None, allowed=None, row_weights=None, col_weights=None,
                randbits=secrets.randbits):
    """Exact canonical/grandcanonical law by acquired branch masses.

    Recomputes the small-width transfer for each prefix choice. No rare-sector
    rejection or externally supplied coefficient oracle is used.
    """
    F, tables, rw, cw = validate(F, allowed, row_weights, col_weights)
    n = len(F)
    if k is not None and (not isinstance(k, int) or k < 0 or k > n//2):
        raise ValueError('invalid sector')

    def mass():
        coefficients, _ = count_band(F, tables, rw, cw, k)
        return sum(coefficients) if k is None else coefficients[k]

    total = mass()
    if not total:
        raise ValueError('zero sector')
    out = []
    for i in range(n):
        choices = [t for t in 'ERC' if t in tables[i]]
        weights = []
        for t in choices:
            tables[i] = {t}
            weights.append(mass())
        assert sum(weights) == total
        selected = choose_rational(weights, randbits)
        tables[i] = {choices[selected]}
        out.append(choices[selected])
        total = weights[selected]
    return ''.join(out)
