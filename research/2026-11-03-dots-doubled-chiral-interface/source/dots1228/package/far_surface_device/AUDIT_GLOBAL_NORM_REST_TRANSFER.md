# Independent audit: finite-volume rest-parent transfer by global norm

2026-11-03. Audited `GLOBAL_NORM_REST_PARENT_TRANSFER.md`, its explicit amplification appendix and subsequent corrections, together with `COMPRESSED_REST_GAP_INTERFACE.md`.

## Verdict

The corrected finite-volume global-norm route closes at the stated existence/resource level. It does not invoke locality or generic stability of a projected Q-mode algebra. Instead it constructs actual physical finite-patch coefficients and compares their entire many-body Hamiltonian to a free target factor plus an exact gapped rest parent. The price is volume-dependent range/thickness of squared-logarithmic order with enormous fixed microscopic constants.

Two substantive gaps in the first draft were repaired during audit:
- The exterior-tensor Fock estimate is not valid for arbitrary BdG Gaussian lifts without phase control. The explicit principal-log Spin-lift certificate now resolves this.
- The direct near-mass leakage V_near-QV_nearQ must be paid in addition to the free normal-chain residual. It is now displayed and assigned to the common amplification budget.

## 1. Exact comparison and the static Q input

F must contain ALL far momenta below the full static cutoff, both k and -k, and complete internal species. Canonical copy and hole projectors must be the conjugate/onsite-transported versions. These are not optional conditions when using the purification; an arbitrary asymmetric probe band from the response-only lemma is insufficient.

Removal of the exact far singular-vector branch leaves the audited near localizer plus the high sector. Its Schur gap is >M/3. The geometric-to-exact subspace rotation has norm distance <=4b_*^L, so transporting the compression changes it by <=8R_h b_*^L. The stated bound gives a geometric-compression gap >=M/4. If decoration is included in the same sign polynomial, its gap must also enter g_fast=min(M/4,Delta_dec); the corrected note does so.

The rest occupied-count index follows directly from this near/high calculation. Complete multiplets make the reference half-count integral and preserve the required parity compensation. The canonical construction can therefore be applied algebraically to Q even though Q is nonlocal in physical coordinates.

The dummy +mu P_F is legitimate in the number-conserving block. Its BdG extension must be diag(+mu P_F,-mu P_F*) rather than an identity shift violating particle-hole symmetry. The corrected note specifies this. The fixed F block commutes with the Q block in the canonical construction, and its exponential factors cancel EXACTLY in every relative reset kernel. Scalar reference contributions are rotor independent.

## 2. Polynomial data and the crucial anchored cancellation

For possibly gapless physical A with ||A||<=1, the partial binomial polynomial p_k(A) is still a contraction: for each real scalar x, its positive partial sum has magnitude at most the full binomial sum 1. No approximation to the physical sign is claimed. Only the uniformly gapped extended A_tilde uses the exponentially small sign tail.

The relative Taylor expression

 I+T_J(G_phi)T_J(-G_phi')-T_J(G_phi)T_J(-G_phi)

is essential. Every nonconstant term contains a difference between the two configurations. Expanding that difference by ordinary noncommutative telescoping anchors each word at one local mass/pairing change. Its total physical walk degree is bounded by D, including the fixed texture stencil offset.

A patch containing every such D-step walk therefore reproduces the entire anchored Taylor expression EXACTLY, extended by identity outside. Individual patch sign matrices need not be gapped. The actual operator implemented is the exact exponential of the bounded finite-patch Gaussian generator, not a nonunitary Taylor polynomial. The Taylor expression is used only to certify its error.

## 3. Mixed projected/physical words: why the profile factor really appears

Start by replacing the local projected change Q Delta A Q by Delta A. The difference has P_F immediately adjacent to the near insertion. Then replace all remaining projected factors by physical factors starting nearest that insertion and moving outward, separately on each side.

At a replacement,

 A_tilde-A=-P_F A-A P_F+P_F A P_F+(mu/R)P_F.

Every discrepancy therefore has a P_F separated from the near insertion by a segment composed ENTIRELY of physical finite-range factors. All factors farther away can remain projected contractions. The segment length is at most D. Selecting the P_F nearest the insertion gives the explicit profile factor sqrt(n)b_*^(L-1-D), with no assumed locality of a projected factor. At most O(D^2) insertion choices occur. This is the correct telescoping order; an arbitrary product difference would not justify the same local-profile estimate.

For the scalar energy, first subtract a fixed-texture reference. The same noncommutative telescope anchors each trace difference at a near-boundary change; cyclicity positions that insertion next to the physical segment. The trace costs at most another factor n. No rotor-dependent far contribution remains unanchored. The removed reference is only a scalar energy zero, not a supplied state or response oracle.

The updated coefficient l1 bound B=4^(k+2) safely dominates the grouped generator's monomial coefficients, including fixed canonical matrices. The relative Taylor expression costs at most 4(J+1)^2 B^(2J), plus polynomial degree/insertion factors. Combining this with at most n_rot terms, trace/Fock factors of order n, and the scalar energy scale is safely dominated by

  10000(n+n_rot+1)^4(R+1)(D+1)^4(J+1)^4 B^(2J+2).

The extra B^2 and support powers provide substantial slack. The large coefficient is used only to select thickness/precision; it is not a computational instruction to enumerate all words.

## 4. Gaussian lift phase: the repaired argument is sound

For every exact, partial-polynomial, and patch canonical generator, the actual one-body norm is <=pi/4. A relative path exp(tG_phi)exp(-tG_phi') therefore has eigenangles in [-pi/2,pi/2]. It stays in the principal-log neighborhood, and its exponential-defined Spin lift is the continuous principal-log lift from identity. This argument uses an explicit Gaussian path, not a smooth path through rotor configurations, so rounding-wall jumps are harmless.

For two normal orthogonal/unitary matrices in this semicircle,

  ||log O-log O'|| <= ||O-O'|| integral_0^infinity ds/(1+s^2)
                    =(pi/2)||O-O'||.

This follows from the resolvent integral and ||(O+sI)^-1||<=1/sqrt(1+s^2). The quadratic Majorana lift and unitary Duhamel then give the conservative 4n amplification now used in the note. Thus neither a Spin sign nor a many-body phase oracle is omitted. Ordinary exterior-product telescoping remains valid for the number-conserving subblocks but is not used as the general BdG justification.

## 5. Full fast error and global conclusion

The literal physical fast matrix differs from h_F direct-summed with Qh_nearQ by TWO contributions:

  free leakage <=2r b_*^L/a,
  near mass leakage <=3 n^(3/2) M b_*^(L-1).

The second bound follows from the physical near support and the full-Fock trace-norm estimate. It is now explicitly absorbed into A_cert b_*^(L-1-D); R>=M and the displayed amplification dominate it.

The sign-tail and factorial-tail allocations have enough slack after the 4n Gaussian-lift factor. Choosing the two displayed leakage budgets then gives the global comparison error <=epsilon, modulo the rotor-independent reference-energy scalar. Exact symmetry twirling contracts the comparison error and only enlarges physical support by its fixed circuit radius.

The exact comparator is H_F plus a rest parent with a unique ground and algebraic gap Delta. Consequently the finite-device low spectrum has the stated multiplicity correspondence whenever the chosen cutoff lies below the rest threshold and at distance >epsilon from the comparator spectrum. Infinite rotor factors do not obstruct this: below Delta, the comparator's rest factor is rank one and its Fock target factor is finite dimensional. No claim that every dense target many-body level has a resolvable gap is justified or made.

## 6. Resource and integration qualifications

At fixed g/R, k and the conservative Taylor order J are logarithmic in total mode count and inverse error. D and log A_cert are quadratic in those logarithms. The implicit n=O(NL) relation can be solved by the displayed scalar inequalities; it does not require a physical-state oracle. The actual finite-patch evaluation uses polynomial matrix recurrences and exact finite Gaussian exponentials. The quoted g/R makes the prefactors astronomical.

This is a VOLUME-DEPENDENT finite-range family, not the earlier fixed-range half-space theorem. It must be labeled as such.

The optional later addition of unbounded kappa sum L_j^2 changes the ultraviolet spectrum. The prior finite-auxiliary ground and new-model finite-energy contracts do not automatically transfer this bounded-rotor device's entire far-band spectrum or state-independent response to that new model. Such a connection requires its own estimate.

Likewise, an uncomputed scalar C_ref is harmless for response, gaps, and aligned spectral counts, but not automatically for a QPE protocol that assumes a known absolute ground-energy bracket. One may compute the explicit finite one-body reference energy to certified accuracy (polynomial sign-trace approximation is available), or use an energy-search protocol. Do not silently inherit the fully gapped parent's zero-energy bracket for the reference-subtracted device.
