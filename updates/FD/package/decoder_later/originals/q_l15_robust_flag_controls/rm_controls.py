"""Direct Reed-Muller controls for the persistent comparator flag learner.

The full-cube decoder uses only conditional raw-label access and the standard
coordinate-flat checksum majority decoder for RM(d,n).  The local decoder uses
the random affine-cube correction stated in p_s02b_matching_robustness/PROOF.txt
and then interpolates the unisolvent Boolean anchors.  Neither learner sees the
source's planted bad set or any clean labels.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True

from itertools import combinations
import json
import math
import random
import resource
import sys as _sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
WAVE = HERE.parent
S09 = WAVE / "q_s09_robust_flag_implementation"
if str(S09) not in _sys.path:
    _sys.path.insert(0, str(S09))

from robust_learner import acquire, as_quadratic
from run_experiment import (PersistentSource, check_after_return,
                            coefficient_points, interpolate, inverse_columns)


def monomials(n: int, d: int) -> list[int]:
    return [sum(1 << i for i in inds)
            for k in range(min(n, d) + 1)
            for inds in combinations(range(n), k)]


def degree_masks(n: int, d: int) -> dict[int, tuple[int, ...]]:
    return {k: tuple(s for s in monomials(n, d) if s.bit_count() == k)
            for k in range(min(n, d) + 1)}


def _zero_masks(n: int) -> tuple[int, ...]:
    N = 1 << n
    out = []
    for i in range(n):
        half = 1 << i
        period = half << 1
        block = (1 << half) - 1
        mask = 0
        for start in range(0, N, period):
            mask |= block << start
        out.append(mask)
    return tuple(out)


def _monomial_masks(n: int, d: int) -> dict[int, int]:
    N = 1 << n
    full = (1 << N) - 1
    zeros = _zero_masks(n)
    masks = {0: full}
    for s in monomials(n, d):
        if not s:
            continue
        m = full
        bits = s
        while bits:
            low = bits & -bits
            i = low.bit_length() - 1
            m &= full ^ zeros[i]
            bits ^= low
        masks[s] = m
    return masks


class ReedChecksum:
    """Coordinate-flat majority decoder, returning the ANF support masks.

    A packed integer stores the truth table with input x in bit position x.
    For support S, repeated Boolean differences followed by a mask to S=0
    produce one parity checksum for each coordinate S-flat.  An error changes
    exactly one checksum for each fixed S.  Strict majority recovers the
    coefficient whenever the whole received table is inside half the RM
    minimum distance.
    """
    def __init__(self, n: int, d: int):
        if n < 1 or d < 0 or d > n:
            raise ValueError("invalid RM parameters")
        self.n, self.d = n, d
        self.N = 1 << n
        self.by_degree = degree_masks(n, d)
        self.zero_masks = _zero_masks(n)
        self.monomial_masks = _monomial_masks(n, d)
        self.full_mask = (1 << self.N) - 1
        self.checksum_tests_per_decode = sum(
            len(supports) * (1 << (n - k))
            for k, supports in self.by_degree.items())
        self.parity_input_reads_per_decode = self.N * sum(
            len(supports) for supports in self.by_degree.values())

    def pack(self, labels: bytearray | bytes) -> int:
        if len(labels) != self.N:
            raise ValueError("truth-table length mismatch")
        packed = bytearray((self.N + 7) // 8)
        for x, bit in enumerate(labels):
            if bit not in (0, 1):
                raise ValueError("RM labels must be bits")
            if bit:
                packed[x >> 3] |= 1 << (x & 7)
        return int.from_bytes(packed, "little")

    def decode_packed(self, word: int) -> tuple[int, ...]:
        coeffs: list[int] = []
        for k in range(self.d, -1, -1):
            for s in self.by_degree[k]:
                tmp = word
                bits = s
                while bits:
                    low = bits & -bits
                    i = low.bit_length() - 1
                    tmp = (tmp ^ (tmp >> (1 << i))) & self.zero_masks[i]
                    bits ^= low
                zero_support = self.full_mask
                bits = s
                while bits:
                    low = bits & -bits
                    zero_support &= self.zero_masks[low.bit_length() - 1]
                    bits ^= low
                votes = (tmp & zero_support).bit_count()
                total = 1 << (self.n - k)
                if 2 * votes > total:
                    coeffs.append(s)
                    word ^= self.monomial_masks[s]
        return tuple(sorted(coeffs))

    def decode(self, labels: bytearray | bytes) -> tuple[int, ...]:
        return self.decode_packed(self.pack(labels))


class FullCubeRMDecoder:
    """Query every conditional raw label once, then globally RM-decode."""
    def __init__(self, n: int, d: int, rho: float, failure: float, rng=None):
        self.n, self.d, self.rho, self.failure = n, d, rho, failure
        self.rm = ReedChecksum(n, d)
        self.decoded_bodies = self.raw_label_requests = 0
        self.checksum_tests = self.parity_input_reads = 0
        self.max_table_bytes = 0
        self.conditional_radius = 2.0 ** (-d - 1)

    def decode(self, raw):
        labels = bytearray(self.rm.N)
        for x in range(self.rm.N):
            labels[x] = int(raw(x))
            self.raw_label_requests += 1
        terms = self.rm.decode(labels)
        self.decoded_bodies += 1
        self.checksum_tests += self.rm.checksum_tests_per_decode
        self.parity_input_reads += self.rm.parity_input_reads_per_decode
        self.max_table_bytes = max(self.max_table_bytes, len(labels))
        return list(terms)

    def ledger(self):
        return dict(decoder="full_cube_standard_rm_coordinate_checksum_majority",
                    degree=self.d, raw_error_density_promise=self.rho,
                    unique_radius=self.conditional_radius,
                    per_body_failure_probability_on_radius=0,
                    decoded_bodies=self.decoded_bodies,
                    logical_raw_label_accesses=self.raw_label_requests,
                    full_cube_positions_per_body=self.rm.N,
                    checksum_tests=self.checksum_tests,
                    parity_input_reads=self.parity_input_reads,
                    fair_random_bits=0,
                    peak_decoder_truth_table_bytes=self.max_table_bytes,
                    peak_decoder_integer_bytes=(self.rm.N + 7) // 8,
                    coordinate_masks_retained=len(self.rm.zero_masks),
                    monomial_masks_retained=len(self.rm.monomial_masks))


class LocalCubeRMDecoder:
    """Standard local RM correction at anchors using random affine cubes.

    For each unisolvent anchor x, draw R independent maps A:F_2^ell->F_2^n,
    query the K=2^ell raw labels at x+A t, decode RM(d,ell) by checksum
    majority, and majority the decoded value at t=0.  Interpolate the anchor
    values to obtain the global ANF.  The theorem only covers a true degree-d
    raw label with fixed global error density at most rho.
    """
    def __init__(self, n: int, d: int, rho: float, failure: float, rng):
        if not 0 <= rho < 2.0 ** (-d - 1) or not 0 < failure < 1:
            raise ValueError("local RM correction needs rho below unique radius")
        self.n, self.d, self.rho, self.failure = n, d, rho, failure
        self.anchors = monomials(n, d)
        self.M = len(self.anchors)
        self.eta = failure / self.M
        self.gamma = 2.0 ** (-d - 1) - rho
        self.l = max(d + 1, math.ceil(math.log2(4.0 / self.gamma ** 2)))
        self.K = 1 << self.l
        self.R = max(1, math.ceil(8.0 * math.log(1.0 / self.eta)))
        if self.R % 2 == 0:
            self.R += 1
        self.rng = rng
        self.rm = ReedChecksum(self.l, d)
        self.raw_label_requests = self.cube_decodes = 0
        self.random_bits = self.checksum_tests = self.parity_input_reads = 0
        self.corrected_targets = self.decoded_bodies = 0
        self.max_cube_truth_table_bytes = 0
        self.max_affine_points = 0

    def correct_at(self, x: int, raw) -> int:
        votes = 0
        for _ in range(self.R):
            columns = [self.rng.getrandbits(self.n) for _ in range(self.l)]
            self.random_bits += self.l * self.n
            points = [0] * self.K
            labels = bytearray(self.K)
            points[0] = x
            labels[0] = int(raw(x))
            self.raw_label_requests += 1
            for t in range(1, self.K):
                low = t & -t
                i = low.bit_length() - 1
                points[t] = points[t ^ low] ^ columns[i]
                labels[t] = int(raw(points[t]))
                self.raw_label_requests += 1
            terms = self.rm.decode(labels)
            votes += int(0 in terms)
            self.cube_decodes += 1
            self.checksum_tests += self.rm.checksum_tests_per_decode
            self.parity_input_reads += self.rm.parity_input_reads_per_decode
            self.max_cube_truth_table_bytes = max(self.max_cube_truth_table_bytes,
                                                  len(labels))
            self.max_affine_points = max(self.max_affine_points, len(points))
        self.corrected_targets += 1
        return int(2 * votes > self.R)

    def decode(self, raw):
        values = {}
        for x in self.anchors:
            values[x] = self.correct_at(x, raw)
        self.decoded_bodies += 1
        coeff = {}
        terms = []
        # On Boolean subset points, q(1_S)=xor_{T subseteq S} c_T.
        for s in sorted(self.anchors, key=lambda x: (x.bit_count(), x)):
            c = values[s]
            for t, bit in coeff.items():
                if t != s and (t & s) == t:
                    c ^= bit
            coeff[s] = c
            if c:
                terms.append(s)
        return terms

    def ledger(self):
        return dict(decoder="standard_random_affine_cube_rm_local_correction",
                    degree=self.d, raw_error_density_promise=self.rho,
                    local_cube_dimension=self.l, local_cube_size=self.K,
                    strict_cube_error_threshold=2.0 ** (-self.d - 1),
                    gamma=self.gamma, repetitions_per_anchor=self.R,
                    anchors=self.M, target_label_failure_budget=self.eta,
                    decoded_bodies=self.decoded_bodies,
                    corrected_anchor_labels=self.corrected_targets,
                    logical_raw_label_accesses=self.raw_label_requests,
                    affine_cube_decodes=self.cube_decodes,
                    checksum_tests=self.checksum_tests,
                    parity_input_reads=self.parity_input_reads,
                    fair_random_bits=self.random_bits,
                    peak_cube_truth_table_bytes=self.max_cube_truth_table_bytes,
                    peak_affine_point_count=self.max_affine_points,
                    per_body_failure_probability_bound=self.M * math.exp(-self.R / 8.0))


class OrderedMemo:
    """Exact original-directed pair memo with the S09 250k-entry cap."""
    def __init__(self, n, source_query, max_entries=250000):
        self.n, self.source_query = n, source_query
        self.max_entries = max_entries
        self.cache = {}
        self.requests = self.source_calls = self.cache_hits = self.equal_requests = 0

    def __call__(self, x, y):
        self.requests += 1
        if x == y:
            self.equal_requests += 1
            return 0
        key = x | (y << self.n)
        if key in self.cache:
            self.cache_hits += 1
            return self.cache[key]
        self.source_calls += 1
        answer = int(self.source_query(x, y))
        if len(self.cache) < self.max_entries:
            self.cache[key] = answer
        return answer

    def ledger(self):
        return dict(logical_comparison_requests=self.requests,
                    external_source_calls=self.source_calls,
                    effective_oracle="original_directed_C",
                    ordered_pair_cache_enabled=True,
                    reverse_answer_inferred=False,
                    ordered_pair_cache_entries=len(self.cache),
                    ordered_pair_cache_entry_cap=self.max_entries,
                    memo_hits=self.cache_hits, equal_requests=self.equal_requests,
                    transmitted_query_argument_bits=2 * self.n * self.source_calls,
                    transmitted_answer_bits=self.source_calls,
                    cache_key_logical_bits_upper=(2 * self.n + 1) * len(self.cache))


def decoder_factory_full(n, d, rho, failure, rng):
    return FullCubeRMDecoder(n, d, rho, failure, rng)


def decoder_factory_local(n, d, rho, failure, rng):
    return LocalCubeRMDecoder(n, d, rho, failure, rng)


def run_full_case(n=16, r=2, seed=960162, epsilon=1/32, beta=.05,
                  mode="asymmetric_hash", bad_count=None,
                  pair_cache_cap=250000, max_requests=None, check=True,
                  decoder_factory=decoder_factory_full):
    if bad_count is None:
        bad_count = max(1, int(epsilon * (1 << n)))
    if bad_count / (1 << n) > epsilon:
        raise ValueError("fixture exceeds supplied noise upper bound")
    source = PersistentSource(n, r, seed, bad_count, mode)
    memo = OrderedMemo(n, source.query, pair_cache_cap)
    learner_seed = seed + 100000
    rss0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    receipt, model, comp = acquire(n, r, epsilon, beta, memo, learner_seed,
                                   sequential=True,
                                   decoder_factory=decoder_factory,
                                   max_logical_requests=max_requests)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    receipt.update(source=dict(n=n, r=r, fixture_seed=seed,
                               learner_seed=learner_seed,
                               actual_bad_count=bad_count,
                               actual_bad_density=bad_count / (1 << n),
                               supplied_epsilon_upper_bound=epsilon,
                               fault_mode=mode,
                               fixed_bad_items_hidden_from_learner=True,
                               source_setup_seconds=source.setup_seconds,
                               fresh_rank_evaluations_acquisition=source.ideal.fresh_ranks,
                               cached_rank_payload_logical_bits=2 * n * len(source.ideal.cache)),
                   oracle=memo.ledger(), truth_access_only_after_return=True,
                   process_peak_rss_acquisition_bytes=(rss * 1024
                       if sys.platform != "darwin" else rss),
                   process_peak_rss_before_acquisition_bytes=(rss0 * 1024
                       if sys.platform != "darwin" else rss0))
    assert receipt["comparison_requests"] == memo.requests
    if model is not None:
        receipt["returned_model"] = [p.body() for p in model]
        receipt["acquired_toggles"] = comp.toggles
        if check:
            receipt["post_return_checks"] = check_after_return(source, model, comp,
                                                               exhaustive=n <= 16)
            if receipt["post_return_checks"]["rank_errors"] or not receipt["post_return_checks"]["coefficients_exact"]:
                receipt["finite_result"] = "RETURNED_WRONG_MODEL"
            else:
                receipt["finite_result"] = "EXACT_MODEL_CHECKED_AFTER_RETURN"
    else:
        receipt["finite_result"] = "UNKNOWN"
    return receipt


def run_local_target_diagnostic(n=16, r=2, seed=960162, epsilon=1/32,
                                mode="asymmetric_hash", bad_count=None,
                                target_count=16, target_seed=81016,
                                pair_cache_cap=250000):
    """Correct target labels on actual source via C only; truth scores after."""
    if bad_count is None:
        bad_count = max(1, int(epsilon * (1 << n)))
    source = PersistentSource(n, r, seed, bad_count, mode)
    memo = OrderedMemo(n, source.query, pair_cache_cap)
    # Source truth is consulted only in the harness to select a genuine toggle
    # and score predictions after the corresponding comparator work.
    from run_experiment import inverse_columns
    toggles = inverse_columns(source.ideal._rows, n)
    v = toggles[0]
    # For d=2,rho=2epsilon=1/16, the S02b local corrector uses K=1024 and
    # R=51 when this control requests eta=1/(4 M_2(16)).
    private_rng = random.Random(target_seed)
    M = len(monomials(n, 2))
    decoder = LocalCubeRMDecoder(n, 2, 2 * epsilon, .25, private_rng)
    targets = random.Random(target_seed + 1).sample(range(1 << n), target_count)
    outputs = []
    source_before = memo.source_calls
    logical_before = memo.requests
    t0 = time.perf_counter()
    for x in targets:
        cache = {}
        def raw(y):
            if y not in cache:
                cache[y] = 1 ^ memo(y, y ^ v)
            return cache[y]
        got = decoder.correct_at(x, raw)
        outputs.append((x, got, len(cache)))
    elapsed = time.perf_counter() - t0
    predictions = []
    for x, got, unique_labels in outputs:
        truth = (source.ideal.rank(x) >> (n - 1)) & 1
        predictions.append(dict(target=x, prediction=got, truth_afterward=truth,
                                correct=got == truth,
                                unique_raw_labels=unique_labels))
    return dict(status="local_rm_target_diagnostic_completed",
                source=dict(n=n, r=r, fixture_seed=seed, actual_bad_count=bad_count,
                            actual_bad_density=bad_count / (1 << n),
                            supplied_epsilon_upper_bound=epsilon,
                            fault_mode=mode, fixed_bad_items_hidden_from_decoder=True),
                raw_label_contract="g_v(x)=1 xor C(x,x+v), one original-directed source comparison per unseen x; no truth labels are returned",
                conditional_true_direction_supplied_to_kernel_by_harness=True,
                target_count=target_count, predictions=predictions,
                successes=sum(int(p["correct"]) for p in predictions),
                logical_comparison_requests=memo.requests - logical_before,
                external_source_calls=memo.source_calls - source_before,
                global_ordered_pair_cache_entries=len(memo.cache),
                decoder=decoder.ledger(),
                seconds=elapsed,
                scorer_truth_reads_after_each_label=target_count,
                scope="Kernel benchmark only; the true direction is supplied by the test harness, not part of a full learner result.")


def run_local_body_diagnostic(n=16, r=2, seed=960162, epsilon=1/32,
                              mode="asymmetric_hash", bad_count=None,
                              pair_cache_cap=250000):
    """Decode one complete true body through local cubes and source labels."""
    if bad_count is None:
        bad_count = max(1, int(epsilon * (1 << n)))
    source = PersistentSource(n, r, seed, bad_count, mode)
    memo = OrderedMemo(n, source.query, pair_cache_cap)
    toggles = inverse_columns(source.ideal._rows, n)  # harness-only selection
    v = toggles[0]
    learner_rng = random.Random(seed + 100000)
    decoder = LocalCubeRMDecoder(n, 2, 2 * epsilon, .25, learner_rng)
    raw_cache = {}
    def raw(x):
        if x not in raw_cache:
            raw_cache[x] = 1 ^ memo(x, x ^ v)
        return raw_cache[x]
    started = time.perf_counter()
    terms = decoder.decode(raw)
    elapsed = time.perf_counter() - started
    candidate = as_quadratic(terms, n)
    # All truth access is post-decode and remains inside the test harness.
    pts = coefficient_points(n)
    truth = interpolate({x: (source.ideal.rank(x) >> (n - 1)) & 1
                         for x in pts}, n)
    exact = candidate.body() == truth.body()
    mismatches = 0
    for x in range(1 << n):
        mismatches += int(candidate(x) != ((source.ideal.rank(x) >> (n - 1)) & 1))
    return dict(status="local_rm_full_body_diagnostic_completed",
                source=dict(n=n, r=r, fixture_seed=seed, actual_bad_count=bad_count,
                            actual_bad_density=bad_count / (1 << n),
                            supplied_epsilon_upper_bound=epsilon,
                            fault_mode=mode,
                            fixed_bad_items_hidden_from_decoder=True),
                conditional_true_direction_supplied_to_kernel_by_harness=True,
                raw_label_contract="g_v(x)=1 xor C(x,x xor v); the decoder receives only original-directed comparator labels",
                decoded_polynomial=candidate.body(), exact_coefficients=exact,
                rank_bit_mismatches_after_return=mismatches,
                logical_comparison_requests=memo.requests,
                external_source_calls=memo.source_calls,
                ordered_pair_cache_entries=len(memo.cache),
                unique_raw_labels=len(raw_cache), decoder=decoder.ledger(),
                seconds=elapsed,
                process_peak_rss_bytes=(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                    if sys.platform == "darwin" else 1024 * resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
                truth_access_only_after_decode=True,
                scope="Single true-direction body kernel; it tests the raw-label correction step, not full flag acquisition.")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=["full-cube", "local-full", "local-targets", "local-body"], default="full-cube")
    parser.add_argument("--n", type=int, default=16)
    parser.add_argument("--r", type=int, default=2)
    parser.add_argument("--seed", type=int, default=960162)
    parser.add_argument("--epsilon", type=float, default=1/32)
    parser.add_argument("--beta", type=float, default=.05)
    parser.add_argument("--mode", choices=["asymmetric_hash", "flip_incident", "bad_first_total_order", "ideal"], default="asymmetric_hash")
    parser.add_argument("--bad-count", type=int)
    parser.add_argument("--target-count", type=int, default=16)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    if args.case == "full-cube":
        receipt = run_full_case(args.n, args.r, args.seed, args.epsilon, args.beta,
                                args.mode, args.bad_count)
        default_name = "full_cube_rm_n16_r2_hash_directed.json"
    elif args.case == "local-full":
        receipt = run_full_case(args.n, args.r, args.seed, args.epsilon, args.beta,
                                args.mode, args.bad_count,
                                decoder_factory=decoder_factory_local)
        default_name = "local_rm_full_learner_n16_r2_hash_directed.json"
    elif args.case == "local-targets":
        receipt = run_local_target_diagnostic(args.n, args.r, args.seed,
                                              args.epsilon, args.mode,
                                              args.bad_count, args.target_count)
        default_name = "local_rm_targets_n16_hash_directed.json"
    else:
        receipt = run_local_body_diagnostic(args.n, args.r, args.seed,
                                            args.epsilon, args.mode,
                                            args.bad_count)
        default_name = "local_rm_body_n16_hash_directed.json"
    output = HERE / (args.output or default_name)
    output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(dict(output=str(output), status=receipt.get("status"),
                          finite_result=receipt.get("finite_result"),
                          success=receipt.get("successes"),
                          seconds=receipt.get("seconds"),
                          comparison_requests=receipt.get("comparison_requests",
                                                           receipt.get("logical_comparison_requests")),
                          source_calls=receipt.get("oracle", {}).get("external_source_calls",
                                                                      receipt.get("external_source_calls")),
                          body_decoder=receipt.get("body_decoder")), indent=2))


if __name__ == "__main__":
    main()
