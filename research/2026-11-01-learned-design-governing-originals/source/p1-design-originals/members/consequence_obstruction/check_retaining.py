"""Executable checks of a conventional KL retaining comparator.

No unknown-parameter source simulation is passed off as source acquisition:
the p values below are validator-only fixture values. For a small adaptive
query service we enumerate the true joint law exactly up to floating point.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path


def bernoulli_kl(p: float, q: float) -> float:
    return p * math.log(p / q) + (1-p) * math.log((1-p) / (1-q))


def query(p: tuple[float, float], history: tuple[int, ...], counts: tuple[int, int]) -> float:
    """An actually adaptive positive quotient with uniform logit L1 bound 4."""
    parity = (sum(history) + counts[0] + 2*counts[1]) % 2
    exponent = 1 + ((len(history) + sum(history)) % 2)
    multiplier = (1/3, 1, 3)[(sum(history) + counts[0]) % 3]
    first = (1+p[parity])**exponent
    second = multiplier * (1+p[1-parity])**exponent
    return first/(first+second)


def conditional_law(p: tuple[float, float], counts: tuple[int, int], n: int, horizon: int):
    empirical = (counts[0]/n, counts[1]/n)
    frontier = {(): (1.0, 1.0)}
    chain_kl = 0.0
    for _ in range(horizon):
        nxt = {}
        for h, (a, b) in frontier.items():
            u, v = query(p, h, counts), query(empirical, h, counts)
            chain_kl += a * bernoulli_kl(u, v)
            nxt[h+(1,)] = (a*u, b*v)
            nxt[h+(0,)] = (a*(1-u), b*(1-v))
        frontier = nxt
    direct_kl = sum(a*math.log(a/b) for a,b in frontier.values())
    tv = sum(abs(a-b) for a,b in frontier.values())/2
    assert abs(chain_kl-direct_kl) < 1e-10
    eta = max(abs(empirical[i]-p[i]) for i in range(2))
    kl_bound = horizon*(4*eta)**2/8
    tv_bound = 4*eta*math.sqrt(horizon)/4
    assert direct_kl <= kl_bound+1e-12
    assert tv <= tv_bound+1e-12
    return tv, direct_kl, eta**2


def fixture(n: int, horizon: int) -> dict:
    p=(.2,.8)
    tv = kl = mse_max = total_prob = 0.0
    for counts in itertools.product(range(n+1), repeat=2):
        weight = math.prod(math.comb(n, counts[i])*p[i]**counts[i]*(1-p[i])**(n-counts[i]) for i in range(2))
        ctv, ckl, cmse = conditional_law(p, counts, n, horizon)
        tv += weight*ctv
        kl += weight*ckl
        mse_max += weight*cmse
        total_prob += weight
    mse_bound=(math.log(4)+1)/(2*n)
    kl_bound=(math.log(4)+1)*horizon*4**2/(16*n)
    tv_bound=math.sqrt((math.log(4)+1)*horizon*4**2/(32*n))
    assert abs(total_prob-1)<1e-11
    assert mse_max<=mse_bound+1e-12
    assert kl<=kl_bound+1e-12
    assert tv<=tv_bound+1e-12
    return dict(n=n,horizon=horizon,joint_tv=tv,joint_kl=kl,
                expected_sup_error_squared=mse_max,mse_bound=mse_bound,
                kl_bound=kl_bound,tv_bound=tv_bound,
                calibration_source_draws=2*n,
                conditional_histories=(n+1)**2*(2**horizon))


def main():
    points=[]
    # The bound itself is elementary. This grid catches constants and
    # adaptation mistakes without pretending to validate a general proof.
    worst_ratio=0
    for a in range(-80,81):
        for b in range(-80,81):
            if a==b:
                continue
            theta,psi=a/10,b/10
            p=1/(1+math.exp(-theta));q=1/(1+math.exp(-psi))
            ratio=bernoulli_kl(p,q)/((theta-psi)**2/8)
            worst_ratio=max(worst_ratio,ratio)
            assert ratio<=1+1e-10
    for n,h in [(4,3),(8,5),(16,7),(32,7)]:
        points.append(fixture(n,h))
    cutoff=100000
    partial=math.fsum(1/(t*math.log(t+1)**2) for t in range(1,cutoff+1))
    tail_upper=1/math.log(cutoff)
    assert partial+tail_upper<6
    results=dict(
        verdict="All enumerated adaptive transcript and KL checks passed.",
        nature="Conventional sufficient comparator; not an optimality or new-factory claim.",
        bernoulli_logit_grid_pairs=161*160,
        largest_kl_to_logit_bound_ratio=worst_ratio,
        adaptive_fixtures=points,
        infinite_schedule_series_partial=partial,
        infinite_schedule_series_tail_upper=tail_upper,
        infinite_schedule_series_upper=partial+tail_upper,
    )
    target=Path(__file__).with_name("retaining_check_results.json")
    target.write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps(results,indent=2))


if __name__=="__main__":
    main()
