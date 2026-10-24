#!/usr/bin/env python3
"""Post-run exact arithmetic/control checks. No additional observation calls."""
import ast
import copy
import json
from fractions import Fraction
from pathlib import Path

import island_learner
from local_plant import LocalPlant,post_execution_reference
from run_island import exp_negative_upper,jsonable


HERE=Path(__file__).resolve().parent
RUN=HERE/"run_retained_202610241"


def f(x):
    return Fraction(x["numerator"],x["denominator"])


def main():
    observations=json.loads((RUN/"learner_input.json").read_text())
    certificate=json.loads((RUN/"certificate.json").read_text())
    assert island_learner.certify(observations)==certificate
    c=observations["contract"]
    b=c["guard"]
    t=observations["exploration"]["rounds"]
    assert t==64903 and len(observations["observed_rows"])==240
    assert all(x["samples"]==2500 for x in observations["observed_rows"])
    assert sum(x["total_observed_exposures"] for x in observations["observed_rows"])==t*len(b)
    assert observations["exploration"]["paid_site_updates"]==t*17==1103351
    assert observations["exploration"]["paid_raw_sensor_reads"]==t*32*81==168228576
    assert observations["exploration"]["full_initializer_calls"]==0
    raw=(RUN/"learner_input.json").read_text()
    for forbidden in ('source_seed','_good','_base','true_context','true_state','response_probabilities'):
        assert forbidden not in raw
    tree=ast.parse((HERE/"island_learner.py").read_text())
    imported={x.name for node in ast.walk(tree) if isinstance(node,ast.Import) for x in node.names}
    assert imported <= {"argparse","json"}
    # Read known private fixture parameters only after the entire experiment.
    provenance=json.loads((RUN/"source_provenance.json").read_text())
    plant=LocalPlant(provenance["source_seed"])
    widths=Fraction(*c["table_width"])
    interval_checks=0
    for row in observations["observed_rows"]:
        i=row["site"]
        old={j:int(bool(row["context"] & (1 << bit))) for bit,j in enumerate(c["parents"][str(i)])}
        truth=Fraction(plant._prob100(i,row["mode"],old),100)
        assert abs(Fraction(row["ones"],row["samples"])-truth)<=widths
        interval_checks += 1
    assert all(certificate["selected_public_modes"][str(i)]==plant._good[i] for i in b)
    q=f(certificate["maximum_upper_row_sum"])
    upper={i:[f(x) for x in certificate["selected_upper_influences"][str(i)]] for i in b}
    assert q==max(sum(row) for row in upper.values()) and q<1
    assert all(weight>=Fraction(1,25) for row in upper.values() for weight in row)
    v={i:Fraction(1) for i in b}
    scalar_checks=0
    for k in range(1,c["preparation_rounds"]+1):
        v={i:min(Fraction(1),sum(a*(v[j] if j in v else 1)
                                  for j,a in zip(c["parents"][str(i)],upper[i]))) for i in b}
        for i in b:
            distance=8-abs(i)
            assert v[i]<=q**k+q**distance
            scalar_checks += 1
    epsilon=f(certificate["uniform_target_future_tv_diameter"])
    assert epsilon==sum(v[i] for i in (-1,0,1))
    assert epsilon<f(certificate["scalar_first_exit_tv_bound"])
    # An unobserved context must abstain; no exact hidden-state fill-in.
    missing=copy.deepcopy(observations)
    missing["observed_rows"][0].update(samples=0,ones=0)
    assert island_learner.certify(missing)["status"]=="UNKNOWN"
    # Pure copying of the left input: internal-only optimism cannot discard
    # the guard boundary. Both controls in this countermodel have full-row 1.
    copying=copy.deepcopy(observations)
    for row in copying["observed_rows"]:
        row["ones"]=2500*(row["context"] & 1)
    copy_result=island_learner.certify(copying)
    assert copy_result["status"]=="UNKNOWN" and f(copy_result["maximum_upper_row_sum"])>=1
    truth=post_execution_reference(plant,certificate,c)
    joint=truth["reference_cone_configuration_probabilities"]
    assert min(joint)>=0 and sum(joint)==1
    # Independently score by summing the eight physical neighborhood cases,
    # rather than the evaluator's event-polynomial contraction.
    direct={"unmeasured_c":Fraction(0),"local_feedback_c":Fraction(0)}
    for z,mass in enumerate(joint):
        old={j:int(bool(z & (1 << bit))) for bit,j in enumerate((-1,0,1))}
        pc=Fraction(plant._prob100(0,"c",old),100)
        pa=Fraction(plant._prob100(0,"a",old),100)
        first=Fraction(1,10)+Fraction(4,5)*old[0]
        direct["unmeasured_c"]+=mass*(Fraction(1,10)+Fraction(4,5)*pc)
        direct["local_feedback_c"]+=mass*(Fraction(1,10)+Fraction(4,5)*(first*pc+(1-first)*pa))
    assert direct==truth["reference_event_probabilities"]
    # Math-only scorer reconstructs source parameters; no additional sensor or
    # update/initializer API call occurred in these checks.
    assert plant.counters()==dict(site_updates=0,update_rounds=0,raw_sensor_reads=0,
                                 native_hold_read_ticks=0,full_initializer_calls=0)
    future=json.loads((RUN/"future_observations.json").read_text())
    assert len(future["blocks"])==2
    assert sum(x["trials"] for x in future["blocks"])==10000
    assert sum(x["paid_cost"]["site_updates"] for x in future["blocks"])==1810000
    assert sum(x["paid_cost"]["raw_sensor_reads"] for x in future["blocks"])==15000
    assert all(x["paid_cost"]["full_initializer_calls"]==0 for x in future["blocks"])
    assert future["controller_selection_bits"]==0 and future["guard_stage_state_or_bath_readouts"]==0
    # Same-data ordinary local empirical-kernel learner's interval derivative
    # bound is abs(phat(z)-phat(z'))+2w (with endpoint clipping). Its chosen
    # minimum upper row-sum modes coincide. No method win is claimed.
    count={(r["site"],r["mode"],r["context"]):Fraction(r["ones"],r["samples"])
           for r in observations["observed_rows"]}
    ordinary={}
    for i in b:
        scores={}
        for a in ("a","b"):
            entries=[count[i,a,z] for z in range(8)]
            scores[a]=sum(max(min(1,entries[z]+widths)-max(0,entries[z^(1 << bit)]-widths)
                              for z in range(8)) for bit in range(3))
        ordinary[str(i)]=min(scores,key=lambda a:(scores[a],a))
    assert ordinary==certificate["selected_public_modes"]
    # Stronger public controls need not identify each site's preferred mode:
    # deterministic alternation already has a useful finite-matrix bound.
    all_upper={}
    for i in b:
        for a in ("a","b"):
            p=[count[i,a,z] for z in range(8)]
            all_upper[i,a]=[max(min(1,p[z]+widths)-max(0,p[z^(1 << bit)]-widths)
                                 for z in range(8)) for bit in range(3)]
    schedules={"selected":None,"all_a":("a",),"all_b":("b",),
               "alternate_ab":("a","b"),"alternate_ba":("b","a")}
    allowance=epsilon+Fraction(1,25)
    comparison={}
    for name,pattern in schedules.items():
        dv={i:Fraction(1) for i in b}
        best=None
        depth12=None
        for depth in range(1,101):
            actions={i:(ordinary[str(i)] if pattern is None else pattern[(depth-1)%len(pattern)]) for i in b}
            dv={i:min(Fraction(1),sum(a*(dv[j] if j in dv else 1)
                                      for j,a in zip(c["parents"][str(i)],all_upper[i,actions[i]]))) for i in b}
            diameter=min(Fraction(1),sum(dv[i] for i in (-1,0,1)))
            enough=None
            if diameter < allowance:
                ratio=Fraction(8)/(allowance-diameter)**2
                enough=(ratio.numerator+ratio.denominator-1)//ratio.denominator
                candidate=(enough*(15*depth+1),depth,enough,float(diameter))
                if best is None or candidate < best:
                    best=candidate
            if depth==12:
                depth12={"diameter":float(diameter),
                         "certifies_requested_preparation_tolerance_0_05":diameter<=Fraction(1,20),
                         "trials_for_same_numerical_allowance_own_reference":enough}
        comparison[name]={"actual_executed":name=="selected","depth12":depth12,
                          "best_site_pulses_per_new_program_over_depths_1_to_100":
                           ({"site_pulses":best[0],"depth":best[1],"trials":best[2],"diameter":best[3]}
                            if best is not None else None)}
    assert comparison["alternate_ab"]["depth12"]["certifies_requested_preparation_tolerance_0_05"]
    assert comparison["alternate_ba"]["depth12"]["certifies_requested_preparation_tolerance_0_05"]
    # The Taylor upper bound is exact and finite, with monotone refinement.
    for x in (Fraction(25,2),Fraction(648,25),Fraction(16)):
        assert exp_negative_upper(x,96)<=exp_negative_upper(x,48)
    assert Fraction(1,10)>exp_negative_upper(Fraction(648,25))
    report={"status":"PASS","post_execution_true_probability_intervals_checked":interval_checks,
            "matrix_vs_first_exit_checks":scalar_checks,
            "unvisited_context_and_copying_boundary_obstructions":"UNKNOWN as required",
            "sensor_persistent_flip_obstruction":"marginal error ceiling alone rejected by contract",
            "learner_queries_returning_true_probabilities_or_contexts":0,
            "additional_physical_observation_calls_in_check":0,
            "same_data_ordinary_local_controller":"identical selected public modes",
            "independent_eight_case_reference_scoring":"exact rational equality",
            "max_response_row_exposure":max(x["total_observed_exposures"] for x in observations["observed_rows"]),
            "min_response_row_exposure":min(x["total_observed_exposures"] for x in observations["observed_rows"]),
            "actual_q":float(q),"matrix_epsilon":float(epsilon),
            "same_data_public_schedule_comparisons":comparison,
            "comparison_scope":"exact certificate arithmetic only; different schedules have own references unless separately matched; no new experiments; all planners may adopt selected modes"}
    (RUN/"operation_checks.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    main()
