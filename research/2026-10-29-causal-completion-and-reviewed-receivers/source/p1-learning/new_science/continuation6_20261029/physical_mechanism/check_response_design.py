#!/usr/bin/env python3
"""Visible-only response design and a matched ordinary score comparator.

Declared rational 32-state population supplier; no apparatus is simulated in
microscopic detail. All sampled native operations execute on persistent hidden
states. The learner receives only endpoint signs and its own operation counts.
Population matrices are used afterwards for validation, not to select weights.
"""
from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
RAW = HERE / "response_design_records"
RHO = 7 / 8
Q = 1 / 8
C = 7.0
HIDDEN = 16
FLIP_NUM = np.array([56 if h in (0, 3, 5, 10) else 1 + h % 3
                     for h in range(HIDDEN)], dtype=np.int64)


class NativeBox:
    """Only draw() is supplied to the design algorithm."""

    def __init__(self, seed: int):
        self.rng = np.random.default_rng(seed)

    def draw(self, w: Fraction, n: int, forced: int | None = None):
        rng = self.rng
        state = rng.integers(0, 2 * HIDDEN, n)
        f0 = np.where(state < HIDDEN, 1, -1).astype(np.int8)
        mode1 = np.zeros(n, np.int32)
        mode2 = np.zeros(n, np.int32)

        def native(ids: np.ndarray, action: np.ndarray):
            first = ids[action == 0]
            second = ids[action == 1]
            if first.size:
                h = state[first] % HIDDEN
                flip = rng.integers(0, 128, first.size) < FLIP_NUM[h]
                state[first[flip]] ^= HIDDEN
                mode1[first] += 1
            if second.size:
                u = rng.integers(0, 32, second.size)
                mask = np.zeros(second.size, np.int64)
                mask[u < 8] = 1
                mask[(u >= 8) & (u < 12)] = 2
                mask[(u >= 12) & (u < 14)] = 4
                mask[u == 14] = 8
                state[second] ^= mask
                mode2[second] += 1

        def prefix():
            lengths = np.zeros(n, np.int32)
            ids = np.arange(n)
            # One fresh 3-bit stop coin for every active path and round.
            while ids.size:
                ids = ids[rng.integers(0, 8, ids.size) != 0]
                if not ids.size:
                    break
                action = (rng.integers(0, w.denominator, ids.size)
                          >= w.numerator).astype(np.int8)
                native(ids, action)
                lengths[ids] += 1
            return lengths

        nleft = prefix()
        if forced is not None:
            native(np.arange(n), np.full(n, forced, dtype=np.int8))
            nright = prefix()
        else:
            nright = np.zeros(n, np.int32)
        fend = np.where(state < HIDDEN, 1, -1).astype(np.int8)
        assert np.array_equal(mode1 + mode2,
                              nleft + nright + int(forced is not None))
        return dict(f0=f0, fend=fend, nleft=nleft, nright=nright,
                    mode1=mode1, mode2=mode2)


def save_record(name: str, record: dict, w: Fraction, forced: int | None):
    path = RAW / (name + ".npz")
    np.savez_compressed(path, **record)
    n = len(record["f0"])
    ncalls = int(np.sum(record["mode1"], dtype=np.int64)
                 + np.sum(record["mode2"], dtype=np.int64))
    random_calls = ncalls - (n if forced is not None else 0)
    stop_draws = random_calls + n * (2 if forced is not None else 1)
    selector_bits = int(math.log2(w.denominator))
    bit_cost = (5*n + 3*stop_draws + selector_bits*random_calls
                + 7*int(np.sum(record["mode1"], dtype=np.int64))
                + 5*int(np.sum(record["mode2"], dtype=np.int64)))
    return dict(name=name, samples=n, w=str(w), forced=forced,
                baseline_preparations=n, endpoint_readings=2*n,
                actual_native_calls=ncalls,
                operation_selector_draws=random_calls,
                geometric_stop_draws=stop_draws,
                ideal_discrete_random_bit_count=bit_cost,
                maximum_native_calls_in_one_trial=int(np.max(
                    record["mode1"] + record["mode2"])),
                record_file=str(path.relative_to(HERE)),
                record_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def score_values(record, w):
    w = float(w)
    y = record["f0"].astype(float) * record["fend"]
    score = record["mode1"] / w - record["mode2"] / (1-w)
    return y, score


def population():
    n = 2*HIDDEN
    p1 = np.eye(n)
    for y in range(2):
        for h in range(HIDDEN):
            p = FLIP_NUM[h]/128
            p1[y*HIDDEN+h, y*HIDDEN+h] = 1-p
            p1[y*HIDDEN+h, (1-y)*HIDDEN+h] = p
    hidden = np.eye(HIDDEN)*(17/32)
    for h in range(HIDDEN):
        for mask, p in ((1, 8/32), (2, 4/32), (4, 2/32), (8, 1/32)):
            hidden[h, h ^ mask] += p
    p2 = np.kron(np.eye(2), hidden)
    f = np.r_[np.ones(HIDDEN), -np.ones(HIDDEN)]
    assert np.array_equal(p1, p1.T) and np.array_equal(p2, p2.T)
    assert np.array_equal(p1.sum(1), np.ones(n))
    assert np.array_equal(p2.sum(1), np.ones(n))
    return p1, p2, f


def pop_response(w: float, rho=RHO):
    p1, p2, f = population()
    n = len(f); q = 1-rho; c = rho/q
    r = np.linalg.inv(np.eye(n)-rho*(w*p1+(1-w)*p2))
    u = q*r@f
    fj = np.array([u@p1@u/n, u@p2@u/n])
    value = float(q*f@r@f/n)
    g = c*fj
    result = dict(w=w, rho=rho, F=value,
                  filter_variance=(2*value-q)/(1+rho),
                  gradient=list(g), derivative=float(g[0]-g[1]),
                  gap=float(w*g[0]+(1-w)*g[1]-min(g)))
    if 0 < w < 1:
        d = p1-p2
        psecond = p1/w + p2/(1-w)
        eys2 = float((q*rho*f@r@psecond@r@f
                      + 2*q*rho**2*f@r@d@r@d@r@f)/n)
        es2 = c/(w*(1-w))
        b = eys2/es2
        derivative = result["derivative"]
        lr_var = es2-derivative**2
        lr_opt_var = es2*(1-b*b)-derivative**2
        ins_cost_var = 2*c*c*(2*c+1)*float(np.sum(1-fj*fj))
        result.update(score_second_moment=es2,
                      optimal_constant_reward_baseline=b,
                      raw_score_variance=lr_var,
                      optimal_baseline_score_variance=lr_opt_var,
                      raw_score_variance_times_expected_calls=c*lr_var,
                      optimal_score_variance_times_expected_calls=c*lr_opt_var,
                      insertion_variance_times_expected_calls=ins_cost_var,
                      insertion_to_optimal_score_cost_variance_ratio=
                          ins_cost_var/(c*lr_opt_var))
    return result


def main():
    RAW.mkdir(exist_ok=True)
    box = NativeBox(202610290601)
    receipts=[]; pilot=[]
    lo, hi = Fraction(0), Fraction(1)
    # Ordinary, untrusted pilot: five selector-score bisection steps.
    # Independent validation, not this noisy pilot, establishes the guarantee.
    for step in range(5):
        w=(lo+hi)/2
        rec=box.draw(w, 80000)
        receipts.append(save_record(f"pilot_{step}", rec, w, None))
        y,s=score_values(rec,w)
        cut=len(y)//2
        baseline=float(np.sum(y[:cut]*s[:cut]**2)/np.sum(s[:cut]**2))
        estimate=float(np.mean((y[cut:]-baseline)*s[cut:]))
        pilot.append(dict(w=str(w), estimated_derivative=estimate,
                          independent_pilot_baseline=baseline))
        if estimate < 0: lo=w
        else: hi=w
    selected=(lo+hi)/2

    # A new, bounded endpoint-only intervention certificate.
    n_insert=500000
    means=[]
    inserted=[]
    for j in (0,1):
        rec=box.draw(selected,n_insert,forced=j)
        receipt=save_record(f"insertion_{j}",rec,selected,j)
        receipts.append(receipt); inserted.append(receipt)
        means.append(float(np.mean(rec["f0"]*rec["fend"])))
    beta_insert=.005
    grad=np.array(means)*C
    xi=C*math.sqrt(2*math.log(4/beta_insert)/n_insert)
    w=float(selected)
    gap_hat=w*grad[0]+(1-w)*grad[1]-min(grad)
    insert_upper=gap_hat+2*xi

    # The ordinary competitor receives the same expected native-call budget.
    # Its baseline estimation is included, not supplied from the population.
    expected_insert_calls=2*n_insert*(2*C+1)
    n_score=math.ceil(expected_insert_calls/C)
    rec=box.draw(selected,n_score)
    score_receipt=save_record("ordinary_score_comparison",rec,selected,None)
    receipts.append(score_receipt)
    y,s=score_values(rec,selected)
    baseline_n=50000
    b=float(np.sum(y[:baseline_n]*s[:baseline_n]**2)
            /np.sum(s[:baseline_n]**2))
    corrected=(y[baseline_n:]-b)*s[baseline_n:]
    raw=y[baseline_n:]*s[baseline_n:]
    corrected_mean=float(np.mean(corrected))

    # Rigorous finite-variance median-of-means certificate for RAW scores.
    # A reward baseline improves empirical variance, but is not silently used
    # with the smaller raw-score variance upper bound in this certificate.
    beta_score=.005
    blocks=math.ceil(2*math.log(1/beta_score)/math.log(16/7))
    if blocks % 2 == 0: blocks+=1
    blocksize=len(raw)//blocks
    blockmeans=raw[:blocks*blocksize].reshape(blocks,blocksize).mean(axis=1)
    mom=float(np.median(blockmeans))
    vmax=C/(w*(1-w))
    mom_radius=math.sqrt(8*vmax/blocksize)
    mom_fail=(7/16)**(blocks/2)
    score_upper=max(0.0,w*(mom+mom_radius),-(1-w)*(mom-mom_radius))

    # Independent population verification; it did not influence selected w.
    opt=minimize_scalar(lambda v: pop_response(float(v))["F"],
                        bounds=(0,1),method="bounded",options={"xatol":1e-13})
    selected_pop=pop_response(w)
    derivative=selected_pop["derivative"]
    regret=selected_pop["F"]-opt.fun
    assert max(abs(grad-np.array(selected_pop["gradient"]))) <= xi
    assert abs(mom-derivative) <= mom_radius
    assert regret <= insert_upper and regret <= score_upper
    assert mom_fail <= beta_score
    assert np.linalg.norm(population()[0]@population()[1]
                          -population()[1]@population()[0]) > .1

    # Formula (3), from a convergent autocorrelation/filter sum.
    p1,p2,f=population(); p=w*p1+(1-w)*p2
    power=f.copy(); autoc=[]
    for k in range(500):
        autoc.append(float(f@power/len(f))); power=p@power
    filter_series=Q/(1+RHO)*(autoc[0]+2*sum(
        RHO**k*autoc[k] for k in range(1,len(autoc))))
    assert abs(filter_series-selected_pop["filter_variance"])<1e-12

    # The common-invariant-law nonreversible convexity counterexample.
    rot=np.roll(np.eye(3),1,axis=1)
    f3=np.array([1.,-1.,0.]); f3/=np.linalg.norm(f3)
    vals=[]
    for t in (0.,.5,1.):
        value=Q*f3@np.linalg.solve(np.eye(3)-RHO*(t*rot+(1-t)*rot.T),f3)
        closed=Q*(1+RHO/2)/((1+RHO/2)**2+3*RHO**2*(2*t-1)**2/4)
        assert abs(value-closed)<1e-14
        vals.append(float(value))
    assert vals[1]>(vals[0]+vals[2])/2

    out=dict(status="PASS",scope="Declared rational population source and synthetic native operation samples; not a laboratory result or interval-certified physical implementation",
             physical_model=dict(states=32,visible_values=2,hidden_values=16,
                 fixed_round_duration="tau, actual supplied common duration",
                 common_equilibrium="uniform on 32 microscopic states",
                 rho=RHO,geometric_mean_native_calls=C,
                 mode1="flip visible bit with hidden-dependent dyadic probability",
                 mode2="lazy hidden hypercube move, visible bit unchanged",
                 noncommuting=True),
             pilot=pilot,selected_weight=str(selected),
             insertion_certificate=dict(beta=beta_insert,n_per_intervention=n_insert,
                 gradient_estimate=list(grad),gradient_radius=xi,
                 global_F_regret_upper=insert_upper,
                 filtered_noise_regret_upper=2*insert_upper/(1+RHO),
                 actual_native_calls=sum(x["actual_native_calls"] for x in inserted),
                 baseline_preparations=2*n_insert),
             ordinary_score_comparator=dict(beta=beta_score,samples=n_score,
                 baseline_pilot_samples=baseline_n,learned_reward_baseline=b,
                 corrected_derivative=corrected_mean,
                 empirical_raw_variance=float(np.var(raw,ddof=1)),
                 empirical_corrected_variance=float(np.var(corrected,ddof=1)),
                 median_of_means_derivative=mom,median_of_means_radius=mom_radius,
                 median_of_means_blocks=blocks,median_of_means_blocksize=blocksize,
                 median_of_means_failure_upper=mom_fail,
                 global_F_regret_upper=score_upper,
                 filtered_noise_regret_upper=2*score_upper/(1+RHO),
                 expected_native_calls=n_score*C,
                 actual_native_calls=score_receipt["actual_native_calls"],
                 baseline_preparations=n_score),
             population_validation=dict(selected=selected_pop,
                 oracle_optimum_weight=float(opt.x),oracle_optimum_F=float(opt.fun),
                 true_F_regret=float(regret),uniform=pop_response(.5),
                 native_only=[pop_response(0),pop_response(1)],
                 filter_series_check=filter_series),
             variance_comparison=[pop_response(ww,rr)
                 for rr in (.5,.875,.97) for ww in (.01,.5,w,.99)],
             nonreversible_counterexample=vals,
             receipts=receipts,
             acquisition_totals=dict(
                 baseline_preparations=sum(x["baseline_preparations"] for x in receipts),
                 endpoint_readings=sum(x["endpoint_readings"] for x in receipts),
                 actual_native_calls=sum(x["actual_native_calls"] for x in receipts),
                 ideal_discrete_random_bits=sum(x["ideal_discrete_random_bit_count"] for x in receipts)))
    path=HERE/"RESPONSE_DESIGN_CHECKS.json"
    path.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"status":out["status"],"selected_weight":str(selected),
                     "true_regret":float(regret),
                     "insertion_bound":insert_upper,"ordinary_score_bound":score_upper,
                     "total_native_calls":out["acquisition_totals"]["actual_native_calls"],
                     "score_cost_variance_ratio":selected_pop[
                         "insertion_to_optimal_score_cost_variance_ratio"]},indent=2))


if __name__ == "__main__":
    main()
