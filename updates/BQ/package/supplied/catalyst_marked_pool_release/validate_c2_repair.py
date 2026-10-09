"""Nonvacuous multi-catalyst regression and independent FSP comparison."""
import json, os
import numpy as np
from scipy.linalg import expm
from scipy.stats import poisson
from marked_pool import (MarkedPoolLikelihood, full_cme_endpoint,
                         candidate_event_edges, build_between_event_generator)


def cycle_generator(q):
    Q=np.zeros((q,q))
    for i in range(q):
        Q[i,(i+1)%q]+=.4; Q[i,(i-1)%q]+=.2; Q[i,i]-=.6
    return Q


def main():
    q,N,C=3,16,2
    Q=cycle_generator(q); mu0=np.array([1.,0.,0.])
    T,lam,koff,kcat,K=.6,1.1,.7,.9,12
    model=MarkedPoolLikelihood(N,Q,0,1,lam,koff,kcat,mu0,catalysts=C)
    obs=(10,3,1); bobs=2
    result=model.solve(T,K,obs,observed_bound=bobs,rtol=2e-11,atol=2e-14)
    exact, fsp_dim, fsp_mass=full_cme_endpoint(N,Q,0,1,lam,koff,kcat,mu0,T,
                                               obs,bobs,catalysts=C)
    assert sum(obs)+bobs==N and exact>0
    assert result.lower-2e-10 <= exact <= result.lower+result.poisson_tail+2e-10
    assert abs(result.mass-poisson.cdf(K,C*lam*T))<2e-9

    # Structural state: two complexes bound while one marked free molecule in
    # state 1 jumps to state 0, with b unchanged.
    states,ix=model._make_states(4)
    R=build_between_event_generator(states,ix,Q,0,1,koff,kcat)
    src=(3,2,(0,1,0)); dst=(3,2,(1,0,0)); wrong=(3,1,(1,0,0))
    q_rate=float(R[ix[src],ix[dst]])
    wrong_rate=float(R[ix[src],ix[wrong]])
    assert abs(q_rate-Q[1,0])<1e-14 and abs(wrong_rate)<1e-14
    p=mu0@expm(Q*.4)
    edges=candidate_event_edges(src,N,3,0)
    candidate_mass=sum(weight*(1.0 if coef<0 else p[coef])
                       for _,coef,weight in edges)
    assert abs(candidate_mass-1.0)<1e-14

    # The earlier test vector had b=0 and only 14 free molecules for N=16,
    # hence it was an impossible observation and both methods returned zero.
    old_obs=(9,5,0)
    old_exact,_,_=full_cme_endpoint(N,Q,0,1,lam,koff,kcat,mu0,T,old_obs,
                                     observed_bound=0,catalysts=C)
    old_marked=model.solve(T,K,old_obs,observed_bound=0,rtol=2e-11,atol=2e-14)
    assert sum(old_obs)!=N and old_exact==0.0 and old_marked.lower==0.0

    record={
      "status":"corrected C=2 validation passed",
      "model":{"N":N,"q":q,"catalysts":C,"T":T,"lambda_per_catalyst":lam,"koff":koff,"kcat":kcat,"K":K,"Q":Q.tolist(),"mu0":mu0.tolist()},
      "valid_joint_observation":{"free_counts":obs,"bound_count":bobs,"sum_free_plus_bound":sum(obs)+bobs,"marked_lower":result.lower,"marked_tail":result.poisson_tail,"marked_upper":result.lower+result.poisson_tail,"fsp_exact_query":exact,"absolute_lower_minus_fsp":result.lower-exact,"marked_states":result.dimension,"fsp_states":fsp_dim,"marked_retained_mass":result.mass,"independent_fsp_total_mass":fsp_mass,"poisson_cdf_K":float(poisson.cdf(K,C*lam*T))},
      "structural_regression":{"state_b2_with_one_free_mark":src,"q_transition_destination":dst,"rate_expected":float(Q[1,0]),"rate_actual":q_rate,"incorrect_b1_destination_rate":wrong_rate,"candidate_edge_mass_at_test_time":candidate_mass},
      "superseded_vacuous_c2_test":{"observation":old_obs,"bound_count":0,"N":N,"sum_free_counts":sum(old_obs),"exact_likelihood":old_exact,"marked_lower":old_marked.lower,"reason":"sum_free_counts + bound_count = 14 < N=16; both zero outputs did not validate the solver"},
      "numerical_note":"Poisson truncation interval is analytic for exact ODE solution; floating ODE/expm errors are not rigorously enclosed."
    }
    path=os.path.join(os.path.dirname(__file__),"c2_repair_validation.json")
    with open(path,"w") as f: json.dump(record,f,indent=2)
    print(json.dumps(record,indent=2))

if __name__=='__main__': main()
