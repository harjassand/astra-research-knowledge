# Independent receiving: fixed-effect full-decoder odd branch

28 October 2026. Reviewer: `producer-workspace/audit_count_pilot_fresh`.

**PASS, with the canonical/fixed-slice boundary preserved.** Reviewed source SHA-256 `433e0b0ce9b0361968d73cb7de060fae7f24dda7c03f410d466876d105c31077`, file `ordinary_fixed_effect_decoder_positive_cost_geometry_20261028.md`. No author source was edited. This is receiving of a known-matrix optimization branch, not source acquisition or a generic full-decoder oracle.

## 1. Full-CPTP slice and exact positive cost

Block positivity with diagonal blocks A and I-A is equivalent to `B=sqrt(A) K sqrt(I-A)` for a contraction K, including singular supports. The Choi partial trace is exactly I, so this is a full CPTP slice, not a rank-one or entanglement-breaking restriction. With `M=sqrt(I-A)W_10 sqrt(A)=L S R*` and `K=-R V L*`, cyclicity gives `2 Re Tr(W_10 B)=-2 Re Tr(SV)`. Hence the displayed cost is exactly `m+2Tr[S(I-Re V)]`. Since V=I is feasible and W is PSD, m is at least m0. No inverse source or unknown frame is acquired in this calculation.

For nonnormal V, both `V*V<=I` and `VV*<=I` hold. Thus `X^2+H^2=(V*V+VV*)/2<=I`, with X=Re V,H=Im V. For E=I-X, `H^2<=2E-E^2<=2E`. This is genuinely noncommutative; it does not require simultaneous eigenvectors. The even/odd numerator decomposition and its factor 2 are valid in the realified Hilbert norm. The even branch is an actual one-sided effect problem, not diagonal coordinates. The odd deterministic H is admissible for the covariance relaxation and has `m+Tr(SH^2)<=u(V)`.

## 2. Gaussian covariance and finite probability

For any supplied feasible rational covariance, the matrix Gaussian has variance rho=E G^2<=I. Its PSD quadratic numerator has mean s and second moment at most 3s^2. Paley-Zygmund therefore gives numerator at least s/2 with probability at least 1/12. The cost event follows by Markov, including the exactly zero-cost case. No independence of these events is used.

I independently read [Tropp's primary preprint, Theorem 4.1](https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf), printed page 14: the Hermitian Gaussian operator-norm bound has prefactor 2k and variance `||sum A_l^2||`. Applied to a covariance factor it gives the stated norm event. The integer R is conservative. Subtracting two failure probabilities 1/48 leaves at least 1/24; subtracting the coupling failure 1/96 leaves 1/32. This is not an empirical concentration claim.

The covariance body has bounded trace, rational moment maps and a known strict center. Its perspective fractional SDP is a conventional finite known-matrix optimization. The rounding theorem itself takes a supplied feasible covariance, so it does not need an exact optimizer or a numerical source oracle.

## 3. Polynomial completion and all-history feasibility

For Hermitian H of norm at most 1/2,

`V_±=I-2H^2 ± iH`,

`I-V_±*V_±=3H^2-4H^4>=0`.

Both signs have the same even part and the same positive cost `m+4Tr(SH^2)`. Their numerator average is the squared common affine part plus `||L0(iH)||^2`, so one sign retains the odd numerator regardless of the offset. This is an exact polynomial completion, not an approximation to a unitary or an assumed positive-completion oracle.

For the finite coupled matrix, the root-norm triangle inequalities yield numerator at least s/8, cost at most 96q+m/8 and norm at most R+delta. With H=Gtilde/(4R), the norm certificate has strict slack on the favorable event. The actual ratio is at least

`s/[128R^2 m+3072q+4m] >= s/[256R^2 m+3072q]`.

The final relaxation factor and fixed-trial failure bound therefore follow. Exact rational PSD certification ensures feasibility on all returned histories; failed trials fall back to V=I. A tiny m or s increases precision bits, not a reciprocal-small-cost trial count. The finite Gaussian coupling is imported only from the separately received binary-POVM Section 4 contract, with its receipt manifest reverified. No discrete/continuous total-variation approximation is asserted.

## 4. Exact independent evidence and boundary

The companion `fixed_effect_and_one_sided_rounding_statistics_check_20261028.py/.json` contains 12 exact rational full-CPTP slice/completion checks, including a singular A, complex polar frames, exact cost and TP identities, and principal-minor PSD certification. A separate nonnormal contraction checks the Re/Im inequality without commutation. Exact finite Gaussian tail constants and extreme-precision inequalities are also checked. No random matrix draws, source calls, SDP solves or hardware operations were performed by this review.

The canonical output V is rational and feasible. Transferring arbitrary rational A,W through their square roots and polar factors and returning an exactly rational full Choi matrix still needs the expressly missing conditioning/precision ledger. This review does not replace that gap with exact floating eigenvectors. The source's exact mathematical fixed-slice transfer is sound, while its finite algorithm is accepted only for the supplied canonical rational instance. The effect A is not optimized. The later one-sided-effect result can supply the canonical even branch but still does not solve moving-A optimization or establish a new source-query rate. All routines are available to the strongest equally informed conventional learner.

No unresolved load-bearing objection remains at this scoped boundary.
