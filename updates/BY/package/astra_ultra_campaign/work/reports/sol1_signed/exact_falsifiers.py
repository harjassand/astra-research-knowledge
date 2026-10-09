"""Exact rational checks of two indispensable interpolation hypotheses.

This verifies form-level falsifiers, not the all-state amplifier EPnI.
No third-party packages or finite-Fock approximation are involved.
"""

from fractions import Fraction as Q
from pathlib import Path


def weights(r, v, orientation):
    r = Q(r)
    v = Q(v)
    assert v.denominator == 1 and v != 0
    q = (r + 1) / r
    qv = q ** int(v)
    b = v * (qv + 1) / (2 * (qv - 1))
    arithmetic = (b + v / 2, b - v / 2)
    if orientation == "down":
        assert v != 1
        metric = (b - (r + Q(1, 2)) * v) / (1 - v)
        constants = (r, r + 1)
    else:
        assert orientation == "up" and v != -1
        metric = (b + (r + Q(1, 2)) * v) / (1 + v)
        constants = (r + 1, r)
    return arithmetic + constants, metric


def creation_orientation_falsifier():
    source, f0 = weights(1, -5, "down")
    a, fa = weights(Q(1, 10), -2, "down")
    b, fb = weights(Q(1, 10), -2, "up")
    _, fb_wrong = weights(Q(1, 10), -2, "down")
    wa, wb = Q(7, 4), Q(3, 4)
    target = tuple(wa * x + wb * y for x, y in zip(a, b))
    assert all(x <= y for x, y in zip(target, source))
    correct = wa * fa + wb * fb
    wrong = wa * fa + wb * fb_wrong
    assert correct == Q(103, 72) <= f0 == Q(105, 62)
    assert wrong == Q(133, 72) > f0
    return {
        "source_four_weights": source,
        "target_four_weights": target,
        "source_metric": f0,
        "oriented_target": correct,
        "wrong_target": wrong,
        "wrong_excess": wrong - f0,
    }


def multiplier_invariance_falsifier():
    p, fp = weights(1, 10, "down")
    m, fm = weights(1, -10, "down")
    a, fa = weights(1, -4, "down")
    source = tuple(x + y for x, y in zip(p, m))
    target = tuple(2 * x for x in a)
    assert all(x <= y for x, y in zip(target, source))
    source_metric = fp + fm
    target_metric = 2 * fa
    assert source_metric == Q(296650, 101277)
    assert target_metric == Q(248, 75) > source_metric
    return {
        "source_four_weights": source,
        "target_four_weights": target,
        "source_metric": source_metric,
        "target_metric": target_metric,
        "excess": target_metric - source_metric,
    }


def main():
    records = {
        "creation_orientation": creation_orientation_falsifier(),
        "multiplier_invariance": multiplier_invariance_falsifier(),
    }
    lines = ["PASS: both exact rational falsifiers verified."]
    for name, record in records.items():
        lines.append("\n" + name)
        for key, value in record.items():
            if isinstance(value, tuple):
                value = ", ".join(str(x) for x in value)
            lines.append(f"{key}: {value}")
    output = "\n".join(lines) + "\n"
    Path(__file__).with_name("exact_falsifiers_result.txt").write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
