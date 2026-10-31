# Independent review: one private global interaction sign

Verdict: scoped mathematical PASS for the displayed complete logical-channel error bound, conditional on actual access to the two physical sign settings. This is not a novelty finding, a free physical-control operation, or a practical resource claim.

Source: PRIVATE_SIGN_PAIR_REDUCTION_CANDIDATE.md, read in full on 2026-10-31. Source SHA-256: 299bfbc80c35aed153b4c0ea2ebe1c8ea59dc4a0c289d4335b58f1669863f3c6 (6,404 bytes). Dependencies are the separately reviewed generic dark-source logical reduction and its complete return/resolvent estimate. No additional source inverse is implemented.

## Centered pair lemma

Let B denote the K=0 controlled base protocol and E_sigma the actual protocol of sign sigma. In the controlled Duhamel expansion of E_sigma−B, place actual propagation on the initial side of each insertion and base propagation on the terminal side. On the latter side, every system-only H0 propagation and instrument commutes with the source semigroup and stationary projection. This remains true for rectangular record-algebra maps and policies controlled by earlier public records: they are still the same prescribed system/record operation in both branches and do not act on the source.

Consequently a base suffix of total duration u satisfies B_suffix Q_sup=(exp(lambda u G†)−Pi) composed with a complete contraction. Its norm is at most q(lambda u), not q(lambda u) times an additional norm of Q_sup. Each perturbation insertion has complete norm at most 2b sqrt(lambda). Summing the two comparisons with the same base gives

    ||(E_+−E_−)Q_sup||cb <= 4b sqrt(lambda) integral_0^t q(lambda u)du
                              <= 4b ell/sqrt(lambda).

The integration variable is accumulated physical suffix time. Zero-time control slots do not reset that time or add a fresh mixing integral. This is a complete operator-map estimate, not a stationary-state or average-energy estimate.

For a general observable split I=Pi+Q_sup. Since Pi is a complete contraction and its range is the embedded system/record algebra, the previously proved single-sign logical bound gives ||(E_+−E_−)Pi||cb<=2 delta. Therefore the displayed full-pair bound 2 delta+4b ell epsilon is valid. There is no extra factor 2 from Q_sup: that projection was already present inside the proved centered lemma.

## Averaged intertwiner and constants

Use T_sigma=P+sigma epsilon F1+epsilon^2 F2 with the same effective evolution for both signs. Its residual is sigma epsilon A1+epsilon^2 A2, and each control defect has the same odd/even form.

In the two endpoint terms, the unpropagated odd endpoint cancels exactly in the average. The propagated odd endpoint is epsilon(E_+−E_−)F1/2. Since Pi F1=0, its norm is at most 2b ell epsilon^2 f1. The even endpoints cost 2 epsilon^2 f2.

Each odd control defect J1_j is centered because source averaging commutes with the system-only control and Pi F1=0. It therefore costs at most 2b ell epsilon^2 ||J1_j|| after signed averaging. The even control defects cost epsilon^2 J2. These statements apply to the actual record algebra at that slot and any retained reference.

The odd residual A1 need not be centered. Its averaged insertion is bounded using the full-pair estimate on the actual prefix, with the effective suffix remaining a contraction. Global T_total and control-budget bounds upper-bound those of every prefix. This costs epsilon T_total C1(delta+2b ell epsilon). The even residual costs epsilon^2 T_total C2. Combining these terms yields exactly

    epsilon^2[2b ell(f1+J1)+B2]
      +epsilon T_total C1[delta+2b ell epsilon],

with B1=2f1+T_total C1+J1 and B2=2f2+T_total C2+J2. Substituting delta<=epsilon B1+epsilon^2 B2 gives the displayed epsilon^2 and epsilon^3 expression. The T_total^2 contribution is real and has not been discarded. The inherited values of f1, f2, C1, C2, J1 and J2 are consistent with the generic review.

The comparison is uniform over arbitrary initial quantum source-system-reference correlations because all estimates are complete observable-map bounds. Neither cold preparation nor a P/Q-homogeneous source-jump representation is required. The source generator may have QLQ recycling. For fixed time and control budget, the error is O(1/lambda). Lambda must be positive in the inverse-rate expression; the zero-rate case has the separate trivial bound 2.

## Physical and computational boundary

The implemented operation must be the positive CPTP average of two protocols with the same source generator, same H0, same timing, and same public-record feedback policy, differing only by the sign of K. One independent private fair bit is sampled before the entire protocol. Initial correlation with that bit, revealing it for user feedback, flipping H0 too, or using different source dynamics does not meet this interface.

The bit is discarded, and source output is discarded. The retained output is the system, reference, and system-only instrument records. These are not claims about a retained bath history or access to the private sign. Sign-setting bias, transients, source mismatch, encoding and gate errors need separate complete-error accounting. A supplied block encoding or norm certificate does not itself acquire analog sign control.

This establishes a cancellation mechanism using the already proved logical reduction, not an implementation of the effective stack or a favorable resource comparison. Ordinary symmetrization, antithetic mixtures, effective-operator methods, and direct fresh-ancilla implementations remain relevant alternatives. No claim of new general machinery or literature exhaustiveness is made. The supplied floating sign-symmetrization diagnostic is not needed for this proof and has not been promoted to a certified numerical bound.
