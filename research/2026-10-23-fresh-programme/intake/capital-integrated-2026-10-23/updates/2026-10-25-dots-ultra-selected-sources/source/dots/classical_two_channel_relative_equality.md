# Two arbitrary classical channels: conditional and complete relative order coincide

24 October 2026. Extension of `classical_channel_sld_bkm_equality.md`, proposed by the parent and checked here. No external priority claim.

Let K and L be finite stochastic channels with the same input alphabet; their output alphabets may differ. Fix any finite constant c>=0. The following three uniform statements are equivalent:

1. For every finite quantum reference and every pair rho,sigma with rho_R=sigma_R,

       D(K rho || K sigma) <= c D(L rho || L sigma).

2. For every finite quantum reference and every pair rho,sigma for which the displayed quantities are finite,

       D(K rho || K sigma) - D(rho_R || sigma_R)
         <= c [D(L rho || L sigma) - D(rho_R || sigma_R)].

3. For every faithful cq baseline sigma and Hermitian tangent H with H_R=0,

       g^S_(K sigma)(K H) <= c g^S_(L sigma)(L H).

Output reference identity maps are implicit.

## Proof

(2) implies (1) by restricting to equal-reference pairs.

(1) implies the analogous complete BKM metric inequality by infinitesimal faithful pairs. Apply the Liouville/vacuum boundary construction from the preceding note to the same input sigma,H. That construction commutes simultaneously with K and L, regardless of their output alphabets. Divide its complete BKM inequality by log(1/epsilon) and take epsilon to zero. The common factor 2r cancels, proving (3).

For (3) implies (2), start with arbitrary sigma,H. The reference score L_R=Omega_(sigma_R)^-1(H_R) is common to both outputs, since both channels preserve the reference marginal. Put H0=H-Omega_sigma(I tensor L_R). Then H0_R=0, and the exact SLD gauge at each output yields

    g^S_(K sigma)(K H) - g^S_(sigma_R)(H_R)
      = g^S_(K sigma)(K H0),
    g^S_(L sigma)(L H) - g^S_(sigma_R)(H_R)
      = g^S_(L sigma)(L H0).

Apply (3). The untouched-reference-qubit integral converts the resulting conditional SLD inequality to the conditional BKM inequality with the same c. Integrate along the state-pair segment to obtain (2). Standard common faithful regularization handles finite-relative-entropy boundary pairs.

## Zero denominators and relative coefficients

The theorem is deliberately stated as equivalence of inequalities, so no 0/0 convention is needed. If the denominator SLD quadratic form vanishes at a faithful baseline, then L(H)=0. Its lifted tangent is also exactly zero after L. Thus a positive numerator with zero denominator really excludes every finite c; it is not an indeterminate limit. If numerator and denominator both vanish, that test imposes no restriction.

The infimum of admissible finite c, with value +infinity if there is none, is therefore the same for complete Umegaki, conditional Umegaki, and complete SLD relative comparison. Swapping K and L proves the equivalent statement for uniform lower bounds. Alternatively define the lower coefficient directly as the supremum of all a>=0 for which numerator>=a denominator uniformly; the same gauge, lift, and integration prove equivalence without dividing by zero.

This covers arbitrary classical transmitted channels with quantum references. It is stronger than comparing each channel only against the identity. For Weyl random-unitary channel pairs on a shared Weyl system, the exact orbit/Bell encodings transfer this entire relative-order statement to their classical convolution pair. Individual unitary canonicalizations do not justify the corresponding claim for arbitrary pairs of unital qubit channels with incompatible input rotations.
