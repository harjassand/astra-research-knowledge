"""Compare complete costs using the same variance-aware calibration bounds."""
from decimal import Decimal as D
from fractions import Fraction as F
from pathlib import Path
import json
import sys
import math
from renewal_acquisition import binomial_interval, dec, SLACK

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "core"))
from markov_residual_events import MembershipInstrument


def certify_flags(inv_g, flags, depth=4, ell=10):
    g=F(1,inv_g); a=1-g/2
    z=dec(depth)+1/(1-dec(a)**2)
    out=[]
    for flag in flags:
        n=flag["trials"]
        lo,hi=binomial_interval(flag["first_step_departures"], n, ell)
        q=dec(flag["first_step_departures"])/dec(n); t=1-q
        err=max(q-lo,hi-q)+SLACK
        _,pu=binomial_interval(flag["successes"],n,ell)
        qu=z*pu+SLACK
        qm=(qu.sqrt()+err/(1-dec(a)**2).sqrt())**2+SLACK
        out.append({"t_error_upper":str(err), "Q_upper":str(qu),
                    "theta_squared_upper":str(qm/(1-t*t)+SLACK),
                    "correction_noise_upper":str(err/(1-t*t)+SLACK)})
    bound=2*max(D(r["theta_squared_upper"]) for r in out)+max(
        D(r["correction_noise_upper"]) for r in out)
    return {"g":str(g), "flags":flags, "certificates":out,
            "all_word_error_upper":str(bound+SLACK),
            "joint_failure_probability_upper":6*math.exp(-ell),
            "cost":{"logical_trials":sum(f["trials"] for f in flags),
                    "physical_preparations_upper":sum(
                        1+f["first_step_departures"]-f["successes"] for f in flags),
                    "primitive_steps":sum(f["primitive_applications"] for f in flags),
                    "membership_readings":sum(f["membership_bits"] for f in flags)}}


def main():
    old=json.loads((ROOT/"results/MARKOV_RESIDUAL_EVENTS.json").read_text())
    first=certify_flags(20,[r["flag"] for r in old["receipts"]])
    g=F(1,100); a=1-g/2
    hidden=[[[1-g,g],[g,F(1,4)]],[[1-2*g,g],[g,F(1,3)]]]
    instrument=MembershipInstrument(hidden,seed=2026102821)
    flags=[instrument.mixed_flag(i,12_000_000,4,1/(1-a*a)) for i in range(2)]
    second=certify_flags(100,flags)
    comparisons=[]
    for inv_g, count, fixed in ((20,100000,first),(100,500000,second)):
        renewal_path=Path(__file__).with_name(
            f"RENEWAL_RESULTS_g{inv_g}_n{count}_cal2000000.json")
        renewal=json.loads(renewal_path.read_text())
        comparisons.append({
            "g":str(F(1,inv_g)), "fixed_flag":fixed,
            "renewal":{"all_word_error_upper":renewal["all_words_same_calibration"][
                "total_scalar_output_error_upper"],
                "joint_failure_probability_upper":renewal["joint_failure_probability_upper"],
                "cost":renewal["total_charged_cost"],"source_file":renewal_path.name}})
    result={"comparisons":comparisons,
            "scope":"Executed finite budgets; this is not a proof of global estimator optimality.",
            "shared_confidence_method":"Rare departure-count and rare event binomial bounds.",
            "cemetery_hidden_from_observer":True}
    path=Path(__file__).with_name("RENEWAL_FLAG_COMPARISON.json")
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"comparisons":[{
        "g":c["g"],
        "flag_error":float(D(c["fixed_flag"]["all_word_error_upper"])),
        "flag_cost":c["fixed_flag"]["cost"],
        "renewal_error":float(D(c["renewal"]["all_word_error_upper"])),
        "renewal_cost":c["renewal"]["cost"]} for c in comparisons],
        "output":str(path)},indent=2))


if __name__=="__main__":
    main()
