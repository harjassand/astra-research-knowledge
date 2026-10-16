"""Independent numerical reconstruction checks and authored-only frozen manifest."""
import hashlib
import json
import math
from pathlib import Path
from fractions import Fraction
import subprocess
import numpy as np
from acquire_and_analyze import read_xlsx,threshold_delta
from electrical_and_fixed_model import model

R=Path(__file__).resolve().parent
W=Path("/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016")
P=R.parents[1]/"originals/catalysis/final_Fig2.xlsx"
pin="9dbe934e5475f415c2d160a6c0715534aafa546b"

checks={"scope":"Finite numerical checks only. Analytic arguments are separately stated in PROOFS.md. No physical or external mathematical validation.","W_expected_pin":pin}
checks["W_observed_pin"]=subprocess.check_output(["git","rev-parse","HEAD"],cwd=W,text=True).strip()
assert checks["W_observed_pin"]==pin
checks["input_sha256_after"]=hashlib.sha256(P.read_bytes()).hexdigest()
checks["fresh_source_sha256"]=hashlib.sha256((R/"external_excluded_from_publication/final_Fig2_fresh.xlsx").read_bytes()).hexdigest()
assert checks["input_sha256_after"]==checks["fresh_source_sha256"]=="47a571bed2750c89ba2cf38cc75235f1e7497727c57e2b9b28fc3fdfc667a3fe"

wb=read_xlsx(P);c=wb["Figure 2 c"]["cells"];d=wb["Figure 2 d"]["cells"]
assert all((Fraction(c[f"B{j}"]),Fraction(c[f"C{j}"]))==(Fraction(d[f"B{j}"]),Fraction(d[f"C{j}"])) for j in range(2,32))
checks["paired_grid_conditions_checked"]=30
checks["source_formula_count"]=sum(len(s["formulas"]) for s in wb.values())
loaded=json.loads((R/"workbook_checks.json").read_text())
g=sorted([x for x in loaded["grid_rows"] if x["duty_h_over_d"]=="10"],key=lambda x:x["row"])
checks["longest_pair_sensitivity"]={"XS":threshold_delta(g[-2:],"XS"),"S":threshold_delta(g[-2:],"S"),"X":threshold_delta(g[-2:],"X")}

cases=0;worst=0
for mu in np.geomspace(.001,1000,21):
    for lam in np.geomspace(.001,1000,21):
        means=[]
        for scale in [.001,.01,.1,1]:
            a=lam;c0=10*mu
            F=(-math.expm1(-a*scale))*(-math.expm1(-c0*scale))/(mu*scale*11*(-math.expm1(-(a+c0)*scale)))
            means.append(10/11-F)
        worst=min(worst,min(means[i+1]-means[i] for i in range(3)))
        assert all(means[i+1]>=means[i]-1e-12 for i in range(3))
        cases+=1
checks["scalar_monotonicity_finite_cases"]=cases
checks["scalar_min_increment"]=worst

models=json.loads((R/"fixed_model_checks.json").read_text())
params=[models["illustrative_fixed_parameters"],models["parameters"]]
max_return_error=max_integral_error=max_simplex_violation=0
for p in params:
    k,r,w=p["k_per_s"],p["r_per_s"],p["w_per_s"]
    beta=p.get("beta",p.get("beta_illustrative"));bp,A=p["bplus"],p["A"]
    for h,duration in [(.01,.001),(.1,.01),(1,.1),(10,1),(.1,.001),(1,.01),(10,.1),(1,1)]:
        b,state=model(h,duration,k,r,w,bp,beta,A)
        s=np.linspace(0,h,20001)
        occupancy=state["I0"]*np.exp(-r*s)+k*state["W0"]*(np.exp(-r*s)-np.exp(-k*s))/(k-r)
        integral=float(np.trapezoid(occupancy,s))
        recovered=(h*bp-A*integral+duration*beta)/(h+duration)
        error=abs(b-recovered);max_integral_error=max(max_integral_error,error)
        assert error<2e-7
        W_end=state["W0"]*math.exp(-k*h)
        I_end=state["I0"]*math.exp(-r*h)+k*state["W0"]*(math.exp(-r*h)-math.exp(-k*h))/(k-r)
        return_W=1-math.exp(-w*duration)+math.exp(-w*duration)*W_end
        return_I=math.exp(-w*duration)*I_end
        max_return_error=max(max_return_error,abs(return_W-state["W0"]),abs(return_I-state["I0"]))
        max_simplex_violation=max(max_simplex_violation,-min(state.values()),max(state.values())-1)
        assert min(state.values())>=-1e-12 and max(state.values())<=1+1e-12
        assert 0<=b<=max(bp,beta)+1e-12
checks["sequential_model_quadrature_max_b_error"]=max_integral_error
checks["sequential_model_return_map_max_error"]=max_return_error
checks["sequential_model_simplex_max_violation"]=max_simplex_violation
checks["illustrative_peak_time_s"]=math.log(.5/.1)/(.5-.1)
checks["illustrative_fixed_N_delta05_alpha05"]=math.ceil(8*math.log(20)/.05**2)

routes={
"N887_exact_causal_proof":"updates/GA-conformal-causal-genesis-20261016/package/derived/root/CAUSAL_IDENTIFIABILITY_THEOREM.md",
"N884_exact_fresh_cohort_proof":"updates/FZ-positive-memory-genesis-20261016/package/derived/workers/fz_catalysis_causal_genesis/CAUSAL_IDENTIFICATION.md",
"N887_dossier":"frontier/dossiers/N887.txt",
"N884_dossier":"frontier/dossiers/N884.txt"}
checks["pinned_proof_sources"]={name:{"path":path,"sha256":hashlib.sha256((W/path).read_bytes()).hexdigest()} for name,path in routes.items()}
(R/"verification_results.json").write_text(json.dumps(checks,indent=2)+"\n")

files=[]
for path in sorted(R.iterdir()):
    if path.is_file() and path.name!="FROZEN.json":
        files.append({"path":path.name,"bytes":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
manifest={"status":"FROZEN_FOR_PARENT_REVIEW","physical_control":"NOT_ACQUIRED","W_pin":pin,"external_validation":"UNKNOWN","historical_novelty":"UNKNOWN","files":files,
          "excluded_from_authored_pack":["external_excluded_from_publication/","__pycache__/"],
          "input_writes":False,"W_writes":False,"outreach":False,"current_peer_worker_outputs_read":False}
(R/"FROZEN.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(checks,indent=2))
