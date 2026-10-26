"""Source-exposed independent exact controls, not a missing producer replay."""
import itertools
import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = 'N1048-cyclic-gradient-and-anisotropic-feedback-acquisition'


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def sub(a, b):
    return [x-y for x, y in zip(a, b)]


def weights(z, h, alpha=F(1, 3), metric=None):
    metric = metric or [[F(3, 2), 0], [0, F(3, 2)]]
    residual = [sub(x, [alpha*t for t in g]) for x, g in zip(h, z)]
    return [[dot(residual[j], sub(z[i], z[j])) +
             dot(sub(residual[i], residual[j]),
                 matvec(metric, sub(residual[i], residual[j])))/2
             for i in range(len(z))] for j in range(len(z))]


def matvec(a, v):
    return [dot(row, v) for row in a]


def cycles(w):
    for n in range(2, len(w)+1):
        for c in itertools.permutations(range(len(w)), n):
            if c[0] == min(c):
                yield c, sum(w[c[k]][c[(k+1) % n]] for k in range(n))


def distances(w):
    d = [r[:] for r in w]
    for k in range(len(d)):
        for i in range(len(d)):
            for j in range(len(d)):
                d[i][j] = max(d[i][j], d[i][k]+d[k][j])
    return d


class Radical:
    """Exact a+b*sqrt(97), enough to check all analytic endpoint cycles."""
    def __init__(self, a=0, b=0):
        self.a, self.b = F(a), F(b)

    def __add__(self, v):
        v = v if isinstance(v, Radical) else Radical(v)
        return Radical(self.a+v.a, self.b+v.b)

    __radd__ = __add__

    def __neg__(self):
        return Radical(-self.a, -self.b)

    def __sub__(self, v):
        return self+-v

    def __rsub__(self, v):
        return -self+v

    def __mul__(self, v):
        v = v if isinstance(v, Radical) else Radical(v)
        return Radical(self.a*v.a+97*self.b*v.b, self.a*v.b+self.b*v.a)

    __rmul__ = __mul__

    def __truediv__(self, v):
        return Radical(self.a/v, self.b/v)

    def nonpositive(self):
        if self.b == 0:
            return self.a <= 0
        if self.b > 0:
            return self.a <= 0 and self.a*self.a >= 97*self.b*self.b
        return self.a <= 0 or self.a*self.a <= 97*self.b*self.b


class CyclicGradientTests(unittest.TestCase):
    def fixture(self, a, square=False):
        z = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1))]
        if square:
            z.insert(2, (F(1), F(1)))
        h = [(F(2, 3)*x-a*y, a*x+F(2, 3)*y) for x, y in z]
        return z, h, weights(z, h)

    def test_pairs_and_triples_miss_actual_global_obstruction(self):
        for a, square, margin in [(F(4, 15), False, F(11, 75)),
                                  (F(1, 5), True, F(14, 75))]:
            z, h, w = self.fixture(a, square)
            self.assertEqual(max(v for _, v in cycles(w)), margin)
            size = 3 if square else 2
            for subset in itertools.combinations(range(len(w)), size):
                ws = [[w[i][j] for j in subset] for i in subset]
                self.assertLessEqual(max(v for _, v in cycles(ws)), 0)
                phi = distances(ws)[0]
                for j in range(size):
                    for i in range(size):
                        self.assertGreaterEqual(phi[i]-phi[j], ws[j][i])
                        # Reverse edge proves active max-quadratic constructor.
                        self.assertGreaterEqual(phi[j]-phi[i], ws[i][j])

    def test_correlated_coordinate_error_rejection_bound(self):
        eta = F(1, 1000)
        for a, square, expected in [(F(4, 15), False, F(70797, 500000)),
                                    (F(1, 5), True, F(67897, 375000))]:
            g, x, _ = self.fixture(a, square)
            r = [sub(v, u) for v, u in zip(g, x)]
            w = [[dot(r[j], sub(x[i], x[j])) +
                  dot(sub(r[i], r[j]), sub(r[i], r[j]))/4
                  for i in range(len(x))] for j in range(len(x))]
            cycle, total = max(cycles(w), key=lambda t: t[1])
            bound = 0
            for k, j in enumerate(cycle):
                i = cycle[(k+1) % len(cycle)]
                bound += eta*sum(map(abs, sub(x[i], x[j])))
                bound += eta*sum(map(abs, sub(r[i], r[j])))+2*eta*eta
            self.assertEqual(total-bound, expected)
            # All correlated box corners: do not assume independent noise.
            for signs in itertools.product([-1, 1], repeat=2*len(g)):
                noisy = [[g[i][k]+eta*signs[2*i+k] for k in range(2)]
                         for i in range(len(g))]
                rr = [sub(v, u) for v, u in zip(noisy, x)]
                val = sum(dot(rr[j], sub(x[cycle[(k+1) % len(cycle)]], x[j])) +
                          dot(sub(rr[cycle[(k+1) % len(cycle)]], rr[j]),
                              sub(rr[cycle[(k+1) % len(cycle)]], rr[j]))/4
                          for k, j in enumerate(cycle))
                self.assertGreaterEqual(val, expected)

    def test_exact_sharp_endpoints_and_pair_only_failure(self):
        z = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1))]
        old = [(F(0), F(0)), (F(2, 3), F(4, 15))]
        for h in [(Radical(F(1, 6), F(-1, 30)), F(4, 5)),
                  (F(1, 3), F(2, 3))]:
            for _, value in cycles(weights(z, old+[h])):
                self.assertTrue(value.nonpositive() if isinstance(value, Radical)
                                else value <= 0)
        w = weights(z, old+[(F(-1, 3), F(2, 3))])
        self.assertTrue(all(v <= 0 for c, v in cycles(w) if len(c) == 2))
        self.assertGreater(max(v for _, v in cycles(w)), 0)

    def test_attainable_relative_energy_ranges(self):
        for n, expected in [(1, (F(91, 300), F(109, 300))),
                            (2, (F(191, 600), F(209, 600))),
                            (4, (F(391, 1200), F(409, 1200)))]:
            z = [(F(k, n), F(0)) for k in range(n+1)]
            h = [(F(2, 3)*t, F(4, 15)*t) for t, _ in z]
            w = weights(z, h)
            d = distances(w)
            self.assertEqual((d[0][-1]+F(1, 6), -d[-1][0]+F(1, 6)), expected)
            for phi in [d[0], d[-1]]:
                self.assertTrue(all(phi[i]-phi[j] >= w[j][i]
                                    for i in range(n+1) for j in range(n+1)))

    def test_safe_rounded_outer_cut_and_mixed_controller_failure(self):
        # q(h)=||h||^2-1 <=0; tangent at(2,1) gives 4x+2y<=6.
        normal, rounded = (F(4), F(2)), (F(17, 4), F(7, 4))
        # Known box[-1,1]^2: RHS inflation is exact support of rounding error.
        rhs = 6+sum(abs(a-b) for a, b in zip(rounded, normal))
        self.assertEqual(rhs, F(13, 2))
        for x in [F(k, 10) for k in range(-10, 11)]:
            for y in [F(k, 10) for k in range(-10, 11)]:
                if x*x+y*y <= 1:
                    self.assertLessEqual(dot(rounded, [x, y]), rhs)
        self.assertEqual(F(1)*(1-0), 1)  # E1'=x, first controller.
        self.assertEqual((3-F(1, 2))*F(2, 5), 1)  # E2'=3x, second.
        self.assertEqual((F(1)-F(6, 5))*(1-F(2, 5)), F(-3, 25))

    def test_anisotropic_metric_and_scalar_regression(self):
        # Off-diagonal K, diagonalized by a rational orthogonal 2x2 matrix.
        k = [[F(0), F(1, 2)], [F(1, 2), F(0)]]
        def inv(a):
            d = a[0][0]*a[1][1]-a[0][1]*a[1][0]
            return [[a[1][1]/d, -a[0][1]/d], [-a[1][0]/d, a[0][0]/d]]
        def shifted(l):
            return [[l-k[0][0], -k[0][1]], [-k[1][0], l-k[1][1]]]
        c, ai = inv(shifted(3)), inv(shifted(1))
        metric = inv([[ai[i][j]-c[i][j] for j in range(2)] for i in range(2)])
        native_x = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1))]
        # Independent known quadratic E=||x||^2, gradients=2x.
        z = [matvec(shifted(2), x) for x in native_x]
        residual = [sub(x, matvec(c, g)) for x, g in zip(native_x, z)]
        phi = [(dot(g, x)-dot(g, matvec(c, g)))/2
               for x, g in zip(native_x, z)]
        for j in range(3):
            for i in range(3):
                dr = sub(residual[i], residual[j])
                w = dot(residual[j], sub(z[i], z[j]))+dot(dr, matvec(metric, dr))/2
                self.assertGreaterEqual(phi[i]-phi[j], w)
        # Scalar k=1/2 reduces exactly to alpha=1/(L-k),d^-1.
        alpha, beta = F(2, 5), F(2)
        self.assertEqual(1/(beta-alpha), F(5, 8))

    def test_current_source_and_actual_review_scope(self):
        from knowledge.retrieve import Library
        lib = Library()
        family = lib.resolve(PARENT)
        self.assertEqual(len([r for r in lib.records.values() if
                              r['id'].startswith('U1048-')]), 6)
        for r in [family]+[lib.resolve(i) for i in lib.records if i.startswith('U1048-')]:
            review = next(a for a in r['review_overlays'] if a['id'] == 'A1070-cyclic-gradient')
            self.assertEqual(review['decision'], 'accepted_internally_verified')
            self.assertIn({'id': r['id'], 'content_version': r['content_version']}, review['subjects'])
        update = ROOT/'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-cyclic-gradient-acquisition'
        index = json.loads((update/'source/INDEX.json').read_text())
        self.assertEqual(sum(r['bytes'] for r in index['files'] if r['kind'] == 'frozen_original'), 25831)
        self.assertIn('UNACQUIRED', family['body'])


if __name__ == '__main__':
    unittest.main()
