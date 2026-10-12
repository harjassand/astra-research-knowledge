"""Rational embedded-race assay: no exponential, log, or floating probability.

Under independent unbiased random bits, the endpoint and event counts have exactly
those of the rational CTMC stopped by its independent reset clock. Python's seeded
Random is used only to make these research tests reproducible. This does not claim
that a finite PRNG seed creates genuinely independent physical randomness.

The hidden simulator still owns and stores its full adjacency data. Only its small
Summary is returned to inference. Physical duration is NOT simulated here; expected
duration and realised duration are intentionally distinguished.
"""
from __future__ import annotations
from fractions import Fraction
from math import lcm
from random import Random
from dataclasses import asdict
import math, json, time
from pathlib import Path
import numpy as np
from flux_design import Summary,concentration_radii,build_outer_lp,solve_outer,exact_dual_upper
from opaque_assay import generate_instance
from benchmark import matrices,stationary,true_optimum,exact_probes
from rational_confidence import calibration_radii,validation_radius

ROOT=Path(__file__).resolve().parent

def sample_integer(inst, rates, samples: int, seed: int):
    if samples<=0: raise ValueError('Positive sample count required.')
    k=inst.channels
    rates=[Fraction(str(x)) for x in rates]
    if len(rates)!=k or min(rates)<0: raise ValueError('Invalid rates.')
    rho=Fraction(str(inst.reset_rate)); bg=Fraction(str(inst.background_rate))
    if rho<=0 or bg<0: raise ValueError('Invalid background/reset rates.')
    races=[]
    for u in rates+[Fraction(0)]:
        scale=lcm(rho.denominator,bg.denominator,u.denominator)
        a,b,c=int(rho*scale),int(bg*scale),int(u*scale)
        races.append((a,a+b,a+b+c))
    # randrange in CPython uses getrandbits plus rejection; thus uniform integer
    # sampling has no float-probability discretisation under the random-bit model.
    rng=Random(seed); pick=rng.randrange
    adj=inst.adjacency.tolist(); dst=inst.destinations.tolist(); reward=inst.reward.tolist()
    degree=len(adj[0]); source=[0]*k;counts=[0]*k;rs=nb=nc=mx=0
    for _ in range(samples):
        state=pick(k);cnt=0
        while True:
            a,b,total=races[state if state<k else k]
            event=pick(total)
            if event<a:
                if state<k:source[state]+=1
                rs+=reward[state];mx=max(mx,cnt)
                break
            if event<b:
                state=adj[state][pick(degree)];nb+=1
            else:
                counts[state]+=1;nc+=1;cnt+=1;state=dst[state]
    # nan is a sentinel, not a claimed elapsed physical duration.
    summary=Summary(samples,source,rs,counts,float('nan'),nb,nc,mx)
    return summary,dict(expected_physical_duration=str(Fraction(samples)/rho),
                        race_integer_max_bits=max(t.bit_length() for _,_,t in races),
                        duration_was_simulated=False)

def serializable(s):
    d=asdict(s);d['physical_time']=None
    return d

def run():
    inst=generate_instance(160,4,714032,background_rate=1,reset_rate=1)
    k=4;ncal=800000;nval=400000;cap=600;U=[1000000]*k
    summaries=[];resources=[];begin=time.perf_counter()
    for j in range(k+1):
        rate=[0]*k
        if j:rate[j-1]=cap
        s,resource=sample_integer(inst,rate,ncal,seed=884100+j)
        summaries.append(s);resources.append(resource)
    acquisition_seconds=time.perf_counter()-begin
    means=np.array([s.means() for s in summaries])
    r=np.array([summaries[j+1].intervention_counts[j]/ncal for j in range(k)])
    etaq,etarq,radius_proof=calibration_radii(ncal,k,Fraction(1,200),Fraction(1),Fraction(1))
    eta,etar=float(etaq),float(etarq)
    model=build_outer_lp(means,r,np.repeat(cap,k),eta,etar,2)
    start=time.perf_counter();fit=solve_outer(model);lp_seconds=time.perf_counter()-start
    start=time.perf_counter()
    cert=exact_dual_upper(summaries,[cap]*k,etaq,etarq,1,1,fit['dual'])
    cert_seconds=time.perf_counter()-start
    # Any chosen rates are valid; independent validation covers numerical rounding.
    # Use explicit rational rates rounded to 6 decimal places, then implement those.
    rates=[Fraction(round(u*1000000),1000000) for u in fit['rates']]
    start=time.perf_counter();val,vr=sample_integer(inst,rates,nval,884999);val_seconds=time.perf_counter()-start
    radiusq=validation_radius(nval,Fraction(1,200));radius=float(radiusq)
    lowerq=max(Fraction(0),Fraction(val.reward_sum,nval)-radiusq);lower=float(lowerq)
    satq=Fraction(6,cap);sat=float(satq)
    upperq=min(Fraction(1),Fraction(cert['upper_exact'])+satq);upper=float(upperq)
    pre=matrices(inst);values_true,r_true=exact_probes(inst,np.repeat(cap,k),pre)
    achieved=float(inst.reward@stationary(inst,[float(x) for x in rates],pre))
    optimum=true_optimum(inst,U,pre);capped=true_optimum(inst,[cap]*k,pre)
    event=bool(np.max(abs(means-values_true))<=eta and np.max(abs(r-r_true))<=etar)
    assert event and lower<=achieved<=upper and optimum<=upper
    # Check error radius rounding with high precision, not just ordinary float ceil.
    import mpmath as mp
    with mp.workdps(80):
        t=mp.log(2*29/mp.mpf('.005'))
        assert mp.mpf(str(eta))>=mp.sqrt(t/(2*ncal))
        assert mp.mpf(str(etar))>=2*(2*mp.sqrt(t/ncal)+t/ncal)
        assert mp.mpf(str(radius))>=mp.sqrt(mp.log(2/mp.mpf('.005'))/(2*nval))
    out=dict(hidden_seed=714032,hidden_states=160,controls=k,calibration_settings=5,
        calibration_episodes_per_setting=ncal,validation_episodes=nval,total_episodes=5*ncal+nval,
        learned_rational_rates=list(map(str,rates)),nominal_joint_confidence=.99,rational_confidence_proof=radius_proof,
        calibration_flux_estimates=r.tolist(),endpoint_error_radius=eta,flux_error_radius=etar,
        exact_rational_dual_certificate=cert,validation_reward_mean=val.reward_sum/nval,
        validation_radius=radius,achieved_lower=lower,capped_optimum_upper=cert['upper'],
        saturation_allowance=sat,original_optimum_upper=upper,global_regret_upper=math.nextafter(float(upperq-lowerq),math.inf),
        global_regret_upper_exact=str(upperq-lowerq),original_optimum_upper_exact=str(upperq),achieved_lower_exact=str(lowerq),
        truth_optimum=optimum,truth_capped_optimum=capped,truth_achieved=achieved,truth_regret=optimum-achieved,
        confidence_event_checked_against_truth=event,
        expected_physical_duration=(5*ncal+nval),realised_physical_duration=None,
        background_events=sum(x.background_events for x in summaries)+val.background_events,
        controlled_events=sum(x.intervention_events for x in summaries)+val.intervention_events,
        maximum_episode_controls=max([s.maximum_episode_interventions for s in summaries]+[val.maximum_episode_interventions]),
        acquisition_seconds=acquisition_seconds,inference_lp_seconds=lp_seconds,
        exact_dual_seconds=cert_seconds,validation_seconds=val_seconds,
        integer_race_max_bits=max([x['race_integer_max_bits'] for x in resources]+[vr['race_integer_max_bits']]),
        sample_summaries=[serializable(s) for s in summaries],validation_summary=serializable(val),
        assumptions='Exact endpoint/count sampling algorithm under unbiased random bits; experiment uses a reproducible finite PRNG. Model/actuator/clock assumptions are not established by the algorithm.')
    (ROOT/'integer_results.json').write_text(json.dumps(out,indent=2,allow_nan=False))
    print(json.dumps({k:v for k,v in out.items() if k not in ['sample_summaries','validation_summary','exact_rational_dual_certificate']},indent=2))

if __name__=='__main__':run()
