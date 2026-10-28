# Independent receiving: approximate on-site full-reference future-memory recovery

2026-10-28 17:49 UTC. **PASS at the stated mathematical and physical-interface scope** for `ordinary_approximate_onsite_frozen_memory_recovery_20261028.md`, SHA256 `8ed5031f786c6eac4a3a5c10e02d2cb149f70343bc1a519ee1ce8a4d3eea54d5`.

This review independently receives the full-reference extraction, actual-future-memory comparator transfer, arbitrary-receiver lower bounds, time-dependent local-crosstalk interface and bounded-drift corollary. It also checked the normalized-fit geometric composition into those claims. The actual ordinary-record acquisition/concentration and finite quaternion implementation retain their separate acquisition/finite-control review; this receipt does not claim to have run a production learner or a gate compiler. None of the main source, exact source or existing received artifacts was edited by this reviewer.

## Correction required and resolved before binding

The initial candidate used the same symbol for incoming source memory and an emitted gauge state in its virtual-loss comparison. That was dimensionally ambiguous. The final source now defines `G_(alpha,omega)=Tr_(M') G_alpha(omega)` and `g_omega=sum_alpha G_(alpha,omega)`, and writes the complete positive-operator chain

    excess <= Tr[(I-T_I)G_(I,omega)]
           <= Tr[(I-T_I)g_omega] = ell0(g_omega).

This resolves the issue without changing the bound. The earlier bytes are preserved separately. The author also added the stronger source-specific-midpoint lower construction, checked below. There are no unresolved mathematical issues within this receipt's scope.

## Main claims independently checked

1. **No approximate tensor factorization is assumed.** For every purified gauge/memory state the exact logical X/Z Bell stabilizers fix the full encoded Bell state. The candidate physical X/Z stabilizers commute on all q reference/output pairs. Individual failure is exactly one quarter of a squared vector difference. Their commuting-projector union bound proves `ell0<=sum ||Ahat_ij-B_ij||op²/4`, retaining the entire q-input reference and arbitrary gauge purifier. This is uniform in the gauge state and does not introduce a q² penalty.

2. **The geometric floor is genuinely independent of kappa.** Positivity of each signed gauge block gives `|m|<=lambda` and `r.m>=lambda(1-tau²/2)`. A normalized column remains within tau of its hidden axis even when lambda is very small. Same-lambda wrong-site leakage is bounded by tau lambda. The proper two-column least-squares objective controls exactly the two generator errors needed by the Bell bound; no Y margin, improper polar branch, source inverse or hidden source eigengap is used. Stacking yields the source's root bound `3 sqrt(q/2) tau + sqrt(epsilon)/3` and hence `9q tau²+epsilon` after stated probability/control debits.

3. **Strongest same-state oracle is valid.** Every decoder induces a positive Bell-block POVM on gauge space. CP identity dominance makes exact algebra extraction optimal among all CPTP q-output decoders at the same current source memory. The comparison is not against a changed past policy or a decoder following a different occupation law. Positivity bounds the learned excess by the virtual loss at the total emitted gauge state, and the all-gauge inequality then removes that state from the bound.

4. **Actual-memory implementation transfer uses the right special property.** The nominal good event is a record-defined subset yielding fixed recovered sites/controls close to fixed witness axes. Record-TV discrepancy changes its probability once. Every physical record in that subset yields the same deterministic all-gauge bound, even if imperfect training or intervening evolution changes the actual future memory completely. One whole-q-input half-diamond service discrepancy adds `nu_svc`. This is why calibration-record TV suffices here; it is not asserted for a generic occupation-dependent learner. The comparator remains the stated underlying source channel at its actual current state, with the implementation interface and ideal source-informed receiver exactly as declared.

5. **One unknown simultaneous payload, not repeated service.** The full payload/reference is introduced independently of source/acquisition at the chosen service boundary (or conditionally independently given the allowed record). The argument proves a Bell-channel statement for all q inputs jointly. Optional private Pauli frames, paid at the whole-q port, give the declared averaged half-diamond conversion; it is not an untwirled or key-conditioned assertion. No protected payload must exist during calibration, and no indefinite repeated-payload guarantee is inferred.

6. **The lower bound applies to arbitrary frozen full CPTP receivers.** Fresh gauge-0 preparations make the complete training channel identical for all hidden sign completions, even with arbitrary coherent/adaptive probes and retained ancillas. Fresh gauge-1 at the fixed later boundary is the same physical gauge output across signs, so a collective receiver on all logical/gauge outputs is one arbitrary logical CPTP channel with sign-independent ancillas. Sign averaging gives product dephasing. The largest-Pauli-weight Bell-fidelity optimum proves the weaker exact finite-q floor and its saturation. With source-specific midpoint witness axes, the future angle doubles while both gauge branches stay within tau of their allowed fixed witnesses, giving the stronger lower bound

    1-[1-tau²(1-tau²/4)]^q.

The source-informed oracle has zero loss. Thus the floor is an information obstruction, not a restriction to product receivers or ordinary probes. The hidden witness axes are existential, not common supplied data across source completions.

7. **Local Duhamel is valid for time ordering.** Differentiating `W(t,s) A W(s,0)` gives the fixed commutator `[H(s),A]`. Therefore the generator deviation is bounded by the integrated incident coupling sum; bath-only terms can be arbitrarily large without a spurious global Hamiltonian charge. Summing squared per-site deviations gives the stated quadratic local-coupling scale. No inverse crosstalk control is supplied or learned.

8. **Bounded drift is a genuine corollary at its explicit tube promise.** At each time/history a potentially different U_t may obey the same operator-norm tube around ONE fixed unknown on-site frame. The contrast cap and leakage are pointwise and convex under adaptive averaging, the concentration is conditional, and extraction is evaluated at the current U_t. The oracle may consequently vary with time; a common oracle decoder is not asserted. Unrestricted post-training drift and empirical certification of tube membership remain excluded.

## Independent evidence actually executed

All checks are deterministic and source-disabled. They supplement the analytical proofs; floating finite-matrix residuals are not formal interval certificates.

- `approximate_onsite_memory_bound_independent_20261028.py/json`: 27 coupled-unitary fixtures through q=3, arbitrary positive/noncommuting gauge blocks, global Bell gauge-operator bounds, normalized fits, Bell-block POVM/comparator identities, local leakage and crosstalk; 20 controlled-rotation lower fixtures; 32 exact Fraction finite-q lower identities. Largest positive numerical residual below 8e-16.
- `approximate_onsite_midpoint_floor_independent_20261028.py/json`: 40 exact rational SU(2)/generator-difference identities and 28 exact finite-q dephasing-weight fixtures, including q=128. Both branch deviations, midpoint probability, normalization and largest Pauli coefficient are verified without trigonometric rounding.
- `approximate_onsite_drift_receiver_check_20261028.py/json`: 24 time-ordered history fixtures, three noncommuting Hamiltonian segments each, q=1,2 and one/two gauge qubits, large bath-only Hamiltonians, changing U_t inside a fixed on-site tube, full worst-gauge Bell operators and adaptive-average contrast caps. Four exact Fraction record-TV/service-transfer fixtures. No positive inequality residual.

Zero sampled source outcomes, zero RNG draws, no hardware calls, no production optimization or synthesis execution. The main all-memory result is proved analytically, not inferred from these small examples.

## Dependencies and binding discipline

Read the final source and the received exact on-site source plus its root/statistics receipts. Checked the relevant rational Jacobi import. Reverified all 56 direct bindings across the exact on-site root/statistics receipts, general-width local root/statistics receipts and finite-positive-cost-rounding statistics receipt (3+14+7+22+10); repeated paths are counted per receipt, not as distinct scientific files. The companion JSON hashes every direct source/check/note/dependency used here, including this audit. This is scoped independent internal receiving, not external peer review or a priority determination. Conventional normalized Wahba/Procrustes learning remains the strongest equally informed baseline, not a weaker straw comparator.
