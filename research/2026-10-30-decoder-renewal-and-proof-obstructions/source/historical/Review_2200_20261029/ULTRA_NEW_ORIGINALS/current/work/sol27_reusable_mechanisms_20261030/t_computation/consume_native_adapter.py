"""Predeclared native-only adapter control on the SAME rare binary law.

No bias service, original VALUE, hidden factor or full GLS/LM learner is used.
The tested tau/tolerance are a COARSE PRIMITIVE CONTROL, explicitly not the
primary theorem's much tighter full-learning schedule, which is recorded only.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import time

import numpy as np
from flint import arb, ctx

from native_fixed_rank_adapter import (
    SmoothedPaddedBinary, CachedBinaryLogits, primary_binary_parameters,
)

HERE = Path(__file__).resolve().parent


class WordCoins:
    """Exact rational-coin kernel under iid64 words; seeded PRNG diagnostic.

    Equal first64-digit blocks recurse only on their residual coins. Counting
    a batch aggregates independent shots; it never prices that batch as one
    native query. Local dyadic coins terminate at their finite binary length.
    """
    def __init__(self, seed):
        self.rng = np.random.Generator(np.random.PCG64(seed))
        self.seed, self.words, self.buffer, self.left = seed, 0, 0, 0
        self.maximum_block_rounds = 0

    def raw(self, n):
        self.words += n
        return self.rng.bit_generator.random_raw(n)

    def bit(self):
        if not self.left:
            self.buffer = int(self.raw(1)[0])
            self.left = 64
        value = self.buffer & 1
        self.buffer >>= 1
        self.left -= 1
        return value

    def count(self, probability, n):
        p = F(probability)
        if not 0 <= p <= 1 or n < 0:
            raise ValueError("invalid rational coin")
        numerator, denominator = p.numerator, p.denominator
        remaining, heads, rounds = n, 0, 0
        while remaining:
            if numerator == 0:
                break
            if numerator == denominator:
                heads += remaining
                break
            rounds += 1
            if rounds > 256:
                raise RuntimeError("diagnostic random-bit cap exceeded")
            threshold, residue = divmod(numerator << 64, denominator)
            undecided, left = 0, remaining
            while left:
                block = min(left, 1 << 17)
                words = self.raw(block)
                heads += int(np.count_nonzero(words < np.uint64(threshold)))
                if residue:
                    undecided += int(np.count_nonzero(words == np.uint64(threshold)))
                left -= block
            remaining, numerator = undecided, residue
        self.maximum_block_rounds = max(self.maximum_block_rounds, rounds)
        return heads

    def bernoulli(self, probability):
        return self.count(probability, 1)


class HiddenNativeRareBit:
    """The primitive can ask only paid next-bit samples at its valid prefix."""
    def __init__(self, hidden_L, coins):
        self._probability = F(1, 1 + (1 << hidden_L))
        self._L, self.coins = hidden_L, coins
        self.native_draws, self.native_ones = 0, 0
        self.max_submitted_prefix_length = 0

    def count(self, prefix, n):
        if tuple(prefix) != ():
            raise ValueError("original length-one teacher queried beyond its domain")
        self.native_draws += n
        result = self.coins.count(self._probability, n)
        self.native_ones += result
        return result

    def next(self, prefix):
        return self.count(prefix, 1)


def aa(q):
    q = F(q)
    return arb(q.numerator) / q.denominator


def exact_json(value):
    if isinstance(value, F):
        return {"numerator_hex": hex(value.numerator), "denominator_hex": hex(value.denominator)}
    if isinstance(value, int) and value.bit_length() > 1024:
        return {"integer_hex": hex(value), "bits": value.bit_length()}
    return value


def main():
    started = time.perf_counter()
    local_coins, native_coins = WordCoins(2026103002), WordCoins(2026103003)
    native = HiddenNativeRareBit(1443, native_coins)
    schedule = primary_binary_parameters(1, 1, 32, F(1, 4), F(1, 20))
    # This larger tau and coarse query tolerance test only the implementable
    # primitive; the full theorem's tau/xi/caps are NOT claimed executed.
    adapter = SmoothedPaddedBinary(native, 1, schedule["padded_length"], F(1, 32), local_coins)
    cache = CachedBinaryLogits(adapter, F(1, 4), F(1, 20), max_draws=1_000_000)
    estimate = cache.get(())
    native_at_cache = native.native_draws
    assert cache.get(()) == estimate and native.native_draws == native_at_cache
    assert cache.get((1, 0, 1)) == 0 and native.native_draws == native_at_cache
    first_bits = []
    for _ in range(64):
        word = adapter.future(())
        assert len(word) == schedule["padded_length"]
        first_bits.append(word[0])
    assert native.native_draws == adapter.stats["native_next_draws"]
    assert adapter.stats["native_submitted_symbols"] == 0
    # The native client is now locked; expose the hidden probability only here.
    ctx.prec = 256
    truth_p = (1 - adapter.tau) * native._probability + adapter.tau / 2
    truth_logit = (aa(truth_p).log() - aa(1 - truth_p).log()) / 2
    error = abs(aa(estimate) - truth_logit)
    assert error < aa(cache.xi)
    probability_discrepancy = abs(truth_p - native._probability)
    assert probability_discrepancy <= adapter.tau / 2
    assert cache.draws == 344064
    record = {
        "status": "PASS",
        "scope": "native padding/smoothing/cached-logit primitive; NOT a full fixed-rank learner run",
        "randomness_scope": "seeded PCG64 diagnostic; exact rational kernels conditional on iid64 words",
        "primitive_control": {"original_T": 1, "alpha": 32,
                              "padded_H": schedule["padded_length"],
                              "tau": str(adapter.tau), "logit_tolerance": str(cache.xi),
                              "per_context_failure": str(cache.failure),
                              "uses_primary_full_learning_parameters": False,
                              "estimator_draws": cache.draws,
                              "sampled_padded_futures": 64,
                              "cached_estimate": str(estimate),
                              "true_smoothed_logit_arb": str(truth_logit),
                              "observed_logit_error_arb": str(error),
                              "cache_hits": cache.hits,
                              "known_padding_logit": "0",
                              "padded_future_first_bit_ones": sum(first_bits)},
        "native_and_adapter_counts": adapter.stats,
        "native_draws": native.native_draws, "native_ones": native.native_ones,
        "native_raw_PRNG_words": native_coins.words,
        "local_raw_PRNG_words": local_coins.words,
        "total_generated_PRNG_bits": 64 * (native_coins.words + local_coins.words),
        "native_maximum_block_rounds": native_coins.maximum_block_rounds,
        "local_maximum_block_rounds": local_coins.maximum_block_rounds,
        "actual_native_query_prefixes": ["empty original prefix only"],
        "source_audit_after_lock": {"hidden_L": native._L,
                                    "probability": "1/(1+2^1443)",
                                    "no_probability_VALUE_used_by_adapter": True},
        "cached_estimation_records": cache.records,
        "primary_schedule_record_only": {k: exact_json(v) for k, v in schedule.items()},
        "full_GLS_or_LM_runs": 0, "physical_shots": 0,
        "module_sha256": hashlib.sha256((HERE / "native_fixed_rank_adapter.py").read_bytes()).hexdigest(),
        "port_proof_sha256": hashlib.sha256((HERE / "FIXED_RANK_NATIVE_PORT.md").read_bytes()).hexdigest(),
        "elapsed_seconds_after_imports": time.perf_counter() - started,
    }
    (HERE / "NATIVE_ADAPTER_EXECUTION.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "scope": record["scope"],
                      "estimator_draws": cache.draws, "native_draws": native.native_draws,
                      "generated_PRNG_bits": record["total_generated_PRNG_bits"],
                      "observed_logit_error": str(error),
                      "elapsed_seconds_after_imports": record["elapsed_seconds_after_imports"]}, indent=2))


if __name__ == "__main__":
    main()
