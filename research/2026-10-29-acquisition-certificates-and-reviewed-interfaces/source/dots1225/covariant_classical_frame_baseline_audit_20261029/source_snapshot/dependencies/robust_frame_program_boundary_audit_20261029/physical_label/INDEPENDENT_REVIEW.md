# Independent exact physical source-to-label review
2026-10-29. Mathematical derivation and independent checks pass.

The ten Kraus operators are TP and unital. They realize precisely the singlet block plus completely mixed triplet block: the two inequivalent collective SU(2) irreducibles have multiplicity1, so this is the collective Haar twirl. Orthogonality of the nine Pauli products under Tr(A†B)/4 is exact. Their transfer is the rank-one projector onto vec(I3)/sqrt3. Conjugating both input and output by V tensor I rotates that coefficient vector; Tr(P_ab W SWAP W†)/(2sqrt3) has unit norm, with no missing factor2.

Expanding sum_l Tr([K_l,P_a]†[K_l,P_b])/8, trace preservation and unitality supply the two diagonal terms, and self-adjointness equates the two cross transfers. Thus H=I-Pc. Depolarization has zero product-Pauli transfer and H=I; linearity in the channel yields the asserted noisy H. This is a statement about the channel, independent of the Kraus representation chosen.

The actual minus-branch amplitudes are [K_l,P_a]/(2sqrt9). With a trusted I4/4 input, the output label entry is sum_l Tr([K_l,P_a][K_l,P_b]†)/144=H_ba/18. Consequently q_minus=(8+eta)/18 and normalized state=(P_perp+eta Pc)/(8+eta). The real normalized c_R makes the transpose harmless in this particular family. Source eta and label x=eta/(8+eta) must not be identified.

Exact Choi spectrum of the untwisted twirl is1 once,1/3 nine times,0 six times. Local conjugation preserves it. The contaminated spectrum is1-3eta/4 once,(4-eta)/12 nine times,eta/4 six times. Thus the stated lower bound is attained and Choi rank is16 for eta>0. Eta=1 yields I9/9 labels independent of the frame; eta=0 retains the exact dark direction.

Memorylessness plus fresh trusted instrument ancillas proves independent normalized minus records; full-rank marginals alone would not. This is a concrete mathematical source family, not a prepared laboratory source or an arbitrary correlated-noise reduction. Its application to separate growth/purification recurrences requires their own actual-scope proofs and finite-cap accounting.

Independent exact program:16 channel matrix-unit identities;2 rational twists;8 explicit full minus-instrument calculations; exact Choi spectrum. Author50 binary64 fixtures replay identically with maximum Gram residual2.6166925806938827e-15. These checks supplement the proof and make no hardware claim.
