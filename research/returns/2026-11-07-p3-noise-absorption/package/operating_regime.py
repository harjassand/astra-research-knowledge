"""An exact one-actuator noisy native law and its full-output rate certificate.

Each factor's warranted generator is lambda D[X] + a(D[down]+e D[X]).
For physical targets U(tensor tau_i)U*, every generator is dressed by the SAME
supplied U. This is a specific native affine law, not a generic apparatus claim.
"""
from fractions import Fraction as F
from pathlib import Path
import json, math
import numpy as np
from scipy.linalg import expm
from scipy.stats import binom
from noise_absorption import X, noise_super, reset_super, choi_from_super

ROOT=Path(__file__).resolve().parent


def operating_rate(p, background, self_noise, cap=None):
    p=F(p);background=F(background);self_noise=F(self_noise)
    if background<=0 or self_noise<0 or not 0<p<F(1,2):
        raise ValueError("Need lambda>0, e>=0, 0<p<1/2")
    denominator=p*(1+2*self_noise)-self_noise
    if denominator<=0:
        return {"feasible":False,"reason":"Target at/below exact self-noise floor",
                "floor":str(self_noise/(1+2*self_noise))}
    a=background*(1-2*p)/denominator
    if cap is not None and a>F(cap):
        return {"feasible":False,"reason":"Required native rate exceeds supplied cap","required":str(a)}
    w=background+self_noise*a
    assert w/(a+2*w)==p
    return {"feasible":True,"p":str(p),"background":str(background),"self_noise":str(self_noise),
            "control_rate":str(a),"floor":str(self_noise/(1+2*self_noise)),
            "x_decay":str(a/2),"y_decay":str(a/2+2*w),"z_decay":str(a+2*w),
            "total_jump_activity_per_site":str(background+(1+self_noise)*a)}


def binomial_tv(n,p,q):
    if p==q:return 0.
    if p>q:p,q=q,p
    crossing=-n*math.log((1-q)/(1-p))/math.log(q*(1-p)/(p*(1-q)))
    k=min(n,max(-1,math.floor(crossing)))
    return float(binom.cdf(k,n,p)-binom.cdf(k,n,q))


def exact_stationary_interval_certificate(n,p,lambda_interval,e_interval,a_interval,epsilon):
    p=F(p);ll,lh=map(F,lambda_interval);el,eh=map(F,e_interval);al,ah=map(F,a_interval)
    assert 0<p<1 and 0<ll<=lh and 0<=el<=eh and 0<al<=ah
    def pop(l,e,a):return (l+e*a)/(2*l+(1+2*e)*a)
    ql=pop(ll,el,ah);qh=pop(lh,eh,al)
    assert 0<ql<=qh<1
    z=max(abs(ql-p),abs(qh-p));v=min(p*(1-p),ql*(1-ql),qh*(1-qh))
    bound_squared=n*z*z/(4*v)
    return {"arithmetic":"fractions.Fraction; exact interval monotonicity and rational KL/Pinsker squared bound",
            "n":n,"p":str(p),"lambda_interval":[str(ll),str(lh)],"e_interval":[str(el),str(eh)],
            "a_interval":[str(al),str(ah)],"q_interval":[str(ql),str(qh)],"max_population_error":str(z),
            "variance_lower":str(v),"global_error_squared_bound":str(bound_squared),
            "epsilon":str(F(epsilon)),"certified":bool(bound_squared<=F(epsilon)**2),
            "display_only_global_bound":math.sqrt(float(bound_squared)),
            "minimum_decay_rate":str(al/2),
            "scope":"Conditional on simultaneously valid intervals and the native model; intervals are declared, not experimentally acquired."}


def run():
    rec=operating_rate("1/5","1","1/10",cap="5")
    assert rec["control_rate"]=="30/7" and rec["x_decay"]=="15/7"
    a=float(F(rec["control_rate"]));e=.1;lam=1.;p=.2
    down=np.array([[0,1],[0,0]],complex)
    l=noise_super(np.zeros((2,2)),[np.sqrt(lam+e*a)*X,np.sqrt(a)*down])
    tau=np.diag([1-p,p])
    rec["stationarity_binary64_residual"]=float(np.linalg.norm(l@tau.reshape(-1,order="F")))
    rec["time_samples"]=[]
    for t in [.1,.5,1.,2.,4.]:
        delta=choi_from_super(expm(t*l)-reset_super(tau),2)/2
        rec["time_samples"].append({"time":t,"max_ent_reference_attained_error":float(np.linalg.norm(delta,ord="nuc")/2),
                                    "complete_upper_bound":min(1.,2*math.exp(-a*t/2))})
        assert rec["time_samples"][-1]["max_ent_reference_attained_error"]<=rec["time_samples"][-1]["complete_upper_bound"]+1e-12
    rec["failed_cap4"]=operating_rate("1/5","1","1/10",cap="4")
    rec["failed_target1over20"]=operating_rate("1/20","1","1/10")
    rec["scope"]="Declared affine native-generator model with all per-command self-noise in e; no device calibration or execution."
    table=[]
    for n in [1,100,10000,1000000]:
        eps=.01;t=math.log(2*n/eps)/(a/2)
        table.append({"n":n,"epsilon":eps,"parallel_model_time":t,
                      "total_norm_activity_through_preparation":n*float(F(rec["total_jump_activity_per_site"]))*t,
                      "total_control_norm_activity":n*(1+e)*a*t,
                      "residual_half_diamond_rate_budget_for_additional_error_0.001":.001*(a/2)/(2*(1+math.log(2*n))),
                      "note":"Continuing residual bound uses complete decay min(1,2N exp(-g t)); modeled self-noise is already included, residuals are separate."})
    rec["resource_table"]=table
    (ROOT/"NOISY_NATIVE_REGIME.json").write_text(json.dumps(rec,indent=2)+"\n")
    calibration=[{"n":int(n),"p":.2,"q":.202,"global_trace_distance":binomial_tv(int(n),.2,.202),
                  "single_factor_trace_distance":.002} for n in [1,100,10000,1000000,100000000]]
    (ROOT/"GLOBAL_CALIBRATION_SEPARATION.json").write_text(json.dumps(calibration,indent=2)+"\n")
    # Exact finite-time inverse within the declared one-actuator family.
    h=.1
    acquisition=[]
    recovered=[]
    for aa in [0.,a]:
        w=lam+e*aa;rate=2*w+aa;pp=w/rate
        s=-math.expm1(-rate*h);up=pp*s;dn=(1-pp)*s
        rr=-math.log1p(-(up+dn))/h
        ww=rr*up/(up+dn);ar=rr*(dn-up)/(up+dn)
        recovered.append((ww,ar))
        acquisition.append({"command_rate":aa,"h":h,"u":up,"v":dn,
                            "recovered_w":ww,"recovered_a":ar})
    lr=recovered[0][0];er=(recovered[1][0]-lr)/recovered[1][1]
    assert abs(lr-lam)<1e-12 and abs(er-e)<1e-12
    acq={"synthetic_records":acquisition,"recovered_lambda":lr,"recovered_e":er,
         "statistical_example":{"delta_probability":.001,"failure_probability":.01,"number_probabilities":4,
                                "trials_per_probability":math.ceil(math.log(800)/(2*.001**2)),
                                "total_trials":4*math.ceil(math.log(800)/(2*.001**2))},
         "scope":"Finite-time inverse within a WARRANTED model with calibrated 0/1 preparation/readout; coherence, SPAM and model validity are not inferred from population data alone."}
    (ROOT/"FINITE_TIME_ACQUISITION_AUDIT.json").write_text(json.dumps(acq,indent=2)+"\n")
    radius=F(1,100000);aa=F(30,7)
    conf=exact_stationary_interval_certificate(1000000,"1/5",[F(1)-radius,F(1)+radius],
          [F(1,10)-radius,F(1,10)+radius],[aa-radius,aa+radius],"3/500")
    assert conf["certified"]
    (ROOT/"EXACT_GLOBAL_PARAMETER_CERTIFICATE.json").write_text(json.dumps(conf,indent=2)+"\n")
    print(json.dumps({"native":rec,"calibration":calibration},indent=2))


if __name__=="__main__":run()
