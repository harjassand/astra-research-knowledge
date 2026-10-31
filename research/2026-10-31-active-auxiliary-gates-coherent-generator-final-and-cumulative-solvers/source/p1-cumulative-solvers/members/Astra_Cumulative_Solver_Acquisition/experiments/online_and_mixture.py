"""Targeted online confidence/cost check and exact primitive-mixture failure."""
from pathlib import Path
import json
import numpy as np
from compare_solvers import Source, Retained, acquire, pcg, true_error


def main():
    n=12;m=3;r=3
    u=np.eye(n)[:,:r]
    hs=[]
    for j in range(m):
        h=np.zeros((r,r));h[j,j]=16.
        hs.append(h)
    tails=np.zeros(m)
    source=Source(u,hs,tails)
    lib=Retained(source)
    rng=np.random.default_rng(1901)
    jobs=[]
    for t in range(75):
        # Later novel tasks occur AFTER more accepted tasks than ambient n.
        theta=np.array([1.,0.,0.]) if t<25 else np.array([.5,1.,0.]) if t<50 else np.ones(3)
        b=rng.normal(size=n)
        before_stages=len(lib.stages);before_dim=lib.q.shape[1]
        acquire(lib,theta,1.,.01,rng,"cumulative_witness")
        x,it=pcg(source,lib,theta,1.,b,1e-7)
        err=true_error(u,hs,tails,theta,1.,b,x)
        assert err<=1e-7
        jobs.append({"task":t+1,"new_stages":len(lib.stages)-before_stages,
                     "added_directions":lib.q.shape[1]-before_dim,
                     "retained_dimension":lib.q.shape[1],"iterations":it,
                     "actual_relative_energy_error":err})
    assert lib.q.shape[1]==3
    assert len(lib.stages)==3+3
    assert lib.reused_certificates==72
    assert [x["task"] for x in jobs if x["added_directions"]]==[1,26,51]
    delta_sum=sum(x["delta_stage"] for x in lib.stages)
    assert delta_sum<.01
    # Exact rational mixture counterexample is expressible with small integers:
    # S=span(1,1), A=diag(1,0), B=diag(0,1).
    # N_S(A)=A,N_S(B)=B, while 2 E_S(A+B)=[[1,-1],[-1,1]].
    twice_mixture=np.array([[1,-1],[-1,1]],dtype=int)
    assert np.array_equal(twice_mixture@np.array([1,1]),[0,0])
    assert np.array_equal(twice_mixture@np.array([1,-1]),[2,-2])
    out={"kind":"binary64 online control-flow diagnostic plus exact integer mixture identities",
         "n":n,"m":m,"tasks":75,"accepted_tests":3,"rejected_tests":3,
         "reused_certificates":lib.reused_certificates,
         "final_dimension":3,"total_stages":len(lib.stages),"confidence_budget_sum":delta_sum,
         "primitive_counts":source.counts,"jobs":jobs,"stages":lib.stages,
         "hindsight_envelope":{"spectrum_nonzero":[16,16,16],"rank":3,
                              "log2det_I_plus_4C":float(3*np.log2(65.))},
         "primitive_mixture_counterexample":{"primitive_residuals_zero":True,"mixture_residual_eigenvalues":[0,1]},
         "limitations":["Tasks are scheduled, not an adversarial-universal empirical test; theorem permits adaptive tasks", "No numerical interval proof", "Actual transition of task domain and all repeated certification costs retained"]}
    dest=Path(__file__).resolve().parents[1]/"results"/"online_and_mixture.json"
    dest.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"tasks":75,"stages":len(lib.stages),"dimension":3,
                      "novelty_tasks":[x["task"] for x in jobs if x["added_directions"]],
                      "primitive_counts":source.counts},indent=2))


if __name__=="__main__":
    main()
