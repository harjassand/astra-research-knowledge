# Binding actual logical-erasure lemma
2026-10-30. Reviewer construction to close the retained-copy blocker.

Let a fixed computation code V have distance d. The incoming working-period module is the linear span of E_a V with weight(E_a)<=r on its child symbols. Let S include EVERY child whose old symbol can survive in any retained system, including bad resets and malformed-input refresh work, with |S|<=b. Every other GOOD child reset is an actual lower-level replacement channel on that child's logical symbol, tensored with a syndrome/environment map that does not retain its old logical symbol. Survivor branches may keep all information in their b input child symbols, with arbitrary shared bath coupling. Assume

    2r+b < d.                                          (E1)

For any operator A on the survivor child subset S, |S|<=b,

    V† E_b† (A_S tensor I) E_a V = c_ab(A) I_L,          (E2)

because the operator has support at most 2r+b<d. Duality therefore gives

 Tr_(S complement)[E_a V |z><z'| V† E_b†]
       = delta_(z,z') tau_ab,S,                         (E3)

with tau independent of z. The entire surviving system, including arbitrary coefficient baths, is independent of the input logical state. Resetting all nonsurvivor children has thus genuinely ERASED the old logical information, not merely transferred it to retained work. Subsequent preparation of encoded zero preserves that independence. The argument is two-sided and linear, so applies to signed good histories; no fault trajectory is measured.

Base case: the supplied exact target replacement channel R on a physical symbol discards that symbol's old state into an inaccessible Markov reservoir and leaves modeled retained bath untouched. Actual finite replacements differ by the accepted delta and are counted in the cavity faults. This explicit reservoir exclusion is necessary: a unitary implementation retaining every reservoir would not erase the global state.

Induct recursively, applying the lemma to good logical-reset modules. Include input refresh, child resets and known-zero preparation as finite actual circuits; all retained scratch/garbage that might contain old symbols must be reset or included in the survivor-support accounting. Conservatively, malformed incoming children may transfer their old symbol to retained refresh work and must be added to S. With r<=k ell and at most k newly bad child resets, take b<=r+k. The strict choice d_c>=2k ell and code distance d>=2d_c+1 ensures 2r+b<=3r+k<=4k ell<d (ell>=1). Increase the fixed computation-code parameters if necessary; do not silently use the weaker k ell<=d_c without checking E1.

A protected outcome-dephasing module can now CNOT the protected classical label into a zero encoded ancilla and execute this actual logical erasure on the ancilla. Good histories implement genuine dephasing even when every other consumed DATA/work system and the modeled bath is retained. The inaccessible replacement reservoir receives the erased coherence. The module's full faults, including physical finite-reset residues, are part of b_comp.

This lemma supplies the missing deterministic receiving statement. To claim its threshold strength x_j, use actual disjoint reset/preparation rectangles with the corresponding finite A and spread/margin constants; no numerical threshold is certified here.
