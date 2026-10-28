# Generic relative learning by a seed-or-relative-slack dichotomy

28 October 2026. New composition candidate; independent receiving is pending. It removes the USEFUL-SEED PROMISE from a received protected-reference bootstrap, not the paid protected-reference transport or calibrated coherent-input controls. Warm acquisition is ordinary; a low-loss branch subsequently uses actual source-generated coded reference transport and the separately supplied coherent Gamma preparation. This is NOT a generic strict-ordinary k² theorem. No new two-way purification, pre-shared entanglement or protected bypass is used.

## 1. Contract and conclusion

Use the stationary independently reset source, calibrated quaternion encoder family with implementable known relative controlled-anchor phases, valid uniform encoded Choi-rank bound R, and common effective output dimension k<=min(s,8R). Full CPTP decoders are allowed. Use the received efficient causal common-frame compiler for a public finite horizon and retain its quantum memory throughout. Known encoder controls, local memories, finite code gates and necessary classical policy/key communication are supplied and charged; the source is never inverted or coherently controlled.

The ordinary encoder controls and the COHERENT Gamma preparation are distinct assumptions. The latter is exactly the received controlled-anchor/Bell/control preparation, not inferred from access only to the real-x ordinary channels. It sends one physical data register through the source and leaves three reference qubits at the sender; those references must be actually transported by the protocol below. Any alternative contraction/filter realization retains its actual preparation/heralding/failure costs and is not covered by silently replacing W=[V_i] with an isometry.

For every source satisfying these interface/rank/reset assumptions, every 0<gamma,epsilon<=1 and prescribed M>=1, there is a total finite protocol with worst-case raw-call cap

    N_raw=O_tilde(k² M/(gamma epsilon))+M,              (1)

and polynomial theoretical known controls/classical processing in the charged horizon/dimensions/precision, whose actual private-framed output channel obeys

    ||Lambda_actual,M-id||_diamond
       <=min{2,(1+gamma)Delta_star_(family,frame,M)+epsilon}. (2)

There is NO promise that a seed exists, no entropy/NPT/spectral gap promise, and no conditional-success normalization. The original comparator permits predetermined per-use encoder lists and arbitrary collective full-CPTP recovery, but only one source use per payload and no joint encoder/rate change, extra payload-dependent calls, or bypass. Its received value is

    a_star=1-ell_star,
    ell_star=min_(x,D CPTP)[1-F_e(D E_x)],
    Delta_star_(family,frame,M)=2(1-a_star^M).            (3)

The finite-M guarantee tests logical outputs with calibration records, private Pauli keys and frame memory discarded. No public-record guarantee or indefinite learned-program reuse follows. The equally informed conventional learner can use the identical protocol.

## 2. Public thresholds, confidence and ordinary pilot

Fix the constants and parameters

    tau=1/80, p0=2tau=1/40,
    alpha=gamma/2, e=epsilon/(8M),
    a=tau(gamma+e)/64,
    beta_t=beta_v=epsilon/64,
    delta_ref=epsilon/4, nu<=epsilon/4.                 (4)

Here a is a PILOT tolerance, not Bell fidelity or filter acceptance. Since e<=1/8, one has a<=9tau/512<tau/4.

Run the received ten-anchor inverse-square ordinary learner with its accuracy parameter epsilon_0=4a and joint density-bank confidence beta_t, retaining its finite feasible PSD model fit, full-CPTP decoder SDPs and encoder-grid tolerances. Explicitly,

    delta_a=a/256, m_a=delta_a²/8,
    d=2k, r=min(d,3R), D_a=nextpow2(d r),
    n_a=ceil[(80 D_a/m_a) log(120 D_a/beta_t)].

The ten actual homogeneous ordinary loss-state banks use10n_a raw calls and one continuing frame. The accepted good-event inequality gives a physical pilot (x0,D0) with actual Bell loss p satisfying

    p<=ell_star+a.                                    (5)

It is this high-confidence event, not merely the predecessor's averaged headline, that is imported. The candidate positive completion remains only a physical prediction fit; no Choi-state oracle is prepared in the pilot.

Freeze the pilot. Acquire

    n_v=ceil[(2/a²) log(2/beta_v)]

FRESH uniform six-state return tests using that same encoder, decoder and frame. The mismatch probability is q=2p/3; put phat=(3/2)qhat. Hoeffding gives

    Pr(|phat-p|>a | U,training)<=beta_v,

because n_v exceeds9 log(2/beta_v)/(8a²). U denotes the single mathematical common frame, not a physical coordinate available to the learner. Let G be the intersection of the ten-bank good event and this holdout event. It is entirely pre-payload, includes no future coherent-learner observations, and has

    Pr(G^c)<=beta_t+beta_v=epsilon/32.                  (6)

No seed promise was used to get this event. On a failed fit/solver history the actual algorithm returns a physical replacement policy and follows the same finite cap; such histories are included in G^c.

## 3. The actual branch rule and its two good-history guarantees

Use the simple public rule:

* **LOW branch:** if phat<=tau, retain the pilot as a seed and run Sections4–5.
* **HIGH branch:** otherwise, skip coherent acquisition and retain the pilot for all M subsequent one-use payloads.

On G, LOW implies

    p<=tau+a<2tau=p0<1/20.                             (7)

Thus a genuinely useful low-error seed has been acquired with a fixed coding margin whenever that branch is taken. No assertion that LOW must occur for every source is needed.

On G, HIGH implies p>tau-a. Combining with(5),

    ell_star>tau-2a>=tau/2,
    p-ell_star<=a
       <=gamma ell_star/32+e/64
       <=alpha ell_star+e.                            (8)

The first bound is the key: if a small-loss seed was not selected, a near-optimal pilot already certifies enough NONZERO comparator risk that relative slack pays its additive error. It is not a capacity certificate or a conclusion that no good communication code exists. Near the threshold either branch is acceptable, so no exact classification of an unknown optimum is required.

## 4. LOW branch: the already received physical reference transport

On G in LOW, privately Pauli-frame every subsequent seed use before x0 and undo the key after D0 in the SAME continuing frame. Conditional on U and the full frozen warm record, the exact reset/common-frame law gives iid Pauli channels with nonidentity probability p<=p0. This statement is a complete channel identity on arbitrary reference-correlated inputs, not a conclusion drawn from holdout marginals alone. Arbitrary local faults are not inserted into this probability and squared.

Use the received coherent learner at parameters alpha,e. For explicit conservative choices put

    d_G=8k, r_G=min(4R,d_G), D_G=nextpow2(d_G r_G),
    L_G=2+ceil(log_2(2D_G)),
    n_G=ceil[20480 D_G L_G/(alpha e)],
    a_eig²<=alpha e/4096, eta_opt<=alpha e/8.             (9)

The accepted Bures/positive-loss argument gives, with PERFECT returned reference wires,

    E_future ell_fine<=(1+alpha)ell_star+e,              (10)

uniformly in U and every frozen warm record. The larger base-two L_G is a conservative replacement for the source's natural-log factor. The finite global encoder net and full-CPTP decoder SDPs cost classical work, not extra source banks. In the received causal-frame extension the chosen decoder is retained for deployment in this SAME frame; no independently realigned decoder is reused.

There are Q=3n_G actual sender reference qubits. For each, use the received level-L concatenated five-qubit transmission encoder and deterministic syndrome decoder. Its conditional independent-Pauli error bound is

    p_L<=4^(-2^L)/10.

Choose the smallest L>=0 such that

    (Q/5)4^(-2^L)<=delta_ref,
    B=Q5^L.                                           (11)

The Q logical reference channels then have unhalved complete discrepancy at most2Qp_L<=delta_ref. Exactly B ordinary seed-carrier source calls are paid; no reference is transported through a supplied link. This is direct source transmission coding, NOT the new two-way recurrence/teleportation factory. No purification success probability or uncounted backward distillation communication is introduced.

Use the received data-first chronology: prepare each actual controlled-anchor Gamma data sample, send its physical data once and enter the next frame step, retain its three references at the sender, encode/transmit/decode those references through the seed calls, and assemble the bank at the receiver. All waits, local codeword/reference memories, source environments and stored data correlations are included by the complete reference-channel comparison. The source and frame are not reset or physically deleted when references are replaced by identities in the ANALYSIS. The actual noisy bank may be full rank and correlated; only its ideal comparison bank is passed to the accepted iid low-rank theorem.

## 5. One deterministic horizon and all-history processing

The public cap is

    N_w=10n_a+n_v,
    H=N_w+n_G+B+M.                                    (12)

Initialize the frame for H before any data. All branches use at most this many calls. HIGH skips the optional acquisition/coding calls; causal-prefix validity suffices, or harmless predatum dummy calls can pad the reserved slots if a fixed schedule is desired. Either convention is fixed publicly and all used controls are paid. Bad records, solver aborts and coding errors never trigger unbounded retries.

Every payload uses the selected encoder/source once, the next continuing frame step, the selected full CPTP decoder and its private independent Pauli unframe. LOW uses the fine policy; HIGH uses the pilot. No final payload code or across-use encoder is introduced. Payloads arrive only after all calibration has ended. The source stationarity/reset and arbitrary-operator frame law are substantive assumptions, including through classical computation and waiting times.

Since 5^L is bounded by a constant times[1+log(Q/delta_ref)]^(log_2 5), the reference bill is Q times a fixed polylogarithm. Also

    D_a=O(k²), D_G=O(k²),
    1/(gamma+e)²<=1/(4gamma e)=2M/(gamma epsilon).

Thus the entire warm cap O_tilde(k²/a²), n_G and B fit(1); the fixed tau contributes only an explicit, large constant. The claimed fast accuracy is not obtained by hiding an inverse-square pilot at a target-independent confidence: the pilot accuracy depends on gamma+e, and the displayed inequality pays it at the same source scale.

Known-control/classical bit complexity is polynomial in the actual deterministic horizon, k, log ambient output dimension,1/gamma,1/epsilon,M and supplied circuit sizes. It includes ten density estimators, finite model-fit/decoder SDPs, the coarse and fine encoder grids, all code gates, private keys/classical messages and the later efficient causal compiler. Frame memory persists for the full history. These theoretical caps are not practical-runtime or hardware claims.

## 6. Global relative comparison, including selected histories

First analyze the exact-reference experiment and condition on G, then average over its allowed warm histories and common U. On HIGH, inequality(8) holds pointwise. On LOW with perfect returned references, inequality(10) holds over FRESH future learning randomness for every such warm history; conditioning on G does not condition those future observations. Consequently the combined ideal selected policy on G obeys

    E[ell_selected | G]<=(1+alpha)ell_star+e.           (13)

Every realized policy is physical, so its fidelity f satisfies0<=f<=a_star. The M independently private-framed payloads have identity Pauli probability E[f^M|G], NOT(E[f|G])^M. The accepted comparator and the elementary power inequalities give

    2[1-E(f^M|G)]
       <=(1+alpha)Delta_star_(family,frame,M)+2M e.      (14)

This is the original global collective-decoder comparator, not the looser2M ell_star surrogate.

On LOW good histories, actual reference transmission changes the ENTIRE subsequent learner/payload process by at most delta_ref; on HIGH it costs zero. No bad-warm probability is absorbed into a marginal p and amplified M times. Instead the pre-payload event G is independent of the unknown payload input, so its complementary channel branch costs at most2Pr(G^c) ONCE in the complete M-output channel. Conditional analysis is only a proof device; the deployed protocol is not postselected or normalized. Finally add a SINGLE whole-interactive implementation discrepancy nu, paying all source controls, frame updates/memory, code gates, finite random sampling, decoder implementations and M payload operations uniformly over every history.

Together,

    ||Lambda_actual,M-id||_diamond
       <=(1+alpha)Delta_star+2M e+delta_ref
                              +2(beta_t+beta_v)+nu
       <=(1+gamma)Delta_star+13epsilon/16,

which proves(2) with slack and the trivial saturation at2. Exposed calibration records, key/environment export or an unknown local-fault model require a different statement and are not inferred.

## 7. Governing imports, comparator and scientific scope

The ordinary high-confidence pilot is the received ten-anchor derivation in `../ordinary_generic_inverse_square_polynomial_baseline_20261028.md`, with the exact density-query cap from `../ordinary_bures_matrix_query_confidence_20261027.md`. The source-generated concatenated reference code and actual chronology are received in `../bootstrap_protected_calibration_20261027/BOOTSTRAPPED_PROTECTED_COHERENT_CALIBRATION.md` and its five-qubit/composition receipts. The expected coherent full-policy inequality, retained-frame extension and complete reference-bank argument are also explicitly assembled in `../block_reference_entropy_bootstrap_20261027/BLOCK_REFERENCE_ENTROPY_BOOTSTRAP.md`. The original global comparator is `../direct_cptp_bures_bridge_20261027/PRIVATE_FRAMED_COMPLETE_OPTIMALITY.md`. The later efficient online causal compiler, not the older dense existence proof, supplies the paid frame.

The new step is the good-history LOW/HIGH dichotomy and its source/accounting composition. Existing coded references, coherent positive-loss tomography and conventional concatenated coding are not claimed as inventions. The previously stated seed promise is no longer a theorem assumption here because sources on the HIGH branch are already handled to the RELATIVE target by an acquired coarse policy.

This does not decide quantum capacity or assert that every source can transport protected qubits. HIGH may include sources with no useful quantum communication capability at all. It does not solve generic strict-ordinary rank-squared acquisition, because LOW genuinely creates and transports coherent references. If communication alone is the objective, directly coding payloads through a useful seed is a simpler stronger conventional baseline than learning a one-use near-optimal policy; the latter has its own fixed-rate comparator. The two-way NPT factory remains independently useful for source-generated reference entanglement beyond unassisted coding seeds, but it is not needed for this generic relative-regret dichotomy.
