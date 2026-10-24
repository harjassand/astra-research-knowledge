#!/usr/bin/env python3
"""Acquire guard from one retained observed stream, then acquire new local events."""
import argparse
import json
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

import island_learner
from local_plant import LocalPlant,post_execution_reference


def jsonable(x):
    if isinstance(x,Fraction):
        return island_learner.rational(x)
    if isinstance(x,dict):
        return {k:jsonable(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):
        return [jsonable(v) for v in x]
    return x


def save(path,value):
    path.write_text(json.dumps(jsonable(value),indent=2)+"\n")


def exp_negative_upper(x,terms=96):
    """Finite exact arithmetic: exp(-x)<=1/sum_(j=0)^terms x^j/j!."""
    term=Fraction(1)
    total=term
    for j in range(1,terms+1):
        term *= x/j
        total += term
    return 1/total


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-dir",type=Path,required=True)
    p.add_argument("--seed",type=int,default=202610241)
    args=p.parse_args()
    args.out_dir.mkdir(parents=True,exist_ok=False)
    contract=island_learner.default_contract()
    save(args.out_dir/"prospective_contract.json",contract)
    plant=LocalPlant(args.seed)
    start=time.perf_counter()
    observations=island_learner.explore(plant.read_counts,plant.parallel_update,contract)
    acquisition_seconds=time.perf_counter()-start
    save(args.out_dir/"learner_input.json",observations)
    acquisition_cost=plant.counters()
    # Offline certificate process is given only actual counts and physical
    # contracts, with no source seed, hidden bits or private model metadata.
    subprocess.run([sys.executable,str(Path(__file__).with_name("island_learner.py")),
                    str(args.out_dir/"learner_input.json"),"--out",str(args.out_dir/"certificate.json")],
                   check=True,capture_output=True,text=True)
    cert=json.loads((args.out_dir/"certificate.json").read_text())
    if cert["status"] != "CERTIFIED":
        save(args.out_dir/"source_provenance.json",{"source_seed":args.seed,"acquisition_cost":acquisition_cost})
        print(json.dumps({"status":cert["status"],"acquisition_cost":acquisition_cost}))
        return
    programs=("unmeasured_c","local_feedback_c")
    trials=5000
    blocks=[]
    future_start=time.perf_counter()
    for name in programs:
        before=plant.counters()
        ones=0
        for _ in range(trials):
            for _ in range(contract["preparation_rounds"]):
                plant.parallel_update({int(i):a for i,a in cert["selected_public_modes"].items()})
            ones += plant.local_future_program(name)
        after=plant.counters()
        blocks.append({"unmeasured_program":name,"trials":trials,"ones":ones,
                       "sample_mean":Fraction(ones,trials),
                       "paid_cost":{k:after[k]-before[k] for k in after}})
    future_seconds=time.perf_counter()-future_start
    save(args.out_dir/"future_observations.json",{"blocks":blocks,"controller_selection_bits":0,
         "fixed_public_preparation_rounds":contract["preparation_rounds"],
         "guard_stage_state_or_bath_readouts":0,"source_seed_exposed":False})
    # Source truth first enters the scorer after the complete experiment.
    truth=post_execution_reference(plant,cert,contract)
    epsilon=Fraction(cert["uniform_target_future_tv_diameter"]["numerator"],
                     cert["uniform_target_future_tv_diameter"]["denominator"])
    tau=Fraction(1,25) # N=5000 => 2*N*tau^2=16 per program.
    errors={block["unmeasured_program"]:abs(block["sample_mean"]-
            truth["reference_event_probabilities"][block["unmeasured_program"]]) for block in blocks}
    truth["realized_errors"]=errors
    save(args.out_dir/"private_post_execution_truth.json",truth)
    M=len(observations["observed_rows"])
    # Finite positive Taylor sums give rigorous rational upper exp bounds;
    # no exact-real exponentiation is granted to the confidence calculation.
    table_exp=2*contract["min_samples_per_row"]*Fraction(*contract["table_width"])**2
    sensor_exp=2*contract["sensor_repetitions"]*(Fraction(1,2)-Fraction(*contract["sensor_error_ceiling"]))**2
    table_fail=2*M*exp_negative_upper(table_exp)
    sensor_tests=contract["exploration_round_cap"]*(len(contract["guard"])+len(contract["exploration_collar"]))
    sensor_fail=sensor_tests*exp_negative_upper(sensor_exp)
    future_fail=4*exp_negative_upper(Fraction(16))
    allowance=epsilon+tau
    exact_n=Fraction(8)/(allowance*allowance)
    exact_n=(exact_n.numerator+exact_n.denominator-1)//exact_n.denominator
    summary={"status":"RETAINED_TRAJECTORY_PREPARATION_ACQUIRED",
             "acquisition_cost":acquisition_cost,"total_cost":plant.counters(),
             "acquisition_rounds":observations["exploration"]["rounds"],
             "context_rows_completed":M,"full_initializer_calls_entire_run":plant.full_initializer_calls,
             "target_future_tv_diameter":epsilon,"scalar_first_exit_bound":cert["scalar_first_exit_tv_bound"],
             "future_sampling_tolerance":tau,"future_total_allowance":allowance,
             "unconditional_return_and_invalid_failure_upper":table_fail+sensor_fail+future_fail,
             "failure_event":"return with invalid certificate or future mean error above allowance",
             "confidence_exponential_upper_method":"96-term positive Taylor sum, exact rational arithmetic",
             "all_program_errors_inside_allowance":all(e<=allowance for e in errors.values()),
             "matched_exact_initializer_sufficient_trials_per_program":exact_n,
             "acquired_preparation_trials_per_program":trials,
             "acquisition_simulator_seconds":acquisition_seconds,"future_simulator_seconds":future_seconds,
             "same_data_conventional_local_table_controller":"ties modes and certificate",
             "cost_or_novelty_advantage":"NOT_ESTABLISHED",
             "physical_clock_sensor_locality_contract":"SUPPLIED, not certified from observations",
             "physical_platform_validation":"NOT_ESTABLISHED"}
    save(args.out_dir/"summary.json",summary)
    save(args.out_dir/"source_provenance.json",{"source_seed":args.seed,
         "source_only_initial_field":"zero existing field; not disclosed or reset by learner",
         "statistical_prng_fixture_only":True,"sensor_batching":"exact binomial read-count distribution, every represented read/hold paid"})
    print(json.dumps(jsonable(summary),indent=2))


if __name__ == "__main__":
    main()
