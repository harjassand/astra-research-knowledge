"""Independent exact replay of saved counts; no additional simulation."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"core"))
from echo_compiler import sqrt_upper


def su(x):
    return sqrt_upper(x,bits=256)


def interval(x,n,ell):
    return (max(F(0),(F(x)-su(F(2*ell*x)))/n),
            min(F(1),(F(x+ell)+su(F(ell*ell+2*ell*x)))/n))


def round_up(x,bits=200):
    scale=1<<bits
    return F((x.numerator*scale+x.denominator-1)//x.denominator,scale)


def replay_source(source,ell):
    a=F(source["source_cap_premise"])
    pilot=source["pilot"]; main=source["first_return"]
    _,d2u=interval(pilot["returns"],pilot["trials"],ell)
    tail=round_up(a**(main["horizon"]-1)*d2u/(1-a))
    pooled=source["pooled_first_step_calibration"]
    n=pooled["trials"]; count=pooled["departures"]
    qlo,qhi=interval(count,n,ell)
    qhat=F(count,n); that=1-qhat
    delta=max(qhat-qlo,qhi-qhat)
    _,ru=interval(main["returns"],main["trials"],ell)
    _,eu=interval(main["even"],main["trials"],ell)
    olo,_=interval(main["odd"],main["trials"],ell)
    ru=min(F(1),ru+tail); eu=min(F(1),eu+tail)
    shi=max(F(0),min(ru,eu-olo))
    tlo,thi=1-qhi,1-qlo
    dp=max(1-a,1-thi-ru); dm=max(1-a,1+tlo-shi)
    qu=eu+ru*ru/(2*dp)+shi*shi/(2*dm)
    qm=(su(qu)+su(delta*delta/(1-a*a)))**2
    loss=1-that*that
    exact={"t_error_upper":delta,"missed_return_tail_upper":tail,
           "true_Galerkin_weighted_residual_upper":qu,
           "estimated_model_weighted_residual_upper":qm,
           "theta_squared_upper":qm/loss,
           "correction_noise_upper":delta/loss}
    for key,value in exact.items():
        assert value <= F(source["certificate"][key]), key
    exact.update({"pilot_squared_defect_upper":d2u,"a":a,
                  "initial_model":that,"coefficient_loss":loss,
                  "true_t_lower":tlo,"true_t_upper":thi})
    return exact


def replay_flags(comparison):
    receipt=comparison["fixed_flag"]; g=F(comparison["g"]); a=1-g/2
    z=F(4)+1/(1-a*a); exact=[]
    for flag,displayed in zip(receipt["flags"],receipt["certificates"]):
        n=flag["trials"]; x=flag["first_step_departures"]
        qlo,qhi=interval(x,n,10); qhat=F(x,n); t=1-qhat
        delta=max(qhat-qlo,qhi-qhat)
        _,pu=interval(flag["successes"],n,10)
        qu=z*pu; qm=(su(qu)+su(delta*delta/(1-a*a)))**2
        fields={"t_error_upper":delta,"Q_upper":qu,
                "theta_squared_upper":qm/(1-t*t),
                "correction_noise_upper":delta/(1-t*t)}
        for key,value in fields.items():assert value<=F(displayed[key]),key
        exact.append(fields)
    total=2*max(e["theta_squared_upper"] for e in exact)+max(e["correction_noise_upper"] for e in exact)
    assert total<=F(receipt["all_word_error_upper"])
    return {"g":str(g),"exact_all_word_error_upper":str(total),
            "all_word_error_upper_float":float(total),
            "displayed_receipt_dominates_exact_replay":True}


if __name__=="__main__":
    results=[]
    for name in ("RENEWAL_RESULTS_g20_n100000_cal2000000.json",
                 "RENEWAL_RESULTS_g100_n500000_cal2000000.json"):
        data=json.loads(Path(__file__).with_name(name).read_text())
        exact=[replay_source(s,data["arguments"]["ell"]) for s in data["sources"]]
        total=2*max(s["theta_squared_upper"] for s in exact)+max(
            s["correction_noise_upper"] for s in exact)
        displayed=F(data["all_words_same_calibration"]["total_scalar_output_error_upper"])
        assert total<=displayed
        results.append({"receipt":name,
            "sources":[{k:str(v) for k,v in e.items()} for e in exact],
            "exact_all_word_error_upper":str(total),
            "all_word_error_upper_float":float(total),
            "displayed_receipt_dominates_exact_replay":True})
    comparisons=json.loads(Path(__file__).with_name("RENEWAL_FLAG_COMPARISON.json").read_text())
    output={"method":"Fraction arithmetic and verified rational square-root upper bounds; no new observations.",
            "all_checks_passed":True,"receipts":results,
            "flag_comparisons":[replay_flags(c) for c in comparisons["comparisons"]]}
    path=Path(__file__).with_name("RENEWAL_EXACT_REPLAY.json")
    path.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({"all_checks_passed":True,
        "certified_bounds":[r["all_word_error_upper_float"] for r in results],
        "output":str(path)},indent=2))
