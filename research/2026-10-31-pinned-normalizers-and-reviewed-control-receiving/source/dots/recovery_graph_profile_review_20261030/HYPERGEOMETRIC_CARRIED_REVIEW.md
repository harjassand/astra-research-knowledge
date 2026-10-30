# Independent hypergeometric carried-profile review

30 October 2026. Frozen source SHA256 d9eba1dba8330fca848d3a17a728e8dbb90dffa48e8af695f99e2c87c9f59a3b, copied to `product_sources/HYPERGEOMETRIC_CARRIED_PROFILE.md`.

**Verdict: accept the exact uniform-reset carried profile, its local graded Green and actual-A kill-output estimates, and the stated abstract killing-time power sharpness.** This is restricted to the specified null-slot uniform-reset module. It does not supply a carried population-small output norm or a raw/global transfer.

## Harmonicity and comparability

For j specified old targets, each entry at working size r misses all of them with probability 1-j/(r+ell). The product from r=Y through n-1 equals (Y+ell-1)_j/(n+ell-1)_j. Multiplying by (A)_j gives exactly the factorial moments of Hypergeom(n+ell-1,A,Y+ell-1). These moments determine the bounded integer distribution. Pure source entries reach Y=n almost surely, so the expected terminal f_s is precisely Phi_s and is harmonic under entry/reset, including its exact finite-population fluctuations. Equivalently,

    Phi(A,Y) = (1-A/(Y+ell))Phi(A,Y+1)
               + A/(Y+ell)Phi(A-1,Y+1).

Coupling marked sets shows Phi_s decreases with A at fixed Y. Thus genuine working progress and any additional working-only rank decreases have nonpositive drift. No heuristic inverse of the martingale is substituted for this value function.

The hypergeometric exponential-transform comparison follows from the elementary symmetric mean inequality for the nonnegative sampling weights. Pair averaging preserves their sum and increases the symmetric polynomial through its nonnegative product coefficient. The binomial-style transform upper bound is therefore valid without independence. At theta=log 2, exponential Markov at H<=mu/2 gives exp[-(1-log 2)mu/2]. Splitting f_s there proves the upper comparison; convexity gives the lower. Constants are uniform in all population/pool states, with the specified degenerate convention. Jensen and the comparison imply Phi_s^2<=Phi_(2s)<=C_s Phi_s^2.

An independent exact-rational check (`check_hypergeom_profile.py/.json`) verifies 8,160 harmonic recurrence states and 8,160 target-monotonicity states for n=1,...,15, ell=1,...,4 and s=1,2,3; Jensen's squared-profile inequality was also checked. These are falsification aids, not the analytic proof.

## Actual stopped scale

The model has monotone working population and per-worker adverse participation gamma C/(Y+ell)<=gamma C/(1+Y). First-third source entry produces order nT workers unless the initial pool is already sufficiently large. Conditional on that realized pool, second-third product forcing has damping bounded below by a constant because the adverse rate is at most B/T. It produces order nT^(L+1) targets with exponential failure at that scale.

The final target cohort is chosen from actual past information. On an interval epsilon T, bounded-touch exponential counting yields fewer than half the cohort touched with exponentially high probability when epsilon is fixed sufficiently small relative to B. Safe/progress moves cannot remove untouched targets. This supplies an actual positive-length target plateau, not merely a terminal count. Its integrated kill hazard is order T[nT^(L+1)]^m.

At alpha=m/((L+1)m+1) and T=C n^-alpha, choose C large for the hazard term and then n large for the forcing/touch errors. Conditional block survival is at most one half, uniformly over every initial pool/rank state. Because n stays fixed, geometric block restarting gives all fixed time moments and the square-root survival integral at scale n^-alpha. No replenishment is needed for this particular fixed-n model when n is sufficiently large; n<m is explicitly excluded.

For the exact one-step/no-extra-safe subclass, ignoring resets with the same independent source-entry and progress clocks gives a pathwise target-dominating reference. Each reference label completes one entry and L progress stages with probability at most gamma q^L t^(L+1)/(L+1)!. Its independent factorial target moment bounds the actual integrated kill intensity. This proves the matching lower moment scale from the all-source initial state. The result is sharpness of the uniform abstract population power, not leading constants or physical-network optimality.

## Graded and actual output consequences

The bounded supermartingale Phi_s can be used at deterministic times and at the independent Cox kill's pre-jump state. Its grade-2s expectation, the squared-profile comparison and unconditioned Cauchy-Schwarz give the integrand bound C Phi_s(initial) P(alive)^(1/2). Integrating yields the claimed incoming carried Green. Since the hypergeometric count never exceeds A, Phi_s>=f_s(A), so the actual-A integrand is also covered.

At the kill, bounded loss of at most m targets gives actual-A inverse-profile preservation relative to incoming Phi_s. Grade 2s plus the squared-profile comparison and the actual low-input kill compensator then yield the stronger actual output grade s+p with factor n^[-alpha p/(2p+m)]. This uses Phi_s(initial), never the invalid replacement f_s(initial A).

The carried-output preservation is valid for the EXPLICIT update (n,Y,A)->(n-d,Y-d,A-d), 0<=d<=m. For A>=2m, the two numerator factors in mu shrink by at most a factor two each while the denominator decreases, so mu_out>=mu_pre/4. For A<2m, pre-kill mu is bounded and trivial boundedness pays the ratio. This does not automatically cover arbitrary additional worker/source losses, or new metadata changes at the terminal mark. Degenerate zero population is handled by the stated convention.

No population-small factor for Phi at output follows. Repeated cycles may need the resource Y/n retained explicitly. General nonuniform/batched C/Y resets, worker-to-source returns, immigration, seed deletion, other terminal outputs and physical-clock conversion are outside this theorem. In particular the exact harmonic identity cannot be transferred merely from a matching mean reset rate. No load-bearing gap was found in the frozen local construction.
