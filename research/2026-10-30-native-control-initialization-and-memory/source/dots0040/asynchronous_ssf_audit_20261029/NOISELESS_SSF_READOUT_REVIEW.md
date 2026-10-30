# Independent review: polynomial-time ideal SSF readout
2026-10-29. This is an additive review; accepted compiler manuscripts were not edited.

Reviewed source:
`producer-workspace/NOISELESS_SSF_READOUT_CANDIDATE.md`
SHA256: 10d138825580018b8ae5b07daa73bd26b4cea5d928d287911a299153f04a1185.

## Verdict
**Valid under the accepted sectorwise D0/D1 and transactional composition premises.** The candidate replaces the possibly expensive minimum-syndrome recovery by a polynomial-time ideal mathematical SSF recovery without requiring a probabilistic quantum residual law. I found no failure in the nonzero-syndrome stopping argument, virtual representative substitutions, roots in appended decoder blocks, or the positive certificate count.

This does not establish a noise-tolerant physical readout with O(N)-time classical latency, and does not provide arbitrary quantum retrieval during continuing noise. The candidate correctly separates those tasks.

## 1. Exact channel represented by the appended history
The terminal full-syndrome measurement is part of the proposed recovery channel. Conditional on a full outcome sigma, the DATA lies in that full syndrome sector, possibly entangled with a retained bath. A Pauli correction P_F sends that whole sector to sigma XOR syndrome(F). Every later local syndrome query in the deterministic decoder therefore has a definite outcome on that sector.

Consequently, after the one full snapshot, appending local ideal syndrome-evaluation instruments and their immediately applied corrections has exactly the same DATA/bath action as classically updating sigma and applying the one accumulated Pauli mask at the end. There is no additional dephasing inside a fixed measured syndrome sector. This establishes the equivalence for coherent Pauli expansions and bath entanglement, not merely classical Pauli mixtures.

The full syndrome measurement has not been inserted into the memory interval. It occurs only at the specified terminal mathematical output after F^dagger. That distinction is necessary.

## 2. Complexity and guaranteed stopping
Let n_chk count both CSS sectors' check bits in the syndrome-weight potential. Every accepted move lowers this nonnegative integer by at least one, and the other CSS sector's corrections preserve it. There are at most n_chk accepted moves total.

Every productive scan contains at least one accepted move, so at most n_chk productive scans can occur. Within n_chk+1 complete scans there is a no-change scan. Once a full scan makes no change, the input syndrome to every hub is the same; repeating the same deterministic scan can make no change either. Padding to a multiple of R is safe.

A hub has only a fixed finite candidate family for a fixed-degree code. Thus scanning O(N) hubs costs O(N) elementary classical work, with possibly large code-dependent constants. The naive SSF work is O(N n_chk)=O(N^2). Gaussian elimination/Clifford stabilizer decoding adds polynomial work and an ideal polynomial-size circuit; no claim of efficient noisy physical implementation follows.

A constant-depth colored ideal scan is available if the fixed order is chosen compatible with the conflict coloring. It need not reproduce an arbitrarily prescribed serial permutation. Parallel depth is not needed for the accepted polynomial-work claim.

## 3. Why a stuck nonzero syndrome forces cutoff badness
Apply the same branchwise representative gauge after every complete physical or appended proof block. Good blocks have components below both the FGL small-error cutoff and code distance, so their original error and chosen sector representative differ by stabilizers. This equivalence preserves all syndrome-dependent decisions of the actual deterministic decoder, without requiring the decoder to compute those representatives.

Suppose no cutoff-bad block occurred and the final no-change scan has nonzero syndrome in one sector. The final canonical sector representative has that syndrome and is contained componentwise in the last good enlarged support. At least one component has nonzero syndrome and weight below the FGL cutoff. Proposition 14 gives an accepted candidate there. The full read-footprint/check adjacency prevents other components from modifying that candidate's syndrome evaluation; it is globally accepted. Because the final scan evaluated every hub and made no changes, it must have executed such an accepted correction, a contradiction.

Thus the syndrome is zero. The canonical sector representative is then empty, and the actual branch error is a stabilizer by the chain of good-block gauge equivalences. This proves success of the ACTUAL computed SSF correction, not success of an unperformed minimum-weight correction. Apply the same argument to both sectors.

## 4. First bad roots and terminal locations
Every accepted move in an appended scan is a correct SSF event. There are no bad insertions and no missed opportunities in such a scan, so Q=M=0. The deterministic finite-work bound and backward dichotomy remain applicable even though these are proof-time rather than physical-time blocks.

If the extended history first becomes cutoff-bad in an appended block, D0 supplies its root exactly as for a physical block. The backwards chain cannot terminate in any appended layer: the required fresh positive density is impossible with Q=M=0. It must reach a genuine physical terminal obstruction, or contradict the exact initial codespace.

The artificial layers have the same bounded-degree spatial graph and nearest-layer vertical edges. Connectivity and the terminal-volume estimate therefore remain valid. For a fixed certificate with physical earliest layer, its positive event is bounded by the already accepted physical-record moment; any certificate whose earliest layer is artificial has probability zero. Rooting across L+J possible layers, J=ceil((n_chk+1)/R), gives the stated bound

  ||E_efficient-dec-id_L||_diamond
  <=2 min{1, 2(L+J) R N r^ell/(1-r)}.

J=O(N) changes only a polynomial prefactor. It does not introduce a Pauli-label union, noise-free PHYSICAL storage periods, or a new quantum residual distribution.

## 5. Quantum and operational scope
All coherent branches with the same terminal full syndrome use the same deterministic correction. Every branch outside the physical certificate event has correct logical action; the common-correctable-span/CP-effect argument from the accepted composition proof applies unchanged.

The final channel still requires an ideal terminal F^dagger, complete syndrome snapshot, reliable classical computation, application of its Pauli correction, and stabilizer-code decoding. While the abstract channel is efficient, the physical autonomous system continues to evolve during real classical processing. Its noise cannot be dropped simply because the correction mask was computed from an earlier snapshot. Stopping/draining/switching controls, output noise and quantum-state retrieval require a separate theorem.

No complete destructive CSS readout candidate existed in the shared directory at the time of this review. This verdict does not cover an unwritten destructive-readout protocol or infer one from the ideal channel.

## Access and changes
Read the candidate and used the previously reviewed deterministic/composition premises. Wrote only this independent review. No accepted manuscript was edited, no external mutation occurred, and no access was denied.
