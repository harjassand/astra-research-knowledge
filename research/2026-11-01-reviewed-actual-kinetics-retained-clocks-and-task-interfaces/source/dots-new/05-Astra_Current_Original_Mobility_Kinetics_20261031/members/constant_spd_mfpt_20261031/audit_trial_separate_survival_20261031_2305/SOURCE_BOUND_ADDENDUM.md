# Independent source-bound addendum: trial and separate-current survival theorem

**Verdict: PASS, theorem-only, for the two immutable sources below.** This supplements, and does not overwrite or expand the executable scope of, `audit_survival_theorem_20261031_2256/REVIEW.md`. No correction to either new source was needed.

## Exact source boundary

- `TRIAL_RESOLVENT_TO_SURVIVAL_ROOT_V2.md`: SHA-256 `7d4d7f61e03860e11e0e550ab850714497acc6f395b5179e4f318a1739434e83`.
- `SEPARATE_CURRENT_SURVIVAL_COROLLARY_ROOT.md`: SHA-256 `5a98beb1d277777aa03016e6d56b76f29ebe52188c5fe981b0cf95c050dee7f4`.
- Prior source `RESOLVENT_TO_SURVIVAL_ROOT_CANDIDATE.md` remains SHA-256 `2414f104c0b74b59796af2f24c9a93ac5300a1a6eee7bd1137e0adef1dbfee67`.

Both new files were read in full and snapshotted byte-for-byte here. Prior review artifacts and all source files were left untouched.

## 1. Any admitted trial, not necessarily a committor

The V2 scalar lemma is the previously checked statement, with the same proof and constants. Its Hilbert-space argument needs only a trial in the actual killed form domain, with 0<=h<=1, h=1 on A, and finite energy upper bound C0. It never uses harmonicity, energy minimization, or equality of energy and capacity. Its notation `<h,Kh>` is explicitly quadratic-form notation; h need not be in the operator domain.

Let N=||h||_m^2. Then M<=N<=M+S0. For r>0, positivity of the resolvent and h<=1_D imply Q_h(r)<=Q_D(r); inverse-form Cauchy applies at every r. Monotone spectral convergence sends r down to zero. Finite source bounds control Q_h and exclude a zero spectral atom in the h measure, without requiring a killed spectral gap.

Form/inverse Cauchy gives N^2<=E_h Q_h. Consequently E_h>0 and C0>0 whenever the hypotheses hold (M>0 and Q_h finite). In particular division by k0=C0/M is legitimate, and the formula for epsilon cannot be negative for valid exact hypotheses. The normalized h spectral measure obeys the two moment hypotheses. Neither a committor oracle nor an angular sampler is hidden in this step.

The actual initial-law comparison is unchanged: e=h-1_A and d=1_D-h are nonnegative, supported on S, bounded by one. The exact unnormalized difference is `<1_A,P_t d>-<e,P_t h>`. Positivity lets one use the maximum of their two bounds, not their sum. L2 contraction and normalization give d_init=rho+sqrt[rho(1+rho)]. Thus the uniform absolute survival and CDF error follows for the exact full initial law m(.|A).

In the stated fiber application the explicit scalar slab profile has derivative -1/(Rq), and energy exactly 1/(beta R), under the stated unit y-mobility and acquired reference marginal q. The profile is bounded, has finite L2 norm and form energy and the correct killed trace; the actual receiving must still establish its killed-form-domain membership by the already required approximation. A general abstract process cannot be assigned this scalar energy without those application premises.

The V2 coupled source hypothesis remains valid only when Q_S<=rho^2 B_A has actually been earned. Improving B_A alone does not improve Q_S. The application paragraph's J_S<=rho J_A argument pertains to the original shared transport construction; it is not permission to replace its A-current by an unrelated improved one while keeping the coupled conclusion.

## 2. Independent source bounds

For separately earned finite Q_A<=B_A and Q_S<=B_S, positivity and Cauchy at positive resolvent parameter, followed by monotone convergence, give

    Q_h <= Q_D = Q_A+2 Q_AS+Q_S
        <= (sqrt(Q_A)+sqrt(Q_S))^2
        <= U := (sqrt(B_A)+sqrt(B_S))^2.

Thus E_h Q_h>=N^2>=M^2 implies C0 U/M^2>=1, proving nonnegativity of the corollary's epsilon. For X=lambda/k0 under the normalized spectral measure,

    E X=E_h/(N k0)<=1,
    E(1/X)=k0 Q_h/N<=C0 U/M^2=1+epsilon.

Every remaining V2 step is literally unchanged. B_S=0 is allowed, including a null-mass S; positivity then forces the associated cross inverse form to vanish. No positive lower bound on S0 or B_S is needed.

Substituting B_A=B_new and B_S<=rho^2 B_old gives exactly C0(sqrt(B_new)+rho sqrt(B_old))^2/M^2-1. With C0=1/(beta R), division of both B values by beta M^2 R yields exactly `(sqrt(b_new)+rho sqrt(b_old))^2-1`. The source warning against silently replacing B_old by B_new is mathematically essential and correct. This corollary proves the combining rule, not the validity or cost of any future well-redistribution current.

## 3. Acquired midpoint reference

For 0<k_lo<=k0<=k_hi and k_star=(k_lo+k_hi)/2, the mean-value theorem in the rate gives

    |exp(-k_star t)-exp(-k0 t)|
      <=[(k_hi-k_lo)/2] t exp(-k_lo t).

The all-time maximum of t exp(-k_lo t) is 1/(e k_lo). Hence the error is at most `(k_hi/k_lo-1)/(2e)`, which is at most `(3/16)(k_hi/k_lo-1)` because e>8/3. The inequality remains valid for a zero-width rate interval. The triangle inequality gives the stated total KS bound, with separately earned epsilon_upper, rho_upper and an outward square-root bound. It requires no temporal grid or finite-horizon extrapolation. If rate endpoints come from time-scale endpoints, the interval must be inverted in the correct order; a rate midpoint is not the reciprocal of a time midpoint.

## 4. Scope retained

This is all-time **absolute** survival/CDF accuracy for the specified actual killed reversible process and exact full Gibbs-type A initialization. It does not establish tail-relative accuracy, positive exponential moments, accurate relative extreme quantiles, all-start behavior, or mean stability under small-TV preparation error. The independently constructed reversible heavy-tail counterexample in the prior audit remains applicable. A separately proved initial-law TV error may be added for bounded survival probabilities, not silently for the unbounded MFPT.

The prior review's full Hilbert/form, zero-resolvent and process-receiving premises and ordinary spectral/variational prior credits remain in force. The finite source-current construction, same-measure normalization, raw input admission, mobility and noise model, time-homogeneous model validity, and all outward arithmetic must be established by the actual receiving. A bound on an unrelated mean is not a substitute for an inverse-form/current bound.

No candidate code, numerical KS value, work budget, finite-bit sampler, physical preparation, control or hardware implementation is accepted here. No new generic exponentiality or historical novelty claim is made.

## 5. Check artifacts and preservation

`check_separate_source.py` supplies independent exact symbolic normalization/midpoint checks and finite weighted reversible killed-chain fixtures with independently loosened A and S inverse bounds. Trials include nonharmonic profiles, h=1_A and h=1_D. General infinite-dimensional and all-time statements are justified by the proof above, not by fixture enumeration. `CHECK_RESULTS.json` records the completed assertions and `AUDIT_SHA256.json` binds all new artifacts. Source hashes are rechecked at completion.
