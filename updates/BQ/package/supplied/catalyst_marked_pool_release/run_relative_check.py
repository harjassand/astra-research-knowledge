"""One-solve adaptive-K demonstration for relative tail/lower criteria."""
import json
import numpy as np
from scipy.linalg import expm
from marked_pool import MarkedPoolLikelihood


def main():
    q, N, T, lam, Kmax = 4, 100, 0.8, 2.0, 14
    Q = np.zeros((q, q))
    for i in range(q):
        Q[i, (i + 1) % q] += 0.4
        Q[i, (i - 1) % q] += 0.2
        Q[i, i] -= 0.6
    mu0 = np.array([1.0, 0.0, 0.0, 0.0])
    pT = mu0 @ expm(Q*T)
    obs = tuple(map(int, np.floor(N*pT)))
    obs = (obs[0] + N-sum(obs),) + obs[1:]
    engine = MarkedPoolLikelihood(N, Q, 0, 1, lam, 0.8, 1.2, mu0)
    result = engine.solve(T, Kmax, obs, observed_bound=0,
                          rtol=2e-10, atol=2e-13)
    tolerances = [1e-3, 1e-4, 1e-5, 1e-6]
    cuts = [result.relative_cutoff(eps, lam*T) for eps in tolerances]
    payload = {
        "scope":"single terminal full count vector; Poisson truncation only; ODE numerical error is separate",
        "parameters":{"N":N,"q":q,"T":T,"lambda_per_catalyst":lam,
                      "Kmax":Kmax,"observation":obs,"observed_bound":0},
        "dimension_at_Kmax":result.dimension,
        "Kmax_lower":result.lower,
        "Kmax_tail":result.poisson_tail,
        "Kmax_mass":result.mass,
        "relative_cutoffs":[{"requested_relative_tail_over_lower":eps, **cut}
                             for eps,cut in zip(tolerances,cuts)],
    }
    with open("relative_tolerance_check.json","w") as f:
        json.dump(payload,f,indent=2)
    print(json.dumps(payload,indent=2))


if __name__ == "__main__": main()
