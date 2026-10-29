# Receiving review: coherent multibranch filtering

2026-10-29. Accepted as an exact instrument with explicit ideal-control conditions, and as a useful negative comparison result. No generic historical novelty or advantage is accepted.

## Algebra and retained memory

Expanding the average of m independent conjugated Kraus operators gives diagonal terms T/m and off-diagonal terms (1−1/m)G. Therefore the accepted map is G+(T−G)/m. T−G has the explicit positive covariance-Kraus representation. This equality holds before tracing memory and extends to every reference. For the Pauli basis, averaging removes unequal components and leaves id⊗B0 plus weighted Pauli branches. The trace effect is scalar on the logical space, so the actual accepted memory map factors through the incoming memory marginal even when logical input and memory are correlated. The subnormalized half-diamond bound follows by comparing two CP maps with the same bad trace effect. No normalized bound is inferred without acceptance control.

For general irreducible group representations, Schur yields the same scalar memory effect. Even if one uses only a conjugation 1-design ensemble rather than a whole group, the marginal conclusion follows directly: trace removes the post-unitary, and the pre-unitary average replaces the logical input by I/d times its memory marginal. A covariance argument should not be read as automatically applying to every nongroup ensemble; this does not invalidate the stated group uses or the map identity.

The raw input/output intertwiner claim requires a genuine common group representation and multiplicity one. Extending projective Pauli representatives by identity on leakage violates that premise. The qutrit example gives acceptance 5/8 rather than 1/2; honest Q8 restores the result. Completing the logical decoder first is a different, valid interface with a different GOOD component. No N1041 control protection is inherited automatically.

## Exact conventional comparator

Nested controlled checks must be undone in reverse order. The adjoint Pauli projections commute even when the underlying Paulis anticommute, so the accepted amplitude retains exactly the commuting Pauli components. Independent uniform checks retain each nonidentity component with probability 2^-b. A fresh independent Pauli pad removes the remaining unequal-component coherences. Thus the comparator is EXACTLY the same full-memory accepted CP map as m=2^b independent branches. Omitting the pad, repeating the same branch key, or dephasing flags gives the documented distinct maps. Control resources O(bk) and 2k(b+1) classical bits are conservative primitive bounds under all-to-all access; routing, errors, coherent holding and timing isolation remain additional.

Clifford tag comparison follows by uniformizing nonidentity Pauli components. Among accepted tag I/Z strings, m−1 have identity payload, and m(d²−1) have nonidentity payload. This gives the stated equation (2), acceptance and bad-mass formulas. It is not claimed to dominate every resource/yield criterion, and no Clifford circuit was executed in this review.

## Executed checks

Both author programs were copied and replayed without changing frozen source. They include rectangular joint channels, full Choi matrices, full nested controlled gates, and the leakage/phase, missing-pad, reused-key and dephasing failures. Independently authored k=2, input memory 2/output memory 3 code enumerated all two-key branches and all padded single-check keys. Both maps match the target to 1.18e−16; scalar trace-effect residual is 1.35e−17. These floating checks support the analytical identities but are not interval certificates or hardware evidence.

## Primary attribution and decision

The directly relevant existing coherent-check mechanism is described in van den Berg et al., [arXiv:2212.03937](https://arxiv.org/pdf/2212.03937). The primary source's introductory discussion and two-sided-check construction were consulted. The Clifford/Pauli twirl and nonidentity uniformization were checked against Aharonov et al., [arXiv:1704.04487](https://arxiv.org/html/1704.04487v1), section 3, especially lemmas 3.4–3.6. The present memory-retaining calculations specify the instrument rather than establishing priority for those mechanisms.

The protected flags, private fresh keys, completed endpoint maps and source/control isolation are real resources. A dephased flag cannot deliver the ideal filter; an unknown failed payload cannot simply be retried. The depolarizing example requires flags comparable to the payload and therefore offers no uncounted escape from capacity limits. No matched practical advantage, scalable reliable communication, calibration acquisition or physical error threshold is established here. Retain the operation and counterexamples, reject the proposed generic multiplexor advantage.
