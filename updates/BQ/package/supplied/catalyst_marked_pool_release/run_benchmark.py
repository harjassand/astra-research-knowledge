"""Matched exact FSP vs marked-pool endpoint-likelihood timing."""
import json, os, platform, sys, time
from statistics import median

import numpy as np
import scipy
from scipy.linalg import expm

from marked_pool import MarkedPoolLikelihood, full_cme_endpoint


def cycle_generator(q):
    Q = np.zeros((q, q))
    for i in range(q):
        Q[i, (i + 1) % q] += 0.4
        Q[i, (i - 1) % q] += 0.2
        Q[i, i] -= 0.6
    return Q


def timed(fn, repeats=1):
    vals=[]; out=None
    for _ in range(repeats):
        t=time.perf_counter(); out=fn(); vals.append(time.perf_counter()-t)
    return median(vals), out


def main():
    q, T, lam, koff, kcat, K = 4, 0.8, 2.0, 0.8, 1.2, 10
    Q = cycle_generator(q)
    mu0 = np.zeros(q); mu0[0] = 1.0
    pT = mu0 @ expm(Q*T)
    rows=[]
    for N in [10, 20, 40, 60, 100]:
        obs = tuple(map(int, np.floor(N*pT)))
        obs = (obs[0] + N - sum(obs),) + obs[1:]
        model = MarkedPoolLikelihood(N,Q,0,1,lam,koff,kcat,mu0)
        marked_time, marked = timed(lambda: model.solve(T,K,obs,observed_bound=0,
                                                          rtol=1e-9,atol=1e-12))
        fsp_fwd_time, (exact, fsp_dim, mass) = timed(lambda: full_cme_endpoint(
            N,Q,0,1,lam,koff,kcat,mu0,T,obs,0,direction="forward"))
        fsp_adj_time, (adj_exact, adj_dim, _) = timed(lambda: full_cme_endpoint(
            N,Q,0,1,lam,koff,kcat,mu0,T,obs,0,direction="adjoint"))
        fsp_time = min(fsp_fwd_time, fsp_adj_time)
        rows.append({
            "N":N, "q":q, "K":K, "lambda_T":lam*T, "observation":obs,
            "marked_dimension":marked.dimension, "fsp_dimension":fsp_dim,
            "marked_seconds":marked_time,
            "fsp_forward_seconds":fsp_fwd_time, "fsp_adjoint_seconds":fsp_adj_time,
            "fsp_best_endpoint_query_seconds":fsp_time,
            "speedup_fsp_over_marked":fsp_time/marked_time,
            "likelihood_lower":marked.lower,
            "poisson_tail":marked.poisson_tail,
            "likelihood_upper":marked.lower+marked.poisson_tail,
            "fsp_exact_likelihood":exact,
            "fsp_adjoint_likelihood":adj_exact,
            "abs_error_from_lower":abs(exact-marked.lower),
            "bound_holds_up_to_2e-8_numeric_slack":bool(
                marked.lower-2e-8 <= exact <= marked.lower+marked.poisson_tail+2e-8),
            "marked_mass":marked.mass,
            "fsp_mass":mass,
        })
    payload={
        "description":"One terminal full-count snapshot; known iid/monodisperse initial pool; one catalyst; four free molecular states; all approaches solve the same exact model.",
        "parameters":{"q":q,"T":T,"lambda":lam,"koff":koff,"kcat":kcat,"K":K,
                      "Q":Q.tolist(),"mu0":mu0.tolist(),"bind_state":0,"product_state":1},
        "environment":{"python":sys.version,"numpy":np.__version__,"scipy":scipy.__version__,
                        "platform":platform.platform(),"processor":platform.processor(),
                        "cpu_count":os.cpu_count()},
        "timing_method":"single run per case, process-local wall time from perf_counter; includes state construction and solve. FSP forward computes the full distribution; FSP adjoint propagates only the endpoint indicator, which is the stronger fair baseline for one queried observation. Reported speedup uses the faster FSP direction.",
        "results":rows,
    }
    with open("benchmark_results.json","w") as f: json.dump(payload,f,indent=2)
    print(json.dumps(payload,indent=2))

if __name__ == "__main__": main()
