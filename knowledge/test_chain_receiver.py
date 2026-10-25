"""A documented scientific composition must reach its actual receiving proof."""
import unittest
from knowledge.retrieve import Library


class CompleteBellRecordReceiver(unittest.TestCase):
    def test_actual_prior_and_complete_instrument_route(self):
        library = Library()
        identifier = 'U1007-complete-noisy-bell-record-receiver'
        source = library.source(identifier, 0)
        self.assertTrue(source['source']['path'].endswith('sol_c/SUPPORT_AWARE_GLUING.txt'))
        self.assertEqual(source['source']['lines'], [194, 363])
        self.assertIn('P^dagger P+Q^dagger Q=I', source['text'])
        self.assertIn('pi_success=1/6', source['text'])
        self.assertIn('eta = log(2)/(2 log(5))', source['text'])
        self.assertIn('The local Hessian ratio at p is 5/32', ' '.join(source['text'].split()))
        self.assertIn('6ccc93118898ba5ec074c7ca9a4e5f8a897bb338', source['text'])
        transfer = library.bridge('N994', identifier)['transfers'][0]
        self.assertEqual(transfer['state'], 'ESTABLISHED COMPATIBLE INTERFACE')
        self.assertEqual(transfer['from_version'], library.resolve('N994')['content_version'])
        self.assertEqual(transfer['to_version'], library.resolve(identifier)['content_version'])


if __name__ == '__main__':
    unittest.main()
