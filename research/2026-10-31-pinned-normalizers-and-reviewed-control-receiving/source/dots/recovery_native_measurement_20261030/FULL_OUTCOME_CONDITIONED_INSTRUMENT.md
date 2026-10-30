# Binding completion: retained bath and positive outcome-conditioned instrument
2026-10-30. Candidate completion to DESTRUCTIVE_CSS_MEASUREMENT.md. This supersedes any claim there that the retained auxiliary is independent of the outcome. Together with the binding ACTUAL_PROTECTED_ERASURE.md operation/resource/margin, it closes the previously explicit §7 gap, subject to review.

## 1. Rank-one measured logical branches, not an independent-garbage assumption
Let H_M be the ENTIRE logical Hilbert space of the consumed bank (whole-bank Z measurement) or two consumed banks (complete encoded Bell measurement). Write its measured orthonormal basis |z>. Let R contain every untouched logical system and reference. The source provides the accepted common correctable input chart H_M tensor H_aux, with arbitrary correlations of R with M and, where the upstream interface permits, aux. All physical histories retain the same bath; no trace/reset of that bath is inserted.

For each GOOD two-sided coefficient history, the actual physical output has its protected logical outcome equal to z on input |z>. This is the full deterministic branch-intertwining statement from the corrected-word decoder and the good FT common module. It holds for arbitrary ancilla/bath operators, not merely positive path probabilities. All operators on a bad record coordinate are admitted, malformed field values are sanitized, and good tower/gadget logical actions are exact. The final encoded logical output is dephased by a protected copy followed by the ACTUAL_PROTECTED_ERASURE.md finite-reset erasure of the entire copied block, under its strict code margin. A coherent copy retained as garbage is NOT enough. The nominal Markov replacement reservoir is outside the modeled retained finite bath; all other garbage remains retained.

Consequently, in a common protected-output module chart, the COMPLETE good instrument, including retained consumed DATA, work and bath, has the form

 G(rho_MRaux) = sum_z |z><z|_out tensor
        (Id_R tensor K_z)(<z|rho_MRaux|z>).              (1)

The K_z are signed linear auxiliary maps; they may know z and be different for every z. Proof: expand rho in |z><z'|; branch intertwining places the ket in output z and bra in output z'. The actual encoded dephasing eliminates z≠z'. On a diagonal block the input M is one-dimensional, so its remaining linear action can only be a map on aux, tensored with Id_R. This proof requires rank ONE of each measured logical projector. It does not follow from label probabilities alone, nor would it justify the same claim for a partial logical measurement with a multidimensional unmeasured sector.

Earlier capture-local KL identities remain a useful check, but are not needed to assert outcome-independent coefficients after consumed DATA feeds into the bath. In particular an arbitrary later bath operation can use the retained raw outcome. Equation (1), not M tensor one K, is the receiving object.

## 2. Reduced instrument and trace defect
Write actual Phi=G+B with ||B||diamond<=b, using the ONE full-circuit signed sieve. Actual Phi is CPTP. Since trace of (1) is diagonal on M,

 max_z ||K_z^*(I)-I||infinity <= b.                     (2)

For any positive reference-entangled input, rho_z=<z|rho|z> are positive and their traces sum to one. Applying (2) to these blocks shows the reduced good output differs from the ideal destructive logical measurement by at most b; the bad output costs another b. Thus the claimed reduced error remains <=2b, plus epsilon_in. No factor equal to the number of outcomes occurs.

## 3. Positive complete replacement, including outcome-leaking bath
Fix the common output module as a physical isometric embedding J of the protected classical logical register and its syndrome/auxiliary space. It includes the union of admitted hierarchical sparse output histories, with all retained bath and consumed garbage in aux. The good output has support in JJ† on both sides. J is an analysis chart, not a physical decoder. Complete the chart outside the module arbitrarily; compression is enough below.

Define Psi=J† Phi J_in (·) J_in† J, where J_in is the common input embedding; equivalently apply the physical input embedding, Phi, then output compression J†. Psi is CP/TNI. Its signed good part in this chart is (1), and its bad part has diamond norm at most b. For each z define the CP/TNI auxiliary map

 A_z(X)=<z|_out Psi(|z><z|_M tensor X)|z>_out.           (3)

Input preparation and output compression are complete contractions, so

    ||A_z-K_z||diamond <= b  for every z.               (4)

Now set

 G_pos(rho)=J [sum_z |z><z|_out tensor
              (Id_R tensor A_z)(<z|rho|z>)] J†.        (5)

This map is CP/TNI, has the correct rank-one measurement action on R, has genuine outcome-dependent auxiliary output, and remains in the same protected-output module. Its auxiliary branch survival may depend on z; this is priced as a trace defect, not concealed by normalization.

The diamond norm of a classically controlled direct-sum map is the MAXIMUM of the branch diamond norms. Indeed pinching M is a complete trace-norm contraction into the direct-sum algebra, whose trace norm is the sum of block trace norms, and each branch acts on its own output block. Thus (4) implies ||G_pos-G||diamond<=b. Compare DIRECTLY to Phi=G+B, not by separately charging Phi minus its projection:

    ||Phi-G_pos||diamond <= 2b.                        (6)

All embeddings/compressions here are analytical. No actual measurement of virtual fault labels or depolarization is performed. In particular a small bad logical error lying inside the allowed code module is retained in B and bounded; a broad projector is not mistaken for a correct-target guarantee.

The construction uses exponentially many z only as a proof-indexed family. The physical Boolean/GPT circuit computes them without enumerating outcomes; (3)-(5) are not additional physical gates. No exponential outcome factor enters (6).

## 4. Receiver contract and limitations
A subsequent protected processor and native waiting-bank proof may receive (5) branchwise: the historical classical outcome z is an analysis label; the physical protected controls can still fault and must be handled by their own rectangles. Each branch's bath may retain z, raw codeword data and all syndrome work. It cannot contain additional information about the consumed rank-one logical branch beyond what is already in rho_z; Id_R in (5) is the exact statement protecting the still-unknown reference/teleported quantum state.

If the source was only approximately a positive common logical/auxiliary module, add its complete error epsilon_in before applying this construction. If subsequent native waiting dynamics need an energy/BUSY support constraint, verify that the actual-output compression and A_z extraction preserve that separately earned logical-independent cut; no such waiting-bank moment theorem is invented here. The original finite CP-divisible gate/reset/connectivity scope and polynomial potentially enormous costs remain unchanged.
