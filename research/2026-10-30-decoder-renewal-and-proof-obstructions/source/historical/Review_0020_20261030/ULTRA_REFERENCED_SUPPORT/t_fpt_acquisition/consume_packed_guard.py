"""Finite exact compiler control; no PRF, optimizer or learning run."""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path
from time import perf_counter

from packed_guard import (PackedGuard, Instruction, mv, dot, row_times,
                          race_small_weight)


def rat(x):
    return {"numerator": str(x.numerator), "denominator": str(x.denominator)}


def main():
    started = perf_counter()
    identity = tuple(range(5))
    cycle = (1, 2, 3, 4, 0)
    reverse = (4, 0, 1, 2, 3)
    swap = (1, 0, 2, 3, 4)
    program = [Instruction(0, identity, cycle),
               Instruction(3, swap, identity),
               Instruction(1, identity, reverse)]
    src = PackedGuard(4, 2, program, accept=1)
    states = {(): list(src.initial)}
    invariant_checks = label_checks = 0
    max_sim_error = F(0)
    max_label_sim_error = F(0)
    public_membership_calls = 0
    for t in range(src.active):
        for h in product((0, 1), repeat=t):
            x = states[h]
            assert x[0] == 1
            for i in range(src.p):
                assert x[src.z[i]] == x[src.r[i]]**2
            if t >= src.N:
                assert x[src.v] == x[src.u]**2
            assert x[src.g] == src.direct_guard(h)
            assert sum(x[i] for i in src.q) == 1
            assert all(x[i] in (0, 1) for i in src.q)
            assert x[src.g].denominator == 1 and x[src.g] >= 0
            p = src.probability_from_state(t, x)
            assert 0 < p < 1
            sim, calls = src.simulated_probability(h, src.program_bit)
            err = abs(p-sim)
            max_sim_error = max(max_sim_error, err)
            assert err <= 16*F(2)**(-2*src.K)
            public_membership_calls += calls
            if t == src.N+src.m:
                max_label_sim_error = max(max_label_sim_error, err)
                assert err <= 15*F(2)**(-src.C)
                assert calls == int(x[src.g] == 0)
                label_checks += 1
            for b in (0, 1):
                states[h+(b,)] = mv(src.maps[t][b], x)
            invariant_checks += 1

    # Literally bind every active-cut/future readout to its linear state
    # factorization. Both log2/log15 coefficient identities are exact.
    factorization_checks = 0
    for cut in range(src.active):
        for flen in range(src.active-cut):
            for f in product((0, 1), repeat=flen):
                a, b = src.readout(cut+flen)
                for pos in range(flen-1, -1, -1):
                    a = row_times(a, src.maps[cut+pos][f[pos]])
                    b = row_times(b, src.maps[cut+pos][f[pos]])
                for h in product((0, 1), repeat=cut):
                    aa, bb = src.readout(cut+flen)
                    assert dot(a, states[h]) == dot(aa, states[h+f])
                    assert dot(b, states[h]) == dot(bb, states[h+f])
                    factorization_checks += 1

    correct_probability = F(0)
    copied_bit_checks = 0
    for payload in product((0, 1), repeat=src.N):
        h = payload
        weight = F(1, 2**src.N)
        for bit in src.correct_scan(payload):
            p = src.probability(h)
            p_correct = p if bit else 1-p
            assert 1-p_correct <= F(2)**(-2*src.K)
            weight *= p_correct
            h += (bit,)
            copied_bit_checks += 1
        x = states[h]
        assert x[src.g] == 0
        assert x[src.q[src.accept]] == src.program_bit(payload)
        assert src.probability(h) == (F(15, 16) if src.program_bit(payload)
                                      else F(1, 16))
        correct_probability += weight
    copy_failure = 1-correct_probability
    copy_union_bound = src.m*F(2)**(-2*src.K)
    assert copy_failure <= copy_union_bound

    # Deterministic arithmetic words exercise rare branches at a1000-bit
    # odds exponent. This is not a stochastic performance experiment.
    class Tape:
        def __init__(self, word):
            self.word, self.used = word, 0
        def bits(self, width):
            part = self.word[self.used:self.used+width]
            assert len(part) == width
            self.used += width
            return int(part, 2) if part else 0
    word_controls = []
    for factor, rare_word in ((0, "0"+"0"*1000),
                             (1, "0"+"0"*996+"1110"),
                             (-1, "0"+"0"*1000+"0000")):
        for expected, word in ((0, "1"), (1, rare_word)):
            tape, counters = Tape(word), {}
            assert race_small_weight(1000, factor, tape.bits, counters) == expected
            assert counters["fair_bits"] == tape.used == len(word)
            word_controls.append({"factor15": factor, "output": expected,
                                  "fair_bits": tape.used, **counters})
    assert F(124, 15) < 10  # Uniform native-reply bound derived in the proof.
    out = {
        "scope": "exact noncryptographic packed-state/compiler control",
        "status": "PASS",
        "payload_n": src.n, "packing_p": src.p, "block_s": src.s,
        "state_dimension": src.dim, "program_reads": src.L,
        "active_positions": src.active, "padded_horizon": src.T,
        "supplied_alpha": src.alpha,
        "all_active_prefixes_checked": invariant_checks,
        "all_label_prefixes_checked": label_checks,
        "both_log_coefficient_factorizations_checked": factorization_checks,
        "correct_copy_bit_controls": copied_bit_checks,
        "public_simulator_membership_calls": public_membership_calls,
        "copy_failure_exact": rat(copy_failure),
        "copy_failure_display": float(copy_failure),
        "copy_union_bound_exact": rat(copy_union_bound),
        "max_native_simulator_TV_exact": rat(max_sim_error),
        "native_simulator_bound_exact": rat(16*F(2)**(-2*src.K)),
        "max_label_simulator_TV_exact": rat(max_label_sim_error),
        "label_simulator_bound_exact": rat(15*F(2)**(-src.C)),
        "native_race_deterministic_word_controls": word_controls,
        "native_expected_fair_bits_upper": rat(F(124, 15)),
        "source_random_draws": 0, "physical_measurements": 0,
        "cryptographic_instances": 0, "learner_runs": 0,
        "padding_enumerated": False,
        "runtime_seconds_after_imports": perf_counter()-started,
        "inputs": {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                   for name in ("packed_guard.py", "consume_packed_guard.py",
                                "PACKED_GUARD_THEOREM.md")},
    }
    target = Path(__file__).with_name("PACKED_GUARD_EXECUTION.json")
    target.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({k: v for k, v in out.items()
                      if not k.endswith("exact") and k != "inputs"}, indent=2))


if __name__ == "__main__":
    main()
