"""Exact ordered-distinct-fault sampler for a certified rational supersolution.

Float arithmetic proposes endpoint indices only; the original integer uniform
is certified against outward prefix enclosures, or an exact prefix is used.
Ideal independent fair bits give exact iid Bernoulli output. random.Random is
only a reproducible PRNG implementation and is not an iid proof. See SAMPLER.md.
"""
from __future__ import annotations
import argparse
import bisect
import hashlib
import json
import math
from pathlib import Path
import random
import resource
import sys
import time
from collections import Counter
from fractions import Fraction

import numpy as np
import pymatching

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'canonical_qec_circuit_gate_20261105'))
from tilted_pilot import CircuitModel
sys.path.insert(0, str(ROOT.parent / 'canonical_qec_witness_20261105'))
from confidence_fast import exact_cp


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


class CountedBits:
    """Unbiased discrete transforms, conditional on ideal getrandbits output."""
    def __init__(self, seed):
        self.source = random.Random(seed)
        self.bits = 0
        self.bit_calls = 0
        self.uniform_calls = 0
        self.uniform_rejections = 0
        self.noise_bits = 0
        self.thinning_bits = 0

    def getrandbits(self, k):
        assert k >= 0
        if not k:
            return 0
        self.bits += k
        self.bit_calls += 1
        return self.source.getrandbits(k)

    def below(self, n):
        if n <= 0:
            raise ValueError('Uniform range must be positive')
        self.uniform_calls += 1
        k = (n - 1).bit_length()
        while True:
            value = self.getrandbits(k)
            if value < n:
                return value
            self.uniform_rejections += 1

    def all_zero(self, k):
        """Short-circuit fair-bit thinning, with exact probability 2**(-k)."""
        while k:
            block = min(k, 64)
            self.thinning_bits += block
            if self.getrandbits(block):
                return False
            k -= block
        return True

    def noise_bytes(self, n):
        self.noise_bits += 8 * n
        return self.getrandbits(8 * n).to_bytes(n, 'little')

    def summary(self):
        return {k: v for k, v in vars(self).items() if k != 'source'}


class CertifiedPrefix:
    """O(n) float proposal, O(n) exact fallback, no persistent state CDF cache.

    For n <= 2**20, positive finite normal inputs formed from uint128 integers,
    and exact power-of-two scaling, 16(n+1)2**-53 times the computed total bounds
    every prefix error. See SAMPLER.md for the full error derivation. The integer
    threshold itself is never rounded for the final accept/reject decision.
    """
    def __init__(self, j_lo, j_hi, distance_cap):
        assert j_lo.dtype == np.uint64 and j_hi.dtype == np.uint64
        assert j_lo.shape == j_hi.shape and j_lo.ndim == 2
        self.lo, self.hi = j_lo, j_hi
        self.n, self.N = j_lo.shape
        self.D = int(distance_cap)
        if not 0 < self.n <= (1 << 20):
            raise ValueError('CDF error proof requires 0 < n <= 2**20')
        self.indices = np.arange(self.n)
        # Each uint64 conversion is correctly rounded; ldexp is exact here.
        self.j_float = j_lo.astype(np.float64) + np.ldexp(j_hi.astype(np.float64), 64)
        self.counters = Counter()
        if not np.isfinite(self.j_float).all():
            raise ValueError('J float representation is not finite')

    def integer(self, x, r):
        return int(self.lo[x, r]) | (int(self.hi[x, r]) << 64)

    def exact_select(self, threshold, distances, residues):
        prefix = 0
        for x in range(self.n):
            prefix += self.integer(x, int(residues[x])) << (self.D - int(distances[x]))
            if threshold < prefix:
                return x
        return None

    def enclosures(self, distances, residues):
        masses = np.ldexp(self.j_float[self.indices, residues], self.D - distances)
        cdf = np.cumsum(masses, dtype=np.float64)
        total = float(cdf[-1])
        if not math.isfinite(total):
            return None, None
        if total == 0.0:
            # Nonnegative integer inputs imply all masses are exactly zero.
            return cdf, 0.0
        factor = math.ldexp(float(16 * (self.n + 1)), -53)
        error = math.nextafter(factor * total, math.inf)
        return cdf, error

    @staticmethod
    def upper_integer_bound(prefix, error):
        # nextafter corrects possible downward rounding in prefix + error.
        return math.ceil(math.nextafter(float(prefix) + error, math.inf))

    @staticmethod
    def lower_integer_bound(prefix, error):
        # A negative lower bound is harmless. floor only makes it more strict.
        return math.floor(math.nextafter(float(prefix) - error, -math.inf))

    def select(self, threshold, distances, residue, force_exact=False):
        assert threshold >= 0
        distances = np.asarray(distances, dtype=np.int16)
        assert distances.shape == (self.n,)
        assert np.all((distances >= 0) & (distances <= self.D))
        residues = (residue - distances) % self.N
        self.counters['endpoint_draws'] += 1
        if force_exact:
            self.counters['forced_exact'] += 1
            return self.exact_select(threshold, distances, residues)
        cdf, error = self.enclosures(distances, residues)
        if cdf is not None:
            candidate = int(np.searchsorted(cdf, float(threshold), side='right'))
            prev = 0.0 if candidate == 0 else cdf[candidate - 1]
            lower_ok = candidate == 0 or threshold >= self.upper_integer_bound(prev, error)
            upper_ok = candidate == self.n or threshold < self.lower_integer_bound(cdf[candidate], error)
            if lower_ok and upper_ok:
                self.counters['float_certified'] += 1
                if candidate == self.n:
                    self.counters['float_certified_null'] += 1
                    return None
                return candidate
        self.counters['exact_fallbacks'] += 1
        return self.exact_select(threshold, distances, residues)


class FaultTupleProposal:
    def __init__(self, directory, force_exact=False):
        self.directory = Path(directory)
        self.meta = json.loads((self.directory / 'parameters.json').read_text())
        self.N = int(self.meta.get('N', self.meta.get('modulus', 64)))
        self.D = int(self.meta.get('D', self.meta.get('cut_distance', 64)))
        self.Q = int(self.meta.get('Q', self.meta.get('table_denominator_exponent', 52)))
        self.qden = int(self.meta.get('qden', self.meta.get('q_noise_denominator_exponent', 64)))
        if self.D != 64 or self.N != 64:
            raise ValueError('This audited implementation is scoped to N=D=64')
        if self.qden != 64:
            raise ValueError('Vectorized Bernoulli implementation requires qden=64')
        self.G = json.loads((self.directory / 'input_graph.json').read_text())
        self.edges = [tuple(map(int, edge)) for edge in self.G['edges']]
        self.costs = list(map(int, self.G['costs']))
        self.nd = int(self.G['internal_vertices'])
        self.nv = 1 + max(max(edge) for edge in self.edges)
        self.left, self.right = set(self.G['left']), set(self.G['right'])
        self.dl, self.dr = list(map(int, self.meta['dl'])), list(map(int, self.meta['dr']))
        self.qnum = list(map(int, self.meta['q_numerators']))
        assert len(self.qnum) == len(self.edges)
        assert all(0 <= q < (1 << self.qden) for q in self.qnum)
        assert all(c > 0 for c in self.costs)
        assert len(self.dl) == len(self.dr) == self.nv
        self.q = np.asarray(self.qnum, dtype=np.uint64)
        self.U = np.load(self.directory / 'U.npy', mmap_mode='r')
        self.distance = np.load(self.directory / 'distance.npy', mmap_mode='r')
        self.Jlo = np.load(self.directory / 'J_lo.npy', mmap_mode='r')
        self.Jhi = np.load(self.directory / 'J_hi.npy', mmap_mode='r')
        assert self.U.shape == (self.nv, self.N) and self.U.dtype == np.uint64
        assert self.distance.shape == (self.nd, self.nd) and self.distance.dtype == np.uint8
        assert self.Jlo.shape == (self.nd, self.N)
        self.prefix = CertifiedPrefix(self.Jlo, self.Jhi, self.D)
        self.force_exact = force_exact
        self.hashes = {name: sha256(self.directory / name) for name in
                       ['parameters.json', 'input_graph.json', 'U.npy', 'distance.npy', 'J_lo.npy', 'J_hi.npy']}
        expected = self.meta.get('sha256', self.meta.get('file_sha256', self.meta.get('hashes', {})))
        for name, digest in expected.items():
            actual = self.hashes.get(name)
            if actual is None:
                actual = sha256(self.directory / name)
            if actual != digest:
                raise ValueError(f'File hash mismatch: {name}')
        if self.meta.get('source_sha256') is not None:
            if self.hashes['input_graph.json'] != self.meta['source_sha256']:
                raise ValueError('Source graph hash mismatch')
        if max(self.dr[v] for v in range(self.nv) if v not in self.left) + self.N - 1 > self.Q + self.qden + self.D:
            raise ValueError('Terminal common denominator cannot represent every state exactly')
        self.model = CircuitModel(self.G)
        self.outgoing = [[] for _ in range(self.nd)]
        starts = []
        self.max_dl = max(self.dl)
        if 'dlmax' in self.meta:
            assert self.max_dl == self.meta['dlmax']
        for e, (u, v) in enumerate(self.edges):
            for x, y in ((u, v), (v, u)):
                if x not in self.right and y not in self.left:
                    starts.append((x, y, e))
                if x < self.nd and y not in self.left:
                    self.outgoing[x].append((y, e))
        self.starts, self.start_cdf = [], []
        total = 0
        for x, y, e in starts:
            score = self.costs[e] - self.dl[x]
            mass = (self.qnum[e] << (self.costs[e] + self.max_dl - self.dl[x])) * int(self.U[y, score % self.N])
            if mass:
                total += mass
                self.starts.append((x, y, e))
                self.start_cdf.append(total)
        self.Znum = total
        self.Z = Fraction(total, 1 << (self.qden + self.Q + self.max_dl))
        expected_z = self.meta.get('Z_exact', self.meta.get('Z'))
        if expected_z is not None:
            assert self.Z == Fraction(expected_z), (self.Z, expected_z)
        self.static_array_bytes = sum(a.nbytes for a in
            (self.q, self.U, self.distance, self.Jlo, self.Jhi, self.prefix.j_float, self.prefix.indices))

    def fault_witness(self, errors):
        """Extract orientation and faults from the fixed CircuitModel path."""
        path = self.model.witness(errors)
        if path is None:
            return None
        first_u, first_v = self.edges[path[0]]
        assert (first_u in self.left) != (first_v in self.left)
        x = first_u if first_u in self.left else first_v
        result = []
        for e in path:
            u, v = self.edges[e]
            assert x == u or x == v
            y = v if x == u else u
            if errors[e]:
                result.append((x, y, e))
            x = y
        assert x in self.right and result
        return tuple(result)

    def trial(self, rng):
        x, v, e = self.starts[bisect.bisect_right(self.start_cdf, rng.below(self.Znum))]
        score = self.costs[e] - self.dl[x]
        residue = score % self.N
        faults = [(x, v, e)]
        seen_edges = {e}
        steps = 1
        while True:
            denominator = int(self.U[v, residue]) << (self.qden + self.D)
            assert denominator > 0
            exponent = self.Q + self.qden + self.D - self.dr[v] - ((residue - self.dr[v]) % self.N)
            if exponent < 0:
                raise ValueError('Terminal numerator is not integral at configured denominator')
            terminal = 1 << exponent
            assert terminal <= denominator
            pick = rng.below(denominator)
            if pick < terminal:
                score -= self.dr[v]
                residue = score % self.N
                break
            pick -= terminal
            if v in self.right:
                return 0, 'null', steps, 0, score
            assert v < self.nd
            x = self.prefix.select(pick, self.distance[v], residue, self.force_exact)
            if x is None:
                return 0, 'null', steps, 0, score
            gap = int(self.distance[v, x])
            pre_residue = (residue - gap) % self.N
            j = self.prefix.integer(x, pre_residue)
            pick_edge = rng.below(j)
            chosen = None
            for y, edge in self.outgoing[x]:
                rr = (pre_residue + self.costs[edge]) % self.N
                mass = (self.qnum[edge] << self.costs[edge]) * int(self.U[y, rr])
                if pick_edge < mass:
                    chosen = (y, edge, rr)
                    break
                pick_edge -= mass
            assert chosen is not None, 'J is inconsistent with graph, q, costs, or U'
            y, e, residue = chosen
            score += self.costs[e] - gap
            steps += 1
            if e in seen_edges:
                return 0, 'repeated_edge', steps, 0, score
            seen_edges.add(e)
            faults.append((x, y, e))
            v = y
            assert steps <= len(self.edges)
        if score < 0:
            return 0, 'negative_score', steps, 0, score
        thin = score - residue
        assert thin >= 0 and thin % self.N == 0
        if not rng.all_zero(thin):
            return 0, 'fold_reject', steps, 0, score
        # Drawing and discarding tuple-edge noise is harmless; every other edge
        # is independent with exactly q_num/2**64, and tuple edges are forced 1.
        errors = (np.frombuffer(rng.noise_bytes(8 * len(self.edges)), dtype='<u8') < self.q).astype(np.uint8)
        errors[list(seen_edges)] = 1
        canonical = self.fault_witness(errors)
        if canonical is None:
            return 0, 'not_failure', steps, 1, score
        if canonical != tuple(faults):
            return 0, 'other_witness', steps, 1, score
        return 1, 'accepted', steps, 1, score


def run(directory, shots, seed, confidence=True, output=None, force_exact=False, progress=10000):
    if shots <= 0:
        raise ValueError('A fixed positive number of trials is required')
    started = time.perf_counter()
    proposal = FaultTupleProposal(directory, force_exact)
    setup_seconds = time.perf_counter() - started
    rng = CountedBits(seed)
    counts = Counter({k: 0 for k in ('null', 'repeated_edge', 'negative_score', 'fold_reject', 'not_failure', 'other_witness', 'accepted')})
    steps = decoders = maxsteps = 0
    maxscore = -10**100
    sample_started = time.perf_counter()
    for i in range(shots):
        value, kind, length, decoded, score = proposal.trial(rng)
        counts[kind] += 1
        steps += length
        decoders += decoded
        maxsteps = max(maxsteps, length)
        maxscore = max(maxscore, score)
        if progress and (i + 1) % progress == 0:
            print(json.dumps({'completed': i + 1, 'seconds': time.perf_counter() - sample_started}), flush=True)
    sample_seconds = time.perf_counter() - sample_started
    confidence_started = time.perf_counter()
    interval = None
    if confidence:
        lo, hi = exact_cp(counts['accepted'], shots, Fraction(1, 1000), bits=24)
        tv = Fraction(proposal.meta['conversion_TV_upper_exact'])
        lower, upper = max(Fraction(0), proposal.Z * lo - tv), min(Fraction(1), proposal.Z * hi + tv)
        interval = {
            'confidence': 0.999, 'acceptance_exact': [str(lo), str(hi)],
            'failure_probability_exact': [str(lower), str(upper)],
            'failure_probability_float': [float(lower), float(upper)],
            'includes_conversion_bias': True, 'finite_length_tail': 0,
            'alpha_exact': '1/1000', 'endpoint_denominator_bits': 24,
        }
    result = {
        'scope': 'Exact rational ordered-fault proposal and fixed-shot outward statistical interval under ideal independent fair bits; fixed circuit, independent-edge noise law, and frozen decoder only.',
        'randomness_caveat': 'Python random.Random is a reproducible Mersenne Twister PRNG, not a source or proof of ideal independent bits. IID and coverage claims are mathematical conditional claims.',
        'shots': shots, 'seed': seed, 'distance': proposal.directory.name,
        'counts': dict(counts), 'normalizer_exact': str(proposal.Z),
        'normalizer_float': float(proposal.Z),
        'point_estimate_rounded_model': float(proposal.Z * Fraction(counts['accepted'], shots)),
        'interval': interval,
        'mean_fault_steps': steps / shots, 'maximum_fault_steps_including_repeat': maxsteps,
        'maximum_terminal_or_rejection_score': maxscore, 'decoder_calls': decoders,
        'endpoint_selection': dict(proposal.prefix.counters), 'random_bits': rng.summary(),
        'setup_seconds': setup_seconds, 'sampling_seconds': sample_seconds,
        'confidence_seconds': time.perf_counter() - confidence_started,
        'total_seconds': time.perf_counter() - started,
        'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'static_array_bytes': proposal.static_array_bytes,
        'cdf_storage': 'One temporary O(internal_vertices) CDF; no vertex-by-residue-by-target CDF cache.',
        'force_exact_prefixes': force_exact,
        'implementation_sha256': sha256(__file__), 'input_sha256': proposal.hashes,
        'decoder_implementation_sha256': sha256(ROOT.parent / 'canonical_qec_circuit_gate_20261105' / 'tilted_pilot.py'),
        'dependency_sha256': {name: sha256(ROOT.parent / 'canonical_qec_witness_20261105' / name)
                              for name in ['sampler.py', 'confidence_fast.py', 'sampler_frozen_phenomenological.py']},
        'python_version': sys.version, 'numpy_version': np.__version__,
        'pymatching_version': pymatching.__version__,
    }
    if output is not None:
        Path(output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--shots', type=int, required=True)
    parser.add_argument('--seed', type=int, required=True)
    parser.add_argument('--no-confidence', action='store_true')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--force-exact-prefixes', action='store_true')
    parser.add_argument('--progress', type=int, default=10000)
    args = parser.parse_args()
    run(args.directory, args.shots, args.seed, not args.no_confidence,
        args.output, args.force_exact_prefixes, args.progress)
