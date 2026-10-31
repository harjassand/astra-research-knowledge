import itertools
import random
import tempfile
import unittest
from fractions import Fraction as Q
import sympy as sp
from acquire import (EVEN, I, acquire, apply_certificate, brute_contract,
                     cube_graph, generate_task, kron, make_hidden)
from acquire import save_certificate, load_certificate
from strong_retained_comparison import one_instance_acquire, same_admitted_subspaces
from all_weights_pfaffian import contract
from retained_elimination import compile_plan, execute


class ConstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inc, cls.edges, _ = cube_graph()
        cls.hidden = make_hidden(cls.inc, cls.edges)
        rng = random.Random(110)
        cls.obs = [generate_task(cls.hidden, rng)[0] for _ in range(4)]
        cls.multi = acquire(cls.inc, cls.edges, cls.obs)
        cls.single = one_instance_acquire(cls.inc, cls.edges, cls.obs[0])

    def test_entire_subspaces_match(self):
        self.assertTrue(same_admitted_subspaces(self.multi, self.single))

    def test_stalled_rank_is_insufficient_data(self):
        with self.assertRaisesRegex(ValueError, 'dimension is 1, not four'):
            acquire(self.inc, self.edges, [self.obs[0]]*10)

    def test_incompatible_edge_rejected(self):
        shear = sp.Matrix([[1, 1], [0, 1]])
        op = kron([shear, I, I])
        bad = [[sp.Matrix(t) for t in obs] for obs in self.obs]
        for obs in bad:
            obs[0] = op*obs[0]
        with self.assertRaisesRegex(ValueError, 'incompatible'):
            acquire(self.inc, self.edges, bad)

    def test_wrong_input_shapes_rejected(self):
        with self.assertRaisesRegex(ValueError, 'wrong number'):
            apply_certificate(self.single, self.obs[0][:-1])
        bad = self.obs[0][:]
        bad[0] = sp.zeros(4, 1)
        with self.assertRaisesRegex(ValueError, 'eight coefficients'):
            apply_certificate(self.single, bad)

    def test_off_family_query_rejected(self):
        bad = [sp.MutableDenseMatrix(t) for t in self.obs[0]]
        bad[0][0] += 1
        with self.assertRaisesRegex(ValueError, 'outside certified family'):
            apply_certificate(self.single, bad)

    def test_persistent_certificate_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = directory+'/chart.json'
            save_certificate(self.single, self.inc, self.edges, path)
            loaded = load_certificate(path, self.inc, self.edges)
            self.assertTrue(same_admitted_subspaces(loaded, self.single))
            self.assertEqual(apply_certificate(loaded, self.obs[0]),
                             apply_certificate(self.single, self.obs[0]))

    def test_exact_signed_cancellation(self):
        inc, edges = [[0, 1, 2], [0, 2, 1]], [(0, 1)]*3
        a, b = sp.zeros(8, 1), sp.zeros(8, 1)
        a[0] = a[3] = b[0] = 1
        b[3] = -1
        self.assertEqual(brute_contract([a, b], inc, edges), 0)
        self.assertEqual(contract([a, b], inc, edges), 0)

    def test_signed_singular_queries_exact(self):
        rng = random.Random(1992)
        plan = compile_plan(self.inc, self.edges)
        for case in range(8):
            canonical = []
            for v in self.inc:
                t = sp.zeros(8, 1)
                for i in EVEN:
                    t[i] = rng.randint(-3, 3)
                canonical.append(t)
            raw = [h*t for h, t in zip(self.hidden, canonical)]
            acquired = apply_certificate(self.single, raw)
            self.assertEqual(contract(acquired, self.inc, self.edges), execute(plan, raw))
            if case < 2:
                self.assertEqual(execute(plan, raw), brute_contract(raw, self.inc, self.edges))

    def test_parallel_disconnected_and_pivot_flips(self):
        inc = [[0, 1, 2], [0, 2, 1], [3, 4, 5], [3, 5, 4]]
        edges = [(0, 1)]*3+[(2, 3)]*3
        rng = random.Random(255)
        for _ in range(20):
            ts = []
            for v in inc:
                t = sp.zeros(8, 1)
                for i in EVEN:
                    t[i] = rng.randint(-2, 2)
                ts.append(t)
            self.assertEqual(contract(ts, inc, edges), brute_contract(ts, inc, edges))

    def test_local_city_signature_exhaustive(self):
        # Independent six-vertex matching recursion checks all eight deletions.
        def matching(vertices, weights):
            if not vertices:
                return Q(1)
            a = min(vertices)
            total = Q(0)
            for b in vertices-{a}:
                w = weights.get(tuple(sorted((a, b))), 0)
                if w:
                    total += w*matching(vertices-{a, b}, weights)
            return total
        for weights3 in itertools.product((-1, 0, 2), repeat=3):
            weights = {(0, 3):Q(1), (1, 4):Q(1), (2, 5):Q(1),
                       (3, 4):Q(weights3[0]), (3, 5):Q(weights3[1]),
                       (4, 5):Q(weights3[2])}
            expected = {0:Q(1), 6:Q(weights3[0]), 5:Q(weights3[1]), 3:Q(weights3[2])}
            for mask in range(8):
                removed = {i for i in range(3) if (mask >> (2-i)) & 1}
                self.assertEqual(matching(set(range(6))-removed, weights), expected.get(mask, 0))


if __name__ == '__main__':
    unittest.main()
