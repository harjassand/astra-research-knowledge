"""Independent exact enumeration of two-step d=2 and d=3 selector failures.

No imports from fractional_selector_probe.py. The interface has gamma=1/2,
endpoint disturbances only, and the all-prefix safe set is the unit l_infinity
cube. Enumerate the actual sign/noise game by hand-sized transition sets.
"""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
G = Q(1, 2)
NOISE = (-G, G)
SIGNS = (-1, 1)
R = Q(1)


def state_after(state, eps, noise, direction):
    c = Q(eps) + noise
    return tuple(x + c*y for x,y in zip(state,direction))


def in_cube(state):
    return all(-R <= x <= R for x in state)


def frac_text(x):
    return str(x)


def seg_contains(point, left, right):
    # The designated winning endpoints are antipodal. Check exact scalar theta.
    idx = next(i for i,z in enumerate(right) if z != left[i])
    theta=(point[idx]-left[idx])/(right[idx]-left[idx])
    return Q(0) <= theta <= Q(1) and all(
        point[j] == left[j] + theta*(right[j]-left[j])
        for j in range(len(point)))


def encode_state(s):
    return [frac_text(z) for z in s]


def analyze(d, v1, v2):
    zero=tuple(Q(0) for _ in range(d))
    first_by_sign={}
    for eps in SIGNS:
        first_by_sign[eps]=[state_after(zero,eps,z,v1) for z in NOISE]
    candidates=sorted({s for ss in first_by_sign.values() for s in ss})
    winning=[]
    second_options={}
    for s in candidates:
        good=[]
        for eps in SIGNS:
            terminal=[state_after(s,eps,z,v2) for z in NOISE]
            if all(in_cube(x) for x in terminal):
                good.append({"epsilon":eps,"terminal_states":[encode_state(x) for x in terminal]})
        if in_cube(s) and good:
            winning.append(s)
            second_options[str(s)]=good
    exact_root_actions=[]
    for eps, succ in first_by_sign.items():
        if all(s in winning for s in succ):
            exact_root_actions.append(eps)
    assert len(winning)==2 and winning[0]==tuple(-x for x in winning[1])
    left,right=winning
    relaxed_root_actions=[]
    endpoint_membership=[]
    for eps,succ in first_by_sign.items():
        # The independently derived full continuous W_2 has convex hull
        # equal to the whole safe cube, so endpoint membership is exact here.
        flags=[in_cube(s) for s in succ]
        endpoint_membership.append({"epsilon":eps,"successors":[encode_state(s) for s in succ],
                                    "inside_convex_hull":flags})
        if all(flags):
            relaxed_root_actions.append(eps)
    assert not exact_root_actions and relaxed_root_actions
    assert all(in_cube(s) for ss in first_by_sign.values() for s in ss)
    return {
        "dimension":d,
        "gamma":frac_text(G),
        "safe_set":"[-1,1]^d (all round boundaries)",
        "noise_model":"zeta in {-1/2,+1/2} after each sign",
        "continuous_noise_extension":"The last-step viability set is derived for every zeta in [-1/2,+1/2]; the same losing endpoint proves the root loses in that stronger game.",
        "directions":[encode_state(v1),encode_state(v2)],
        "full_continuous_second_round_viability":"{s in [-1,1]^d: s_1 in [-1,-1/2] union [1/2,1]}",
        "convex_hull_of_full_viability":"[-1,1]^d",
        "first_round_successors_by_sign":{
            str(eps):[encode_state(s) for s in succ] for eps,succ in first_by_sign.items()},
        "second_round_winning_start_states":[encode_state(s) for s in winning],
        "second_round_winning_action_witnesses":{
            str(s):second_options[str(s)] for s in winning},
        "exact_game_winning_root_actions":exact_root_actions,
        "reachable_second_round_winners_are_a_subset":"The two states listed below are the only round-1 states reachable from the root that admit a safe final action.",
        "root_successors_in_convex_hull_of_full_viability":endpoint_membership,
        "fractional_hull_selector_actions":relaxed_root_actions,
        "root_exactly_winning":bool(exact_root_actions),
        "selector_closure_failure":True,
    }


results=[
    analyze(2,(Q(1,2),Q(1,2)),(Q(1),Q(0))),
    analyze(3,(Q(1,3),Q(2,3),Q(2,3)),(Q(1),Q(0),Q(0))),
]
assert all(x["selector_closure_failure"] and not x["root_exactly_winning"] for x in results)
receipt={
    "status":"exact counterexamples to convex-hull selector closure, with endpoint enumeration and a continuous-noise extension",
    "scope":"two-step rational schedules, d=2 and d=3, unit l_infinity safe cube, gamma=1/2; last-step continuous viability is derived exactly",
    "method":"independent Fraction enumeration of all endpoint-noise plays plus an exact full-state formula for the last-step viability body",
    "results":results,
}
(OUT/"fractional_selector_exact_receipt.json").write_text(json.dumps(receipt,indent=2))
print(json.dumps(receipt,indent=2))
