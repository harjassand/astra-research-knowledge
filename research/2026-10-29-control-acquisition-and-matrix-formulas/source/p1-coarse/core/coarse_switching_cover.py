"""Paid coarse survival data certify a finite cover of every switching word.

The private reversible source has a countable slow tail, norm one and infinite
mean lifetime. The learner sees only chosen controls and live/absorbed reports.
Fixed balanced control tapes share prefix observations; no live label resets a
hidden state. Statistical acceptance uses exact rational KL endpoints.
"""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import json, random, sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'branches' / 'physical'))
from multiboundary_positive_events import binomial_interval


class PrivateInstrument:
    def __init__(self, seed=2026102904):
        self.rng = np.random.default_rng(seed)
        self.bits = random.Random(seed + 1)
        self.kernel = np.array([[[10, 2], [2, 2]], [[8, 1], [1, 2]]])

    def prepare(self, n):
        micro = self.rng.integers(0, 2, size=n)
        level = np.full(n, -1, dtype=np.int64)
        slow = np.flatnonzero(self.rng.integers(0, 1024, size=n) == 0)
        for j in slow:
            ell = 0
            while self.bits.getrandbits(1) == 0:
                ell += 1
            level[j] = ell
        return micro, level

    def step(self, micro, level, active, modes):
        # Exactly one physical application/report per member of active.
        activated = level[active] < 0
        for ell in np.unique(level[active][~activated]):
            positions = np.flatnonzero(level[active] == ell)
            bits = int(ell) + 4
            if bits <= 60:
                activated[positions] = self.rng.integers(0, 1 << bits,
                                                       size=len(positions)) == 0
            else:
                activated[positions] = [self.bits.getrandbits(bits) == 0
                                         for _ in positions]
        changed = active[activated]
        mode = modes[activated]
        row = self.kernel[mode, micro[changed]]
        draw = self.rng.integers(0, 16, size=len(changed))
        survived_change = draw < row.sum(axis=1)
        micro[changed] = (draw >= row[:, 0]).astype(np.int64)
        live = np.ones(len(active), dtype=bool)
        live[activated] = survived_change
        return active[live]

    def repetitions(self, mode, n=8192, cap=32):
        micro, level = self.prepare(n)
        active = np.arange(n)
        survivors, steps = [n], 0
        for _ in range(cap):
            steps += len(active)
            active = self.step(micro, level, active,
                               np.full(len(active), mode, dtype=np.int64))
            survivors.append(len(active))
        assert steps == sum(survivors[:-1])
        return dict(mode=mode, trials=n, cap=cap, survivors_by_time=survivors,
                    primitive_applications=steps, coarse_observations=steps,
                    fresh_preparations=n)

    def balanced_tapes(self, depth=10, per_tape=512):
        n = (1 << depth)*per_tape
        tapes = np.arange(n, dtype=np.int64) % (1 << depth)
        micro, level = self.prepare(n)
        active = np.arange(n)
        records, survivors, steps = {}, [n], 0
        for h in range(1, depth + 1):
            steps += len(active)
            mode = (tapes[active] >> (depth-h)) & 1
            active = self.step(micro, level, active, mode)
            counts = np.bincount(tapes[active] >> (depth-h), minlength=1 << h)
            for index, count in enumerate(counts):
                records[format(index, '0%db' % h)] = dict(
                    assigned_trials=n >> h, survived=int(count))
            survivors.append(len(active))
        assert steps == sum(survivors[:-1])
        return dict(depth=depth, per_full_tape=per_tape, trials=n,
                    counts_by_prefix=records, survivors_by_depth=survivors,
                    primitive_applications=steps, coarse_observations=steps,
                    fresh_preparations=n,
                    assignment='Every depth-10 control tape has 512 independent fresh preparations. Dead trajectories count as zero for each longer assigned prefix.')


def exp_upper_minus(x):
    return 1/sum((F(x)**k/F(factorial(k)) for k in range(90)), F(0))


def infer_repetition_tail(receipts, target=F(1, 16)):
    candidates = []
    cap = min(r['cap'] for r in receipts)
    for m in range(1, cap//2+1):
        uppers = [binomial_interval(r['survivors_by_time'][2*m], r['trials'],
                                    F(12), upper_only=True)[1] for r in receipts]
        s = max(uppers)
        if s >= target:
            continue
        z, h = F(1), 0
        while z > target:
            z = s + F(m-1, m)*(z-s)
            h += 1
        candidates.append(dict(m=m, single_action_upper=str(s), half_length=h,
                               all_switching_length=2*h, tail_bound=str(z)))
    assert candidates
    chosen = min(candidates, key=lambda d: (d['all_switching_length'], d['m']))
    return dict(chosen=chosen, candidates=candidates,
                one_sided_tails=len(receipts)*(cap//2), tail_exponent=12,
                source_scope='Common reversible preparation, positive contractions, irreversible loss. No hidden rank or strict source norm cap.')


def infer_cover(receipt, target=F(1, 16)):
    cover, unresolved, stack = {}, [], ['0', '1']
    while stack:
        word = stack.pop(0)
        r = receipt['counts_by_prefix'][word]
        lo, hi = binomial_interval(r['survived'], r['assigned_trials'], F(18))
        if hi <= target:
            cover[word] = dict(kind='terminal', interval=[str(lo), str(hi)],
                               prediction='0', all_extension_bound=str(hi))
        elif hi-lo <= 2*target:
            cover[word] = dict(kind='branch', interval=[str(lo), str(hi)],
                               prediction=str((lo+hi)/2), error=str((hi-lo)/2))
            if len(word) < receipt['depth']:
                stack.extend([word+'0', word+'1'])
            else:
                unresolved.append(word)
        else:
            unresolved.append(word)
    assert not unresolved, unresolved
    for word, node in cover.items():
        if node['kind'] == 'branch':
            assert word+'0' in cover and word+'1' in cover
        assert len(word) <= receipt['depth']
    return dict(nodes=cover, all_word_error=str(target),
                maximum_prefix_length=max(map(len, cover)),
                terminal_nodes=sum(n['kind'] == 'terminal' for n in cover.values()),
                branch_nodes=sum(n['kind'] == 'branch' for n in cover.values()),
                interval_count=len(cover),
                potential_interval_count=len(receipt['counts_by_prefix']),
                tail_exponent=18,
                future_execution='Follow the selected controls through this finite prefix tree. At a terminal node return zero for every extension; at an exact branch word return the saved midpoint. Empty word is exactly one.')


def fast_probability(word, level=-1):
    # Private exact finite-block checker, never passed to infer_*.
    a = [[[F(10,16),F(2,16)],[F(2,16),F(2,16)]],
         [[F(8,16),F(1,16)],[F(1,16),F(2,16)]]]
    if level >= 0:
        e = F(1, 1 << (level+4))
        a = [[[e*c+F(i==j)*(1-e) for j,c in enumerate(row)]
              for i,row in enumerate(k)] for k in a]
    p = [F(1,2), F(1,2)]
    for control in word:
        k = a[int(control)]
        p = [sum(k[i][j]*p[j] for j in range(2)) for i in range(2)]
    return sum(p)


def hidden_check(cover, levels=8):
    omitted = F(1,1024*(1 << levels))
    maxima = F(0)
    for word, node in cover['nodes'].items():
        true_lo = F(1023,1024)*fast_probability(word)
        for ell in range(levels):
            true_lo += F(1,1024*(1 << (ell+1)))*fast_probability(word,ell)
        true_hi = true_lo+omitted
        lo,hi = map(F,node['interval'])
        assert lo <= true_lo <= true_hi <= hi
        if node['kind'] == 'terminal':
            assert true_hi <= F(cover['all_word_error'])
        else:
            pred = F(node['prediction'])
            maxima = max(maxima, abs(pred-true_lo), abs(pred-true_hi))
    return dict(verified_nodes=len(cover['nodes']), retained_slow_levels=levels,
                omitted_probability_upper=str(omitted),
                max_retained_word_error_upper=str(maxima),
                role='Private exact source checks, excluded from learner inputs. The all-word proof uses positivity and terminal-prefix coverage.')


def run(replay=False):
    raw_path = ROOT/'results'/'COARSE_SWITCHING_RAW_RECEIPTS.json'
    if replay:
        raw = json.loads(raw_path.read_text())
    else:
        instrument = PrivateInstrument()
        pure = [instrument.repetitions(i) for i in (0,1)]
        print('repetition acquisition complete', flush=True)
        tapes = instrument.balanced_tapes()
        raw = dict(repetitions=pure, balanced_tapes=tapes)
        raw_path.write_text(json.dumps(raw,indent=2)+'\n')
        print('balanced tape acquisition complete', flush=True)
    tail = infer_repetition_tail(raw['repetitions'])
    cover = infer_cover(raw['balanced_tapes'])
    failure = (tail['one_sided_tails']*exp_upper_minus(12)
               +2*cover['potential_interval_count']*exp_upper_minus(18))
    assert failure < F(1,1000)
    private = hidden_check(cover)
    costs = {key: sum(r[key] for r in raw['repetitions'])+raw['balanced_tapes'][key]
             for key in ('primitive_applications','coarse_observations','fresh_preparations')}
    output = dict(repetition_tail=tail, cover=cover, complete_costs=costs,
                  failure_probability_upper='1/1000', private_check=private,
                  scope='Executed integer-RNG software source, countably infinite live states, norm one. Fresh preparation of the common reversible distribution and exact live/absorbed reports are interface premises. No hidden labels enter inference.')
    (ROOT/'results'/'COARSE_SWITCHING_COVER.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(tail=tail['chosen'], costs=costs,
                         cover={k:v for k,v in cover.items() if k!='nodes'},
                         private_check=private),indent=2))


if __name__ == '__main__':
    run('--replay' in sys.argv)
