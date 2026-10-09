"""Product-only endpoint inference: marked solver vs query-specific exact FSP."""
from __future__ import annotations
import json, os, platform, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.integrate import quad
from scipy.linalg import expm
from scipy.stats import poisson
from marked_pool_partial import MarkedPoolLikelihood, full_cme_endpoint


def model():
    # States A, B, C, P. P has no incoming/outgoing Q edges and starts empty,
    # so only catalytic release can create observed product.
    q=4
    Q=np.zeros((q,q))
    Q[0,1]=0.70; Q[0,0]=-0.70
    Q[1,0]=0.15; Q[1,2]=0.40; Q[1,1]=-0.55
    Q[2,1]=0.25; Q[2,2]=-0.25
    mu0=np.array([1.,0.,0.,0.])
    return Q,mu0


def meanfield_product_prob(Q,mu0,T,lam,koff,kcat,kobs=1):
    """Unperturbed-reservoir baseline: fresh Bernoulli target at each attempt.

    Solve enzyme/product CTMC with time-dependent bind rate lambda*p_A(t).
    This is asymptotically correct as N->infinity at fixed observation time,
    but ignores finite-N reuse/depletion correlations.
    """
    q=len(mu0); pA=lambda t: float((mu0@expm(Q*t))[0])
    states=[(r,b) for r in range(kobs+1) for b in (0,1)]
    ix={s:i for i,s in enumerate(states)}
    y0=np.zeros(len(states)); y0[ix[(0,0)]]=1
    def rhs(t,y):
        dy=np.zeros_like(y); h=lam*pA(t)
        for r,b in states:
            x=y[ix[(r,b)]]
            if b==0:
                dy[ix[(r,0)]]-=h*x
                dy[ix[(r,1)]]+=h*x
            else:
                dy[ix[(r,1)]]-=(koff+kcat)*x
                dy[ix[(r,0)]]+=koff*x
                if r<kobs: dy[ix[(r+1,0)]]+=kcat*x
        return dy
    sol=solve_ivp(rhs,(0,T),y0,method='DOP853',rtol=1e-12,atol=1e-14)
    return sum(sol.y[ix[(kobs,b)],-1] for b in (0,1))


def one_clock_path_lower(Q,mu0,T,lam,koff,kcat,bind=0):
    """Likelihood lower bound from exactly one candidate, binding then catalysis.

    If the sole candidate event occurs at t, its selected free molecule is in
    the bind state with marginal probability p_bind(t). The bound complex then
    catalyzes before T with the two-channel exponential race probability.
    This path is a subset of the terminal event P(T)=1.
    """
    rate=koff+kcat
    def integrand(t):
        p=float((mu0@expm(Q*t))[bind])
        cat_before_T=(kcat/rate)*(1-np.exp(-rate*(T-t))) if rate>0 else 0.0
        return np.exp(-lam*T)*lam*p*cat_before_T
    return float(quad(integrand,0,T,epsabs=1e-14,epsrel=1e-13)[0])


def certified_K(mean_candidates, path_lower, relative_eps):
    for k in range(10000):
        tail=float(poisson.sf(k,mean_candidates))
        if tail <= relative_eps*path_lower:
            return k,tail
    raise RuntimeError("could not select a finite K")


def main():
    Q,mu0=model(); T=1.0; lam=2.2; koff=.55; kcat=1.3; kobs=1
    target_eps=1e-5
    path_lower=one_clock_path_lower(Q,mu0,T,lam,koff,kcat)
    K, selected_tail=certified_K(lam*T,path_lower,target_eps)
    output={"scope":"Terminal product-count observation only; product state has no Q transitions to/from other states, starts empty, and is produced only by catalytic release. States with product count above the observed count are pruned exactly. Exact marker truncation tail is separate from numerical ODE error.",
            "parameters":{"T":T,"lambda":lam,"koff":koff,"kcat":kcat,"Q":Q.tolist(),"mu0":mu0.tolist(),"bind_state":0,"product_state":3,"observation":{"3":kobs},"catalyst_count":1},
            "relative_error_selection":{"requested_relative_truncation_bound":target_eps,"constructive_one_candidate_path_likelihood_lower_bound":path_lower,"K_chosen_before_solver":K,"poisson_tail_at_K":selected_tail,"tail_over_constructive_lower":selected_tail/path_lower},
            "environment":{"python":platform.python_version(),"numpy":np.__version__,"platform":platform.platform()},
            "cases":[]}
    for N in (20,100,300):
        engine=MarkedPoolLikelihood(N,Q,0,3,lam,koff,kcat,mu0)
        tm=time.perf_counter(); mark=engine.solve(T,K,{3:kobs},observed_bound=None,rtol=2e-10,atol=1e-13); mark_s=time.perf_counter()-tm
        # Query-specific reduced FSP: keep exact counts of all free states but
        # prune product counts > kobs, since P is irreversible.
        tf=time.perf_counter(); fsp,dim,mass=full_cme_endpoint(N,Q,0,3,lam,koff,kcat,mu0,T,{3:kobs},direction='forward',monotone_cap=(3,kobs)); fsp_s=time.perf_counter()-tf
        mf=meanfield_product_prob(Q,mu0,T,lam,koff,kcat,kobs)
        case={"N":N,"marked_seconds":mark_s,"marked_states":mark.dimension,"K":K,"marked_lower":mark.lower,"poisson_tail":mark.poisson_tail,"tail_over_lower":mark.poisson_tail/mark.lower,"marked_mass":mark.mass,"query_specific_fsp_seconds":fsp_s,"query_specific_fsp_states":dim,"query_specific_fsp_mass_after_kill":mass,"query_specific_fsp_likelihood":fsp,"meanfield_unperturbed_reservoir_likelihood":mf,"meanfield_relative_error_vs_fsp":abs(mf-fsp)/fsp,"marked_minus_fsp":mark.lower-fsp,"marked_interval_covers_fsp":(mark.lower-5e-9 <= fsp <= mark.lower+mark.poisson_tail+5e-9)}
        output["cases"].append(case)
        print(json.dumps(case))
    # Parameter sensitivity in the catalyst-informative partial observation.
    sens=[]
    N=300
    for l in (0.8,1.4,2.2,3.0):
        engine=MarkedPoolLikelihood(N,Q,0,3,l,koff,kcat,mu0)
        m=engine.solve(T,18,{3:kobs},rtol=3e-10,atol=2e-13)
        fsp,dim,_=full_cme_endpoint(N,Q,0,3,l,koff,kcat,mu0,T,{3:kobs},direction='forward',monotone_cap=(3,kobs))
        mf=meanfield_product_prob(Q,mu0,T,l,koff,kcat,kobs)
        sens.append({"lambda":l,"marked_lower_K18":m.lower,"tail":m.poisson_tail,"tail_over_lower":m.poisson_tail/m.lower,"fsp":fsp,"meanfield":mf,"mf_relerr":abs(mf-fsp)/fsp,"states_fsp":dim})
    output["lambda_sensitivity_N300"]=sens
    # For physical catalyst-free model, P=1 is impossible exactly.
    output["catalyst_free_likelihood_for_product_one"]=0.0
    output["observed_event_is_informative"]="likelihood of one product is positive under catalysis and identically zero when lambda=0; lambda dependence also reported above"
    outpath=os.path.join(os.path.dirname(__file__),"product_count_results.json")
    with open(outpath,"w") as f: json.dump(output,f,indent=2)
    print(json.dumps(output,indent=2))

if __name__=='__main__': main()
