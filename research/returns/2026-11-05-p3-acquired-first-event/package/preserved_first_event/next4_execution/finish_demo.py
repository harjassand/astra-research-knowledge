"""Compile finite event clocks, attach records, and compare independent references.

Run block_sampler first. This program acquires q_G from its histogram; reference
q_G and lifetime are loaded only after all event-clock samples are generated.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,math,random,time
from finite_geometric import GeometricClockCompiler

ROOT=Path(__file__).resolve().parent

def main():
    start=time.perf_counter()
    raw=json.loads((ROOT/"block_results.json").read_text())
    n=raw["calibration_proposals"]
    mu=sum(F(v,int(k)) for k,v in raw["calibration_histogram"].items())/n
    p=F(3,2**raw["rare_bits"])
    qhat=p*(raw["L"]+1)*mu
    clock=GeometricClockCompiler(qhat,F(1,2**24))
    rng=random.Random(2026110505)
    records=[];multiplications=0;cdf_queries=0;bits=0
    t0=time.perf_counter()
    for record in raw["records"]:
        r=dict(record)
        if not record["early"]:
            k,meta=clock.sample(rng)
            offset=2*raw["buffer"]+k*(raw["L"]+raw["buffer"])
            calendar=(offset<<raw["digits"])+r["block_bin"]
            multiplications+=meta["actual_fixed_point_multiplications"]
            cdf_queries+=meta["actual_cdf_evaluations"]
            bits+=meta["actual_random_bits"]
            r["failed_blocks"]=str(k)
        else:
            calendar=r["block_bin"];r["failed_blocks"]="0"
        r["calendar_bin"]=str(calendar)
        r["physical_time_denominator"]=raw["R"]*(1<<raw["digits"])
        # A path integrity check, independent of any reference probability.
        state=r["window_initial"];age=raw["H"]*(1<<raw["digits"])
        for j,(a,old,new) in enumerate(r["jumps"]):
            assert old==state and 0<=a<=age
            if j+1<len(r["jumps"]):assert new<2
            state=new;age=a
        assert state==r["terminal"] and state>=2 and r["jumps"][-1][0]==0
        records.append(r)
    geometric_seconds=time.perf_counter()-t0
    (ROOT/"event_records.json").write_text(json.dumps({
        "clock_certificate":clock.certificate(),
        "time_units":"calendar_bin / physical_time_denominator",
        "records":records},indent=2)+"\n")

    # Only now read the exact reference, which never supplied the clock rate.
    ref=json.loads((ROOT/"exact_reference.json").read_text())
    mean=float(ref["mean_physical"])
    values=sorted(int(r["calendar_bin"])/r["physical_time_denominator"]/mean
                  for r in records)
    from exact_reference import rational_model,m
    import mpmath as mp
    mp.mp.dps=160
    pi,q,_,_=rational_model()
    qa=mp.matrix([[m(q[i][j]/4) for j in range(2)] for i in range(2)])
    tr=qa[0,0]+qa[1,1];det=mp.det(qa)
    fast=(tr-mp.sqrt(tr*tr-4*det))/2;slow=det/fast
    derivative=qa[0,0]+qa[0,1]
    cs=(derivative-fast)/(slow-fast);cf=1-cs
    mean_norm=mp.mpf(ref["mean_normalized"])
    def cdf_scaled(t):
        return float(1-cs*mp.exp(slow*mean_norm*t)-cf*mp.exp(fast*mean_norm*t))
    size=len(values)
    ks=max(max((i+1)/size-cdf_scaled(t),cdf_scaled(t)-i/size)
           for i,t in enumerate(values))
    counts=Counter(f"{r['preceding']}->{r['terminal']}" for r in records)
    exact={k:float(v) for k,v in ref["first_entry_joint"].items()}
    mark_tv=sum(abs(counts[k]/size-exact[k]) for k in exact)/2

    # Exact rational sufficient calibration/schedule certificate for ideal draws.
    h=F(27,1024);lower=mu-h;eta=F(1,2**14)
    exponent=2*n*h*h
    exp_partial=sum(exponent**k/math.factorial(k) for k in range(13))
    assert exp_partial>200
    structure=(eta/(1-eta)+(1+eta)/(1-eta)*
        F(int(raw["H"])+raw["buffer"]+2,raw["L"]+1)/lower+
        (1+eta)*p*(raw["buffer"]+1))
    geometric_rate_error=h/lower
    certificate={
        "palm_mean_numerator":str(mu.numerator),
        "palm_mean_denominator":str(mu.denominator),
        "palm_mean_estimate":float(mu),"radius":str(h),
        "mean_lower":float(lower),"mean_upper":float(mu+h),
        "confidence_failure_upper":float(2/exp_partial),
        "hoeffding_exponent":str(exponent),"certified_eta":str(eta),
        "structural_upper_under_ideal_block_sampling":float(structure),
        "geometric_upper_under_mean_interval":float(geometric_rate_error),
        "combined_upper_before_finite_primitive_errors":float(structure+geometric_rate_error),
        "qhat_numerator":str(qhat.numerator),"qhat_denominator":str(qhat.denominator),
        "scope":"Confidence assumes ideal independent Palm clocks. C++ uses floating distribution primitives whose error is not certified. The geometric compiler uses exact integer arithmetic."}
    (ROOT/"acquired_schedule_certificate.json").write_text(json.dumps(certificate,indent=2)+"\n")
    summary={
        "stationary_failure_probability":float(p),
        "q_G_estimate":float(qhat),"q_G_reference":float(ref["q_G"]),
        "q_G_relative_error":float(qhat)/float(ref["q_G"])-1,
        "palm_mean_estimate":float(mu),"palm_mean_reference":float(ref["palm_mean"]),
        "event_records":size,"entry_counts":dict(counts),
        "entry_joint_empirical_TV":mark_tv,
        "time_CDF_empirical_KS":ks,
        "sample_mean_over_true_mean":sum(values)/size,
        "reference_mean_physical":mean,
        "min_calendar_bin":str(min(int(r["calendar_bin"]) for r in records)),
        "max_calendar_bin":str(max(int(r["calendar_bin"]) for r in records)),
        "geometric_clock":clock.certificate(),
        "geometric_actual":{"multiplications":multiplications,"cdf_queries":cdf_queries,
                            "fair_bits_assumed":bits,"seconds":geometric_seconds},
        "native_counts":raw["counts"],"native_seconds":raw["seconds"],
        "instance_certificate":certificate,"total_postprocess_seconds":time.perf_counter()-start,
        "scope":["Seeded PRNG diagnostic, not laboratory measurements.",
                 "Exact integer kernel choices; floating Poisson, beta/order-statistic and binomial clocks.",
                 "Integer geometric compiler has proved finite-bit TV and resource bounds under fair bits.",
                 "Four-state direct exact solver is faster and is the appropriate baseline.",
                 "This does not execute the general correlated Gibbs static algorithm or the conservative uniform schedule."]}
    (ROOT/"execution_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
    fig,axes=plt.subplots(1,2,figsize=(11,4.2),layout="constrained")
    grid=np.linspace(0,5,300)
    axes[0].plot(grid,[cdf_scaled(float(t)) for t in grid],color="#143e63",lw=2,label="Exact four-state law")
    axes[0].step(values,np.arange(1,size+1)/size,where="post",color="#c66b22",lw=1.3,label="Generated first-event records")
    axes[0].set(xlim=(0,5),ylim=(0,1.02),xlabel="First-event time / exact mean",ylabel="Cumulative probability",
                title=f"Finite event clock across a mean of {mean:.2e} time units")
    axes[0].legend(loc="lower right",frameon=False,fontsize=8)
    keys=["0->2","1->2","0->3","1->3"];pos=np.arange(4);w=.25
    axes[1].bar(pos-w,[exact[k] for k in keys],w,color="#143e63",label="Exact entry law")
    axes[1].bar(pos,[counts[k]/size for k in keys],w,color="#c66b22",label="Generated records")
    axes[1].bar(pos+w,[float(ref["wrong_forward_as_reverse_joint"][k]) for k in keys],w,color="#9cabb8",label="Wrong reverse kernel")
    axes[1].set(xticks=pos,xticklabels=[k.replace("->",r"$\to$") for k in keys],
                ylabel="Probability of transition entering failure",
                title="The direction of the precursor matters",ylim=(0,.53))
    axes[1].legend(frameon=False,fontsize=8)
    fig.savefig(ROOT/"event_law_diagnostic.pdf")
    fig.savefig(ROOT/"event_law_diagnostic.png",dpi=180)
    print(json.dumps({k:summary[k] for k in ["q_G_relative_error","entry_joint_empirical_TV",
                     "time_CDF_empirical_KS","sample_mean_over_true_mean","geometric_actual"]},indent=2))
if __name__=="__main__":main()
