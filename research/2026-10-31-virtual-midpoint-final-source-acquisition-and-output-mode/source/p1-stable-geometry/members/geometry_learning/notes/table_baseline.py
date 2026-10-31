"""One paid finite-horizon table run, plus an analytical phase-family bill.

The four-state learner uses only the same physical scalar-report interface.
Truth is consulted only after the table has been acquired. The phase table
is a constructive cost calculation, not another physical-source simulation.
"""
from __future__ import annotations

from fractions import Fraction as F
import itertools
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import direct_baseline as direct
cg=direct.cg


def phase_family_bill(horizon=256,epsilon=F(1,50),delta=F(1,100)):
    """Same explicit reflection family and ten-bit physical-report rounding."""
    k=(horizon+1)//2
    rounding_bias=F(1,1 << 11)
    statistical_eps=epsilon-rounding_bias
    if statistical_eps<=0:
        raise ValueError("report rounding cannot meet task precision")
    log2_upper=cg.log_upper_integer(2*k/delta)
    # ln(2)<7/10 is certified, for example, by a positive Taylor lower sum
    # showing exp(7/10)>2. Thus this is an outward rational logarithm bound.
    log_upper=F(7,10)*log2_upper
    shots=cg.ceil_fraction(8*log_upper/(statistical_eps**2))
    preparations=k*shots
    shortest_controls=k*k*shots       # sum_{n=1}^k (2n-1)
    existing_api_controls=k*(k+1)*shots  # existing mean(n) uses 2n reflections
    out={
        "status":"constructive analytical comparator; no additional phase-source run",
        "horizon":horizon,"epsilon_exact":str(epsilon),"delta_exact":str(delta),
        "source_promise":"same two circle reflections and unit-L2 cosine seed",
        "known_index_update":"A: k -> -k; B: k -> 1-k; output cos(k theta)",
        "largest_needed_absolute_index":k,"sampled_cosine_moments":k,
        "known_without_sampling":"c_0=1",
        "physical_report_range":2,"fractional_report_bits":10,
        "report_rounding_bias_upper_exact":str(rounding_bias),
        "statistical_tolerance_exact":str(statistical_eps),
        "log_upper_exact":str(log_upper),"shots_per_moment":shots,
        "stationary_preparations":preparations,"endpoint_readouts":2*preparations,
        "shortest_actual_word_primitive_reflections":shortest_controls,
        "shortest_actual_word_max_return_depth":2*k-1,
        "existing_mean_api_primitive_reflections":existing_api_controls,
        "existing_mean_api_max_return_depth":2*k,
        "unit_cost_total_shortest_words":shortest_controls+3*preparations,
        "unit_cost_total_existing_api":existing_api_controls+3*preparations,
        "retained_table_entries_including_known_c0":k+1,
        "numeric_execution":"exact integer phase index and rational rounded-report means",
        "proof":"bounded-report Hoeffding plus union bound over k moments; exp(7/10)>2 proves log bound",
    }
    old_path=HERE/"geometry_acquisition_results.json"
    if old_path.exists():
        old=json.loads(old_path.read_text())
        compared=[]
        for c in old["cases"]:
            b=c["bill"]
            compared.append({"label":c["label"],"reported_phase_learner_bill":b,
                "phase_to_table_preparation_ratio":b["episodes_and_stationary_preparations"]/preparations,
                "phase_to_shortest_table_control_ratio":b["primitive_reflections"]/shortest_controls,
                "phase_to_shortest_table_unit_total_ratio":b["unit_cost_total_if_prep_and_readout_each_cost_one"]/(shortest_controls+3*preparations)})
        out["comparison_to_preserved_phase_diagnostics"]=compared
    return out


def run():
    source=cg.StationaryEndpointSource(0.4,20261103)
    started=time.perf_counter()
    model=direct.acquire_exhaustive_table(source,3,8,F(1,2),F(1,100))
    acquisition_seconds=time.perf_counter()-started
    bill=source.ledger()
    # Only this post-acquisition block inspects source truth.
    maximum=F(0)
    worst=()
    for word,estimate in model["predictions_exact"].items():
        true=sum((u*v for u,v in zip(source._exact_feature(()),source._exact_feature(word))),F(0))
        error=abs(estimate-true)
        if error>maximum:
            maximum,worst=error,word
    assert maximum<=F(1,2)
    assert source.ledger()==bill
    n=model["reports_per_word"]
    counts=[]
    for value in model["predictions_exact"].values():
        count=(value*n+n)/2
        assert count.denominator==1
        counts.append(count.numerator)
    report={
        "case":"mixed_controls_exhaustive_retaining_table",
        "status":"success","task_horizon":8,"task_epsilon":0.5,
        "joint_failure_probability_at_most":0.01,
        "source":"same common-stationary four-state physical endpoint-product source",
        "physically_executed":False,
        "simulation_method":"same aggregate binomial reports; exact physical means and reserved coin-rounding bias",
        "learner_access":"scalar G(empty,w) reports only; no latent arrays, rank, basis or operation matrices",
        "sampled_and_retained_predictions":len(counts),
        "reports_per_word":n,"complete_physical_bill":bill,
        "maximum_error_over_entire_declared_word_set_audit":float(maximum),
        "maximum_error_exact_audit":str(maximum),"worst_word_audit":list(worst),
        "observed_uniform_accuracy_event_audit_only":True,
        "later_source_calls":0,
        "stored_prediction_precision":"positive-report integer counts plus common denominator n; exact rational lookup",
        "packed_count_bytes_if_one_uint8_per_entry":len(counts),
        "acquisition_cpu_seconds":acquisition_seconds,
        "correction":"this table wins complete acquisition cost on the declared H8 task; compact fixtures demonstrate small stable machinery, not minimum total task cost",
    }
    teacher=json.loads((HERE.parent/"compact_geometry_results.json").read_text())[0]
    direct_result=json.loads((HERE/"direct_baseline_results.json").read_text())[0]
    report["comparisons"]={}
    for label,other in [("teacher_then_compact",teacher),("direct_compact",direct_result)]:
        b=other["complete_physical_bill"]
        report["comparisons"][label]={
            "other_attained_error_certificate":other["all_word_error_certificate_at_task_horizon"],
            "other_physical_bill":b,
            "preparation_ratio_other_over_table":b["stationary_preparations"]/bill["stationary_preparations"],
            "control_ratio_other_over_table":b["primitive_controls"]/bill["primitive_controls"],
        }
    saved={"alphabet":3,"maximum_word_length":8,
           "word_order":"increasing length, lexicographic within each length",
           "reports_per_word":n,
           "prediction_rule":"for the word's stored count p, return exact rational (2*p-n)/n",
           "positive_reports_breadth_first_lex":counts}
    phase=phase_family_bill()
    (HERE/"table_baseline_results.json").write_text(json.dumps(report,indent=2)+"\n")
    (HERE/"table_baseline_model.json").write_text(json.dumps(saved,indent=2)+"\n")
    (HERE/"phase_table_baseline_bill.json").write_text(json.dumps(phase,indent=2)+"\n")
    print(json.dumps({"four_state_table":{k:report[k] for k in [
        "status","sampled_and_retained_predictions","reports_per_word","complete_physical_bill",
        "maximum_error_over_entire_declared_word_set_audit","comparisons"]},
        "phase_family_table_analytical":{k:phase[k] for k in [
            "shots_per_moment","stationary_preparations","endpoint_readouts",
            "shortest_actual_word_primitive_reflections","existing_mean_api_primitive_reflections",
            "unit_cost_total_shortest_words","unit_cost_total_existing_api"]}},indent=2))


if __name__=="__main__":
    run()
