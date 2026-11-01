# Independent assessment: repeatable protected operations with retained warm apparatus

Date: 2026-10-31. This analysis began independently of the root meter design. The finite parity-displacement proposal was supplied only after the independent construction below had been developed. The results are proofs and comparison tools, not a claim of a new threshold theorem or a completed experimental implementation.

## 1. Main conclusion

**The broad capability is already possible using ordinary tools.** Exact hot-bus/dirty-ancilla gates, transversal containment, operator quantum error correction, and local non-Markovian fault-tolerance theorems collectively allow useful repeated operations with an apparatus that retains arbitrary quantum state and correlations. Perfect preparation, perfect measurement, and an independent fault coin are unnecessary under the actual locality and strength hypotheses of those theorems. An unrestricted arbitrary noise process is not tolerable merely because its one-time marginal error rate is small.

The most complete close bosonic baseline is Xu, Zeng, Xu, and Jiang's 2024 GPI construction: universal error-corrected gadgets for four-legged cat qubits, with a qutrit ancilla, bosonic loss, ancilla faults, and extended-rectangle composition [1]. It is substantially stronger than an isolated matched-qutrit parity detector. Its presented ancilla-assisted operations start from a specified ancilla state, and its stated probabilistic scaling argument invokes independent jumps across gadgets. Those are material distinctions from a genuinely arbitrary retained state, but they do not establish an impossibility for ordinary apparatus: initialization can itself be a finite noisy operation, and the general non-Markovian threshold theorem already handles an indefinitely remembering bath [2].

**The credible constructive delta of the root proposal is an apparatus/time tradeoff:** a finite mapping plus finite pre/post observation may replace a long apparatus cooldown while rejecting the old internal state from a chosen output mode. The qubus control algebra is old; the potentially distinctive deliverable is the complete finite-window instrument, its finite signal penalty, its warm-loss/switching budget, and its actual repeated noisy decoder. A new general computational capability has not been established merely by combining those pieces.

The independent route below is a useful comparison baseline. It also gives a stronger guarantee in a different direction: an arbitrarily bad, persistent apparatus defect can be tolerated indefinitely when it is confined to a small fixed set of physical coordinates. This is a support restriction, not a weak-noise or independence assumption.

## 2. Exact finite warm-mediator compiler

Let two data qubits be d and e and let m be a mediator qubit in an arbitrary state, possibly entangled with the data, a reference, other mediators, or a large environment. Apply, chronologically,

1. controlled-X from d to m;
2. controlled-Z from e to m;
3. controlled-X from d to m;
4. controlled-Z from e to m.

For data basis values x,y, the mediator word is Z^y X^x Z^y X^x=(-1)^(xy)I. Therefore the complete joint operator is exactly

\[
V=\mathrm{CZ}_{de}\otimes I_m.
\]

This is a whole-Hilbert-space identity. It makes no assumption about a mediator state, a mediator temperature, or a product state at the gate entrance. It therefore continues to hold when the mediator carries correlations left by a previous faulty operation. The gate is a finite-dimensional instance of the known ancillary-qudit geometric gate construction [3]. It is not a new entangler.

### Microscopic fault support

An arbitrary fault during a primitive operation can be expanded in operators on that primitive's data qubit, the mediator, and the external bath. Propagation through the rest of the four-step word produces an operator supported on the intended two data qubits plus the bath. It cannot touch a third data qubit. For transversal gates between code blocks, this means at most one data position in each block.

The supplied verification program checks the exact 8-by-8 identity, all 60 nonidentity Pauli basis faults after the four two-qubit primitives, and all 64 incoming joint data-mediator operator basis elements. The numerical spectral-norm discrepancy of the ideal identity is exactly zero. These finite checks illustrate the algebraic proof; they do not replace it or claim to simulate a full fault-tolerant computer.

### Uniform coherent noise bound

Suppose each primitive joint operation differs in operator norm by at most epsilon from its ideal operation, uniformly over the external bath. Telescoping a product of four unitaries gives

\[
\|\widetilde V-V\|\le 4\epsilon.
\]

Use each four-step gate as one macro-location. A set R of r marked faulty macro-locations then has fault-path-sum norm at most (4 epsilon)^r, provided the unmarked operations are included as full physical operations and the normal locality condition is satisfied. The environment may be shared, retain state forever, and correlate different operations. No stochastic coin or bath reset was used in this argument. This is precisely the type of hypothesis to which ordinary non-Markovian fault tolerance applies [2].

The natural complete route is consequently: compile the two-qubit locations of a standard fault-tolerant universal circuit into these warm-mediator words; retain its noisy preparation, noisy syndrome extraction, actual correction/frame processing, and state-injection machinery; pay the four-coupling macro overhead and altered malignant-location counts. This is a constructive use of the existing threshold framework, not a new threshold result.

### Important qualifications

The four pulses must act on the full declared mediator Hilbert space. A physical transmon called a qubit is not a two-dimensional system when leakage is allowed. Either include those levels in the controlled operations or count leakage and its subsequent effects as faults. A finite even-dimensional mediator can use anticommuting full-space unitaries; a qubit is the simplest case.

An arbitrary shared operation on *other active mediators* in the middle of simultaneous loops can spoil locality. Sequential macro execution avoids this particular ambiguity. Parallel execution needs the ordinary physical locality assumption: one microscopic fault may affect its active mediator and bath, not every other active mediator at once. Arbitrary initial correlations are harmless by themselves; arbitrary interactions are not.

This compiler does not turn a permanent changed Hamiltonian into one transient fault. If a damaged mediator malfunctions each time it is reused, the usual temporal fault model counts each damaging use. The following architecture handles a restricted permanent-defect model directly.

## 3. Persistent-coordinate containment theorem

Use an [[n,1,d]] code in each data block. Assign mediator i permanently to physical coordinate i across blocks. At the logical level perform transversal operations, so physical coordinate i interacts only with coordinate i of other blocks. Let A_S be the algebra of arbitrary joint operators on all data qubits in coordinates S, tensored with arbitrary apparatus and bath operators.

**Claim.** Suppose all damaging apparatus/data operations throughout an arbitrarily long computation are supported in a coordinate union S, with |S|<=t, and every ideal logical operation is transversal. Then the complete physical computation differs from the target logical computation by an error in A_S. A code with d>=2t+1 corrects that error even if S is unknown, even when the errors are coherent across blocks, and even when their apparatus memory is retained indefinitely.

**Proof.** Every transversal ideal gate normalizes A_S: conjugating a coordinate-supported operator preserves its coordinate support. Moving each damaging operation to the final interaction picture therefore leaves it in A_S. The product of arbitrarily many such operators is still in A_S. Expand the final joint error in a Pauli basis on the data. Every term has weight at most t in each code block; all bath coefficients remain arbitrary. The ordinary Knill-Laflamme conditions, or their subsystem version when gauge degrees of freedom are retained, correct the entire linear span. The argument works for mixtures, coherent superpositions, and correlations with external references. It contains no operation-count factor.

This is an elementary but useful consequence of transversality and QEC, not an independently novel fault-tolerance mechanism. Its distinction from the weak-noise theorem is substantive: bad apparatus on the declared coordinates can be arbitrarily strong and malfunction repeatedly. The cost is a strict spatial support restriction and a restricted ideal gate family.

### The required old-error plus new-fault case

Let an old error on coordinate i survive a completed operation, correlated arbitrarily with apparatus M. In the next transversal operation a new apparatus/data fault occurs on coordinate j. The output has an expansion

\[
\sum_{\alpha,\beta}E_{j,\beta}E'_{i,\alpha}
U_{\mathrm{ideal}}P\otimes M_{\alpha\beta},
\]

where E'_i is the old error propagated through the ideal transversal gate. Each term has support contained in {i,j} in each data block. Thus distance five suffices. If the old apparatus defect replays forever on i, it still contributes only coordinate i. A new fault at j adds one coordinate, not an assumed independent probability factor.

### Concrete repeated operation and terminal readout

A conservative explicit choice is the twice-concatenated Steane code [[49,1,9]]. It supports a full transversal Clifford gate family using inherited Steane operations. It is larger than needed for the two-coordinate claim, but easy to specify and audit. One can run arbitrary sequences of logical H, S, and CNOT/CZ with warm finite mediators without introducing new within-block error positions. Non-Clifford resources and arbitrary noisy state preparation still need the standard fault-tolerant machinery; the persistent-coordinate theorem alone is not a universal-computation threshold.

For a terminal logical Z measurement, measure each physical qubit in Z, Hamming-decode each seven-qubit inner block, and Hamming-decode the resulting seven logical bits. Logical X measurement is obtained by the corresponding basis change. The program exhaustively checks every pattern of zero, one, two, and three flipped physical outcomes: 19,650 patterns in total, with no failure. Translation covariance of the Hamming decoder makes the result independent of which ideal measurement codeword occurred. The program also exhibits a four-error failure, at physical locations 0,1,7,8, so it does not quietly equate this simple decoder with optimal distance-nine recovery.

This explicit algorithm is not a claim that its classical hardware is perfect. Classical gate/storage faults must be included in its reliability budget, or the output must remain a protected classical block. AGP explicitly discusses this boundary: a faulty final single-bit decoding gate creates an O(epsilon) output-error floor; arbitrary suppression requires protected classical output or reliable classical processing [2]. An ideal decoder used in a correctness proof is a semantic map, not a physical free component.

## 4. Independent algebraic audit of the root parity map

The root supplied H=chi Z1 n+u Z2(a+a-dagger), u=lambda chi, and chi T=pi with the main outlet isolated. Let S=Z1 Z2. Completing the square gives

\[
U(T)=e^{i\pi\lambda^2Z_1}D(-2\lambda S)P_a,
\qquad P_a=(-1)^{n_a}.
\]

The identity is correct on the whole oscillator Hilbert space. The two conditional rotations become the same oscillator parity because exp(-i pi Z1 n)=P_a for either value of Z1. After the known local Z1 phase, the operation depends only on S. If S is a stabilizer or gauge observable, this is a legitimate logical-preservation statement even with arbitrary initial apparatus correlations. It is not necessary for the oscillator to be empty or to return to its initial state.

The close prior control algebra is van Loock et al. [4]. They derive exact conditional displacement from controlled rotations and unconditional displacement, and explicitly discuss H(epsilon,chi sigma-z)=epsilon(a+a-dagger)+chi n sigma-z followed by an opposite-sign-chi interval. The root's second-data-controlled force and a single positive-chi half-turn are a useful hardware-specific specialization; the underlying forced-oscillator control identity is established qubus machinery.

### Finite observation claim

Write the selected full output record as initial-state response F x0 plus signal h S plus input-field noise. Here F has two columns for the initial a and m operators. If the pre-observation window is observable on both initial modes, h is nonzero after the mapping and zero before it, and the output model remains linear, then h cannot lie in the column span of F. There is a mode w with w-dagger F=0 and w-dagger h nonzero.

The maximum retained signal norm is explicitly

\[
\|h_\perp\|^2=h^\dagger h-
h^\dagger F(F^\dagger F)^{-1}F^\dagger h,
\]

with a pseudoinverse when appropriate. This is a real finite-time resource cost. Small pre-observation duration or poor observability can make h_perp weak. Exact initial-operator rejection does not by itself establish a favorable signal-to-noise ratio, a low-error decoder, or protection from unmonitored loss during mapping. The root identifies Astra N1520 as the finite-observation precedent; I have not independently retrieved that earlier internal result and make no novelty claim concerning it.

### Strong containment alternative to a small warm-loss rate

There is a useful subsystem interpretation. For a weight-two gauge check G=Zi Zj, all apparatus-mediated diagonal operations on that pair lie in

\[
\operatorname{span}\{I,Z_i,Z_j,Z_iZ_j\}\otimes\mathcal B(M)
=\operatorname{span}\{I,Z_i\}\,\mathcal G\otimes\mathcal B(M),
\]

where mathcal G contains the gauge generator G. Thus arbitrary-strength apparatus errors can reduce to one physical Z error modulo gauge. With an incoming correctable Pauli E, the relevant set is {E,Zi E} times gauge; it is explicitly a two-error problem when E is on another physical coordinate. This holds on the error sectors as well as the codespace, because gauge factors can be commuted through Pauli errors with their signs tracked.

This can make a warm meter compatible with a subsystem code even when a uniform small-norm loss bound fails. It does not make an arbitrary high-weight partial check Z1 correctable. It also does not make the reported gauge-measurement bit reliable. Bacon-Shor/OQEC already provides the conceptual precedent [5,6].

## 5. Obstructions that any comparison must retain

### Unrestricted oscillator warmth and imperfect controls

An exact oscillator closure identity is state-independent. An imperfect one generally is not uniformly close to ideal over all oscillator states. Consider a residual U_epsilon=exp(-i epsilon Z p). For a zero-mean Gaussian with momentum variance V, the data coherence is exp(-2 epsilon^2 V). Fixed epsilon>0 and increasing V therefore give order-one dephasing. With a wavepacket concentrated near p=pi/(2 epsilon), the data operation approaches Z and the channel distance from identity approaches its maximum.

Equivalently, any nonzero Weyl displacement has operator-norm distance two from identity. A perturbative gate bound requires an energy/moment constraint or an algebraic error-containment argument. Under a mean-energy bound N, a simple energy-constrained estimate scales as epsilon sqrt(2N+1), rather than epsilon uniformly over all warm states. The program includes an analytic Gaussian demonstration, not a misleading finite-Fock cutoff.

### Intrinsic-loss example for the root map

With intrinsic amplitude decay rate kappa and the compensated force u(t)=u0 exp(-kappa t/2), the final passive coefficient at chi T=pi is indeed -exp(-kappa T/2), independent of Z1. However, for a coherent initial storage amplitude alpha and fixed S=s, the unobserved intrinsic-output waveforms for Z1=+1 and -1 differ by

\[
\Delta b(t)=-2i\sqrt\kappa\,e^{-\kappa t/2}
(\alpha+\lambda s)\sin(\chi t).
\]

Their coherent-state overlap magnitude is

\[
\exp\left[-\frac{4\chi^2(1-e^{-\kappa T})}
{\kappa^2+4\chi^2}|\alpha+\lambda s|^2\right].
\]

It approaches zero for sufficiently large old amplitude at any nonzero kappa. Endpoint passive-map equality does not prevent transient individual-qubit information leakage. A small warm-loss budget or the gauge-error argument above is therefore necessary. Equal thermal covariance between branches would not prove logical protection: a controlled unitary can dephase data while leaving the environment's marginal thermal density operator unchanged.

### Marginal error rates do not imply fault-order suppression

A hidden environment bit can trigger one damaging event in an earlier operation and another in a later operation. Both event marginals can equal p, while their joint probability is p rather than p-squared. Any claimed quadratic improvement must state a local-stochastic joint bound, a coherent fault-path norm bound, or another proven replacement. Mere small marginals and a retained-state label do not supply it.

### No entropy-free indefinite correction

No finite closed apparatus initially allowed to be fully mixed can repeatedly erase arbitrary syndrome entropy for free. In particular, a unitary on data plus an arbitrary full-rank finite apparatus cannot map r mutually orthogonal syndrome sectors into one codespace while leaving all entropy only in that same fixed-size apparatus: the input subspace has r times the output dimension. Gauge storage can postpone entropy removal but does not grant unlimited correction capacity. Ordinary noisy measurement, cooling, replacement, and reservoirs are allowed resources; a perfect reset is not required.

### No perfect final decision

No scheme protects a final single classical bit against an unconstrained fault on its final decoding gate. The output-error floor or protected output representation must be explicit. This is a known boundary of the ordinary threshold theorem, not a defect unique to the proposed meter [2].

## 6. Resource comparison and novelty judgment

| Route | What it already gives | Main cost or hypothesis | Meaningful comparison for the root proposal |
|---|---|---|---|
| Hot-ion/qubus geometric gates | Entangling operations independent of initial mediator state under exact closure; direct parity mechanisms also exist | Accurate control and loss budget; oscillator moments matter under imperfections | Root's half-turn uses known forced-oscillator algebra; compare full time, controls, and loss exposure |
| Matched qutrit detector | Ancilla relaxation can be prevented from spreading by matching dispersive shifts; demonstrated improved propagation suppression | Engineered matching, multilevel control, finite readout and initialization | Root may avoid ancilla reinitialization, but adds an oscillator, readout memory, switching, and a signal-projection penalty |
| Degeneracy-preserving or biased-cat detector | Sector-preserving parity readout, or suppression of dangerous ancilla noise by a biased cat [10] | Strong nonlinear engineering or stabilized cat preparation; residual nonideal terms and readout noise | A sector-scalar apparatus already treats its retained state as logical gauge; finite nulling adds a readout/reuse feature, not a new degeneracy-protection principle |
| GPI plus bosonic exRecs | Universal protected cat-qubit operations, finite ancilla faults, data loss, repeated measurement | Specified initial ancilla state in AAO, control assumptions, approximate bosonic code behavior; stated independent-jump scaling | Root must beat a complete gadget set at equal resources, not only an unprotected parity pulse |
| Subsystem/gauge measurements | Apparatus faults can be absorbed into gauge plus bounded physical support | Code overhead, noisy syndrome processing, locality | Particularly natural host for the root's weight-two check; not a new gauge principle |
| Erasure conversion | Strong benefit from detected physical error locations, with residual undetected faults and replacement procedures | Imperfect detection, residual non-erasure errors, replacement/reset | A finite nulling record is not automatically an erasure flag; detector errors remain ordinary faults |
| Non-Markovian FT | Unlimited bath memory and temporal/spatial correlations under local coherent-noise bounds | Small uniform coupling/fault-path strength and real entropy-export resources | Covers repeated composition in principle; arbitrary bath memory alone is not a novelty claim |
| Fixed-coordinate warm finite bus | Exact no-initialization entanglers; permanent defects can be confined to few coordinates | Four elementary couplings, one mediator per coordinate if used for permanent-defect protection, restricted transversal gate family | An honest ordinary baseline with no meter reset and explicit old-plus-new-error protection |

The root protocol can establish a practical enabling result in a constrained hardware regime: reinitialization is slow or poorly controlled; a reciprocal finite readout mode is unavoidable; the needed coupling switch is available; the projected signal remains strong; and the total added warm-loss/control/decoder error is smaller than the avoided reset/idle error. That requires quantitative comparison. It does not currently establish a capability unavailable to matched-qutrit/GPI or sector-scalar operations in general. In a genuinely sector-scalar implementation, retained apparatus state is already logical gauge, so the new filter chiefly addresses readout contamination and reuse latency.

For a defensible advance, report a Pareto comparison at equal apparatus count, available couplings/signs, mean-energy envelope, total cycle time, detector efficiency, and physical fault strengths. Use the actual noisy decoder and retained cross-cycle state in both arms. Show a region where finite nulling achieves a target logical error per useful repeated operation that the best matched-qutrit/reset or sector-scalar baseline cannot achieve under the same resource constraints. The boundary observation must include a pre-existing data error followed by a new apparatus/data fault; an isolated clean-input parity measurement is not sufficient.

## 7. Primary-source audit

Each description below is deliberately narrow. The claims above extend the sources only where an explicit derivation is supplied.

1. **Q. Xu, P. Zeng, D. Xu, L. Jiang, PRX 14, 031016 (2024).** https://arxiv.org/abs/2310.20578 and https://arxiv.org/pdf/2310.20578 . Universal four-legged-cat gadgets with one mode and three-level ancilla. PDF pp.2–3 defines AAOs with initialized |i>; pp.4–5 gives exRec reduction; p.5 explicitly says quantum jumps occur independently in gadgets; p.7 discusses repeating parity measurement three times for a second-order measurement error. Full source retrieved as turn64view2 / turn66view1 / turn66view2 / turn76view1.

2. **P. Aliferis, D. Gottesman, J. Preskill, QIC 6, 97–165 (2006).** https://arxiv.org/abs/quant-ph/0504218 and https://arxiv.org/pdf/quant-ph/0504218 . Section 11 allows a shared indefinitely remembering bath with arbitrary bath Hamiltonian and a local fault-path norm bound. Pages 5, 11–13 explicitly discuss classical-output protection and the final-decoder error floor; the concrete threshold counting assumes flawless instantaneous classical processing. Retrieved as turn64view4 / turn66view4 / turn66view5 / turn76view0. Terhal–Burkard's preceding theorem is https://arxiv.org/abs/quant-ph/0402104 .

3. **T. J. Proctor, S. Dooley, V. Kendon, PRA 91, 012308 (2015).** https://arxiv.org/abs/1402.6674 and https://arxiv.org/pdf/1402.6674 . Finite-dimensional mediator geometric phase gates from controlled qudit displacements, with spin-ensemble variants. Retrieved as turn71view0 / turn69view1. This is direct prior art for the finite-mediator word, not evidence that the present permanent-coordinate architecture is experimentally optimized.

4. **P. van Loock et al., PRA 78, 022303 (2008), preprint 2007.** https://arxiv.org/abs/quant-ph/0701057 and https://arxiv.org/pdf/quant-ph/0701057 . Exact conditional displacement from rotations/displacements; the simultaneous driven dispersive Hamiltonian and sign-reversed interval are on p.4. Retrieved as turn74view0 / turn76view3. **T. P. Spiller et al., NJP 8, 30 (2006)**, https://arxiv.org/pdf/quant-ph/0509202 , provides qubus gates and direct parity variants. **S. G. R. Louis et al., PRA 78, 022326 (2008)**, https://arxiv.org/abs/0804.3240 , analyzes bus dissipation and iteration suppressing correlated dephasing. **A. Sorensen and K. Molmer, PRL 82, 1971 (1999)**, https://arxiv.org/abs/quant-ph/9810039 , is a hot-ion gate predecessor.

5. **S. Rosenblum et al., Science 361, 266 (2018).** https://arxiv.org/abs/1803.00102 and https://arxiv.org/pdf/1803.00102 . Multilevel transmon/cavity experiment with engineered dispersive matching, error-transparency logic, factor-five ancilla-error propagation suppression, and excitation-induced dephasing protection. It does not by itself establish a universal repeated noisy-decoder architecture. Retrieved as turn71view2 / turn64view1.

6. **D. Kribs, R. Laflamme, D. Poulin, PRL 94, 180501 (2005)**, https://arxiv.org/abs/quant-ph/0412076 ; **M. Nielsen and D. Poulin, PRA 75, 064304 (2007)**, https://arxiv.org/abs/quant-ph/0506069 ; **D. Poulin, PRL 95, 230504 (2005)**, https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.95.230504 . Operator/subsystem error correction supplies the correct arbitrary-gauge-state language. Retrieved as turn63search0 / turn69view0 / turn63search3.

7. **A. Kubica, A. Haim, Y. Vaknin, H. Levine, F. Brandao, A. Retzker, PRX 13, 041022 (2023)**, https://journals.aps.org/prx/abstract/10.1103/PhysRevX.13.041022 ; **Y. Wu, S. Kolkowitz, S. Puri, J. D. Thompson, Nat. Commun. 13, 4657 (2022)**, https://www.nature.com/articles/s41467-022-32094-6 . Erasure encodings convert dominant identifiable decay into located errors while preserving a residual ordinary error budget. Retrieved as turn77view0 / turn69search0. Hardware erasure detection is not perfect: the primary circuit-based neutral-atom LDU experiment reports about 93.4% detection accuracy, https://doi.org/10.1103/PRXQuantum.5.040343 (turn69search1).

8. **G. P. Geher et al., npj Quantum Information 11, 39 (2025).** https://arxiv.org/abs/2408.00758 . No-reset syndrome extraction is already studied; memory and logical-operation timing can behave differently, and reset duration/infidelity changes the preferred regime. Retrieved as turn70academia48. This strengthens the need for operation-level timing and noisy-readout comparison.

9. **B. Royer, S. Puri, A. Blais, Science Advances 4, eaau1695 (2018).** https://pmc.ncbi.nlm.nih.gov/articles/PMC6269160/ . Parametrically driven nonlinear resonator parity measurements provide another direct-parity baseline. Retrieved as turn74view3. **A. Halaski, C. P. Koch, PRApplied 26, 034074 (2026)**, https://journals.aps.org/prapplied/abstract/10.1103/8bkm-b48b , identifies continuous parity-measurement corruption when logical and error sectors cannot both be protected by ordinary two-body meter couplings. Retrieved as turn74view2. Its continuous-operation obstruction does not itself rule out gated isolated mapping with explicit extra controls.

10. **J. Cohen, W. C. Smith, M. H. Devoret, M. Mirrahimi, PRL 119, 060503 (2017).** https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.119.060503 and https://arxiv.org/abs/1611.01219 . A strongly nonlinear high-impedance Josephson interaction yields degeneracy-preserving continuous parity-type readout for cavity cat encodings; this is a direct primary baseline for the sector-scalar idea. Retrieved as turn79view0 / turn79search1. **S. Puri et al., PRX 9, 041009 (2019)**, https://journals.aps.org/prx/abstract/10.1103/PhysRevX.9.041009 and https://arxiv.org/abs/1807.09334 , uses a stabilized bosonic-cat ancilla with strongly biased errors for protected syndrome extraction (turn78view0). The two designs should not be conflated: direct degeneracy-preserving coupling and biased ancilla noise are different mechanisms. **A. Sarlette and M. Mirrahimi, PRA 95, 032329 (2017)**, https://arxiv.org/abs/1604.04490 , additionally shows repeated weak parity measurements with cat-state probes in a lossy channel; a specified nonclassical probe state is essential (turn79view1).

## 8. Files and verification status

- verify_warm_mediator.py: exact finite-mediator identity/fault-support audit and explicit terminal readout decoder.
- verification_results.json: reproducible results, including the decoder's four-error counterexample.
- primitive_fault_table.json: all 60 checked elementary fault-basis propagations.

No complete noisy EC circuit or experimental time/resource optimum has been simulated here. The broad ordinary route is complete at the theorem/framework level; the persistent-defect claim is a proved restricted noise-model result; the root's finite-observation approach still needs the quantitative same-resource comparison described above.
