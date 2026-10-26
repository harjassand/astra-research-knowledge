"""Protect actual proof branches and chemical model boundaries; no producer replay."""
import ast
from fractions import Fraction as Q
import hashlib,json,subprocess,sys,unittest
from knowledge.model import ROOT
from knowledge.retrieve import Library

UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-cooperative-footprints'
UNITS=['U1024-cooperative-blocking-sets','U1024-guide-release-feedback-set','U1024-blind-reaction-order','U1024-joint-guide-clearance','U1024-idempotent-retry-ceiling']
PROOF='1287ccc2db35fce707fa3956ed37b1a4d0222f77fa30b419ebbe4a66730374f7'

class CooperativeFootprints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_cooperative_source_is_not_a_pairwise_or_hardware_claim(self):
        source=self.library.source(UNITS[0],0)
        self.assertEqual(source['source']['sha256'],PROOF)
        self.assertEqual(source['source']['lines'],[15,25])
        self.assertIn('B_0={{1,2}}',source['text'])
        self.assertIn('outcome-aware scheduling',source['text'])
        code=self.library.source(UNITS[0],1)
        self.assertEqual(code['source']['lines'],[11,43])
        self.assertIn('def dp(done, footprints)',code['text'])
        self.assertIn('release is allowed only after a successful bond',code['text'])
        record=self.library.resolve(UNITS[0])
        self.assertIn('unmeasured',record['body'])

    def test_feedback_set_reduction_keeps_prerequisite_and_port_scope(self):
        source=self.library.source(UNITS[1],0)
        self.assertIn('no chemical prerequisites',source['text'])
        record=self.library.resolve(UNITS[1])
        self.assertIn('no prerequisites',record['contract']['requires'][0])
        self.assertIn('i!=j',record['contract']['requires'][0])
        self.assertIn('outgoing edges',record['body'])
        self.assertIn('cooperative blocking sets require',record['body'])
        # An edge0->1 requires1 before0; adding prerequisite0 before1
        # makes execution impossible despite an acyclic blocker graph.
        from itertools import permutations
        feasible=[order for order in permutations(range(2)) if order.index(1)<order.index(0) and order.index(0)<order.index(1)]
        self.assertEqual(feasible,[])

    def test_self_footprints_are_not_strict_precedence_constraints(self):
        # Before a one-site first reaction, its own product is absent.
        self.assertFalse({0}.issubset(set()))
        # A literal graph self-loop is a directed cycle requiring FVS size1;
        # chemical release count is0, so it must be omitted from that graph.
        record=self.library.resolve(UNITS[1])
        self.assertEqual(record['version'],2)
        self.assertIn('omit self arcs',record['body'])
        source=self.library.source(UNITS[1],2)
        self.assertEqual(source['source']['lines'],[143,154])
        self.assertIn('if i!=j',source['text'])
        prior=ROOT/'knowledge/units'/UNITS[1]/'v0001.json'
        self.assertEqual(record['previous'],hashlib.sha256(prior.read_bytes()).hexdigest())

    def test_feasibility_does_not_import_blind_execution(self):
        from itertools import permutations
        orders=list(permutations(range(3)))
        self.assertEqual(Q(sum(order[-1]==2 for order in orders),len(orders)),Q(1,3))
        bridge=self.library.bridge(UNITS[0],UNITS[2])['transfers'][0]
        self.assertEqual(bridge['state'],'REFUTED TRANSFER')
        for endpoint in ['from','to']:
            self.assertEqual(bridge[endpoint+'_version'],self.library.resolve(bridge[endpoint])['content_version'])
        self.assertIn('2/6=1/3',bridge['scope'])
        actual=self.library.source(UNITS[2],2)
        self.assertEqual(actual['source']['lines'],[211,247])
        self.assertIn('weight*=rates[j]/sum',actual['text'])
        self.assertEqual(self.library.bridge('N1020',UNITS[4])['state'],'NO SUPPORTED CONNECTION')

    def test_joint_retention_does_not_follow_from_marginals(self):
        q=Q(1,10)
        self.assertEqual(1-q*q,Q(99,100))
        self.assertEqual(1-q,Q(9,10))
        record=self.library.resolve(UNITS[3])
        self.assertIn('independence across motifs',record['statement'])
        self.assertIn('cannot be replaced by those products',record['body'])
        self.assertIn('not uniquely steric causation',record['body'])
        source=self.library.source(UNITS[3],0)
        self.assertEqual(source['source']['lines'],[43,53])
        self.assertIn('Frechet bounds',source['text'])

    def test_zero_feed_error_is_visible_without_running_original_code(self):
        source=self.library.source(UNITS[4],1)
        self.assertEqual(source['source']['lines'],[300,310])
        tree=ast.parse(source['text'])
        function=tree.body[0]
        assignment=next(n for n in function.body if isinstance(n,ast.Assign))
        self.assertIsInstance(assignment.value,ast.IfExp)
        self.assertEqual(ast.unparse(assignment.value.orelse),'p')
        p=Q(3,5);w=Q(2,5)
        self.assertEqual(sum((p*(1-p-w)**k for k in range(0)),Q(0)),0)
        self.assertEqual(sum((p*(1-p-w)**k for k in range(1)),Q(0)),p)
        record=self.library.resolve(UNITS[4])
        self.assertIn('Y_0=0',record['statement'])
        self.assertTrue(any(n['notice_id']=='SN-U1024-ZERO-FEED-BOUNDARY-20261026' for n in record['notices']))
        self.assertIn('permanent wrong',record['body'].lower())

    def test_frozen_assets_versioned_acceptance_and_default_wire_packets(self):
        index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']),3)
        self.assertEqual(sum(r['bytes'] for r in index['files']),39977)
        for row in index['files']:
            self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])
        for identifier in ['N1024',*UNITS]:
            record=self.library.resolve(identifier)
            review_id='A1043-cooperative-distinct-site-scope' if identifier in ['N1024',UNITS[1]] else 'A1042-cooperative-footprints'
            review=next(r for r in record['review_overlays'] if r['id']==review_id)
            self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects'])
            self.assertEqual(review['decision'],'accepted_internally_verified')
            self.assertEqual(review['working_device'],'not established')
            self.assertRegex(review['scope'],r'No source scientific code|no producer scientific program')
            result=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',identifier],cwd=ROOT,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertLessEqual(len(result.stdout),32768)
        result=subprocess.run([sys.executable,'knowledge/retrieve.py','bridge',UNITS[0],UNITS[2]],cwd=ROOT,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertLessEqual(len(result.stdout),32768)

if __name__=='__main__':unittest.main()
