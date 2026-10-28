#!/usr/bin/env python3
"""Exact checks of the hidden-coloring lower bound; standard library only.

The d=2,3 witness laws are checked by exhaustive color assignments. Full
coarse transcript laws and a small adaptive policy are also checked. The
arbitrary-policy conclusion is established by the accompanying proof.
"""
from collections import defaultdict
from fractions import Fraction as F
import json


def move(position, action, d):
    if action == "X":
        return position ^ 1
    assert action in ("R0", "R1")
    offset = 0 if action == "R0" else 1
    return sum(((position >> j) & 1) << ((offset - j) % d) for j in range(d))


def translation(w, d):
    actions = []
    for t in range(d):
        if w & (1 << ((-t) % d)):
            actions.append("X")
        actions += ["R0", "R1"]
    assert len(actions) == 2 * d + w.bit_count()
    return tuple(actions)


def witness(w, d):
    return ("K",) + translation(w, d) + ("K",)


def check_translations():
    for d in range(2, 6):
        for start in range(1 << d):
            for action in ("X", "R0", "R1"):
                assert move(move(start, action, d), action, d) == start
            for w in range(1 << d):
                position = start
                for action in translation(w, d):
                    position = move(position, action, d)
                assert position == start ^ w


def survival(word, c, d, secret=None):
    total = F(0)
    for start in range(1 << d):
        position, queried = start, set()
        for action in word:
            if action == "K":
                queried.add(position if secret is None else min(position, position ^ secret))
            else:
                position = move(position, action, d)
        total += F(1, 2 ** len(queried))
    return c ** len(word) * total / (1 << d)


def law(word, c, d, secret=None):
    result, previous = {}, F(1)
    for t in range(1, len(word) + 1):
        current = survival(word[:t], c, d, secret)
        result[f"D{t}"] = previous - current
        previous = current
    result["L"] = previous
    assert sum(result.values()) == 1
    return result


def exhaustive_survival(word, c, d, secret=None):
    size = 1 << d
    reps = list(range(size)) if secret is None else [x for x in range(size) if x < (x ^ secret)]
    index = {x: j for j, x in enumerate(reps)}
    successes = 0
    for coloring in range(1 << len(reps)):
        for start in range(size):
            position, alive = start, True
            for action in word:
                if action == "K":
                    site = position if secret is None else min(position, position ^ secret)
                    if not coloring & (1 << index[site]):
                        alive = False
                        break
                else:
                    position = move(position, action, d)
            successes += alive
    return F(successes, size * (1 << len(reps))) * c ** len(word)


def baseline_latent(word, c, d):
    """Law of (observed outcome, D, terminal-zero bad-difference set)."""
    result = defaultdict(F)
    size, length = 1 << d, len(word)
    unit = F(1, size * (1 << size))
    for coloring in range(1 << size):
        for start in range(size):
            position, queried = start, set()
            for t, action in enumerate(word, start=1):
                old = set(queried)
                if action == "K":
                    queried.add(position)
                else:
                    position = move(position, action, d)
                result[(f"D{t}", len(queried), frozenset())] += unit * (1 - c) * c ** (t - 1)
                if action == "K" and not coloring & (1 << position):
                    bad = frozenset(position ^ previous for previous in old)
                    assert 0 not in bad
                    result[(f"D{t}", len(queried), bad)] += unit * c ** t
                    break
            else:
                result[("L", len(queried), frozenset())] += unit * c ** length
    assert sum(result.values()) == 1
    coarse = defaultdict(F)
    for (outcome, _, _), probability in result.items():
        coarse[outcome] += probability
    assert all(coarse[key] == value for key, value in law(word, c, d).items())
    return dict(result)


def tv(left, right):
    return sum(abs(left.get(key, 0) - right.get(key, 0)) for key in set(left) | set(right)) / 2


def mix(laws):
    result = defaultdict(F)
    for distribution in laws:
        for key, value in distribution.items():
            result[key] += value / len(laws)
    return dict(result)


def gray_word(d):
    positions = [j ^ (j >> 1) for j in range(1 << d)]
    actions = ["K"]
    for before, after in zip(positions, positions[1:]):
        difference = before ^ after
        assert difference.bit_count() == 1
        actions += list(translation(difference, d)) + ["K"]
    return tuple(actions)


def fixed_case(d):
    size, c = 1 << d, 1 - F(1, 20 * d)
    alternatives, gaps = size - 1, []
    for secret in range(1, size):
        word = witness(secret, d)
        p0 = exhaustive_survival(word, c, d)
        p1 = exhaustive_survival(word, c, d, secret)
        assert p0 == survival(word, c, d) == c ** len(word) / 4
        assert p1 == survival(word, c, d, secret) == c ** len(word) / 2
        gaps.append(p1 - p0)
        for n in range(5):
            for action in ("K", "X", "R0", "R1"):
                repeated = (action,) * n
                expected = c ** n / (2 if action == "K" and n else 1)
                assert exhaustive_survival(repeated, c, d, secret) == expected
                assert exhaustive_survival(repeated, c, d) == expected
        general = ("K", "R0", "K", "R1", "X", "K")
        assert exhaustive_survival(general, c, d, secret) == survival(general, c, d, secret)
        assert exhaustive_survival(general, c, d) == survival(general, c, d)
    assert min(gaps) >= F(1, 5)
    word = gray_word(d)
    records = baseline_latent(word, c, d)
    law0 = law(word, c, d)
    law1 = mix([law(word, c, d, secret) for secret in range(1, size)])
    distance = tv(law0, law1)
    bad = sum(probability * len(b) / alternatives for (_, _, b), probability in records.items())
    dm1 = sum(probability * (distinct - 1) for (_, distinct, _), probability in records.items())
    pairs = sum(probability * F(distinct * (distinct - 1), 2)
                for (_, distinct, _), probability in records.items())
    assert distance <= bad <= dm1 / alternatives <= F(1, alternatives)
    assert pairs <= 2
    return {"d": d, "c": c, "minimum_witness_gap": min(gaps), "gray_word_steps": len(word),
            "transcript_tv": distance, "bad_difference_probability": bad,
            "expected_D_minus_1": dm1, "expected_binomial_D_2": pairs}


def adaptive_case():
    d, c, alternatives = 2, F(39, 40), 3
    first = witness(1, d)

    def target(outcome):
        return 2 if int(outcome[1:]) % 2 else 3

    def policy_law(secret=None):
        result = defaultdict(F)
        for outcome1, p1 in law(first, c, d, secret).items():
            if outcome1 == "L":
                result[(outcome1,)] += p1
            else:
                for outcome2, p2 in law(witness(target(outcome1), d), c, d, secret).items():
                    result[(outcome1, outcome2)] += p1 * p2
        return dict(result)

    law0 = policy_law()
    # Crucial: the same secret parameter is used in both episodes.
    law1 = mix([policy_law(secret) for secret in range(1, 4)])
    expected_n, union, dm1 = 2 - survival(first, c, d), F(0), F(0)
    second_records = {w: baseline_latent(witness(w, d), c, d) for w in (2, 3)}
    for (outcome1, distinct1, bad1), p1 in baseline_latent(first, c, d).items():
        dm1 += p1 * (distinct1 - 1)
        if outcome1 == "L":
            union += p1 * len(bad1) / alternatives
        else:
            for (_, distinct2, bad2), p2 in second_records[target(outcome1)].items():
                union += p1 * p2 * len(bad1 | bad2) / alternatives
                dm1 += p1 * p2 * (distinct2 - 1)
    distance = tv(law0, law1)
    assert distance <= union <= dm1 / alternatives <= expected_n / alternatives
    return {"d": d, "policy": "stop if first episode survives; otherwise select second word by death time",
            "baseline_expected_episodes": expected_n, "joint_transcript_tv": distance,
            "bad_difference_union_probability": union, "sum_expected_D_minus_1": dm1,
            "expected_episodes_over_M": expected_n / alternatives}


def serializable(value):
    if isinstance(value, F):
        return {"exact": str(value), "decimal": float(value)}
    if isinstance(value, dict):
        return {key: serializable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [serializable(item) for item in value]
    return value


if __name__ == "__main__":
    check_translations()
    print(json.dumps(serializable({"alphabet": ["K", "X", "R0", "R1"],
                                   "translation_checks": "all starting points and translations for d=2,3,4,5",
                                   "fixed_episodes": [fixed_case(2), fixed_case(3)],
                                   "adaptive_policy": adaptive_case()}), indent=2))
