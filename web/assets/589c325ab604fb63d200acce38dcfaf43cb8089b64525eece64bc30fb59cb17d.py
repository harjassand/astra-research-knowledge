"""Exact finite diagnostics for the normal-form repetition consequence."""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import json
from pathlib import Path


def text_fraction(x):
    return f"{x.numerator}/{x.denominator}"


def erases(selector):
    # p=1: field elements are their single canonical bits.
    return selector == (1, 1, 1)


selectors = list(product((0, 1), repeat=3))
alpha = F(1, 8)
q = 1 - alpha

# Distinct original component labels 0 and 1. Retain all local selector
# aliases. Both erased bodies coincide, giving a genuine seed collision.
pair_mass = defaultdict(F)
for sa, sb, label in product(selectors, selectors, (0, 1)):
    xa = (sa, 0 if erases(sa) else label)
    yb = (sb, 0 if erases(sb) else label)
    pair_mass[(xa, yb)] += F(1, 128)
assert sum(pair_mass.values()) == 1
mass_x, mass_y = defaultdict(F), defaultdict(F)
for (x, y), prob in pair_mass.items():
    mass_x[x] += prob
    mass_y[y] += prob


def local_witness(view):
    salt, body = view
    return F(0) if erases(salt) else F(1 if body == 0 else -1)


pair_witness = {z: local_witness(z[0]) + local_witness(z[1])
                for z in pair_mass}
cond_x, cond_y = defaultdict(F), defaultdict(F)
for (x, y), prob in pair_mass.items():
    cond_x[x] += prob * pair_witness[(x, y)] / mass_x[x]
    cond_y[y] += prob * pair_witness[(x, y)] / mass_y[y]

eigen_residual = max(abs((cond_x[x] + cond_y[y]) / 2
                         - F(15, 16) * pair_witness[(x, y)])
                     for x, y in pair_mass)
assert eigen_residual == 0
assert sum(prob * pair_witness[z] for z, prob in pair_mass.items()) == 0
assert any(pair_witness.values())
norm_a = sum(prob * local_witness(x)**2 for x, prob in mass_x.items())
norm_b = sum(prob * local_witness(y)**2 for y, prob in mass_y.items())
cov_ab = sum(prob * local_witness(x) * local_witness(y)
             for (x, y), prob in pair_mass.items())
assert norm_a == norm_b == q
assert cov_ab == q*q

# Uniform three-vertex question pairs, equality on diagonals, inequality
# off-diagonal: a synchronous binary-answer game with classical value 7/9.
old_q = (0, 1, 2)
bot = "bottom"
new_q = old_q + (bot,)


def old_accept(x, y, a, b):
    return (a == b) if x == y else (a != b)


def repaired_accept(x, y, a, b):
    if x == y:
        return a == b
    if x != bot and y != bot:
        return old_accept(x, y, a, b)
    return (x != bot or a == 0) and (y != bot or b == 0)


def best_classical_value(questions, law, accept):
    best = F(0)
    for out_a, out_b in product(product((0, 1), repeat=len(questions)),
                                repeat=2):
        strategy_a = dict(zip(questions, out_a))
        strategy_b = dict(zip(questions, out_b))
        value = sum(prob * accept(x, y, strategy_a[x], strategy_b[y])
                    for (x, y), prob in law.items())
        best = max(best, value)
    return best


old_law = {(x, y): F(1, 9) for x, y in product(old_q, repeat=2)}
new_law = {(x, y): q*q*prob for (x, y), prob in old_law.items()}
new_law.update({(x, bot): q*alpha/F(3) for x in old_q})
new_law.update({(bot, y): q*alpha/F(3) for y in old_q})
new_law[(bot, bot)] = alpha*alpha
old_value = best_classical_value(old_q, old_law, old_accept)
new_value = best_classical_value(new_q, new_law, repaired_accept)
assert old_value == F(7, 9)
assert new_value == 1-q*q*(1-old_value) == F(239, 288)
for x, a, b in product(new_q, (0, 1), (0, 1)):
    assert repaired_accept(x, x, a, b) == (a == b)
# In particular, the non-default equal answer must be accepted on the
# erased diagonal. A fixed-answer-only predicate would fail this check.
assert repaired_accept(bot, bot, 1, 1)

# Threshold aggregation needs an additional diagonal check to remain
# strictly synchronous. Exhaustively check that this is a restriction of
# the original threshold, rather than an accidental additional acceptance.
threshold_cases = 0
for xvec, yvec, avec, bvec in product(product(new_q, repeat=2),
                                     product(new_q, repeat=2),
                                     product((0, 1), repeat=2),
                                     product((0, 1), repeat=2)):
    count = sum(repaired_accept(x, y, a, b)
                for x, y, a, b in zip(xvec, yvec, avec, bvec))
    standard = count >= 1
    synchronous = (avec == bvec) if xvec == yvec else standard
    assert not synchronous or standard
    if xvec == yvec:
        assert synchronous == (avec == bvec)
    threshold_cases += 1

selector_counts = []
for field_bits in (1, 3, 5):
    cardinality = 2**field_bits
    # Every canonical first bit is fair. Count the triple event as the
    # product of independently counted one-register events.
    one_count = sum((z >> (field_bits-1)) & 1 for z in range(cardinality))
    chance = F(one_count**3, cardinality**3)
    assert chance == alpha
    selector_counts.append({"field_bits": field_bits,
                            "field_cardinality": cardinality,
                            "one_bit_count": one_count,
                            "triple_event_probability": text_fraction(chance)})

rate = F(1, 16)*F(49, 64)**3/F(1024)
assert rate == F(117649, 2**32)
threshold_rate = F(1, 16)*(F(49, 64)/2)**3/F(1024)
honest_rate = 2*(F(49, 64)/2)**2
assert threshold_rate == F(117649, 2**35)
assert honest_rate == F(2401, 8192)
report = {
    "status": "PASS_EXACT_SCOPED_DIAGNOSTICS",
    "decorated_sampler": {
        "seed_count": 128,
        "positive_pair_count": len(pair_mass),
        "positive_local_question_counts": [len(mass_x), len(mass_y)],
        "nonconstant_eigenvalue": "15/16",
        "eigen_residual": text_fraction(eigen_residual),
        "local_norm_squared": text_fraction(norm_a),
        "cross_covariance": text_fraction(cov_ab),
        "maximal_correlation_witness": "7/8",
        "exact_gap_combining_upper_witness_and_analytic_bound": "1/16",
    },
    "strict_synchrony_value_fixture": {
        "original_classical_value": text_fraction(old_value),
        "wrapped_classical_value": text_fraction(new_value),
        "affine_value_residual": "0/1",
        "erased_diagonal_nondefault_equal_answers_accept": True,
    },
    "canonical_selector_counts": selector_counts,
    "cubic_rate_coefficient_before_epsilon_and_answer_factor": text_fraction(rate),
    "threshold_diagonal_repair": {
        "enumerated_cases": threshold_cases,
        "acceptance_is_subset_of_standard_threshold": True,
        "strict_synchrony": True,
        "soundness_rate_before_gap_and_answer_factor": text_fraction(threshold_rate),
        "honest_rate_before_gap_factor": text_fraction(honest_rate),
    },
    "scope": "Finite exact checks; not universal proof, commuting-value computation, or external validation."
}
out = Path(__file__).with_name("repetition_attack_check.json")
out.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
