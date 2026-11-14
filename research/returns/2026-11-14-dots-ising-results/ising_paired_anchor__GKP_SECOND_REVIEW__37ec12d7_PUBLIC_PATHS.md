# Independent second review: paired-anchor finite closure

Read RESULT.md and independently reconstructed the transfer and endpoint algebra. Reran check.py and pair_check.py; the exact R10000 negative exponent33296 and all fixed-count transfer tests passed.

## Two-column preimages

For d1<=d2, mismatch excess over the sorted pair is2n10, so its Peierls factor is t^n10. The fugacity z^(n01-n10)=z^(d2-d1) cancels exactly with z^-Delta. Bottom00/top11 force one vertical flip in each column; their combined mandatory weight epsilon²=t is correctly removed by t^-1. Swapping column names when d1>d2 is a fixed-count analytical convention, not an independently sampled binary label and requires no factor2.

For w=(1,20epsilon,20epsilon,1), KDw/w has ratios
 1+19t+(20/z)t²,
 1+t²/z,
 1/10+zt+t/z,
 1+19t+(20/z)t².
They are at most1+20t under the displayed small-t condition; Ke11<=w. The resulting positive overcount drops fixed counts only after retaining their fugacity penalty. Inter-pair mismatches have nonnegative excess over sorted-column Hamming minima. No independence assumption is introduced.

## Height and boundary penalties

The paired factor contributes at most c TV(d). Writing theta_eff=theta-c/2 yields
 E_theta-cTV=E_theta_eff-c(d1+dm).
Thus the required endpoint cost is PLUS c(d1+dm), bounded by2ch. The note pays this explicitly. Uniform-height denominator delta_eff=8/R+2c is positive; bounding its reciprocal by1+R/8 is safe. The t^-R factor and quadratic-in-R pressure20Rh exp(-16) remain in the stated bound. This does not remove the asymptotic fixed-temperature pressure problem.

## Continuation and original source

For an axial displacement L, tilted walk weight divided by original weight is(u/epsilon)^L; summing all walks is a positive overcount. Reference energy exp(8(L+2)) cancels epsilon^L, leaving exp16 and u^-L<=exp(L/999). Root/orientation and all remaining loop pressure remain charged. This uses the inherited fixed-full-column native path and its retained-boundary cancellation, not a newly assumed winding seed.

The endpoint law is bounded by Q times the ORIGINAL Gibbs weight. It is not reset to Gibbs. The combined factor4n² QJ includes anchor labels and native stages. All A, kappa, conductances, voltage and target remain unchanged.

## Union with the proof basin F

At R10000 the no-solid-anchor event is independently bounded in both no-essential phases: minus-sea outsideF by exp(-256367), plus-background by exp(-104428). The new solid-anchor bound exp(-33296) covers arbitrary source states containing the anchor, including either phase. Three positive branch bounds sum to at most exp(-33294). This concerns only the no-essential sector OUTSIDE F; original core and F\A numerator contributions are not discarded.

Combined with the already reviewed winding-sector bounds and their paid union constants, the stated all-topology outsideF bound exp(-4354) is consistent. The original-source F normalizer/downset theorem is the correct interface, not an unproved replacement of original M5 or source current.

This is a finite occupation certificate. It does not acquire C, prove polynomial W/C, construct a physical decision-time estimator, or establish the original fixed-theta uniform growing-R North Star. Frozen artifacts were not modified during this review.
