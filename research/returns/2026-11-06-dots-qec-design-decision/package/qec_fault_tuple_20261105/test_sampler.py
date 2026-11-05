"""Deterministic adversarial checks, not a performance or statistical pilot."""
import argparse
import bisect
import hashlib
import json
from pathlib import Path
import random
import time
import numpy as np
from exact_sampler import CertifiedPrefix, CountedBits, FaultTupleProposal, CircuitModel


def split(values, shape):
    return (np.asarray([v & ((1 << 64) - 1) for v in values], dtype=np.uint64).reshape(shape),
            np.asarray([v >> 64 for v in values], dtype=np.uint64).reshape(shape))


def prefix_tests():
    rng = random.Random(1300521)
    tested = bounds = fallbacks = 0
    for case in range(160):
        n, N, D = rng.choice([1, 2, 3, 7, 31, 128]), 64, 64
        special = [0, 1, (1 << 53) - 1, (1 << 53) + 1, (1 << 64) - 1,
                   1 << 64, (1 << 64) + 1, (1 << 127) - 1, (1 << 128) - 1]
        values = [rng.choice(special) if case % 3 else rng.getrandbits(rng.randrange(129))
                  for _ in range(n * N)]
        if case == 0:
            values = [0] * (n * N)
        lo, hi = split(values, (n, N))
        selector = CertifiedPrefix(lo, hi, D)
        distances = np.asarray([rng.randrange(D + 1) for _ in range(n)], dtype=np.int16)
        residue = rng.randrange(N)
        residues = (residue - distances) % N
        exact = []
        total = 0
        for x in range(n):
            total += values[x * N + int(residues[x])] << (D - int(distances[x]))
            exact.append(total)
        float_cdf, error = selector.enclosures(distances, residues)
        for x, true in enumerate(exact):
            lower = selector.lower_integer_bound(float_cdf[x], error)
            upper = selector.upper_integer_bound(float_cdf[x], error)
            assert lower <= true <= upper, (case, x, lower, true, upper)
            bounds += 1
        thresholds = {0, total, total + 1, max(0, total - 1)}
        for point in exact:
            thresholds.update([max(0, point - 1), point, point + 1])
        for _ in range(20):
            thresholds.add(rng.randrange(total + 10))
        for threshold in thresholds:
            selected = selector.select(threshold, distances, residue)
            expected = bisect.bisect_right(exact, threshold)
            if expected == n:
                expected = None
            assert selected == expected, (case, threshold, selected, expected)
            tested += 1
        fallbacks += selector.counters['exact_fallbacks']
    return {'adversarial_bucket_checks': tested, 'prefix_enclosure_checks': bounds,
            'exact_fallbacks_exercised': fallbacks}


class ScriptedBits:
    def __init__(self, values, edge_count):
        self.values = iter(values)
        self.edge_count = edge_count
    def below(self, n):
        value = next(self.values)
        assert 0 <= value < n, (value, n)
        return value
    def all_zero(self, k):
        assert k == 0
        return True
    def noise_bytes(self, n):
        assert n == 8 * self.edge_count
        # UINT64_MAX means every generated Bernoulli noise bit is zero.
        return b'\xff' * n


def tiny_proposal():
    p = FaultTupleProposal.__new__(FaultTupleProposal)
    p.N = p.D = p.qden = 64
    p.Q = 10
    p.edges = [(2, 0), (0, 1), (1, 3)]
    p.costs = [1, 1, 1]
    p.nd, p.nv = 2, 4
    p.left, p.right = {2}, {3}
    p.dl, p.dr = [1, 2, 0, 3], [2, 1, 3, 0]
    p.qnum = [1 << 54] * 3
    p.q = np.asarray(p.qnum, dtype=np.uint64)
    p.U = np.full((4, 64), 4 << p.Q, dtype=np.uint64)
    p.distance = np.array([[0, 1], [1, 0]], dtype=np.uint8)
    p.outgoing = [[(1, 1)], [(0, 1), (3, 2)]]
    p.starts = [(2, 0, 0), (0, 1, 1), (1, 0, 1), (1, 3, 2)]
    p.start_cdf = []
    total = 0
    for x, y, e in p.starts:
        score = 1 - p.dl[x]
        total += (p.qnum[e] << (1 + 3 - p.dl[x])) * int(p.U[y, score % 64])
        p.start_cdf.append(total)
    p.Znum = total
    values = []
    for x in range(2):
        for r in range(64):
            values.append(sum((p.qnum[e] << 1) * int(p.U[y, (r + 1) % 64])
                              for y, e in p.outgoing[x]))
    p.Jlo, p.Jhi = split(values, (2, 64))
    p.prefix = CertifiedPrefix(p.Jlo, p.Jhi, 64)
    p.force_exact = False
    p.G = {'edges': p.edges, 'costs': p.costs, 'left': [2], 'right': [3], 'internal_vertices': 2}
    p.model = CircuitModel(p.G)
    return p


def structural_tests():
    p = tiny_proposal()
    # First fault 2->0, second fault 0->1. A shared endpoint must be accepted.
    terminal = 1 << (p.Q + 128 - p.dr[0] - ((1 - p.dr[0]) % 64))
    result = p.trial(ScriptedBits([0, terminal, 0, 0], 3))
    assert result == (1, 'accepted', 2, 1, 1), result
    # First fault 0->1; next 1->0 is the same underlying edge in reverse.
    initial = p.start_cdf[0]
    residue = 0
    terminal = 1 << (p.Q + 128 - p.dr[1] - ((residue - p.dr[1]) % 64))
    preceding_x = p.prefix.integer(0, 63) << 63
    result = p.trial(ScriptedBits([initial, terminal + preceding_x, 0], 3))
    assert result[1] == 'repeated_edge' and result[2] == 2 and result[3] == 0, result
    # Canonical fault extraction has fixed left-to-right orientation and omits clean edges.
    assert p.fault_witness(np.array([1, 1, 0], dtype=np.uint8)) == ((2, 0, 0), (0, 1, 1))
    assert p.fault_witness(np.array([0, 1, 1], dtype=np.uint8)) == ((0, 1, 1), (1, 3, 2))
    return {'shared_endpoint_acceptance': True, 'reverse_underlying_edge_rejection': True,
            'ordered_oriented_fault_extraction': True}


def same_seed_tests(directory, shots):
    a = FaultTupleProposal(directory)
    b = FaultTupleProposal(directory, force_exact=True)
    ra, rb = CountedBits(202611051333), CountedBits(202611051333)
    outcomes = []
    for _ in range(shots):
        outcome_a, outcome_b = a.trial(ra), b.trial(rb)
        assert outcome_a == outcome_b, (outcome_a, outcome_b)
        assert ra.summary() == rb.summary()
        outcomes.append(outcome_a)
    return {'directory': str(directory), 'deterministic_trials': shots,
            'bitwise_same_outcomes_and_bit_counts': True,
            'outcome_digest': hashlib.sha256(json.dumps(outcomes).encode()).hexdigest(),
            'certified_selector': dict(a.prefix.counters),
            'exact_selector': dict(b.prefix.counters),
            'normalizer_exact': str(a.Z)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=Path, action='append', default=[])
    parser.add_argument('--differential-trials', type=int, default=256)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('sampler_unit_results.json'))
    args = parser.parse_args()
    start = time.perf_counter()
    result = {'scope': 'Deterministic correctness checks only, not an inference or speed pilot.',
              'prefix_tests': prefix_tests(), 'structural_tests': structural_tests(),
              'same_seed_tests': [same_seed_tests(d, args.differential_trials) for d in args.directory]}
    result['seconds'] = time.perf_counter() - start
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
