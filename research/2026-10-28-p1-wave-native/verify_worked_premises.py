"""Own exact-arithmetic diagnostics of worked premises, not archived-script replay."""
from fractions import Fraction as Q
import json
from pathlib import Path


def product(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def main():
    # A noncommuting time-dependent symmetric lens is allowed by the affine
    # algebra. These sampled rational substitutions are diagnostics; the
    # general proof is the block computation in THREE_DISPLAYED_IDENTITIES.
    substitutions = []
    for t in (Q(-1, 3), Q(0), Q(2, 5)):
        k = [[t, Q(1)], [Q(1), t*t]]
        kp = [[Q(1), Q(0)], [Q(0), 2*t]]
        b = [[Q(0)]*5 for _ in range(5)]
        bp = [[Q(0)]*5 for _ in range(5)]
        m = [[Q(0)]*5 for _ in range(5)]
        for i in range(2):
            b[i][i+2] = Q(1)
            for j in range(2):
                b[i+2][j] = -k[i][j]
                bp[i+2][j] = -kp[i][j]
                m[i][j] = m[i+2][j+2] = k[i][j]
                m[i+2][j] = kp[i][j]
        bb = product(b, b)
        assert all(bp[i][j]+bb[i][j]+m[i][j] == 0 for i in range(5) for j in range(5))
        assert sum(b[i][i] for i in range(5)) == 0
        assert all(x == 0 for x in m[4])
        substitutions.append(str(t))

    # Two atoms with a=1, w=(1,0,0),(0,2,0), b=2,-3.
    # T=diag(1,4,0), R=(4,-12,0), e=13; the singular bound is sharp.
    r = [Q(4), Q(-12), Q(0)]
    tp = [Q(1), Q(1, 4), Q(0)]
    value = sum(x*x*y for x, y in zip(r, tp))
    assert value == 4*13 == 52
    # For any actually supplied curve of arclength <=3, the proof's trace
    # budget is <=14. This is a bound, not a measured resolving-window cost.
    trace_budget = 2+4*3
    assert trace_budget == 14
    output = {
        "scope": "Owner-derived exact substitutions and worked uses of accepted conditional premises; not a proof by fixtures, wave-archive replay, physical acquisition or advantage test.",
        "affine_block_identity_rational_times": substitutions,
        "moment_example": {"T_diagonal": [1, 4, 0], "R": [4, -12, 0], "e": 13,
                           "R_Tplus_R": int(value), "upper_bound_4e": 52,
                           "enabled": "Use a singular stress moment without imposing an artificial positive eigenvalue floor; actual amplitude/moment model still required."},
        "curve_example": {"supplied_arclength_upper_bound": 3, "trace_upper_bound": trace_budget,
                          "enabled": "Cover the supplied continuum of rank-one resolving states by one explicit positive operator; no finite grid surrogate or uncharged orbit acquisition."},
    }
    target = Path(__file__).resolve().parent / "evaluation/WORKED_PREMISES.json"
    target.write_text(json.dumps(output, indent=2)+"\n")
    print("Exact worked-premise diagnostics passed; mathematical scope only.")


if __name__ == "__main__":
    main()
