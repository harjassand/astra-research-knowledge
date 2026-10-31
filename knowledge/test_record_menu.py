"""Protect complementary source routes without query-specific ranking fixtures."""
import unittest

from knowledge.mcp_adapter import record_menu


class RecordMenuTests(unittest.TestCase):
    def setUp(self):
        self.records = {x: {"id": x, "parents": [], "kind": "result"} for x in "ABCDEFG"}
        self.records['UA'] = {"id": 'UA', "parents": ['A'], "kind": 'mechanism'}

    @staticmethod
    def lane(*names):
        return [{"id": x} for x in names]

    def test_parent_and_intermediate_share_family_support_and_one_slot(self):
        chosen = record_menu([self.lane('A', 'B', 'C'), self.lane('UA', 'C', 'B')], [], self.records)
        self.assertEqual(chosen[0], 'UA')
        self.assertNotIn('A', chosen)
        self.assertEqual(len(chosen), 3)

    def test_distinct_lane_leaders_survive_consensus_candidates(self):
        lanes = [self.lane('A', 'C', 'D', 'E', 'F', 'G'), self.lane('B', 'C', 'D', 'E', 'F', 'G')]
        chosen = record_menu(lanes, [], self.records)
        self.assertEqual(len(chosen), 5)
        self.assertTrue({'A', 'B'} <= set(chosen))
        # Both independent opportunities survive even when shared candidates
        # collect more reciprocal-rank support than either unique leader.
        self.assertEqual(chosen[:3], ['C', 'D', 'E'])

    def test_explicit_sibling_identities_keep_order_and_budget(self):
        lanes = [self.lane('B', 'C'), self.lane('D', 'E')]
        self.assertEqual(record_menu(lanes, ['A', 'UA'], self.records, limit=3), ['A', 'UA', 'B'])
        self.assertEqual(record_menu(lanes, ['A', 'UA', 'C', 'D'], self.records, limit=2), ['A', 'UA'])

    def test_declared_consumer_opportunity_uses_a_slot_without_losing_leaders(self):
        lanes = [self.lane('A', 'E', 'F', 'G'), self.lane('B', 'E'),
                 self.lane('C', 'E'), self.lane('D', 'E')]
        chosen = record_menu(lanes, [], self.records, declared_routes={'F'})
        self.assertEqual(len(chosen), 5)
        self.assertTrue({'A', 'B', 'C', 'D', 'F'} <= set(chosen))
        self.assertNotIn('E', chosen)

    def test_route_keeps_its_actual_member_without_duplicating_the_family(self):
        chosen = record_menu([self.lane('A', 'B'), self.lane('B', 'UA')],
                             [], self.records, declared_routes={'UA'})
        self.assertIn('UA', chosen)
        self.assertNotIn('A', chosen)
        self.assertEqual(len(chosen), 2)

    def test_declared_route_cannot_displace_explicit_requested_identities(self):
        requested = ['A', 'B', 'C', 'D', 'E']
        self.assertEqual(record_menu([self.lane('G', 'F')], requested,
                                     self.records, declared_routes={'F'}), requested)

    def test_empty_lanes_and_repeat_family_votes_are_bounded(self):
        self.assertEqual(record_menu([[], []], ['A'], self.records), ['A'])
        self.assertEqual(record_menu([self.lane('A', 'UA', 'A'), self.lane('B')], [], self.records), ['A', 'B'])


if __name__ == '__main__':
    unittest.main()
