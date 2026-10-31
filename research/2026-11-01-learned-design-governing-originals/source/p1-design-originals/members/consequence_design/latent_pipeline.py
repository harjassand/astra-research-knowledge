"""Full ordinary OA acquisition -> acquired logical variables -> integer service.

The hidden partition, dense matrix and source coefficients are used only by the
fixture source and independent post-acquisition scoring. The learner receives
the source's public scalar measurement interface and an error/field budget.
"""
from fractions import Fraction
from pathlib import Path
import argparse
import itertools
import json
import sys
import time

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"consequence_mechanism"))
sys.path.insert(0,str(HERE.parent/"consequence_origin"))
from latent_design import ScalarQuadraticExperiment, compile_acquired, make_fixture, true_energy
from orthogonal_energy_acquisition import acquire_orthogonal_quadratic


def run(n, hidden_groups, seed, transverse=20., cross=.3, generic=.03, queries=12,
        sigma=5.e-6, replicates=1):
    # Fixture parameters are never passed to acquisition or compilation.
    true_A,true_b,true_labels,locking,fixture = make_fixture(
        n,hidden_groups,seed,transverse,cross,generic)
    source = ScalarQuadraticExperiment(true_A,true_b,sigma=sigma,seed=seed+1)
    start=time.perf_counter()
    full,acquisition=acquire_orthogonal_quadratic(
        source,n,global_failure=Fraction(1,20),replicates=replicates,grid_bits=36,
        report_rounding_radius=Fraction(1,10**9))
    acquisition_seconds=time.perf_counter()-start
    full["source_regret_bound"]=acquisition["source_regret_bound"]
    full["confidence_failure"]=.05
    start=time.perf_counter()
    service,compilation=compile_acquired(full,H=Fraction(1,5),epsilon_per_site=Fraction(1,50),
        source_regret_bound=Fraction(acquisition["source_regret_bound"]),confidence_failure=.05)
    compilation_seconds=time.perf_counter()-start
    result={"n":n,"fixture_only_hidden_groups":hidden_groups,"fixture_parameters":fixture,
            "source_noise_sigma":sigma,"replicates":replicates,
            "acquisition":acquisition,"compilation":compilation,
            "source_cost":source.costs(),"acquisition_seconds":acquisition_seconds,
            "compilation_seconds":compilation_seconds,
            "status":"accepted" if service else "no certified service"}
    if service is None:
        return result,full
    # Independent truth checks begin here, after acquisition and acceptance.
    learned={frozenset(i for i,a in enumerate(service.labels) if a==g) for g in range(service.r)}
    planted={frozenset(i for i,a in enumerate(true_labels) if a==g) for g in range(hidden_groups)}
    result["fixture_only_partition_recovered"]=learned==planted
    P=np.eye(service.r)[service.labels]
    true_coarse=P.T@true_A@P
    true_coarse_b=P.T@true_b
    small_physical=(np.array(list(itertools.product((-1,1),repeat=n)),dtype=np.int8)
                    if n<=12 else None)
    coarse_states=(np.array(list(itertools.product((-1,1),repeat=service.r)),dtype=np.int8)
                   if service.r<=16 else None)
    rng=np.random.default_rng(seed+2)
    previous=np.ones(n,dtype=np.int8)
    records=[]
    answers=set()
    for t in range(queries):
        h=.16*rng.uniform(-1,1,n)+.03*previous*((-1)**t)
        start=time.perf_counter()
        answer,work=service.solve(h)
        elapsed=time.perf_counter()-start
        answers.add(answer.tobytes())
        record={"query":t,"execution_seconds":elapsed,"work":work,
                "source_calls_for_query":0,"physical_controls":answer.tolist(),
                "physical_objective":true_energy(true_A,true_b,answer,h)}
        if small_physical is not None:
            minimum=float(np.min(true_energy(true_A,true_b,small_physical,h)))
            regret=record["physical_objective"]-minimum
            assert -1.e-9<=regret<=float(service.regret_bound)+1.e-9
            record.update({"full_physical_enumeration":True,"physical_states_checked":len(small_physical),
                           "true_global_regret":regret})
        else:
            record["full_physical_enumeration"]=False
        if coarse_states is not None:
            coarse_values=(coarse_states@(true_coarse_b+P.T@h)
                           +.5*np.einsum("bi,ij,bj->b",coarse_states,true_coarse,coarse_states,optimize=True))
            record["true_regret_vs_all_learned_aligned_states"]=record["physical_objective"]-float(np.min(coarse_values))
            record["aligned_states_checked"]=len(coarse_states)
        previous=answer
        records.append(record)
    # The same retained consumer must reject requests beyond its certified box.
    bad=np.zeros(n);bad[0]=.20001
    try:
        service.solve(bad)
    except ValueError:
        out_of_box_rejected=True
    else:
        raise AssertionError("The consumer accepted an uncertified field")
    off=~np.eye(n,dtype=bool)
    result.update({"learned_logical_variables":service.r,
                   "ambient_binary_configurations":str(2**n),
                   "latent_binary_configurations":str(2**service.r),
                   "retained_labels":len(service.labels),
                   "retained_scalar_coefficients":len(service.coarse_b_units)+len(service.forest),
                   "retained_field_bound":str(service.H),
                   "uniform_physical_regret_bound":str(service.regret_bound),
                   "uniform_physical_regret_bound_float":float(service.regret_bound),
                   "requested_physical_regret":.02*n,
                   "distinct_executed_designs":len(answers),"queries":records,
                   "out_of_box_rejected":out_of_box_rejected,
                   "fixture_only_locking_rank":int(np.linalg.matrix_rank(locking,tol=1.e-8)),
                   "fixture_only_nonzero_ambient_edges":int(np.count_nonzero(np.triu(true_A,1))),
                   "fixture_only_both_interaction_signs":bool(np.any(true_A[off]>0) and np.any(true_A[off]<0)),
                   "query_seconds_total":sum(q["execution_seconds"] for q in records),
                   "limitations":["Synthetic scalar instrument with stated noise and readout contract",
                                  "No claim that prototype establishes physical preparation access",
                                  "Exact rational certificates and integer consumer; floating source/spectral proposals",
                                  "Global exhaustive scoring is only performed for n<=12",
                                  "No superiority claim over conventional algorithms adopting the same reduction"]})
    return result,full


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--n",type=int,default=24)
    parser.add_argument("--groups",type=int,default=6)
    parser.add_argument("--seed",type=int,default=13001)
    parser.add_argument("--transverse",type=float,default=20.)
    parser.add_argument("--cross",type=float,default=.3)
    parser.add_argument("--generic",type=float,default=.03)
    parser.add_argument("--sigma",type=float,default=5.e-6)
    parser.add_argument("--replicates",type=int,default=1)
    parser.add_argument("--output",default="latent_pipeline_results.json")
    args=parser.parse_args()
    result,full=run(args.n,args.groups,args.seed,args.transverse,args.cross,args.generic,
                    sigma=args.sigma,replicates=args.replicates)
    path=HERE/args.output
    path.write_text(json.dumps(result,indent=2)+"\n")
    full_path=path.with_name(path.stem+"_acquired_model.json")
    full_path.write_text(json.dumps(full,indent=2)+"\n")
    print(json.dumps({"output":str(path),"n":args.n,"status":result["status"],
                      "groups":result.get("learned_logical_variables"),
                      "source_shots":result["acquisition"]["raw_source_reports"],
                      "certificate":result.get("uniform_physical_regret_bound_float"),
                      "budget":result.get("requested_physical_regret"),
                      "acquisition_seconds":result["acquisition_seconds"],
                      "compilation_seconds":result["compilation_seconds"],
                      "query_seconds":result.get("query_seconds_total")},indent=2))


if __name__=="__main__":
    main()
