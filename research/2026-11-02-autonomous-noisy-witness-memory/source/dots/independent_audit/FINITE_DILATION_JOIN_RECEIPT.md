# Independent whole-model receipt: finite-rate autonomous dilation

2026-11-01. **Conditional mathematical PASS for the exact finite-ancilla Hamiltonian/reset model and its decoded-memory conclusion.** No new algebraic or composition blocker found. This is an exact finite-rate Lindbladian result, not a microscopic hardware/reservoir certification.

## Bytes and imports received

- `FINITE_DILATION_JOIN_DRAFT.md`: SHA256 1b73fb52b1c4a11b13a052385b37a9fd0e3796e757f4d0960c1263af4f1d3ec9.
- `ANCILLA_CURRENT_HYPOCOERCIVE_LIFT.md`: SHA256 1e7e17b0d4b55649cc2e9b4553b47f02c649eac925f821a4daee3197a198c204; independently proved in my `ANCILLA_LIFT_RECEIPT.md`, SHA256 a6a40b7f4779d6845f0e8aa165b17a6bf6e0e492bd84d69cf767ec94a67a5f14.
- The previously independently received joined Tanner-witness controller/flat-component theorem and its specified-family qualifications.
- `producer-workspace/TANNER_IDEAL_READOUT_ADDENDUM.md`: SHA256 b2ddba696f5f3e7d02488b7ab59c0c35be691d1963664aaabbbb488f39fe73f7. I checked its algebraic consumer transfer; its quoted LZ Theorem 13 decoder radius is an explicitly imported source theorem, not independently reproved here.

## Activity, system size, and direct generator

The upper activity bound <=4W is global by the defect count, while the lower W/K bound remains basin-restricted. This distinction is sufficient and important: global upper activity proves global V/Q comparability and the initial thermal moment estimate; only reflected safe-sector mean drift uses the lower activity.

Dropping no-update dephasing branches does not weaken the received downhill count. Exact-drop splitting is into orthogonal pattern projectors and does not duplicate enabled activity. One ancilla per actual channel is explicitly counted, including its overlap incidence, reset norm, and potential contribution. Consequently C1, C_loc, H0, R0 and L0 may be huge but remain independent of n. The claimed physical size is 5n+M_anc, with M_anc<=L0 n; neither the old factor-five noise budget nor a free multilevel bundling is silently retained.

The current algebra, positive V, exact conservation [Q,V]=0, and local imaginary-time expansion used by the join are those proved in the separate lift receipt. No limit g/gamma→0 or finite-time reduced-channel approximation enters this composition.

## Reflected component and coherent logical transport

Define the full component by actual joint system/ancillary computational labels below Q<beta n, admitting all relevant full Pauli transition components. Projecting any such path onto system/witness labels gives a path below W<beta n because W<=Q. The original safe-component argument therefore applies to the projected system labels, with all projected local noise supports included in its alphabet. Its minimum representative and protected flatness conclusions are retained.

Each actual exact-drop A_alpha edge conserves Q. Its endpoints are in the same admitted component, so the component projector P commutes with C, Q, V and F. Ideal lowering reset maps stay in the component; their adjoint products are diagonal ancillary number operators. Thus actual and reflected IDEAL generators agree on component-supported states, including coherent states. Local exponential estimates are proved on the full system first and only then compressed—no locality is falsely assigned to a global projected jump.

Ancillary factors do not create protected logical operators. For every system label use the original small representative and correct ancillary labels separately in the analytic frame. The reflected Hamiltonian and resets are identity on the protected subsystem tensor operations on syndrome, gauge, ancillas and bath. The auxiliary reflected channel consequently preserves protected-logical/reference information exactly.

## Constants of the noisy Foster join

The local expansion gives the weighted ideal bound -a c_V Q+C2a^2 n. The actual noise contribution is at most 2C_loc a(h+gamma_noise)n. With the stated choices,

    C2a^2 <=a c_V theta/4,
    2C_loc a(h+gamma_noise)<=a c_V theta/4.

Their total remainder is <=k=a c_V theta/2. Above Q>=theta n the weighted drift is <=-k n; below it is <=k n. Since Q commutes with V, this proves exactly

    Lref*F<=-k n F+2k n exp[a(1+eta)theta n]I.

The choices eta<=1/4 and theta=beta/4 give

    (1-eta)beta-(1+eta)theta >=7beta/16>0.

Thus the author did NOT incorrectly reuse the old exponent margin. For the TWO-step Q boundary, V>=(1-eta)Q yields the stated occupation estimate. The already received exact dissipator/Hamiltonian boundary comparison then gives

    n(2h+4gamma_noise)T sqrt(C_init)
      exp[a(1-eta)b_Q]
      exp{-a[(1-eta)beta-(1+eta)theta]n/2}.

Here b_Q covers all admitted Pauli components on data, witnesses and new ancillas. Ideal terms contribute zero to the comparison. The bound is uniform over external references and bounded admitted bath couplings, with the previous well-defined-propagator and bath-initialization qualifications.

The exponent is strictly positive for fixed parameters, so an exponentially increasing storage interval with vanishing error follows. This is a conditional existence statement with potentially extremely small constants, not a useful finite-device threshold.

## Vacuum and thermal initialization

For encoded W=0 system input and ancillary vacuum, C annihilates the initial subspace, so V=Q=0 there and the initial F moment is exactly one. The Foster solution is bounded by the initial moment plus twice the displayed low-energy exponential; hence C_init=3 is valid (conservative).

For independent diagonal thermal ancillas, the product bound is the actual moment generating function of Q at a(1+eta). Under the stated product-log bound, ordinary Chernoff gives precisely

    p_out<=exp[-a(1+eta)(beta-theta)n].

This uses the Q moment directly, not a mistaken inversion of the F bound. With system W=0, all ancillary occupation patterns below cutoff are reachable from vacuum by monotonically adding their excitations, so they belong to P. The initial mixture commutes with P; removing and renormalizing its excluded part costs exactly 2p_out in trace norm. This independent ancillary truncation does not change the protected logical input. If p_out<=1/2, the conditioned F moment is at most twice the low-energy exponential, so C_init=4 follows conservatively from Foster. Contractivity carries the 2p_out preparation cost through the actual dynamics and terminal decoding.

General correlated preparation is not admitted merely by a moment bound: protected logical preparation and component-tail effects require their own argument. The draft states this restriction correctly. Added ancilla count L0 n also enters the required small thermal density and all upward-reset/noise budgets.

## Explicit ideal terminal consumer

The readout addendum requires the additional fixed-radius shrink R<(4/5)D_seq, where D_seq is the guaranteed radius of the source's actual sequential Tanner decoder in both CSS sectors. This shrink must also be reflected in beta and the subsequent parameter choices; it remains a fixed positive family constant.

For every canonical system/witness representative E_s with weight<R/4, conjugation by the fixed five-qubit-block Clifford U† gives a data Pauli of weight at most 5R/4<D_seq. The same fixed source decoder therefore corrects every such data Pauli modulo original stabilizers, rather than merely finding a matching syndrome. Both CSS components satisfy the radius condition.

In a Stinespring implementation of this fixed recovery, each admitted error acts as identity on the protected code tensor an error-label/gauge/environment operation. Hence recovery corrects the entire coherent span of these representatives with arbitrary gauge operators. Different syndromes are transferred to the discarded measurement record; equal-syndrome admissible errors have the same protected action. This establishes the consumer for arbitrary states of the reflected component, including entanglement with the newly added ancillas and the reference. The new ancillas may simply be discarded after system recovery.

Thus U† plus the original efficient ideal Tanner decoder replaces an executable minimum-weight oracle at final readout. This is an IDEAL terminal operation only: noisy gates, noisy syndrome measurement, decoder hardware faults, and finite-duration data faults during readout are not supplied by the storage theorem. Initial encoding is likewise not made free.

## Accepted statement and hard boundary

The whole finite-dilation join passes mathematically under the specified Tanner-family imports, actual bounded-support high-body J couplings, bounded local noise, and Markov lowering-reset model with separately bounded nonzero upward/reset noise. Fixed independent bath initialization yields the usual restricted-code channel statement; initially correlated baths retain the pointwise joint/output interpretation rather than an automatically defined system-only channel.

What remains unearned is substantive: native few-body implementation, useful finite code/costs, fixed-density Euclidean routing, finite-capacity microscopic reset reservoirs valid over exponential time, and reliable noisy terminal readout/encoding. The model is finite in auxiliary qubits but still uses real reset reservoirs. No claim of a closed finite quantum Hamiltonian memory or competitive hardware follows.

No new blocker was found in this bounded whole-model audit. The formal review is closed at this qualified exact-generator result.
