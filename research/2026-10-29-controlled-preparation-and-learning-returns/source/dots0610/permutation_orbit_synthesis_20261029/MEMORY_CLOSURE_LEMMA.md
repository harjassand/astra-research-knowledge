# Full coarse memory closure after private permutation retirement
2026-10-29. Root independent derivation; communicate to theorem/review authors.

Write the physically twirled joint source T(X)=E_g (Uout_g† tensor I) N((Uin_g tensor I)X(Uin_g† tensor I))(Uout_g tensor I). Tracing physical output removes the output permutation. Since Uin is irreducible, its uniform conjugation is the completely depolarizing map. Therefore EXACTLY, for every correlated LM operator X,

 Tr_H T(X) = Tr_H N((I_L/d) tensor Tr_L X) = B_total(Tr_L X).

This direct first-moment proof needs no claim that refined Kraus labels are independent and no simultaneous diagonalization. If T=id_embedding tensor B_good + T_bad is the independently derived CP split, subtracting its good memory marginal gives

 Tr_H T_bad(X) = (B_total-B_good)(Tr_L X) = B_bad(Tr_L X).

B_bad is CP because it equals the memory output of the CP map T_bad on I/d tensor an arbitrary memory state (including a reference). Thus BOTH coarse branches have exact CP memory closure. Restricting to a proper subcode by W and applying any TP output decoder preserves this identity.

For a sequential use on separate outer-code positions, each coarse branch therefore updates memory by a fixed CP map independent of that position's logical content, even when that position is entangled with memory and the remaining code blocks. Tests are fresh-data operations and also define CP maps on memory. Composing the coarse CP memory maps gives the actual accepted memory map B_acc, not a dummy-input substitute. Outcome probabilities are independent of an initially independent logical payload; when initial logical and memory systems correlate, postselection can still steer the logical marginal, precisely as id_logical tensor B_acc predicts.

For every path containing at most t bad native locations, expand joint Kraus operators: good locations are identity on their data blocks, so errors act only on those t blocks plus memory. An actual outer code correcting arbitrary t-block operators restores identity logical action tensor a memory map. TP recovery cannot alter the path's memory marginal, so that path's map is exactly its coarse memory-map composition. On the union of paths with more than t bad locations, let actual map be Phi_bad and memory map B_bad_acc. If the uniform hazard proof gives Tr Phi_bad(rho)<=epsilon for all states, equivalently its effect<=epsilon I, then both Phi_bad and id tensor B_bad_acc have diamond norm<=epsilon. Hence halfdiamond(Phi_acc - id tensor B_acc)<=epsilon. There is no need to assume latent Pauli errors or to replace the actual accepted memory map by a dummy one.

Output scope: M means the source memory and pre-decoder classical test/controller history only. Outer decoder syndrome, reset trash, private permutation keys and key purifications are retired. Newly exposed decoder syndrome is not part of the pre-existing memory marginal: on uncorrectable paths it can depend on payload, so a larger-output target needs the separately justified dummy-simulator fallback instead of the same actual memory filter.

Outstanding: rigorous independent sequential hazard transfer and initial-correlation conventions, finite instruments/control implementation, and explicit computational comparison. Exact private key retirement is essential. Exposing the key later is not covered by the coarse channel.
