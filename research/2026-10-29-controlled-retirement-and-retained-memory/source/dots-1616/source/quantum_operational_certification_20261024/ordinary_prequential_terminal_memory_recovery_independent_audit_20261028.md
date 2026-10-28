# Independent review: ordinary prequential terminal memory recovery

28 October 2026. Auditor: `producer-workspace/review_prequential_memory_recovery`.

**PASS / received at its stated conditional, averaged, one-shot terminal-service scope.** Reviewed source `ordinary_prequential_terminal_memory_recovery_20261028.md`, SHA-256 `20e59391aeab608e0fb76dbaee3fee6825d434991892a2c63fe5e57634316079`. This receipt does not assert hardware implementation, successful empirical acquisition, a resettable source, a future frozen-decoder guarantee, or a learning advantage over ordinary convex optimization. No source samples were acquired. No author proof was edited by this reviewer.

The initial reviewed version was `f8c21ffbb0d7b0e0b1cec86e4ed0ef8c618ef987c4eb149f45b47a32b3e2406e`, now separately preserved by its owner. The only reviewed source changes were explicit product independence of the **full QR state**, and a prescribed dyadic solver-output mesh preventing recursive denominator growth. Both resolve clarity/finite-implementation obligations without changing the principal result.

## 1. Actual instruments, rather than iid tomography

The preceding classical record is an actual instrument record. Tracing unobserved quantum systems yields a conditional density operator for the retained source memory, not a fictitious classical hidden state. A fresh independently prepared logical input then induces a genuine channel `E_(t,h)`. For every such channel and each six-state label,

`E_W,b[d b W | h,j,s] = r_(j,s)`.

Consequently the actual single-copy estimator obeys

`E[g_t|h] = -(d/12) sum_(j,s) s sigma_j tensor r_(j,s)^T`,

which is the ambient Hermitian gradient of the displayed affine Choi loss. The transpose, the factor `d`, the uniform six-state probability, and the uniform `d^2` Pauli-word probability are consistent. Identity-word outcomes are correctly deterministic. Recording just parity is adequate provided the conditional memory is obtained by the **actual local instrument**, with unused individual outcomes summed; it is not legitimate to substitute a different coherent parity instrument. The source explicitly fixes the all-probe measurement instruments, so this distinction causes no gap.

For a trace-preserving qubit channel, the six-state loss is `(2/3)(1-F_e)`, also for nonunital channels. Direct Hilbert–Schmidt calculation gives `||g_t||_F^2=d^5/2` and operator norm `d^2/2`. The chosen rational-step bound satisfies `||g_t||_F<=G` and `G^2<=2d^5`. These are conditional identities and deterministic bounds, not iid concentration claims. There is no source-memory reset and no imported Bures bank.

## 2. Finite physical iterates and the new quadratic objective

The received Choi-repair/finite-synthesis import is pinned to `ordinary_local_mixed_gauge_cptp_erm_addendum_20261028.md`, SHA-256 `1c77dc05f10750e0c53ce51a6c9676f529883f421b4f8ac472d610de62d3959c`. Its existing independent mathematical and controls receipts were read. Only its known-center finite optimization, rational feasibility repair and finite synthesis are used. Its iid acquisition theorem is not transferred.

For normalized Choi matrices, `||J||_F<=1`, diameter is at most `sqrt(2)`, and initial squared distance from the replacement center is at most 1. Thus `||Y_t||_F<=2`. The imported trace-norm repair bound divides by `d` to give `||Jphys-Jtilde||_F<=9 delta`. Since `Jphys` is feasible, `||Jtilde||_F<=1+9 delta`. Therefore the **quadratic**, rather than old linear, objective changes by at most

`9 delta (||Jphys||_F+||Jtilde||_F+2||Y_t||_F) <= 9 delta(6+9 delta) < 100 delta`

for `delta<=1/100`. This independently establishes the new transfer of the repair to squared-distance optimization. The stated objective/interior/repair allowances leave genuine slack below `xi`.

The added grid is adequate. Entry rounding changes a Hermitian `2d`-dimensional matrix by at most `4d u` in operator/Frobenius norm, and its output partial trace by at most `8d u`. Starting at residual `delta/2`, `u<=delta/(64d)` leaves both certified residuals below `delta`. In normalized variables the Frobenius change is at most `4u`, so the stated `u<=xi/(1024d)` also fits the objective slack. `delta=xi/1024` and the fixed dyadic grid allow each repaired iterate to have a new bounded-size common denominator independent of earlier denominator growth; the rational gradient and rational `eta` preserve polynomial entry-bit length. The Choi variable is dimension `2d`; a Schur-complement epigraph may use a larger polynomial-size SDP lift, which does not alter the claimed polynomial-in-`d` scope.

The known affine interior and bounded radius support a deterministic finite weak convex solve at these precisions. The result is a theorem under that explicitly supplied **certified finite implementation contract**, not evidence that a particular floating SDP package was executed. Exact rational positivity and TP are essential. An uncertified replacement preserves physicality but cannot claim the optimization guarantee for free.

## 3. Pathwise regret and exactly which comparator it implies

Let `P_t` be the exact Euclidean projection. The variational inequality gives `||J_(t+1)-P_t||_F<=sqrt(xi)`. Since all three feasible points have mutual distances at most `sqrt(2)`, replacing `P_t` by the repaired iterate adds at most `2 sqrt(2) sqrt(xi)<3 sqrt(xi)` to its squared distance from any fixed comparator. Telescoping then gives exactly

`1/(2 eta)+(eta/2)N G^2+3N sqrt(xi)/(2 eta)=(11/8)G sqrt(N)`.

Predictability of `J_t` and conditional unbiasedness justify taking expectations against each **fixed** comparator. Compactness/continuity allow minimizing the resulting expected occupation objective over a deterministic fixed decoder. This is external regret on the actually generated all-probe occupation. It is **not** regret against histories produced by a different earlier probe/control policy, or a sample-path-specific hindsight optimizer. The manuscript expressly excludes both substitutions. Adaptive source memory causes no extra term because the comparator is evaluated on the same visited conditional channels, not its own counterfactual memory path.

## 4. Private terminal time gives an actual reference-preserving channel

This is the central new transfer and it is valid under the stated complete-port contract.

* `T` is independent private randomness; the full initial `QR` state is product with source memory and acquisition randomness.
* For each `t`, conditioning on `T=t` leaves the actual first `t-1` probe/control/instrument process identical to the all-probe prefix. The fixed public padded schedule, private current decoder and hidden role prevent a different source map from being selected before the current call is complete.
* The held `QR` datum remains untouched; hence on history `h` it is product with the actual conditional memory. The complete current source map induces `id_R tensor E_(t,h)`, followed by the pre-fixed decoder.
* The payload is terminal and its output isolated. Neither equality of the post-call memory instruments nor any prediction of later source behavior is required.

Averaging therefore gives the exact CPTP identity

`Lambda = (1/N) sum_t sum_h p_t(h) D_(t,h) E_(t,h)`.

It is an equality of channels, so tensoring **any retained reference** is valid; the proof does not merely match average input marginals or Bell scores. The source may discriminate the actual quantum input in its fixed complete CPTP map. It may not receive an extra current role, timing, routing or complete-port signal selecting a different map. If that trusted-interface premise fails, the transfer fails, and no estimation accuracy repairs it.

Linearity of Bell fidelity and the `3/2` six-state conversion give excess at most `3G/sqrt(N)`. The specified least power of four gives excess at most `epsilon/2`, `N<144G^2/epsilon^2<=288d^5/epsilon^2`, and counts the payload among at most `N` calls. Mean calls are `(N+1)/2`.

The conclusion is for the averaged terminal channel, **not** conditioned on `T`, the final transcript, or a retained twirl key. Untwirled Bell loss is not numerically equal to worst-input or reference-stable trace-distance error; a standard safe qubit bound is half-diamond distance at most `min(1,2 sqrt(1-F_e))`. The optional private Pauli twirl changes the service, preserves Bell fidelity, and makes half-diamond distance equal to Bell loss after averaging its private key. The manuscript states these distinctions correctly.

## 5. Supplied CP-memory family and the strongest same-occupation oracle

The complete map in (12) is CPTP even on correlated logical-memory inputs because its summands are CP and the summed memory instrument is TP, followed by a unitary. Its CP-order dominance is a supplied structural promise, not inferred from finite data. On every conditional memory state it implies `H_I>=H_alpha`, including singular and noncommuting gauge blocks.

For any CPTP terminal decoder, the positive dual effect `E=(id_R tensor Dtilde†)(Phi_0)` has `Tr_R E=I_(LG)/2`. Each `T_alpha` is equivalently the positive Bell compression `<Phi_alpha|E|Phi_alpha>`, and the four blocks sum to `I_G`. Therefore

`F_e=sum_alpha Tr(H_alpha T_alpha)<=sum_alpha Tr(H_I T_alpha)=Tr H_I`.

The single fixed decoder `Tr_G Ad_(U†)` attains equality at every history. Thus its expected risk equals both the fixed-comparator optimum and the historywise optimum among all terminal CPTP decoders with the same accessible physical output. This is a legitimate strong informed oracle on the **same** occupation; it is not an oracle that redesigns earlier controls or accesses retained source memory. No gauge floor, visibility, contrast estimate or environment reconstruction is inserted.

The deterministic-cutoff obstruction is also correct: the two fixed-unitary timer worlds give identical first-`K` quantum experiments, while their designated payload maps average to complete `X` dephasing, whose recoverable Bell fidelity is at most `1/2`. A fixed inverse-unitary oracle has zero loss in each world. The example does not defeat private randomized stopping; it demonstrates why a future deterministic cutoff claim would be invalid.

## 6. Resource and operational-error accounting

The ledger includes all `N` potential source calls/compilations, all source-side memory retention, finite classical update and compilation time, trusted payload storage during that time, local measurement settings/outcomes, O(`d^2`) bounded-bit Choi storage, optional O(`Nw`) raw records, and at most two additional decoder reset qubits. Kraus rank at most `2d` gives a `4d`-dimensional unitary embedding; generic synthesis is polynomial in `w` times `4^w` before precision/routing overhead. This is exponential in patch width, not an efficient hidden global receiver oracle.

Finite two-bit rejection has per-label exhaustion probability `4^(-R)` and total at most `N4^(-R)<=nu_rng`. With padded finite sampling, fallback loss belongs inside the single whole-process allowance. There is no fictitious confidence event for the expectation theorem, no infinite rejection loop and no numerical-failure probability invented to hide an uncertified optimizer.

The remaining `epsilon/2` must bound the **complete actual-versus-declared-ideal causal experiment**, including trusted input/measurement controls, padding/role sealing, storage and terminal synthesis. The benchmark in (11) is the declared ideal all-probe occupation. A claim relative to a separately perturbed actual benchmark would require paying its difference too; the source explicitly warns against double absorption. No uniform hardware threshold or clock-speed theorem is supplied or inferred here.

## 7. Independent deterministic evidence

The companion `ordinary_prequential_terminal_memory_recovery_independent_check_20261028.py` is independent of the owner's fixture. It was executed successfully and its JSON records:

1. Exact complex-rational coherent-memory channel, actual six-state/Pauli expectation, full gradient equality and a nonunital decoder's six-state/Bell identity.
2. Exact rational feasibility repair with all 15 nonempty principal minors strictly positive, exact TP, and squared-objective perturbation below `100 delta`.
3. Noncommuting singular gauge blocks with a common-dominance oracle fidelity `2/5`; three explicit physical decoder duals have positive blocks summing to identity and fidelities `2/5`, `194/845`, `5201/21125`.
4. A numerical **complete-instrument** enumeration retaining a coherent qubit source memory, a three-dimensional reference, and a history-dependent physical decoder over three possible terminal slots. Prefix branch counts are `1,42,1764`; all masses are one to numerical precision. Direct propagated reference output agrees with the separately assembled averaged-channel action to `5.28e-16`; the full QR/memory factorization residual is below `1.78e-18`.

The three-slot fixture tests the transfer identity; power-of-four horizons are needed only for rational learning steps. Its decoder is not the projected learner. These are deterministic mathematical checks, **not** random source samples, an OGD performance pilot, an executed SDP solver or hardware evidence. The universal claims rest on the proof above, not these finite fixtures.

## 8. Acceptance boundary

No unresolved load-bearing mathematical objection remains within the frozen premises. Receive the new result as an ordinary finite online-CPTP learner with a privately timed **one-shot averaged terminal channel**, arbitrary retained source quantum memory, a fixed encoder/known physical patch, fresh full-QR independence, certified paid controls, and the supplied common-algebra CP-order corollary. Do not promote it to iid acquisition, reusable future recovery, unknown-patch/encoder discovery, counterfactual-policy regret, a per-history high-confidence certificate, or a separation from equally informed conventional learning.
