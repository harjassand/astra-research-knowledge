"""Exact rational branch check for adaptive safe-behavior acquisition.

The output dynamics are z' = G u + e, with K=[0,1], U=[0,1]^2,
E=[0,1/20], and three possible row maps.  The disturbance is observed and
subtracted for identification, but the full E is charged in every safety
check.  This is a finite test of the branch geometry, not a proof of the
general polyhedral theorem.
"""
from fractions import Fraction as Q

MODELS = {
    "a": (Q(1, 2), Q(1, 4)),
    "b": (Q(1, 2), Q(3, 4)),
    "c": (Q(0), Q(-1, 4)),
}
E_MAX = Q(1, 20)
K_LO, K_HI = Q(0), Q(1)
U_LO, U_HI = Q(0), Q(1)


def image(g, u):
    return sum((gi * ui for gi, ui in zip(g, u)), Q(0))


def robustly_safe(u, models):
    if any(not (U_LO <= ui <= U_HI) for ui in u):
        return False
    for g in models:
        lo = image(g, u)  # min over e in [0,E_MAX]
        hi = lo + E_MAX
        if lo < K_LO or hi > K_HI:
            return False
    return True


def observe(models, actual, u, e):
    z_next = image(MODELS[actual], u) + e
    residual = z_next - e
    posterior = {name for name in models if image(MODELS[name], u) == residual}
    assert actual in posterior
    return z_next, residual, posterior


def main():
    prior = set(MODELS)
    e1, e2 = (Q(1), Q(0)), (Q(0), Q(1))
    assert robustly_safe(e1, [MODELS[k] for k in prior])
    assert not robustly_safe((Q(0), Q(1, 100)), [MODELS[k] for k in prior])
    # The c-model forces u_2=0; with u_2=0 every u_1 in [0,1] is safe.
    print("initial_common_safe_set_exactly={u in [0,1]^2: u2=0}")

    e = Q(1, 40)
    for actual in ("a", "b", "c"):
        z1, y1, post1 = observe(prior, actual, e1, e)
        assert robustly_safe(e1, [MODELS[k] for k in prior])
        if actual == "c":
            assert post1 == {"c"}
            assert not robustly_safe(e2, [MODELS[k] for k in post1])
            print(f"branch={actual}; z1={z1}; residual={y1}; posterior={sorted(post1)}; e2_safe=False")
        else:
            assert post1 == {"a", "b"}
            assert robustly_safe(e2, [MODELS[k] for k in post1])
            z2, y2, post2 = observe(post1, actual, e2, e)
            assert post2 == {actual}
            assert robustly_safe(e2, [MODELS[k] for k in post2])
            print(
                f"branch={actual}; z1={z1}; residual1={y1}; "
                f"posterior1={sorted(post1)}; e2_safe=True; "
                f"z2={z2}; residual2={y2}; posterior2={sorted(post2)}"
            )
    print("all exact-rational assertions passed")


if __name__ == "__main__":
    main()
