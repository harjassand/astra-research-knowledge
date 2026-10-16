# Prior-art check: tracked Pauli randomization to local stochastic error effects

2026-10-15. Bounded primary-source extension of PRIOR_ART.md. Literature only; no Willow work or execution of author code. Candidate bridge is still being proved; this report does not certify it.

## Finding

The physical protocol belongs squarely to established randomized dynamical decoupling/randomized compiling: track a random physical control frame and remove it at the output, while averaging over private randomness. Exact Pauli classicalization in the presence of a persistent bath is also prior art. A very close October 2026 preprint explicitly treats Poisson frame refresh and bath-preserving operational suppression.

**No inspected result supplied the proposed spatial all-subset effect inequality with local J, rate γ, and constants uniform in lattice size and bath.** This negative search result is not a novelty verdict. The possible distinction is the combination of that inequality with the local coloring argument, not the physical random-frame protocol or the Pauli-Kraus expansion.

## 1. Closest continuous-process source: He Wang, 2610.01521v1

[Continuous-Process Randomized Compilation for Quantum Process Tensors](https://arxiv.org/html/2610.01521v1). Explicitly inspected v1; [metadata](https://arxiv.org/abs/2610.01521) also lists v2.

Proposition3, Eqs.21–22, gives nonnegative normalized Pauli-history weights under independent whole-interval conjugations. Initial factorization and frame independence are specified. Theorem1 bounds complete adaptive-record error by a control-mixing integral. AppendixJ, Eqs.218–219, specializes to Poisson refresh, including the bound 3g_*²T/λ_r. This is global coupling strength, not a local support parameter. Its finite-width analysis also counts accumulated pulse errors and overlap exceptions. It does not establish the proposed spatial subset bound.

## 2. Non-Markovian RC: watch the definition of “local stochastic”

[Winick, Wallman, Dahlen, Hincks, Ospadov, Emerson, Concepts and conditions for error suppression through randomized compiling, arXiv:2212.07500v1](https://arxiv.org/html/2212.07500v1), §III.2, Eq.2 and Theorem3; §III.3; §III.4.1, Theorem5.

Theorem3 treats a persistent ancillary environment and twirled cycles with gate-independent easy-gate noise. Its term “local stochastic Pauli channel” means a reduced-subsystem Pauli description with environment-dependent coefficients. It is **not defined as** Pr(S⊆supp E)≤p^|S|. The paper also exhibits coherent failure when control-dependent errors reveal a twirl parity to the environment. Its random-decoupling discussion uses a known inverse control sequence and global O(TΔtλ²) error suppression, and connects that protocol to RC.

**Comparison:** close prior for private-control assumptions, classicalization, persistent memory, and physical-frame recovery. It does not provide the proposed spatial support tail or a local, lattice-uniform γ-dependent noise parameter. Do not cite its abstract as though it already proves that stronger support definition.

## 3. Original randomized compiling

[Wallman and Emerson, Noise tailoring for scalable quantum computation via randomized compiling, arXiv:1512.01098](https://arxiv.org/pdf/1512.01098), PRA94,052325 (2016).

This is the established gate-cycle noise-tailoring construction: independent twirls compiled into easy operations, logical compensation, stochastic Pauli noise under the gate-independence assumptions, and bounds for departures from ideal tailoring. It addresses arbitrary Markovian noise, including spatial correlations; merely being Pauli-diagonal does not force high-weight events to be rare.

**Comparison:** the bridge should cite this for noise tailoring, not claim a new realization of stochastic Pauli noise. To derive the desired local support model one must add quantitative local Hamiltonian and control-rate information that a general Pauli twirl alone does not supply.

## 4. Random decoupling in 2005 and the 2006 followups

[Viola and Knill, Random decoupling schemes for quantum dynamical control and error suppression, quant-ph/0511120](https://arxiv.org/pdf/quant-ph/0511120), PRL94,060502 (2005), Theorems1–2 and Appendix.

The logical frame removes the applied controls; their history can recover the physical frame. The open-system theorem gives a worst-case averaged error probability O(TΔtλ²), with bounded joint coupling and no bath-speed term after a bath rotating-frame transformation. The proof uses forward/backward Dyson series and cancellation of isolated random-control insertions. λ is an aggregate interaction norm. Exact finite-separation independence is assumed, unlike telegraph correlations with exponential tails.

**Comparison:** strong antecedent for both the physical protocol and proof strategy. Applying its global bound to a many-qubit register can introduce size dependence; local pulse implementation does not itself convert a global theorem into a support-product theorem.

The relevant 2006 followups are [Santos and Viola, Enhanced Convergence and Robust Performance of Randomized Dynamical Decoupling, quant-ph/0602168](https://arxiv.org/pdf/quant-ph/0602168), PRL97,150501, and [Viola and Santos, Randomized Dynamical Decoupling Techniques for Coherent Quantum Control, quant-ph/0602175](https://arxiv.org/abs/quant-ph/0602175), J.Mod.Opt.53,2559. They study randomized/hybrid protocols, long-time performance and interacting spin registers; the former explicitly uses global fidelity and expected entanglement fidelity. No all-subset stochastic error-effect theorem was identified there. They should not be described as a separate “Viola–Knill 2006” spatial theorem.

## 5. Closest all-subset interface remains AGP

[Aliferis, Gottesman, Preskill, quant-ph/0504218](https://arxiv.org/pdf/quant-ph/0504218), §11.1, Eq.59, provides an all-specified-location bound on coherent fault-path amplitude norms under shared-bath local Hamiltonian noise. It permits arbitrary bath dynamics. It does not supply the random-control improvement or the candidate actual Pauli-effect statement. PRIOR_ART.md gives the exact comparison.

The intended bridge could connect this established locality-of-faults interface to randomized-decoupling suppression, but that connection must be demonstrated rather than inferred from global fidelity.

## 6. Mathematical distinctions the bridge must preserve

The following are assessment points, not claims attributed to a paper:

1. **Joint CP instruments are the safe object.** Twirling a joint system–bath map can give a sum of Pauli actions tensored with bath CP maps. For already correlated system–bath input, the reduced output need not be determined by the two marginals. Work with the joint instrument and effects rather than assert an autonomous reduced Pauli channel for every correlated input.
2. **Endpoint Choi probability versus uniform bath effect.** A normalized Choi trace at one bath state only gives one averaged probability. The sequential product argument needs the relevant effect bounded in operator order, uniformly over the bath/reference and any admissible conditional state.
3. **Spatial probabilities need local structure.** Global Pauli twirling can retain a distribution that assigns a small but fixed probability to a register-wide Pauli. Pauli diagonality alone cannot prove p^|S| tails. The local Hamiltonian decomposition and separated-guard argument carry this burden.
4. **Specify the Poisson law and rate.** Uniform Pauli redraw at rate λ, deterministic multiplication by an involution at rate γ, and independent X/Z clocks are different generators. A nontrivial telegraph character under involution flips decays at 2γ; a uniform refresh character decays at λ. Factors of two cannot be transferred between protocols silently.
5. **Fresh seeds are not fresh baths.** A per-block effect inequality uniform over conditional bath states can support multiplication by conditioning. An unconditional error probability or a fresh random seed alone cannot. Ideal inter-block correction and any public record must preserve the stated conditioning interface.
6. **Seed coarse-graining is substantive.** The ensemble guarantee need not hold conditioned on a particular complete control trajectory. Distinguish secrecy from an adversarial/control-dependent Hamiltonian, discarding the classical seed from the output, and the physical bath learning something about past controls through allowed interactions. The last phenomenon is compatible with a fixed laboratory Hamiltonian and must remain inside the joint proof.
7. **The lift is a representation, not extra hardware.** P_D⊗P_R^T commutes for Pauli labels because the phases cancel. Dephasing in this lifted error representation does not mean untracked physical stabilizer dephasing protects all quantum information.
8. **Coloring loss needs explicit hypotheses.** For p=q^(1/χ), require q≤1, a verified largest separated class of at least |S|/χ, and an implication from every physical support event to the grouped lifted endpoint event. State how χ depends on interaction range/degree and whether unions over Pauli labels contribute factors.

## Scope and stopping point

Read targeted primary sources on continuous-process RC, persistent-bath RC, random decoupling, and local fault-path bounds. No inspected theorem matches the proposed bath-uniform spatial subset product and coloring bridge. Existing work already covers most surrounding mechanisms. No public novelty claim, hardware advantage, or whole-memory threshold is supported by this literature pass.

## Latest-version check: 2610.01521v2 (supersedes v1-only comparison)

Checked 2026-10-15. arXiv lists v1: 2026-10-01 11:55:16 UTC; latest v2: 2026-10-03 00:15:37 UTC. [v2 full text](https://arxiv.org/html/2610.01521v2).

V2 adds Theorem1/AppendixH.3: full trajectory-averaged, trace-closed cPT Fock-norm convergence for a fixed finite system, interval, and operation basis. The coefficient majorant is bath-dimension independent, but its summed tail contains q=d_S^4−1 (Eqs.193–198); this is not spatial lattice-uniformity. No general convergence rate is supplied there.

The operational theorem is now Theorem2, Eq.33. Its clarified assumption is initially independent, autonomous no-feedback control; generated records may correlate with control. AppendixJ retains the global Poisson bound, now Eqs.232–233. No spatial all-subset/local-interaction-norm or randomizer-character joint-effect product was located in the theorem statements, proof sections, or targeted text search.

Comparison to the team's newly supplied additive private-sign extension: the unresolved distinction remains a finite-time product of selected Fourier-character error effects uniform over arbitrary sign-independent base evolution. Fock-sector insertion counts are not spatial error-support counts. Conditioning external geometry while averaging internal telegraph clocks must remain explicit. This extension was reported by the team, not independently proved in this literature check.
