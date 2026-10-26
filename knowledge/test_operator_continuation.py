"""Independent exact controls for four acquired proof versions; no producer imports."""
import itertools
import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def transpose(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    return [[sum(x*y for x, y in zip(r, c)) for c in zip(*b)] for r in a]


def plus(a, b, sign=1):
    return [[x+sign*y for x, y in zip(r, s)] for r, s in zip(a, b)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def inverse(a):
    n = len(a)
    b = [[F(x) for x in r]+s for r, s in zip(a, eye(n))]
    for j in range(n):
        k = next(i for i in range(j, n) if b[i][j])
        b[j], b[k] = b[k], b[j]
        d = b[j][j]
        b[j] = [x/d for x in b[j]]
        for i in range(n):
            if i != j:
                d = b[i][j]
                b[i] = [x-d*y for x, y in zip(b[i], b[j])]
    return [r[n:] for r in b]


def scalar_form(a, v):
    return sum(v[i]*a[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))


class OperatorContinuationTests(unittest.TestCase):
    def test_common_rank_one_has_interior_extremum(self):
        def contrast(t):
            return 3/(3*t+2)-F(49, 16)*3/(3*t+8)
        self.assertEqual(contrast(F(2)), F(-9, 32))
        self.assertEqual(contrast(F(1)), F(-207, 880))
        for t in [F(k, 10) for k in range(10, 31)]:
            s = [[2, 1, 0], [1, 2, 0], [0, 0, t]]
            values = []
            for k in [1, 2]:
                a = plus(s, [[0, 0, k], [0, 0, 0], [-k, 0, 0]], -1)
                values.append(inverse(a)[2][2])
            self.assertEqual(values[0]-F(49, 16)*values[1], contrast(t))
            self.assertLessEqual(F(-9, 32), contrast(t))
            self.assertLessEqual(contrast(t), F(-207, 880))
            lhs = -144*(3*t+8)**2+441*(3*t+2)**2
            self.assertEqual(lhs, 81*(t-2)*(33*t+46))

    def test_noisy_saturation_and_biased_transcript(self):
        s = F(1, 1000)
        beta, gamma = (1-s*s)/(1+s*s), 2*s/(1+s*s)
        self.assertEqual(beta*beta+gamma*gamma, 1)
        self.assertEqual(1-beta, F(2, 1000001))
        self.assertEqual(gamma, F(2000, 1000001))
        # These tridiagonal matrices have eigenvalues 2,2+-sqrt(beta^2+gamma^2).
        eta = F(1, 100)
        for c in [F(k, 20) for k in range(21)]:
            # t0+-2eta and biases b0-+eta give reports within eta of midpoint.
            difference = 4*eta*c-2*eta
            self.assertLessEqual(abs(difference), 2*eta)

    def test_port_interval_lift_including_singular_visible_uncertainty(self):
        # D and M are both singular; the actual rational Moore-Penrose inverse
        # is supplied explicitly here rather than hidden behind a floating SVD.
        d = [[F(2), 0, 0], [0, 0, 0], [0, 0, 0]]
        p = [[F(1), 0, 0], [0, 0, F(1)]]
        md = [[F(1, 2), 0], [0, 0]]
        e = [[F(1), 0], [0, 0]]
        x = mm(mm(mm(mm(mm(d, transpose(p)), md), e), md), mm(p, d))
        self.assertEqual(mm(mm(p, x), transpose(p)), e)
        self.assertEqual(x, [[F(1), 0, 0], [0, 0, 0], [0, 0, 0]])
        source = inverse(plus(eye(3), x))
        reduced = inverse(mm(mm(p, inverse(source)), transpose(p)))
        self.assertEqual(reduced, [[F(1, 2), 0], [0, F(1)]])
        # Separate exact boundary intervals do not preserve a common source.
        h = [[F(1), 0], [0, F(1, 3)]]
        q = [F(3, 5), F(4, 5)]
        self.assertEqual(1/scalar_form(h, q), F(75, 43))
        self.assertLess(F(75, 43), 3)

    def test_actual_network_shunt_reaction_and_reciprocal_calibration(self):
        t = [[F(2), F(1, 4)], [F(1, 4), F(5, 2)]]
        h = inverse(t)
        base = [[F(2), F(1), 0, 0], [F(1), F(2), 0, 0],
                [0, 0, t[0][0], t[0][1]], [0, 0, t[1][0], t[1][1]]]
        for v in [[F(1), F(0)], [F(0), F(1)], [F(1), F(1)]]:
            for gain in [F(1), F(5, 4)]:
                for strength in [F(1, 2), F(1), F(2)]:
                    u = [F(1), F(0), -v[0], -v[1]]
                    a = plus(base, [[gain*strength*x*y for y in u] for x in u])
                    row = [a[0][1:]]
                    inner = [r[1:] for r in a[1:]]
                    native = a[0][0]-mm(mm(row, inverse(inner)), transpose(row))[0][0]
                    expected = F(3, 2)+gain*strength/(1+gain*strength*scalar_form(h, v))
                    self.assertEqual(native, expected)
                    self.assertEqual(1/(native-F(3, 2)), scalar_form(h, v)+1/(gain*strength))
        q0, invgain, b0 = F(3, 5), F(4, 5), F(3, 2)
        xs = [F(2), F(1), F(1, 2)]
        ys = [b0+1/(q0+invgain*x) for x in xs]
        a = (ys[1]-ys[0])*(xs[1]-xs[2])
        b = (ys[2]-ys[1])*(xs[0]-xs[1])
        recovered = (b*ys[0]-a*ys[2])/(b-a)
        self.assertEqual(recovered, b0)
        z = [1/(y-recovered) for y in ys]
        self.assertEqual((z[0]-z[1])/(xs[0]-xs[1]), invgain)

    def test_gain_free_task_and_all_input_calibration_gauge(self):
        h = [[F(3, 5), F(-4, 79)], [F(-4, 79), F(2, 3)]]
        v, w = [F(3, 5), F(4, 5)], [F(3, 5), F(-4, 5)]
        self.assertEqual(F(25, 48)*(scalar_form(h, v)-scalar_form(h, w)), h[0][1])
        delta, gain, strength = F(1, 100), F(4, 5), F(2)
        changed = plus(h, [[delta, 0], [0, delta]])
        for q in [v, w, [F(1), F(0)], [F(0), F(1)]]:
            old = scalar_form(h, q)+gain/strength
            new = scalar_form(changed, q)+(gain-strength*delta)/strength
            self.assertEqual(old, new)
        self.assertEqual(F(40, 79)*F(32, 79)-F(781, 1580)**2, F(-97961, 2496400))

    def test_balanced_codrift_and_sharp_protocol_source_pairs(self):
        bq, bh, eps = F(1, 40), F(1, 50), F(1, 10000)
        for tau, times, xs, radius, dh, expected in [
            (F(3, 10), [-1, 0, 1], [2, 1, 2], lambda t: t*t*(bq/2+bh)+3*eps,
             lambda t: -2*eps-t*t*(bq/2+bh), F(129, 40000)),
            (F(1, 10), [-3, -1, 1, 3], [2, 1, 1, 2],
             lambda t: t*t*(7*bq/2+8*bh)+3*eps,
             lambda t: -2*eps-t*t*(4*bq+17*bh/2), F(111, 40000))]:
            error = radius(tau)
            self.assertEqual(error, expected)
            for sign in [-1, 1]:
                for multiple, x in zip(times, xs):
                    time = multiple*tau
                    q = F(3, 5)+sign*(error+bq*time*time/2)
                    h = F(4, 5)+sign*(dh(tau)+bh*time*time/2)
                    self.assertLessEqual(abs(q+x*h-(F(3, 5)+x*F(4, 5))), eps)
                    self.assertTrue(F(1, 3) < q < 1 and h > 0)
        tau = F(1, 10)
        def z(t, x):
            return F(3, 5)+F(1, 25)*t+x*(F(4, 5)-F(1, 20)*t)
        self.assertEqual(2*z(0, 1)-(z(-tau, 2)+z(tau, 2))/2, F(3, 5))

    def test_causal_design_uses_actual_preceding_actions(self):
        strengths = [F(1, 2), F(2), F(1, 2), F(2), F(1)]
        times = [F(i, 10) for i in [-2, -1, 0, 1, 2]]
        previous = [F(0)]+strengths[:-1]
        rows = [[F(1), t, 1/l, t/l, w] for t, l, w in zip(times, strengths, previous)]
        # Invertibility verifies one realizable sequential five-call design.
        matrix_inverse = inverse(rows)
        truth = [[F(3, 5)], [F(1, 25)], [F(4, 5)], [F(-1, 20)], [F(1, 100)]]
        self.assertEqual(mm(matrix_inverse, mm(rows, truth)), truth)
        def unseen(w):
            return F(1, 100)*w*(w-F(1, 2))*(w-2)
        self.assertTrue(all(unseen(w) == 0 for w in previous))
        self.assertEqual(unseen(F(1)), F(-1, 200))

    def test_current_acceptance_is_at_actual_versions(self):
        from knowledge.retrieve import Library
        lib = Library()
        for n, count in [(1049, 4), (1050, 4), (1051, 3)]:
            family = lib.resolve('N'+str(n))
            units = [r for r in lib.records.values() if family['id'] in r['parents']]
            self.assertEqual(len(units), count)
            for r in [family]+units:
                review = next(a for a in r['review_overlays'] if a['id'] == f'A{n+22}-operator-continuation')
                self.assertEqual(review['decision'], 'accepted_internally_verified')
                self.assertIn({'id': r['id'], 'content_version': r['content_version']}, review['subjects'])
        self.assertIn('JOINT', lib.resolve('N1050')['statement'])
        update = ROOT/'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-retained-operator-continuation'
        index = json.loads((update/'source/INDEX.json').read_text())
        original = [r for r in index['files'] if r['kind'] == 'frozen_original']
        self.assertEqual((len(original), sum(r['bytes'] for r in original)), (13, 141397))


if __name__ == '__main__':
    unittest.main()
