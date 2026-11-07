# A finite-program Poisson corrector and an observed residual

This supplies explicit budgets for the finite-program operation in the constructor's final attack. Spectral mixing, bounded Monte Carlo and the union bound are established machinery. No historical novelty or finite-N prediction theorem is asserted.

## Finite-program lemma

Let p range over P parameters. For each p, a reversible irreducible continuous-time chain has states in {0,1}^m, stationary minimum probability at least p_*>0, gap at least g>0, and uniformization proposal rate at most R. Let |j_p|<=J be exactly stationary centered. A proposal and j_p(x) must be computable with declared polynomial cost; E proposal labels and their probabilities must be evaluable to b bits with polynomial bit cost. The chain is not supplied by an exponentially large matrix. Assume J>0; J=0 is trivial.

There is a random finite program that, with probability at least 1-delta, defines simultaneous deterministic functions fhat_p with

    sup_(p,x)|fhat_p(x)-G_p^(-1)j_p(x)|<=e,   G_p=-L_p,

where the inverse has zero stationary mean. Storage and evaluation cost are polynomial in P,m,E,J,R,g^(-1),e^(-1),log(1/p_*),log(1/delta) and local proposal bit cost.

**Proof.** Reversibility and the gap give |E_x j_p(X_t)|<=J p_*^(-1/2)e^(-gt). Choose a rational upper approximation to

    tau=max(1,g^(-1)log(max(1,4J/(g e sqrt(p_*))))).

The resolvent tail is at most e/4. For independent U uniform on [0,tau], Y=tau j_p(X_U) started at x has |Y|<=tau J and expectation equal to the truncated integral. Use

    M>=8 tau^2 J^2 e^(-2)log(2P 2^m/delta)

independent seed blocks at each p. Hoeffding and the union bound give simultaneous error <=e/2 over all p,x. The SAME seeds are reused for every input x. The blocks remain independent for each fixed x; independence across different inputs is unnecessary. The log cardinality m enters the sample count. No enumeration of inputs is performed.

A finite-bit implementation has a uniform bias budget e/4. Uniformize at R, put mu=R tau, and take

    Kcap>=max(2exp(1)mu,log_2(max(1,32tau J/e)))+2.

The Poisson tail is <=2^(-Kcap)<=e/(32tau J). Aborting at this cap changes a bounded score mean by <=e/16. Round U and the capped Poisson and local categorical probabilities to b bits with positive residual labels. Coupling the draws and the time discrepancy bounds the path-law error by

    [(Kcap+1)+Kcap E+R tau]2^(-b).

Choose b so 2tau J times this bound is <=e/16, approximate the drift to e/(16tau), and reserve e/16 for arithmetic. Clip the approximated drift to [-J,J] and the final trajectory score to [-tau J,tau J]; clipping cannot increase error from a true score in that interval and preserves the stated concentration bound. Capped Poisson probabilities can be computed by elementary exponential/Taylor bounds at polynomial bit cost. Each block holds the finite bits for U, the capped Poisson draw and Kcap proposals. Apply bounded concentration directly to these digital scores, whose means differ from the ideal means by <=e/4. Tail, bias and sampling error total <=e. Clip the returned function to any independently proved resolvent bound if desired. This proves the claim.

## Explicit application

For the open primal exclusion cells at p in [a,1-a], p_*>=a^m, g>=a^2/(12L^2), R<=lambda L and J<=lambda L. Hence all budgets are polynomial in L,a^(-1),lambda,e^(-1) and log confidence. The empirical-density glue in Funaki-Gu-Wang (6.34) uses only polynomially many clamped count fractions. Its density cutoff a=large_side^(-1/6) and small_side about large_side^(1/12) preserve polynomial costs in the large side.

Use the source's actual spatial truncation, sum the open correctors, and divide by the large volume to form F. The finite program forms Fhat of the SAME support. Its error and supremum bound are explicit from the number of summands and the above Poisson estimates. Fresh unrelated noisy answers inside a formal probability density would not define the required function; fixed seed blocks do.

For support interval size m_F, ||F||,||Fhat||<=B_F, at most 2m_F translates change under exchange of 0,1. Therefore

    |pi_(0,1)Gamma_(F-Fhat)|<=4m_F||F-Fhat||,
    |pi_(0,1)(ell+Gamma_F)|<=1+4m_F B_F.

The energy-score change is at most 8lambda m_F||F-Fhat||(1+4m_F B_F). This uses a common cap on both functions.

Define, to fix the normalization,

    R_F(rho)=E_rho Z_F-2rho(1-rho)D(rho),
    Z_F=c_(0,1)[pi_(0,1)(ell+Gamma_F)]^2.

The variational characterization gives R_F>=0. The source's Proposition6.7 and Lemma6.8/Proposition6.9 give uniform algebraic convergence for the glued sequence. Our residual is twice a half-energy convention where applicable; the subtracted conductivity is always exactly 2rho(1-rho)D(rho).

If Z_Fhat depends on q bits including the rate neighborhood, B_Z=lambda(1+4m_F B_F)^2 bounds it. The finite Bernoulli polynomial obeys |dE_rho Z/drho|<=2qB_Z on [0,1]. The score is zero at constant configurations, so within e_R/(16qB_Z) of an endpoint its residual is <=e_R/8. Elsewhere, independent bounded Bernoulli samples give upper energy intervals; the independent primal/dual compiler gives lower conductivity intervals. A mesh spacing <=e_R/(16qB_Z), the energy modulus, and the minimum certified conductivity on each cell give an observed upper bound on sup R_Fhat. The latter minimum follows from the compiler's cellwise density intervals and the explicit quadratic rho(1-rho); no derivative of D is assumed.

Relative acquired-rate error eta inflates the true residual upper bound to

    upper_energy_acquired/(1-eta)
       -lower_conductivity_acquired/(1+eta).

Refine eta to fit the residual budget. Polynomial support/norm/evaluation at each stage and the published uniform algebraic convergence prove polynomial termination at fixed class parameters. Failure allocations proportional to 2^(-stage^2) control adaptive correctness and expected work. The convergence constant is not an input to the observed residual test. This does not yet provide the separate finite-N entropy/profile lift.
