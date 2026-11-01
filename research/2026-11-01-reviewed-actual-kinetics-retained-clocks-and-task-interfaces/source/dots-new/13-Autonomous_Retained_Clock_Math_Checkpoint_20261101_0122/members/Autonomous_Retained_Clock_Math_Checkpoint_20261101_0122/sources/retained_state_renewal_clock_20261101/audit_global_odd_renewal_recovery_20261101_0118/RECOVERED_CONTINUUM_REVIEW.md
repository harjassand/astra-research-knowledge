# Retained-clock continuum proof: recovery rendering

This is a NEW recovery rendering of the independent proof completed before the approximately 01:14 UTC workspace incident. It is not claimed to have the byte hash of the vanished `DERIVATION_REVIEW.md`. The four author mathematical sources have been freshly rehashed exact; the original final acceptance itself has been recovered byte-for-byte. No theorem premise or acceptance scope is expanded.

## Global odd source and finite inverse form

The actual process is the unchanged conservative reversible diffusion with potential v(y)U(z), constant mobility diag(1,M_z), M_z>=mu I, unit longitudinal mobility, and the exact full Gibbs|A law once. Smoothness, quartic coercivity and the already received proper Lyapunov function earn the actual global process. With Z_U=int exp(-beta U), w=exp(-beta vU)/Z_U has marginal q=v^-alpha, and all M,S0,R/current formulas use that same scale.

Reflect the accepted left-half current by J_ref(x)=-R0 J(R0x), R0=diag(-1,I). Its longitudinal component matches at zero and its transverse components reverse; its divergence is -w1_B on the right. Since the inverse block mobility commutes with R0, norms match. The complete signed-source price is therefore beta[M²Rplus+2E_rest]: one full slab, two complete wells. The odd residual r=psi-(1_A-1_B) is supported in S, with nonnegative left half and opposite right half. Its cumulative flux starts and ends at zero and is at most S0/2; conditional dilation and the integrated slab bound give B_r=beta(S0/2)²R(1+C_s).

Both sources have zero global mean. Compact-core distributional integration and finite weighted current resistance give |<f,g>|²<=B_f E(g,g), likewise for r. The global form closure extends these inequalities to resolvent tests. For a>0 and g=(K+a)^-1 f, Q_f(a)=E(g,g)+a||g||²<=sqrt(B_f Q_f(a)), hence Q_f(a)<=B_f. Monotone spectral convergence earns the global inverse forms without a gap, a bounded global inverse, or a pointwise infinity flux limit. Triangle inequality for K^-1/2 gives Q_psi<=(sqrt(B_f)+sqrt(B_r))². The weighted Cauchy upper in the source is valid; its excess is (eta/2)(sqrt(b_f)-sqrt(1+C_s))².

The bounded scalar psi is globally in the form domain, has zero mean by symmetry, N in [2M,Ztot] and energy 4/(beta R). Constants are in the finite-mass form domain by cutoffs, and zero energy on connected Euclidean space forces a constant, so the mean-zero generator is injective. With k=2/T0, its normalized spectral moments satisfy EX=2M/N<=1 and E(1/X)<=1+epsilon. The accepted scalar lemma and self-adjoint semigroup identity give the whole-vector bound sqrt(epsilon). Thus correlation rate is 2/T0 and flip rate is 1/T0, with no factor-of-two transplantation from a killed process.

## Actual stationary augmentation and committor

Irreducibility/local ellipticity and the constant-only invariant kernel give ergodicity of the finite invariant law. A two-sided stationary path visits both positive-mass basins arbitrarily far in the past; its last-visited-basin label is well defined and jointly stationary. Continuity and the unit separation of the basins imply finitely many full crossings on each compact time interval, but do not by themselves imply finite expected count.

Minimize the global form over functions 0 on A and 1 on B. Clamping a minimizing sequence to [0,1] preserves constraints and bounds its L2 norm by finite mass. Bounded energy and weak compactness in the Hilbert form domain, closed convex constraints and lower semicontinuity give a minimizer. Equality in the convex energy minimization and the constant-only kernel give uniqueness. The scalar trial bounds its energy cap by C0=1/(beta R). Local elliptic regularity gives a harmonic representative on S and smooth local one-sided traces at the flat boundaries; its constant extension is continuous and locally piecewise smooth. Stationary recurrence/disintegration gives finite basin hitting for almost every start. Bounded stopped harmonic martingales, compact localization and nonexplosion identify the minimizer with the actual committor q_B. Positive-time local densities remove exceptional regular interior starts if desired; almost-everywhere identification already suffices for the stationary and dominated path laws here.

This earns a genuine finite-variation boundary decomposition, not merely the name of a Fukushima zero-energy term. Generalized Itô–Tanaka on compact stops gives q_B(X_t)-q_B(X_0)=M_t+C^A_t-C^B_t, with continuous boundary-supported local-time FV terms. Its martingale bracket is 2 int Gamma(q_B)dt. The signed generator charges are positive at A and negative at B by the local maximum principle.

The unbounded fibers are controlled globally: choose nonnegative compact cutoffs chi_R increasing to one, E(chi_R)->0. Test the local distributional identity with chi_R q_B and chi_R(1-q_B). Their cutoff cross terms are bounded by sqrt(cap E(chi_R)); the principal energy term tends to cap. Monotone convergence of the nonnegative charges proves that each total boundary charge is cap. No uniform derivative bound at infinity or artificial boundary is assumed.

## Count identity and conditioning

For the actual stationary last-visited label L in {0,1}, let F_t=(q_B(X_t)-L_t)². At every completed opposite-basin hit it jumps from one to zero, contributing exactly -1. On local-time supports q_B equals the current retained label. The predictable previous label differs only at locally finite switching instants, which continuous local-time measures do not charge. Thus boundary FV terms vanish in the square identity:

    F_t-F_0 = 2 int (q_B-L)_(u-) dM_u
              +2 int Gamma(q_B)(X_u)du -N_t.

Stationarity and finite energy give expected energy t cap/Ztot, and the stochastic integral has expected bracket at most 8t cap/Ztot. Compact/count stopping first earns finite stopped expectations; Fatou establishes count integrability before unstopped expectations are used. Alternatively, the localized martingales converge in L2, energy in L1 and bounded F terms by domination, yielding the same count convergence. Augmented stationarity cancels the endpoint expectations and gives exactly E_pi N_t=2t cap/Ztot<=(1-s)lambda t<=lambda t.

The stationary augmented law has masses (1-q_B)pi and q_B pi for the two labels. Its conditioning on X0 in A is precisely the once-only full Gibbs|A forward experiment with label A. That *entire future-path law* is dominated by C=Ztot/M times the stationary one. The stationary count equality is not asserted under conditioning, nor is an entrance distribution assumed to be Gibbs.

## Full paths, waits and scope

The finite-record entropy argument conditions on actual histories but uses only unconditional deterministic-time density domination. It gives the stated KL/Pinsker error with the full initial Gibbs|A law. H and the binary total sign differ only in S, costing n eta on n later grid points. An initial nonanticipating classical mark can be retained by conditioning that argument on the mark and averaging; the comparison chain may be independent of it. This is not a postselection-uniform or adaptive-control result.

Stationarity and the L1 slab comparison give sign correlation <=exp(-2x)+epsilon+2s. Two endpoint retained-label mismatches give retained odd-flip probability >=(1-exp(-2x))/2-epsilon/2-3s. Since 1{N>=2}<=(N-1{N odd})/2, the actual stationary multi-jump probability is at most (x²+epsilon/2+3s)/2. Its conditioned whole-path probability is multiplied by C. The comparison CTMC separately costs n x²/2 for multi-jump bins. Maximal grid coupling followed by actual conditional path kernels therefore gives formula (13), including 5n eta/2, and matches same-order jumps in each bin within Delta. Deterministic jump atoms are absent by densities, or by stationary finite intensity and domination. Piecewise-linear matching of jump times gives the increasing time change. No continuous timestamp-vector TV is implied.

At fixed scaled horizon H, x=H/n of order epsilon^(1/4) makes all failure terms vanish, with C bounded and eta exponentially small. Uniformity is over the admitted fixed-floor angular/mobility class. For the first j waits, pay P(Poisson(H)<j); successful timestamp matching gives first wait error x and later increment error at most 2x. For each joint wait-CDF, one-sided exponential threshold strips cost at most 2j x. Choose H large first and then alpha large to obtain the finite-j renewal limit. It is not exact iid at fixed dimension or an unbounded-moment guarantee. Same-direction output cycles still include the intervening return and are sums of two reference exponentials.

## Narrow supplements

The accepted sharper storage theorem applies here with **zero added processing** on the actual global mean-zero self-adjoint semigroup. Its weak projected identities and energy storage are exact for u'= -Au; e need only lie in the form domain. Both chronological orientations coincide. This admits G(epsilon)=0.5sqrt(epsilon(1+epsilon))+epsilon/EulerNumber, with the 3/8 upward rational coefficient. No nonzero stirring or autonomous/nonreversible capacity-count extension is accepted by this baseline receipt.

The midpoint interval gives lambda in [(1-d)lambda_star,(1+d)lambda_star], physical deterministic Delta=x/lambda_star and all-time correlation-rate error <=3d/[8(1-d)]. Rate uncertainty is charged twice where logically needed: in the sign-vector/grid bound, and separately as the count drift C n d x. The actual cluster bound is at most d x+x²/2+epsilon/4+3s/2, giving F2 exactly. The dynamic program counts sampled endpoint changes, not hidden completed jumps, with O(n(U+2)) finite-state arithmetic plus bit/enclosure costs.

The no-gap supplement is valid: scalar tail cutoffs have variance order R^(1-4alpha) and energy O(R^(-1-4alpha)); subtracting their negligible mean gives Rayleigh quotient O(R^-2). Fixed finite transverse cutoffs earn form membership. Injectivity on mean zero therefore coexists with zero spectral bottom.

All numerical receiving, physical preparation, sensor/exposure/hardware, arbitrary adaptive schedules, relative-tail guarantees and novelty remain excluded. This recovery rendering supplies no additional theorem beyond the exact original acceptance.
