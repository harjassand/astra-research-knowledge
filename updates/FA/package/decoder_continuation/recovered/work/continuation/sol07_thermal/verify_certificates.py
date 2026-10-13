#!/usr/bin/env python3
"""Read-only independent rational checker for saved certificate outputs."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def decode(x):
    if isinstance(x, dict) and "rational" in x:
        return F(x["rational"])
    if isinstance(x, dict):
        return {k: decode(v) for k, v in x.items()}
    if isinstance(x, list):
        return [decode(v) for v in x]
    return x


def read(name):
    return decode(json.loads((HERE/name).read_text()))


def dot(x,y):
    return sum((a*b for a,b in zip(x,y)), F(0))


def check_exp(x, threshold):
    term = result = F(1)
    for k in range(1, 100):
        term *= x/k
        result += term
    assert result > threshold


checks = 0
receipt = read("RUN_RECEIPT.json")
for row in receipt["outputs"]:
    assert hashlib.sha256((HERE/row["path"]).read_bytes()).hexdigest() == row["sha256"]
    checks += 1

w = read("exact_identifiability.json")
mu = [b-a for a,b in w["common_loss_coordinate_intervals"]]
T = w["common_step_temperatures_K"]
lo,hi = w["v_dx_du_bounds"]
L = w["length_m"]
lam = w["dual_multiplier_K"]
for key, choose in [("minimum_mean_model", min), ("maximum_mean_model", max)]:
    model = w[key]
    assert dot(mu, model["v"]) == L
    assert all(lo <= v <= hi for v in model["v"])
    assert all(a*v == 1 for a,v in zip(model["a_per_m"],model["v"]))
    mean = dot(T,[m*v for m,v in zip(mu,model["v"])])/L
    dual = (lam*L+sum(m*choose((t-lam)*lo,(t-lam)*hi) for m,t in zip(mu,T)))/L
    assert mean == dual == model["physical_mean_K"]
    checks += 5
assert w["mean_diameter_K"] == w["exact_mean_interval_K"][1]-w["exact_mean_interval_K"][0]
assert 2*w["any_point_estimator_minimax_absolute_error_lower_K"] == w["mean_diameter_K"]
tri = w["continuous_triangular_temperature_witness"]
assert tri["mean_interval_K"] == [300+(x-300)/2 for x in w["exact_mean_interval_K"]]
assert 2*tri["minimax_error_lower_K"] == tri["mean_interval_K"][1]-tri["mean_interval_K"][0]
checks += 4

c = read("finite_calibration.json")
A,B = c["design"],c["left_inverse_dual_certificates"]
for i,row in enumerate(B):
    for j in range(4):
        assert dot(row,[a[j] for a in A]) == F(i==j)
        checks += 1
norms = [sum(abs(x) for x in row) for row in B]
assert norms == c["dual_L1_error_amplifications"]
systematic = c["separate_normalized_contrast_error_bounds"]["total_systematic_floor"]
parts = [v for k,v in c["separate_normalized_contrast_error_bounds"].items() if k!="total_systematic_floor"]
assert sum(parts) == systematic
assert c["infinite_integration_parameter_error_floor"] == [n*systematic for n in norms]
checks += 3
for plan in c["plans"]:
    N=10*plan["bins"]
    check_exp(plan["x"], 2*N/plan["joint_failure_probability_strictly_below"])
    m = plan["complex_mode_count_each_power"]
    root = plan["single_power_statistical_error_K_counts"]/1000-plan["x"]/m
    assert root>=0 and root*root>=2*plan["x"]/m
    total=2*plan["single_power_statistical_error_K_counts"]/50+systematic
    assert total==plan["contrast_plus_design_total_error"]
    assert [n*total for n in norms] == plan["parameter_error_radii"]
    checks += 4

a=read("boundary_alarm.json")
A,C,D=a["constructed_absorption_A"],a["constructed_C_in_kB_units"],a["constructed_D_C_minus_threshold_A"]
assert D==[[C[i][j]-a["threshold_K"]*A[i][j] for j in range(2)] for i in range(2)]
dual=a["exact_entrywise_dual_certificate"]
v=dual["v_unnormalized"]
assert dot(v,[dot(row,v) for row in D]) == dual["quadratic_form"]
assert dual["quadratic_form"]-dual["entry_error_bound"] == dual["strict_positive_lower_bound"]>0
p=a["heldout_mode_power_certificate"]
check_exp(p["finite_sample_x"],4/p["conditional_joint_failure_below"])
m=p["integration_s_each_state"]*p["equivalent_independent_bandwidth_Hz"]
root=p["statistical_difference_error_bound_K_counts"]/(2*p["power_upper_bound_K_counts"])-p["finite_sample_x"]/m
assert root>=0 and root*root>=2*p["finite_sample_x"]/m
margin=p["constructed_measured_power_centers_K_counts"][0]-p["constructed_measured_power_centers_K_counts"][1]-p["statistical_difference_error_bound_K_counts"]-sum(p["hypothetical_acquired_systematic_budgets_K_counts"].values())
assert margin == p["strict_positive_margin_after_all_stated_errors_K_counts"]>0
checks += 6

result={"status":"PASS", "exact_rational_assertions":checks,
        "scope":"Saved rational primal/dual, concentration enclosures and algebra checked independently of generator; physical premises and general analytic proofs are not machine formalized."}
(HERE/"VERIFY_RECEIPT.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
