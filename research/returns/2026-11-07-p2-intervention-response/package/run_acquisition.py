"""Reproduce a fully numerical acquisition, prediction and design example.

This is an exact rational periodic laminate, not acquired physical data.
The predictor and designer see only calibrated scalar records. The closed
form is confined to the numerical source and independent output checks.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from time import perf_counter
import importlib.util
import json
import math
import sys

from intervention import (qtree, round_dyadic, precision_for, energy_tensor,
                          compile_predictor, evaluate_predictor,
                          certified_design, represented_name_reader, ellipsoid_design,
                          finite_quadratic_reader)

ROOT=Path(__file__).resolve().parent

def true_tensor(theta):
    a=1+Q(theta[0]); b=Q(3,2)*(1+Q(theta[1]))
    return [[2*a*b/(a+b),Q(0)],[Q(0),(a+b)/2]]

def true_energy(theta,e):
    mat=true_tensor(theta)
    return sum(Q(e[i])*mat[i][j]*Q(e[j]) for i in range(2) for j in range(2))

all_reads=[]
def reader(theta,e,radius):
    bits=precision_for(radius)+1
    actual=true_energy(theta,e)
    mid=round_dyadic(actual,bits)
    error=Q(1,1<<(bits+1))
    assert abs(mid-actual)<=error<=radius
    record=dict(theta=list(theta),loading=list(e),mid=mid,error=error,
                source="exact rational laminate, rounded to a certified dyadic record",
                record_bits=bits)
    all_reads.append(record)
    return record

def save(name,value):
    (ROOT/name).write_text(json.dumps(qtree(value),indent=2)+"\n")

def main():
    timings={}
    start=perf_counter()
    baseline,b_error,baseline_records=energy_tensor(reader,[Q(0),Q(0)],2,Q(1,1000))
    U=Q(5,2); S=Q(5,4)
    assert baseline[0][0]+baseline[1][1]+2*b_error<=U
    assert baseline[0][0]+b_error<=S
    save("BASELINE_RECORDS.json",dict(records=baseline_records,tensor=baseline,
                                     operator_error=b_error,U=U,S=S))
    print("Baseline calibration completed: U=5/2, S=5/4.",flush=True)

    tick=perf_counter()
    model=compile_predictor(reader,k=2,d=2,r=Q(1,2),U=U,
                            epsilon=Q(1,100),max_nodes=2000)
    timings["predictor_seconds"]=perf_counter()-tick
    predictions=[]
    # These checks audit the implementation; the uniform proof is separate.
    for theta in [(Q(-1,2),Q(-1,2)),(Q(1,2),Q(1,2)),
                  (Q(-1,2),Q(1,2)),(Q(1,2),Q(-1,2)),
                  (Q(0),Q(0)),(Q(2,7),Q(-3,11)),(Q(-1,5),Q(4,9))]:
        predicted=evaluate_predictor(model,theta)
        exact=true_tensor(theta)
        row_error=max(sum(abs(predicted[i][j]-exact[i][j]) for j in range(2))
                      for i in range(2))
        assert row_error<=model["uniform_operator_error"]
        predictions.append(dict(theta=theta,actual=exact,predicted=predicted,
                                row_error_bound=row_error))
    save("PREDICTOR.json",model)
    save("PREDICTION_CHECKS.json",predictions)
    print("Whole-family predictor completed:",model["parameters"]["n"],
          "nodes per axis;",len(model["acquisitions"]),"settings.",flush=True)

    tick=perf_counter()
    vertices=[[Q(0),Q(0)],[Q(1,2),Q(0)],[Q(0),Q(1,2)]]
    design=certified_design(reader,vertices,[Q(1),Q(0)],Q(1,2),S,Q(1,100),
                            max_iterations=5000)
    timings["design_seconds"]=perf_counter()-tick
    # Independent analytic optimum: 75-30*sqrt(6). Rationally enclose it.
    root_lo=Q(2); root_hi=Q(3)
    for _ in range(100):
        mid=(root_lo+root_hi)/2
        if mid*mid<=6: root_lo=mid
        else: root_hi=mid
    optimum_lo=75-30*root_hi; optimum_hi=75-30*root_lo
    achieved=true_energy(design["theta"],[1,0])
    true_regret_interval=[max(Q(0),optimum_lo-achieved),optimum_hi-achieved]
    assert true_regret_interval[1]<=design["gap_upper"]<=Q(1,100)
    assert design["optimum_interval"][0]<=optimum_lo<=optimum_hi<=design["optimum_interval"][1]
    assert all(x>=0 for x in design["theta"]) and sum(design["theta"])<=Q(1,2)
    design["independent_check"]=dict(analytic_optimum_interval=[optimum_lo,optimum_hi],
                                      achieved_exactly=achieved,
                                      true_regret_interval=true_regret_interval)
    save("DESIGN_CERTIFICATE.json",design)
    print("Global continuous design certified after",design["updates"],
          "updates; certificate gap",float(design["gap_upper"]),flush=True)

    tick=perf_counter()
    ellipsoid=ellipsoid_design(reader,vertices,[Q(1),Q(0)],Q(1,2),S,Q(1,100))
    timings["ellipsoid_design_seconds"]=perf_counter()-tick
    ellipsoid_achieved=true_energy(ellipsoid["theta"],[1,0])
    assert optimum_hi-ellipsoid_achieved<=ellipsoid["gap_upper"]<=Q(1,100)
    ellipsoid["independent_check"]=dict(analytic_optimum_interval=[optimum_lo,optimum_hi],
        achieved_exactly=ellipsoid_achieved,regret_upper=optimum_hi-ellipsoid_achieved)
    save("ELLIPSOID_DESIGN_CERTIFICATE.json",ellipsoid)
    print("Rational ellipsoid design:",ellipsoid["iterations"],"iterations,",
          len(ellipsoid["records"]),"scalar records;",ellipsoid["reason"],flush=True)

    # Exercise the volume-based stopping guarantee as well as the local gap.
    # These are separate numerical acquisitions, and every one is counted.
    tick=perf_counter()
    volume=ellipsoid_design(reader,vertices,[Q(1),Q(0)],Q(1,2),S,Q(1,100),
                            force_volume_certificate=True)
    timings["ellipsoid_volume_check_seconds"]=perf_counter()-tick
    volume_achieved=true_energy(volume["theta"],[1,0])
    assert optimum_hi-volume_achieved<=volume["gap_upper"]<=Q(1,100)
    assert volume["reason"]=="rounded ellipsoid volume bound"
    volume["independent_check"]=dict(analytic_optimum_interval=[optimum_lo,optimum_hi],
        achieved_exactly=volume_achieved,regret_upper=optimum_hi-volume_achieved)
    save("ELLIPSOID_VOLUME_CERTIFICATE.json",volume)
    print("Volume guarantee exercised:",volume["iterations"],"iterations,",
          len(volume["records"]),"scalar records.",flush=True)

    # Construct the promised reader from a coefficient name and the unchanged
    # predecessor certificate solver. This check does not use the laminate
    # closed form to produce its energy interval.
    tick=perf_counter()
    predecessor=ROOT/"predecessor_exact_response.py"
    if not predecessor.exists():
        predecessor=ROOT.parent/"certified_degenerate_response_20261106"/"exact_response.py"
    spec=importlib.util.spec_from_file_location("predecessor_exact_response",predecessor)
    exact=importlib.util.module_from_spec(spec); spec.loader.exec_module(exact)
    name_calls=[]
    def make_name(kind):
        def name(n):
            name_calls.append(dict(name=kind,precision=n,explicit_boxes=4))
            vals={}
            for ix in product(range(2),repeat=2):
                a=Q(1) if ix[0]==0 else Q(3,2)
                if kind=="D1" and ix[0]!=0: a=Q(0)
                if kind=="D2" and ix[0]!=1: a=Q(0)
                vals[ix]=[[a,Q(0)],[Q(0),a]]
            return exact.StepField(2,1,vals,Q(0))
        return name
    numeric_reader,numeric_records=represented_name_reader(
        exact,make_name("A"),[make_name("D1"),make_name("D2")],
        Q(1,4),Q(2),Q(1,2),max_stages=8)
    numeric_record=numeric_reader([Q(1,4),Q(1,8)],[Q(1),Q(0)],Q(1,32))
    value=Q(135,94)
    assert abs(numeric_record["mid"]-value)<=numeric_record["error"]
    timings["coefficient_name_reader_seconds"]=perf_counter()-tick
    save("COEFFICIENT_NAME_ACQUISITION.json",dict(record=numeric_record,
         requested_scalar_radius=Q(1,32),independent_exact_value=value,
         base_tau=Q(1,4),base_M=Q(2),control_moment_tau=Q(1,8),
         coefficient_name_calls=name_calls))
    print("Constructed coefficient-name reader certified an independent energy interval.",flush=True)

    A=[[1,0],[0,1]]
    D1=[[Q(1,4),Q(1,4)],[Q(1,4),Q(1,4)]]
    D2=[[Q(1,6),Q(-1,6)],[Q(-1,6),Q(1,3)]]
    finite_reader,finite_records=finite_quadratic_reader(A,[D1,D2],1)
    finite_record=finite_reader([Q(1,4),Q(-1,4)],[Q(1)],Q(1,1000000))
    assert abs(finite_record["mid"]-Q(1139,1128))<=finite_record["error"]
    save("FINITE_QUADRATIC_ACQUISITION.json",dict(base=A,directions=[D1,D2],ports=1,
          record=finite_record,independent_value=Q(1139,1128)))

    summary=dict(
        purpose="Deterministic numerical acquisition only; no physical data or new experiment.",
        phase_conductivities=["1", "3/2"],phase_volumes=["1/2","1/2"],
        k=2,d=2,r=Q(1,2),target_absolute_accuracy=Q(1,100),
        baseline_scalar_records=3,
        predictor_settings=len(model["acquisitions"]),
        predictor_scalar_records=3*len(model["acquisitions"]),
        predictor_nodes_per_axis=model["parameters"]["n"],
        predictor_uniform_operator_error=model["uniform_operator_error"],
        predictor_error_decimal=float(model["uniform_operator_error"]),
        predictor_rational_node_bits=model["node_bits"],
        predictor_maximum_coefficient_bits=model["maximum_coefficient_bits"],
        design_updates=design["updates"],
        design_scalar_records=4*len(design["transcript"]),
        design_theta=design["theta"],
        design_theta_decimal=[float(t) for t in design["theta"]],
        design_gap_certificate=design["gap_upper"],
        design_gap_decimal=float(design["gap_upper"]),
        design_actual_regret_upper=true_regret_interval[1],
        design_actual_regret_decimal=float(true_regret_interval[1]),
        design_reading_radius=design["reading_radius"],
        design_maximum_control_bits=design["maximum_control_bits"],
        ellipsoid_iterations=ellipsoid["iterations"],
        ellipsoid_maximum_iterations=ellipsoid["maximum_iterations"],
        ellipsoid_scalar_records=len(ellipsoid["records"]),
        ellipsoid_theta_decimal=[float(t) for t in ellipsoid["theta"]],
        ellipsoid_gap_decimal=float(ellipsoid["gap_upper"]),
        ellipsoid_actual_regret_decimal=float(optimum_hi-ellipsoid_achieved),
        ellipsoid_maximum_control_bits=ellipsoid["maximum_control_bits"],
        ellipsoid_center_bits=ellipsoid["center_bits"],
        ellipsoid_shape_bits=ellipsoid["shape_bits"],
        ellipsoid_volume_iterations=volume["iterations"],
        ellipsoid_volume_scalar_records=len(volume["records"]),
        ellipsoid_volume_actual_regret_decimal=float(optimum_hi-volume_achieved),
        separate_coefficient_name_reader_records=len(numeric_records),
        coefficient_name_calls=len(name_calls),
        coefficient_name_total_returned_boxes=4*len(name_calls),
        separate_finite_quadratic_records=len(finite_records),
        total_laminate_reader_records=len(all_reads),
        timings_seconds=timings,total_seconds=perf_counter()-start)
    assert len(all_reads)==(3+3*len(model["acquisitions"])+4*len(design["transcript"])
                           +len(ellipsoid["records"])+len(volume["records"]))
    save("EXECUTION_SUMMARY.json",summary)
    print(json.dumps(qtree({key:value for key,value in summary.items()
                          if key.endswith("decimal") or key.endswith("records")
                          or key in ("design_updates","predictor_settings","total_seconds",
                                     "coefficient_name_calls","predictor_maximum_coefficient_bits",
                                     "predictor_rational_node_bits","design_maximum_control_bits")})),flush=True)

if __name__=="__main__": main()
