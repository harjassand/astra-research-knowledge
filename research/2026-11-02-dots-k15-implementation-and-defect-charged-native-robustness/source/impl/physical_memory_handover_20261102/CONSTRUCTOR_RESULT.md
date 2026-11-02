# In-situ quantum handover: concrete operation, residual-state class, and the native basin gate

2 November 2026. Independent positive-constructor pass. The initial candidate—grow and protect the target collectively in place, instead of moving one growing FT block per final carrier—was recorded to the parent before reading its access approaches. The source code/thermal results below are used within their existing internally reviewed scope, not independently re-certified here.

## Result first

**A real constant-density quantum handover is available at the CSS-code layer:** interleave two identical macroscopic code blocks, perform transversal CNOT, measure the old block in X, and decode/track the logical phase. A sampled nonzero target syndrome is accommodated by a known classical frame shift. This transfers an arbitrary unknown logical qubit, including its external entanglement; it is not classical readout or known-state preparation. Only O(n) physical registers are needed, not n separate polylog-sized blocks. Its fault exposure must be analyzed as a whole active extended rectangle, including target preparation and waiting.

**This is not yet a native noisy WRITE theorem.** The attainable output has a finite-density residual error distribution, not the exact actual joint Gibbs gauge state. Moreover the previously reviewed filtered-parent preparation starts from H0+onsite bath+weak V; it has not been extended to the strongly noncommuting native clock reference. Those are two separate missing joins. At V=0 the native prefix-gauged reference commutes with the decoded logical algebra for every gauge state, so a globally trace-close Gibbs target is unnecessarily strong there. For nonzero allowed V, a local nonstationary-basin theorem for the explicit output class below is the right operational gate.

No permission denial, unavailable file, or access block occurred. The unmet gate is mathematical/physical, not operational tooling.

## 1. Resources and input, without a routing fiction

Use the actual bounded-density 3D CSS code C_n with one logical qubit and its fixed decoder D(s). Let V_s=D(s)V_0 be the syndrome-s logical embedding; Pauli phases are irrelevant. Use constant-many interleaved copies of each local physical site for source A, target B, and bounded-degree check ancillas. A constant rescaling of the 3D embedding admits them at constant density and bounded link length. No growing-size block is placed in a constant-volume ball.

The source arrives **encoded in C_n** with a stated active-input error/residual-syndrome contract, or a separately charged code-conversion protocol supplies that contract. It is not enough that it is encoded in an arbitrary unrelated code. The source is continuously protected while the target is prepared, while syndrome records are processed, and while handover results propagate. A bare unknown input retains its first-contact error floor.

This is a mechanism for a macroscopic code-to-code port, not proof that every convenient small port admits cheap conversion to this code.

Data, clocks, accessible bath spins, check ancillas, classical controller memory, resets, coherent controls, and all switch modes are counted. The active comparator gets precisely the same resource envelope. In particular native clock dimension/energy is the admitted K-dependent one, not a fictitious seven-level device.

## 2. Exact signed-syndrome one-bit teleportation

Prepare B in V_s|0>, with s sampled independently of the incoming logical state. Apply transversal CNOT A→B. For a CSS code this is encoded CNOT. Measure every source qubit in X; classical decoding of the outcomes supplies the encoded X measurement bit m. Apply or track logical Z^m on B.

For the zero-syndrome inputs this is the ordinary identity

    |psi>_A |0>_B -> CNOT -> X_A measurement m
                           -> Z_B^m |psi>_B.

It holds as a channel on arbitrary reference-entangled inputs.

A physical target Pauli E_s=X(x)Z(z) propagates through transversal CNOT as

    CNOT (I_A tensor E_s,B) CNOT†
       = Z_A(z) tensor E_s,B.

Consequently the known z shifts source X measurement outcomes; subtract that shift before decoding the logical m. The target then contains **E_s V_0 |psi>**, not a state with an unknown syndrome-dependent logical phase. Known source frames can be incorporated similarly. This is ordinary classical frame arithmetic, not a noiseless quantum operation; its implementation errors are charged.

The transversal contact has bounded depth and bounded error spread. The individual physical X measurements can be simultaneous local operations, but reliable **logical** m requires the actual classical decoder and full correlated fault-history analysis. Two individually decoded-correct incoming blocks do not automatically give a correct joint measurement.

A finite calculation in `steane_signed_teleport_check.py` verifies the identity for a [[7,1,3]] Steane block entangled with an external reference, 32 signed-target Pauli frames, and all 512 nonzero measurement branches. Minimum branch fidelity was 0.9999999999999996; total-probability discrepancy was below 1.7e-15. This validates the algebra, not the actual recursive code's circuit-level threshold.

## 3. In-place target preparation is possible in principle, but its threshold must be earned

For a CSS target |0_L>, initialize physical |0>s, measure X checks, and choose the appropriate Z correction. Repeat noisy syndrome acquisition with active protection and account for hook faults, measurement faults, local idles, classical errors, and decoder delay. Apply the known D(s) as parallel local Pauli pulses or equivalent explicitly implemented frame-covariant controls. Merely labeling a virtual frame does not physically create the sampled thermal syndrome.

Bounded check weight and degree give a bounded-color local syndrome-extraction schedule, albeit with possibly huge fixed constants. They do **not** alone prove a measurement-noise threshold or a low-latency classical implementation for this family. The banked component theorem is a syndrome/decoder-stability theorem, not by itself a circuit-level repeated-measurement theorem.

If the target construction takes T_prep and the decoder has delay T_dec, all source/target waiting locations belong in the active error ledger. The handover cannot end at the measurement timestamp while the source or target sits bare awaiting its frame. Pauli-frame processing may be delayed while active correction continues; actual non-Pauli subsequent controls require the relevant frame in time.

This removes the old *geometrical* n-independent-block release problem, not these *fault-tolerant circuit* obligations.

## 4. Explicit residual class under a declared Pauli service model

Consider gate-independent stochastic Pauli faults at data preparations, Clifford gates, idles, measurements, and Pauli pulses. Noiseless classical processing is not assumed: a protected classical subsystem contributes an explicit bad-history probability. The commanded syndrome s changes only known Clifford/Pauli frames. Under this covariance, the physical fault distribution can be drawn independently of s.

Suppose a whole-rectangle analysis yields a syndrome-frame-covariant good event on the unconditional fault space, whose complement has probability delta_act, and a residual physical Pauli E on that event. Define E=I on its complement. Require this UNCONDITIONALLY defined residual to have local-stochastic parameter p_res. The good event and residual function must depend on the fault history rather than on the sampled syndrome; uniform logical correctness alone does not imply this contract. The decoder's active operation need not produce independent site errors; local stochasticity is the stated weaker contract:

    Pr[F subset supp(E)] <= p_res^|F|.

The reference-safe output class is then

    W_n(rho_LR) = sum_(s,E) mu_n(s) nu_n(E)
       (E V_s tensor I_R) rho_LR (V_s† E† tensor I_R),       (1)

up to diamond error at most 2 delta_act. The independent product is justified by the frame-covariant circuit contract, not by conditioning on success. More generally use the actual joint law and prove its joint sparse-source bounds. A good-event conditional law must never be substituted for an unconditional independent law.

This residual class is far more concrete than saying “the memory has been FT-prepared.” It specifies where the unknown qubit is, the physical syndrome noise, its correlations, and the exact missing dynamical input.

### Static logical-correctness bound for (1)

Assume mu_n obeys the banked local-stochastic syndrome bound with parameter q_s. If a physical error affects at most b checks and each check sees boundedly many candidate error sites, the induced syndrome of E obeys a bound q_e <= C p_res^(1/b), with C a fixed geometry/alphabet constant. Each fixed site-order prefix E_<=j obeys the same bound. Independence and a union-over-assignments argument imply

    s_j = s + syndrome(E_<=j)

has local-stochastic parameter at most q_s+q_e: for any required check set T, assign each occupied check to the original s or to the residual-error syndrome and sum over assignments.

Apply the reviewed ANY-local-stochastic decoder-instability theorem at every prefix. There are only O(n) prefixes and a constant Pauli alphabet; no independence of the current error from s_j is needed, because each actual jump event is contained in the union of the corresponding fixed-Pauli bad events. Thus, in the theorem's small-fugacity regime,

    Pr[decoded logical E is nontrivial]
       <= poly(n) exp[-c n^eta],                              (2)

and the decoded diamond error is bounded by twice this probability plus 2 delta_act. The same argument treats an external reference exactly because it is a classical mixture of Pauli channels.

Equation (2) is **initial logical fidelity**, not long-time stability under the actual noncommuting H. It does not certify a hidden active circuit threshold; its premises are explicit.

## 5. Native clocks and an honest physical starting-state class

Let U be the exact bounded-depth controlled-prefix dressing and

    H_nat = U H_anc(S) U†.

The banked native construction gives [H_anc(S),Q_L]=0 for every decoded logical operator Q_L, including for gauge states far from Gibbs. Therefore, at V=0, a dressed output satisfying (2) retains that decoded information under H_nat for all times. This statement allows arbitrary clock gauge states; it uses the exact reference symmetry, not a ground-space approximation.

A concrete in-place startup can initialize clocks with noisy local resets, initialize accessible bath sites with their noisy local thermal/reset service, perform the bounded-depth U circuitry, and enable native couplings over a finite window. Its output has the schematic, physically meaningful form

    U N_sw [ sum_s mu(s) V_s rho_LR V_s†
                       tensor xi_clock,bath(s) ] U†,          (3)

where xi and N_sw are the actual outputs/channels of those charged circuits. Clock reset faults, dressing faults, finite switching time, and the still-running environment belong in them. These objects are NOT declared to be the native conditional Gibbs state or independent Pauli noise unless the actual circuit establishes that claim.

A candidate particularly worth testing is a dilute noisy-vacuum clock startup, optionally followed by local gapped clock dressing. It avoids assuming a globally thermalized clock bank. It also produces nonequilibrium clock energy and therefore needs an actual basin theorem; being “colder” in one basis does not establish native-Gibbs domination. No such native dressing/preparation theorem is asserted here.

At nonzero generic weak V, native logical commutation is only a typical-sector property. The old exact-H equilibrium proof uses stationarity to keep the decoder-bad sector rare. Equations (1)–(3), even when initially decoded-correct with overwhelming probability, do not supply that stationarity.

## 6. Minimal useful missing theorem, rather than excessive trace matching

Fix the actual physical H=H_nat+H_B+V used after switching; do not silently replace it by a commuting surrogate or a retuned sampler. For the **actual** output family Sigma_n(rho) of a specified active handover circuit, a sufficient operational theorem is

    sup_rho || Dec_M Tr_B[e^(-itH) Sigma_n(rho) e^(itH)]
                         - rho ||_1
      <= epsilon_write(n) + epsilon_hold(n,t),                (4)

reference-safely for t up to exp(c n^eta), where epsilon_write→0 and epsilon_hold is small on that horizon. An intermediate sufficient form controls the time-dependent expectation of the enlarged decoder-bad projector, with the correct insertion/operator estimates used by the exact-H proof. An initial small bad-projector expectation alone is insufficient.

A local/multiplicative sparse-fault theorem for (1)–(3) could establish (4) without preparing the entire joint Gibbs state in trace norm. Conversely it may reveal the required clock preparation or a restriction on allowed V. Both outcomes are more informative than assuming perfect release.

The parent's soft-energy-cutoff benchmark fits this distinction: O(1) or a sub-barrier number of local release faults may admit a tolerable energy-transfer/relative-domination cost. At fixed residual rate, O(n) faulty sites/energy are typical. A global exp[O(n)] domination factor overwhelms exp[-c n^eta] when eta<1. This is failure of that proof method, not a proof that the memory fails.

## 7. Two transfers explicitly NOT earned

1. **Native filtered-parent preparation.** `filtered_code_preparation_20261101/ROOT_FILTERED_THERMAL_ENCODER_JOIN.md` uses a commuting H0 plus onsite bath reference and sufficiently weak V. Strong native internal clock hopping is not that reference. The exact prefix gauge yields an ancilla Hamiltonian depending on S, not an automatically commuting/weakly perturbed product clock state. Its conditional quantum clock preparation, parent gap, and quantum ensemble interface need their own proof.
2. **Syndrome measurement on actual Gibbs.** Measuring original checks generally removes V-induced off-diagonal syndrome coherences. A small local V does not imply small total trace disturbance over an extensive array. This may still be an operationally harmless basin change, but that is precisely a new theorem. Do not run ordinary stabilizer correction on the actual Gibbs state and claim the old gauge/bath correlations remain untouched.

## 8. Same-resource comparison

The strongest active alternative receives the same 3D volume, constant-density controls/ancillas, coupler modes, reset/cooling services, gate rates, classical hardware, and noise assumptions. If noisy switching/cancellation of native interactions is supplied to the loader, it is supplied to the comparator. If it is unavailable, neither side may presume it.

A conservative established active baseline is a geometrically local concatenated-code memory with all transport, idles, and recursive decoding charged. For a specific circuit family with effective fault recursion

    p_(r+1) <= A p_r^2,

and total physical space factor B per concatenation level, choose r so T p_r <= epsilon. Its space scales as

    S_active(T,epsilon) = O([log(T/epsilon)]^kappa),
    kappa = log_2 B,

with additional explicitly charged polynomial-log factors for the chosen local/control implementation. For the passive advertised T=exp(c n^eta), this becomes polynomial in n, approximately n^(eta kappa). Thus the passive lifetime exponent alone does not establish a space advantage; the inequality eta kappa<1 is a concrete benchmark to check after instantiating the active architecture and its constants. No favorable numerical exponent is asserted without that implementation.

Relevant primary sources establish local-gate threshold architectures and thresholds for weak local/non-Markovian Hamiltonian noise; they do not make this candidate code's circuit-level threshold automatic:
- Gottesman, *Fault-Tolerant Quantum Computation with Local Gates*, https://arxiv.org/abs/quant-ph/9903099 .
- Aliferis–Gottesman–Preskill, *Quantum accuracy threshold for concatenated distance-3 codes*, https://arxiv.org/abs/quant-ph/0504218 .
- Aharonov–Kitaev–Preskill, *Fault-Tolerant Quantum Computation with Long-Range Correlated Noise*, https://arxiv.org/abs/quant-ph/0510231 .

At equal *available* resources, an optimized controller may always choose to turn control off and use the passive protocol, so the full allowed-control optimum cannot be worse than the passive subclass. This dominance observation is not a substitute for comparison to a specified continuously active FT code, and it does not compare integrated energy costs by itself.

The potentially meaningful passive benefit is reduced ongoing control/entropy-removal work after a charged rare write. A continuously active memory pays repeated syndrome/reset work over T; a completed passive loader would pay its preparation and handover plus its actual cooling/hold costs. No equal-total-energy advantage is proven until those costs and the complete basin theorem are supplied. If the same total energy budget cannot run the active code throughout T, report that as the resource tradeoff rather than denying it its controls.

## Verdict

The independent candidate produces a genuine quantum code-to-code handover architecture and an explicit residual-state target; it resolves the conceptual necessity of moving n growing protected blocks into n dense carriers. It does **not** resolve the stronger native noisy preparation/hold join. The next decisive test is (4) for a fully specified locally imperfect startup, with native clocks and switching included. Until that passes, the honest consequence is an earned ideal passive-storage theorem plus a partial physical interface, not a usable scalable passive memory or a demonstrated advantage over active FT.
