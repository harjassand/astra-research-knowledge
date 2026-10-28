# Independent quantum-process audit: finite mixed TEST/USE service

28 October 2026. Reviewer: separate CP-predictive/quantum-process worker. **SCOPED PASS for the temporal quantum-channel transfer and optional complete-channel Pauli twirl.** This is conditional on the separately reviewed bandit, prox, sampling/control and implementation statements; no statistical rate or numerical bandit constant is accepted by this audit alone.

Reviewed formal source: `ordinary_prequential_mixed_payload_memory_service_20261028.md`, SHA256 `ca691d92eb120edaf9ffbe1937db4a445e6b3cc902815a2a933beaba126a1133`. The immutable scratch was reviewed first as history; this receipt binds the corrected formal theorem. Earlier received files are unchanged. All checks below use zero source samples.

## 1. A single global channel is the correct object

The joint q-input/reference state must initially be product with source memory and independent initial protocol randomness. Future input slots are held without interaction until their selected USE; every recovered output is isolated from all subsequent source and control operations. Isolation means no later operations, **not** absence of entanglement with memory. Role coins and all private framing keys are fresh and independent; current decoder/exploration is independent of the current role and frozen before the source call (equivalently presampled before the role), with a role-independent call schedule. TEST and USE must use the same complete source port at the actual history, with no additional current-role side channel.

Under these conditions, the adaptive finite service—including measurements, stopping, discarded unused inputs and physical missing-slot replacements—is a CPTP map Lambda from all q input slots to all q output slots. It is not assumed to factor across time. The source may retain arbitrary quantum memory, become entangled with delivered references and outputs, and react to actual past exposed controls.

Use the single GLOBAL Choi input `Phi_2^(tensor q)`, equivalently the maximally entangled state of dimension `2^q`. At the jth USE, the next untouched input/reference Bell pair is independent of the entire prior process, even conditional on actual earlier classical records. Therefore its reduced conditional source channel E_(t,h) and the conditional six-state/Bell calibration identity are legitimate. This independence is used only in the Choi calculation; it is not claimed for arbitrary actual inputs entangled across slots. The complete-channel statement obtained below then applies to arbitrary joint inputs/reference by channel theory.

## 2. Mixed occupation and the delivered-marginal identity

Let A_t indicate an active round and let current decoder randomness be included in the predictable conditioning before drawing the role coin. Conditional on that information, USE has probability r and its current marginal Bell loss is the same conditional-channel loss that the TEST calibration measures, after averaging its independent decoder exploration if applicable.

Consequently the sum of Bell failures **at the time of delivery**, averaged over the ACTUAL mixed process, is

    C_delivered = r sum_t E[A_t ell_t(C_t)]
                = (3/2) r sum_t E[A_t q_t(C_t)].       (Q1)

The second equality needs the source's stated six-state decoder-return identity, not any all-probe substitution. Earlier USE rounds alter memory/record occupation; they cannot be replaced by TEST rounds in this expectation. This audit does not rederive the importance-weighted bandit inequality.

For each delivered slot j, condition first on the history through its delivery. All subsequent operations act on its complement, with a complete trace-preserving instrument after summing later records. They therefore leave the already delivered `(R_j,O_j)` reduced state unchanged. The later source may remain correlated with that pair; no-signaling does not require a product state. Hence (Q1) equals the expected sum of **final** Bell failures of the slots that were actually delivered.

Conditioning on an individual future record could steer an earlier marginal. The proof does not do that: it sums the complete future instrument for each delivery history. This distinction is load-bearing.

## 3. Shortfall is charged once

Let beta be the probability fewer than q USEs occur before the cap. Decompose the final global Choi state into subnormalized success and shortfall parts. With `F_j=I-Phi_(R_j O_j)` and `F_global=I-product_j Phi_(R_j O_j)`, commuting projectors give

    Tr(F_global rho_final)
      <= beta + sum_j Tr(F_j rho_success)
      <= beta + sum_j Tr(F_j rho_delivered_j)
       = beta + C_delivered.                          (Q2)

The second inequality uses positivity: the branches where slot j was delivered include every complete-success branch. It does not charge the individual failures of all missing slots. Thus no q*beta factor is needed. Missing slots still require actual CPTP replacement and discard of held inputs; (Q2) does not implement a free bypass.

Pre-sampling N independent role coins makes shortfall exactly the event `Binomial(N,r)<q`; stopping after the qth USE does not alter this event. The asserted tail bound for mean mu>=2q follows from the ordinary lower-tail Chernoff bound `exp(-mu/8)`. Its source accounting and finite random-bit sampling remain matters for the separate control review.

## 4. Global twirling, including missing slots

Fix a vector of q private Pauli keys P. Because each future input slot is untouched before its USE, its input frame commutes through every previous operation, even for entangled inputs. Because delivered outputs are isolated, their inverse output frames commute to the end. Keys are not supplied to the learning rule or public controls.

For a missing slot, the actual protocol may never apply its input frame. This is still equivalent to applying it at the beginning: a local unitary disappears under the later discard of that unused input, including when it was entangled with other slots. The physical replacement output **must receive the matching inverse frame**, as the source states.

It follows for every fixed key vector—not just at the Choi state—that the framed service is

    Lambda_P = Ad_(P^dagger)_out composed with Lambda
                                      composed with Ad_P_in.    (Q3)

Averaging fresh independent keys yields the ordinary global q-qubit Pauli twirl of the complete adaptive service. One must not substitute a product of separately twirled per-round channels; there need not be such independent channels.

At the global Choi input, each input Pauli can instead be moved to its untouched reference, while inverse output Paulis cannot affect later record probabilities. Thus the actual probe/role record law at this analysis input is unchanged by the keys. This supports using the same mixed-occupation calibration analysis for the twirled service. It is not a role-sealing theorem or a claim that the source cannot discriminate quantum inputs.

The averaged q-output channel is Pauli: `Lambda_twirl=sum_P p_P Ad_P`, with global Bell fidelity `p_I`, unchanged by twirling. The triangle inequality gives half-diamond error at most `1-p_I`; the global Bell input attains this because Pauli error states are orthogonal. Therefore

    (1/2)||Lambda_twirl-id||_diamond =1-F_e(Lambda)
                                     <= C_delivered+beta.       (Q4)

This is an averaged-key, averaged-record q-output channel guarantee, not a guarantee conditional on a retained key. Any stronger record-boundary claim would need its own statement. Trusted framing controls and 2q private key bits are real resources.

## 5. Comparator and implementation boundaries

The formal source correctly compares against a fixed decoder's cumulative marginal cost on the ACTUALLY visited mixed occupation. It is neither relative error against an oracle's global channel nor the occupation law induced by deploying that decoder on previous rounds. Perfectly correlated logical errors can make a sum of marginal losses q times their global union loss; the proposed general comparator cannot silently be tightened.

If the supplied complete CP-dominant common-algebra contract makes one fixed D_* optimal at every mixed history, it can identify that cumulative comparator. In its genuinely logical-noiseless subfamily, zero cumulative oracle loss permits a reliable joint service by (Q2)-(Q4). The contract must hold for the actual retained-memory source, not merely iid or reset calibration channels.

A separately proved **whole-q-input half-diamond discrepancy**, uniform over arbitrary joint payload/reference, is charged once after the transfer. The actual imperfect framed channel need not be Pauli: use the ideal Pauli equality and the diamond triangle inequality. Per-call compiler errors, all stored inputs/isolated outputs, waiting time, physical replacements, key handling and framing must already be included in this complete-process bill. Bell fidelity or calibration-trajectory agreement alone is insufficient. No repeated per-payload use of a one-terminal error guarantee is valid.

The comparator remains on the genuinely mixed occupation of the declared IDEAL TRUSTED-INTERFACE controller with the actual unknown source. A single whole-channel discrepancy does not freely move this cumulative comparator to the imperfect implementation’s changed histories. For example, a rare common Pauli fault can change global loss by nu while changing a sum of q marginal costs by q*nu. Both the complete-norm and comparator-convention qualifications were raised during this quantum review and incorporated before this receipt.

## 6. Distinct deterministic check

`prequential_mixed_service_quantum_independent_check_20261028.py/.json` imports no author fixture. It uses q=2, cap N=3, r=1/2, a coherent qubit memory, partial-SWAP source `(15I+8i SWAP)/17`, and an adaptive decoder selected by previous TEST parity. TEST deliberately uses a fixed |+> probe with Z readout, **not a 2-design**: this isolates the temporal-channel proof and does not test the calibration estimator or bandit guarantee.

It enumerates every actual branch without RNG, keeps both Bell references, performs physical shortfall replacement, and explicitly compares all 16 on-demand framing schedules with an algebraic global twirl. Results:

- Global Bell loss `0.6235656948637931`.
- Accumulated delivered marginal loss `0.331886848644226` equals its final isolated-marginal value within `1e-12`.
- Shortfall `0.5`, giving the nonvacuous bound `0.8318868486442258` when charged once.
- Actual framing/global-twirl maximum matrix discrepancy `0` in this fixture; record/key probability discrepancy below `1.4e-17`.
- Twirled Bell-Pauli basis off-diagonal magnitude below `3.5e-17`; global Bell fidelity is unchanged.

These finite diagnostics guard tensor ordering and stopping/framing conventions; the general argument is (Q1)-(Q4). They claim no learning performance, common-algebra advantage, acquisition budget or hardware execution. No decisive quantum-process flaw was found at the stated scope.
