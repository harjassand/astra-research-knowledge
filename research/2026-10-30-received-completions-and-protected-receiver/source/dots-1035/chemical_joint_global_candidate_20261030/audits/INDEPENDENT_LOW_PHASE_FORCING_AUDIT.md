# Independent audit: exact low-phase forcing and extreme-composition closure

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal mathematical review. Reviewed EXACT_LOW_PHASE_FORCING_CLOSURE.md.

## Verdict

The explicit global function F, its exact low-phase Poisson identity, sharp clearing-return bounds, and both extreme-composition drift inequalities pass. This is actual boundary-feedback control, not a frozen or stationary average. No recurrence theorem follows from the covered sectors alone.

## 1. Exact recursion and norm-likeness

At B=b<4 the only enabled channels are immigration, at rate 1 and shift (A,B)→(A+1,B+1), and activation, at rate ab and shift (A,B)→(A+2,B+3). Both leave C fixed. First reaching B≥4 takes at most four jumps, and each holding rate is at least one. The displayed descending recursion is exactly the first-step equation for expected terminal V0 plus accumulated running cost V0. Multiplying by (C!)^alpha gives LF=−V0 exactly at every low-phase state, including a=0 and b=0.

The terminal B count is at most 6 and A increases by at most 8, so the stated factorial upper bound follows from at most four expected holding-time contributions and one terminal contribution. Backward induction also gives f_b(a)≥(a!b!)^alpha: both future baseline factorial values are at least the current one, and the added running cost is positive. Hence F≥V0 and is norm-like globally.

## 2. Sharp recursion asymptotics

For b=3, activation's target is ((a+2)!6!)^alpha and its probability tends to one. The immigration branch is even smaller than the claimed O(a^(alpha−1)) relative error. For b=2, the already solved immigration target f_3(a+1) has one additional A factorial factor relative to activation, while its probability is O(1/a); the relative error is therefore O(a^(alpha−1)). The same argument gives b=1. Repeated immigration subbranches are successively smaller because alpha<1. The running-cost and activation-probability errors are also bounded by this error order.

At b=0 the exact identity f_0(a)=(a!)^alpha+f_1(a+1) adds a relative O(a^(−3alpha)) term to the activation/return asymptotic. Thus delta=min(1−alpha,3alpha)>0 is correct.

For B=4 and A≥3, substitution a=A−3 yields return ratio 1+O(A^−delta), so the positive clearing contribution divided by F is at most C(B)_4 A^(3−delta) for large A. For B=5,6,7, substitution in the b=1,2,3 formula gives the more precise ratio (AB)^−alpha[1+o(1)], which is eventually below one. At B≥8 both values are baseline factorials and the ratio is [(A)_3(B)_4]^−alpha≤1 whenever clearing is enabled. Finitely many remaining A values at B=4,...,7 are absorbed in a fixed constant. This proves the claimed uniform bound over all B≥4; C cancels from every ratio.

## 3. Extreme-composition fast drift, including endpoints

When 1≤A≤C/M and S is large, the increasing-A ratio is at most (2/M)^alpha. Choosing M sufficiently large makes its contribution at most a fixed negative multiple of C³, because its rate includes 6(C)_3. The positive decreasing-A contribution is bounded by a constant times

    C^(2+alpha)A^(1−alpha)
     +C^(1+alpha)A^(2−alpha)+C^alpha A^(3−alpha).

Relative to C³ these are powers (A/C)^(1−alpha), (A/C)^(2−alpha), and (A/C)^(3−alpha), all tending to zero as M increases. At A=0 the decreasing rate is zero and the increasing ratio C^−alpha tends to zero directly.

The reversed cone is analogous: the decreasing-A rate contains (A)_3, its ratio is small, and the increasing-A positive terms are bounded by powers of C/A with strictly positive exponents. At C=0 the increasing rate is zero and the decreasing ratio A^−alpha tends to zero. Therefore a fixed negative multiple of S³(B)_4 is valid uniformly in both cones for large S, including small nonzero minority populations.

## 4. All connector feedback is lower order there

Immigration has positive ratio at most ((A+1)(B+1))^alpha. Activation has rate AB and positive ratio at most [(A+1)(A+2)(B+1)(B+2)(B+3)]^alpha. Dividing by (B)_4, the B factors remain uniformly bounded for B≥4: the largest power is B^(1+3alpha−4), with alpha<1. Hence both are bounded by C(B)_4[1+A^(1+2alpha)] before comparison with fast drift.

Both exponents 1+2alpha and 3−delta are strictly less than three. The actual clearing return and both upward connector contributions are therefore uniformly absorbed by the negative cubic fast term after enlarging S0. This verifies the asserted sector inequality with the globally defined F, not merely with a function specified separately in each region.

## 5. Additional compatible bulk region already earned

If the same alpha is chosen within the previously proved single-linkage primal bulk interval, the present F also inherits that bulk inequality without a new gluing construction wherever B≥8 and A,C,B satisfy the prior high-count bulk cutoff (outside its finite class exception set). At such a source every reaction target has B≥4, so F and V0 agree both at source and at every target, and LF=LV0 EXACTLY. The present construction works for every alpha<1, so taking the common sufficiently small bulk alpha is compatible and does not create a new parameter circularity.

This observation does not fill the remaining balanced-composition region at bounded intermediate B, nor the B-large region with small A,C. It only records that the accepted bulk sector, the two extreme-composition sectors, and all B<4 already coexist in one explicit F when that common alpha is selected.

## Scope

The fast term can remain positive in the balanced cone, especially after leading clearing loss is canceled by the B=4 return. Global recurrence, compatible remaining-region repair, and control of any feedback caused by that further repair remain unproved. Prior failed adjoint numerical tests concern a different measure and are not reclassified as successes.

Reviewed source hash:
98a2de4688a3592fb09b681bb8fe0a0406d69bd8e5347de3950150e45412e6fd  producer-workspace/EXACT_LOW_PHASE_FORCING_CLOSURE.md
