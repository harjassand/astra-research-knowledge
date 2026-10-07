"""Exact independent check of a quadratic robust certificate.

The network has 0 <-> A, 0 <-> B, A <-> A+B, B <-> A+B; each of the
eight reaction rates is independently predictable in [1,2].  The derivation
and its limits are recorded in CROSS_PHASE_AUDIT.txt.
"""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


# (reactant, product, lower rate, upper rate, label)
REACTIONS = [
    ((0, 0), (1, 0), F(1), F(2), "0->A"),
    ((1, 0), (0, 0), F(1), F(2), "A->0"),
    ((0, 0), (0, 1), F(1), F(2), "0->B"),
    ((0, 1), (0, 0), F(1), F(2), "B->0"),
    ((1, 0), (1, 1), F(1), F(2), "A->A+B"),
    ((1, 1), (1, 0), F(1), F(2), "A+B->A"),
    ((0, 1), (1, 1), F(1), F(2), "B->A+B"),
    ((1, 1), (0, 1), F(1), F(2), "A+B->B"),
]


def falling(x, y):
    out = 1
    for xi, yi in zip(x, y):
        if xi < yi:
            return 0
        for k in range(yi):
            out *= xi-k
    return out


def potential(x):
    return x[0]*x[0] + x[1]*x[1]


def generator(x, rates):
    v0 = potential(x)
    total = F(0)
    for k, (y, yp, _, _, _) in zip(rates, REACTIONS):
        prop = falling(x, y)
        if not prop:
            continue
        target = tuple(xi-yi+y_i for xi, yi, y_i in zip(x, y, yp))
        total += k*prop*(potential(target)-v0)
    return total


def ceil_fraction(x):
    return (x.numerator+x.denominator-1)//x.denominator


def certificate_constants():
    # All intervals are [1,2].  The generic derivation uses these endpoint
    # combinations and is valid pointwise for every rate vector in the box.
    imm_a = imm_b = cat_a = cat_b = F(2)
    death_a = death_b = rev_a = rev_b = F(1)
    c0 = imm_a+imm_b
    ca = 2*imm_a+death_a+cat_a
    cb = 2*imm_b+death_b+cat_b
    delta = min(death_a, death_b)
    beta = min(rev_a, rev_b)
    cross = 2*cat_a+2*cat_b+rev_a+rev_b
    threshold = max(1, ceil_fraction(cross/(2*beta)))
    large_b = c0+(ca*ca+cb*cb)/(2*delta)
    small_max = threshold-1
    small_b = (c0+max(ca, cb)*small_max
               + cross*F(small_max*small_max, 4))
    B = max(large_b, small_b)
    # Independent simplifications expected from the displayed [1,2] box.
    assert (c0, ca, cb, delta, beta, cross, threshold) == (4, 7, 7, 1, 1, 10, 5)
    assert large_b == 53 and small_b == 72 and B == 72
    return {
        "c0": c0, "c_a": ca, "c_b": cb, "delta": delta,
        "beta": beta, "cross": cross, "large_threshold": threshold,
        "B_large": large_b, "B_small": small_b, "B": B,
    }


def path_from_core(x, q, count_cap):
    """Drain by unary deaths, then make q A and q B by zero-source births."""
    state = list(x)
    steps = 0
    max_count = sum(state)
    while state[0] or state[1]:
        i = 0 if state[0] else 1
        state[i] -= 1
        steps += 1
        max_count = max(max_count, sum(state))
    assert state == [0, 0]
    for _ in range(q):
        state[0] += 1
        steps += 1
        max_count = max(max_count, sum(state))
    for _ in range(q):
        state[1] += 1
        steps += 1
        max_count = max(max_count, sum(state))
    assert state == [q, q]
    assert steps <= count_cap["H"]
    assert max_count <= count_cap["D"]
    return steps, max_count


def exact_checks():
    cert = certificate_constants()
    corners = [tuple(F(v) for v in bits) for bits in product((1, 2), repeat=8)]
    checked = 0
    max_gap = None
    for a, b in product(range(13), repeat=2):
        x = (a, b)
        for rates in corners:
            drift = generator(x, rates)
            gap = F(72)-potential(x)-drift
            assert gap >= 0, (x, rates, drift, gap)
            max_gap = gap if max_gap is None else min(max_gap, gap)
            checked += 1

    # A fixed rate point in the box is not complex balanced.  The four
    # complex-balance equations for c=(c_A,c_B) are checked by contradiction:
    # 0 gives c_A+c_B=2; A and B give 2c_A=1+c_A*c_B and
    # 3c_B=1+c_A*c_B.  These force (c_A,c_B)=(6/5,4/5), which violates A.
    c_a, c_b = F(6, 5), F(4, 5)
    assert c_a+c_b == 2
    assert 2*c_a != 1+c_a*c_b

    R = 73  # ceil((B+1)/delta); outside V<=R, drift <= -1.
    Ncore = 13  # ceil(sqrt(2R)); a+b <= Ncore whenever V<=R.
    q = 2
    D = max(Ncore, 2*q)
    U = sum(r[3] for r in REACTIONS)
    Q = U*(D+1)**2
    ell = min(r[2] for r in REACTIONS)
    alpha = ell/(2*Q)
    H = Ncore+2*q
    p = alpha**H
    t0 = F(H, Q)
    hit_constant = (F(R)+(cert["B"]+1)*t0)/p
    assert (U, Q, ell, alpha, H, t0) == (16, 3136, 1, F(1, 6272), 17, F(17, 3136))
    assert hit_constant == F(230169, 3136)/(F(1, 6272)**17)

    # Check the acquired molecular path from every lattice point in the core.
    path_states = 0
    max_steps = 0
    for a, b in product(range(Ncore+1), repeat=2):
        if potential((a, b)) <= R:
            steps, cap = path_from_core((a, b), q, {"H": H, "D": D})
            assert cap <= D
            max_steps = max(max_steps, steps)
            path_states += 1

    return {
        "method": "exact Fraction generator at all rate-box corners on a bounded state grid",
        "rate_box": "each of eight rates independently in [1,2]",
        "certificate": {k: str(v) for k, v in cert.items()},
        "finite_corner_state_checks": checked,
        "minimum_checked_drift_slack": str(max_gap),
        "noncomplex_balanced_rate_point": {
            "rates": ["1", "1", "1", "1", "1", "1", "2", "1"],
            "forced_equilibrium_candidate": [str(c_a), str(c_b)],
            "complex_balance_residuals_A_B": [
                str(2*c_a-(1+c_a*c_b)), str(3*c_b-(1+c_a*c_b))],
        },
        "recovery_certificate": {
            "target": "a>=2 and b>=2",
            "core_potential_threshold": R,
            "count_cap": Ncore,
            "path_count_cap": D,
            "total_rate_cap": str(Q),
            "one_step_probability": str(alpha),
            "attempt_steps": H,
            "attempt_duration": str(t0),
            "attempt_success_probability": str(p),
            "expected_hit_upper_bound": "a^2+b^2 + " + str(hit_constant),
        },
        "core_path_states_checked": path_states,
        "max_checked_witness_steps": max_steps,
        "scope": "diagnostics support the symbolic bound; no simulation or generic synthesis claim",
    }


if __name__ == "__main__":
    out = exact_checks()
    dest = Path(__file__).with_name("quadratic_cross_foster_checks.json")
    dest.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps({
        "checks": out["finite_corner_state_checks"],
        "core_path_states": out["core_path_states_checked"],
        "B": out["certificate"]["B"],
        "drift_slack": out["minimum_checked_drift_slack"],
        "recovery": out["recovery_certificate"],
        "output": str(dest),
    }, indent=2))
