"""Exact Euclidean-ball selector counterexamples for d=2 and d=3.

The checker is independent of fractional_selector_probe.py. It uses Fraction
arithmetic, explicitly enumerates all sign/noise endpoint plays, and uses
convexity of the Euclidean ball to lift endpoint checks to the full interval
zeta in [-1/2,1/2].
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
G=F(1,2)
R=F(11,10)
SIGNS=(-1,1)
NOISE=(-G,G)


def add_scaled(s,c,v):
    return tuple(x+c*y for x,y in zip(s,v))


def sqnorm(s):
    return sum(x*x for x in s)


def safe(s):
    return sqnorm(s)<=R*R


def terminal_states(s,epsilon,v):
    return [add_scaled(s,F(epsilon)+z,v) for z in NOISE]


def winning_last_action(s,v):
    if not safe(s):
        return []
    return [e for e in SIGNS if all(safe(q) for q in terminal_states(s,e,v))]


def txt(x):
    return str(x)


def enc(s):
    return [txt(x) for x in s]


def analyze(d,v1,v2,low,witness_a,witness_b,high):
    zero=tuple(F(0) for _ in range(d))
    first={e:terminal_states(zero,e,v1) for e in SIGNS}
    assert all(safe(s) for branch in first.values() for s in branch)

    # Directly enumerate the complete endpoint disturbance game.
    second_witnesses={}
    for s in sorted({q for branch in first.values() for q in branch}):
        acts=winning_last_action(s,v2)
        if acts:
            second_witnesses[txt(s)]=[
                {"epsilon":e,"terminal_states":[enc(q) for q in terminal_states(s,e,v2)]}
                for e in acts]
    exact_root_actions=[]
    for e,branch in first.items():
        if all(txt(s) in second_witnesses for s in branch):
            exact_root_actions.append(e)
    assert not exact_root_actions

    # W_2 is the full continuous-noise last-step viability set. Endpoint
    # checks suffice here because the entire scalar successor segment is convex.
    assert safe(witness_a) and safe(witness_b)
    assert winning_last_action(witness_a,v2)
    assert winning_last_action(witness_b,v2)
    assert tuple((a+b)/2 for a,b in zip(witness_a,witness_b))==low
    assert safe(high) and winning_last_action(high,v2)
    assert safe(low) and not winning_last_action(low,v2)
    low_failures=[]
    for e in SIGNS:
        terminals=terminal_states(low,e,v2)
        failed=[q for q in terminals if not safe(q)]
        assert failed
        low_failures.append({
            "epsilon":e,
            "endpoint_states":[enc(q) for q in terminals],
            "endpoint_squared_norms":[txt(sqnorm(q)) for q in terminals],
            "endpoint_safe":[safe(q) for q in terminals],
        })
    neg=lambda s:tuple(-x for x in s)
    assert safe(neg(witness_a)) and winning_last_action(neg(witness_a),v2)
    assert safe(neg(witness_b)) and winning_last_action(neg(witness_b),v2)
    assert tuple((a+b)/2 for a,b in zip(neg(witness_a),neg(witness_b)))==neg(low)

    # Every first-sign endpoint lies in conv(W_2): the high state is in W_2;
    # the low state is an explicit midpoint of two W_2 states. The negative
    # branch follows from symmetry. Yet low itself is not in W_2.
    hull_membership=[]
    for e,branch in first.items():
        flags=[]
        for s in branch:
            if s==high or s==neg(high):
                flags.append("in_W2")
            elif s==low:
                flags.append("midpoint_of_W2_witnesses")
            elif s==neg(low):
                flags.append("midpoint_of_negative_W2_witnesses")
            else:
                raise AssertionError((s,low,high))
        hull_membership.append({"epsilon":e,"successors":[enc(s) for s in branch],
                                "convex_hull_membership_witness":flags})

    return {
        "dimension":d,
        "gamma":txt(G),
        "safe_set":"Euclidean ball ||s||_2 <= 11/10 at every round boundary",
        "safe_radius_squared":txt(R*R),
        "directions":[enc(v1),enc(v2)],
        "v1_norm_squared":txt(sqnorm(v1)),
        "full_last_round_viability_definition":"W_2={s: ||s||_2<=11/10 and for some epsilon in {-1,+1}, both s+(epsilon-1/2)v2 and s+(epsilon+1/2)v2 lie in the ball}",
        "reachable_first_round_successors_by_sign":{str(e):[enc(s) for s in branch] for e,branch in first.items()},
        "reachable_second_round_winners_with_actions":second_witnesses,
        "low_losing_state":enc(low),
        "low_state_squared_norm":txt(sqnorm(low)),
        "low_state_is_in_W2":False,
        "low_state_second_round_failures":low_failures,
        "why_low_state_loses":"For each second sign, one endpoint successor has squared norm greater than (11/10)^2.",
        "convex_hull_witness_for_low_state":{"state_a_in_W2":enc(witness_a),"state_b_in_W2":enc(witness_b),"weights":["1/2","1/2"]},
        "convex_hull_witness_action_options":{"state_a_actions":winning_last_action(witness_a,v2),"state_b_actions":winning_last_action(witness_b,v2)},
        "high_winning_state":enc(high),
        "high_state_squared_norm":txt(sqnorm(high)),
        "high_state_is_in_W2":True,
        "convex_hull_membership_of_root_successors":hull_membership,
        "fractional_hull_selector_accepts_root_actions":list(SIGNS),
        "exact_continuous_game_winning_root_actions":exact_root_actions,
        "root_is_exactly_losing":True,
    }


results=[
    analyze(2,
        (F(1,2),F(1,2)),(F(1),F(0)),
        (F(1,4),F(1,4)),(F(1),F(1,4)),(F(-1,2),F(1,4)),
        (F(3,4),F(3,4))),
    analyze(3,
        (F(1,2),F(1,2),F(1,10)),(F(1),F(0),F(0)),
        (F(1,4),F(1,4),F(1,20)),(F(1),F(1,4),F(1,20)),(F(-1,2),F(1,4),F(1,20)),
        (F(3,4),F(3,4),F(3,20))),
]
receipt={
    "status":"exact Euclidean counterexamples to selector closure of pointwise convexified viability",
    "method":"independent direct endpoint-game enumeration with exact Fraction arithmetic; exact last-step interval safety follows from convexity of the Euclidean ball",
    "scope":"two-step rational d=2 and d=3 schedules in the unit ball, gamma=1/2, Euclidean radius 11/10; all-prefix round-boundary safety",
    "claim_limit":"This rejects the pointwise convex-hull completion relaxation, not every compact polytope, every separation oracle, or all polynomial-time controllers.",
    "results":results,
}
(OUT/"euclidean_selector_exact_receipt.json").write_text(json.dumps(receipt,indent=2))
print(json.dumps(receipt,indent=2))
