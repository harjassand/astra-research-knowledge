#!/usr/bin/env python3
"""Noisy observed-context acquisition and finite local-preparation certificate.

No private plant import, true context, response table, hidden state, initializer
or exact probability oracle is used. Exploration calls only noisy read-count
and legal parallel-update capabilities. Offline certification uses integers.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path


def rational(x):
    return {"numerator": x.numerator, "denominator": x.denominator, "decimal": float(x)}


def default_contract():
    guard = list(range(-7, 8))
    return {"guard": guard, "exploration_collar": list(range(-8, 9)),
            "parents": {str(i): [i-1, i, i+1] for i in guard},
            "candidate_modes": ["a", "b"], "future_legal_modes": ["a", "b", "c"],
            "sensor_error_ceiling": [1,10], "sensor_repetitions": 81,
            "min_samples_per_row": 2500, "table_width": [1,20],
            "exploration_round_cap": 100000, "preparation_rounds": 12,
            "future_visible_support": [0], "future_round_horizon": 1,
            "backward_cone": [-1,0,1], "requested_tv_diameter": [1,20],
            "supplied_physical_contract": [
                "complete clocked local native binary memory, including sensor/control memory",
                "finite stated parents for every legal control; no unmodelled memory/long-range input",
                "synchronous product updates conditional on old configuration and controls",
                "fresh conditional update noise; site-selective parallel pulses are legal",
                "bits fixed during paid nondemolition reads; uniform conditional read-error ceiling",
                "preparation emits no state/bath readout; fixed public modes and duration",
                "future policy observes only declared support, using fresh sensor noise"]}


def explore(read_counts, parallel_update, contract):
    """One retained trajectory. read_counts returns actual noisy integer sums."""
    b = contract["guard"]
    collar = contract["exploration_collar"]
    modes = contract["candidate_modes"]
    m = contract["min_samples_per_row"]
    r = contract["sensor_repetitions"]
    rows = {(i,a,z): [0,0] for i in b for a in modes
            for z in range(1 << len(contract["parents"][str(i)]))}
    exposure = {key: 0 for key in rows}
    rounds = 0
    completed = False
    for t in range(contract["exploration_round_cap"]):
        a = modes[t % len(modes)]
        before_counts = read_counts(collar, r)
        before = {i: int(c > r//2) for i,c in zip(collar,before_counts)}
        # Context labels are acquired from the noisy raw read sums, never
        # supplied by the plant. Selection occurs before fresh update noise.
        contexts = {i: sum(before[j] << bit for bit,j in enumerate(contract["parents"][str(i)]))
                    for i in b}
        parallel_update({i: a for i in collar})
        after_counts = read_counts(b, r)
        for i,c in zip(b,after_counts):
            key = (i,a,contexts[i])
            exposure[key] += 1
            if rows[key][0] < m:
                rows[key][0] += 1
                rows[key][1] += int(c > r//2)
        rounds = t+1
        if all(n == m for n,ones in rows.values()):
            completed = True
            break
    return {"contract": contract,
            "observed_rows": [{"site": i, "mode": a, "context": z,
                               "samples": n, "ones": ones,
                               "total_observed_exposures": exposure[i,a,z]}
                              for (i,a,z),(n,ones) in rows.items()],
            "exploration": {"rounds": rounds, "coverage_complete": completed,
                            "full_initializer_calls": 0,
                            "paid_site_updates": rounds*len(collar),
                            "paid_raw_sensor_reads": rounds*r*(len(collar)+len(b)),
                            "paid_native_hold_read_ticks": rounds*r*(len(collar)+len(b)),
                            "public_schedule": "alternate a/b on all collar sites in parallel",
                            "data_dependent_acquisition_completion_time_public": True}}


def certify(data):
    if set(data) != {"contract", "observed_rows", "exploration"}:
        raise ValueError("Unexpected private/audit metadata in count learner input")
    c = data["contract"]
    if c != default_contract():
        raise ValueError("This executable verifies its fixed prospective contract; the proof is general")
    b, modes = c["guard"], c["candidate_modes"]
    m, r = c["min_samples_per_row"], c["sensor_repetitions"]
    w, es = Fraction(*c["table_width"]), Fraction(*c["sensor_error_ceiling"])
    table = {}
    for row in data["observed_rows"]:
        key = (row["site"],row["mode"],row["context"])
        if key in table or not (0 <= row["ones"] <= row["samples"] <= m):
            raise ValueError("Invalid or duplicated integer response row")
        table[key] = row
    expected = {(i,a,z) for i in b for a in modes
                for z in range(1 << len(c["parents"][str(i)]))}
    if set(table) != expected:
        raise ValueError("Missing or undeclared response rows")
    missing = [list(key) for key,row in table.items() if row["samples"] < m]
    base = {"status": "UNKNOWN", "missing_rows": missing,
            "full_hankel_rank_assumed": False,
            "physical_local_completeness_still_supplied": True,
            "full_initializer_calls": 0,
            "confidence_semantics": "unconditional probability of return AND invalid certificate",
            "table_bad_event": {"coefficient": 2*len(table),
                                "negative_exp_exponent": rational(2*m*w*w)},
            "sensor_bad_event": {
                "coefficient": c["exploration_round_cap"]*(len(c["exploration_collar"])+len(b)),
                "negative_exp_exponent": rational(2*r*(Fraction(1,2)-es)**2)},
            "reference_contract": "same guard kernel from an actual anchor field; local finite-horizon target only",
            "record_contract": "deterministic public fixed-duration update modes; no guard-stage readout; microscopic noise unmonitored"}
    if missing:
        base["reason"] = "Finite exploration cap reached before all contexts appeared"
        return base
    bounds = {}
    for i in b:
        parents = c["parents"][str(i)]
        for a in modes:
            means = [Fraction(table[i,a,z]["ones"],m) for z in range(1 << len(parents))]
            intervals = [(max(Fraction(0),p-w),min(Fraction(1),p+w)) for p in means]
            influence = []
            for bit in range(len(parents)):
                upper = max(max(intervals[z][1]-intervals[z^(1 << bit)][0],
                                intervals[z^(1 << bit)][1]-intervals[z][0])
                            for z in range(len(means)))
                influence.append(upper)
            bounds[i,a] = influence
    selected = {i: min(modes,key=lambda a: (sum(bounds[i,a]),a)) for i in b}
    rowsums = {i: sum(bounds[i,selected[i]]) for i in b}
    q = max(rowsums.values())
    # Monotone clipped disagreement recursion includes every exterior parent.
    v = {i: Fraction(1) for i in b}
    for _ in range(c["preparation_rounds"]):
        v = {i: min(Fraction(1),sum(weight*(v[j] if j in v else 1)
                                  for j,weight in zip(c["parents"][str(i)],bounds[i,selected[i]])))
             for i in b}
    epsilon = min(Fraction(1),sum(v[i] for i in c["backward_cone"]))
    # Scalar first-exit comparison is an additional check, not the used bound.
    radius = max(abs(i) for i in b)
    distance = radius-c["future_round_horizon"]+1
    scalar = min(Fraction(1),len(c["backward_cone"])*(q**c["preparation_rounds"]+q**distance)) if q < 1 else Fraction(1)
    success = q < 1 and epsilon <= Fraction(*c["requested_tv_diameter"])
    base.update({"status": "CERTIFIED" if success else "UNKNOWN",
                 "reason": "Acquired local preparation island" if success else "No useful certified guard within budget",
                 "selected_public_modes": {str(i): a for i,a in selected.items()},
                 "selected_upper_influences": {str(i): [rational(x) for x in bounds[i,selected[i]]] for i in b},
                 "selected_upper_row_sums": {str(i): rational(x) for i,x in rowsums.items()},
                 "maximum_upper_row_sum": rational(q),
                 "prepared_cone_disagreement_bounds": {str(i): rational(v[i]) for i in c["backward_cone"]},
                 "uniform_target_future_tv_diameter": rational(epsilon),
                 "scalar_first_exit_tv_bound": rational(scalar),
                 "preparation_rounds": c["preparation_rounds"],
                 "site_updates_per_preparation": len(b)*c["preparation_rounds"],
                 "controller_selection_random_bits": 0,
                 "max_certificate_integer_bits": max(abs(z).bit_length() for f in (q,epsilon,scalar)
                                                     for z in (f.numerator,f.denominator))})
    return base


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("counts",type=Path)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    result=certify(json.loads(args.counts.read_text()))
    args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"q":result.get("maximum_upper_row_sum"),
                      "epsilon":result.get("uniform_target_future_tv_diameter")},indent=2))


if __name__ == "__main__":
    main()
