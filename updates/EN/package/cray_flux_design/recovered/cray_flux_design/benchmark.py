"""Independent synthetic tests and a matched known-model occupation-measure LP.

The hidden model is generated before fitting. Exact equilibrium solves are truth
checks and exact-input diagnostics, not the sampled acquisition protocol.
"""
from __future__ import annotations
import json, time, platform
from pathlib import Path
from dataclasses import asdict
import numpy as np
from scipy.optimize import linprog
from scipy.linalg import solve
from flux_design import build_outer_lp,solve_outer,concentration_radii,exact_dual_upper
from opaque_assay import generate_instance

ROOT=Path(__file__).resolve().parent

def matrices(inst):
    n=len(inst.reward);k=inst.channels;degree=inst.adjacency.shape[1]
    L=-np.eye(n)*inst.background_rate
    for src in range(n):
        for dst in inst.adjacency[src]:L[dst,src]+=inst.background_rate/degree
    B=np.zeros((n,k))
    for j,dst in enumerate(inst.destinations):B[j,j]-=1;B[dst,j]+=1
    nu=np.zeros(n);nu[:k]=1/k
    return L,B,nu

def stationary(inst,rate,pre=None):
    L,B,nu=matrices(inst) if pre is None else pre
    n=len(nu);k=inst.channels
    T=L.copy()
    T[:,:k]+=B*np.asarray(rate)[None,:]
    p=solve(inst.reset_rate*np.eye(n)-T,inst.reset_rate*nu,assume_a='gen',check_finite=False)
    if abs(p.sum()-1)>1e-7 or p.min()<-1e-8:raise ArithmeticError('Invalid truth solve.')
    return p

def true_optimum(inst,bounds,pre=None):
    L,B,nu=matrices(inst) if pre is None else pre
    n=len(nu);k=inst.channels
    Aeq=np.c_[L-inst.reset_rate*np.eye(n),B]
    A=np.zeros((k,n+k))
    for j in range(k):A[j,j]=-bounds[j];A[j,n+j]=1
    result=linprog(-np.r_[inst.reward,np.zeros(k)],A_ub=A,b_ub=np.zeros(k),
                   A_eq=Aeq,b_eq=-inst.reset_rate*nu,bounds=(0,None),method='highs')
    if not result.success:raise RuntimeError(result.message)
    return float(-result.fun)

def exact_probes(inst,s,pre=None):
    k=inst.channels;pre=matrices(inst) if pre is None else pre
    values=[];r=[]
    for j in range(k+1):
        rate=np.zeros(k)
        if j:rate[j-1]=s[j-1]
        p=stationary(inst,rate,pre)
        values.append(np.r_[p[:k],inst.reward@p])
        if j:r.append(s[j-1]*p[j-1])
    return np.array(values),np.array(r)


def exact_suite():
    rng=np.random.default_rng(90817)
    records=[];max_prediction=0.;max_opt_error=0.;max_saturation_ratio=0.
    start=time.perf_counter()
    for case in range(40):
        k=2+case%6;n=25+(case%8)*9
        inst=generate_instance(n,k,20261012+case,background_rate=.5+(case%4)*.5,reset_rate=.7+(case%3)*.3)
        pre=matrices(inst);U=10**rng.uniform(-.5,2.5,k);s=U.copy()
        values,r=exact_probes(inst,s,pre)
        model=build_outer_lp(values,r,U,0,0,inst.background_rate+inst.reset_rate)
        fit=solve_outer(model)
        truth=true_optimum(inst,U,pre)
        achieved=float(inst.reward@stationary(inst,fit['rates'],pre))
        opt_error=max(abs(fit['floating_upper']-truth),abs(achieved-truth));max_opt_error=max(max_opt_error,opt_error)
        z0=values[0,:k];F=(values[1:,:k]-z0).T;df=values[1:,k]-values[0,k]
        error=0.
        for _ in range(12):
            u=U*rng.random(k)
            H=F/r[None,:]
            z=np.linalg.solve(np.eye(k)-H*u[None,:],z0)
            alpha=u*z/r
            pred=values[0,k]+df@alpha
            direct=float(inst.reward@stationary(inst,u,pre))
            error=max(error,abs(pred-direct))
        max_prediction=max(max_prediction,error)
        u=10**rng.uniform(2,5,k);cap=30.
        a=float(inst.reward@stationary(inst,u,pre));b=float(inst.reward@stationary(inst,np.minimum(u,cap),pre))
        lam=inst.background_rate+inst.reset_rate
        saturation_bound=lam*(1+lam/inst.reset_rate)/cap
        max_saturation_ratio=max(max_saturation_ratio,abs(a-b)/saturation_bound)
        assert opt_error<1e-7 and error<1e-7 and abs(a-b)<=saturation_bound+1e-8
        records.append(dict(seed=20261012+case,states=n,controls=k,known_model_optimum=truth,
                            compiled_value=achieved,maximum_prediction_error=error,optimality_error=opt_error))
    return dict(cases=40,held_out_predictions=480,max_prediction_error=max_prediction,
                max_optimality_error=max_opt_error,max_saturation_error_over_bound=max_saturation_ratio,
                elapsed_seconds=time.perf_counter()-start,instances=records)


def sampled_suite():
    inst=generate_instance(160,4,714032,background_rate=1.,reset_rate=1.)
    k=inst.channels;U=np.repeat(1000000.,k);cap=600.;s=np.minimum(U,cap)
    ncal=800000;nval=400000;delta_cal=.005;delta_val=.005
    # JIT compilation excluded from acquisition timing and reported separately.
    st=time.perf_counter();inst.assay(np.zeros(k),1,0);compile_time=time.perf_counter()-st
    summaries=[];st=time.perf_counter()
    for j in range(k+1):
        u=np.zeros(k)
        if j:u[j-1]=s[j-1]
        summaries.append(inst.assay(u,ncal,200100+j))
    calibration_time=time.perf_counter()-st
    values=np.array([x.means() for x in summaries])
    r=np.array([inst.reset_rate*summaries[j+1].intervention_counts[j]/ncal for j in range(k)])
    em,er=concentration_radii(ncal,k,delta_cal,inst.background_rate,inst.reset_rate)
    model=build_outer_lp(values,r,s,em,er,inst.background_rate+inst.reset_rate)
    st=time.perf_counter();fit=solve_outer(model);lp_time=time.perf_counter()-st
    st=time.perf_counter()
    certified=exact_dual_upper(summaries,s.tolist(),em,er,inst.background_rate,inst.reset_rate,fit['dual'])
    dual_time=time.perf_counter()-st
    st=time.perf_counter();validation=inst.assay(fit['rates'],nval,300001);validation_time=time.perf_counter()-st
    ev=np.ceil(np.sqrt(np.log(2/delta_val)/(2*nval))*1e12)/1e12
    valmean=validation.reward_sum/nval;lower=max(0.,valmean-ev)
    lam=inst.background_rate+inst.reset_rate;sat=lam*(1+lam/inst.reset_rate)/cap
    upper=min(1.,certified['upper']+sat)
    pre=matrices(inst)
    st=time.perf_counter();known=true_optimum(inst,U,pre);full_lp_time=time.perf_counter()-st
    capped=true_optimum(inst,s,pre)
    actual=float(inst.reward@stationary(inst,fit['rates'],pre))
    exactvalues,exactr=exact_probes(inst,s,pre)
    confidence_event=bool(np.max(abs(values-exactvalues))<=em and np.max(abs(r-exactr))<=er)
    assert lower<=actual+1e-8 and upper+1e-8>=known and confidence_event
    duration=sum(x.physical_time for x in summaries)+validation.physical_time
    out=dict(seed=714032,hidden_states=160,controls=k,calibration_settings=k+1,
        calibration_episodes_per_setting=ncal,validation_episodes=nval,
        total_episodes=(k+1)*ncal+nval,nominal_joint_confidence=1-delta_cal-delta_val,
        original_upper_rates=U.tolist(),implemented_caps=s.tolist(),learned_rates=fit['rates'],
        observed_calibration_fluxes=r.tolist(),true_calibration_fluxes=exactr.tolist(),
        endpoint_error_radius=em,flux_error_radius=er,confidence_event_checked_against_truth=confidence_event,
        validation_mean=valmean,validation_radius=float(ev),achieved_interval_lower=lower,
        capped_optimum_upper=certified['upper'],saturation_allowance=sat,global_optimum_upper=upper,
        certified_regret_upper=upper-lower,truth_optimum=known,truth_capped_optimum=capped,
        truth_achieved=actual,truth_regret=known-actual,
        jit_compile_seconds=compile_time,calibration_runtime_seconds=calibration_time,
        inference_lp_seconds=lp_time,rational_dual_check_seconds=dual_time,
        validation_runtime_seconds=validation_time,known_full_model_lp_seconds=full_lp_time,
        total_simulated_physical_time=duration,
        background_events=sum(x.background_events for x in summaries)+validation.background_events,
        intervention_events=sum(x.intervention_events for x in summaries)+validation.intervention_events,
        inference_variables=2*k,known_model_variables=160+k,
        rational_certificate=certified,
        calibration_summaries=[asdict(x) for x in summaries],validation_summary=asdict(validation),
        implementation_scope='Synthetic CTMC assay with floating-point PRNG/event simulation; rational LP upper verified exactly. Not a hardware validation or uniformly certified sampler.')
    return out


def counterexamples():
    # Aggregating two microscopically distinct source states breaks the one-source response identity.
    # rho=1; initial law=(1/2,1/2,0); unforced exits a=0,b=3 to product state 3.
    z=lambda theta:.5/(1+theta)+.5/(4+theta)
    z0=z(0.);zs=z(1.);H=(zs-z0)/zs
    records=[]
    for u in [2.,4.,10.]:
        predicted=z0/(1-u*H);true=z(u)
        records.append(dict(rate=u,true_source_population=true,predicted_source_population=predicted,
                            error=abs(true-predicted)))
    assert records[-1]['error']>0.005
    return dict(pooled_source_failure=records,
                explanation='A knob acting on both hidden source states is rank two, not the single-source actuator assumed by the theorem.')

if __name__=='__main__':
    results=dict(environment=dict(python=platform.python_version(),numpy=np.__version__),
                 exact_tests=exact_suite(),sampled_benchmark=sampled_suite(),counterexamples=counterexamples())
    (ROOT/'results.json').write_text(json.dumps(results,indent=2))
    brief={k:v for k,v in results['sampled_benchmark'].items() if k not in ['calibration_summaries','validation_summary','rational_certificate']}
    print(json.dumps(dict(exact_summary={k:v for k,v in results['exact_tests'].items() if k!='instances'},sampled_summary=brief,counterexamples=results['counterexamples']),indent=2))
