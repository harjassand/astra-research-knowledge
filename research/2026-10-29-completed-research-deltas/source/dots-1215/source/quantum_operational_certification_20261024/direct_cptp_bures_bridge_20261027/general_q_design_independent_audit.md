# Independent audit — separate general-q state-design extension

27 October 2026. Auditor: `producer-workspace/independent_bures_bridge`.

**PASS.** This audit concerns only `GENERAL_Q_DESIGN_ADDENDUM.md`; it does not modify the frozen qubit proof or an older multilevel receipt. No full quantum circuit has been executed and no historical novelty is asserted.

## 1. Explicit weighted design works in every q

For `Q=4^a` with `q<=Q<4q`, evaluating a uniformly chosen cubic at any d≤4 distinct field points gives a uniform vector in `GF(Q)^d`. The d-by-4 evaluation matrix contains an invertible d-by-d Vandermonde minor. This argument is valid in characteristic two: distinct evaluation points have nonzero pairwise differences, and no derivative argument is needed.

Applying any surjective binary-linear map to two coordinates preserves independence and makes those two bits uniform. Any bijection to fourth roots consequently produces four-wise independent uniform phases. The choice of phase bijection need not respect field addition.

In `E[z_a z_b conjugate(z_c z_d)]`, each distinct coordinate has exponent in `{-2,-1,0,1,2}`. Uniform fourth roots have zero expectation at all these nonzero exponents. Thus the moment equals one exactly when the positive and negative index multisets agree. There is no mistaken third-moment or Haar-phase assumption. The all-equal term appears once, giving `(I+F-Delta)/q²`.

Computational states with total weight `1/(q+1)` contribute `Delta/[q(q+1)]`; the phase ensemble with total weight `q/(q+1)` contributes `(I+F-Delta)/[q(q+1)]`. Their sum is the exact projective 2-design moment. Duplicate labels remain harmless when their weights and banks are counted separately. The construction requires neither prime-power logical dimension q nor complete mutually unbiased bases.

Field construction itself can be made polynomial in q: even enumerating the O(Q) monic degree-log₂Q binary candidates and testing irreducibility is a polynomial-q procedure. Enumerating all Q⁴ phase labels is likewise polynomial in q, though very inefficient in log₂q.

## 2. Full-CPTP loss and resource cap

The state-2-design identity gives `Favg=(q F_e+1)/(q+1)` for any TP q-dimensional channel. Hence `b_q=(q+1)/q` times average state infidelity is exactly entanglement infidelity. The effects `b_q(I-D†P_l)` lie between zero and `b_q I`, uniformly for every CPTP decoder. The weighted direct-sum Uhlmann argument is unchanged, with direct-sum weights `sqrt(w_l)`.

Two transfers yield the exact same optimization dependence and constants `32b_q m/gamma+4eta/gamma`, bounded by the qubit constants because `b_q<=3/2`. This optimizes one compatible full CPTP decoder, and therefore does not inherit the factor-two witness loss of the earlier separately optimized phase-POVM route.

Choi rank≤R implies common output support≤qR and every pure-input output rank≤R. With `k=min(s,qR)`, `r=min(R,k)`, and `D<2kr<=2qR²`, each bank needs the same `O(D log(2D)/(gamma epsilon))` expected-risk copies. The `M=q+Q⁴=O(q⁴)` bank count gives the stated, deliberately loose `O(q⁵R² log(2qR)/(gamma epsilon))` deterministic acquisition cap. All-bank-plus-datum reduction, reference extension, separate homogeneous purification, consumed programme and finite-error qualifications are exactly the received qubit interfaces with the label count enlarged. The all-estimate union bound is `2DM exp(-nm/(80D))`, agreeing with the proposed high-confidence count.

For a known k-dimensional output space, r=k suffices without a source rank promise. Six logical-qubit inputs and `D<2k²` give `O(k² log(2k)/(gamma epsilon))` source calls. This fixed-frame corollary needs no outer random reduction. The final added paragraph correctly permits reuse of the classical learned CPTP decoder on future independent data in that known physical space, with its ordinary training-confidence qualification. The quantum bank is still consumed. This does not give reusable compression or latent-frame alignment in the unknown-support theorem, and it does not automatically upgrade an existing adaptive encoder, approximate-support, or validation theorem.

## 3. q-dependent SDP repair is genuinely polynomial

The Choi dimension is qk, the TP constraint is `Tr_out C=I_k`, and the strict point has minimum eigenvalue `1/q`. The stated coefficient bounds are correct:

`0<=H<=b_q I`, `Tr H=b_q(q-1)`.

The latter means qubit-specific operator-error debits cannot be copied without their q factors. The addendum expressly requires those factors. Here is an explicit sufficient scaling, showing no hidden source condition number:

- Let `b=b_q`, `0<eta<=1`, `lambda=eta/(8b)`.
- Start with a Hermitian weak primal whose minimum eigenvalue is at least `-kappa`, TP residual norm at most kappa, and sufficiently small initial primal/dual gap, where `kappa<=eta/(128bq)`.
- Correct TP using `C1=Ctilde-(Tr_out Ctilde-I) tensor I_q/q`. Its minimum eigenvalue is at least `-(1+1/q)kappa`.
- Mix with `lambda(I_k tensor I_q/q)`, then round to Hermitian operator error `e<=eta/(128bq)` and repeat the TP correction. Because partial trace has operator norm at most q, the rounding-plus-repair error is at most 2e.
- The final minimum eigenvalue is at least `lambda/q-(1+1/q)kappa-2e >= lambda/(2q)`. It is exactly TP in rational arithmetic.
- The first TP correction costs at most `b(q-1)kappa/q` in objective. Final rounding costs at most `2b(q-1)e`. Mixing adds O(b lambda), since the fixed-point objective is `b(q-1)/q< b` and the weak primal has only the explicitly bounded negative part.
- A near-feasible dual slack `delta_dual<=eta/(8k)` is repaired by shifting Y downward by `delta_dual I_k`, with objective debit≤eta/8. Coefficient rounding norm≤eta/(8k) costs≤eta/4 for the two optimization comparisons.

With an initial gap≤eta/8 these stated smaller tolerances leave total debit safely below eta. All tolerances have inverse-polynomial dependence on q,k,eta. A Kraus rank at most qk gives a Stinespring output dimension at most q²k, as claimed. Finite known-state preparation and finite gate synthesis must still be paid; none is an unknown-source operation.

## 4. Independent checks

The author's exact enumeration script was read and replayed successfully for q=2,3,4,5. The independent script uses a separate polynomial-long-division field multiplication routine, a different two-bit projection, and a different phase bijection. It reports:

- 3,483 exact finite-field Vandermonde rank checks, including 17 evaluation points in GF(64);
- 255 exact four-wise projection-count checks for nine coordinates in GF(16);
- 256 exact fourth-moment multiplicity-pattern checks;
- finite full weighted-design average-fidelity checks at q=2,3,5,6,9, including non-prime-power q=6, with residual at most `1.2e-16`;
- q-dependent affine TP/margin checks through q=9, with TP residual at most `2.9e-16` and the prescribed positive margins satisfied.

These support the algebra but do not execute Schur compression, purification, the complete decoder learner, or final synthesis. The all-q conclusion is the Vandermonde/moment proof, not extrapolation from numerical tests. No cardinality optimality, practical advantage, generic-noise scalability, or reusable unknown physical frame is claimed. Polynomial q and R can both mean exponential dependence on qubit counts.
