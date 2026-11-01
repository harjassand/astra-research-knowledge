# Independent theorem audit: source inverse forms to all-time survival

## Verdict and frozen boundary

**PASS, theorem-only**, for `RESOLVENT_TO_SURVIVAL_ROOT_CANDIDATE.md`, SHA-256 `2414f104c0b74b59796af2f24c9a93ac5300a1a6eee7bd1137e0adef1dbfee67`. No source correction was needed, and the frozen bytes were not edited.

The scalar spectral lemma, form/inverse-form normalization, positivity domination, actual-initial-law comparison, all-time bound and finite-parameter substitution are sound. The result is UNIFORM ABSOLUTE survival/CDF accuracy for the declared full Gibbs|A initial law, not tail-relative accuracy, exact exponentiality, an exponential-moment bound, or a generic initial-law replacement theorem.

No executable, proposed numerical KS value (including the mentioned 0.00492567), or new numerical certificate is accepted here. The ordinary constant-mobility family and its previously earned Poisson-current premises remain actual model assumptions; a mobility floor is not an accuracy knob that can be supplied without changing/identifying kinetics.

Two useful theorem-only additions are separately proved in `TRIAL_FUNCTION_AND_MIDPOINT_COROLLARIES.md`: any suitable form-domain trial h suffices, so the explicit scalar transition profile can replace the actual committor; and an arithmetic midpoint of an outward rate interval incurs at most 3/16 times its relative width in additional uniform absolute error. `LIMITS_COUNTEREXAMPLE.md` gives an exact reversible process validating the tail/initialization limits. Neither addition silently modifies the root theorem.

## 1. Scalar spectral lemma: all-time control with only first and inverse moments

Let X>0, E X<=1 and E X^-1<=1+epsilon, epsilon>=0. Both required moments are finite. For s>=0, convexity gives E exp(-sX)>=exp(-s E X)>=exp(-s).

The Taylor remainder around x=1 is

    R_s(x)=exp(-sx)-exp(-s)+s exp(-s)(x-1)>=0.

For x>=1 it equals integral_1^x (x-u)s^2 exp(-su)du; for x<=1 it equals integral_x^1 (u-x)s^2 exp(-su)du. For every fixed u>0, maximizing over s>=0 gives s^2 exp(-su)<=4/(e^2 u^2). Both integrals of the resulting elementary kernel equal x-1-log x. Thus

    0<=R_s(x)<=[4/e^2](x-1-log x)
                 <=[4/e^2](x-1)^2/x.

The last inequality is equivalent to log x>=1-1/x, valid for all x>0 by differentiation or concavity. It is not restricted to x>=1. The root's two displayed remainder expressions are algebraically identical and correct.

Cauchy–Schwarz gives E X E X^-1>=1, hence E X>=1/(1+epsilon) and

    0<=1-E X<=epsilon/(1+epsilon),
    E[(X-1)^2/X]=E X+E X^-1-2<=epsilon.

Taking expectations in the Taylor identity and using sup_s s exp(-s)=1/e gives

    E exp(-sX)-exp(-s)
       <=epsilon/[e(1+epsilon)]+4epsilon/e^2<=epsilon.

The last constant is safely below one: even the rational estimate e>8/3 gives 1/e+4/e^2<3/8+9/16=15/16<1. At epsilon=0, equality of arithmetic/harmonic moments forces X=1 almost surely. The argument covers s=0 and all arbitrarily large s with the same constant; it is not a time-grid test.

No second moment of X, second inverse moment, lower spectral support bound, upper support bound, or exponential inverse moment is required. In particular, the lemma does not imply an exponentially decaying true tail just because its absolute discrepancy from an exponential is small.

## 2. Killed Hilbert form and zero-resolvent interpretation

Let K>=0 be the self-adjoint operator associated with the ACTUAL killed reversible Dirichlet form. The reference measure may be any finite positive multiple of the invariant measure of the original process, restricted to D; it need not be invariant under the killed semigroup. Its finiteness ensures bounded h and the indicator sources lie in L2(m).

The hypotheses must include that h lies in the killed form domain, has the stated boundary/range values, and finite form energy. The notation <h,Kh> is correctly interpreted as ||K^(1/2)h||^2; membership in the operator domain D(K) is not needed. In the inherited smooth constant-SPD model this form/domain statement follows from the weighted H1 variational construction and target trace. Alternatively the explicitly constructed scalar trial in the separate corollary avoids any dependence on an actual committor existence argument.

For r>0 let R_r=(K+r)^-1. It is positivity preserving, self-adjoint and bounded. Inverse forms mean

    Q_f=lim_(r down0)<f,R_r f>,

not a globally bounded inverse operator. The source-current construction and its compact-core/extended-energy approximation must genuinely establish finite Q_A and Q_S. The reviewed theorem does not replace that work by a formal K^-1 symbol. The prior MFPT current proof uses positive discounted resolvents and full-tail bounds before passing to zero, so it supplies the needed kind of premise.

For nonnegative h<=1_D, positivity first gives R_r h<=R_r1_D, then

    <h,R_r h><=<1_D,R_r1_D>.

This pointwise-positive domination is valid; it is not an invalid assertion that arbitrary ordered vectors preserve quadratic forms. Decomposing 1_D=1_A+1_S and applying positive-operator Cauchy–Schwarz yields

    <1_D,R_r1_D>
       <=[sqrt(Q_A(r))+sqrt(Q_S(r))]^2
       <=B_A(1+rho)^2.

Monotone convergence gives finite Q_h with the same upper bound. This is source-specific inverse-form information. The spectrum of K may still accumulate at zero, and K may have no bounded inverse on the whole Hilbert space.

## 3. Spectral normalization, epsilon positivity, and time units

Set N=||h||^2. The boundary/range values give M<=N<=M+S0=M(1+rho), where M=m(A)>0 and rho=S0/M. The spectral measure

    nu_h(dlambda)=N^-1 d||E_K(lambda)h||^2

is a probability measure. Its first moment equals E(h,h)/N; its inverse moment equals Q_h/N. Finiteness of Q_h excludes an atom at lambda=0. It does NOT exclude spectral support arbitrarily near zero.

The form/inverse-form Cauchy inequality is

    N^2 <= E(h,h) Q_h.

It follows directly from the spectral integral, using sqrt(lambda) and 1/sqrt(lambda). It implies the form energy is positive, hence any finite upper C0 is positive and k0=C0/M is well-defined. It also verifies the source's claimed epsilon>=0:

    M^2<=N^2<=E(h,h)Q_h
       <=C0 B_A(1+rho)^2.

For X=lambda/k0,

    E X=E(h,h)/(N k0)<=C0/(N k0)=M/N<=1,
    E X^-1=k0 Q_h/N
             <=C0 B_A(1+rho)^2/M^2=1+epsilon.

The scalar lemma therefore applies with s=k0 t, proving that C_h(t)=<h,P_t h>/N lies between exp(-k0t) and exp(-k0t)+epsilon for ALL t>=0.

No normalizer is missing. Multiplying m by any positive constant multiplies M,S0,N,C0,B_A and Q_h by that constant, leaving k0, rho and epsilon unchanged. For the fiber application, C0=1/(beta R), so k0=1/(beta M R) has the intended time units. It is the scalar trial reference rate, not an assertion that the actual conductance or inverse mean equals k0.

## 4. Exact comparison with the requested initial law

The actual survival from m(.|A) is

    S_A(t)=<1_A,P_t1_D>/M.

Define e=h-1_A and d=1_D-h. Both are nonnegative, supported in S and bounded by one. The exact unnormalized difference is

    <1_A,P_t1_D>-<h,P_th>
       =<1_A,P_t d>-<e,P_t h>.

Positivity preserving P_t makes BOTH terms on the right nonnegative. Contraction bounds them by sqrt(M S0) and sqrt(N S0). Therefore the absolute value of their difference is bounded by the MAXIMUM, sqrt(N S0), not by their sum. This factor is valid and important.

To change normalization, use 0<=<h,P_th>/N<=1 and 1<=N/M<=1+rho:

    |S_A(t)-C_h(t)|
       <=sqrt(N S0)/M+(N/M-1)
       <=sqrt(rho(1+rho))+rho=d_init.

Combining this with the scalar lemma gives exactly the root's lower and upper survival bounds. Clipping to [0,1] preserves them. The corresponding CDF has the same uniform absolute error because F_A(t)=1-S_A(t). No density-ratio estimate, angular sampling, pointwise mixing, or gap enters this initialization comparison.

The claim is specifically for the declared conditioned invariant law. In the ordinary constant-SPD quartic model, matching only the (Y,U) marginal or using a fixed angular ray is NOT an equivalent initialization: that process has no established exact (Y,U) Markov closure. The earlier engineered-lift initialization freedom must not be imported here.

## 5. Application: what the acquired current bounds actually supply

With the common unknown fiber partition divided out, the y marginal is q, M=integral_A q and S0=integral_S q. The scalar transition profile gives C0=1/(beta R), R=integral_slab q^-1. The same A-current and S-current used in the MFPT proof give Q_A<=B_A and Q_S<=rho^2 B_A because J_S<=rho J_A pointwise in the killed domain. In the actual full-state model their inverse-mobility weight must remain the ordinary constant-SPD weight, not the radial engineered weight from another process.

This adds a new spectral/form use of the current certificate; it does not identify a passage time with capacity. No Poisson solution, spectral decomposition, committor sample or angular equilibrium sampler is executed by this argument. The constructed current proves bounds on the needed source inverse forms, and a scalar test proves the form-energy bound.

Suppose T_upper is known to bound the PARTICULAR current expression (1+rho)B_A/M, and T0_lower<=T0=beta M R. Then

    1+epsilon=(1+rho)*[(1+rho)B_A/M]/T0
       <=(1+rho_upper)T_upper/T0_lower.

So the proposed epsilon_upper is sound. Merely possessing some unrelated upper bound on the actual mean is not enough: the receiver must preserve the current-expression domination used here. The externally bound numerical source parameters and their origins cannot be discarded.

If T0 lies in [T0_lower,T0_upper], the exponential ordering is

    exp(-t/T0_lower)<=exp(-t/T0)<=exp(-t/T0_upper).

Thus the root's lower/upper rate endpoint substitutions have the correct directions. A midpoint is not an exact rate, but the separate midpoint corollary pays its uniform error explicitly. Outward square roots for d_init, all source/rate interval arithmetic, the requested total KS budget, and any queried numerical exponential require their own complete receiver. The mentioned numerical candidate is not accepted by this theorem-only audit.

## 6. Stronger trial-function form and rate midpoint: separately scoped results

The proof does not use h's harmonicity, its minimizing property, or equality E(h,h)=cap. It works for any killed-form-domain h with 0<=h<=1, h=1 on A, and E(h,h)<=C0. The explicit scalar optimal profile has exactly the needed energy, range and trace. This removes even the need to introduce the actual committor for this application, while preserving every source/initialization premise. The complete corollary is recorded separately.

For 0<lo<=k0<=hi and arithmetic rate midpoint k_star, differentiation in rate gives

    |exp(-k_star t)-exp(-k0 t)|
      <=[(hi-lo)/2]t exp(-lo t).

Taking the exact all-time supremum gives (hi/lo-1)/(2e), at most (3/16)(hi/lo-1). This may be added to the received absolute error by the triangle inequality. The proof is uniform in time and is not an extra asymptotic or numerical grid premise.

## 7. Tail and initialization limits: an actual counterexample

The separate `LIMITS_COUNTEREXAMPLE.md` constructs a rate distribution with EX=1 and

    E X^-1-1=delta(2-delta)/(3-2delta)<=delta,

but exponential-mixture survival asymptotic to 2delta/t^2. It is realized as an actual finite-reference-measure reversible star-jump process with killed spectral operator multiplication by the rate. It satisfies the abstract theorem with S empty and arbitrarily small epsilon, while its second hitting-time moment and all positive exponential hitting-time moments diverge. The actual quartic diffusion is not claimed to share that particular second-moment divergence; the example proves only that the general certificate cannot imply more.

The same process shows that total-variation preparation contamination of size eta changes every survival probability by at most eta, yet can add eta/x0 to the mean by placing contamination at a tiny rate x0. Hence the root correctly distinguishes bounded-CDF robustness from unbounded-mean robustness. A separately justified TV bound can be added to the survival/CDF error; it does not certify the previous MFPT. No small-TV claim is automatically available for a finite-bit approximation to a continuous Gibbs law.

Small uniform absolute error also does not give uniformly small relative extreme-tail error, relative accuracy of every quantile, a hazard-rate approximation, all-start exponentiality, or a whole-space/killed gap. The zero-gap source note's polynomial-tail scalar test functions are consistent with this result: the theorem only constrains the spectral measure seen by one suitable h in a first/inverse-moment sense.

## 8. Strong ordinary prior and new joining work

I independently opened [Aldous–Fill, Section 3.5](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S5.html), including Section 3.5.4. It explicitly develops complete-monotone spectral mixtures, first/inverse-rate relationships, and uniform absolute exponential-approximation bounds using moment information; its Proposition 3.22 attributes a quantitative moment bound to Mark Brown. Its subsequent relaxation-time bound is one route, not the only ordinary method. The present proof uses a different sufficient first-rate/inverse-rate admission and does not require the second hitting-time moment used by that stated bound. This is a hypothesis distinction, not a novelty claim.

I also inspected [Fernández–Manzo–Nardi–Scoppola, arXiv:1406.2637](https://arxiv.org/pdf/1406.2637), especially its recurrence condition and Theorem 2.3. It provides quantitative exponentiality without reversibility from specified recurrence/exit-time control. Those quantitative premises are not supplied automatically here. Lack of an angular gap or a global gap therefore cannot itself be presented as a new generic exponentiality principle.

The specifically audited joining work is: actual source-current inverse-form bounds; a form-energy test with the same raw process and initialization; a spectral moment lemma; and an explicit comparison to the requested Gibbs|A survival. Equally informed ordinary variational/spectral methods receive the same constructed certificates. No historical priority, proprietary separation, comparative runtime victory or physical calibration is established.

## 9. Independent executed checks and preservation

`check_survival_algebra.py` passed **1,124 exact assertions** without importing any candidate implementation. They include both Taylor kernel integrals, the logarithm/weighted-variance identities, exact rational constant bounds, rational moment fixtures, weighted finite reversible killed chains with true committors AND nonharmonic trials, form/inverse Cauchy and domination, the exact initialization difference identity, the heavy-tail counterexample transform/moments, and the frozen root hash. General Hilbert-space and all-time statements are established by the proofs above; finite fixtures supplement rather than replace them.

The root source snapshot, input hash, script, results, separate corollaries, limits example and this receipt are preserved in a unique audit directory. Source bytes were rechecked unchanged. No frozen proof or prior artifact was overwritten, and no executable survival certificate was accepted.
