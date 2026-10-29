# Two localization calculations and the unresolved sequential step

30 October 2026. Root derivation. These are ordinary probability/convex
identities, not claimed historical novelties or a completed compiler.

1. Write d_t(h)=D(P_future|h || Q_future|h). Chain rule gives
E_(h~P[:t]) d_t(h)<=Delta for every cut. Therefore a fresh batch of N target
prefixes has d_t(h)<=kappa at EVERY sampled prefix except with probability
at most N Delta/kappa. Their conditional future vectors then differ in L1
by at most sqrt(2kappa). An arbitrary adaptively queried prefix has no such
guarantee. If one samples Q prefixes instead, a further N sqrt(Delta/2)
union allowance suffices by coupling prefix marginals. This is not a
conditional P oracle.

For a good prefix h and an extension o with P(o|h)>=tau, conditional chain
rule gives d_(t+1)(ho)<=kappa/tau. Teacher-heavy extensions can be related
to this premise using the next-token marginal TV bound. Repeating this
division through a chain may cost tau^(-T), which is not polynomial in T.

2. Let C be a convex subset of the finite probability simplex and let
z_star minimize D(z_prime||w) over C, with positive w,z_star. For every
z0 in C, the first-order projection inequality implies

    <z0,log(w/z_star)><=0.

For any target z, if ||z-z0||1<=e and the coordinatewise log ratio is
bounded in absolute value by B, then

    D(z||z_star)<=D(z||w)+e B.

Indeed the difference is <z,log(w/z_star)>; insert z0 and use the preceding
inequality. If w,z_star lie between a mu and b mu for the same dominating
positive measure mu, B=log(b/a). This removes the factor-two L1 projection
loss even under APPROXIMATE representability, at a paid log-ratio cost.
It does not grant a computable dominating measure, full-future positivity,
efficient approximate representation or the complete sequential model.

The unresolved operation is acquiring and propagating those weighted
representations from the stated global-KL access at polynomial cost. A
finite-dimensional successful projection or spanner fixture would not prove
that operation. No result is imported merely because the formulas compose
syntactically.
