# Independent global compact-potential / negative-mass receiving audit

2026-10-26. Analytic PASS for `GLOBAL_COMPACT_POTENTIAL_COMPLETENESS.md`, `FINITE_NEGATIVE_MASS_TO_PAID_DISTANCE.md`, and `EFFECTIVE_NEGATIVE_MASS_RECEIVER.md`. This audit reuses the previously received signed canonical L1 stress, actual finite-tree value/closure theorem, and positive-accuracy reward oracle. It does not replay fitting searches or receive any numerical small-negative-mass proposal.

## Global compact completeness

For feasible S*, T=S*−S0 is compactly supported and DivDiv-free. Compactly cut off quadratic tests recover EVERY matrix integral entry, so integral T=0 (not just trace). The deviatoric B=T−tr(T)I/3 retains zero integral and J-nullity because tr J=0. Componentwise Newton inversion gives trace-free/J-null H and DivDiv H=−tr(T)/3, hence K(H)=T, distributionally. No compact-support inverse is asserted.

Mollification gives S0+T_epsilon=S* convolved with rho_epsilon plus the L1 difference S0−S0 convolved with rho_epsilon. Positive convolution and the nuclear-norm Lipschitz bound for negative spectral trace prove the stated negative-mass limit. This step genuinely uses the received L1 S0, not an arbitrary singular seed.

Zero monopole permits subtraction of the Newton kernel at x. Compact source support and bounded first absolute moment give H=O(r^-2), DH=O(r^-3), D²H=O(r^-4), uniformly for small mollifier radii. On the cutoff annulus, K(H_epsilon)=0; the only discrepancy terms contain cutoff derivatives. They are O(R^-4) over volume O(R³). Thus L1 error O(1/R) is correct. Multiplication by a scalar cutoff preserves both algebraic potential constraints.

Conversely exact total signed trace3/4 bounds nuclear variation by3/4+2N. Vague subsequential compactness needs no assumed tightness. N→0 forces positivity; compact-test endpoint/J identities pass. The convex support-function barrier has bounded Hessian and quadratic/linear function/gradient growth. Its Hessian is positive definite at EVERY point outside E because violating normals form an open spherical patch. Large cutoff tests have uniformly bounded Hessian errors on remote annuli, whose pairings tend to zero against the finite LIMIT stress. Hence its positive mass vanishes outside E. Compactly supported quadratic tests then recover trace3/4; no missing escaped activity remains.

Rational finite-dimensional trace-free/J-null polynomial potentials with a larger compact cutoff are C²/L1 dense as asserted. This is global-potential completeness, not support-constrained compact surjectivity inside E.

## Finite negative mass to actual paid-closure distance

For a signed matrix measure, use a common dominating measure and its measurable spectral P−Q decomposition. J:P=J:Q. If c>=0, a fixed negative J-eigenvector supplies PSD repair of trace2c; if c<0 the positive eigenvector supplies trace−c. Since |c|<=tr Q, repair trace<=2tr Q. Thus null-convex Hessians bounded by K pair with S at least−3K tr Q, and the null-concave inequality reverses correctly. No claim that P alone is J-null is used.

The global extension is valid: choose positive nested convex gaps inside the strict local majorant neighborhood, cutoff equal1 through K1, and add a large bounded-Hessian convex support barrier. It vanishes on K0, so values on E remain unchanged; on the transition annulus its positive Hessian dominates every negative cutoff direction. On K1 the original local null-convexity remains, and outside K2 only the convex barrier remains. For chord-radius r<=1/2 the probability-area cap transverse second moment is r^4/16−r^6/96, comfortably above r^4/128; the stated annular m0 is conservative. Explicit computable gaps and cutoff derivative bounds yield finite K independent of the stress support radius. No globally concave polynomial approximation is assumed.

A boundary-net/quantized-value McShane construction gives a finite sup-norm delta-net of normalized1-Lipschitz rewards, with mesh/rounding chosen smaller than delta. The net itself needs no value-function modulus. The already received positive-accuracy oracle supplies each local majorant with root excess<=delta. Extending and testing yields source excess<=delta+3K_delta N for net rewards; two sup-norm errors yield the final **3delta+3K_delta N**. Compact-convex W1 separation/minimax is applied to the actual paid closure, not a finite menu. Choosing delta=tau/6 and N<=tau/(6K_delta) gives <=tau.

The final actual-policy enumeration uses a STRICT positive allowance above that distance bound. Density plus computable W1 upper approximations then ensures a terminating successful branch. Without the allowance, attainment by an enumerated finite law would not follow. K_delta and the search may be enormous; neither has been numerically evaluated here.

## Effective evaluator constants and scope

Directly differentiating (Gamma e)_i gives diagonal derivative bound3 and off-diagonal1, Frobenius<6. Therefore |V|<=2sqrt3, |P|<=3, |B|<=8, |DV|<=24/A. The trace loss in sym(DV P)−tr(DV P)I is paid by factor4, yielding K0<=291/A+2<296/A since A<=9/4. Consequently the weighted canonical matrix has operator norm<=18t²+296t(1−t)<=92 and negative trace<=276.

Four phase squares have Haar mass4rho²/pi², and A<=6rho² there. Thus canonical tail coefficient276*4/pi²<123, while the correction ceiling M contributes exactly at most24M rho^4 after integrating t². Both physical fibers are already in the received radial Jacobian. No pointwise unweighted S0 bound near vertices is substituted.

Off those squares A has a computable positive lower bound, and the weighted field is regular also at t=0. Matrix negative trace is nuclear-Lipschitz; interval eigenvalue/entry bounds with an explicit computable modulus yield convergent regular-region integrals. Outside E, all compact correction/cutoff regions must be integrated; undecided semialgebraic boundary boxes are charged by3M times volume. This proves an effective positive-accuracy evaluator for the explicit computable smooth potential library, not an already implemented full integral. A merely existential C1/W2,infinity collar bound is NOT a numerical M receipt.

## Conclusion and exclusions

The three receiving theorems close representation and finite-stage interfaces conditionally. They do NOT provide a vanishing sequence, an evaluated useful threshold K_delta, a small-N certificate, a new actual W1 law, full positive interior stress, source membership or Morrey resolution. The earlier sampled .849→.750 objective remains unreceived. Any further boundary-concentration lemma is separate from this audit.
