# Stronger ordinary alternative: stratified covariance-action times

This alternative was constructed and executed after the independent-time obstruction. The same authorized helper checked its law bound and the additional arguments below. Full independent proofs are retained in helper/STRATIFIED.md.

## Legal program and unchanged full-law theorem

Draw T_j independently uniform on [(j-1)/k,j/k], rather than all of [0,1]. Use a fresh Gaussian center and two fresh secant actions. Define

    M(t)=E[H_sqrt(1-t)(sqrt(t)C)^2],
    Sigma_j=k integral_((j-1)/k)^(j/k) M(t)dt.

Then E[J_j(v)|v]=Sigma_j v, ||J_j(v)||<=L^2||v||, and (1/k)sum Sigma_j=Sigma. The average action is EXACTLY unbiased. Individual calls are independent but not identically distributed. Conditioned on Z,

    E||Jbar(Z)-Sigma Z||^2
       =k^(-2)sum_j E||J_j(Z)-Sigma_j Z||^2 <=L^4||Z||^2/k.

Every step of THEOREM.md's bound (B) remains valid, with the same deterministic n+4k query cap. `corrected_sampler(..., stratified_time=True)` implements it. Exact mean is mu; covariance is sigma^2 I+E[Jbar Jbar^T]/(4 tau^2 n^2). The independent-time obstruction does not cover this variant.

## Matrix time-quadrature geometry

Let H_t=E[Dg(B_1)|F_t], a bounded self-adjoint matrix martingale. With M(t)=E H_t^2, for u>t,

    M(u)-M(t)=E[(H_u-H_t)^2] >=0,  0<=M(t)<=L^2 I.

The cross terms vanish conditionally; no commutativity is assumed. Thus M is Loewner monotone, including its weak-terminal endpoint. Every realized stratified average and integral Sigma lie between the same lower and upper matrix Riemann sums. Their difference telescopes, yielding pathwise

    ||(1/k)sum_j M(T_j)-Sigma||op <= L^2/k.                  (1)

This does not supply M(t) to the program. The sampled center and secant randomness remain acquired and charged.

## Exact sine-family variance reduction

For g_i=sin(x_i), put v=(1-exp(-2))/2 and q(t)=exp(-1)cosh t. The common-time coefficient qbar=(1/k)sum_j q(T_j) is unbiased for v. On a_j=(j-1)/k,b_j=j/k,

    E q(T_j)=exp(-1)k[sinh(b_j)-sinh(a_j)],
    E q(T_j)^2=exp(-2)[1/2+(k/4)(sinh(2b_j)-sinh(2a_j))].

Therefore

    Var(qbar)=exp(-2){(1/2+sinh(2)/4)/k-k[cosh(1/k)-1]
                      -(sinh(2)/2)tanh(1/(2k))}
              =c_star/k^3+O(k^(-5)),
    c_star=exp(-2)[sinh(2)-2]/48>0.

Also Var(qbar)<=v^2/(12k^3), by sup q'=v and the independent-pair variance identity. At k=8 its exact variance is 8.92191e-6, versus 4.33365e-4 with independent times: a factor 48.5731 reduction at equal action count. This is a variance comparison, not a factor-of-48 TV or runtime improvement.

Executed actual secant samplers at d=65536,n=k=8 used 40 queries each. Across 384 runs radial standard deviations were 1.0984 (independent times), 1.0107 (stratified), and 0.9726 (independent target reference). The finite reference fluctuates too. These diagnostics do not certify full law; THEOREM.md supplies the bound. All seeds and data are in stratified_checks.json.

## A residual d^(1/4) architecture obstruction

**Theorem.** For this exact stratified first correction on the sine family, ANY deterministic n+4k=o(d^(1/4)) has TV error tending to one. This is weaker than the independent-time d^(1/3) obstruction, and does not establish that d^(1/4) suffices. The general upper bound remains d^(1/3).

The coupled diagonal surrogate from OBSTRUCTION.md has variance defect

    delta=(v-qbar)/n+Rbar/(4 tau^2 n^2),
    Rbar=qbar^2+k^(-2)sum_j[r(T_j)-q(T_j)^2].

For k->infinity, Rbar->v^2. The triangular array satisfies W_k=k^(3/2)(qbar-v)=>N(0,c_star): exact variance tends to c_star and each independent normalized summand is bounded by sup|q'|/sqrt(k), proving Lindeberg. Put gamma=n/k^(3/2) and pass to convergent subsequences in [0,infinity]. If gamma->gamma_0<infinity, the n^2-normalized variance defect tends to

    -gamma_0 N(0,c_star)+v^2/(4 tau^2).

This is a positive constant if gamma_0=0, otherwise atom-free. If gamma->infinity, normalize instead by a=n k^(3/2)=n^2/gamma<n^2; then a delta=>N(0,c_star). The target shell tends to zero at both normalizations because n^2/sqrt(d)<=(n+4k)^2/sqrt(d)->0. Conditional-coordinate errors vanish by that bound. The actual-to-surrogate error at n^2 scale is O(n sqrt(log(2d)/d)) in L1, also vanishing. A shrinking shell event separates the candidate from the target.

For bounded k, fixed-k arguments from OBSTRUCTION.md apply. For fixed n,k, delta is analytic and not identically zero on the stratum rectangle: an identically zero expression would extend analytically throughout the connected cube, contradicting positivity as all T_j approach zero. Its zero set has measure zero. These subsequences cover every allocation.

The positive n^(-2) residual is substantive. Conditional Jensen gives Cov(Y)>=sigma^2 I+Sigma^2/(4 tau^2 n^2) for both schedules. Covariance alone would not give a TV lower bound; the coordinate-shell proof is the extra obligation supplied here.

## Exact remaining instrument

Stratification removes one global random coefficient. It does not acquire a deterministic covariance, eliminate spatial action randomization, or provide a reusable quadratic full-law update. A useful next attack is a second acquired positive correction that removes both Sigma^2 and the implemented randomization law, while retaining the nonlinear endpoint action. Inserting another unbiased action inside a presumed matrix square root would repeat the original gap.
