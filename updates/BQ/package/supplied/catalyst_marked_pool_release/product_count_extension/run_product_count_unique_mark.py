"""Matched product-count comparison for event-count vs distinct-mark solvers."""
import json, os, platform
from pathlib import Path
from time import perf_counter
import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm
from scipy.stats import poisson
from marked_pool_partial import MarkedPoolLikelihood, full_cme_endpoint
from unique_mark_engine import UniqueMarkLikelihood
from run_product_count import model, meanfield_product_prob, one_clock_path_lower, certified_K


def main():
    Q,mu0=model(); T=1.; lam=2.2; koff=.55; kcat=1.3; kobs=1; eps=1e-5
    path_lower=one_clock_path_lower(Q,mu0,T,lam,koff,kcat)
    K,tail_selected=certified_K(lam*T,path_lower,eps)
    prior_path=os.path.join(os.path.dirname(__file__),"product_count_results.json")
    prior=json.load(open(prior_path))
    prior_cases={x["N"]:x for x in prior["cases"]}
    out={"scope":"Same terminal product-only model as product_count_results.json, now using a permanent distinct-tag cap instead of a candidate-event-count layer. Product P has literal structural-zero Q row/column and mu0[P]=0, so product-count cap is exact. The Poisson tail is an analytic truncation error for exact ODE solution only; ODE/linear algebra error is separate and uncertified.",
         "parameters":prior["parameters"],
         "relative_error_selection":{"requested_relative_truncation_bound_only":eps,"constructive_one_candidate_path_likelihood_lower_bound":path_lower,"K_chosen_before_solver":K,"poisson_tail":tail_selected,"tail_over_path_lower":tail_selected/path_lower},
         "environment":{"python":platform.python_version(),"numpy":np.__version__,"platform":platform.platform()},
         "cases":[]}
    for N in (20,100,300):
        unique=UniqueMarkLikelihood(N,Q,0,3,lam,koff,kcat,mu0)
        u=unique.solve(T,K,{3:kobs},rtol=2e-10,atol=1e-13)
        tf=perf_counter()
        fsp,fdim,fmass=full_cme_endpoint(N,Q,0,3,lam,koff,kcat,mu0,T,{3:kobs},
                                          direction='forward',monotone_cap=(3,kobs))
        fsp_seconds=perf_counter()-tf
        mf=meanfield_product_prob(Q,mu0,T,lam,koff,kcat,kobs)
        ev=prior_cases[N]
        row={"N":N,"distinct_mark_K":K,"distinct_mark_states":u.dimension,"distinct_mark_seconds":u.seconds,"distinct_mark_lower":u.lower,"distinct_mark_tail":u.poisson_tail,"distinct_mark_tail_over_lower":u.poisson_tail/u.lower,"distinct_mark_retained_mass_after_product_and_tag_pruning":u.retained_mass,"query_specific_exact_FSP_states":fdim,"query_specific_exact_FSP_seconds":fsp_seconds,"query_specific_exact_FSP_likelihood":fsp,"FSP_mass_after_product_cap":fmass,"distinct_mark_minus_FSP":u.lower-fsp,"distinct_mark_interval_covers_FSP":u.lower-5e-10<=fsp<=u.lower+u.poisson_tail+5e-10,"event_count_layer_states":ev["marked_states"],"event_count_layer_seconds":ev["marked_seconds"],"event_count_layer_likelihood_lower":ev["marked_lower"],"meanfield_fresh_draw_likelihood":mf,"meanfield_relative_error_vs_exact_FSP":abs(mf-fsp)/fsp}
        out["cases"].append(row)
        print(json.dumps(row))
    out["parameter_sensitivity_N300"]=prior["lambda_sensitivity_N300"]
    out["catalyst_free_probability_Pequals1"]=0.0
    out["interpretation"]="At N=300 the exact marked methods exploit finite candidate/unique-tag effects; the unperturbed-reservoir approximation is 2.77e-4 relative off, so it does not meet 1e-5. The query-specific FSP is the strongest executed generic exact baseline; balanced-realisation reduced CME is a relevant published approximation but has a different output/error metric and was not implemented here."
    path=os.path.join(os.path.dirname(__file__),"product_count_unique_mark_results.json")
    with open(path,'w') as f: json.dump(out,f,indent=2)
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
