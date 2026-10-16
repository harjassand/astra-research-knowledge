# Exact cost of one imperfect local refresh

For a specified local partial-dephasing channel with residual coherence eta, two own-gap actions a,b have an exact sharp endpoint-flip value F. Put p=sin²(min(a,pi/2)), q=sin²(min(b,pi/2)), Q=p+q-pq. Then

    F = Q + max_(0<=c<=1) [-pq c² + 2 eta sqrt(pq(1-p)(1-q)) c].

The closed formula and a three-level attaining construction are in PROOF.md. For multiple coordinates, each with its own such channel at an independently fixed time, the sharp joint value is the product of these F values, despite an arbitrary shared bath.

Any nonzero residual coherence can exceed the ideal-pinch Q for interior p,q. For a=b=pi/6 and eta=1/2, the exact value is 9/16 versus the ideal 7/16. This is a finite analytical obstruction, not a numerical search result.

The gain over existing capital is the exact optimized two-gap value and its causal product transfer. The identity/full-pinch mixture method already appears in the inherited October 15 notes and is not presented as new. An optional finite-action multiple-node certificate and O(m²) recurrence are explicitly nonsharp.

The channel must hold on the full joint state, act as identity on the persistent bath, and have a fresh inaccessible environment. A reduced coherence measurement alone is insufficient. No hardware readiness, novelty priority, correlated-noise guarantee, or exact many-node optimum is asserted.
