import copy,unittest
from knowledge.interfaces import compile_navigation,peers,packet_navigation,RELATION
class ConsumerTests(unittest.TestCase):
    def setUp(self):
        self.records=[dict(id='P1',content_version='1'*64,title='robust support',parents=['R1'],contract={}),dict(id='R1',content_version='2'*64,title='parent',parents=[],contract={}),dict(id='P2',content_version='3'*64,title='Bayes expectation',parents=[],contract={}),dict(id='C',content_version='4'*64,title='scalar threshold',parents=[],contract={'input_slots':[{'id':'bound','required_binding_fields':['target','lower','upper','units','qualification']}]})]
        self.edges=[]
        for i,p in enumerate(('P1','P2')):
            self.edges.append(dict(id='E'+str(i),**{'from':p,'to':'C'},from_version=self.records[0 if i==0 else 2]['content_version'],to_version='4'*64,state='ESTABLISHED COMPATIBLE INTERFACE',slot_binding=dict(slot='bound',target='support' if i==0 else 'expectation',lower='0',upper='1',units='source-local',qualification='all admissible models' if i==0 else 'declared prior average')))
    def attached(self,records=None,edges=None):
        records=copy.deepcopy(self.records if records is None else records)
        nav=compile_navigation(records,self.edges if edges is None else edges)
        for r in records:
            if r['id'] in nav:r['interface_navigation']=nav[r['id']]
        return {r['id']:r for r in records}
    def test_common_consumer_preserves_distinct_task_qualifications(self):
        records=self.attached();nav=peers(records,'P1');self.assertEqual(nav['relation'],RELATION)
        peer=nav['candidates'][0];self.assertEqual(peer['binding']['target'],'expectation');self.assertEqual(peer['binding']['qualification'],'declared prior average')
        self.assertEqual(peers(records,'R1')['routes'][0]['provider'],'P1')
        self.assertEqual(peers(records,'C')['total_candidates'],2)
        self.assertEqual(len(self.edges),2,'No provider-to-provider edge created')
    def test_consumer_parent_exposes_all_providers_without_inheriting_their_claims(self):
        records=copy.deepcopy(self.records);records[-1]['parents']=['R2'];records.append(dict(id='R2',content_version='6'*64,title='consumer parent',parents=[],contract={}))
        attached=self.attached(records);nav=peers(attached,'R2')
        self.assertEqual(nav['total_candidates'],2);self.assertEqual(nav['routes'],[])
        self.assertEqual(nav['consumers'][0]['consumer'],'C')
        attached['C']['content_version']='7'*64
        with self.assertRaisesRegex(ValueError,'Stale'):peers(attached,'R2')
    def test_packet_mapping_deduplication_keeps_conflicting_assertions_visible(self):
        records=self.attached();nav=records['C']['interface_navigation']
        compact=packet_navigation(nav,self.edges)
        self.assertTrue(all('binding_ref' in item for item in compact['bindings']))
        self.assertTrue(all('binding' in item for item in nav['bindings']),'Canonical bindings must stay complete')
        edges=copy.deepcopy(self.edges);edges[0]['slot_binding']['upper']='different assertion'
        conflict=packet_navigation(nav,edges)
        self.assertIn('binding',conflict['bindings'][0])
        self.assertNotIn('binding_ref',conflict['bindings'][0])
    def test_unproved_analogy_is_not_a_typed_provider(self):
        for state in ('CANDIDATE CONNECTION','INCOMPATIBLE ASSUMPTIONS','PROVEN LOGICAL DEPENDENCY','REFUTED TRANSFER'):
            edges=copy.deepcopy(self.edges);edges[0]['state']=state
            with self.assertRaisesRegex(ValueError,'established compatible'):compile_navigation(self.records,edges)
    def test_stale_mapping_fails_instead_of_borrowing_old_conditions(self):
        edges=copy.deepcopy(self.edges);edges[0]['from_version']='x'*64
        with self.assertRaisesRegex(ValueError,'Stale'):compile_navigation(self.records,edges)
        records=self.attached();records['P2']['content_version']='0'*64
        with self.assertRaisesRegex(ValueError,'Stale'):peers(records,'P1')
    def test_slot_must_exist_and_be_fully_qualified(self):
        edges=copy.deepcopy(self.edges);edges[0]['slot_binding']['slot']='imagined'
        with self.assertRaisesRegex(ValueError,'Unknown'):compile_navigation(self.records,edges)
        for field in ('target','lower','upper','units','qualification'):
            edges=copy.deepcopy(self.edges);del edges[0]['slot_binding'][field]
            with self.assertRaisesRegex(ValueError,'explicit'):compile_navigation(self.records,edges)
    def test_same_target_different_slot_is_not_a_peer(self):
        records=copy.deepcopy(self.records);records[-1]['contract']['input_slots'].append({'id':'cost','required_binding_fields':['target','lower','upper','units','qualification']})
        edges=copy.deepcopy(self.edges);edges[1]['slot_binding']['slot']='cost'
        self.assertEqual(peers(self.attached(records,edges),'P1')['candidates'],[])
    def test_old_unannotated_edges_remain_uninterpreted(self):
        edges=copy.deepcopy(self.edges);del edges[1]['slot_binding']
        records=self.attached(edges=edges);self.assertEqual(peers(records,'P1')['candidates'],[]);self.assertEqual(peers(records,'P2')['total_candidates'],0)
    def test_pagination_preserves_all_providers_without_quadratic_storage(self):
        records=copy.deepcopy(self.records);edges=copy.deepcopy(self.edges)
        for i in range(100):
            p=dict(id='extra'+str(i),content_version='5'*64,title='extra bound',parents=[],contract={});records.append(p)
            edges.append(dict(edges[0],id='extra-edge'+str(i),**{'from':p['id']},from_version=p['content_version']))
        attached=self.attached(records,edges);nav=compile_navigation(records,edges)
        self.assertEqual(sum(len(x['bindings']) for x in nav.values()),len(edges))
        rows=[];offset=0
        while True:
            result=peers(attached,'C',offset=offset,limit=7);rows.extend(result['candidates'])
            if result['next_offset'] is None:break
            offset=result['next_offset']
        self.assertEqual(len(rows),len(edges));self.assertEqual(len({x['provider'] for x in rows}),len(edges))
if __name__=='__main__':unittest.main()
