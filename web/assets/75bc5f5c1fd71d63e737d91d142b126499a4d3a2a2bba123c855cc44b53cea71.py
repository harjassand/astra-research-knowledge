"""Finite model checks only; no biological data are represented here."""

import unittest

from robust_state_dp import robust_open_loop_value, robust_state_feedback_plan


class StateProgramChecks(unittest.TestCase):
    def setUp(self):
        # Toy memory system: M writes state 1; F yields suppression only in
        # state 1. Each action consumes one distinct nutrient unit.
        self.outcomes = {}
        for t in range(2):
            for state in (0, 1):
                for action in ("M", "F"):
                    key = (t, state, action)
                    next_state = 1 if action == "M" else state
                    cost = (1.0, 0.0) if action == "M" else (0.0, 1.0)
                    reward = 1.0 if action == "F" and state == 1 else 0.0
                    self.outcomes[key] = ((next_state, cost, reward),)

    def test_same_occupation_different_order(self):
        mf = robust_open_loop_value(0, ("M", "F"), self.outcomes, (1.0, 1.0))
        fm = robust_open_loop_value(0, ("F", "M"), self.outcomes, (1.0, 1.0))
        self.assertEqual(mf, 1.0)
        self.assertEqual(fm, 0.0)

    def test_dp_finds_stateful_schedule(self):
        result = robust_state_feedback_plan(
            0,
            (("M", "F"), ("M", "F")),
            self.outcomes,
            (1.0, 1.0),
        )
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.suppression_lower, 1.0)
        self.assertIn((0, 0, (1.0, 1.0), "M"), result.policy)
        self.assertIn((1, 1, (0.0, 1.0), "F"), result.policy)

    def test_unresolved_write_uncertainty_is_worst_case(self):
        uncertain = dict(self.outcomes)
        uncertain[(0, 0, "M")] = (
            (0, (1.0, 0.0), 0.0),
            (1, (1.0, 0.0), 0.0),
        )
        result = robust_state_feedback_plan(
            0,
            (("M", "F"), ("M", "F")),
            uncertain,
            (1.0, 1.0),
        )
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.suppression_lower, 0.0)


if __name__ == "__main__":
    unittest.main()
