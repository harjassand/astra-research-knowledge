# Synthesis error receiving through a common sparse-syndrome factor
30 October 2026. New conditional lemma for the known-target polynomial factory.

An ideal circuit approximation is not automatically contractive through a signed good-history sum. The following factorization provides the needed explicit comparison.

Let the actual encoded computation state be tau=G+B, with ||B||_1<=b_c, tau positive of trace one. Retain the fixed COMMON coherent hierarchical decoder D as an isometry, including all syndrome and environment work. The frozen scheduled-FT receiving theorem gives, for the known compiled pure logical target |psi_s>,

    D G D† = |psi_s><psi_s| tensor K.

K is a possibly signed Hermitian operator on syndrome/bath; it is not called a state. Its ket and bra syndrome support lies in S, the span of syndrome vectors of the entire admitted hierarchical sparse-error family. The common cross-term correction theorem works for every logical input, so the entire tensor product L tensor S lies in the image of D, not just the one compiled ray.

Since D is an isometry and tau is positive trace one,

    ||K||_1 = ||G||_1 <= 1+b_c.

Let |psi> be the desired exact embedded-qubit target, with || |psi_s><psi_s|-|psi><psi| ||_1<=epsilon_synth. Define J to be the fixed CPTP inverse/reembedding of D on L tensor S, completed arbitrarily outside that subspace, and define

    G'=J(|psi><psi| tensor K).

Then ||G-G'||_1<=(1+b_c)epsilon_synth, and ||G'||_1<=1+b_c. G' need not be positive, but both its legs lie in the desired target's common sparse-error module. No physical inverse ideal decoder is being installed: J is a comparison map in the proof.

Apply the SAME actual physical top-down decoder and terminal qubit-transfer channel T to G,G',B. Contractivity gives the same comparison norm. Let P_bad be the actual output projector complementary to the target's radius-t module. Its overlap with the decoder-good part acting on G' vanishes by the deterministic quantum intertwiner. If the decoder bad-cardinality map has diamond norm at most b_out, then

    Tr[P_bad T(tau)]
       <= b_c + (1+b_c)(epsilon_synth+b_out).

The left side is an actual nonnegative population; the argument does not assign probabilities to K or G'. A final gentle projection costs at most twice the square root of this bound. This preserves exponentially small support failure when all three scalar terms are exponentially small. It avoids a repeated per-decoding-level synthesis error and also avoids claiming synthesis leakage is a sparse physical Pauli error.

This lemma requires the fixed common decoder INCLUDING syndrome and its product-image property. A decoder that traces syndrome away is insufficient for the reembedding step. These are supplied by the accepted all-logical cross-term sparse-family argument, not by classical-output correctness alone. The computation input here is the declared known target-preparation input, with arbitrary retained bath/reference.
