"""Independent exact checks; no producer code is imported or modified.

All outputs are local to this audit. Finite checks corroborate the separate
symbolic proof; they do not establish its universal quantifiers or novelty.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import time

HERE = Path(__file__).resolve().parent


def zeta(coeffs, n, modulus=None):
    vals = list(coeffs)
    for j in range(n):
        bit = 1 << j
        for x in range(1 << n):
            if x & bit:
                vals[x] += vals[x ^ bit]
                if modulus:
                    vals[x] %= modulus
    return vals


def beta(s):
    return 1 << (s.bit_length() - 1)


def rho_sum(T, minimum_only):
    R = [a for a in T if not any(b != a and b & a == b for b in T)] if minimum_only else T
    return sum(min(beta(sum(a & b == a for b in T)),
                   1 << max((b ^ a).bit_count() for b in T if a & b == a))
               for a in R)


def E(m):
    return max((1 << j) * (m + 1 - (1 << j)) for j in range(m.bit_length()))


def D(m):
    return sum(beta(j) for j in range(1, m + 1))


def or_case(b, copies=1):
    n = 2 * b * copies
    base = []
    for mask in range(1, 1 << b):
        sign = 1 if mask.bit_count() % 2 else -1
        base.extend([(mask, sign), (mask << b, -sign)])
    entries = {0: 1}
    for j in range(copies):
        entries = {a | (u << (2 * b * j)): c * v for a, c in entries.items() for u, v in base}
    coeff = [entries.get(a, 0) for a in range(1 << n)]
    vals = zeta(coeff, n)
    mask = (1 << b) - 1
    for x, val in enumerate(vals):
        expected = 1
        for j in range(copies):
            block = x >> (2 * b * j)
            expected *= int(bool(block & mask)) - int(bool((block >> b) & mask))
        assert val == expected
    T = set(entries)
    N = {x for x, val in enumerate(vals) if val}
    minima = [a for a in T if not any(z != a and z & a == z for z in T)]
    W = sum(1 << (n - a.bit_count()) for a in minima)
    m, k = len(T), len(N)
    assert m == k == (2 * ((1 << b) - 1)) ** copies
    assert W == (b * (1 << (2 * b))) ** copies
    assert T == N
    assert set(entries.values()) <= {-1, 1}
    assert set(vals) <= {-1, 0, 1}
    group_checks = 0
    for modulus in (2, 3, 4, 5, 6):
        for g in range(1, modulus):
            assert {x for x, val in enumerate(vals) if (g * val) % modulus} == N
            assert {a for a, c in entries.items() if (g * c) % modulus} == T
            group_checks += 1
    return dict(b=b, copies=copies, n=n, m=m, k=k, W=W,
                mk=m*k, ratio=str(Q(W, m*k)), exact_proposals=str(Q(W, k)),
                full_cube_points=1 << n, cyclic_group_scalar_checks=group_checks)


def floor_arrays():
    """Check constant floor, equality, and structural bounds on bounded groups."""
    checked = 0
    biased = 0
    for modulus, n in ((2, 3), (3, 3), (4, 3), (6, 2)):
        size = 1 << n
        for coeff in product(range(modulus), repeat=size):
            if not coeff[0]:
                continue
            vals = zeta(coeff, n, modulus)
            T = [a for a, c in enumerate(coeff) if c]
            k = sum(v != 0 for v in vals)
            m = len(T)
            assert beta(m) * k >= size
            if m * k == size:
                union = 0
                for a in T:
                    union |= a
                assert T == [a for a in range(size) if a & union == a]
                assert all(coeff[a] == ((-1) ** a.bit_count() * coeff[0]) % modulus for a in T)
            weights = sum(Q(1, 1 << a.bit_count()) for a in T)
            assert weights <= Q(k, size) * rho_sum(T, False)
            assert rho_sum(T, False) <= D(m)
            checked += 1
            if n == 2:
                ps = [Q(1, 3), Q(1, 4)]
                q = sum((product_mass(x, ps) for x, v in enumerate(vals) if v), Q(0))
                assert q >= Q(1, beta(m))
                biased += 1
    # A genuinely noncyclic coefficient group, with componentwise operations.
    n = 2
    elements = [(a, b) for a in range(2) for b in range(4)]
    noncyclic = 0
    for coeff in product(elements, repeat=4):
        if coeff[0] == (0, 0):
            continue
        c0 = [x[0] for x in coeff]
        c1 = [x[1] for x in coeff]
        v0, v1 = zeta(c0, n, 2), zeta(c1, n, 4)
        m = sum(x != (0, 0) for x in coeff)
        k = sum((a, b) != (0, 0) for a, b in zip(v0, v1))
        assert beta(m) * k >= 4
        noncyclic += 1
    return dict(cyclic_constant_nonzero_arrays=checked,
                noncyclic_Z2_times_Z4_arrays=noncyclic, biased_arrays=biased)


def product_mass(x, ps):
    mass = Q(1)
    for j, p in enumerate(ps):
        mass *= p if x >> j & 1 else 1-p
    return mass


def minimal_factor_max():
    counts = Counter()
    for bits in range(1, 256):
        T = [a for a in range(8) if bits >> a & 1]
        m = len(T)
        v = rho_sum(T, True)
        assert v <= E(m)
        counts[m] = max(counts[m], v)
    attaining = []
    for m in range(1, 33):
        r = max(range(1, m+1), key=lambda r: r*beta(m-r+1))
        T = [1 << j for j in range(r)]
        common = (1 << r)-1
        for j in range(m-r):
            common |= 1 << (r+j)
            T.append(common)
        v = rho_sum(T, True)
        assert len(T) == m and v == E(m)
        attaining.append(dict(m=m, minimal_count=r, E_m=v))
    return dict(all_3cube_supports=255, observed_max_by_m=dict(counts),
                attaining_families=attaining,
                exactness_scope="maximum structural factor, not sharp polynomial ratio")


def rank(cols):
    basis = {}
    for col in cols:
        while col:
            p = col.bit_length()-1
            if p in basis:
                col ^= basis[p]
            else:
                basis[p] = col
                break
    return len(basis)


def matroid_small():
    r, columns = 2, [1, 2, 3]
    n = 2 * len(columns)
    values = []
    for y in range(1 << n):
        value = 0
        for v in range(1 << r):
            active = True
            for j, a in enumerate(columns):
                label = (a & v).bit_count() % 2
                active &= not bool(y & (1 << (2*j+label)))
            value ^= int(active)
        values.append(value)
    # In characteristic two the Boolean Mobius and zeta transforms coincide.
    coefficients = zeta(values, n, 2)
    T = [a for a, c in enumerate(coefficients) if c]
    N = [x for x, v in enumerate(values) if v]
    bases = sum(rank(c) == r for c in combinations(columns, r))
    spanning = sum(rank([a for j, a in enumerate(columns) if c >> j & 1]) == r
                   for c in range(1 << len(columns)))
    minima = [a for a in T if not any(z != a and z & a == z for z in T)]
    assert len(T) == len(N) == (1 << r)*spanning == 16
    assert len(minima) == (1 << r)*bases == 12
    assert all(a.bit_count() == r for a in minima)
    def swap(x):
        return sum(((x >> (2*j) & 1) << (2*j+1)) |
                   ((x >> (2*j+1) & 1) << (2*j)) for j in range(len(columns)))
    assert {swap(x) for x in T} == set(N)
    return dict(rank=r, columns=columns, truth_points=64, m=16, k=16,
                bases=bases, spanning_subsets=spanning, minimal_count=12)


def subspaces_by_low_pivot(r):
    """Independent RREF enumeration with lowest pivots, unlike producer code."""
    for d in range(r+1):
        for pivots in combinations(range(r), d):
            nonpivots = set(range(r)) - set(pivots)
            free = [(i, j) for i, p in enumerate(pivots) for j in sorted(nonpivots) if j > p]
            for choice in range(1 << len(free)):
                basis = [1 << p for p in pivots]
                for k, (i, j) in enumerate(free):
                    if choice >> k & 1:
                        basis[i] |= 1 << j
                vectors = [0]
                for row in basis:
                    vectors += [x ^ row for x in vectors]
                yield d, sum(1 << x for x in vectors)


def gaussian(r, d):
    numerator = denominator = 1
    for j in range(d):
        numerator *= (1 << r)-(1 << j)
        denominator *= (1 << d)-(1 << j)
    return numerator // denominator


def matroid_rank8():
    columns = [5,12,14,19,25,27,34,36,40,47,50,52,57,58,61,64,84,107,
               116,118,122,126,143,147,148,151,153,154,157,159,160,173,
               174,181,183,185,187,211,212,216,226,227,234,236,245,246,251]
    r, count = 8, len(columns)
    assert len(set(columns)) == count and rank(columns) == r
    column_mask = sum(1 << a for a in columns)
    B = P = 0
    dims = [0]*(r+1)
    for d, subspace in subspaces_by_low_pivot(r):
        dims[d] += 1
        n_U = (subspace & column_mask).bit_count()
        codimension = r-d
        mu = (-1)**codimension * (1 << (codimension*(codimension-1)//2))
        B += mu * comb(n_U, r)
        P += mu * (1 << n_U)
    assert dims == [gaussian(r, d) for d in range(r+1)]
    assert sum(dims) == 417199
    assert B == 96991671 and P == 140675317510576
    m = (1 << r)*P
    W = B*(1 << (2*count))
    return dict(rank=r, columns=columns, n=2*count,
                enumerated_subspaces=sum(dims), subspaces_by_dimension=dims,
                bases=B, spanning_subsets=P, m=m, k=m, W=W,
                W_over_mk=str(Q(W,m*m)), spanning_rejection_success=str(Q(P,1 << count)),
                expanded_ANF_or_truth_enumerated=False)


def log_interval(x):
    """Rational atanh-series enclosure for a positive rational's logarithm."""
    x = Q(x)
    e = 0
    while x >= 2:
        x /= 2
        e += 1
    while x < 1:
        x *= 2
        e -= 1
    def core(y):
        z = (y-1)/(y+1)
        N = 70
        low = 2*sum((z**(2*j+1)/(2*j+1) for j in range(N)), Q(0))
        remainder = 2*z**(2*N+1)/((2*N+1)*(1-z*z))
        return low, low+remainder
    lo, hi = core(x)
    two_lo, two_hi = core(Q(2))
    if e >= 0:
        return lo+e*two_lo, hi+e*two_hi
    return lo+e*two_hi, hi+e*two_lo


def decimal_endpoint(x, up=False):
    scale = 10**24
    q, rem = divmod(x.numerator*scale, x.denominator)
    q += bool(up and rem)
    return f"{q//scale}.{q%scale:024d}"


def exponent_intervals(rank8):
    lo, hi = log_interval(Q(rank8['W'], rank8['m']))
    ml, mh = log_interval(rank8['m'])
    explicit = [decimal_endpoint(lo/mh), decimal_endpoint(hi/ml, True)]
    assert explicit == ['1.191504627393948753655902', '1.191504627393948753655903']
    rows = []
    for r, d in ((8,46),(16,93),(32,186),(64,373),(128,746)):
        kappa = Q(1)
        for j in range(1, r+1):
            kappa *= 1-Q(1, 1 << j)
        expected = kappa*comb(d,r)
        guaranteed = -((-expected.numerator)//expected.denominator)
        W = guaranteed*(1 << (2*d))
        M = 1 << (d+r)
        l, h = log_interval(Q(W,M))
        ml, mh = log_interval(M)
        rows.append(dict(rank=r,D=d,existential_only=True,
                         guaranteed_bases=guaranteed,
                         alpha_lower=decimal_endpoint(l/mh)))
    b = 12
    or_m = 2*((1 << b)-1)
    or_W = b*(1 << (2*b))
    l, h = log_interval(Q(or_W,or_m))
    ml, mh = log_interval(or_m)
    or_alpha = [decimal_endpoint(l/mh), decimal_endpoint(h/ml,True)]
    assert or_alpha == ['1.121977691996127544277265','1.121977691996127544277266']
    return dict(explicit_rank8_alpha=explicit, all_group_OR12_alpha=or_alpha,
                finite_existential_bounds=rows,
                limiting_alpha='log2(1+sqrt(2))', limiting_proof='symbolic; not finite extrapolation')


def main():
    started = time.monotonic()
    result = dict(status='PASS', producer_code_imported=False,
                  or_family=[or_case(b) for b in range(1,6)]+[or_case(4,2)],
                  sparse_floor=floor_arrays(), minimum_factor_max=minimal_factor_max(),
                  paired_matroid_small=matroid_small())
    result['paired_matroid_rank8'] = matroid_rank8()
    result['exponents'] = exponent_intervals(result['paired_matroid_rank8'])
    result['elapsed_seconds'] = time.monotonic()-started
    result['scope'] = 'Exact finite checks only; see INDEPENDENT_PROOF.txt for universal arguments.'
    result['script_sha256'] = sha256(Path(__file__).read_bytes()).hexdigest()
    receipt = HERE/'INDEPENDENT_RECEIPT.json'
    receipt.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'], receipt=str(receipt),
                         elapsed_seconds=result['elapsed_seconds'],
                         exact_or_n8=result['or_family'][3],
                         floor=result['sparse_floor'],
                         rank8={k:v for k,v in result['paired_matroid_rank8'].items() if k!='columns'},
                         exponents=result['exponents']),indent=2))


if __name__ == '__main__':
    main()
