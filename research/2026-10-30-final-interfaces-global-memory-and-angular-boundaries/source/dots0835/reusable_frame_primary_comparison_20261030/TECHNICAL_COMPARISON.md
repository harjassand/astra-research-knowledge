# Reusable finite-frame controller: primary mechanisms and an equal-access comparator

2026-10-30. **Bottom line:** the credible target is a resource-controlled physical implementation of finite-frame tracking with continuously live native correction—not a new principle of computing during correction, a new moving-code idea, or deep computation obtained by compressing a finite-group command history. This comparison is not a whole-device audit or a priority determination.

Reviewed candidate: `REUSABLE_FINITE_GROUP_FRAME.md`, SHA-256 `eed4c37774097787ecfcbff79791a2444b3f20c2f7afc473248435d8ba876213`. Its explicit example is the six-element CNOT/SWAP group GL(2,2) on two colocated identical CSS blocks, NOT arbitrary transversal H/S or the full Clifford group.

## What the primary papers actually establish

- **Lebreuilly et al. (2021):** Eqs. (7)–(9) construct recovery and a Hamiltonian implementing any specified logical Hamiltonian throughout correctable error sectors. The performance criterion is O(kappa t/R^c) for a specified finite-dimensional Markovian error model. Appendix IV, Eqs. (69)–(70), even moves between copied code/error spaces using an auxiliary gauge degree; that example assumes a naturally noiseless copy. The construction does not itself impose the candidate's fixed native locality/rates or a uniform many-body common-bath threshold. [Full paper, theorem and Appendix IV](https://arxiv.org/html/2103.05007v1).

- **Roy–Wetherbee–Fatemi (2026):** Sec. II, Eqs. (1)–(5), explicitly uses moving code/error spaces, requiring instantaneous correctability, error-space transport and matched logical dynamics. The implemented binomial-code X/H/T gates are approximate photon-loss-semitransparent controls. Sec. IV uses recovery after gate blocks; Appendix A identifies no-jump backaction, imperfect instantaneous correctability and ancillary errors as limitations. Thus this is not the candidate's uninterrupted arbitrary-local-noise theorem; conversely, its non-Clifford control is outside the candidate's finite GL(2,2) capability. [Full v3, Secs. II–IV and Appendix A](https://arxiv.org/html/2603.15356v3).

- **Ordinary frame methods:** Chamberland–Iyer–Poulin explicitly tracks corrections rather than applying them, with Clifford conjugation rules and separate treatment of propagation through entangling/non-Clifford gates. This is a strong conventional baseline, not a strawman applying every known correction physically. [Secs. 2–3](https://arxiv.org/html/1704.06662v2).

- **Earlier ETH body-count arguments** concern direct Hamiltonians acting consistently on static code/error sectors. Grouped multilevel sites plus a moving program–DATA encoding do not contradict those restrictions or establish an elementary-qubit two-body ETH. [Vy–Wang–Jacobs, Sec. II](https://arxiv.org/html/1210.8007v1).

These statements follow from the constructions, equations and limitations in the full texts, not their abstracts.

## What the proposed device really does

Its permanent onsite controlled unitary G gives the exact nominal relation

    G† L_phys(t) G = L_mem + L_prog(t).

The physical command edge contains u_v u_g†, but becomes DATA identity in this fixed representation. This is a covariant subsystem encoding with a relaxing physical frame register. Its strong feature is that the same native memory and forest remain valid through all commands, including stale/coherent program states and clean busy native prefixes. It does not repeatedly assume that the native controller has returned to idle.

This algebra is not literal transparency to every bare physical error: a noisy register change can induce a DATA error in the fixed frame. The substantive protection is supplied by the underlying local-noise memory theorem and by a program-settling tail, not by claiming that arbitrary error operators commute with the command Hamiltonian.

Physical realization is nevertheless distinguishable from merely renaming a classical frame: when registers settle at r_v and native registers are ready, DATA is actually U_v Enc(rho). The fixed ordinary DATA decoder returns the corresponding logical action. The target forest inverse is identity on native-ready states and cannot manufacture that gate from unchanged encoded DATA. It remains an ideal, target-dependent native readout circuit; only the DATA decoder is target-independent.

## Equal-access comparison

**Only a final output is requested.** For relative commands a_1,...,a_K, compute v=a_K...a_1 using the fixed multiplication table. Store the DATA and materialize one U_v at the end—or change compatible measurement bases if that is the allowed output. Finite b and Gamma make this constant-sized state bookkeeping, independent of K. Therefore the absence of a sum of K gate errors is not evidence of superior computational depth: the intended computation has only finitely many distinct endpoints.

**Intermediate physical targets are requested.** A software label alone is insufficient. Both routes must supply actual target states and count transition/settling time and control faults. The proposed continuously live, asynchronously settling implementation is a real engineering/mathematical capability if proved. But a purported conventional lower bound must not artificially deny the comparator the same paired-column joint gates, calibrated external commands or program-controlled interactions.

**If the conventional apparatus is restricted to bare storage plus pulsed gates**, keeping recovery valid throughout a finite pulse is a genuine extra obligation. Do not grant it a free instantaneous transversal gate, ideal forest drain or perfect pause/restart. Conversely, if it is granted the same permanent G-conjugated memory and onsite conditional transitions, it can implement the same construction: the distinction is then implementation/control organization, not a different computational mechanism. No quantitative separation under equal access has been established here.

The new grouped column is a paid resource: it contains both blocks' resource qudits and the program register. This is not remote LOCC, elementary-qubit two-body locality, or a free physical command broadcast.

## Obligations that could produce a larger consequence

1. **A non-deferrable online interface.** Earn protected measurement/feedforward, an addressable operation on varying partners, or a resource-consuming non-Clifford operation, while preserving one fixed ordinary recovery interface and tracking all live native/controller correlations. Intermediate ideal decoding followed by reinsertion is not such an interface. The task should demonstrate a sequence whose required online behavior cannot be replaced by one final finite-group element.
2. **Fault-tolerant command delivery.** Replace the supplied absolute target and bounded waveform with an actual finite-resource local distribution/acknowledgment mechanism. Analyze noisy, delayed and conflicting commands. A wrong common target is a logical instruction error, not a sparse local DATA fault; current local-noise assumptions cannot conceal it.
3. **Scalable partners without hidden growth.** For a CNOT chain on an increasing set of blocks, conjugating X can spread to arbitrarily many blocks. A naive cumulative G then loses bounded support or fixed onsite dimension. An actual local consolidation/deformation/injection protocol, with a uniform memory/noise estimate, would address a hard missing interface. Enlarging a finite register alone does not.

A narrower but worthwhile theorem is the candidate's exact bounded-resource continuously protected finite-frame handoff, including all noisy register transitions, common-bath correlations, stale states and actual finite-rate settlement. Its value should be stated as a physical compilation/robustness result conditional on the strong memory engine. Neither the targeted literature comparison nor the finite-group algebra supports a novelty, universality or practical-advantage claim.
