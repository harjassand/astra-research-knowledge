# Quadratic realizable net error and a finite exact learner
2026-10-29. Addendum to GAP_FREE_ONLINE_THEOREM_v1.md; author derivation, pending review. It improves the net size and supplies an exact finite-arithmetic option. The v1 expected cumulative theorem remains useful; no high-probability or complete large outer-code execution is silently added.

## Quadratic approximation without a source excitation gap
For every current reduced source Kraus K_a, the true twisted swap S_* commutes with K_a. For any candidate S_C,
 delta(C)=(1/(2D))sum_a ||[K_a,S_C]||F²
         =(1/(2D))sum_a ||[K_a,S_C−S_*]||F²
         <=2||S_C−S_*||op² <=(9/2)||C−C_*||F².
Thus replace v1's comparator term3epsilon T by(9/2)epsilon² T. Taking epsilon=T^(-1/4) still gives O(sqrtT) comparator cost, while M=O(T^(3/4)), not O(T^(3/2)). This uses the exact common-algebra promise, not an estimated gap or independently distributed errors.

## One rational quaternion chart suffices for rotations
Represent any rotation by a unit quaternion q with q0>=0, using q and−q equivalence. Its stereographic coordinate u=q_vec/(1+q0) lies in the unit ball. Choose integer grid k in[-m,m]^3 and u=k/m. The inverse chart is exactly rational:
 q0=(m²−|k|²)/(m²+|k|²), q_vec=2m k/(m²+|k|²).
It is unit length exactly. Euclidean quaternion distance is at most2 times the u-distance; nearest grid point gives distance<=sqrt3/m. Rotation Frobenius distance is at most2sqrt2 times quaternion distance, hence <=2sqrt6/m. Choose m>=2sqrt6/epsilon (an integer conservative choice m=ceil(5/epsilon) avoids an irrational threshold). The net has at most M=(2m+1)^3 candidates. Matrix entries are rational with denominators dividing D_k², D_k=m²+|k|²<=4m². Duplication is harmless.

## Exact multiplicative weights, with all arithmetic and sampling charged
The actual swap-loss estimator lies in[-87/4,93/4]. Shift/scale it:
 fhat=(hatdelta+87/4)/45
     =[10−yz C_ab(1+9uv C_cd)]/20 in[0,1].
For a probe role of probabilityp, use fhat/p; on a service round use0. Its conditional mean is f(C)=(delta(C)+87/4)/45. The additive baseline cancels in regret. For rational eta<=p/2, update integer/rational weights by
 w_(t+1)(C) proportional to w_t(C)[1−eta 1[probe] fhat(C)/p].
All factors are positive. The elementary inequalities log(1−x)<=−x and log(1−x)>=−x−x² for0<=x<=1/2 give, for every comparator,
 E sum_t delta_t(C_t) <=(9/2)epsilon²T +45[logM/eta+eta T/p].
Choose a dyadic rational eta within a factor two of min(p/2,sqrt(p logM/T)); a rational conservative approximation to the logarithmic threshold suffices. The estimate is O(sqrt(T logM/p)+logM/p), with larger constants than signed exponential weights.

For an entirely exact finite implementation, let L=20[((4m²)!)^4]. It is a common denominator for every fhat because each denominator divides20D_k^4. If p and eta are fixed rationals, clear their denominators once as well. All weights can be held as integers with the common factor denominator cancelling after each update. Their bit length grows at most O(T logG), where G is that fixed common update denominator; logG=O(m²logm) plus bits of p,eta. This is polynomial in the declared horizon, but impractically large and is not a practical-runtime claim.

Sample the current integer weights exactly by drawing a uniform integer in[0,sum weights−1] through binary rejection. One attempt succeeds with probability>1/2. Cap the number of attempts per edge/round at r, and abort if the cap is reached. The total added failure probability is at most(n−1)T2^(-r). The bit cost per attempt is the actual bit length of the weight sum. Private role coins and physical permutation keys have separate budgets. Exact rational rotation descriptions do not remove the need to synthesize their physical single-qubit controls to a declared finite accuracy.

## More efficient arithmetic option, not yet the governing executed implementation
Signed exponential weights need only the cumulative integer X00 and Xcorr sufficient statistics per edge: each candidate score is a quadratic form in its rational entries. Ideal probabilities can therefore be recomputed from exact scores rather than recursively rounding tiny weights. Subtract the minimum score, truncate exponentially small tails and approximate remaining exponentials by certified rational intervals, producing a dyadic distribution within prescribed TV. Sampling it adds a bounded expected-loss error because losses lie in[0,2]. This avoids huge integer weight products and is polynomial with smaller bit costs, but requires its own executable precision/sampler receipt before use as the compiled kernel.

The first numerical quantum-memory fixture uses floating signed exponential weights on a small rational net containing the true frames, and labels that scope explicitly. A separate exact-rational small-kernel check supplies evidence for the arithmetic formulas, not a claim that the larger physical run used exact integer sampling.
