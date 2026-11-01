"""Discriminating stage-one tests: native path data versus intervention design.

This is our small exact model, not a reproduction of a molecular application.
It compares observational identifiability, best possible ordinary importance
sampling of an event, and a known-source Gaussian path-factor calculation.
"""
from pathlib import Path
import json, math, importlib.util, hashlib
import numpy as np
from scipy.linalg import expm
from scipy.stats import binom

HERE=Path(__file__).resolve().parent


def generator(u, swap=False):
    # A, H1, H2, B, C. H1/H2 are hidden from the declared observation.
    # Control changes an A-H barrier: BOTH directions get the same multiplier.
    # Thus A-H detailed-balance ratios stay fixed. B/C are stopped endpoints;
    # adding positive reverse exits outside the stopped experiment is allowed.
    z=np.zeros((5,5)); ep,em=np.exp(u),np.exp(-u)
    z[0,1],z[1,0]=.5*ep,ep
    z[0,2],z[2,0]=.5*em,em
    z[1,4 if swap else 3]=1.
    z[2,3 if swap else 4]=1.
    z[np.diag_indices(5)]=-z.sum(axis=1)
    return z


def outcome(u,swap=False):
    q=generator(u,swap); transient=q[:3,:3]
    p=np.linalg.solve(-transient,q[:3,3])
    mfpt=np.linalg.solve(-transient,np.ones(3))
    return float(p[0]),float(mfpt[0])


def indistinguishability():
    lump=np.array([[1,0,0,0],[0,1,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    alpha=np.array([1,0,0,0,0.])
    err=0.
    for t in np.linspace(0,20,101):
        a=alpha@expm(t*generator(0,False))@lump
        b=alpha@expm(t*generator(0,True))@lump
        err=max(err,float(np.max(abs(a-b))))
    # Equality of the entire observed path law is stronger than this marginal
    # check: the hidden-state permutation maps one chain into the other and
    # leaves the observation map and initial law unchanged.
    u=math.log(9)
    p1,t1=outcome(u,False);p2,t2=outcome(u,True)
    assert err<1e-13
    assert abs(p1-.9)<1e-12 and abs(p2-.1)<1e-12
    assert abs(t1-3)<1e-12 and abs(t2-3)<1e-12
    nprobe=40
    # A tie is split randomly, since nprobe is even.
    wrong=float(binom.cdf(nprobe//2-1,nprobe,p1)+.5*binom.pmf(nprobe//2,nprobe,p1))
    return dict(native_observed_marginal_residual=err,
        full_path_equality_reason='hidden-state permutation preserves observation and initial law',
        control_u_in_log_rate_units=u,
        model_one_product_B_probability=p1,
        model_two_product_B_probability=p2,
        mean_first_passage_times=[t1,t2],
        native_product_B_probability=outcome(0)[0],
        native_mean_first_passage_time=outcome(0)[1],
        controlled_probe_trials=nprobe,
        exact_model_identification_error_from_probe=wrong,
        resource_scope='Real actuator coupling is specified by generator; its material realization and work are not acquired. Count entire probe runs, including repeat visits, clock time and observation.')


def overlap():
    # The coarsest EVENT likelihood is the Rao-Blackwell lower-variance limit
    # of any ordinary path-likelihood event estimator on iid native samples.
    p,q=1e-5,.9; relative_se=.1
    native_required=(1-p)/(p*relative_se**2)
    direct_required=(1-q)/(q*relative_se**2)
    n=100000
    rng=np.random.default_rng(62025)
    counts=rng.binomial(n,p,size=20000)
    estimates=q*counts/(n*p)
    # Stronger common competitor: self-normalized importance sampling.
    # It trades bias for variance and cannot represent an unobserved event.
    snis=(q*counts/p)/(q*counts/p+(1-q)*(n-counts)/(1-p))
    kl=q*math.log(q/p)+(1-q)*math.log((1-q)/(1-p))
    return dict(native_event_probability=p,target_event_probability=q,
        best_event_reweighting_samples_for_10pct_relative_SE=native_required,
        direct_target_samples_for_10pct_relative_SE=direct_required,
        integer_direct_target_samples=math.ceil(direct_required),
        native_runs_per_replicate=n,
        probability_no_target_observation=(1-p)**n,
        exact_reweighted_estimator_sd=q*math.sqrt((1-p)/(n*p)),
        monte_carlo_estimator_sd=float(np.std(estimates,ddof=1)),
        monte_carlo_estimator_mean=float(np.mean(estimates)),
        self_normalized_mean=float(snis.mean()),
        self_normalized_sd=float(snis.std(ddof=1)),
        self_normalized_asymptotic_samples_for_10pct_relative_SE=(1-q)**2/(p*(1-p)*relative_se**2),
        samples_for_95pct_chance_of_at_least_one_event=math.ceil(math.log(.05)/math.log1p(-p)),
        binary_path_KL_lower_bound_nats=kl,
        scope='The variance bound is for fixed iid native paths and ordinary UNBIASED likelihood weighting. Self-normalization is included separately and can reduce variance with bias; its asymptotic SE is misleading when only order-one events are expected. Zero-event probability applies to either weighted empirical event measure. No bound on adaptive splitting, multilevel bridges, targeted simulation or separately acquired analytic knowledge. Relative entropy is not automatically dissipated mechanical work.')


def finite_control_projection():
    # Bernoulli event and two physical perturbations: common acceleration and
    # opposite barrier change. Common acceleration alters event times but has
    # zero first-order effect on eventual product probability.
    h=1e-5
    rows=[]
    for u in [-math.log(9),0.,math.log(9)]:
        p,t=outcome(u)
        dp=(outcome(u+h)[0]-outcome(u-h)[0])/(2*h)
        exact=p*(1-p)
        assert abs(dp-exact)<1e-8
        rows.append(dict(u=u,p_B=p,mfpt=t,dp_du=dp,logistic_derivative=exact))
    return rows


def native_score_experiment():
    # Full simulator records, including hidden H identity and dwell times.
    # These are exactly the extra records the coarse observation lacks.
    n=100000;rng=np.random.default_rng(51204)
    states=np.zeros(n,dtype=np.int8);scores=np.zeros(n);clock=np.zeros(n)
    while True:
        live=np.flatnonzero(states<3)
        if not len(live):break
        s=states[live];rates=np.where(s==0,1.,2.)
        dt=rng.exponential(1/rates);clock[live]+=dt
        compensator=np.where(s==1,1.,np.where(s==2,-1.,0.))
        scores[live]-=compensator*dt
        choose=rng.random(len(live))<.5
        nxt=np.where(s==0,np.where(choose,1,2),
                     np.where(choose,0,np.where(s==1,3,4)))
        increment=np.where(s==0,np.where(choose,1.,-1.),
                           np.where(choose,np.where(s==1,1.,-1.),0.))
        scores[live]+=increment;states[live]=nxt
    y=(states==3).astype(float)
    fisher=float(np.mean(scores*scores));gradient=float(np.mean(y*scores))
    assert abs(fisher-3)<.08 and abs(gradient-.25)<.02
    assert abs(scores.mean())<.02
    return dict(native_paths=n,empirical_p_B=float(y.mean()),
        mean_time=float(clock.mean()),score_mean=float(scores.mean()),
        estimated_response_gradient=gradient,exact_response_gradient=.25,
        estimated_path_Fisher_information=fisher,exact_path_Fisher_information=3.,
        fraction_of_event_variance_in_accessible_score_span=1/12,
        acquired_records=['hidden-state identity','reaction-channel identity','dwell time','known control coupling/rates'],
        scope='Ordinary likelihood-ratio sensitivity estimator, not a new algorithm. It quantifies the missing records and actuator dependence.')


def upstream_factor_check():
    # Optional exact upstream-source execution. Source intentionally kept in
    # scratch because the repository did not expose a distribution license.
    source=Path('producer-workspace/stage1_girsanov_factor.py')
    if not source.exists():
        return dict(executed=False,reason='Fetch exact source specified in SOURCES.txt to scratch; our other tests are fully standalone.')
    data=source.read_bytes()
    sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert sha=='8aad363177aed05803a775920a7c24bc5308b274'
    spec=importlib.util.spec_from_file_location('upstream_girsanov',source)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    rng=np.random.default_rng(48293);eta=rng.normal(size=(40000,50));results=[]
    for force in [.25,.75,1.5]:
        delta,logM=mod.M_ABOBA(force,eta,.01,1.,1.,1.,1.)
        logw=-logM.sum(axis=1);weight=np.exp(logw)
        # Exact Gaussian density-ratio identity for deterministic force shifts.
        assert abs(float(weight.mean())-1)<.025
        q_observable=eta.sum(axis=1)/math.sqrt(eta.shape[1])
        target_mean=-float(delta)*math.sqrt(eta.shape[1])
        measured=float(np.mean(weight*q_observable))
        assert abs(measured-target_mean)<.04
        results.append(dict(force=force,delta_eta=float(delta),
            mean_weight=float(weight.mean()),analytic_mean_weight=1.,
            reweighted_noise_sum=measured,analytic_noise_sum=target_mean,
            second_moment_exact=math.exp(eta.shape[1]*float(delta)**2)))
    return dict(executed=True,source_blob_sha1=sha,
        samples=40000,steps=50,results=results,
        scope='Exact fetched M_ABOBA helper, deterministic force difference, known Gaussian innovations, common initial state. Not a molecular MD reproduction or experimentally observed path likelihood.')


if __name__=='__main__':
    results=dict(indistinguishability=indistinguishability(),
                 overlap=overlap(),control_projection=finite_control_projection(),
                 native_score=native_score_experiment(),
                 upstream=upstream_factor_check())
    (HERE/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
