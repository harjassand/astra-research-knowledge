"""Independent scalar-only bounded-projection receiver audit.

Hidden coordinates occur only in imported test fixtures and validation. All
end-to-end reported means below are emulated, not sampled; shot budgets remain
unexecuted. Binary adapter refusal does not run astronomical sample loops.
"""
from fractions import Fraction as F
import itertools
import unittest

from bounded_projection_receiver import BoundedProjectionReceiver
from receiver import BinaryMeanAdapter, TerminalFailure, BudgetRefused
from test_receiver import rank2, rank3, ValidatedMeanEmulator, HiddenOracleForAuditOnly, dot


class AuditedProjectionReceiver(BoundedProjectionReceiver):
    """Inspect only scalar-data optimization, never the fixture hidden oracle."""
    def _solve(self,k,work):
        c,gap=super()._solve(k,work)
        assert sum(map(abs,c))<=self.B
        assert all(x.denominator & (x.denominator-1)==0 for x in c)
        gradient=[2*(sum((a*b for a,b in zip(row,c)),F(0))-ki) for row,ki in zip(self.A,k)]
        exact_gap=sum((a*b for a,b in zip(gradient,c)),F(0))+self.B*max(map(abs,gradient))
        assert gap==exact_gap
        assert gap<=self.B*self.B*self.alpha
        return c,gap


class BoundedProjectionReceiverTests(unittest.TestCase):
    def run_fixture(self, oracle, tasks, minimum_dictionary, adjoints=None):
        H=4;epsilon=F(1,50)
        # Verify supplied adjoints, including the nonselfadjoint rotation fixture.
        adjoints=adjoints or {a:a for a in oracle.operators}
        for label,matrix in oracle.operators.items():
            self.assertEqual(tuple(map(tuple,oracle.operators[adjoints[label]])),tuple(zip(*matrix)))
            columns=tuple(zip(*matrix))
            for i in range(len(columns)):
                for j in range(len(columns)):
                    self.assertEqual(dot(columns[i],columns[j]),F(i==j))
        adapter=ValidatedMeanEmulator(oracle)
        receiver=AuditedProjectionReceiver(alphabet=tuple(oracle.operators),H=H,
            epsilon=epsilon,delta=F(1,100),adjoints=adjoints,adapter=adapter)
        for word in tasks:
            result=receiver.request(word)
            truth=oracle.mean('gram',((),word))
            self.assertLessEqual(abs(result['value']-truth),result['certificate'])
            self.assertLessEqual(result['certificate'],epsilon)
        self.assertGreaterEqual(result['dictionary_size'],minimum_dictionary,'fixture must force real retention')
        count=len(adapter.calls)
        for word in tasks:
            result=receiver.request(word)
            self.assertLessEqual(abs(result['value']-oracle.mean('gram',((),word))),result['certificate'])
        self.assertEqual(count,len(adapter.calls),'replay must not reacquire')
        new=next(w for w in itertools.product(tuple(oracle.operators),repeat=H) if w not in tasks)
        result=receiver.request(new)
        self.assertLessEqual(abs(result['value']-oracle.mean('gram',((),new))),result['certificate'])
        self.assertEqual(count,len(adapter.calls),'full-rank fixture must source-free answer a new task')
        self.assertEqual(len(receiver.words),len(set(receiver.words)))
        self.assertTrue(all(len(w)<=H for w in receiver.words))
        jobs=[(c[5],c[0],c[1]) for c in adapter.calls]
        self.assertEqual(len(jobs),len(set(jobs)),'pair/precision cache must reuse an acquired mean')
        self.assertTrue(all(c[0]=='gram' for c in adapter.calls),'no hidden readout/vector source')
        epoch_shots={}
        for c in adapter.calls:
            self.assertLessEqual(abs(c[6]-c[7]),c[2])
            epoch_shots.setdefault(c[5],set()).add(c[4])
        self.assertTrue(all(len(s)==1 for s in epoch_shots.values()))
        self.assertEqual(adapter.executed_episodes,0)
        self.assertLessEqual(sum((c[3] for c in adapter.calls),F(0)),receiver.beta)
        self.assertTrue(all(x['gap']<=x['delta'] for x in receiver.optimizer_log))
        self.assertGreater(adapter.theoretical_unexecuted_shots,0)
        print('\nBOUNDED PROJECTION AUDIT: rank',len(oracle.seed),'; dictionary',len(receiver.words),
              '; validated unsampled means',len(adapter.calls),'; theoretical unexecuted episodes',
              adapter.theoretical_unexecuted_shots,'; 0 physical episodes')

    def test_rank2_noncommuting_expansion_and_reuse(self):
        oracle=rank2()
        self.assertNotEqual(oracle.state(('a','b')),oracle.state(('b','a')))
        self.run_fixture(oracle,[(),('b','a','b'),('b','a','a','b'),('a','b','a','b')],2)

    def test_rank3_noncommuting_expansion_and_reuse(self):
        oracle=rank3()
        self.assertNotEqual(oracle.state(('a','b')),oracle.state(('b','a')))
        self.run_fixture(oracle,[(),('b','a','b'),('b','a','a','b'),('b','a','c','b')],3)

    def test_near_collinear_words_with_real_adjoint_rotation(self):
        t=F(1,10**12);c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
        oracle=HiddenOracleForAuditOnly(
            {'r':((c,-s),(s,c)),'R':((c,s),(-s,c)),'b':((F(0),F(1)),(F(1),F(0)))},
            [1,0],{'x':[1,0]})
        determinant=F(1)-oracle.mean('gram',((),('r',)))**2
        self.assertGreater(determinant,0)
        self.assertLess(determinant,F(1,10**23))
        self.run_fixture(oracle,[(),('b','r','b','r'),('r','b','r','b')],2,
                         adjoints={'r':'R','R':'r','b':'b'})
        # End-to-end discovery need not retain this near-duplicate pair;
        # bounded_projection_stress.py separately tests an imposed near-collinear dictionary.
        print('Reachable near-collinear Gram determinant:',determinant)

    def test_unexpected_source_exception_latches(self):
        calls=[]
        def source(kind,key):
            calls.append((kind,key));raise RuntimeError('synthetic source unavailable')
        adapter=BinaryMeanAdapter(source)
        receiver=BoundedProjectionReceiver(alphabet=('a',),H=1,epsilon=F(1),delta=F(1,100),
            adjoints={'a':'a'},adapter=adapter)
        with self.assertRaises((TerminalFailure,RuntimeError)):receiver.request(('a',))
        with self.assertRaises(TerminalFailure):receiver.request(())
        self.assertEqual(len(calls),1)

    def test_real_binary_calibration_refusal_latches(self):
        calls=[]
        def source(kind,key):calls.append((kind,key));return 1
        adapter=BinaryMeanAdapter(source,max_total_episodes=10)
        receiver=BoundedProjectionReceiver(alphabet=('a',),H=2,epsilon=F(1,4),delta=F(1,100),
            adjoints={'a':'a'},adapter=adapter)
        with self.assertRaises(BudgetRefused):receiver.request(('a',))
        self.assertEqual(calls,[])
        self.assertEqual(adapter.actual_episodes,0)
        with self.assertRaises(TerminalFailure):receiver.request(())
        self.assertEqual(calls,[])

    def test_bad_psd_latches(self):
        class BadData:
            def __init__(self):self.calls=0
            def estimate(self,kind,key,alpha,beta_job,shots,epoch):
                self.calls+=1
                return F(-1) if key[0]==key[1] else F(0)
        adapter=BadData()
        receiver=BoundedProjectionReceiver(alphabet=('a',),H=2,epsilon=F(1,4),delta=F(1,100),
            adjoints={'a':'a'},adapter=adapter)
        with self.assertRaises(TerminalFailure):receiver.request(('a',))
        count=adapter.calls
        with self.assertRaises(TerminalFailure):receiver.request(())
        self.assertEqual(count,adapter.calls)

    def test_rounded_fw_budget_refusal_latches(self):
        oracle=rank2();adapter=ValidatedMeanEmulator(oracle)
        receiver=BoundedProjectionReceiver(alphabet=tuple(oracle.operators),H=3,epsilon=F(1,50),delta=F(1,100),
            adjoints={'a':'a','b':'b'},adapter=adapter,max_fw_iterations=0,use_small_proposals=False)
        with self.assertRaises(BudgetRefused):receiver.request(('b','a','b'))
        count=len(adapter.calls)
        with self.assertRaises(TerminalFailure):receiver.request(())
        self.assertEqual(count,len(adapter.calls))


if __name__=='__main__':unittest.main(verbosity=2)
