# Independent proof: conditional-odds minimax proposal and cubic compiler

ASTRA-FRESH-20261023 / P3, 23 October 2026 (Australia/Brisbane).

This note verifies and extends the parent construction. These are written mathematical proofs and independently executed finite diagnostics; historical novelty is UNKNOWN. No physical calibration or practical scientific discovery is established.

## 1. Contract

Let the baseline P be an independent Bernoulli product on {0,1}^m with 0<p_i<1. Let f>0 and Z=E_P f. The algorithm can evaluate f at sampled points and is given or has acquired valid uniform intervals

    ell_i <= log f(1,v)-log f(0,v) <= u_i  for every v.

The intervals are actual information; acquiring them is charged. Define

    a_i=logistic(logit(p_i)+ell_i),
    b_i=logistic(logit(p_i)+u_i).

These are bounds for the single-coordinate conditional probability of the normalized target pi=fP/Z, even though neither Z nor the conditionals are evaluated. They satisfy 0<a_i<=b_i<1 when the log endpoints are finite. The proposal is

    q_i=(a_i+b_i)/2, Q_star=product_i Bernoulli(q_i),
    K_i=1+(b_i-a_i)^2/[4q_i(1-q_i)].

For independent draws V~Q_star the standard unbiased importance estimator is f(V)P(V)/Q_star(V). Its relative second moment is at most product_i K_i. The scalar f may be multiplied by any constant without changing the normalized target or relative variance.

## 2. Scalar minimax identity

For a Bernoulli target with success parameter theta and proposal q,

    R(theta,q)=theta^2/q+(1-theta)^2/(1-q)
              =1+(theta-q)^2/[q(1-q)].

At fixed q the maximum over theta in [a,b] is at an endpoint. The two endpoint values agree exactly at q=(a+b)/2. For q below that midpoint the b endpoint dominates and R(b,q) decreases as q approaches b; for q above that midpoint the a endpoint dominates and R(a,q) increases as q moves away from a. Thus the midpoint is the unique minimax proposal except for trivial endpoint degeneracies, and the value is K above. This also covers a=b, where q=a and K=1.

If a numerical or deliberately rounded proposal q_actual is used, the valid factor is simply max{R(a,q_actual),R(b,q_actual)}. Exact numerical minimization is not needed for the certificate.

### A width-only bound and a necessary strong baseline

Let w=u-ell be the log-odds interval width. Then

    K <= 1+tanh(w/4)^2 <= exp(w^2/16).

To see the first inequality, write a=logistic(z-h), b=logistic(z+h), h=w/2 and y=exp(z). Direct simplification gives

    K-1 = y sinh(h)^2 / [(cosh(h)+y)(1+y cosh(h))].

Dividing its denominator by y gives cosh(h)(y+1/y)+1+cosh(h)^2, minimized at y=1. The maximum is therefore tanh(h/2)^2. The second inequality follows from tanh(v)<=v and 1+x<=exp(x). This is useful for an arithmetic certificate because sum_i (u_i-ell_i)^2/16 can be bounded entirely by rational arithmetic before any exponential is evaluated.

However, the equally informed **midpoint log-odds tilt**

    q_log=logistic(logit(p)+(ell+u)/2)

also has a sound factor cosh(w/4)^2<=exp(w^2/16): after this tilt the remaining coordinate log-ratio has absolute value at most w/2, so the tensorized Kantorovich certificate applies. Thus the exact midpoint-probability proposal has a sharper finite-width minimax guarantee, but it does not improve the leading weak-width exponent over this simple strong baseline. Any claimed computational advantage must include that baseline and charge its certificate, not just compare against the original un-tilted estimator.

## 3. Upper bound for dependent target distributions

Write W=fP/Q_star. Condition on all inputs except coordinate m. The one-coordinate fP contribution normalized by its P_m mean has Bernoulli parameter theta_m(v) in [a_m,b_m], giving

    E_{Q_m}[(f P_m/Q_m)^2] <= K_m (E_{P_m} f)^2.

For V=E_{P_m}f, all other log-ratio intervals remain valid: multiply f(0,v,z) by exp(ell_i) and exp(u_i), compare with f(1,v,z), and integrate in z against P_m. Integrate the displayed conditional bound over Q on the remaining coordinates and induct. This proves

    E_Q[(fP/Q)^2]/Z^2 <= product_i K_i

for every positive f satisfying the uniform interval summaries, including dependent targets.

## 4. Exact minimax over arbitrary joint proposals

The same Q_star is minimax among **all joint proposals chosen using only these interval summaries**. This is stronger than minimax within product proposals. The qualifier about information is essential: further evaluations of f, learned structure, adaptivity, or more informative bounds can improve a specific target and fall outside the lower-bound contract.

For a single interval set q=(a+b)/2 and d=(b-a)/2. Let a random endpoint Theta in {a,b} have

    Pr(Theta=b)=w=1/2+d(2q-1)/[4q(1-q)].

This is a valid probability. Indeed d<=min(q,1-q), implying |w-1/2|<=1/4. Direct algebra gives

    E[Theta^2]=K q^2,
    E[(1-Theta)^2]=K(1-q)^2.

Independently choose one endpoint per coordinate with these probabilities, and let pi_Theta be the product Bernoulli distribution with those endpoint parameters. Every pi_Theta is represented by a positive f_Theta relative to the supplied baseline P, with log-ratios equal to the appropriate interval endpoints. For each x,

    E_Theta[pi_Theta(x)^2]=(product_i K_i)Q_star(x)^2.

For any joint proposal Q with full support,

    max_Theta sum_x pi_Theta(x)^2/Q(x)
      >= E_Theta sum_x pi_Theta(x)^2/Q(x)
      = (product_i K_i) sum_x Q_star(x)^2/Q(x)
      >= product_i K_i.

The final inequality is Cauchy–Schwarz, or nonnegativity of chi-square divergence. A proposal lacking support has infinite risk for these positive targets. Combined with Section 3 this proves the exact minimax value and proposal. The lower bound is not a lower bound for all estimators: it concerns the one-sample relative second moment of importance sampling with an interval-only proposal.

### Established framework and novelty limits

The product endpoint part is an elementary special case of established order-two Rényi center/radius theory. Nakiboğlu, *The Rényi Capacity and Center*, IEEE TIT 65(2), 2019, arXiv:1608.02424v8, Lemma 22, p16, equation (58), proves product centers and additive radii for arbitrary positive order. Read source: https://arxiv.org/pdf/1608.02424 . The full conditional-interval ambiguity class upper bound and simulator compiler are a specific application/extension; this note does not establish historical novelty. General robust importance sampling and bounded-range Rényi composition are also relevant predecessors.

## 5. Acquiring the intervals in a nonlinear spatial dynamics model

Let X_t in R^d, X_0=0, and let U_t in {0,1}^d be independent Bernoulli innovations. Let A be a nonnegative row-stochastic matrix. Define componentwise

    X_{t+1}=rho X_t+kappa (A X_t)^(elementwise 3)+sigma(2U_t-1),
    S(U)=sum_{t=1}^T b_t^T X_t,
    f(U)=exp(-C+S(U)),

with rational nonnegative rho,kappa,sigma and b_t>=0, rho+kappa+sigma<=1. The offset C may enforce 0<f<=1; for example C=sum_t ||b_t||_1 suffices. The simulator and its analytical derivative bounds are supplied structure. This is a mathematical discrete-time model, with no claim to be a calibrated physical process.

The invariant cube [-1,1]^d is proved by induction, including the continuous extension U_t in [0,1]^d, because each component of A X_t lies in [-1,1]. Its state Jacobian obeys componentwise

    J_minus=rho I <= D_x F_t <= J_plus=rho I+3kappa A.

The infinity-norm Lipschitz constant is lambda=rho+3kappa. Assume lambda<1 for a uniform perturbation bound. The derivative interval compiler itself is valid for any finite T even if lambda>=1, but its widths may become useless.

Define backward vectors

    v_T^-=v_T^+=b_T,
    v_t^-=b_t+J_minus^T v_{t+1}^-,
    v_t^+=b_t+J_plus^T v_{t+1}^+.

For 0<=t<T the bit (t,j) has sound log-ratio endpoints

    ell_{t,j}=2sigma v_{t+1,j}^-,
    u_{t,j}=2sigma v_{t+1,j}^+.

To prove this, differentiate the tail sum with respect to X_t. Its exact gradient is b_t+J_t^T times the subsequent exact gradient. Nonnegative Jacobians and b imply nonnegative gradients; interval propagation therefore bounds them by v^- and v^+. Differentiating with respect to U_{t,j} gives 2sigma times the appropriate state-gradient component. With all other innovations fixed, integrate that derivative while U_{t,j} goes continuously from 0 to 1. The entire interpolation remains in the invariant cube, so the global derivative interval is valid throughout the integral. The deterministic offset C cancels.

For sparse A the arithmetic operation count is O(T nnz A+Td); state-space enumeration is absent. Exact rational arithmetic has additional bit cost: denominators and numerator lengths in the backward linear recurrence grow with T. Floating interval arithmetic or a scalar closed form can reduce that cost, with outward rounding accounted for. If A is also column-stochastic and b_t=b times the all-ones vector, all adjoint components coincide and exact closed geometric sums apply, allowing O(T+d) compiler arithmetic rather than sparse matrix operations.

## 6. Floating-point state error and weight bias

Suppose each implemented map evaluation has a certified local infinity-norm error at most eta relative to the exact polynomial evaluated at the same input. If the implementation clips every numerical state component to [-1,1], then the projection is nonexpansive and cannot increase its error from the exact invariant state. Writing e_t=||Xhat_t-X_t||_infty gives

    e_{t+1}<=lambda e_t+eta,
    e_t<=eta(1-lambda^t)/(1-lambda)  (Xhat_0=X_0).

Consequently the state-induced log-weight error obeys

    |sum b_t^T Xhat_t - S| <= sum_t ||b_t||_1 eta/(1-lambda).

Add independently bounded dot-product, constant-representation, summation, log-probability and exponential evaluation errors. This statement is conditional on a valid eta for the actual floating operations; an observed discrepancy on fixtures is not such a bound. Without clipping one must first prove an enlarged invariant box and use its enlarged Jacobian envelope; silently applying the unit-cube Lipschitz constant to out-of-cube numerical states is invalid.

If the final computed log importance weight differs from the exact log weight by at most tau uniformly, then the numerical weight lies between exp(-tau) and exp(tau) times the exact one, and its expected value lies between exp(-tau)Z and exp(tau)Z. The numerical estimator is generally biased; one must inflate a confidence interval or reduce the statistical error budget. A recorded dyadic proposal parameter q_actual and exact likelihood-ratio accounting prevent an undocumented mismatch between the sampled proposal and the analyzed proposal.

## 7. Failure scope

* A hard terminal indicator creates zeros and infinite log-ratio intervals. Smoothing introduces bias requiring a separate relative-error analysis.
* A latent bit reused at many times is one innovation block. Treating it as independent per-time noise invalidates the compiler/tensorization.
* Signed coefficients or negative Jacobian entries invalidate the monotone lower/upper products above; general interval multiplication is required.
* A fitted or sampled derivative maximum is not a global derivative envelope. The construction uses known analytic formulas and a proved invariant domain.
* This does not solve generic long-time rare-event sampling. If widths remain substantial for many independent bits, product K is exponentially large, and the minimax theorem proves no interval-only proposal avoids that worst case.
* Stronger target-specific baselines may use the same full code to learn or analytically derive additional structure. Minimax of the summary class does not prove empirical superiority over those baselines.

## 8. Executable diagnostics

`check_minimax_cubic.py` uses exact rational arithmetic to check the least-favourable mixture identity, product endpoint risks, and every discrete log ratio of a small nonlinear cubic trajectory against the compiler. It separately calculates finite-sample diagnostics. A finite check supports implementation consistency; the proofs above establish the general claims.
