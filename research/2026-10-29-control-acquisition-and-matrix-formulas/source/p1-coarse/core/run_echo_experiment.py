"""Synthetic acquisition + exact certificates; no physical device claimed.
The learner gets only calibrated scalar intervals. Hidden matrices are used
by the instrument simulator and a separate exact truth checker.
"""
from fractions import Fraction as F
from pathlib import Path
import itertools, json, random, time
from echo_compiler import EchoCompiler, Interval, propose_maps, matvec, dot
from uniform_certificate import uniform_certificate, psd, diagonal, sub

ROOT = Path(__file__).resolve().parents[1]

def dumpable(x):
    if isinstance(x, F):
        return {'rational': str(x), 'float': float(x)}
    if isinstance(x, Interval):
        return {'lo': dumpable(x.lo), 'hi': dumpable(x.hi)}
    if isinstance(x, dict):
        return {str(k): dumpable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [dumpable(v) for v in x]
    return x

def source(d=12, leakage=F(1, 1000), slow=False):
    blocks = [
        [[F(11,20), F(1,5), 0], [F(1,5), F(9,20), F(1,10)],
         [0, F(1,10), F(1,2)]],
        [[F(13,20), 0, F(1,5)], [0, F(11,20), F(-1,10)],
         [F(1,5), F(-1,10), F(7,20)]]]
    maps = []
    for i in range(2):
        a = [[F(0) for _ in range(d)] for _ in range(d)]
        for j in range(3):
            for k in range(3): a[j][k] = F(blocks[i][j][k])
        for j in range(3, d):
            a[j][j] = F(9999, 10000) if slow else F(3,5)+F(j%3,100)
            # Slow tails must obey the same actual contraction test.
            a[(j+i)%3][j] = a[j][(j+i)%3] = leakage*((-1)**(j+i))
        assert psd(a)
        assert psd(sub(diagonal([F(1)]*d), a))
        maps.append(a)
    return maps, [F(1)]+[F(0)]*(d-1)

def truth(maps, b, word):
    v = b
    for i in word: v = matvec(maps[i], v)
    return dot(b, v)

class Instrument:
    def __init__(self, maps, b, eta=F(1,10**10)):
        self.maps, self.b, self.eta = maps, b, eta
        self.gain, self.offset = F(7,5), F(-3,10)
        self.calls, self.operations = 0, 0
        self.raw = []
    def report(self, value, label):
        # Correlated deterministic bounded errors; repetitions do not reduce eta.
        error = self.eta*F(((self.calls*11+3)%19)-9, 9)
        y = self.gain*value+self.offset+error
        self.raw.append({'label':label, 'report':str(y), 'error_bound':str(self.eta)})
        self.calls += 1
        return y
    def calibrate(self):
        y0 = self.report(F(0), 'standard_zero')
        y1 = self.report(F(1), 'standard_one')
        self.beta = Interval(y0-self.eta, y0+self.eta)
        self.alpha = Interval(y1-y0-2*self.eta, y1-y0+2*self.eta)
        assert self.alpha.lo > 0
    def query(self, word):
        self.operations += len(word)
        y = self.report(truth(self.maps,self.b,word),list(word))
        numer = [y-self.eta-self.beta.hi, y+self.eta-self.beta.lo]
        values = [n/a for n in numer for a in [self.alpha.lo,self.alpha.hi]]
        return Interval(min(values),max(values))

def run_fixture(name, leakage, slow=False, eta=F(1,10**10), shrink=1.0):
    hidden, b = source(leakage=leakage, slow=slow)
    dictionary = [(),(0,),(1,)]
    inst = Instrument(hidden,b,eta)
    inst.calibrate()
    words = sorted(EchoCompiler.required_words(dictionary,2),key=lambda w:(len(w),w))
    records = {w:inst.query(w) for w in words}
    for w, interval in records.items(): assert interval.contains(truth(hidden,b,w))
    proposed = propose_maps(dictionary,2,records,shrink=shrink)
    learner = EchoCompiler(dictionary,2,records,proposed)
    uniform = uniform_certificate(learner, rho=F(9,10))
    tasks = list(itertools.product(range(2),repeat=6))
    rng = random.Random(739)
    tasks += [tuple(rng.randrange(2) for _ in range(h)) for h in [0,1,2,12,24,48]]
    checked, selected = [], []
    for w in tasks:
        cert = learner.certificate(w)
        actual = truth(hidden,b,w)
        assert cert['interval'].contains(actual), (name,w,actual,cert['interval'])
        assert abs(actual-cert['corrected_prediction'].center) <= uniform['all_word_total_bound']
        entry = {'word':w, 'truth':actual, 'certificate':cert,
                 'actual_corrected_error':abs(actual-cert['corrected_prediction'].center),
                 'actual_uncorrected_error':abs(actual-cert['uncorrected_prediction'].center)}
        checked.append(entry)
        if len(w) in [0,1,2,12,24,48] or w == (0,1,0,1,0,1): selected.append(entry)
    six = checked[:64]
    choice = max(six,key=lambda x:x['certificate']['interval'].lo)
    certified_regret = max(x['certificate']['interval'].hi for x in six)-choice['certificate']['interval'].lo
    actual_regret = max(x['truth'] for x in six)-choice['truth']
    assert actual_regret <= certified_regret
    return {'fixture':name, 'hidden_dimension_checker_only':len(b),
            'dictionary':dictionary, 'calibration_standards':2,
            'source_readings':len(words), 'total_readings':inst.calls,
            'native_primitive_executions':inst.operations,
            'resets':len(words), 'maximum_query_length':max(map(len,words)),
            'adc_absolute_error':eta, 'raw_records':inst.raw,
            'decoded_records': [{'word':w,'interval':records[w]} for w in words],
            'maps':proposed, 'uniform_certificate':uniform,
            'checked_task_count':len(tasks), 'selected_tasks':selected,
            'maximum_actual_error':max(x['actual_corrected_error'] for x in checked),
            'maximum_task_interval_radius':max(x['certificate']['interval'].radius for x in checked),
            'finite_menu_selection':{'menu_size':64,'horizon':6,'chosen_word':choice['word'],
                                     'certified_regret':certified_regret,'actual_regret':actual_regret},
            'scope':'synthetic exact-rational acquisition and checking; no physical runtime advantage'}

def main():
    t0=time.perf_counter()
    fixtures=[run_fixture('weak_hidden_modes',F(1,1000)),
              run_fixture('very_slow_hidden_modes',F(1,10000),slow=True),
              run_fixture('biased_proposal_signed_correction',F(1,1000),shrink=0.995),
              run_fixture('higher_measurement_error',F(1,1000),eta=F(1,10**6))]
    result={'fixtures':fixtures,'wall_seconds':time.perf_counter()-t0,
            'all_exact_containment_checks_passed':True}
    out=ROOT/'results'/'ECHO_EXPERIMENT.json'
    out.write_text(json.dumps(dumpable(result),indent=2))
    for f in fixtures:
        print(f['fixture'], 'readings',f['total_readings'],'operations',f['native_primitive_executions'],
              'all-word-error',float(f['uniform_certificate']['all_word_total_bound']),
              'max-observed-error',float(f['maximum_actual_error']),
              'regret',float(f['finite_menu_selection']['certified_regret']))
    print('seconds',result['wall_seconds'],'saved',out)

if __name__=='__main__':main()
