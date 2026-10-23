# Independent verification note: bounded log-weight sensitivity

Branch: ASTRA-FRESH-20261023 / P3. Collaborator: verification_primitive.
Corpus revision read: `e606bfc587c76bdcae8b8fa3ec33e721efa2fbac`; began with `00_START_HERE.txt`.

## Status

The scalar bound below is established mathematics, independently reconstructed here. Its exact order-two form is a Kantorovich inequality and is also the alpha=2 specialization of Harrison and Manurangsi, *Exact zCDP Characterizations for Fundamental Differentially Private Mechanisms*, FORC 2026, Section 6.1, Lemma 25 and Theorem 26. Product composition is elementary. A candidate contribution may concern cheaply acquiring the sensitivities for a scientific simulator, not novelty of the inequality or conditional Monte Carlo estimator.

Primary source read: https://arxiv.org/html/2510.25746v1 . Published version: https://doi.org/10.4230/LIPIcs.FORC.2026.3 . Additional composition context: Cesar and Rogers, ALT 2021, https://proceedings.mlr.press/v132/cesar21a/cesar21a.pdf . Search coverage is focused, not exhaustive.

## The exact tensorized certificate

Let U_1,...,U_m be independent random inputs on arbitrary probability spaces. Let W(U)>0 be measurable. Assume that, outside appropriate product-null sets, changing only coordinate i changes log W by at most c_i >= 0. Equivalently, the essential ratio between the largest and smallest W on each coordinate fiber is at most r_i=exp(c_i). Assume W is not identically infinite and has positive finite mean. Finite bounded-coordinate oscillations imply the needed moment integrability once one finite reference value/fiber is fixed; alternatively explicitly assume W in L2.

Then

    R := E[W^2]/E[W]^2 <= product_i (1+r_i)^2/(4 r_i)
      = product_i cosh(c_i/2)^2
      <= exp((1/4) sum_i c_i^2).

No normalizing constant p=E W, committor, spectral gap, or rare-event probability appears in the certificate. Every c_i must be a proved global or essential coordinate-oscillation bound, not an empirical derivative maximum.

### Scalar proof

For 0<a<=Z<=b, (Z-a)(Z-b)<=0, so E Z^2 <= (a+b)mu-ab, where mu=E Z. The scalar function ((a+b)mu-ab)/mu^2 is maximized on [a,b] at mu=2ab/(a+b), with value (a+b)^2/(4ab). Taking b/a<=r gives the claimed scalar bound. If essential endpoints are not attained, pass to approximating endpoints.

### Product proof

Condition on all coordinates except U_m. The scalar inequality gives

    E_m W^2 <= K_m (E_m W)^2, K_m=cosh(c_m/2)^2.

The marginalized function V=E_m W preserves all remaining coordinate ratio bounds: W(u_i,z)<=r_i W(u_i',z) pointwise, and integration in z preserves this inequality. Induction on m therefore yields E W^2 <= K_m...K_1 (E W)^2.

### Sharpness

For any r_i>=1 choose independent B_i in {0,1} with P(B_i=1)=1/(1+r_i), and let W=product_i r_i^B_i. Every inequality above is an equality. Multiplying W by any deterministic positive constant preserves R and the equality. To impose W<=1, multiply by product_i r_i^-1. Thus the sharpness survives the interpretation as a survival weight.

Since 2 log cosh(c/2)=c^2/4+O(c^4), 1/4 is the best universal constant in a bound exp(C sum c_i^2). A naive application of bounded-difference concentration followed by Jensen gives 1/2 and loses a factor of two in the exponent.

## Compiling c_i from a dynamical model

Let X_0 be deterministic and X_{t+1}=F_t(X_t,U_t), t=0,...,T-1. All scalar components U_{t,j} are independent, or else group correlated components into independent blocks and use a block oscillation. The relevant reachable state domain D_t must be proved invariant. Let

    W=exp(sum_{t=0}^T g_t(X_t)),  g_t=log a_t,

with 0<a_t<=1 for survival. Assume componentwise nonnegative matrices M_t and vectors ell_t, b_{t,j} certify, throughout D_t and the entire innovation support,

    |F_t(x,u)-F_t(y,u)| <= M_t |x-y|,
    |F_t(x,u)-F_t(x,u')| <= b_{t,j} Delta_{t,j},
    |g_t(x)-g_t(y)| <= ell_t^T |x-y|,

where the second comparison changes only innovation coordinate j, whose support diameter is Delta_{t,j}. These are sufficient global certificates, not needed equalities.

Compute backward:

    q_T=ell_T,
    q_t=ell_t+M_t^T q_{t+1}.

Then a sound innovation oscillation bound is

    c_{t,j}=Delta_{t,j} b_{t,j}^T q_{t+1}.

Proof: a perturbation at time t changes X_{t+1} by at most b Delta, then propagates by products M_s. Sum its effects on all subsequent g_s. The backward recurrence is exactly this sum, with matrix multiplication order preserved. A random X_0 must be represented by and charged as independent input blocks too; its sensitivity is not free.

For sparse M_t the backward compiler costs O(sum_t nnz(M_t)+sum_{t,j} nnz(b_{t,j})), plus acquisition/verification of the primitive bounds. If F and g are supplied analytic formulas with elementary derivative envelopes and a proved invariant box, these bounds can be acquired by calculus and rational/interval operations without state enumeration. If only a black-box simulator is supplied, finite probing cannot certify unrestricted global Lipschitz constants. That acquisition gap remains.

Scalar specialization with contraction rho<1, innovation diameter impact sigma and |g'_t|<=L:

    c_{t} <= L sigma (1-rho^(T-t))/(1-rho).

This yields log R <= (L sigma)^2 T/[4(1-rho)^2]. It is not a time-uniform guarantee. Deterministic additive offsets in g_t do not affect c_t or R.

## Failures and falsification targets

1. **Hidden persistent mode.** Let B be one common bit, let W=exp(-kT) r^(TB), and P(B=1)=1/(1+r^T). The exact R is (1+r^T)^2/(4r^T). Treating repeated uses of B as independent falsely predicts ((1+r)^2/(4r))^T. There is one independent block with c=T log r, not T blocks with c=log r. Scaling ensures W<=1 if desired.

2. **Contraction alone does not remove long-horizon hardness.** Let X_t be independent fair bits (rho=0) and W=exp(-kT-eta sum X_t). Then

       R=[2(1+exp(-2eta))/(1+exp(-eta))^2]^T.

   This is exponentially growing in T for every eta>0. Strong contraction gives no uniform relative-variance bound at fixed nonzero log-hazard variability.

3. **No contraction.** Let X_t=sum_{s<=t} U_s with independent bounded U_s, and log a_t=-eta X_t. Innovation s influences T-s+1 hazards. Its c_s=eta(T-s+1), so sum c_s^2 is order eta^2 T^3. A bound using one-step hazard sensitivity alone is unsound.

4. **Zeros.** A terminal hard indicator or a_t=0 gives infinite log oscillation. Smoothing it changes the scientific question and requires a separate relative-bias bound. An additive approximation error does not certify a rare probability relatively.

5. **Unbounded innovations.** Gaussian innovations do not have finite diameters. Truncating them requires a bias analysis on the relative scale of p. Typical-region sensitivities without certified tail handling do not satisfy this theorem.

6. **Equal-information baseline.** Integrating known killing coins to form W is standard conditional Monte Carlo/Rao–Blackwellization. The fair baseline is the same W with the same dynamics and hazard access. A comparison against Bernoulli survival alone only measures the established benefit of integrating known coins. The possible advance is a cheap rigorous stopping/cost certificate for W, not a new estimator or universal rare-event cure.

7. **Finite precision.** Stable implementation uses log weights and logsumexp. If computed log weights differ uniformly by at most tau, expectations are only certified within exp(+-tau). Claiming numerical exactness requires directed rounding or separately accounted arithmetic error. Search/derivative compilation and failed approaches must be charged.

## Concentration consequences

For n independent W samples, relative mean-square error is (R-1)/n. Given an upper bound K on R, Chebyshev gives failure probability <=(K-1)/(n eps^2) for relative error eps. Median-of-independent-means amplifies confidence logarithmically: take each group size at least 8(K-1)/eps^2 so each fails with probability at most 1/8, then an odd number of independent groups logarithmic in 1/delta suffices by a binomial bound. Exact constants should be recomputed for the chosen implementation. This guarantee does not use the unknown p.

## Initial discarded alternative

Positive finite-range log-amplitude wavefunctions turn the stoquastic Collatz–Wielandt ground-energy lower bound into a finite-range classical optimization, tractable by transfer matrices at bounded separator width. Its lower objective is concave in log-amplitude parameters. The base bound is established (Farhi et al., arXiv:1010.0009, Theorem 4), and modern strong lower-bound comparators include renormalization-group and quantum-marginal methods. No computation or novelty claim was completed; this was superseded by the parent-requested variance verification task.
