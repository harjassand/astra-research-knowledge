"""Finite-bit even-walk sampler for a supplied nonnegative rational pure GBS matrix.

See nonnegative_gbs_sampling.md for the proof and scope. No hafnian oracle is used.
This reference implementation emphasizes exact arithmetic and explicit TV budgets,
not optimized performance. A seeded run is a reproducible diagnostic; the theorem
assumes independent random bits. The default unseeded run uses SystemRandom.
"""
from fractions import Fraction
from math import ceil
from random import Random, SystemRandom
from pathlib import Path
import argparse
import json
import time


def multiply(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def inverse(matrix):
    n = len(matrix)
    rows = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for column in range(n):
        pivot = next((i for i in range(column, n) if rows[i][column]), None)
        if pivot is None:
            raise ValueError('Singular matrix.')
        rows[column], rows[pivot] = rows[pivot], rows[column]
        divisor = rows[column][column]
        rows[column] = [x/divisor for x in rows[column]]
        for i in range(n):
            if i != column:
                factor = rows[i][column]
                rows[i] = [x-factor*y for x, y in zip(rows[i], rows[column])]
    return [row[n:] for row in rows]


def require_positive_definite(matrix):
    n = len(matrix)
    l = [[Fraction(i == j) for j in range(n)] for i in range(n)]
    d = []
    for i in range(n):
        pivot = matrix[i][i] - sum(l[i][k]**2*d[k] for k in range(i))
        if pivot <= 0:
            raise ValueError('The supplied symmetric B does not satisfy ||B|| < 1.')
        d.append(pivot)
        for j in range(i+1, n):
            l[j][i] = (matrix[j][i]-sum(l[j][k]*l[i][k]*d[k]
                                      for k in range(i)))/pivot


class EvenWalkSampler:
    def __init__(self, b, epsilon, *, seed=None, max_powers=2500,
                 max_bernoullis=10_000_000):
        self.b = [[Fraction(x) for x in row] for row in b]
        self.epsilon = Fraction(epsilon)
        self.m = len(self.b)
        if not 0 < self.epsilon < 1:
            raise ValueError('epsilon must be in (0, 1).')
        if not self.m or any(len(row) != self.m for row in self.b):
            raise ValueError('B must be a nonempty square matrix.')
        if self.b != [list(row) for row in zip(*self.b)]:
            raise ValueError('B must be symmetric.')
        if any(x < 0 for row in self.b for x in row):
            raise ValueError('B must be entrywise nonnegative.')
        b2 = multiply(self.b, self.b)
        t = [[Fraction(i == j)-b2[i][j] for j in range(self.m)]
             for i in range(self.m)]
        require_positive_definite(t)
        q = inverse(t)
        self.mean = sum(q[i][i] for i in range(self.m))-self.m
        self.k = ceil(2*self.mean/self.epsilon) if self.mean else 0
        if max_powers is not None and 2*self.k > max_powers:
            raise RuntimeError(f'Workload guard: requires {2*self.k} matrix powers; '
                               f'allowed {max_powers}. This instance was not sampled.')
        self.rng = SystemRandom() if seed is None else Random(seed)
        self.powers = [[[Fraction(i == j) for j in range(self.m)]
                        for i in range(self.m)]]
        for _ in range(2*self.k):
            self.powers.append(multiply(self.powers[-1], self.b))
        self.lengths = []
        for length in range(2, 2*self.k+1, 2):
            intensity = sum(self.powers[length][i][i]
                            for i in range(self.m))/length
            if intensity:
                trials = ceil(max(Fraction(1), intensity,
                                  8*self.k*intensity**2/self.epsilon))
                self.lengths.append((length, intensity, trials))
        self.total_trials = sum(r for _, _, r in self.lengths)
        if max_bernoullis is not None and self.total_trials > max_bernoullis:
            raise RuntimeError(f'Workload guard: requires {self.total_trials} Bernoulli '
                               f'trials per sample; allowed {max_bernoullis}. '
                               'This instance was not sampled.')
        draw_bound = self.total_trials + self.m*sum(r*(length+1)
                                                  for length, _, r in self.lengths)
        self.bits = max(1, ceil(4*draw_bound/self.epsilon).bit_length())
        self.denominator = 1 << self.bits
        self.plan = [(length, intensity, trials,
                      int(intensity*self.denominator/trials))
                     for length, intensity, trials in self.lengths]
        self.categorical_cache = {}

    def categorical(self, weights):
        key = tuple(weights)
        if key not in self.categorical_cache:
            total = sum(weights)
            if total <= 0:
                raise ValueError('Zero conditional table reached.')
            cumulative = Fraction(0)
            boundaries = []
            for weight in weights:
                cumulative += weight
                # U/2^bits < cumulative/total iff U < ceil(2^bits*cumulative/total).
                boundaries.append(ceil(self.denominator*cumulative/total))
            self.categorical_cache[key] = boundaries
        u = self.rng.getrandbits(self.bits)
        return next(i for i, boundary in enumerate(self.categorical_cache[key])
                    if u < boundary)

    def walk(self, length, counts):
        start = self.categorical([self.powers[length][i][i]
                                  for i in range(self.m)])
        current = start
        for remaining in range(length, 0, -1):
            counts[current] += 1
            current = self.categorical([self.b[current][j]
                                        * self.powers[remaining-1][j][start]
                                        for j in range(self.m)])
        if current != start:
            raise AssertionError('Closed-walk bridge failed to return.')

    def sample(self):
        counts = [0]*self.m
        for length, _, trials, threshold in self.plan:
            loops = sum(self.rng.getrandbits(self.bits) < threshold
                        for _ in range(trials))
            for _ in range(loops):
                self.walk(length, counts)
        return counts

    def metadata(self):
        return {
            'interface': 'pure, zero displacement, entrywise nonnegative rational B; full photon counts',
            'mean_photons': str(self.mean), 'epsilon': str(self.epsilon),
            'max_walk_length': 2*self.k, 'bernoulli_trials_per_sample': self.total_trials,
            'random_bits_per_draw': self.bits,
            'tv_budget': {'discarded_walks': str(self.epsilon/4),
                          'poisson_binomial': str(self.epsilon/4),
                          'finite_bits': str(self.epsilon/4)},
            'retained_matrix_entries': (2*self.k+1)*self.m*self.m,
            'cached_categorical_tables': len(self.categorical_cache),
            'cached_categorical_entries': self.m*len(self.categorical_cache),
            'max_photons_per_sample': sum(length*r for length, _, r in self.lengths),
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--matrix', type=Path)
    parser.add_argument('--epsilon', default='1/20')
    parser.add_argument('--samples', type=int, default=10000)
    parser.add_argument('--seed', type=int, default=177113)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    b = json.loads(args.matrix.read_text()) if args.matrix else [['0', '1/3'], ['1/3', '0']]
    started = time.perf_counter()
    sampler = EvenWalkSampler(b, args.epsilon, seed=args.seed)
    histogram = {}
    totals = [0]*sampler.m
    for _ in range(args.samples):
        sample = sampler.sample()
        key = str(tuple(sample))
        histogram[key] = histogram.get(key, 0)+1
        totals = [x+y for x, y in zip(totals, sample)]
    result = {'status': 'seeded finite diagnostic, not theorem or external validation',
              'sampler_plan': sampler.metadata(), 'seed': args.seed, 'sample_count': args.samples,
              'empirical_mode_means': [x/args.samples for x in totals],
              'histogram': histogram, 'elapsed_seconds': time.perf_counter()-started}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'histogram'}, indent=2))


if __name__ == '__main__':
    main()
