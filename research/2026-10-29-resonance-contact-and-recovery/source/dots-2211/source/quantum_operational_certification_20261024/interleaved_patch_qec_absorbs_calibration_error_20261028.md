# Interleaved standard QEC can correct the learned frame's local errors too

28 October 2026. Candidate stronger architecture, separate review pending. Standard coding/interleaving is credited; the new bridge is to an actually acquired local inverse and its resource accounting. This supersedes the need to demand whole-frame error O(p²) ONLY when the stronger disjoint-patch/independence layout below applies. The generic overlapping-mixer bridge remains valid at its original cost.

## 1. Five disjoint physical patches, w interleaved logical codes

There are five KNOWN disjoint patches A_1,...,A_5, each containing w physical carriers. Encode w logical qubits using w independent standard [[5,1,3]] encoders, but route codeword position a of EVERY logical code into patch A_a. Each patch therefore contains exactly one carrier from each code. The payloads may be mutually entangled with an arbitrary external reference.

The source and actual frozen receiver factor ACROSS PATCHES:

    native = tensor_(a=1)^5 [Ad_(V_a) composed N_a],
    receiver = tensor_(a=1)^5 Dhat_a.

Within a patch V_a may be an unknown entangling unitary and N_a a non-Pauli w-qubit CPTP channel. The acquired-algebra/positive-block theorem must actually apply to its reduced calibration contrasts; small noise norm alone does not establish that premise. Product unknown-axis AD within each patch is one supplied physical class. The fixed patch layout, access to all physical inputs/outputs, and actual patch-local receiver implementation are substantive resources. Arbitrary overlapping generators or shared unmodelled cross-patch couplings are not covered.

Once the fixed V_a inverses have been acquired, the FUTURE patch noise need not retain the calibration contrast family or damping axes. Equation(1) below only requires that each actual future block still has the same mixer V_a, the declared across-patch product law, and a weak CPTP residual N_a with its stated p_a bound. The calibration structural promise is needed to learn the frame; standard QEC then handles arbitrary weak non-Pauli patch channels at service. This does not certify those future norm/independence premises from finite training.

For each accepted calibration record assume

    half||N_a-id||diamond <= p_a,
    half||Dhat_a-Ad_(V_a dagger)||diamond <= delta_a.

Then the actual residual patch channel T_a=Dhat_a Ad_(V_a) N_a has q_a=half||T_a-id||diamond<=p_a+delta_a. Patch-local receiver control errors can be included in delta_a if their CPTP implementation genuinely remains patch-local. Encoding, routing, storage and syndrome errors that connect patches are separate complete-system debits unless independently fault-tolerantly constructed.

## 2. Product recovery corrects ANY single-patch channel

Let C_tot be the w product encoders with the stated routing, and R_tot the w known syndrome decoders. Any Pauli supported on ONE patch has at most one nonidentity carrier in each individual code. Thus R_tot corrects every such Pauli. More strongly, different Pauli products in that patch have orthogonal product syndromes: each component code distinguishes I,X,Y,Z on its one specified position. Hence the Knill–Laflamme matrix for the whole patch Pauli basis is the identity. By linearity in Kraus expansions, R_tot exactly corrects EVERY CPTP channel on that patch, including entangling coherent errors between its w carriers:

    R_tot (T_a tensor id_otherpatches) C_tot = id_(2^w).

This is a complete logical identity including reference entanglement. It is not merely separate marginal fidelity of the w logical qubits. It does not assert that the retained environment or syndrome itself has been returned to its original state.

## 3. Calibration errors enter the correctable noise, not a global additive penalty

Write Delta_a=T_a-id. In the product expansion all five first-order terms vanish under the code. Therefore

    half||R_tot (tensor_a T_a) C_tot-id||diamond
      <= min(1, (1/2)[product_a(1+2q_a)-1-2sum_a q_a]).       (1)

For q_a<=q this is at most20q²+40q³+40q⁴+16q⁵, clipped at one. Thus if p_a=O(p) and delta_a=O(p), the whole joint logical channel has O(p²) error. There is NO need to force each acquired patch inverse to O(p²) merely to obtain quadratic code performance.

This distinction changes conservative ordinary calibration accuracy: operator-certified inverse learning with cost proportional to delta_a^-2 now needs O_tilde(p^-2) block samples at fixed width/conditioning, rather than O_tilde(p^-4) for the generic additive whole-frame route. The actual width, positive-block floor, finite optimization, local control, confidence and gap costs remain. A finite cap can abstain; this asymptotic statement is not a feasible laboratory budget.

The bound holds record by record on simultaneous good calibration events, so no final-record retirement is needed for this version. However the ACTUAL conditional service law must factor across patches as stated. A complete joint record/source model does not acquire that factorization merely because one-shot marginals appear independent. Initial bath independence, stationary product block channels, or another explicit process contract is needed. Retaining syndrome/bath for future interactions is outside the logical channel guarantee unless separately controlled.

Confidence failure beta and whole encoder/decoder/nonlocal implementation error nu add once for a shared-abort protocol. To retain O(p²) total performance require beta,nu=O(p²); patch-local errors may instead be absorbed in q_a when their actual structure warrants it. No threshold or fault-tolerant implementation theorem is inferred.

## 4. On-site specialization and a distinct faster retired-record version

For w=1, this is a single standard five-qubit code with five independent on-site mixers. The record-retaining route already needs only delta_i=O(p), not O(p²).

A stronger ONE-SERVICE-CYCLE specialization uses the separately received finite ordinary polar-inverse learner. On each site let the fixed qubit calibration Bloch matrix have positive determinant and minimum singular value a_i>0. In THIS specialization V_i means the canonical proper POLAR rotation of that actual calibration channel, or equivalently the residual calibration contraction after V_i is symmetric positive definite. It is not an arbitrary original hardware V_i hidden behind another unknown noise rotation. Define each future residual N_i and p_i after removing this SAME canonical target; any additional future rotation is part of N_i and its error bill. If the original hardware frame is desired instead, an extra identifiability premise is required. A fresh fixed-horizon final bank of N_i ordinary probes produces a private program whose genuinely record-AVERAGED inverse obeys

    delta_i <= min(1,1620/(a_i³ N_i)),

before its separately charged random-cap/control errors. Use independently acquired final programs ACROSS ALL FIVE SITES, and ensure actual training/service independence. Supplied conditioning bounds or separate accepted pilots are paid; final banks must remain fresh conditional on those pilots. Native service channels and all fit programs must factor across sites conditional on the fixed physical parameters and any explicitly conditioned accepted configuration.

Only if all final programs are inaccessible to the source, service controller and final output may their independent averages factor:

    E_[y1,...,y5] tensor_i [D_(i,yi) Ad_(V_i) N_i]
      = tensor_i [(E_yi D_(i,yi)) Ad_(V_i) N_i].

This identity is valid on an entangled encoded input. Apply (1) to these physical averaged local channels. Choosing N_i=O(a_i^-3/p) makes delta_i=O(p), giving a ONE-CYCLE logical O(p²) bound with O(p^-1) final-fit calls per site at fixed conditioning. The large explicit constant1620, separate pilot, finite randomness, bit precision, source-call and control bills are retained. This is a stronger-access/metric specialization, not an improvement of the record-retaining theorem.

A common fitting program is not a product average. As an exact negative control, let a shared private bad coin of probability h make every local correction apply X, otherwise all apply I. Each averaged local channel is within h of identity, but the joint residual is XXXXX with probability h, a logical X of probability h. Substituting the marginals into (1) would falsely predict O(h²). Independent program acquisition and physical retirement are load-bearing, not optional wording.

The same random programs reused in many cycles with coherent feedback need a separate higher-moment/reuse analysis. One-cycle averaging does not turn them into newly sampled independent errors each cycle. The received phase reuse obstruction explains why naive linear cycle scaling can fail. This source makes no unrestricted repeated-cycle or unknown-continuing-memory fast-rate claim.

## 5. Actual evidence and standard comparator

interleaved_patch_five_qubit_check_20261028.py uses w=2 (ten physical carriers, two logical qubits). It checks all80 single-patch Pauli errors across the five patches and a general entangling two-qubit CPTP Kraus fixture. It then enumerates all1,024 patch patterns at six rational rates for a native XX patch event p combined with a learned-frame YY patch event delta=p. The residual per-patch Pauli error is q=2p-p²; exact JOINT logical half-diamond errors obey the analytic expansion bound and the tighter fixture-specific10q² bound. No dense ten-qubit Monte Carlo or acquired data is claimed.

The complementary learned_five_qubit_nonpauli_bridge_20261028.py executes the actual five-carrier encoder, arbitrary-axis AD, fixed block mixers, bounded-perturbation learned reflection extraction and standard recovery. It is a separate non-Pauli composition test; its synthetic contrast perturbations are not sampled confidence data.

The equally informed conventional architecture is precisely standard QEC/interleaving with the same learned inverse. It has identical performance. The point is that calibration uncertainty can itself lie in the code's correctable locality class, avoiding an unnecessarily stringent global inverse-accuracy requirement. Neither code, interleaving nor cancellation of local errors is claimed as historically new.

Primary standard foundations: Laflamme et al., https://arxiv.org/abs/quant-ph/9602019 ; Knill–Laflamme, https://arxiv.org/abs/quant-ph/9604034 . General correlated-error correction was already studied in Knill–Laflamme–Viola, https://arxiv.org/abs/quant-ph/9908066 ; this source does not claim independence is necessary for every possible QEC result, only that its particular product expansion requires the stated factorization.
