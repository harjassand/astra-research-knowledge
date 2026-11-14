# Stronger analytical renewal core: box63

This changes only the set used in a proof of hard-source excursion occupation. It does not change the original model, target, source definition, acquired box18 proposal, or clock.

Let A63 comprise configurations whose augmented plus components each fit a contractible63×63 box. Reuse the hard-source renewal identities and first-exit argument of RENEWAL_CORE_EXIT.md.

## Core normalizer without assuming a new sampler
For a finite polymer of physical perimeter P, area≤P²/16; for box63 also area/P≤63/4. Hence E≥7.9P for P≤40 and E≥7.37P for all P. P4 has one singleton shape per site; P6 has two dominoes; P8 has at most nine anchored shapes (this deliberately counts both diagonal pairs). Their weights are bounded by (10/27)^31, (10/27)^47, (10/27)^63 respectively.

The perimeter injection has at most n128^P codes. For counting, choose the bounding-box southwest corner as anchor, even when it is not an occupied cell. Each cycle's start-cell offsets are nonnegative. Four128-letter symbols provide16 header bits, sufficient to encode the cell plus physical side whenever4b²≤65536. Thus it covers box63, and also the127-wide components needed below. The direction and cycle-end parts of the code are unchanged. Canonical ordering/orientation and winding reconstruction distinguish polymers; the counting anchor need not be the sampling implementation's occupied anchor.

Discarding compatibility gives Z63/w(a)≤expΓ63, where

Γ63 ≤ n[(10/27)^31 +2(10/27)^47 +9(10/27)^63
         +(1/21)^10/(1−1/21)+(1/12)^42/(1−1/12)]
      <2.698e−7.

The first geometric tail overcounts P10..40 and beyond; the second covers all P≥42. Physical perimeter is even, so no P41 case is omitted. The bounds128e^-7.9<1/21 and128e^-7.37<1/12 are certified by finite rational Taylor sums. All small-P exponent comparisons are similarly checked.

Therefore the entire hard-source core excursion occupation contributes less than2.7e−7 to N*/w(a).

## First departure
An addition leaving A63 joins old box63 components at a gate. Aligning each touching component to that gate confines their union to[-63,63]^2. Its new component S has each side≤127<L, and at least one side≥64. Thus P(S)≥2(64+1)=130 and area/P≤127/4, giving E(S)≥6.73P.

The bbox-anchored header needs4·127²=64516<65536 labels. Hence the total weighted new-component envelope is

T63≤n sum_{P≥130}(128e^-6.73)^P
   ≤n(2/13)^130/(1−2/13).

Pay all16129 possible gate sites in S. The same detailed-balance injection into an unaffected A63 configuration yields Flux(A63,A63^c)/Z63≤16129T63. Consequently

P_uniform-singleton(exit A63 before a or B)
 ≤ [1/(1−Γ63)]·16129T63·(1+e^31.96)/n
 <10^-86.

`renewal_box63.py/json` executes exact rational checks, conservatively replacing e^31.96 by3^32. Its rational upper is about7.402e−87. No new stochastic run is used to obtain this probability bound.

## What a duration bound would now suffice to prove
Let M uniformly bound E_x τ_{a∪B} over actual first-departure states x, INCLUDING all thermal companion components. By the strong Markov property, total outside-A63 occupation during a singleton excursion is at most p_exit M: all such occupation follows its first departure, even if it later re-enters and exits repeatedly. Also λ_a<10^-7. Thus M≤10^90 would imply the outside contribution to N*/w(a) is below10^-3, in addition to the2.7e−7 core contribution.

This is a sufficient target, not an established estimate. A small barrier path does not establish M without entropy/congestion or a valid drift certificate. Native clocks, first-majority target, the integer critical side400, and all companion components must be retained. No full mean-time result is claimed.
