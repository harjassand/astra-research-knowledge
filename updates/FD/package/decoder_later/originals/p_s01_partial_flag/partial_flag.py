"""Capped comparison-only partial-flag quadratic acquisition. Stdlib only.

The learner receives query, n, r, parameters and PRNG seed, never source ranks.
The source truth and supplied flag are inspected only after acquire returns.
This is a Monte Carlo learner; an accepted model is not an exact certificate.
"""
import argparse
from dataclasses import dataclass
import json
import math
from pathlib import Path
import random
import time


def parity(x):
    return x.bit_count() & 1


def combine(basis, a):
    z = 0
    while a:
        b = a & -a
        z ^= basis[b.bit_length() - 1]
        a ^= b
    return z


def echelon(rows, n):
    rows = list(rows)
    pivots = []
    for j in range(n):
        i = len(pivots)
        p = next((a for a in range(i, len(rows)) if (rows[a] >> j) & 1), None)
        if p is None:
            continue
        rows[i], rows[p] = rows[p], rows[i]
        for a in range(len(rows)):
            if a != i and ((rows[a] >> j) & 1):
                rows[a] ^= rows[i]
        pivots.append(j)
    return rows[:len(pivots)], pivots


def kernel(rows, n):
    reduced, pivots = echelon(rows, n)
    return [(1 << j) | sum(((row >> j) & 1) << p for row, p in zip(reduced, pivots))
            for j in range(n) if j not in pivots]


def complement(vectors, n):
    kept = list(vectors)
    out = []
    for j in range(n):
        v = 1 << j
        if len(echelon(kept + [v], n)[1]) > len(kept):
            kept.append(v)
            out.append(v)
    assert len(kept) == n
    return out


def linear(rows, x):
    return sum(parity(row & x) << j for j, row in enumerate(rows))


@dataclass
class Quadratic:
    constant: int
    linear: int
    upper: list

    def __call__(self, x):
        z = self.constant ^ parity(self.linear & x)
        a = x
        while a:
            b = a & -a
            z ^= parity(self.upper[b.bit_length() - 1] & x)
            a ^= b
        return z

    def polar(self):
        rows = self.upper.copy()
        for i, a in enumerate(self.upper):
            while a:
                b = a & -a
                rows[b.bit_length() - 1] ^= 1 << i
                a ^= b
        return rows

    def toggles(self, v):
        return all(parity(a & v) == 0 for a in self.polar()) and (self(v) ^ self.constant) == 1

    def body(self):
        return {"constant": self.constant, "linear": self.linear, "upper": self.upper}


def coefficient_points(n):
    return [0] + [1 << i for i in range(n)] + [
        (1 << i) | (1 << j) for i in range(n) for j in range(i + 1, n)]


def interpolate(values, n):
    c = values[0]
    lin = sum((values[1 << i] ^ c) << i for i in range(n))
    upper = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            upper[i] |= (values[(1 << i) | (1 << j)] ^ values[1 << i]
                         ^ values[1 << j] ^ c) << j
    return Quadratic(c, lin, upper)


def median_deviation(m):
    return math.comb(m + 1, (m + 1) // 2) / 2 ** (m + 2)


def parameters(n, r, beta, m=47, tail_floor=7):
    assert 0 <= r <= n and 0 < beta <= 0.5 and m % 2 == 1
    c = min(n, max(r, tail_floor))
    h = n - c
    eta = median_deviation(m) + 2 ** (-c - 1)
    gamma = 0.125 - eta
    if h and gamma <= 0:
        raise ValueError("Median sample count/tail floor do not give positive validation gap")
    p = 2 ** (-r - 1)
    R = math.ceil(math.log(2 * h / beta) / (p * (1 - beta / 2))) if h else 0
    delta = beta / (2 * h * R * R) if h else 0
    t = math.ceil(math.log(1 / delta) / (2 * gamma * gamma)) if h else 0
    M = len(coefficient_points(n))
    tail = M * ((1 << c) - 1)
    unit = M + m * t
    return dict(n=n, r=r, beta=beta, median_samples=m, tail_dimension=c,
                randomized_stages=h, median_error_bound=eta, validation_gap=gamma,
                exposure_probability_bound=p, candidate_cap=R,
                validation_error_per_candidate=delta, validation_labels_per_candidate=t,
                coefficient_points=M, worst_comparison_bound=h * R * unit + tail,
                expected_comparison_bound=(h * (1 / (p * (1 - delta)) + beta / 2) * unit
                                           + tail) if h else tail,
                first_wrong_acceptance_bound=h * R * delta,
                cap_failure_bound=beta / 2 if h else 0,
                overall_failure_bound=(beta / 2 + h * R * delta) if h else 0,
                tail_comparisons=tail)


class Compiler:
    def __init__(self, n, cache=False):
        self.n = n
        self.q = []
        self.toggles = []
        self.stabilizer = [1 << i for i in range(n)]
        self.complement = self.stabilizer.copy()
        self.cache_enabled = cache
        self.sampler_cache = {}
        self.random_bits = self.direction_random_bits = self.validation_point_random_bits = 0
        self.fiber_draws = self.projections = self.projection_q_evaluations = 0
        self.sampler_cache_hits = self.sampler_cache_max_entries = self.enumerated_points = 0

    def prefix(self, x):
        return sum(p(x) << j for j, p in enumerate(self.q))

    def project(self, x, target):
        self.projections += 1
        for j, (p, v) in enumerate(zip(self.q, self.toggles)):
            self.projection_q_evaluations += 1
            if p(x) != ((target >> j) & 1):
                x ^= v
        return x

    def sample(self, target, rng):
        d = len(self.complement)
        a = rng.getrandbits(d)
        self.fiber_draws += 1
        self.random_bits += d
        key = (target << d) | a
        if self.cache_enabled and key in self.sampler_cache:
            self.sampler_cache_hits += 1
            return self.sampler_cache[key]
        x = self.project(combine(self.complement, a), target)
        if self.cache_enabled:
            self.sampler_cache[key] = x
            self.sampler_cache_max_entries = max(self.sampler_cache_max_entries, len(self.sampler_cache))
        return x

    def fiber(self, target):
        for a in range(1 << len(self.complement)):
            self.enumerated_points += 1
            yield self.project(combine(self.complement, a), target)

    def add(self, p, v):
        assert p.toggles(v)
        assert all(all(parity(row & v) == 0 for row in q.polar())
                   and q(v) == q.constant for q in self.q)
        self.q.append(p)
        self.toggles.append(v)
        self.complement = complement(self.toggles, self.n)
        # First restrict to the common polar radical; only there are responses linear.
        radical = kernel([row for q in self.q for row in q.polar()], self.n)
        response = [sum((q(w) ^ q.constant) << a for a, w in enumerate(radical))
                    for q in self.q]
        self.stabilizer = [combine(radical, a) for a in kernel(response, len(radical))]
        self.sampler_cache = {}


def median_label(x, query, comp, m, rng):
    prefix = comp.prefix(x)
    votes = sum(query(x, comp.sample(prefix, rng)) for _ in range(m))
    return int(votes <= m // 2)


def acquire(n, r, query, seed, beta=0.01, m=47, tail_floor=7, cache=False,
            force_zero_directions=False):
    """Only query is provided. force_zero_directions is a test-only cap fixture."""
    start = time.perf_counter()
    cfg = parameters(n, r, beta, m, tail_floor)
    rng = random.Random(seed)
    comp = Compiler(n, cache)
    points = coefficient_points(n)
    stages = []
    calls = interpolation_calls = validation_calls = 0
    for k in range(cfg['randomized_stages']):
        stage_start = time.perf_counter()
        if not comp.stabilizer:
            return dict(status='UNKNOWN', reason='empty_stabilizer', parameters=cfg,
                        stages=stages, comparison_calls=calls), None, comp
        trials = []
        accepted = None
        for j in range(cfg['candidate_cap']):
            a = 0 if force_zero_directions else rng.getrandbits(len(comp.stabilizer))
            if not force_zero_directions:
                comp.direction_random_bits += len(comp.stabilizer)
            v = combine(comp.stabilizer, a)
            if v == 0:
                trials.append(dict(trial=j, direction=0, status='zero_direction', comparisons=0))
                continue
            values = {x: 1 ^ int(query(x, x ^ v)) for x in points}
            calls += len(points)
            interpolation_calls += len(points)
            p = interpolate(values, n)
            if not p.toggles(v):
                trials.append(dict(trial=j, direction=v, status='algebraic_gate_rejected',
                                   comparisons=len(points)))
                continue
            mismatches = labels = 0
            threshold = cfg['validation_labels_per_candidate'] // 8
            for _ in range(cfg['validation_labels_per_candidate']):
                x = rng.getrandbits(n)
                comp.validation_point_random_bits += n
                labels += 1
                mismatches += p(x) != median_label(x, query, comp, m, rng)
                if mismatches > threshold:
                    break  # Exactly anticipates failure of the fixed-size test.
            used = m * labels
            calls += used
            validation_calls += used
            passed = labels == cfg['validation_labels_per_candidate'] and mismatches <= threshold
            trials.append(dict(trial=j, direction=v, status='accepted' if passed else 'validation_rejected',
                               validation_labels=labels, disagreements=mismatches,
                               threshold=threshold, comparisons=len(points) + used))
            if passed:
                comp.add(p, v)
                accepted = p
                break
        stages.append(dict(stage=k, stabilizer_dimension_before=(n if k == 0 else stages[-1]['stabilizer_dimension_after']),
                           stabilizer_dimension_after=len(comp.stabilizer), trials=trials,
                           stage_seconds_including_source=time.perf_counter() - stage_start))
        if accepted is None:
            return dict(status='UNKNOWN', reason='candidate_cap_exhausted', parameters=cfg,
                        stages=stages, comparison_calls=calls,
                        interpolation_comparisons=interpolation_calls,
                        validation_comparisons=validation_calls,
                        acquisition_seconds_including_source=time.perf_counter() - start), None, comp
    tail_start = time.perf_counter()
    remaining = len(comp.complement)
    values = [dict() for _ in range(remaining)]
    for x in points:
        prefix = comp.prefix(x)
        rank = sum(query(y, x) for y in comp.fiber(prefix) if y != x)
        calls += (1 << remaining) - 1
        for j in range(remaining):
            values[j][x] = (rank >> (remaining - j - 1)) & 1
    learned = comp.q + [interpolate(a, n) for a in values]
    assert calls == interpolation_calls + validation_calls + cfg['tail_comparisons']
    return dict(status='returned_model', parameters=cfg, stages=stages,
                comparison_calls=calls, interpolation_comparisons=interpolation_calls,
                validation_comparisons=validation_calls,
                tail_comparisons=cfg['tail_comparisons'],
                tail_seconds_including_source=time.perf_counter() - tail_start,
                acquisition_seconds_including_source=time.perf_counter() - start), learned, comp


class PartialTeacher:
    """Synthetic hidden-affine partial flags with arbitrary quadratic suffix permutations.

    Prefix q_i=u_i+g_i(u_<i,z); suffix is affine mixing of a Toffoli on z.
    This subset is bijective by construction. The theorem covers the full promise.
    """
    def __init__(self, n, r, seed):
        start = time.perf_counter()
        rng = random.Random(seed)
        self.n, self.r = n, r
        while True:
            self._rows = [rng.getrandbits(n) for _ in range(n)]
            if len(echelon(self._rows, n)[1]) == n:
                break
        self._offset = rng.getrandbits(n)
        cutoff = n - r
        self._prefix = []
        for i in range(cutoff):
            allowed = list(range(i)) + list(range(cutoff, n))
            lin = 1 << i
            for a in allowed:
                lin ^= rng.getrandbits(1) << a
            upper = [0] * n
            for a in allowed:
                for b in allowed:
                    if a < b:
                        upper[a] |= rng.getrandbits(1) << b
            self._prefix.append(Quadratic(rng.getrandbits(1), lin, upper))
        while True:
            self._suffix_rows = [rng.getrandbits(r) for _ in range(r)]
            if len(echelon(self._suffix_rows, r)[1]) == r:
                break
        self._suffix_offset = rng.getrandbits(r)
        self.calls = self.fresh_ranks = 0
        self.cache = {}
        self.setup_seconds = time.perf_counter() - start

    def rank(self, x):
        if x not in self.cache:
            self.fresh_ranks += 1
            u = linear(self._rows, x) ^ self._offset
            prefix = 0
            for q in self._prefix:
                prefix = (prefix << 1) | q(u)
            z = u >> (self.n - self.r)
            if self.r >= 3:
                z ^= (((z >> 1) & 1) & ((z >> 2) & 1))
            suffix = linear(self._suffix_rows, z) ^ self._suffix_offset
            suffix_msb = 0
            for j in range(self.r):
                suffix_msb = (suffix_msb << 1) | ((suffix >> j) & 1)
            self.cache[x] = (prefix << self.r) | suffix_msb
        return self.cache[x]

    def query(self, x, y):
        self.calls += 1
        return self.rank(x) < self.rank(y)


def rank_from_model(q, x):
    r = 0
    for p in q:
        r = (r << 1) | p(x)
    return r


def mergesort(values, query):
    if len(values) < 2:
        return values
    mid = len(values) // 2
    left, right = mergesort(values[:mid], query), mergesort(values[mid:], query)
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if query(left[i], right[j]):
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]


def inherited_rm_formula(n, beta, c):
    M = len(coefficient_points(n))
    q = M * ((1 << min(c, n)) - 1)
    for k in range(max(0, n - c)):
        eta = median_deviation(127) + 2 ** (-(n - k))
        gap = 0.5 - 7 * eta
        t = math.ceil(math.log(n * M / beta) / (2 * gap * gap))
        t += 1 - t % 2
        q += 7 * 127 * M * t
    return q


def exact_geometry_receipt():
    cases = []
    # Sharp examples: first r bits linear, next bit own + sum earlier_j*suffix_j.
    for r in range(1, 5):
        n, k = 2 * r + 2, r
        q = [Quadratic(0, 1 << i, [0] * n) for i in range(n)]
        for j in range(r):
            q[k].upper[j] |= 1 << (n - r + j)
        comp = Compiler(n)
        for j in range(k):
            comp.add(q[j], 1 << j)
        good = sum(q[k].toggles(combine(comp.stabilizer, a))
                   for a in range(1 << len(comp.stabilizer)))
        denominator = 1 << len(comp.stabilizer)
        assert good / denominator == 2 ** (-r - 1)
        cases.append(dict(n=n, r=r, stage=k, stabilizer_dimension=len(comp.stabilizer),
                          good_directions=good, total_directions=denominator,
                          exact_exposure_probability=good / denominator,
                          lower_bound=2 ** (-r - 1), lower_bound_sharp=True))
    # Inherited n=4,r=2 impostor has a polynomial self-toggle but is not q_1.
    n = 4
    q = [Quadratic(0, 1, [0, 0, 8, 0]), Quadratic(0, 2, [0, 0, 8, 0]),
         Quadratic(0, 4, [0] * n), Quadratic(0, 8, [0] * n)]
    ranks = [rank_from_model(q, x) for x in range(1 << n)]
    v = 4
    f = interpolate({x: 1 ^ int(ranks[x] < ranks[x ^ v]) for x in coefficient_points(n)}, n)
    truth = [1 ^ int(ranks[x] < ranks[x ^ v]) for x in range(1 << n)]
    assert all(f(x) == truth[x] for x in range(1 << n)) and f.toggles(v)
    distance = sum(f(x) != q[0](x) for x in range(1 << n)) / (1 << n)
    assert distance >= 0.25
    return dict(sharp_exposure_cases=cases, inherited_impostor=dict(
        n=n, r=2, direction=v, candidate=f.body(), candidate_has_exact_own_toggle=True,
        candidate_is_next_bit=False, exact_global_disagreement_with_next=distance,
        original_rank_bijection=len(set(ranks)) == 1 << n))


def run(n, r, seed, beta=0.01, m=47, cache=True, baseline=True):
    teacher = PartialTeacher(n, r, seed)
    result, model, comp = acquire(n, r, teacher.query, seed + 1000000, beta, m, cache=cache)
    result.update(seed=seed, source_setup_seconds=teacher.setup_seconds,
                  source_queries_acquisition=teacher.calls,
                  source_fresh_ranks_acquisition=teacher.fresh_ranks,
                  source_cache_logical_bits=2 * n * len(teacher.cache),
                  source_rank_elementary_bitwork_upper=teacher.fresh_ranks * (3 * n ** 3 + 3 * n ** 2),
                  query_argument_bits=2 * n * teacher.calls, comparison_answer_bits=teacher.calls,
                  direction_random_bits=comp.direction_random_bits,
                  validation_point_random_bits=comp.validation_point_random_bits,
                  fiber_seed_random_bits=comp.random_bits, independent_fiber_draws=comp.fiber_draws,
                  sampler_projections=comp.projections, sampler_polynomial_evaluations=comp.projection_q_evaluations,
                  sampler_cache_enabled=cache, sampler_cache_hits=comp.sampler_cache_hits,
                  sampler_cache_max_entries=comp.sampler_cache_max_entries,
                  sampler_cache_logical_payload_bits_upper=2 * n * comp.sampler_cache_max_entries,
                  tail_enumerated_points=comp.enumerated_points,
                  inherited_rm_comparisons_analytical_unexecuted=inherited_rm_formula(n, beta, max(7, r)))
    assert teacher.calls == result['comparison_calls']
    if model is None:
        return result
    calls_before = teacher.calls
    fresh_before = teacher.fresh_ranks
    start = time.perf_counter()
    points = coefficient_points(n)
    truth = [interpolate({x: (teacher.rank(x) >> (n - i - 1)) & 1 for x in points}, n)
             for i in range(n)]
    equal = [p.body() == q.body() for p, q in zip(model, truth)]
    errors = sum(rank_from_model(model, x) != teacher.rank(x) for x in range(1 << n))
    assert all(equal) and errors == 0
    # Exhaust the acquired final prefix sampler: every seed for every target.
    seen = set()
    for target in range(1 << len(comp.q)):
        fiber = list(comp.fiber(target))
        assert len(set(fiber)) == len(fiber)
        assert all(comp.prefix(x) == target for x in fiber)
        seen.update(fiber)
    assert len(seen) == 1 << n
    rng = random.Random(seed + 2000000)
    targets = rng.sample(range(1 << n), min(64, 1 << n))
    for target in targets:
        pref = sum(((target >> (n - i - 1)) & 1) << i for i in range(len(comp.q)))
        xs = [x for x in comp.fiber(pref) if rank_from_model(model, x) == target]
        assert len(xs) == 1 and teacher.rank(xs[0]) == target
    # Check original promised raw-input directions (truth only after learner return).
    original_flag = []
    for i in range(n - r):
        v = next(x for x in range(1 << n) if linear(teacher._rows, x) == 1 << i)
        assert truth[i].toggles(v)
        assert all(all(parity(row & v) == 0 for row in truth[j].polar())
                   and truth[j](v) == truth[j].constant for j in range(i))
        original_flag.append(v)
    full_gate = Compiler(n)
    extendible = []
    for p in truth:
        radical = kernel([a for q in full_gate.q + [p] for a in q.polar()], n)
        candidate = next((v for a in range(1 << len(radical))
                          if (v := combine(radical, a)) and p.toggles(v)
                          and all(q(v) == q.constant for q in full_gate.q)), None)
        if candidate is None:
            extendible.append(False)
            break
        full_gate.add(p, candidate)
        extendible.append(True)
    result.update(exact_coordinate_bodies=equal, exhaustive_rank_points=1 << n,
                  exhaustive_rank_errors=errors, exhaustive_acquired_prefix_points=len(seen),
                  inverse_targets_checked=len(targets), execution_source_queries=teacher.calls - calls_before,
                  checking_fresh_source_ranks=teacher.fresh_ranks - fresh_before,
                  checking_seconds_including_source=time.perf_counter() - start,
                  original_flag_verified=True, complete_flag_extension_gates=extendible,
                  outside_complete_flag_class=(len(extendible) < n or not all(extendible)),
                  coefficient_payload_bits=n * len(points), toggle_payload_bits=n * len(comp.toggles),
                  acquired_model=[p.body() for p in model], acquired_toggles=comp.toggles)
    if baseline:
        source = PartialTeacher(n, r, seed)
        start = time.perf_counter()
        sorted_points = mergesort(list(range(1 << n)), source.query)
        elapsed = time.perf_counter() - start
        assert all(source.rank(x) == j for j, x in enumerate(sorted_points))
        result['full_domain_sort_control'] = dict(comparisons=source.calls, fresh_source_ranks=source.fresh_ranks,
                                                  source_cache_logical_bits=2 * n * len(source.cache),
                                                  table_points=len(sorted_points), correct=True,
                                                  source_setup_seconds=source.setup_seconds,
                                                  seconds_including_source=elapsed)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cases', default='8:2:910082,10:3:910103,12:2:910122,12:4:910124')
    parser.add_argument('--output', default=str(Path(__file__).with_name('evidence.json')))
    parser.add_argument('--beta', type=float, default=0.01)
    parser.add_argument('--median-samples', type=int, default=47)
    parser.add_argument('--no-sampler-cache', action='store_true')
    parser.add_argument('--baseline-max-n', type=int, default=16)
    args = parser.parse_args()
    receipt = dict(status='restricted_monte_carlo_compiler_no_novelty_claim',
                   geometry=exact_geometry_receipt(), cases=[])
    # No target oracle access is used by the forced-zero cap fixture.
    queried = []
    fixture, fixture_model, _ = acquire(8, 2, lambda x, y: queried.append((x, y)), 123,
                                      force_zero_directions=True)
    assert fixture['status'] == 'UNKNOWN' and fixture_model is None and queried == []
    receipt['forced_cap_fixture'] = dict(status=fixture['status'], reason=fixture['reason'],
                                         attempted_directions=len(fixture['stages'][0]['trials']),
                                         query_count=len(queried), guessed_model=False)
    for spec in args.cases.split(','):
        n, r, seed = map(int, spec.split(':'))
        case = run(n, r, seed, args.beta, args.median_samples,
                   cache=not args.no_sampler_cache, baseline=n <= args.baseline_max_n)
        receipt['cases'].append(case)
        Path(args.output).write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps({k: case[k] for k in ('seed','comparison_calls','interpolation_comparisons',
              'validation_comparisons','acquisition_seconds_including_source','outside_complete_flag_class')}), flush=True)
    receipt['analytic_unexecuted_scaling'] = [parameters(n, r, args.beta, args.median_samples)
                                             for n in (16,24,32,64,128) for r in (2,4)]
    Path(args.output).write_text(json.dumps(receipt, indent=2) + '\n')


if __name__ == '__main__':
    main()
