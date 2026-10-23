# Reversible compression incumbent check

## Verdict

Neither of the two closest primary constructions supplies a faster, fully charged construction under the opening's fixed 1D nearest-neighbor gate/time contract. The strongest *local reversible* incumbent is the recursive 3-bit reversible polarization-compression (RPC) step, which is the same majority recursion used by the opening. Schulman–Vazirani provide a more general, no-clean-bit reversible compression algorithm, but their stated quality is polynomially small error, and their linear-time improvement assumes extra tape/QCA primitives rather than the specified fixed gate schedule. This is an incumbent check, not a no-go theorem: an efficient reversible implementation of a larger-block majority/source-compression permutation remains an open adversarial candidate.

## Primary source 1: Kaye, “Cooling algorithms based on the 3-bit majority” (2007)

[arXiv:quant-ph/0703194](https://arxiv.org/abs/quant-ph/0703194), especially §§1–4.1 and 4.2.

- The stated model asks for cooling without clean ancillas or measurements; the source assumes independent, identically biased input bits for its analysis (§1, lines 48–55; §3, lines 89–93).
- Claim 1 states that, among permutations on an odd block that maximize the bias of one output bit, encoding the block majority into that bit is optimal (§3.2, lines 119–125).
- The three-bit RPC map computes majority into its target, with bias update \(B'=(3B-B^3)/2\) (Eq. 8). Writing \(B=1-2\epsilon\) gives exactly \(\epsilon'=3\epsilon^2-2\epsilon^3\), the opening's recurrence.
- Its simple closed-system recursion partitions the bits into triples, keeps the majority bit, and recurses (§4.1, Eqs. 10–13). At (L=3^k), this is the same logical recursion and therefore the same \(-\ln\epsilon=\Theta((2^k))=\Theta(L^{\ln2/\ln3})\) scaling. The two other bits are described as “discarded”; a closed implementation can keep them as dirty syndrome data, but no entropy is removed.
- Crucially for cost comparison, Kaye says a time estimate must specify the model and account for moving/shuttling states (§4.1, line 167). It does not give an NN depth or faster no-reset schedule. The opening's explicit routing/depth analysis supplies that missing physical compilation cost; it does not improve on the incumbent's basic 3-bit compressor.
- Kaye's much faster numerical cooling rates in §§4.2 and 4.3 use a heat bath that resets heated bits (e.g. §§4.2 lines 168–185). Those are outside the no-bath, no-reset contract and cannot be counted as closed reversible compression.

## Primary source 2: Schulman and Vazirani, “Scalable NMR Quantum Computation” (1998 preprint; STOC 1999 extended abstract)

[arXiv:quant-ph/9804060](https://arxiv.org/abs/quant-ph/9804060), especially §§1–3 and the architecture section.

- This is a genuine stronger reversible-compression incumbent: it explicitly forbids clean workspace, describes initialization as a permutation of computational-basis states, and uses no bath reset in the compression phases (§§1–2, lines 63–86). For iid input it can extract \(\Theta(\epsilon^2 n)\) highly biased bits; its third phase gives per-bit dirty probability \(\delta<n^{-10}\) and probability at most \(n^{-9}\) that any output bit is dirty (lines 191–212).
- Its original one-tape estimate is (O(n^2)) primitive steps; the two-tape architecture reports (O(n^{4/3})), and a further two-tape-plus-QCA enhancement claims linear time (lines 151–158, 193–204, 246–257). Those are source-model step bounds, not an acquired compilation into the opening's fixed SWAP/CNOT/controlled-(V) alphabet with a per-bond (J) limit. The proposed implementation uses cyclic tape shifts, a distinguished tape-head site, and in the linear-time variant parallel cellular-automaton/global-rotation primitives (lines 218–256). Its time claims therefore need a separate compilation before transferring them to the current contract.
- Even accepting its strongest stated linear-time variant, its guarantee is polynomial, \(n^{-10}\) for one bit / \(n^{-9}\) for the whole output block. For (T=\Theta(n\hbar/J)), this is asymptotically much larger than the opening's \(e^{-cT^{\ln2/\ln3}}\) upper error. It produces many useful near-pure bits and is a better yield result, but does not beat the selected error-versus-time exponent.
- The paper uses external random permutations/binning for locally correlated inputs, while its operations are oblivious and deterministic once the tape motion is fixed; for the opening's iid source the initial shuffle is expressly unnecessary (§3, lines 94–100; §2, lines 169–170). This is not by itself a hidden measurement/reset, but the architecture and scheduling assumptions remain distinct.

## Remaining strongest attack

Kaye's optimality claim makes the block majority the best possible *single output bit* among arbitrary reversible permutations of a block, but it says nothing about the locality/time cost of implementing that larger-block permutation. The primary sources checked do not establish whether a reversible, no-clean-ancilla majority/source-compression circuit over the fixed NN gate alphabet can achieve \(\epsilon(L)=e^{-\Omega(L)}\), or any exponent beating \(L^{\ln2/\ln3}\), in (O(L)) time. If such an implementation exists, the general wrap \(P^{-1}\,\mathrm{shift}\,P\) can use its extracted (q) even if it does not preserve the opening's complement-pair syndrome property; under the parent-provided bound, its site mismatch is at most \(2\epsilon(1-\epsilon)\). The opening should thus claim a fully local implementation and a matched resource theorem only, not optimality among all reversible compression maps.
