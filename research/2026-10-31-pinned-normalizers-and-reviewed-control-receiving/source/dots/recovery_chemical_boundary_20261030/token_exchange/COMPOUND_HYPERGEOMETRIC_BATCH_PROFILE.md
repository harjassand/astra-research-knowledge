# Exact carried profile for a fixed reset batch

30 October 2026. New completion of HYPERGEOMETRIC_CARRIED_PROFILE.md; candidate, no global extension.

Replace its one-slot selection by sampling k distinct slots uniformly from the Y+ell old-worker/null slots, with fixed ell>=k>=1. Reset every sampled old working identity to rank L; null selections do nothing. A source entry still creates exactly one new rank-L worker and preserves n. Per-label adverse participation is k gamma C/(Y+ell), so the productive-pool forcing contract remains valid with batch k. All other progress, nonexplosion and killing assumptions are unchanged.

## An explicit finite composition, not an unknown value function

Set, for h=0,...,k-1,

    N_h=n+ell-h-1,   d_h=Y+ell-h-1.

Starting H_0=A, successively draw

    H_(h+1) | H_h ~ Hypergeom(N_h,marked=H_h,draws=d_h),

using conditionally independent auxiliary draws. Define

    Phi_s^(k)(A,Y;n)=E(1+H_k)^(-s),
    mu_k=A product_(h=0)^(k-1) d_h/N_h.

These auxiliary draws are a representation of the value function, not independent physical label histories. Since ell>=k, all populations/draws are valid for0<=A<=Y<=n; boundary N_h=0 uses the natural degenerate convention.

The actual pure-entry terminal old-target count has factorial moments

    E(H_final)_j
      =(A)_j product_h (d_h)_j/(N_h)_j.

Indeed the probability that j specified old targets avoid a k-slot reset at working size r is

    (r+ell-j)_k/(r+ell)_k
      =product_h (r+ell-h-j)/(r+ell-h).

Multiplying over r=Y,...,n-1 telescopes to the displayed moments. The auxiliary successive hypergeometric thinnings have exactly the same factorial moments. Finite-support uniqueness therefore proves their equality in law.

Consequently Phi_s^(k) is EXACTLY harmonic for entry plus batch reset, equals f_s(A) at Y=n, and decreases when A increases. Progress and safe moves have nonpositive drift.

## Uniform comparability

The mean of H_k is mu_k. Jensen gives Phi_s^(k)>=f_s(mu_k). For the reverse bound, use the hypergeometric lower-tail estimate separately at each auxiliary thinning. Conditional on all prior stages losing at most a factor2 relative to their successive means, at stage j=1,...,k the current conditional mean is at least mu_k/2^(j-1), because every remaining thinning fraction is<=1. Hence

    P(H_k<mu_k/2^k)<=k exp(-c_k mu_k).

Split the inverse-profile expectation there to obtain

    f_s(mu_k)<=Phi_s^(k)<=C_(s,k) f_s(mu_k).

This also gives the same square-comparability needed for the graded Green argument. For fixed ell,k and large Y,n, the effective carried count is comparable to A(Y/n)^k, but the exact product of shifted ratios is the formula used at finite heads.

## Consequences and limitations

The stopped killing argument retains alpha=m/((L+1)m+1): batch size k changes constants in product damping and cohort retention, not the source-preparation power. Every local graded assertion of HYPERGEOMETRIC_CARRIED_PROFILE transfers with Phi_s replaced by Phi_s^(k), because harmonicity, monotonicity, square comparability and the actual-A compensator were the only profile properties used.

For a kill deleting at most m targets, if A<2m the pre-kill effective count is bounded. Otherwise every shifted numerator d_h is at least Y>=A>=2m, so after deletion it decreases by at most a factor2, while denominators only decrease. Thus mu_k,out>=2^(-(k+1))mu_k,pre. This supplies bounded-loss carried preservation, not population-small carried reset.

For exact one-step progress and no additional safe moves, the all-source lower example still ignores resets and proves the matching time-power lower bound. Arbitrary biased sampling, working-to-source returns, unbounded batch size, seed deletion or immigration are not automatically included. The contribution is a constructive correlated-batch carried barrier, not a claim that an arbitrary raw face has this exchange law.
