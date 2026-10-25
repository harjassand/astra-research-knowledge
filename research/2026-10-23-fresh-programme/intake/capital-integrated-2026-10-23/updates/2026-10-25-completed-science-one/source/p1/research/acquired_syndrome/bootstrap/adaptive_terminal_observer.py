"""Exact finite controller for bounded terminal QND readout.

Retains the previously acquired 256 positive task weights. Chooses whether to
request another complete round of six local weak probes, and which final
Pauli to apply. It sees no native model, latent syndrome, or logical error.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np

HERE = Path(__file__).resolve().parent
COMMUNICATION = HERE.parent / "communication"


class AdaptiveTerminalObserver:
    def __init__(self, model, epsilon=F(1, 200), max_rounds=35):
        self.model = model
        self.epsilon = F(epsilon)
        self.max_rounds = max_rounds
        self.initial = np.array(model["positive_weight_numerators"], dtype=object).reshape(64, 4)
        assert self.initial.min() >= 0 and sum(self.initial.flat) > 0
        self.best_per_syndrome = np.array([max(range(4), key=lambda s: int(row[s]))
                                           for row in self.initial], dtype=np.int16)
        self.factors = np.array([[1 << (2 * (6 - (mark ^ mu).bit_count()))
                                 for mu in range(64)] for mark in range(64)], dtype=object)
        self.reset()

    def reset(self):
        self.posterior_numerators = self.initial.copy()
        self.rounds = 0
        self.words = np.zeros(6, dtype=np.uint64)
        self.negative_counts = np.zeros(6, dtype=np.int16)

    def assess(self):
        scores = [int(v) for v in self.posterior_numerators.sum(axis=0)]
        total = sum(scores)
        maximum = max(scores)
        perfect = int(self.posterior_numerators[np.arange(64), self.best_per_syndrome].sum())
        gap = perfect - maximum
        assert 0 <= gap <= total
        context = sum(int(v > self.rounds // 2) << j for j, v in enumerate(self.negative_counts))
        preferred = int(self.model.get("hard_tie_policy", [0] * 64)[context])
        choice = preferred if scores[preferred] == maximum else scores.index(maximum)
        stopped_for_value = gap * self.epsilon.denominator <= total * self.epsilon.numerator
        stopped_for_cap = self.rounds == self.max_rounds
        return {"stop": stopped_for_value or stopped_for_cap,
                "reason": "remaining_value" if stopped_for_value else "cap" if stopped_for_cap else "continue",
                "action": choice, "gap_numerator": gap, "normalizer": total,
                "modeled_error_numerator": total - maximum,
                "modeled_perfect_error_numerator": total - perfect}

    def receive_round(self, negative_marks):
        """Consume exactly the six actual weak marks in a requested round."""
        marks = np.asarray(negative_marks, dtype=np.uint8)
        assert marks.shape == (6,) and np.all(marks < 2)
        assert not self.assess()["stop"]
        mask = sum(int(v) << j for j, v in enumerate(marks))
        self.posterior_numerators *= self.factors[mask, :, None]
        self.words |= marks.astype(np.uint64) << np.uint64(self.rounds)
        self.negative_counts += marks
        self.rounds += 1


def replay(record, model, epsilon=F(1, 200), max_rounds=35):
    """Replay only performed observations, rejecting extra/missing marks."""
    observer = AdaptiveTerminalObserver(model, epsilon, max_rounds)
    n = len(record["read_rounds"])
    action = np.empty(n, dtype=np.uint8)
    first_round_action = np.empty(n, dtype=np.uint8)
    stop_reasons = np.empty(n, dtype=np.uint8)
    gaps = []
    for index in range(n):
        observer.reset()
        rounds = int(record["read_rounds"][index])
        words = record["syndrome_words"][index]
        assert rounds <= max_rounds and np.all(words >> np.uint64(rounds) == 0)
        initial = observer.assess()
        prefix_action = initial["action"]
        for turn in range(rounds):
            assert not observer.assess()["stop"]
            observer.receive_round((words >> np.uint64(turn)) & np.uint64(1))
            if turn == 0:
                prefix_action = observer.assess()["action"]
        final = observer.assess()
        assert final["stop"] and observer.rounds == rounds
        action[index] = final["action"]
        first_round_action[index] = prefix_action
        stop_reasons[index] = int(final["reason"] == "cap")
        gaps.append(float(F(final["gap_numerator"], final["normalizer"])))
    assert np.array_equal(action, record["applied_repair"])
    assert np.array_equal(stop_reasons, record["stop_reason"])
    return action, first_round_action, stop_reasons, np.array(gaps)


def controlled_checks():
    # Two nonzero latent bits; remaining four virtual bits are fixed atzero.
    parity = [[0] * 4 for _ in range(64)]
    for mu in range(4):
        parity[mu][(mu.bit_count() & 1)] = 1
    def gain_after(pattern):
        w = [[F(v) for v in row] for row in parity]
        for bit, mark in pattern:
            for mu in range(64):
                factor = F(4, 5) if ((mu >> bit) & 1) == mark else F(1, 5)
                w[mu] = [v * factor for v in w[mu]]
        total = sum(v for row in w for v in row)
        success = max(sum(row[s] for row in w) for s in range(4)) / total
        perfect = sum(max(row) for row in w) / total
        return success, perfect - success
    base = gain_after([])
    assert base == (F(1, 2), F(1, 2))
    one = [gain_after([(bit, mark)]) for bit in (0, 1) for mark in (0, 1)]
    assert all(pair == base for pair in one)
    two = [gain_after([(0, a), (1, b)]) for a in (0, 1) for b in (0, 1)]
    assert all(pair == (F(17, 25), F(8, 25)) for pair in two)
    irreducible = [[9, 1, 0, 0] for _ in range(64)]
    model = {"positive_weight_numerators": sum(irreducible, []), "hard_tie_policy": [0] * 64}
    observer = AdaptiveTerminalObserver(model)
    assessment = observer.assess()
    assert assessment["stop"] and observer.rounds == 0
    assert F(assessment["modeled_error_numerator"], assessment["normalizer"]) == F(1, 10)
    assert assessment["gap_numerator"] == 0
    # A deterministic X inserted between probes would invalidate this kernel;
    # its exact same-count counterexample is retained in the companion source.
    return {"greedy_first_probe_value_exact": "0",
            "fair_two_distinct_probes_success_exact": "17/25",
            "fair_two_distinct_probes_gain_exact": "9/50",
            "irreducible_error_exact": "1/10",
            "irreducible_remaining_value_exact": "0",
            "irreducible_probes_requested": 0}


if __name__ == "__main__":
    result = controlled_checks()
    (HERE / "adaptive_terminal_controlled_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
