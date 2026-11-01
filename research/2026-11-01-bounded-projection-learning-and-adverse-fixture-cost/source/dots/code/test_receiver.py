"""Audits with hidden vectors confined to this file; not physical experiments.

ValidatedMeanEmulator does NOT execute one-bit shots. Its budget counter is the
unexecuted theoretical number requested by the calibrated receiver.
"""
from fractions import Fraction as F
import itertools
import unittest

from receiver import Receiver, TerminalFailure, BudgetRefused, BinaryMeanAdapter, required_shots


def mv(a, x):
    return tuple(sum((u*v for u,v in zip(row,x)), F(0)) for row in a)


def dot(x, y):
    return sum((u*v for u,v in zip(x,y)), F(0))


def diag(xs):
    return tuple(tuple(F(x) if i == j else F(0) for j in range(len(xs))) for i,x in enumerate(xs))


class HiddenOracleForAuditOnly:
    def __init__(self, operators, seed, readouts):
        self.operators = operators
        self.seed = tuple(map(F, seed))
        self.readouts = {k: tuple(map(F,v)) for k,v in readouts.items()}
        self.states = {(): self.seed}

    def state(self, word):
        if word not in self.states:
            self.states[word] = mv(self.operators[word[-1]], self.state(word[:-1]))
        return self.states[word]

    def mean(self, kind, key):
        if kind == 'gram':
            return dot(self.state(key[0]), self.state(key[1]))
        if kind == 'readout':
            return dot(self.readouts[key[0]], self.state(key[1]))
        raise AssertionError(kind)


class ValidatedMeanEmulator:
    """Artificial validated means, NOT empirical means or executed episodes."""
    calibration_mode = 'validated_mean_emulator_no_samples'
    def __init__(self, oracle, perturb=True):
        self.oracle = oracle
        self.perturb = perturb
        self.calls = []
        self.theoretical_unexecuted_shots = 0
        self.executed_episodes = 0

    def estimate(self, kind, key, alpha, beta_job, shots, epoch):
        truth = self.oracle.mean(kind, key)
        error = (alpha/F(2)) * (1 if len(self.calls)%2 else -1) if self.perturb else F(0)
        target = min(F(1), max(F(-1), truth + error))
        # Return an attainable n-shot binary mean on the common-denominator
        # grid, but do not draw or claim to have drawn those n reports.
        j = ((target+1)*shots/2).__floor__()
        answer = F(2*j-shots,shots)
        assert abs(answer-truth) <= alpha
        assert isinstance(answer, F)
        assert shots > 0 and 0 < beta_job < 1
        self.calls.append((kind,key,alpha,beta_job,shots,epoch,answer,truth))
        self.theoretical_unexecuted_shots += shots
        return answer


def rank2():
    return HiddenOracleForAuditOnly(
        {'a': diag([1,-1]), 'b': ((F(3,5), F(4,5)), (F(4,5),F(-3,5)))},
        [1,0], {'x':[1,0], 'y':[0,1]})


def rank3():
    n = (1,2,2)
    reflection = tuple(tuple(F(int(i==j))-F(2*n[i]*n[j],9) for j in range(3)) for i in range(3))
    return HiddenOracleForAuditOnly(
        {'a':diag([1,-1,1]), 'b':reflection, 'c':diag([1,1,-1])},
        [1,0,0], {'x':[1,0,0], 'y':[0,1,0], 'z':[0,0,1]})


class ReceiverAuditTests(unittest.TestCase):
    def run_system(self, oracle, requests, H=3, epsilon=F(1,4)):
        # Every fixture primitive is orthogonal, hence a contraction exactly.
        for matrix in oracle.operators.values():
            columns = tuple(zip(*matrix))
            for i in range(len(columns)):
                for j in range(len(columns)):
                    self.assertEqual(dot(columns[i],columns[j]),F(int(i==j)))
        adapter = ValidatedMeanEmulator(oracle)
        receiver = Receiver(alphabet=tuple(oracle.operators), H=H, epsilon=epsilon,
                            delta=F(1,100), readouts=tuple(oracle.readouts), adapter=adapter)
        for word in requests:
            for readout in oracle.readouts:
                result = receiver.request(word,readout)
                truth = oracle.mean('readout',(readout,word))
                self.assertLessEqual(abs(result['value']-truth), result['certificate'])
                self.assertLessEqual(result['certificate'],epsilon)
        calls = len(adapter.calls)
        # Exactly repeated requests must be certified from retained moments.
        for word in requests:
            for readout in oracle.readouts:
                result = receiver.request(word,readout)
                self.assertLessEqual(abs(result['value']-oracle.mean('readout',(readout,word))),result['certificate'])
        self.assertEqual(calls,len(adapter.calls))
        novel = next(w for w in itertools.product(tuple(oracle.operators),repeat=H) if w not in requests)
        for readout in oracle.readouts:
            result=receiver.request(novel,readout)
            self.assertLessEqual(abs(result['value']-oracle.mean('readout',(readout,novel))),result['certificate'])
        self.assertEqual(calls,len(adapter.calls), 'A new task should reuse the learned full-rank fixture model')
        self.assertEqual(adapter.executed_episodes,0)
        self.assertEqual(len(receiver.words),len(set(receiver.words)))
        self.assertTrue(all(len(w)<=H for w in receiver.words))
        jobs=[(c[5],c[0],c[1]) for c in adapter.calls]
        self.assertEqual(len(jobs),len(set(jobs)), 'pair/precision cache must not resample an identical job')
        epoch_shots={}
        for c in adapter.calls:
            epoch_shots.setdefault(c[5],set()).add(c[4])
        self.assertTrue(all(len(v)==1 for v in epoch_shots.values()), 'one common sample denominator per precision epoch')
        self.assertLessEqual(sum((c[3] for c in adapter.calls),F(0)),receiver.beta)
        self.assertEqual(receiver.acquisition['actual_episodes'],0)
        self.assertGreater(adapter.theoretical_unexecuted_shots,0)
        print('\nAUDIT',len(oracle.seed),'dimensions;',len(adapter.calls),'validated means;',
              adapter.theoretical_unexecuted_shots,'theoretical unexecuted episodes; 0 physically executed')
        return receiver,adapter

    def test_noncommuting_rank2_validated_means_reuse(self):
        oracle = rank2()
        self.assertNotEqual(oracle.state(('a','b')),oracle.state(('b','a')))
        self.run_system(oracle,[(),('b',),('b','a'),('a','b','a'),('b','a','b')])

    def test_noncommuting_rank3_validated_means_reuse(self):
        oracle = rank3()
        self.assertNotEqual(oracle.state(('b','a')),oracle.state(('a','b')))
        self.run_system(oracle,[(),('b',),('b','a'),('b','c'),('b','a','b'),('c','b','a')])

    def test_nearly_singular_reachable_physical_gram(self):
        t=F(1,10**8)
        c=(1-t*t)/(1+t*t)
        s=2*t/(1+t*t)
        oracle=HiddenOracleForAuditOnly(
            {'r':((c,-s),(s,c)), 'b':((F(0),F(1)),(F(1),F(0)))},
            [1,0], {'x':[1,0], 'y':[0,1]})
        det=oracle.mean('gram',((),()))*oracle.mean('gram',(('r',),('r',)))-oracle.mean('gram',((),('r',)))**2
        self.assertGreater(det,0)
        self.assertLess(det,F(1,10**14))
        # The algorithm need not retain this near-duplicate pair: that is a feature.
        self.run_system(oracle,[('r',),('b',),('b','r'),('r','b','r')])
        print('Nearly singular reachable physical Gram determinant:',str(det))

    def test_actual_binary_adapter_small_synthetic_source(self):
        # Genuine n-report loop on a deterministic +1 synthetic scalar source;
        # this unit-tests calibration plumbing, not physical apparatus.
        calls=[]
        def report(kind,key):
            calls.append((kind,key))
            return 1
        adapter=BinaryMeanAdapter(report,max_total_episodes=1000)
        alpha=F(1,2); beta=F(1,10)
        n=required_shots(alpha,beta)
        value=adapter.estimate('gram',((),('a',)),alpha,beta,n,1)
        self.assertEqual(value,F(1))
        self.assertEqual(len(calls),n)
        self.assertEqual(adapter.actual_episodes,n)
        self.assertEqual(adapter.actual_descriptor_controls,n)
        print('Binary calibration plumbing:',n,'synthetic deterministic reports; no physical experiment')

    def test_end_to_end_binary_calibration_explicitly_budget_refused(self):
        calls=[]
        def report(kind,key):
            calls.append((kind,key)); return 1
        adapter=BinaryMeanAdapter(report,max_total_episodes=10)
        receiver=Receiver(alphabet=('a',),H=2,epsilon=F(1,4),delta=F(1,100),readouts=('x',),adapter=adapter)
        with self.assertRaises(BudgetRefused): receiver.request(('a',),'x')
        self.assertEqual(calls,[])
        self.assertEqual(receiver.acquisition['actual_episodes'],0)
        self.assertGreater(receiver.acquisition['theoretical_required_episodes'],10)
        self.assertIsNotNone(receiver.failed)
        with self.assertRaises(TerminalFailure): receiver.request((),'x')
        self.assertEqual(calls,[])

    def test_unexpected_source_error_latches(self):
        calls=[]
        def report(kind,key):
            calls.append((kind,key)); raise RuntimeError('synthetic source unavailable')
        adapter=BinaryMeanAdapter(report)
        receiver=Receiver(alphabet=('a',),H=1,epsilon=F(1),delta=F(1,100),readouts=('x',),adapter=adapter)
        with self.assertRaises((TerminalFailure,RuntimeError)): receiver.request(('a',),'x')
        self.assertIsNotNone(receiver.failed)
        with self.assertRaises(TerminalFailure): receiver.request((),'x')
        self.assertEqual(len(calls),1)

    def test_bad_data_failure_latches(self):
        class BadData:
            def __init__(self): self.calls=0
            def estimate(self,kind,key,alpha,beta_job,shots,epoch):
                self.calls+=1
                return F(-1) if kind=='gram' and key[0]==key[1] else F(0)
        bad=BadData()
        # Construction may initialize lazily or eagerly; either is permitted.
        try:
            receiver=Receiver(alphabet=('a',),H=2,epsilon=F(1,4),delta=F(1,100),readouts=('x',),adapter=bad)
        except TerminalFailure:
            self.fail('Receiver must preserve a failed instance for terminal-latch testing; initialize lazily or latch constructor failures')
        with self.assertRaises(TerminalFailure): receiver.request(('a',),'x')
        count=bad.calls
        with self.assertRaises(TerminalFailure): receiver.request((),'x')
        self.assertEqual(count,bad.calls)


if __name__=='__main__':
    unittest.main(verbosity=2)
