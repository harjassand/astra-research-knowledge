"""Current N901-style updates must not rewrite checkpoint-pinned indexes."""
import copy
import unittest
from knowledge.build import authority_layers


class AuthorityLayers(unittest.TestCase):
    def rows(self, value):
        return ([dict(id='N1', path='cards/N1.txt', status=value)],
                [dict(card_id='N1', card_path='cards/N1.txt', claim_status=value)],
                [dict(id='N1', pointers=dict(card_local='cards/N1.txt'), status=value)])

    def merge(self, old, current):
        return authority_layers(old[0], current[0], old[1], current[1], old[2], current[2])

    def test_current_rows_replace_baseline_without_mutating_it(self):
        old = self.rows('historical')
        before = copy.deepcopy(old)
        merged = self.merge(old, self.rows('current'))
        self.assertEqual(old, before)
        self.assertEqual(merged[0]['N1']['status'], 'current')
        self.assertEqual(merged[1]['N1']['claim_status'], 'current')
        self.assertEqual(merged[2]['N1']['status'], 'current')

    def test_duplicate_current_rows_are_not_last_writer_wins(self):
        current = self.rows('current')
        current[0].append(dict(current[0][0]))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.merge(self.rows('historical'), current)

    def test_partial_replacement_is_rejected(self):
        current = self.rows('current')
        current[1].clear()
        with self.assertRaisesRegex(ValueError, 'must agree'):
            self.merge(self.rows('historical'), current)

    def test_current_row_cannot_change_card_identity(self):
        current = self.rows('current')
        current[2][0]['pointers']['card_local'] = 'cards/other.txt'
        with self.assertRaisesRegex(ValueError, 'changed card identity'):
            self.merge(self.rows('historical'), current)

    def test_new_shard_ids_and_unreplaced_baselines_are_retained(self):
        current = self.rows('new')
        current[0][0]['id'] = current[1][0]['card_id'] = current[2][0]['id'] = 'N2'
        merged = self.merge(self.rows('historical'), current)
        self.assertTrue(all(set(rows) == {'N1', 'N2'} for rows in merged))
