#!/usr/bin/env python3
"""Deterministic exact binary matrix Kloosterman counts.

Uses the established formulas of Erdelyi--Toth, Erdelyi--Sawin--Toth,
and Zelingher.  The implementation adds explicit polynomial-cost finite
field factoring and column-height dynamic programming; no field elements,
Jordan partitions, subspaces, or invertible matrices are enumerated by
the counter.  Exhaustive oracles below are deliberately separate.
"""
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import itertools
import json
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work_field_root'))
from field_kloosterman import (gf_mul, gf_pow, gf_trace, irreducible_binary,
                              kloosterman_dwork)


class Field:
    def __init__(self, h):
        if not irreducible_binary(h):
            raise ValueError('binary modulus is not irreducible')
        self.h = h
        self.a = h.bit_length() - 1
        self.q = 1 << self.a
        self.mul = lambda x, y: gf_mul(x, y, h)
        self.pow = lambda x, n: gf_pow(x, n, h)
        self.inv = lambda x: gf_pow(x, self.q - 2, h) if x else self._zero_inverse()
        self.trace = lambda x: gf_trace(x, h)

    @staticmethod
    def _zero_inverse():
        raise ZeroDivisionError


def trim(f):
    f = list(f)
    while f and not f[-1]:
        f.pop()
    return f


def padd(f, g):
    out = list(f) + [0] * max(0, len(g) - len(f))
    for i, c in enumerate(g):
        out[i] ^= c
    return trim(out)


def pscale(f, c, F):
    return trim([F.mul(x, c) for x in f])


def pmul(f, g, F):
    out = [0] * max(0, len(f) + len(g) - 1)
    for i, x in enumerate(f):
        for j, y in enumerate(g):
            out[i + j] ^= F.mul(x, y)
    return trim(out)


def pdivmod(f, g, F):
    f, g = trim(f), trim(g)
    if not g:
        raise ZeroDivisionError
    out = [0] * max(0, len(f) - len(g) + 1)
    inverse = F.inv(g[-1])
    while len(f) >= len(g):
        j = len(f) - len(g)
        c = F.mul(f[-1], inverse)
        out[j] = c
        for i, x in enumerate(g):
            f[i + j] ^= F.mul(c, x)
        f = trim(f)
    return trim(out), f


def pmod(f, g, F):
    return pdivmod(f, g, F)[1]


def pexact(f, g, F):
    q, r = pdivmod(f, g, F)
    if r:
        raise ArithmeticError('inexact polynomial division')
    return q


def pgcd(f, g, F):
    while g:
        f, g = g, pmod(f, g, F)
    return pscale(f, F.inv(f[-1]), F) if f else []


def ppowmod(f, n, modulus, F):
    out = [1]
    while n:
        if n & 1:
            out = pmod(pmul(out, f, F), modulus, F)
        f = pmod(pmul(f, f, F), modulus, F)
        n >>= 1
    return out


def rref(A, F, width=None):
    A = [list(row) for row in A]
    width = len(A[0]) if width is None and A else (width or 0)
    pivots = []
    r = 0
    for j in range(width):
        p = next((i for i in range(r, len(A)) if A[i][j]), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        c = F.inv(A[r][j])
        A[r] = [F.mul(c, x) for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][j]:
                c = A[i][j]
                A[i] = [x ^ F.mul(c, y) for x, y in zip(A[i], A[r])]
        pivots.append(j)
        r += 1
        if r == len(A):
            break
    return A, pivots


def kernel(A, F, width=None):
    width = len(A[0]) if width is None and A else (width or 0)
    R, pivots = rref(A, F, width)
    out = []
    for j in range(width):
        if j in pivots:
            continue
        v = [0] * width
        v[j] = 1
        for i, p in enumerate(pivots):
            v[p] = R[i][j]
        out.append(v)
    return out


def factor_squarefree(f, F):
    """Berlekamp algebra, split through a fixed binary trace-dual search.

    This enumerates a basis of Fq, not its q elements. For different
    Berlekamp components, some trace of alpha*b separates their values.
    """
    f = trim(f)
    n = len(f) - 1
    if n <= 1:
        return [f] if n else []
    tq = ppowmod([0, 1], F.q, f, F)
    columns = []
    cur = [1]
    for j in range(n):
        v = cur + [0] * (n - len(cur))
        v[j] ^= 1
        columns.append(v)
        cur = pmod(pmul(cur, tq, F), f, F)
    B = kernel([list(row) for row in zip(*columns)], F)
    pieces = [f]
    for b in B:
        for j in range(F.a):
            z = pscale(b, 1 << j, F)
            tr = []
            for _ in range(F.a):
                tr = padd(tr, z)
                z = pmod(pmul(z, z, F), f, F)
            updated = []
            for g in pieces:
                u = pgcd(g, tr, F)
                if 1 < len(u) < len(g):
                    updated.extend([u, pexact(g, u, F)])
                else:
                    updated.append(g)
            pieces = updated
            if len(pieces) == len(B):
                return sorted(pieces, key=lambda x: (len(x), x))
    if len(pieces) != len(B):
        raise AssertionError('binary trace did not separate Berlekamp components')
    return sorted(pieces, key=lambda x: (len(x), x))


def factor_polynomial(f, F):
    """All monic irreducible factors with multiplicities, deterministically."""
    f = trim(f)
    if len(f) <= 1:
        return []
    f = pscale(f, F.inv(f[-1]), F)
    derivative = trim([f[i] if i & 1 else 0 for i in range(1, len(f))])
    if not derivative:
        root = [F.pow(f[i], 1 << (F.a - 1)) for i in range(0, len(f), 2)]
        return [(g, 2 * k) for g, k in factor_polynomial(root, F)]
    repeated = pgcd(f, derivative, F)
    squarefree = pexact(f, repeated, F)
    counts = defaultdict(int)
    for g in factor_squarefree(squarefree, F):
        counts[tuple(g)] += 1
    for g, k in factor_polynomial(repeated, F):
        counts[tuple(g)] += k
    return [(list(g), k) for g, k in sorted(counts.items(), key=lambda x: (len(x[0]), x[0]))]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def mmul(A, B, F):
    rows = len(A)
    cols = len(B[0]) if B else 0
    out = [[0] * cols for _ in range(rows)]
    for i, row in enumerate(A):
        for k, x in enumerate(row):
            if x:
                for j, y in enumerate(B[k]):
                    out[i][j] ^= F.mul(x, y)
    return out


def minverse(A, F):
    n = len(A)
    R, pivots = rref([row[:] + e for row, e in zip(A, eye(n))], F, n)
    return [row[n:] for row in R] if len(pivots) == n else None


def mtrace(A):
    out = 0
    for i, row in enumerate(A):
        out ^= row[i]
    return out


def trace_product(A, B, F):
    out = 0
    for i, row in enumerate(A):
        for j, x in enumerate(row):
            out ^= F.mul(x, B[j][i])
    return out


def charpoly(A, F):
    """Division-free block-adjugate recurrence, O(n^4) field operations."""
    n = len(A)
    if not n:
        return [1]
    M = [row[1:] for row in A[1:]]
    c = list(reversed(charpoly(M, F)))
    out = [0] * (n + 1)
    for i, x in enumerate(c):
        out[i] ^= x
        out[i + 1] ^= F.mul(A[0][0], x)
    R, C = A[0][1:], [[row[0]] for row in A[1:]]
    moments = []
    for k in range(n - 1):
        s = 0
        for x, y in zip(R, C):
            s ^= F.mul(x, y[0])
        moments.append(s)
        C = mmul(M, C, F)
        for i in range(k + 1):
            out[k + 2] ^= F.mul(c[i], moments[k - i])
    return list(reversed(out))


def matrix_poly(g, D, F):
    n = len(D)
    out = [[0] * n for _ in range(n)]
    for c in reversed(g):
        out = mmul(out, D, F)
        for i in range(n):
            out[i][i] ^= c
    return out


def primary_columns(D, g, multiplicity, F):
    n, d = len(D), len(g) - 1
    G = matrix_poly(g, D, F)
    P = eye(n)
    previous = 0
    columns = []
    for _ in range(multiplicity):
        P = mmul(P, G, F)
        nullity = n - len(rref(P, F)[1])
        increment = nullity - previous
        if increment % d:
            raise AssertionError('primary kernel increment has wrong degree')
        columns.append(increment // d)
        previous = nullity
        if previous == d * multiplicity:
            break
    if sum(columns) != multiplicity or any(x <= 0 for x in columns):
        raise AssertionError('invalid primary partition')
    if columns != sorted(columns, reverse=True):
        raise AssertionError('nondecreasing Jordan columns')
    return columns


def invariant_subspace_counts(columns, Q):
    """All invariant-subspace dimensions by polynomial column-height DP.

    columns are the conjugate Jordan partition. At stage i the state is
    (u_{i+1}, already_accumulated_dimension). We sum the elementary
    filtration-count formula from EST Theorem 10, without enumerating
    submodule partitions. At most O(b^3) states and O(b^4) transitions.
    """
    b = sum(columns)
    gaussian = [[0] * (b + 1) for _ in range(b + 1)]
    gaussian[0][0] = 1
    powers = [1]
    for _ in range(b * b):
        powers.append(powers[-1] * Q)
    for n in range(1, b + 1):
        gaussian[n][0] = gaussian[n][n] = 1
        for k in range(1, n):
            gaussian[n][k] = gaussian[n - 1][k - 1] + powers[k] * gaussian[n - 1][k]
    states = {(0, 0): 1}
    transitions = 0
    peak = 1
    for height in reversed(columns):
        nxt = defaultdict(int)
        for (below, total), value in states.items():
            for current in range(below, height + 1):
                weight = (powers[below * (height - current)] *
                          gaussian[height - below][current - below])
                nxt[current, total + current] += value * weight
                transitions += 1
        states = nxt
        peak = max(peak, len(states))
    result = [0] * (b + 1)
    for (_, degree), value in states.items():
        result[degree] += value
    if result != result[::-1] or result[0] != 1:
        raise AssertionError('invariant-subspace duality failed')
    return result, dict(dp_transitions=transitions, peak_dp_states=peak)


def power_sums(s, p, n):
    out = [2]
    if n:
        out.append(s)
    for _ in range(2, n + 1):
        out.append(s * out[-1] - p * out[-2])
    return out


def hall_two_variables(columns, Q, scalar_K):
    counts, stats = invariant_subspace_counts(columns, Q)
    b = len(counts) - 1
    powers = power_sums(-scalar_K, Q, b)
    total = 0
    qpower = 1
    for j in range((b + 1) // 2):
        total += counts[j] * qpower * powers[b - 2 * j]
        qpower *= Q
    if not b & 1:
        total += counts[b // 2] * Q ** (b // 2)
    stats['largest_coefficient_bits'] = max(x.bit_length() for x in counts)
    return total, stats


class Extension:
    """E=Fq[t]/(g), packed in a*d bits. No search for a primitive element."""
    def __init__(self, F, g):
        self.F, self.g = F, g
        self.d = len(g) - 1
        self.a = F.a * self.d

    def unpack(self, x):
        return [(x >> (self.F.a * i)) & (self.F.q - 1) for i in range(self.d)]

    def pack(self, x):
        return sum(c << (self.F.a * i) for i, c in enumerate(x))

    def mul(self, x, y):
        return self.pack(pmod(pmul(self.unpack(x), self.unpack(y), self.F), self.g, self.F))

    def root(self):
        return self.pack(pmod([0, 1], self.g, self.F))

    def minpoly_binary(self, x):
        pivots = {}
        power = 1
        for degree in range(self.a + 1):
            v, coefficient = power, 1 << degree
            while v:
                j = v.bit_length() - 1
                if j not in pivots:
                    pivots[j] = v, coefficient
                    break
                u, c = pivots[j]
                v ^= u
                coefficient ^= c
            if not v:
                if not irreducible_binary(coefficient):
                    raise AssertionError('root minimum polynomial is reducible')
                return coefficient
            power = self.mul(power, x)
        raise AssertionError('missing absolute minimal polynomial')


@lru_cache(maxsize=None)
def scalar_primary_K(field_h, irreducible_g):
    F = Field(field_h)
    E = Extension(F, list(irreducible_g))
    xi = E.root()
    h = E.minpoly_binary(xi)
    e = h.bit_length() - 1
    if E.a % e:
        raise AssertionError('minimum field does not divide ambient field')
    xi_flat = 1 if e == 1 else 2
    K, stats = kloosterman_dwork(xi_flat, h, use_hasse=True)
    lift = E.a // e
    K_full = -power_sums(-K, 1 << e, lift)[lift]
    return K_full, dict(absolute_minimum_degree=e, absolute_extension_degree=E.a,
                       scalar_field_modulus=h, scalar_count=K,
                       frobenius_lift_degree=lift, dwork=stats)


def matrix_kloosterman_from_primary(primary_data, rank_t, field_h=3):
    """Evaluate from acquired reduced-primary data, without matrix units.

    Each entry is a dictionary with irreducible (ascending coefficients),
    multiplicity, jordan_columns. These describe the reduced t-dimensional
    representation. A regular algebra action has t times these nullities;
    the caller must divide by t before supplying them.
    """
    F=Field(field_h)
    n=rank_t
    if not isinstance(n,int) or n<0:
        raise ValueError('matrix rank must be a nonnegative integer')
    if len({tuple(p['irreducible']) for p in primary_data})!=len(primary_data):
        raise ValueError('primary irreducibles must be distinct')
    if sum((len(p['irreducible'])-1)*p['multiplicity'] for p in primary_data)!=n:
        raise ValueError('primary dimensions do not sum to the matrix rank')
    start=time.perf_counter()
    pieces=[]
    product=1
    for primary in primary_data:
        g=list(primary['irreducible'])
        b=primary['multiplicity']
        columns=list(primary['jordan_columns'])
        d=len(g)-1
        if (sum(columns)!=b or columns!=sorted(columns,reverse=True) or
                any(x<=0 for x in columns)):
            raise ValueError('invalid Jordan columns')
        if factor_polynomial(g,F)!=[(g,1)]:
            raise ValueError('factor is not monic irreducible')
        data=dict(irreducible=g,multiplicity=b,primary_dimension=d*b,
                  jordan_columns=columns)
        if g==[0,1]:
            data.update(normalized_factor=1,nilpotent=True)
        else:
            scalar,scalar_data=scalar_primary_K(field_h,tuple(g))
            hall,dp_data=hall_two_variables(columns,F.q**d,scalar)
            product*=hall
            data.update(scalar_K=scalar,normalized_factor=hall,
                        scalar_data=scalar_data,**dp_data)
        pieces.append(data)
    result=(-1)**n*F.q**(n*(n-1)//2)*product
    return result,dict(matrix_rank=n,field_degree=F.a,primary_pieces=pieces,
        seconds=time.perf_counter()-start,enumerated_matrices=0,
        enumerated_subspaces=0,enumerated_field_elements=0)


def matrix_kloosterman(D, field_h=3):
    """Return K(D)=sum_{U in GL_n(Fq)} (-1)^Tr tr(U+D U^-1).

    Handles all D, including nilpotent/singular, nonsplit, and arbitrarily
    nonsemisimple matrices. Deterministic polynomial-time in n,a.
    """
    F = Field(field_h)
    n = len(D)
    if any(len(row) != n or any(not 0 <= x < F.q for x in row) for row in D):
        raise ValueError('invalid square matrix')
    start = time.perf_counter()
    cp = charpoly(D, F)
    factors = factor_polynomial(cp, F)
    primary_data = []
    for g, b in factors:
        columns = primary_columns(D, g, b, F)
        primary_data.append(dict(irreducible=g,multiplicity=b,jordan_columns=columns))
    result,stats=matrix_kloosterman_from_primary(primary_data,n,field_h)
    stats.update(characteristic_polynomial=cp,seconds=time.perf_counter()-start)
    return result,stats


def matrix_trace_cubic_count(A, B, C, field_h=3, constant=0):
    """Count phase-zero of Tr tr(XYZ+AX+BY+CZ)+constant.

    Here A,C must be invertible; B is arbitrary. The number of original
    independent Boolean inputs is 3*a*n*n, without internal-variable
    conversion. Return count plus the signed sum and charged backend data.
    """
    F = Field(field_h)
    n = len(A)
    if any(len(M) != n or any(len(row) != n for row in M) for M in (A,B,C)):
        raise ValueError('source matrix size mismatch')
    if minverse(A, F) is None or minverse(C, F) is None:
        raise ValueError('this reduction requires invertible A and C')
    D = mmul(mmul(A, C, F), B, F)
    K, stats = matrix_kloosterman(D, field_h)
    signed_sum = (-1) ** (constant & 1) * F.q ** (n*n) * K
    inputs = 3 * F.a * n*n
    numerator = (1 << inputs) + signed_sum
    if numerator & 1:
        raise AssertionError('nonintegral Boolean count')
    return numerator // 2, dict(original_inputs=inputs, signed_sum=signed_sum,
                               matrix_K=K, reduced_coefficient=D, backend=stats)


def gaussian_table(n, q):
    out = [[0] * (n + 1) for _ in range(n + 1)]
    out[0][0] = 1
    for r in range(1, n + 1):
        out[r][0] = out[r][r] = 1
        for k in range(1, r):
            out[r][k] = out[r-1][k-1] + q**k * out[r-1][k]
    return out


def injective_fourier(m, r, source_rank, q):
    """Fourier sum over injective maps Fq^r -> Fq^m."""
    if source_rank < 0 or source_rank > min(m,r) or r > m:
        return 0
    out = (-1)**source_rank * q**(r*(r-1)//2)
    for j in range(m-r+1, m-source_rank+1):
        out *= q**j-1
    return out


def cubic_zero_source_from_ranks(matrix_rank, field_degree, rank_A, rank_B, rank_BA):
    """Intrinsic zero-source backend using reduced (not regular-action) ranks."""
    n,a,ra,rb=matrix_rank,field_degree,rank_A,rank_B
    if (a<1 or n<0 or not 0<=ra<=n or not 0<=rb<=n or
            not max(0,ra+rb-n)<=rank_BA<=min(ra,rb)):
        raise ValueError('impossible rank data')
    q=1<<a
    w=ra-rank_BA
    h=n-rb
    G=gaussian_table(n,q)
    total=0
    terms=0
    for k in range(h+1):
        for j in range(max(0,k-h+w),min(k,w)+1):
            number=G[w][j]*G[h-w][k-j]*q**((w-j)*(k-j))
            total += number * q**(n*k) * injective_fourier(n,n-k,ra-j,q)
            terms += 1
    return q**(n*n)*total, dict(rank_A=ra,rank_B=rb,
        image_A_intersect_kernel_B=w,kernel_B=h,rank_strata=terms)


def cubic_zero_source_sum(A, B, field_h=3):
    """Signed sum of Tr tr(XYZ+AX+BY), with A,B completely arbitrary.

    Rank-stratified singular factorization XY=0, summed by closed Gaussian
    intersection counts. No nonsingularity of A or B is required.
    """
    F=Field(field_h)
    n=len(A)
    ra=len(rref(A,F)[1])
    rb=len(rref(B,F)[1])
    rba=len(rref(mmul(B,A,F),F)[1])
    return cubic_zero_source_from_ranks(n,F.a,ra,rb,rba)


def cubic_count_supported(A,B,C,field_h=3,constant=0):
    """Complete for any zero source, or any two invertible sources."""
    F=Field(field_h)
    sources=[A,B,C]
    n=len(A)
    for k in range(3):
        rotated=sources[k:]+sources[:k]
        if not any(x for row in rotated[2] for x in row):
            signed,details=cubic_zero_source_sum(*rotated[:2],field_h)
            signed *= (-1)**(constant&1)
            inputs=3*F.a*n*n
            return ((1<<inputs)+signed)//2,dict(original_inputs=inputs,
                signed_sum=signed,backend='zero-source Gaussian strata',
                cyclic_rotation=k,details=details)
        if minverse(rotated[0],F) is not None and minverse(rotated[2],F) is not None:
            count,stats=matrix_trace_cubic_count(*rotated,field_h,constant)
            stats['cyclic_rotation']=k
            return count,stats
    raise ValueError('nonzero sources with fewer than two invertible members are unsupported')


def matrix_ramanujan(n,source_rank,q):
    return injective_fourier(n,n,source_rank,q)


@lru_cache(maxsize=None)
def scalar_field_K(coefficient,field_h):
    return kloosterman_dwork(coefficient,field_h,use_hasse=True)[0]


def matrix_kloosterman_pair_rank_one_from_data(
        matrix_rank,field_h,rank_A,rank_B,trace_AB,rank_AB,rank_BA):
    """Two-coefficient K(A,B) when at least one coefficient has rank <=1.

    trace_AB is the relative matrix trace in Fq, not its absolute binary
    trace. Ranks are reduced t-dimensional matrix ranks. No matrix units
    are needed by this interface. The rank-one formulas have elementary
    Schur-complement proofs; see SINGULAR_PAIR_REDUCTIONS.tex.
    """
    F=Field(field_h)
    n=matrix_rank
    a,b=rank_A,rank_B
    if not 0<=a<=n or not 0<=b<=n:
        raise ValueError('invalid coefficient ranks')
    if a>b:
        a,b=b,a
        rank_AB,rank_BA=rank_BA,rank_AB
    if a>1:
        raise ValueError('requires a coefficient of rank at most one')
    if a==0:
        return matrix_ramanujan(n,b,F.q),dict(route='zero coefficient',other_rank=b)
    if trace_AB:
        scalar=scalar_field_K(trace_AB,field_h)
        value=F.q**(n-1)*scalar*matrix_ramanujan(n-1,b-1,F.q)
        return value,dict(route='rank-one regular primary',regular_scalar=trace_AB,
                          scalar_K=scalar,other_rank=b)
    value=matrix_ramanujan(n,b,F.q)
    if not rank_AB and not rank_BA:
        value-=F.q**(2*n-1)*matrix_ramanujan(n-1,b,F.q)
        route='rank-one isolated endpoints'
    else:
        route='rank-one connected nilpotent endpoints'
    return value,dict(route=route,other_rank=b,rank_AB=rank_AB,rank_BA=rank_BA)


def matrix_kloosterman_pair_rank_one(A,B,field_h=3):
    F=Field(field_h)
    AB,BA=mmul(A,B,F),mmul(B,A,F)
    return matrix_kloosterman_pair_rank_one_from_data(len(A),field_h,
        len(rref(A,F)[1]),len(rref(B,F)[1]),mtrace(AB),
        len(rref(AB,F)[1]),len(rref(BA,F)[1]))


# Independent exhaustive oracles. Never called from the counting backend.
def all_matrices(n, F):
    for entries in itertools.product(range(F.q), repeat=n*n):
        yield [list(entries[i*n:(i+1)*n]) for i in range(n)]


def matrix_kloosterman_oracle(D, field_h=3):
    F = Field(field_h)
    total, invertible = 0, 0
    for U in all_matrices(len(D), F):
        V = minverse(U, F)
        if V is not None:
            total += (-1) ** F.trace(mtrace(U) ^ trace_product(D, V, F))
            invertible += 1
    return total, invertible


def cubic_oracle(A, B, C, field_h=3, constant=0):
    F = Field(field_h)
    matrices = list(all_matrices(len(A), F))
    total = 0
    for X in matrices:
        ax = trace_product(A, X, F)
        for Y in matrices:
            value = ax ^ trace_product(B, Y, F)
            XY = mmul(X, Y, F)
            XY_C = [[x ^ y for x, y in zip(r, s)] for r, s in zip(XY, C)]
            for Z in matrices:
                phase = F.trace(value ^ trace_product(XY_C, Z, F)) ^ (constant & 1)
                total += 1 - phase
    return total


def jordan(blocks, alpha=1):
    n = sum(blocks)
    A = [[0]*n for _ in range(n)]
    offset = 0
    for b in blocks:
        for j in range(b):
            A[offset+j][offset+j] = alpha
            if j+1 < b:
                A[offset+j][offset+j+1] = 1
        offset += b
    return A


def companion(g):
    n=len(g)-1
    if not n or g[-1]!=1:
        raise ValueError('nonconstant monic polynomial required')
    D=[[0]*n for _ in range(n)]
    for i in range(n):
        D[i][-1]=g[i]
        if i:
            D[i][i-1]=1
    return D


def generalized_jordan(g,blocks):
    base=companion(g)
    d=len(base)
    n=d*sum(blocks)
    D=[[0]*n for _ in range(n)]
    offset=0
    for b in blocks:
        for j in range(b):
            for s in range(d):
                for t in range(d):
                    D[offset+j*d+s][offset+j*d+t]=base[s][t]
                if j+1<b:
                    D[offset+j*d+s][offset+(j+1)*d+s]=1
        offset+=d*b
    return D


def validation():
    rng = random.Random(73481)
    cases = []
    # Every 1x1 and 2x2 matrix over F2; every Jordan-type in dimension <=4,
    # plus nonsplit primary and mixed-singular examples.
    for n in (1, 2):
        for D in all_matrices(n, Field(3)):
            value, stats = matrix_kloosterman(D)
            expected, size = matrix_kloosterman_oracle(D)
            assert value == expected, (D, value, expected)
            cases.append(dict(field_h=3, D=D, value=value, gl_size=size))
    extra = [jordan([3]), jordan([2,1]), jordan([1,1,1]),
             jordan([3],0), [[0,0,1],[1,0,1],[0,1,0]],
             [[0,0,1],[1,0,0],[0,1,1]],
             [[0,1,0],[1,1,0],[0,0,1]],
             [[0,1,0],[1,1,0],[0,0,0]],
             jordan([4]),jordan([3,1]),jordan([2,2]),jordan([2,1,1]),jordan([1,1,1,1]),
             [[0,1,1,0],[1,1,0,1],[0,0,0,1],[0,0,1,1]]]
    for D in extra:
        value, stats = matrix_kloosterman(D)
        expected, size = matrix_kloosterman_oracle(D)
        assert value == expected, (D, value, expected)
        cases.append(dict(field_h=3,D=D,value=value,gl_size=size))
    for _ in range(12):
        D = [[rng.randrange(4) for _ in range(2)] for _ in range(2)]
        value, stats = matrix_kloosterman(D,7)
        expected, size = matrix_kloosterman_oracle(D,7)
        assert value == expected, (D, value, expected)
        cases.append(dict(field_h=7,D=D,value=value,gl_size=size))
    # Independent Boolean phase enumeration checks source order and signs.
    cubic_cases=[]
    for _ in range(5):
        A = rng.choice([[[1,0],[0,1]],[[1,1],[0,1]],[[0,1],[1,0]]])
        C = rng.choice([[[1,0],[0,1]],[[1,0],[1,1]],[[0,1],[1,0]]])
        B = [[rng.randrange(2) for _ in range(2)] for _ in range(2)]
        const = rng.randrange(2)
        value, stats = matrix_trace_cubic_count(A,B,C,constant=const)
        expected = cubic_oracle(A,B,C,constant=const)
        assert value == expected,(A,B,C,value,expected)
        cubic_cases.append(dict(A=A,B=B,C=C,constant=const,count=value,**stats))
    large=[]
    for field_h, blocks in [(3,[16,8,4,2,1,1]),(7,[8,8,8,8]),(0x13,[12,8,6,4,2])]:
        D=jordan(blocks)
        value, stats=matrix_kloosterman(D,field_h)
        n=len(D); a=field_h.bit_length()-1
        signed=(1<<(a*n*n))*value
        count=((1<<(3*a*n*n))+signed)//2
        large.append(dict(field_h=field_h,blocks=blocks,matrix_K=str(value),
                          original_inputs=3*a*n*n,zero_count=str(count),
                          count_bits=count.bit_length(),**stats))
    return dict(status='all exact assertions passed',
                classical_formula='Zelingher Theorems 1.2/4.6 plus EST Theorem 10',
                matrix_oracle_cases=cases,cubic_oracle_cases=cubic_cases,
                growing_rank_cases=large)


if __name__ == '__main__':
    data=validation()
    path=Path(__file__).with_name('matrix_kloosterman_results.json')
    path.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(status=data['status'],
        matrix_cases=len(data['matrix_oracle_cases']),
        cubic_cases=len(data['cubic_oracle_cases']),
        growing_rank_inputs=[x['original_inputs'] for x in data['growing_rank_cases']],
        results=str(path))))
