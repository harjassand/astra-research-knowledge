"""Independent rational LP verification using direct interval integration.

The constructor uses prefix moments. This verifier reconstructs every response
coefficient by the bridge's direct segmentwise polynomial integration, then
checks the full primal and dual identities and the all-time safety margin.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import time
import finite_robust_planner as planner

HERE=Path(__file__).resolve().parent


def main():
    begin=time.perf_counter()
    source=HERE.parent/"bridge/acquired_step_response.json"
    target=HERE/"robust_planner_certificate.json"
    cert=json.loads(target.read_text())
    raw=source.read_bytes();table=json.loads(raw)
    assert hashlib.sha256(raw).hexdigest()==cert["acquired_table_sha256"]
    lp=planner.build(table,cert["settings"],direct=True)
    x=[F(v) for v in cert["primal_exact"]]
    lam=[F(v) for v in cert["dual_exact"]]
    primal,dual,gap=planner.verify(lp,x,lam)
    assert primal==F(cert["primal_minimization_value_exact"])
    assert dual==F(cert["dual_lower_bound_exact"])
    assert gap==F(cert["optimization_gap_exact"])
    assert lp["physical"]==F(cert["uniform_physical_radius_for_all_candidates_exact"])
    assert lp["margin"]==F(cert["complete_grid_tightening_exact"])
    assert lp["L"]==F(cert["acquired_table_lipschitz_exact"])
    c=x[:lp["J"]]
    program=[{"start_exact":planner.fs(t),"ramp_exact":planner.fs(lp["h"]),
              "increment_exact":planner.fs(v)} for t,v in zip(lp["starts"],c) if v]
    assert program==cert["force_program"]
    assert sum(abs(v) for v in c)<=lp["V"]
    endpoint=lp["baseline"]+planner.dot(lp["coefficients"][-1],c)
    assert endpoint==F(cert["predicted_endpoint_exact"])
    region=cert["precomputed_baseline_region"]
    lo,hi=[F(v) for v in region["baseline_interval_exact"]]
    x0=[F(v) for v in region["primal_affine_intercept_exact"]]
    x1=[F(v) for v in region["primal_affine_slope_exact"]]
    assert lo<=lp["baseline"]<=hi
    assert [a+lp["baseline"]*b for a,b in zip(x0,x1)]==x
    slope=[F(-1) if name.startswith("trajectory_upper_") else
           F(1) if name.startswith("trajectory_lower_") else F(0)
           for name in lp["labels"]]
    intercept=[b-s*lp["baseline"] for b,s in zip(lp["b"],slope)]
    gap0=planner.dot(lp["d"],x0)+planner.dot(intercept,lam)
    gap1=planner.dot(lp["d"],x1)+planner.dot(slope,lam)
    assert gap0==F(region["duality_gap_affine_intercept_exact"])
    assert gap1==F(region["duality_gap_affine_slope_exact"])
    for baseline in [lo,hi]:
        xp=[a+baseline*b for a,b in zip(x0,x1)]
        rhs=[a+baseline*b for a,b in zip(intercept,slope)]
        assert all(planner.dot(row,xp)<=bound for row,bound in zip(lp["A"],rhs))
        assert gap0+baseline*gap1>=0
    result={"status":"exact acquired-data planner certificate verified",
            "acquired_table_sha256":cert["acquired_table_sha256"],
            "planner_certificate_sha256":hashlib.sha256(target.read_bytes()).hexdigest(),
            "all_primal_inequalities_verified":len(lp["A"]),
            "dual_stationarity_equalities_verified":lp["n"],
            "nonnegative_dual_multipliers_verified":len(lam),
            "independently_integrated_response_coefficients":(lp["P"]+1)*lp["J"],
            "gap_exact":planner.fs(gap),"gap":float(gap),
            "predicted_endpoint":float(endpoint),
            "physical_radius_for_all_candidates":float(lp["physical"]),
            "complete_grid_tightening":float(lp["margin"]),
            "precomputed_baseline_interval":[float(lo),float(hi)],
            "parametric_region_primal_inequalities_verified":2*len(lp["A"]),
            "parametric_duality_gap_identically_zero":gap0==0 and gap1==0,
            "elapsed_seconds":time.perf_counter()-begin,
            "scope":"Exact finite arithmetic and all-time conditional safety. No physical deployment, model-class test or interval-validated source simulation is inferred."}
    (HERE/"robust_planner_verification.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":main()
