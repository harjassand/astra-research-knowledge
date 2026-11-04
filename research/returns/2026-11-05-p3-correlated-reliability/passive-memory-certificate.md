# A passive hidden-memory residual certificate for nonlinear trajectories

This independent [complete deterministic theorem](package/independent_routes/next3_first_principles/02_PASSIVE_MEMORY_PROOF.md) retains the favorable sign of derivative memory instead of replacing it by an absolute perturbation norm. Its physical acquisition-and-execution endpoint is **unresolved**; an ideal instantaneous clamp is not a finite-slew experiment. It is separate from the [selected correlated reliability construction](README.md).

Let V be mu-strongly convex and the true hidden-memory kernel be a positive mixture `K(t)=sum_i w_i exp(-lambda_i t)`, `w_i>=0`, `lambda_i>=0`, finite total weight. Eliminating a passive bath gives `x_dot+grad V(x)+K*x_dot=f`, with separately accounted initial hidden-force terms. No positive lower bound on bath rates is required; zero-rate modes are allowed.

For two H1 trajectories starting at the same observed coordinate, let rho collect forcing, initial-force and numerical residual mismatches. Set

```text
R=||K-Khat||_L1(0,T) ||xhat_dot||_L2(0,T)+||rho||_L2(0,T).
```

Then `||x-xhat||_L2<=R/mu` and endpoint error is at most `R/sqrt(2mu)`. The positive-mixture identity makes the integrated derivative-memory term nonnegative. Positive rank-one matrix kernels have the same argument. There is no exponential-in-horizon multiplier, damping-dominance assumption or bath gap, but **R itself can grow with horizon and drive**. This is not uniform perpetual prediction or a white-noise path theorem.

Initial hidden mismatch requires its own energy/force allowance. Slow modes can prevent a guard interval from making it small; a microscopic energy bound may grow with hidden volume. If true and fitted kernels are positive mixtures and finite mesh nodes have sound error eta with spacing h and initial heights at most B, the supplied monotonicity argument gives `||K-Khat||_1<=2hB+T eta`. These nodal bands can feed the residual certificate without identifying microscopic rates.

Fresh random-sign ideal clamps cancel retained latent offsets in conditional expectation, but the source explicitly does not complete finite-slew hardware, unknown gain calibration, general thermal simulation, or finite-precision fitting/execution. The sign/no-reset mechanism also has earlier Astra predecessors and is not claimed as a new primitive. Generalized Langevin kernel error/learning and positive extended-state realizations are credited primary comparators. No new Capital audit, simulation, experimental predictor or historical-priority finding is supplied. [Original package and status](SOURCES.json).
