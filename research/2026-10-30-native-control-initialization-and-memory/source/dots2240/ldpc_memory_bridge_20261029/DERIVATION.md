# Autonomous SSF DATA bridge: proved foothold and precise unresolved lemma
2026-10-29. Research note, not a scalable-memory claim.

## Verdict
A natural local channel for the current compiler is **small-set-flip (SSF), with read-footprint locking**. It avoids detailed balance and is implementable with fixed finite workspaces on a bounded-degree interaction graph. There is a rigorous stopped syndrome-drift estimate against continuing nonthermal Pauli jump noise, and a deterministic finite-fault work/footprint bound. Neither establishes scalable quantum memory. The exact missing step is a **composable spacetime residual-DATA support bound for asynchronous, finite-duration SSF transactions with controller faults**, not another controller-flag density bound.

## Strong baselines (read before novelty claims)
1. Hong–Guo–Lucas, https://arxiv.org/html/2403.10599v3, Appendix B.3 and E.1–E.3: their thermal result uses confinement plus cluster counting. Equation (48) defines z=e Δ_C(Δ_B+Δ_C−1); the stated critical bound is β_c≤3 log(2z). E.3 compensates calibrated incoherent errors by adjusting rates to restore Gibbs stationarity. This is not a theorem for uncalibrated time-dependent noise interspersed with finite-duration compiled transactions. E.1 explicitly neglects gate duration in its Lindblad identification. Their geometric-range warning appears in the introduction.
2. Tamiya–Koashi–Yamasaki, https://www.nature.com/articles/s41567-025-03102-5, and supplement https://media.springernature.com/original/springer-static/esm/art:10.1038%2Fs41567-025-03102-5/MediaObjects/41567_2025_3102_MOESM1_ESM.pdf: ordinary SSF already supports constant-time error reduction, including finite classical runtime. Supplement §II assumption 5 assumes noiseless classical computation; §IV Definition 5 demands support-tail reduction, not just weight contraction. Partial circuit reduction handles correlations with surrounding gadgets. Arbitrary-pair quantum gates are allowed. A noisy autonomous processor result would add something, but merely removing explicit measurements does not establish that result.
3. Midha–Abanin, https://arxiv.org/html/2609.38139, main preliminaries and discussion: perfect-syndrome, Z-only code-capacity noise; errors are sampled at time zero, with no further noise during decoding. They explicitly identify online decoding as future work. Thus their autonomous BP evidence does not supply the needed online memory theorem.
4. Fawzi–Grospellier–Leverrier (FGL), https://arxiv.org/html/1808.03821, Proposition 14 and Lemmas 15,31–33, is the direct combinatorial input below. It provides many good flips, confinement, and a parallel-round witness argument. The latter uses a fixed noisy syndrome and complete color sweeps. Replacing these by continuously arriving noise and a random finite-duration scheduler requires a new witness argument.

## 1. Exact local SSF channel to request from the compiler
Work in one CSS sector. Let g be a stabilizer generator of the opposite type, A_g its constant-size support, and F⊆A_g an allowed SSF subset. Define B_g as the set of checks that can be changed by any such F, and

 R_g = A_g ∪ ⋃_{c∈B_g} supp(c).

All sizes and incidences are constants for a fixed-degree code family. The hub must lock **R_g**, not merely A_g or F. Extract the commuting checks in B_g to fresh workspace, compute an accepted F from a fixed finite truth table, apply X_F, then reset workspace. Accept only when

 Δ(σ,F)=|σ|−|σ⊕σ(F)| ≥ β |σ(F)| > 0.

The predicate uses only B_g. A deterministic best accepted candidate is possible; alternatively a fixed candidate may be sampled from a finite set. On a syndrome-diagonal Pauli-error trajectory this is precisely an SSF transition. The syndrome extraction only reveals stabilizer information, not logical information. A finite circuit can be realized via private workspace and one resource at a time, matching the current two-site-qudit convention. No elementary-qubit gate-count improvement is claimed; the truth-table dimension may be enormous but size-independent.

Read-footprint reservation matters. In the test below, checks with binary support masks (111,111,001,010), initial error 100, and disjoint flips 001 and 010 have syndrome weights 2→1 individually, but 2→4 if both decisions use the old syndrome. This is a generic stale-read counterexample, not an HGP threshold counterexample. Exclusive write locks alone do not preserve descent. Locking R_g excludes conflicting reads and writes. Opposite CSS sectors also need physical-gate ownership although their ideal stabilizer observables commute.

For clean transactions with all read resources reserved, completion histories may be serialized to exact local SSF channels. This says nothing about output at a wall-clock instant with incomplete transactions. A finite-rate readout/drain or a dressed-data decoding interface must be supplied separately.

## 2. Proven finite-fault work budget (no Poisson hypothesis)
Consider an arbitrary serial history of correct accepted SSF flips, interspersed with M arbitrary Pauli faults. Each fault affects ≤s data qubits; each accepted correction affects ≤w. Let Δ_q bound checks incident on one data qubit. Let S_t=|σ(E_t)| and m=|E_0|. Every accepted correction lowers integer S by ≥1; every fault increases S by ≤b=Δ_q s. Therefore the number K of accepted corrections obeys, on every prefix,

 K ≤ S_0+bM ≤ Δ_q(m+sM).

For U, the union of initial-error support, fault supports, and all correction supports,

 |U| ≤ m+sM+wK ≤ (1+wΔ_q)(m+sM).                 (1)

This is deterministic, schedule-independent, and nonthermal. It explicitly charges DATA damage, not controller flags. The stronger potential accounting Σ_corrections β|σ(F)|≤S_0+bM also follows.

Consequences: if total seed/fault support in an isolated history is below γ_0√N/(1+wΔ_q), the actual error and exploration remain in the FGL small-error regime. After the last fault, fairness and the good-flip lemma imply eventual zero syndrome; if the explored support stays below code distance, the final zero-syndrome error cannot be nontrivial logical. This is a finite-burst recovery statement, NOT a constant-rate online threshold: total fault count grows as Nt under extensive continuing noise.

Noisy syndrome decisions that execute a non-descending flip must be counted as faulty local events in (1). Reusing one corrupted local controller for many outputs is not one event unless its full active duration and spacetime support are charged. Arbitrary coherent faults are not Pauli events without an additional reduction.

## 3. Proven drift for an IDEAL atomic random-SSF comparator
This is a comparator, not an identification of the compiled controller's physical generator.

Assume independent candidate clocks, each with rate at least λ>0. At a ring, apply F iff its current true syndrome satisfies the accepted condition. Distinct candidate subsets can have separate clocks; there are only O(N) of them, with constants possibly exponential in check weight. FGL uses expansion δ<1/16 and 0<β<β_1=1−16δ. Put β_0=1−8δ and c_1=(β_1−β)/(β_0(1−β)). Until reduced error weight exits γ_0√N, Proposition 14 with D=0 gives

 Σ_{F good}|σ(F)| ≥ c_1 S.

Consequently the correction generator satisfies

 L_corr S = −Σ_{F good} λ_F Δ(σ,F) ≤ −aS,
 a=λβc_1>0.                                                   (2)

If there are ≤νN nonthermal fault channels, each a support-s Pauli jump with possibly history/time-dependent intensity ≤ε, then

 L_total S ≤ −aS + νN ε Δ_q s                                (3)

inside this basin. One may instead assign each generator a rate λ_h and pick uniformly among ≤M_0 candidate subsets; then use λ=λ_h/M_0. A best-candidate rule can only help compared with its averaged candidates.

For the process killed on exiting the basin at τ, let f(t)=E[S_t 1_{t<τ}]. Since killing removes a nonnegative contribution, (3) gives

 f(t) ≤ e^(−at) S_0 + (νN ε Δ_q s/a)(1−e^(−at)).              (4)

With zero noise and the finite-work basin guarantee, P[S_t>0]≤S_0e^(−at), hence clearance time tail is exponential after O(log S_0) time. With ongoing noise, (4) is only a killed syndrome-density estimate. It neither bounds P[τ≤t] nor controls logical information. Confusing it with either would be a substantive error.

The actual coherent finite-duration controller has refractory periods, locks and hidden prefixes. Its completions do not have independent constant-rate Poisson hazards. Equations (2)–(4) cannot be substituted for its generator. A successful local-path probability can potentially replace the clock assumption in a BLOCK argument, but must be proved jointly for separated regions, uniformly in legal competing histories.

## 4. Exact remaining bridge theorem
Fix a constant block duration T, and include data, syndrome workspace, control, locks, monitors, resets, and communication in one bounded-degree spacetime graph. To conclude high-rate memory, one sufficient theorem is:

(A) The noisy compiled evolution admits a joint local-fault expansion with bounded spatial spread and exponentially decaying temporal tails; faults of separated spacetime regions satisfy a product-type bound. Clearing an owner flag alone is not (A).

(B) The asynchronous SSF DATA map over T maps a joint locally stochastic residual-error/ambient-fault class below p_* to the same class with strict slack, e.g. residual parameter q_*<p_* after incoming block noise is included, while logical-failure probability per block is ≤C N exp(−c√N). This must be composable jointly with untouched future/exterior faults, not only a statement conditioned on a block-local success event. A witness proof should charge each surviving reduced-DATA set either to enough fresh bad spacetime cells or to sufficiently many missed opportunities; (1) supplies spatial work control and (2) suggests erosion, but neither supplies these witnesses.

(C) Final readout handles unfinished good and bad transactions locally without unbounded waiting or hidden perfect processors; both CSS sectors and arbitrary logical/reference input states are covered.

If A–C hold, induction over blocks with a union bound gives decoded logical failure ≤(t/T) C N exp(−c√N), and N physical data plus O(N) fixed-size controller/reset sites store Θ(N) logical qubits. This is a conditional implication, not a proved result here. Finite-energy extraction/pumping and all reset power scale extensively.

The hard point is B. FGL's parallel proof charges a candidate destroyed before its scheduled color to earlier beneficial flips, with a fixed syndrome-error set. In the present setting the syndrome changes from new noise, reads take time, and scheduling failure has temporal correlation. The previous proof does not apply verbatim. The known circuit baseline solves a different, clocked/noiseless-processor composition problem.

## 5. Exact obstructions to shortcuts
- Sparse controller defects do not imply sparse residual DATA errors, even after all flags clear.
- Small syndrome expectation does not imply good memory: every logical Pauli has zero syndrome, and rare basin escape is precisely the event needing control.
- An expected multiplicative decrease is not a support-tail theorem. Distribution: E equals one fixed logical support L with probability p, and is empty otherwise. Every marginal is ≤p, but P[L⊆E]=p rather than p^|L|; its syndrome is always zero.
- Globally applying (3) fails at fixed ε and large N: the floor is Θ(εN), larger than the √N confinement scale. Cluster-local analysis is essential.
- Finite local diamond-norm perturbations can be coherent/non-Pauli. Converting them to stochastic Pauli support probabilities is an extra assumption or theorem; a norm fault-path proof would need a corresponding amplitude-summability version of A/B.
- HGP expander incidence is graph locality, not fixed-dimensional geometric locality. Locking full read footprints keeps graph degree bounded but does not provide wires, bandwidth, routing time, or clean syndrome hardware. Geometric routing overhead can destroy constant time and rate.

## Validation and failure log
`check_work_budget.py` exhausts 154,308 prefixes through six events on a three-bit repetition syndrome graph and verifies (1), then checks the stale-read counterexample (syndrome weights 2,1,1,4). This validates accounting and the counterexample, not an HGP theorem.
An initial attempted repetition-code stale-read example falsely claimed a logical final error; its assertion failed. It was discarded and replaced by the explicit energy-increase example. No threshold simulation was run. All cited governing passages were accessible; no blocked or uncertain external mutation occurred. No publication or repository push was made.
