# A whole-model discriminator against ordinary Gaussian rejection

This controls ONE serious exact comparator, not every conventional algorithm.
The faster small-cell Gaussian rejection execution is preserved in EXECUTION.json.

Let k=n-1 be the pinned field dimension. Write the unweighted Laplacian as
L_0=B B^T and P=B^T L_0^(-1)B. Then P is a projection of rank k, and its diagonal
leverage scores tau_e=P_ee obey 0<=tau_e<=1 and sum tau_e=k.

For a conductance configuration X, Sylvester's identity and 0<=P<=I give

    log[det L_X/det L_0]
      =log det[I+rho diag(X) P diag(X)]
      >= log(q) sum_e tau_e X_e.

Here each nonzero eigenvalue lies in [0,1], and log(1+rho lambda)>=lambda logq.
The acceptance probability alpha of the ordinary low-stiffness Gaussian rejection
sampler is exactly E_(independent Bernoulli p_e)[(det L_X/det L_0)^(-r/2)].
For constant p this yields

    alpha <= prod_e [1-p+p q^(-r tau_e/2)]
           <= [1-p+p q^(-r/2)]^k.                       (R1)

The second step uses convexity of log[1-p+p exp(-a t)] on [0,1]: its graph is below
the chord joining t=0,1. Thus the expected proposal count is at least the inverse
of the right side. This is exponential in k for fixed p>0,q>1,r, on EVERY graph.

This does not imply that the new CFTP implementation is faster at small size:
64 exact quarter-grid fields on the 16-site torus took .1002 s by ordinary Gaussian
rejection and 1.1039 s by CFTP. Rational dense inverse updates are expensive.
Nor does (R1) lower-bound latent Gaussian Gibbs, preconditioned Langevin/HMC,
special tree/cycle factorization, other perfect samplers, or all algorithms.
The SAME new contraction proof is freely available to the conventional chain.

The acquired distinction is an all-graph polynomial expected number of exact
conditional updates and a terminating normalized output, not generic incumbent
dominance. No new size/source grid is needed to establish the analytic contrast.
