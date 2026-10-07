"""Exact raw-generator counterexample to a naive fourth-layer product.

This rejects this ansatz, not recurrence or all possible fourth-layer V.
"""
from fractions import Fraction as F
import json
import pathlib


def valid_three_layer_v(a, b, c):
    return (F(29, 3) * a + F(13, 3) * (1 + F(1, a + 1)) * b
            + (1 + F(5, 6) / ((a + 5) * (b + 1))) * c)


def candidate_v(state):
    a, b, c, d = state
    return valid_three_layer_v(a, b, c) + (1 + F(1, (a + 1) * (b + 1)
                                                 * (c + 1))) * d


def raw_generator(state):
    a, b, c, d = state
    # Each pair is source, target, propensity in the four-species lattice.
    reactions = [
        ((0, 0, 0, 0), (1, 0, 0, 0), 1),
        ((1, 0, 0, 0), (0, 0, 0, 0), a),
        ((1, 0, 0, 0), (1, 1, 0, 0), a),
        ((1, 1, 0, 0), (1, 0, 0, 0), a * b),
        ((0, 1, 0, 0), (0, 1, 1, 0), b),
        ((0, 1, 1, 0), (0, 1, 0, 0), b * c),
        ((0, 0, 1, 0), (0, 0, 1, 1), c),
        ((0, 0, 1, 1), (0, 0, 1, 0), c * d),
    ]
    value = candidate_v(state)
    terms = []
    for source, target, intensity in reactions:
        if intensity == 0:
            continue
        new = tuple(x + z - y for x, y, z in zip(state, source, target))
        term = intensity * (candidate_v(new) - value)
        terms.append({"source": source, "target": target,
                      "intensity": intensity, "term": str(term)})
    return sum(F(z["term"]) for z in terms), terms


if __name__ == "__main__":
    n = 100
    state = (n, n, 0, n**4)
    lv, terms = raw_generator(state)
    assert lv > 0
    # Exact analytic coefficient of D at A=B=n,C=0, all shifts one.
    p = F(1, (n + 1)**2)
    lp = p * (-F(1, n + 2) + 1 - F(n, n + 2) + n - F(n, 2))
    assert lp > 0
    report = {"status": "EXACT_ANSATZ_REFUTATION",
              "network": "0<->A, A<->A+B, B<->B+C, C<->C+D; all rates 1",
              "state": state, "candidate_V": str(candidate_v(state)),
              "raw_LV": str(lv), "coefficient_of_D": str(lp),
              "raw_reaction_terms": terms,
              "scope": "Naive product reciprocal fourth-layer V only"}
    path = pathlib.Path(__file__).with_name("four_layer_product_counterexample.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items()
                      if k != "raw_reaction_terms"}, indent=2))
