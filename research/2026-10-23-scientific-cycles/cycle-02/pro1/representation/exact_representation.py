#!/usr/bin/env python3
"""Exact finite diagnostics for the two-seed Fock representation.

Standard library only. Operator normal forms are exact on the infinite bath;
the replay tests specified finite identities, not an asymptotic capacity claim.
Run: python exact_representation.py --output replay.json
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json
import platform
import resource
import time


@dataclass(frozen=True)
class G:
    """Gaussian rational."""
    re: F = F(0)
    im: F = F(0)

    def __add__(self, other):
        other = asg(other)
        return G(self.re + other.re, self.im + other.im)
    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-asg(other))

    def __mul__(self, other):
        other = asg(other)
        return G(self.re * other.re - self.im * other.im,
                 self.re * other.im + self.im * other.re)
    __rmul__ = __mul__

    def conjugate(self):
        return G(self.re, -self.im)

    def __bool__(self):
        return bool(self.re or self.im)


def asg(x):
    return x if isinstance(x, G) else G(F(x))


I_G = G(F(0), F(1))
EMPTY = ()
# ('F',u,v) = I_seed tensor L_u L_v*.
# ('K',u,v) = X_seed tensor |u><v|.
ONE = {('F', EMPTY, EMPTY): G(F(1))}
ROOT = {('K', EMPTY, EMPTY): G(F(1))}


def clean(a):
    return {k: v for k, v in a.items() if v}


def add(*terms):
    out = {}
    for term in terms:
        for k, v in term.items():
            out[k] = out.get(k, G()) + v
    return clean(out)


def scale(a, c):
    c = asg(c)
    return clean({k: c * v for k, v in a.items()})


def prefix(x, p):
    return len(x) >= len(p) and x[:len(p)] == p


def even_matrix_unit(u, v):
    # |u><v| = L_u L_v* - sum_a L_(u a) L_(v a)*.
    return [(('F', u, v), 1)] + [
        (('F', u + (a,), v + (a,)), -1) for a in (1, 2)]


def basis_product(a, b):
    kind, u, v = a
    kind2, x, y = b
    if kind == 'F' and kind2 == 'F':
        if prefix(x, v):
            return [(('F', u + x[len(v):], y), 1)]
        if prefix(v, x):
            return [(('F', u, y + v[len(x):]), 1)]
        return []
    if kind == 'F' and kind2 == 'K':
        return [(('K', u + x[len(v):], y), 1)] if prefix(x, v) else []
    if kind == 'K' and kind2 == 'F':
        return [(('K', u, y + v[len(x):]), 1)] if prefix(v, x) else []
    return even_matrix_unit(u, y) if v == x else []


def mul(a, b):
    out = {}
    for ka, ca in a.items():
        for kb, cb in b.items():
            for k, sign in basis_product(ka, kb):
                out[k] = out.get(k, G()) + ca * cb * sign
    return clean(out)


def adjoint(a):
    return {(kind, v, u): c.conjugate() for (kind, u, v), c in a.items()}


def trace_stationary(a, theta=F(1, 6)):
    return sum((c * theta**len(u) for (kind, u, v), c in a.items()
                if kind == 'F' and u == v), G())


def gram(a, b, theta=F(1, 6)):
    return trace_stationary(mul(adjoint(a), b), theta)


S = {a: {('F', (a,), EMPTY): G(F(1))} for a in (1, 2)}


def port_matrix(alpha, beta):
    b = [[{} for _ in range(3)] for _ in range(3)]
    b[0][0] = add(scale(ROOT, alpha), scale(ONE, I_G * beta))
    for a in (1, 2):
        b[0][a] = scale(S[a], alpha)
        b[a][0] = scale(adjoint(S[a]), alpha)
        b[a][a] = scale(ONE, I_G * beta)
    return b


def amplitude(b, x, y):
    out = ONE
    for xi, yi in zip(x, y):
        out = mul(b[yi][xi], out)
        if not out:
            break
    return out


def dyck_words(m):
    def shapes(p, opened, closed):
        if opened == m and closed == m:
            yield p
            return
        if opened < m:
            yield from shapes(p + (1,), opened + 1, closed)
        if closed < opened:
            yield from shapes(p + (0,), opened, closed + 1)
    words = []
    for shape in shapes((), 0, 0):
        for colors in product((1, 2), repeat=m):
            it = iter(colors)
            words.append(tuple(next(it) if bit else 0 for bit in shape))
    return words


def ideal_output(w):
    stack, out = [], []
    for x in w:
        if x:
            stack.append(x)
            out.append(0)
        else:
            out.append(stack.pop())
    assert not stack
    return tuple(out)


def balanced_exponent(w, z):
    """r when T[z,w]=(-1)^(m-r) alpha^(2r) beta^(2m-2r); None if zero."""
    stack, moves = [], 0
    for x, y in zip(w, ideal_output(z)):
        if x and not y:
            stack.append(x)
            moves += 1
        elif not x and y:
            if not stack or stack.pop() != y:
                return None
            moves += 1
        elif x and y and x != y:
            return None
    assert not stack and moves % 2 == 0
    return moves // 2


def rational_rank(a):
    a = [[F(x) for x in row] for row in a]
    nr, nc, rank = len(a), len(a[0]), 0
    for col in range(nc):
        pivot = next((i for i in range(rank, nr) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        pv = a[rank][col]
        for i in range(rank + 1, nr):
            if not a[i][col]:
                continue
            factor = a[i][col] / pv
            for j in range(col + 1, nc):
                a[i][j] -= factor * a[rank][j]
            a[i][col] = F(0)
        rank += 1
        if rank == nr:
            break
    return rank


def run():
    started = time.perf_counter()
    # Rational point exactly on the unit circle, within the requested small-angle range.
    t = F(1, 2048)
    alpha = (1 - t*t)/(1 + t*t)
    beta = 2*t/(1 + t*t)
    assert alpha*alpha + beta*beta == 1 and 0 < beta <= F(1, 512)
    b = port_matrix(alpha, beta)

    for a in (1, 2):
        for c in (1, 2):
            assert mul(adjoint(S[a]), S[c]) == (ONE if a == c else {})
        assert mul(ROOT, S[a]) == {}
        assert mul(adjoint(S[a]), ROOT) == {}
    defect = add(ONE, *(scale(mul(S[a], adjoint(S[a])), -1) for a in (1, 2)))
    assert mul(ROOT, ROOT) == defect
    assert trace_stationary(ROOT) == G()
    assert trace_stationary(defect) == G(F(2, 3))
    for a in range(3):
        for c in range(3):
            value = add(*(mul(adjoint(b[y][a]), b[y][c]) for y in range(3)))
            assert value == (ONE if a == c else {})

    # Two-slot code: exact amplitudes, independent of a finite bath truncation.
    checks_two = 0
    for a in (1, 2):
        for y in product(range(3), repeat=2):
            expected = {}
            if y == (0, a):
                expected = scale(ONE, alpha*alpha)
            elif y == (0, 0):
                expected = scale(S[a], I_G * alpha * beta)
            elif y[0] == a and y[1] in (1, 2):
                expected = scale(adjoint(S[y[1]]), I_G * alpha * beta)
            elif y == (a, 0):
                expected = add(scale(ROOT, I_G * alpha * beta), scale(ONE, -beta*beta))
            assert amplitude(b, (a, 0), y) == expected
            checks_two += 1
    good = [scale(ONE, alpha*alpha),
            add(scale(ROOT, I_G*alpha*beta), scale(ONE, -beta*beta)),
            scale(adjoint(S[1]), I_G*alpha*beta),
            scale(adjoint(S[2]), I_G*alpha*beta)]
    probability = alpha*alpha*beta*beta
    assert add(*(mul(adjoint(x), x) for x in good)) == scale(ONE, 1-probability)

    # Dark pair identity, with exact real and genuinely complex colors.
    dark_colors = [(G(F(1)), G()), (G(), G(F(1))),
                   (G(F(3, 5)), G(F(4, 5))),
                   (G(F(3, 5)), G(F(0), F(4, 5)))]
    dark_checks = 0
    for colors in dark_colors:
        sc = add(*(scale(S[a], colors[a-1]) for a in (1, 2)))
        for y in product(range(3), repeat=2):
            value = add(*(scale(add(amplitude(b, (0, a), y),
                                    scale(amplitude(b, (a, 0), y), -1)),
                                colors[a-1]) for a in (1, 2)))
            value = mul(value, sc)
            scalar = G()
            if y[0] == 0 and y[1] in (1, 2):
                scalar = -colors[y[1]-1]
            elif y[0] in (1, 2) and y[1] == 0:
                scalar = colors[y[0]-1]
            assert value == scale(sc, scalar)
            dark_checks += 1

    balanced = []
    for m in (1, 2, 3):
        ws = dyck_words(m)
        for w in ws:
            for z in ws:
                r = balanced_exponent(w, z)
                coeff = F(0) if r is None else ((-1)**(m-r) * alpha**(2*r)
                                               * beta**(2*m-2*r))
                assert amplitude(b, w, ideal_output(z)) == scale(ONE, coeff)
        # Separate exact rational point beta^2=1/D for a small-block spectral diagnostic.
        D = 2**20
        p = [[0 if (r := balanced_exponent(w, z)) is None
              else (-1)**(m-r)*(D-1)**r for w in ws] for z in ws]
        cap = (D-1)**2 * D**(2*m-2)
        gram_defect = [[int(i == j)*cap - sum(p[k][i]*p[k][j] for k in range(len(ws)))
                       for j in range(len(ws))] for i in range(len(ws))]
        nullity = len(ws) - rational_rank(gram_defect)
        assert nullity == m+1  # checked only at m=1,2,3, not claimed universally
        balanced.append({'m': m, 'dimension': len(ws), 'amplitude_identities': len(ws)**2,
                         'max_singular_subspace_dimension_at_beta_squared_2^-20': nullity})

    return {'status': 'exact_finite_diagnostics_passed',
            'unit_circle_point': {'alpha': str(alpha), 'beta': str(beta)},
            'two_slot_amplitude_checks': checks_two,
            'dark_pair_checks': dark_checks,
            'balanced_filters': balanced,
            'bath_truncation_used': False,
            'universal_claims_depend_on': 'written operator proofs, not finite check count',
            'wall_seconds': time.perf_counter()-started,
            'max_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'python': platform.python_version(), 'platform': platform.platform()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    args = parser.parse_args()
    receipt = run()
    rendered = json.dumps(receipt, indent=2) + '\n'
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as handle:
            handle.write(rendered)
    print(rendered, end='')
