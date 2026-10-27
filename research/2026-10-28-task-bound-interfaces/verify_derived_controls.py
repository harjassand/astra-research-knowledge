"""Independent exact finite controls; no imported scientific program or experiment."""
from fractions import Fraction as F
import json
from pathlib import Path


def main():
    checks = []
    for lower, upper, threshold, expected in (
        (F(1), F(2), F(2), "all_true"),
        (F(1), F(2), F(0), "all_false"),
        (F(1), F(2), F(1), "unresolved"),
        (F(0), F(2), F(1, 2), "unresolved"),
    ):
        result = "all_true" if upper <= threshold else "all_false" if lower > threshold else "unresolved"
        assert result == expected
        checks.append(dict(control="threshold boundary", lower=str(lower), upper=str(upper),
                           threshold=str(threshold), result=result))

    # The loose enclosure straddles, but the true singleton task is always one.
    assert not F(1) <= F(1, 2)
    checks.append(dict(control="a loose straddling enclosure does not prove two witnesses"))

    # Both hidden states retain positive conditional support after either Y.
    joint = {(s, y): F(9, 20) if s == y else F(1, 20) for s in (0, 1) for y in (0, 1)}
    posterior_risk = sum(min(joint[s, y] for s in (0, 1)) for y in (0, 1))
    assert all(p > 0 for p in joint.values()) and posterior_risk == F(1, 10) < F(1, 2)
    checks.append(dict(control="unchanged support with improved Bayes risk", before="1/2", after=str(posterior_risk)))

    weights = ((F(9, 20), F(9, 20)), (F(1, 20), F(1, 20)))
    total = sum(sum(row) for row in weights)
    current = max(sum(row) for row in weights)
    perfect = sum(max(weights[s][mu] for s in (0, 1)) for mu in (0, 1))
    benefit, absolute_error = (perfect - current) / total, 1 - current / total
    assert benefit == 0 and absolute_error == F(1, 10)
    checks.append(dict(control="zero remaining modeled benefit with nonzero absolute error",
                       benefit=str(benefit), absolute_error=str(absolute_error)))

    error = F(1, 100) + F(2, 3) * F(1, 200) + F(1, 3) * F(1, 400)
    assert error == F(17, 1200)
    checks.append(dict(control="all three absolute correlation errors are paid", error=str(error)))

    assert F(63, 1024) < F(1, 16) < F(33, 512)
    checks.append(dict(control="actual signed-task endpoints straddle 1/16"))

    regret_bound = F(2) ** 2 / (2 * F(4))
    assert regret_bound == F(1, 2) <= F(3, 5)
    checks.append(dict(control="conditional gradient-regret premise enables a tolerance decision",
                       bound=str(regret_bound), tolerance="3/5",
                       qualification="G=2 and mu=4 are illustrative supplied warranted bounds, not acquired measurements"))

    output = dict(scope="Independent finite exact controls of signs, qualifications and arithmetic. These do not acquire any scientific input, replay an archive program, certify general retrieval, establish a physical effect or replace the complete mathematical proofs.",
                  result="passed", checks=checks)
    Path(__file__).with_name("DERIVED_CONTROLS.json").write_text(json.dumps(output, indent=2) + "\n")
    print(len(checks), "exact controls passed")


if __name__ == "__main__":
    main()
