"""Finite arithmetic checks; these validate code only, not biological claims."""

import math
import unittest

from robust_frontier import (
    collapse_context_bounds,
    hoeffding_radius,
    one_context_frontier,
    replicates_for_radius,
    required_net_suppression_rate,
)


class FrontierChecks(unittest.TestCase):
    def test_single_feasible_dose(self):
        result = one_context_frontier([1.0, 2.0, 4.0], [0.1, 0.5, 0.9], 2.0)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertAlmostEqual(result.suppression_rate, 0.5)
        self.assertAlmostEqual(result.resource_rate, 2.0)
        self.assertEqual(result.weights, ((1, 1.0),))

    def test_two_dose_mixture_hits_budget_frontier(self):
        result = one_context_frontier([1.0, 3.0], [0.2, 0.8], 2.0)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertAlmostEqual(result.resource_rate, 2.0)
        self.assertAlmostEqual(result.suppression_rate, 0.5)
        self.assertAlmostEqual(result.weights[0][1], 0.5)
        self.assertAlmostEqual(result.weights[1][1], 0.5)

    def test_worst_context_collapse(self):
        resources, suppression = collapse_context_bounds(
            [[1.0, 2.0], [1.5, 1.8]],
            [[0.2, 0.6], [0.3, 0.4]],
        )
        self.assertEqual(resources, [1.5, 2.0])
        self.assertEqual(suppression, [0.2, 0.4])

    def test_simultaneous_hoeffding_count(self):
        n = replicates_for_radius(18, 0.05, 0.25)
        self.assertEqual(n, 53)
        self.assertLessEqual(hoeffding_radius(n, 18, 0.05), 0.25)
        self.assertGreater(hoeffding_radius(n - 1, 18, 0.05), 0.25)

    def test_48_hour_ninety_percent_threshold(self):
        self.assertAlmostEqual(required_net_suppression_rate(0.1, 48), math.log(10) / 48)
        self.assertAlmostEqual(required_net_suppression_rate(0.1, 48), 0.0479705228, places=9)


if __name__ == "__main__":
    unittest.main()
