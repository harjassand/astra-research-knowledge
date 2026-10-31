# Independent review: dark-source logical reduction

Verdict: scoped mathematical PASS, not a complete executable effective-channel compiler or a novelty finding.

Source fully read: DARK_SOURCE_LOGICAL_REDUCTION_CANDIDATE.md, SHA-256 ff711b0d4c93d0b0a0b86a1ac09bcc20affac0716ef50d87732036601acf2229. This version includes the explicit acquired-normalization correction. Review date: 2026-10-31.

## Return and analysis maps

For the finite dark source, the energy drift yields p=Tr(Q sigma_t) <= min(1,(h/g)e^{-kappa t}). The gentle projection estimate is valid with an arbitrary reference. Moreover the difference between the true reference marginal and the partial trace of P sigma_t P is positive with trace p. Hence the complete return bound 2 sqrt(p)+p, capped at 2, is justified. Integrating min(2,3 sqrt(h/g)e^{-kappa t/2}) gives exactly the displayed upper bound ell=4[1+log((3/2)sqrt(h/g))]/kappa.

The finite-source resolvent is a completely bounded analysis map with norm at most ell. Its identities R Pi=Pi R=0 and G†R=−(I−Pi) follow from the return limit. Centering gives Pi VP=0. Thus F1=RVP and F2=RVF1 obey the stated cancellation identities without an extra norm factor for I−Pi. The intertwiner need not be a channel and is not implemented.

Expanding L_lambda T−T L_eff cancels the leading terms. The remaining terms are lambda^{-1/2}(VF2+[L0,F1]−F1D) and lambda^{-1}([L0,F2]−F2D). The source-only resolvent commutes with system H0. The resulting constants 2d ell+16b^3 ell^2 and 8bd ell^2+16b^4 ell^3 are valid. A common intertwiner across prescribed system-only instrument slots leaves only two endpoint defects. The control defect bounds follow by commuting each instrument through R and Pi and expanding its commutator through the two V factors. All statements extend completely to reference and retained-record algebras.

## Effective CP generator

The dark coherence identity G(|v><psi|)=−H|v><psi| is exact even when Q L_j Q is nonzero: the recycling term vanishes on this particular coherence because L_j psi=0. Its adjoint orientation is likewise valid. This does NOT assume that all source jumps return directly to psi.

The effective stack E=sqrt(2) H_Q^{-1/2} K(|psi> tensor I) has the displayed generator. In particular, the two recycling contributions from the second-order double commutator combine under the source partial trace into 2 Tr_source(H_Q^{-1/2} K P rho K H_Q^{-1/2}); the loss coefficient is E†E/2=<psi|K H_Q^{-1}K|psi>. There is no additional Lamb-shift term under the stated source assumptions. An extra source Hamiltonian would change this derivation and is not included. The Gram matrix may be complex and its effective jumps non-Hermitian.

This is a genuinely CP effective generator, but not a free normalized isometry. The corrected source properly distinguishes ||E||<=sqrt(2/g)b from acquired block normalization. Direct composition from K/alpha_K pays sqrt(2/g)alpha_K. A smaller normalization requires an acquired construction or paid amplification. Inverse-square-root conditioning, the actual H encoding normalization, psi preparation, label retention/tracing, effective Lindblad execution, and H0 execution remain paid. No full G-resolvent oracle is assumed or needed for this coefficient formula.

## Output and limits

The endpoint estimate compares with an effective channel acting on the initial system marginal, uniformly over arbitrary quantum source-system-reference initial correlations. This follows from the uniform observable comparison; stationary preparation or initial dephasing is unnecessary. Only system/reference/system-only-instrument records are retained. Source outputs and source interventions are excluded. Inverse-lambda displayed estimates apply to lambda>0; at lambda=0 the trivial distance-2 bound remains available, not a singular formula.

The result is ordinary adiabatic-elimination/intertwiner machinery with a concrete dark-source certificate and constructive positive effective stack. It is not a claim that these broad ideas are new, that an optimal effective encoding has been acquired, or that the generic model has a practical advantage. The source's prior comparison correctly notes that direct-return effective-operator formulas do not by themselves cover QLQ recycling; that distinction is not an absence-of-prior-art proof. A paid nonclassical instance and execution comparison are separate work.
