"""Exact rational tests of same-edge block gates outside the XXZ LC cone."""
from fractions import Fraction as F


def p2(x):
    return 1 + x + x*x/2


def sector_values(alpha, gamma, kappa, s):
    # Eigenvalues of I+s(kappa I + alpha(XX+YY)+gamma ZZ).
    return (
        1 + s*(kappa + gamma),
        1 + s*(kappa - gamma + 2*alpha),
        1 + s*(kappa - gamma - 2*alpha),
    )


def q_weights_from_sector(v0, vp, vm):
    return v0, (vp + vm)/2, (vp - vm)/2


def main():
    alpha, kappa, s = F(1), F(10), F(1, 10)
    results = []
    for gamma in (F(1), F(11, 10), F(-1), F(-11, 10)):
        v0, vp, vm = sector_values(alpha, gamma, kappa, s)
        for power in (1, 2, 3, 5, 8):
            a, b, c = q_weights_from_sector(v0**power, vp**power, vm**power)
            # Outside the upper side, a > b+c=vp^power; outside the lower
            # side, b-c=vm^power > a.
            upper_slack = a - b - c
            lower_slack = b - c - a
            if gamma > alpha:
                assert upper_slack > 0
            elif gamma < -alpha:
                assert lower_slack > 0
            else:
                assert upper_slack == 0 if gamma == alpha else lower_slack == 0
            results.append({
                "gamma": str(gamma), "power": power,
                "eigenvalues_F": [str(v0), str(vp), str(vm)],
                "weights_a_b_c": [str(a), str(b), str(c)],
                "upper_triangle_slack_a_minus_b_minus_c": str(upper_slack),
                "lower_triangle_slack_b_minus_c_minus_a": str(lower_slack),
            })

    p2_results = []
    for gamma in (F(11, 10), F(-11, 10)):
        v0arg = kappa + gamma
        vparg = kappa - gamma + 2*alpha
        vmarg = kappa - gamma - 2*alpha
        a, b, c = q_weights_from_sector(p2(v0arg), p2(vparg), p2(vmarg))
        if gamma > alpha:
            assert a - b - c == p2(v0arg) - p2(vparg) > 0
        else:
            assert b - c - a == p2(vmarg) - p2(v0arg) > 0
        p2_results.append({
            "gamma": str(gamma), "shift": str(kappa),
            "p2_arguments": [str(v0arg), str(vparg), str(vmarg)],
            "weights_a_b_c": [str(a), str(b), str(c)],
            "violated_triangle_slack": str(a-b-c if gamma > alpha else b-c-a),
        })

    # A second-order consistent local approximation remains outside-LC for
    # sufficiently small step on every strict outside fixture.  Here the
    # scalar gate is f_h(x)=1+h*x+(h*x)^2/2.
    small_step_results = []
    for gamma in (F(11, 10), F(-11, 10)):
        x0, xp, xm = kappa + gamma, kappa - gamma + 2*alpha, kappa - gamma - 2*alpha
        for step in (F(1, 10), F(1, 100), F(1, 1000)):
            f = lambda x: 1 + step*x + (step*x)**2/2
            a, b, c = q_weights_from_sector(f(x0), f(xp), f(xm))
            slack = a-b-c if gamma > alpha else b-c-a
            assert slack > 0
            small_step_results.append({
                "gamma": str(gamma), "step": str(step),
                "first_order_outside_difference": str(step*(2*(gamma-alpha) if gamma > alpha else -2*(gamma+alpha))),
                "violated_triangle_slack": str(slack),
            })

    j = (F(1), F(1), F(11, 10))
    sorted_sv = sorted(j, reverse=True)
    assert sorted_sv[0] > sorted_sv[1] == sorted_sv[2]
    print({"power_gate_checks": results})
    print({"second_order_gate_checks": p2_results})
    print({"small_step_consistent_gate_checks": small_step_results})
    print({"local_unitary_invariant": {
        "outside_cone_singular_values": [str(x) for x in sorted_sv],
        "unique_largest": sorted_sv[0] > sorted_sv[1],
        "target_easy_plane_requires_two_equal_largest": True,
    }})
    print({"status": "PASS", "exact_rational_cases": len(results)+len(p2_results)+len(small_step_results)})


if __name__ == "__main__":
    main()
