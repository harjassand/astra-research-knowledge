# Astra Scientific Information Genesis
## Condition-matched, reference-preserving exchange

Date: 15 October 2026

**Status:** An explicitly specified candidate extension of established multi-copy decorrelation. The acquisition identity below follows under stated resource assumptions and has finite numerical checks. Historical novelty, an acquired bath-safe implementation, economic advantage over the strongest baselines, and a consequential real-device decision are **not established**. This is not a demonstrated new scientific capability and not a claim of a civilisation-scale advance.

This checkpoint is a local research artifact. It has not been committed to GitHub. Astra repository context was read at revision `1c45f77e32d6fbd72483aed5014061c7bda4f372`. No unreviewed repository theorem is required in the construction. OpenAI/math was consulted for orientation; no result from it is claimed as a prerequisite or validation.

## 1. Scientific decision and why this operation was considered

Target a memory-bearing quantum processor or quantum simulator with an accessible data register S, an already recorded classical condition C, and inaccessible degrees of freedom E that can affect subsequent performance. A reference R, when used, verifies preservation of quantum information in S. Examples of C include an actual measured syndrome or an externally recorded preparation condition. C is not assumed to identify a microscopic state.

The target question is not whether correlations exist. It is whether associations between (R,S) and E **beyond the recorded C** are responsible for the ranking of two actual continuation policies a and b. For example, should a calibrated controller preserve an impending environmental return or suppress it? The intended performance measure is a bounded success score on a specified workload, not an entropy reconstruction.

The operation considered is an intervention on which data register meets which environment. It is not relabelling already measured data. It requires physically exchanging quantum states between independent prepared replicas, while following each state's original reference.

This scientific attribution is distinct from selecting between already executable policies. A direct randomized comparison is already sufficient to choose between those policies on the tested workload. The candidate must eventually justify an extra decision: whether conditional routing, altered memory suppression, or a revised control design improves a held-out workload after all costs. A control-ranking reversal alone is not evidence of such an advantage.

## 2. Closest prior art and novelty boundary

1. G. Coeuret Cauquil et al., *Irreversibility of decorrelating processes: an experimental assessment in cavity QED*, arXiv:2601.07011, v2 (25 May 2026), https://arxiv.org/html/2601.07011v2. Explicitly discusses and experimentally implements two-copy subsystem recombination to access complete decorrelation. Thus exchanging replicas to obtain product marginals is not a new invention here.
2. M. Berta, F. G. S. L. Brandao, C. Majenz, M. M. Wilde, *Conditional Decoupling of Quantum Information*, Physical Review Letters 121, 040504 (2018), arXiv:1808.00135, https://arxiv.org/abs/1808.00135. Conditional erasure is itself an established information-theoretic subject. Its existence precludes a generic novelty claim about removing conditional correlations.
3. A. Sander et al., *Quantum non-Markovian response spectra*, arXiv:2610.10684 (initial submission 7 October 2026), https://arxiv.org/html/2610.10684v2. Uses system-only history/future interventions to diagnose hidden environmental memory without demanding complete process tomography. Such targeted methods, not only exhaustive tomography, are a necessary comparator.
4. H. Liu et al., *Realizing Universal Non-Markovian Noise Suppression*, arXiv:2511.20304, https://arxiv.org/html/2511.20304; journal result *Experimental Demonstration of Calibration-Free Non-Markovian Noise Suppression*, DOI 10.1103/77n6-slpf (2026). Uses Pauli twirling, auxiliary registers, controlled swaps and postprocessed observables. Comparisons must include its sampling normalization, gate overhead and applicable noise assumptions. The phrase "without reconstructing the noise" is not a novelty claim.
5. D. Bluvstein et al., *A quantum processor based on coherent transport of entangled atom arrays*, arXiv:2112.03923, https://arxiv.org/html/2112.03923v1. Demonstrates useful transport/control components, not a certificate that a proposed routing operation leaves an inaccessible environment intact.
6. P.-A. Mortemousque et al., *Enhanced spin coherence while displacing electron in a 2D array of quantum dots*, arXiv:2101.05968, https://arxiv.org/abs/2101.05968. Physical motion as noise control is an established competitor, not an invention of this checkpoint.

The narrower retained formulation combines conditioning on an actual classical record, preservation of the data-reference marginal by reference tracking, finite-batch treatment without discarding rare records, and a task-value contrast. Whether that combination is sufficiently distinct from established protocols remains unresolved. The literature search was targeted, not an exhaustive priority assessment.

## 3. Exact input and resource contract

At a specified cut, one replica has classical-quantum state

\[
 \rho_{CRSE}=\sum_c p_c |c\rangle\langle c|\otimes\rho^c_{RSE}.
\]

Required resources:

- N independent preparations from this same joint ensemble, not merely identical reduced states. These are preparations, not clones of one unknown input.
- The classical records C are available before routing. No new measurement of S, R or E is needed for the selection rule. A noisy record is allowed: the target is conditional on the actually recorded value, not an imaginary error-free label.
- Calibrated interchangeable sites and continuation dynamics. Site heterogeneity must be included explicitly or bounded; calling modules replicas does not establish this.
- A physical permutation of the S registers whose net joint action, relative to a matched-duration reference evolution, is close enough to the intended permutation and leaves the relevant environment dynamics unchanged. Reduced-system gate fidelity is insufficient; see Section 9.
- Independent batches, or an independently justified alternative concentration argument, for the stated sampling bounds.
- A fixed, bounded scored continuation. Corrected detector estimates with a wider range require the corresponding wider-range concentration bound.

Reference R may be an idle register entangled with S. It need not move. Its identity must follow the quantum state that originated with it. An arbitrary entangled collection of different jobs is not a supply of independent replicas.

## 4. Physical construction

For each batch, group replica indices by the observed value c. If a group has at least two members, cyclically permute their S registers so that no register stays at its original site. Leave singleton groups untouched. Record the source-to-destination map.

If site i receives S from source j, continue the experiment at site i with its resident environment E_i, but score the resulting data register against reference R_j. Match C_i=C_j. All systems are retained; there is no selection on success or on convenient labels.

A k-member cyclic permutation can be compiled using k-1 block swaps. Gate count, routing topology, idle time, controller latency and reference storage are resources, not free primitives. For an m-qubit data block the operation must exchange the entire relevant block.

## 5. Acquisition identity and proof

For independent replicas i and j with the same observed c, their joint conditioned state is

\[
 \rho^c_{R_iS_iE_i}\otimes\rho^c_{R_jS_jE_j}.
\]

After exchanging S_i and S_j, tracing all unused systems and retaining the recipient data S_i together with donor reference R_j gives

\[
 \rho_{R_jS_iE_i}'=\rho^c_{RS}\otimes\rho^c_E.
\]

The reason is exact: R_j and the state delivered into S_i originate in copy j, while E_i originates in an independent copy i. The partial traces factor. No microscopic state label, trajectory, eigenbasis measurement or tomography enters the proof.

Following the recipient's old reference R_i instead would generally destroy the intended data-reference marginal. Reference tracking is therefore part of the operation, not an optional bookkeeping improvement.

With indefinitely available matching partners, the tagged output state is

\[
 \mathcal G_C(\rho)=\sum_c p_c |c\rangle\langle c|
       \otimes\rho^c_{RS}\otimes\rho^c_E.
\]

This preserves the CR S and CE marginals and the frequency of each observed condition. It removes associations between RS and E conditional on that observed condition. It does not erase global correlations among all output replicas: they can be relocated across sites.

The expression is nonlinear as a function of one unknown input density matrix. Its implementation consumes multiple independent preparations; no universal nonlinear single-copy quantum channel is being postulated.

### Finite batch, including rare conditions

A tagged replica with condition c has no partner with probability

\[
 a_c(N)=(1-p_c)^{N-1}.
\]

Therefore the average tagged output is exactly

\[
 \rho_N=\sum_c p_c|c\rangle\langle c|\otimes
 \left[a_c(N)\rho^c_{RSE}+
 (1-a_c(N))\rho^c_{RS}\otimes\rho^c_E\right].
\]

The probability weight still unexchanged is

\[
 s_N=\sum_c p_c(1-p_c)^{N-1}.
\]

With trace distance D(x,y)=||x-y||_1/2, block orthogonality and D<=1 imply

\[
 D(\rho_N,\mathcal G_C(\rho))\le s_N.
\]

For any continuation channel and effect 0<=M<=I,

\[
 |F_a(\rho_N)-F_a(\mathcal G_C(\rho))|\le s_N.
\]

Consequently a two-policy contrast changes by at most 2s_N. These are support-independent bounds, but do not say that s_N is small: if conditions have very high diversity, practically every replica can be a singleton.

The fraction of replicas in singleton classes in each real batch is an unbiased estimate of s_N. Its uncertainty must also be accounted for. For independent batches it is a bounded [0,1] variable. There is no need to estimate every p_c. This prevents silent p_c-squared weighting from keeping only matched pairs.

For a decision about the actual finite-batch routing policy, s_N is not an error: finite-batch routing is itself the tested intervention. The s_N bound is needed only when inferring the ideal fully conditionally decorrelated comparison.

## 6. What is measured

For a continuation a and an actual bounded success observable, let F_a(rho) denote its mean score. The directly acquired contrast is

\[
 K_a=F_a(\rho)-F_a(\rho_N).
\]

It is a performance consequence of a specified routing intervention, not an entropy, a reconstruction of a bath state, or a proof of uniquely quantum memory. Classical hidden correlations can generate it.

For two actual continuations a and b, measure four arms:

\[
 \Delta_0=F_a(\rho)-F_b(\rho),\qquad
 \Delta_N=F_a(\rho_N)-F_b(\rho_N).
\]

Opposite signs with adequate uncertainty margins show that the routing intervention changes the controller ranking. Attributing this specifically to conditional correlations requires the full acquisition contract, especially the environmental action and replica assumptions. A null result does not prove Markovianity or sufficiency of C for untested histories, observables, or policies.

## 7. Exactly solvable decision-reversal witness

This is an engineered mathematical model, not measured hardware and not a model fitted to any cited experiment.

Let E be a hidden classical phase bit, represented as a qubit. Let |Phi+> and |Phi-> denote Bell states of RS. Within condition c,

\[
 \rho^c_{RSE}=(1-u_c)|\Phi^+\rangle\langle\Phi^+|\otimes|0\rangle\langle0|
 +u_c|\Phi^-\rangle\langle\Phi^-|\otimes|1\rangle\langle1|.
\]

The past interaction has recorded the same phase bit in the data-reference phase and the environment. Two continuation policies are:

- Echo: allow a controlled-Z from E onto S, which restores the original Bell state when the original association remains.
- Isolate: suppress that later interaction, leaving the current RS marginal alone.

The score is the probability of passing a |Phi+> test. Before exchange,

\[
 F_{echo}=1,\qquad F_{isolate}=1-u_c.
\]

After ideal conditional exchange, the phase bit carried by RS and the recipient environment bit are independent given c:

\[
 F_{echo}^{graft}=(1-u_c)^2+u_c^2,\qquad
 F_{isolate}^{graft}=1-u_c.
\]

Thus for 0<u_c<1/2 the ranking reverses. The data-reference and environment marginals have not changed. With p=(0.9,0.1), u=(0.2,0.4), the aggregate scores are:

| State preparation | Echo | Isolate |
|---|---:|---:|
| Original associations | 1.000000 | 0.780000 |
| Ideal condition-matched exchange | 0.664000 | 0.780000 |
| Batch size 2 | 0.736000 | 0.780000 |
| Batch size 4 | 0.699280 | 0.780000 |
| Batch size 32 | 0.665831298 | 0.780000 |

At N=32, s_N=0.003815204244769458.

**Interpretation limit:** This example does not demonstrate improved performance: the best original policy already scores 1. It shows only that the intended causal contrast can change a decision. It is analytically solvable and ordinary calibrated controls can reproduce its predictions; it supplies no experimental or computational advantage claim.

## 8. Why conditioning, independence and reference tracking matter

### A false conditional-causality claim from ordinary exchange

Let C be a fair bit, and given C=c let S=c and E=c deterministically. There is no S-E correlation left after conditioning on C. A future parity check scores 1 naturally and 1 after condition-matched exchange. Unconditional cross-copy exchange scores 1/2. Its signal arises from breaking the association with the known condition, not from hidden dependence beyond it.

### Equal marginals do not establish independent replicas

In the Bell-phase example with u=0.2, prepare two replicas using the same unrecorded bit e rather than independent bits. Each individual replica has exactly the promised one-replica density matrix. Nevertheless exchanging their S registers leaves the future echo score at 1; assuming independence predicts 0.68. The discrepancy is 0.32.

A stream of repeated runs that shares an unreset environment is not automatically an independent copy source. Shared drive noise, reservoirs and cross-site couplings require explicit treatment. Adding measured common-mode information to C can repair some classical dependence; it cannot certify removal of arbitrary unobserved common variables or entanglement.

## 9. Decisive hardware counterexample: reduced gate certification is insufficient

Consider the implemented operation

\[
 \widetilde U=SWAP_{S_1,S_2}\otimes X_{E_1}\otimes X_{E_2}.
\]

For every input, its reduced action on all accessible R and S registers is the same as the ideal SWAP: a unitary on traced-out environments cannot change an immediately measured reduced state. Moreover, \widetilde U^2=I. Thus perfect accessible-register gate tomography and a perfect double-swap echo are compatible with a large unwanted environmental action.

Start each copy in |Phi+>_RS tensor |0>_E, with no initial RS-E correlation. Under a subsequent controlled-Z from E onto S, the ideal exchange gives Bell success 1; the implemented operation above gives success 0. The entire apparent causal signal is a change to the hidden environment.

**Consequence:** Neither qubit-only gate fidelity nor a round-trip sham certifies the intervention as changing only associations. A useful implementation needs either a justified joint dynamics bound, a sufficient independently accessible environmental audit, or a task-specific bound on the unwanted environmental effect. For the last option the audit must not circularly assume that the observed contrast comes only from correlations.

For example, on a justified bounded-energy sector a calibrated residual Hamiltonian bound can control the finite-duration gate defect through an integrated norm estimate. The cutoff tail, couplings, switching process and norm bound must be acquired; they are not supplied by the algebra. A black-box environment with no such control remains an open acquisition gate.

## 10. Uncertainty and total costs

Treat each independent batch, not each within-batch endpoint, as an independent observation. Cross-copy exchange creates correlations between endpoints. Let the batch mean score lie in [0,1], and let B batches be acquired independently for each of four predeclared arms. A union-bound Hoeffding radius for each mean is

\[
 r=\sqrt{\log(8/\delta)/(2B)}.
\]

Each two-arm contrast has statistical radius 2r. Add bounded systematic biases for each arm. Inferring a fully decorrelated contrast also requires 2s_N, using an upper confidence bound on s_N rather than an unqualified plug-in estimate.

Illustration only: B=4000, N=32, delta=0.05 gives r=0.0251872, two-arm radius 0.0503745, and 4BN=512000 prepared replicas. This is a conservative sufficient accounting example with independent batches, not a measured sample requirement or an estimate of laboratory wall time. It excludes gate, detector, batch-independence, module-mismatch and environmental-control systematic errors.

A bounded joint preparation discrepancy epsilon_p, joint implementation discrepancy epsilon_g, matched-continuation discrepancy epsilon_f and readout bias epsilon_m yield a task score bias at most their sum, using trace-distance/diamond-distance normalization appropriate to [0,1] effects. Such bounds must be justified on the relevant joint states, not inferred from reduced gate benchmarking.

Costs include duplicated or buffered modules, initial preparation, reference storage, measured condition acquisition, classical matching, real register exchanges, idle dephasing, detector calibration, reset/cooling and repetition of complete histories. Finite-batch sparsity and rare conditions may defeat the scheme. There is no established dimension-independent total-cost advantage.

Preserved local marginals do not imply preserved interaction energy. For a system-bath coupling H_SE, the intended change can include

\[
 \Delta E_{int}=\sum_c p_c Tr[H_{SE}(\rho_S^c\otimes\rho_E^c-\rho_{SE}^c)].
\]

Switching work and altered couplings must be included. Nothing here implies free decorrelation, heat extraction or a thermodynamic advantage.

## 11. Comparison that must be passed

The evaluation must include direct randomized testing of actual continuation policies; state-matched causal breaks where affordable; targeted non-Markovian response matrices; unconditioned multi-copy decorrelation; standard dynamical decoupling and motional/routing controls; and applicable calibration-free non-Markovian noise-suppression protocols.

A conventional reset of S can destroy entanglement with its reference. The proposed bookkeeping preserves the donor RS marginal instead. This identifies a potentially different experimental access contract, not a universal separation from every existing protocol. When conditional states are simple or known, a conventional state-matched preparation may be cheaper. When quantum correlations are inaccessible experimentally, a simulation assuming them does not supply the missing access.

For a small controlled bath, first hide its parameters from the diagnostic procedure but permit independent validation on separate runs. Demonstrate the acquisition identity, the independent-source condition, reference pairing and a bound on gate-induced environmental changes. Then remove the privileged environmental audit only when a transferable bound is justified. Passing the small controlled test would establish an implementation, not a useful scalable technology.

A consequential validation must show that information from the assay leads to a preregistered improvement in a held-out controller or workload compared with a cost-matched baseline. If direct policy trials or existing response measurements achieve the same decision at lower total cost, terminate the advantage claim even if the mathematical identity remains correct.

## 12. Negative research capital from the screen

The preceding solar-cell route considered a common selector followed by two calibrated reference outcomes. Under an exact common-selection and no-collateral-effect contract, D_j=M(r_j-q) gives M=(D_1-D_0)/(r_1-r_0) and q=(r_0D_1-r_1D_0)/(D_1-D_0). This algebra alone does not acquire M or prove a valid selector. With interactions, the inferred q is a net causal value rather than necessarily a carrier probability. Most importantly, an occupied carrier's rescue value does not identify the value of structurally passivating its trap: the latter changes capture, electrostatics and available pathways.

Strong photovoltaic comparators include Pan et al., *Operando dynamics of trapped carriers in perovskite solar cells observed via infrared optical activation spectroscopy*, Nature Communications 14, 8000 (2023), DOI 10.1038/s41467-023-43852-5, and Zhang et al., *Overcoming the fill-factor limit of organic solar cells*, Nature Photonics (2026), DOI 10.1038/s41566-026-01946-8. The latter combines several experimental methods rather than using an intentionally weak single-measurement baseline. No distinct, acquired, decision-changing advantage for the proposed dual-reference trap assay was established; that route was not promoted.

Astra's temporal isotope programme supplies the related observation-map warning, not a theorem about the new system. Its N813 dossier retains real whole-parent acquisition and cost-matched decision gates. Neutral entry-history labels should not be treated as labels of internal causal importance.

## 13. Verification and continuation obligations

`verify.py` uses NumPy and the standard library. It checks the exact two-copy identity for 32 random mixed RSE states with dimensions (2,2,3), reference preservation, rational finite-batch formulas, exhaustive small-batch label enumeration, the Bell-phase decision witness, the shared-hidden-bit failure and the invisible-bath-gate failure. The saved output is `verification_results.json`.

These checks verify finite instances and implementation consistency. The factorization and finite-batch proofs above establish the stated identities mathematically; external proof review remains absent. None of the checks verifies priority, experimental feasibility, a real material mechanism, or advantage over existing methods.

The next necessary evidence is not a larger ideal simulation. It is a same-platform environmental-action certificate and a specified held-out decision comparator. Until those are acquired, retain this as a conditional candidate, not as a breakthrough, validated technology or completed mission.
