# Removing rooted/order/gate overcount without losing any actual source

This refines the complete global trial, not its shape support. Bridge independently approved the three combinatorial steps below.

## 1. Physical roots and tuple orders

An actual positively oriented simple resolved contour with physical perimeterP has exactlyP physical-edge roots. Its contracted physical trace may touch vertices but cannot repeat a physical edge. Distinct roots give distinct(root location,word) labels; a nontrivial cyclic word period would repeat an edge of the lifted embedded contour. The fixed diagonal resolution reconstructs the actual contour from its rooted physical trace.

Therefore divide the acquired rooted activity upper A_P byP. Each actual UNROOTED contour retains its full weight in this sum, while every invalid overcount word still contributes nonnegative mass. Actual affected outer domains at a structural gate are distinct; allj! orderings occur with equal product weight. Dividing the orderedj-tuple polynomial byj! consequently retains each unordered actual tuple once.

Write alpha(z)=sum_(P<=Mper)(A_P/P)z^P.

## 2. Only a boundary-collar gate is possible

An actual structural addition lies outside each selected filled domain and is an augmented neighbor of at least one. Every Chebyshev outside neighbor is covered by a physical boundary edge's outside endpoint and the endpoint's two tangential neighbors. For a diagonal neighbor, take a two-step physical path from its inside site: if the first intermediate site is outside, the gate is a tangential neighbor of that boundary edge's outside endpoint; otherwise the gate itself is the outside endpoint of the second boundary edge. Thus at most3P gate marks suffice for a domain of physical perimeterP, and3S for a tuple of total perimeterS. Extra marks and repeated gate locations are safe overcounts.

The complete truncated structural energy upper is therefore

 W_short/Z_M <= Q
 =3 sum_(j=1)^8 1/j! sum_(S>=S0) S [z^S] alpha(z)^j.

Keep the PREVIOUS n*T_tail bound for omitted long contours. There is no need to assume a new tail perimeter-moment estimate. Target crossings and source overlap are unchanged.

## 3. Complete finite result

certify_global_upper_marked.py uses the same already acquired rational-tilt magnetic moments, divides coefficient uppers byP, and runs an upward-rounded positive convolution with a weighted S-Horner sum. It divides byj!, multiplies by3, and then adds the old full tail and original source/target terms.

At R200,r5,s79/40 it gives

 log(W_short/Z_M)<=-6215.6620093449592...,
 log(C_kappa/ZA)<=-6215.6619158297127...,
 hence C_kappa/ZA<=exp(-6215).

Receipt: cert_r200/certificate_marked_s79_40.json. This is a mathematical upper certificate subject to the same explicit hardware/arithmetic and inherited geometric interfaces, not an estimate of actual C. No new long-walk run was needed.

## 4. Matching actual energy proposal

The proposal of ACTUAL_ENERGY_PROPOSAL.md can use exactly this refined normalizer Q:

- Give an ordered rooted tuple weight product(b_gamma/P_gamma) times(3S/j!).
- Select uniformly one of its3S boundary marks, which determines the proposed gate.
- Draw y from the auxiliary core, inverse-flip domains and validate the actual cut edge as before.
- Do NOT demand canonical roots or ordering. Require instead that all words describe the actual affected unordered domains with positive orientation. Among repeated boundary marks yielding this gate, accept only a deterministic first mark for this representation.
- Accept with the same probability c_i(x)w(x)/[w(y)product b_gamma].

For one actual edge there are j!product P_gamma valid root/order representations, each with proposal/accepted density

 g(x,x^i)/[Q Z_aux j!product P_gamma].

Their sum is exactly g/(Q Z_aux). Thus accepted edges retain the actual conductance-weighted law, with the unnecessary root/order rejection loss removed. Missing inverse-image energy is now bounded by Q Z_M u', since expanding all boundary marks covers the same change-of-variables bound. All long-tail/target/source errors are still paid separately.

Using only the conservative C/ZA>=exp(-6449) and auxiliaryr'=64 gives acceptance at least0.5exp(-234), an enormous finite bound. A stronger same-cut energy witness can improve acceptance even without improving C: it must genuinely lie among the retained short edges and have inverse image in the auxiliary core. That support check is required before substituting its weight. None of these finite acceptance bounds establishes a uniform polynomial W/C theorem or a practical experiment.
