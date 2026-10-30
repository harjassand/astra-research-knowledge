# Actual retained-history logical Clifford teleportation receiver
30 October 2026. New receiving construction; independent scoped audit required. Prior measurement, handoff and feedforward proofs remain frozen. A concurrent factory is a separate supplied source until its own receipt is bound.

## 0. Ordinary mechanism and exact scope
Gate teleportation through a precomputed entangled state is established science, not a new gate principle: Gottesman–Chuang, *Quantum Teleportation is a Universal Computational Primitive*, arXiv:quant-ph/9908010, https://arxiv.org/html/quant-ph/9908010v1, especially Sections I–II. The present obligation is receiving that principle through the already earned actual noisy native-bank, protected-measurement and distributed-classical-control operations while retaining the same modeled bath.

Take three code-identical native banks A,B,C, each with K logical qubits, where K is the FULL logical dimension of the chosen Tanner code and K=O(N). A requested operation on K_active<=K coordinates is extended as U=U_active tensor I on the remaining coordinates. A carries an unknown state with arbitrary reference. Fix a classical, offline description of a K-qubit Clifford U. It is not a coherent/adaptive quantum program. The target known resource on B,C is

 |Phi_U>_BC=(I_B tensor U_C)|Phi_d>_BC,
 |Phi_d>=d^(-1/2) sum_x |x>_B|x>_C, d=2^K.             (T1)

The resource T1 has Bell pairs on ALL K native logical coordinates, including spectators of U_active. Spectator input coordinates on A may start in |0>, but resource spectators on B,C are NOT separate |0> states. This binding choice keeps the complete whole-bank Bell basis rank one and all d^2=4^K ideal outcome weights equal. The same logical X/Z coordinate basis is used on all banks. Full-bank transversal CNOT A->B must implement the matched logical CNOT in that basis, as in the accepted native matching construction. The receiver below consumes A,B and returns U rho U^dagger on C in a native safe/warm chart. It does not physically decode C.

### Supplied joint resource contract, not a marginal factory assertion
Let F_actual be the actual preceding source operation, including the old unknown bank A. Require a fixed common joint chart J_ABC and a CP/TNI auxiliary map A_src such that on its declared initial domain

 F_pos(rho_AE)=J_ABC [(Id_A tensor Prep_Phi_U,BC tensor A_src)(rho_AE)]

is positive and ||F_actual-F_pos||<=epsilon_src. Ordering of factors is fixed by the obvious register permutation. The auxiliary E contains all apparatus, consumed records from prior work, processor memory and the SAME retained finite bath. The chart must have hard measured-bank A,B radius/BUSY support and survivor-C basin/moment envelopes required by J2–J3 of the accepted measurement-survivor proof. It must be logical-independent, defined on the entire allowed auxiliary domain, with the strict Bell-capture/GPT/KL/erasure/native parameter intersection there. A target-specific known resource plus an unrelated marginal memory bound is NOT this contract.

For a stand-alone supplied state one may take a fixed auxiliary input rather than a map A_src. For an actual concurrent source the preceding contract must be established by its separate whole receipt. The legal probe domain of the receiver is the common logical/error chart extended across ALL logical ABC values with the SAME auxiliary support. This is not a claim that the factory physically prepares every such value: its certified error is used only for its actual fixed known Phi_U target. The distinction is binding.

## 1. Bell convention derived, including phases and references
For binary K-vectors a,b, put X^b=product_i X_i^{b_i}, Z^a=product_i Z_i^{a_i}. Apply logical transversal CNOT A->B and measure X on A with eigenvalues (-1)^{a_i}, Z on B with eigenvalues (-1)^{b_i}. Equivalently the analysis circuit is H^tensorK on A after CNOT, then computational measurements a on A and b on B. Define its normalized input Bell vectors

 |beta_ab>_AB=CNOT_AB^dagger (H_A^tensorK tensor I_B) |a>_A|b>_B.

For |psi>=sum_x psi_x |x>, direct contraction gives

 (<a|H_A^tensorK tensor <b|) CNOT_AB
       (|psi>_A tensor |Phi_U>_BC)
   = d^(-1) U X^b Z^a |psi>_C.                        (T2)

Indeed after CNOT, the B output label is y+x, so b fixes y=b+x; the A measurement contributes d^(-1/2)(-1)^{a dot x}, in addition to the resource factor d^(-1/2). The sum is exactly U X^b Z^a psi. Thus there is NO transpose or complex conjugate of U. Applying the inverse Pauli frame

 Q_ab=U Z^a X^b U^dagger                              (T3)

gives Q_ab U X^b Z^a=U exactly in this ordered convention. Global Pauli phases may be discarded only when passing to conjugation channels.

Equation T2 is an operator identity from H_A to H_C, so tensoring an arbitrary reference and arbitrary input auxiliary operators preserves it. In density-operator form each ideal branch is

 d^(-2) Ad_{U X^b Z^a}(rho_AR).

Here a,b are the DECODED LOGICAL Bell labels, not individual raw physical capture words. Their ideal probability is d^(-2), independent of the unknown input; no uniform-probability assertion is made for each raw record. The actual noisy branch probabilities and the positive TNI comparator's branch survival may differ: do not assert they are exactly uniform, and do not divide by them.

### Actual implementation of this convention
Use the accepted actual Bell instrument on physical A,B, with paired-coordinate fault grouping and the admitted pre-capture live-prefix bounds. It executes physical CNOT A->B, destructive logical X readout of A and logical Z readout of B, producing a,b in protected computation-code registers. Destructive X readout uses the swapped/transformed CSS checks and the matched logical-X label basis. It does NOT require a physical transversal H to preserve the original native code or claim a protected native logical H gate. All coordinate capture, field sanitization, corrected-word GPT, actual protected copy/reset-erasure and idles are included in the accepted Bell instrument. The measured M=AB logical Hilbert space is entirely consumed, with rank-one Bell projectors beta_ab.

## 2. Actual Clifford correction compiler and bounded resources
Because U is Clifford, Q_ab is a Pauli up to phase. Let F_U be its binary symplectic action on Pauli coordinates ordered (x,z). The frame to cancel has input coordinates (b,a), so the correction's logical binary vector is

 (x_out,z_out)=F_U (b,a) over F_2.                     (T4)

The reversed Z^a X^b versus X^b Z^a only changes a global phase. Fix physical logical-Pauli representatives once: binary matrices map these logical vectors to physical command bits (c^X_i,c^Z_i) for all N sites. Composing those matrices with F_U produces an explicit linear Boolean command circuit. That circuit is executed using the actual protected processor; offline computation of matrices is NOT an unprotected run-time computation on random a,b.

All 2N command outputs remain encoded until their separately executed top-down quantum decoders produce local physical controls. Two final command–DATA layers apply the fixed ordered Pauli product. Each native recipient has bounded control degree. No single decoded master bit is broadcast. All finite reset/port/decoder/control errors and native idles are counted by the accepted joint OR/cardinality law. The actual native C bank is ON during the polynomial command latency, OFF only during the fixed terminal physical-control window, and ON afterward without resetting its histories.

Uniformity across a predetermined family of Clifford steps is available without an unbounded U-dependent ideal circuit cost: use the signed Clifford tableau (including its phase/sign data for the resource) and a polynomial canonical symplectic elimination compiler for state and command descriptions. Equivalently restrict to supplied polynomial-size Clifford circuits with an explicitly common polynomial bound and pad them. K<=O(N), the fixed computation code/gate library, native hardware, strict margins, reset times and error strengths are identical for every step. Command evaluation is a fixed polynomial-size XOR network after offline matrices are supplied, padded to a common worst-case schedule. Constants do not depend on the actual outcome a,b. This does not receive arbitrary adaptive programs, unbounded online classical compilation or exponentially long U descriptions.

The resource Phi_U is a known stabilizer state. Its tableau is generated from K Bell pairs by applying U on C, with the actual physical Tanner encoding included in its known-state preparation description. A stabilizer-state Gaussian-elimination circuit supplies a polynomial physical ideal description for the ordinary protected factory. This is only compilation of the requested fixed source; it does not replace the separately required concurrent factory theorem.

## 3. Receive the actual Bell measurement and actual feedforward together
Invoke the accepted whole measurement-survivor handoff with M=AB, S=C, measured basis beta_ab, and feedforward Pauli Q_ab. Its proof runs the ENTIRE actual Bell operation on the SAME survivor-C killed process, not on a separately protected abstract reference. One endpoint safe cut plus positive branch repair derives the protected-classical/C source chart for the actual subsequent feedforward. All the measured-bank and survivor initial margins in Section 0 are required.

Let epsilon_native, p_safe, b_M be its native full/killed, joint endpoint-tail and complete Bell/capture/GPT/erasure/record-idle bad-map quantities. Let epsilon_W,FF, b_FF, epsilon_C,FF be its actual command waiting/cut, complete control bad-map and optional final native cooldown errors. With epsilon_src paid only ONCE for the actual input resource, define

 E_tel=epsilon_src+epsilon_native+2sqrt(p_safe)+2b_M
                          +epsilon_W,FF+2b_FF+epsilon_C,FF.             (T5)

Omit the last term only for warm rather than restored safe delivery. By the handoff J13 theorem, there are CP/TNI auxiliary maps B_ab on the common initial resource auxiliary domain and output embeddings J_out,ab such that the actual physical receiver, composed with the actual source, differs by at most E_tel from

 sum_ab J_out,ab [(Ad_Q_ab on C tensor B_ab)
                  (<beta_ab| rho_ABC,E |beta_ab>_AB)] J_out,ab^dagger. (T6)

Here rho_ABC,E is the positive source comparison with Phi_U inserted and A_src already applied. Equivalently absorb A_src into B_ab; never apply it twice. T6 is a comparison map, not a physical replacement, postselection or ideal detector. All modeled bath and old raw/control garbage are retained in B_ab.

No additional independent-fidelity multiplication occurs at this step: the handoff proof supplied one joint process and its actual branch maps. CP/TNI source comparison has complete norm at most one, so downstream uniform source-chart errors compose by addition, even with subnormalized branches. The native full/killed loss and safe-cut transfer already present in T5 must not be charged a second time or normalized away.

## 4. Full retained-history logical factorization after correction
Insert T1 and T2 into T6 and use T3. The branch logical operation is the SAME Ad_U for every a,b. More explicitly, in the common canonical native-C chart all the output embeddings can be written

 J_out,ab = J_C composed with (Id_C,logical tensor W_ab),

where W_ab embeds only auxiliary/protected-record labels. This uses the same zero-reference native code, forest and logical-coordinate convention for every Pauli branch. The final safe/warm support constraints are logical-independent. Any surviving protected-record label can be retained inside the auxiliary; if it is later garbage it need not remain a noiseless classical register. Thus there is no branch-dependent change of the native logical interpretation hidden in J_C.

Define

 A_tel = d^(-2) sum_ab Ad_W_ab composed with B_ab composed with A_src,   (T7)

when B_ab is taken before A_src (otherwise omit the final composition). There are d^2 branches; T7 is an AVERAGE, not an unweighted outcome sum. Each term is CP/TNI, so A_tel is CP/TNI. The entire positive comparison becomes

 T_pos(rho_AE)=J_C [(Ad_U tensor A_tel)(rho_AE)] J_C^dagger.             (T8)

This proves the desired full retained-history logical factorization. For a fixed logically independent initial auxiliary state, all retained consumed DATA, work, bath and outcomes in T8 carry no further information about the unknown input state. They may depend on U, prior auxiliary data and the Bell outcome, and they have not been reset. For a joint input on the explicit A/E algebra, T8 remains the tensor-channel identity with references; it does not assert that pre-existing input/auxiliary correlations vanish.

The Bell-outcome independence used here is the exact algebraic factor d^(-2) in the ideal resource contraction. Positive branch maps can have different trace defects, so surviving comparison outcome weights need not be uniform. Nonetheless after correction their logical action is identical and all survival dependence lies in A_tel, not in an unknown-input-dependent selection. No rare branch is ever normalized.

## 5. Trace normalization and a real next-cycle source chart
The actual physical source-plus-receiver is TP. Its E_tel proximity to T8 implies the auxiliary effect defect is at most E_tel on the SAME initial source domain. For fixed normalized auxiliary input sigma, writing p=Tr A_tel(sigma) gives 0<=p<=1 and 1-p<=E_tel. Hence after the common mathematical native DATA benchmark decoder and tracing auxiliaries,

 ||Out_actual-Ad_U||_diamond <= min(2,2E_tel).           (T9)

For a full allowed auxiliary parameter space, the same result is the trace-effect duality bound ||I-A_tel^*(I)||<=E_tel; no division by p is needed. The final benchmark decoder is NOT a physical gate or terminal detector.

With the accepted actual final cooldown included, J_C has fixed support E_C<=eN, M_BUSY,C<=bN and canonical radius<=eN/h, inside the SAME received native basin. On its ENTIRE auxiliary input space,

 J_C^*(P_C)=I,
 J_C^*(F_C)<=exp([g+s e]N)I,
 J_C^*(G_BUSY,C)<=exp(2C_B delta_B b N)I,               (T10)

with the received strict barrier and receiving gaps. These follow from the actual endpoint cut and spectral envelopes, not just from attained output-state moments. Taking the sum of branch auxiliary supports does not enlarge native energy/BUSY/radius bounds: each branch lies in the same fixed logical-independent safe cut; the span remains in that cut. All retained non-C systems may occupy their full finite auxiliary Hilbert space, restricted only as required by the declared hardware/noise model.

For next-cycle use, choose these FINAL hard thresholds from the common parameter intersection, not merely from feedforward H0. In particular the old-bank bare radius e/h+2f b, together with the future partner-bank radius, the accepted Bell pre-capture enlargement and the future capture allowance theta, must remain strictly inside BOTH the GPT decoding radius and the quantum KL radius for EACH measured bank. Concretely, if r_Bell(e,b;e_partner,b_partner) is the accepted per-bank post-Bell-prefix bare error bound, require r_Bell+theta N<rho_GPT N and 2(r_Bell+theta N)<d_native, with uniform positive gaps. Also retain the native basin, energy/BUSY floor and source-barrier gaps of T10. The received small-parameter hierarchy permits choosing e,b and capture/control allowances first, then hardware ratios/amplitude and finally noise/reset strengths to meet their finite intersection. Alternatively a later factory may earn a stricter final old-bank cut at its own charged cost; without one of these explicit receiving conditions this note does NOT claim the output is ready for the next consumed-bank measurement.

Thus C is a valid unknown-bank input chart for a later concurrent known-resource factory, including mathematical maximally mixed logical probes with arbitrary allowed dirty auxiliary states. The corrected output factor T8, not merely its reduced fidelity, establishes this. Consumed A,B need not be clean and may retain outcomes; they can be reset only by actual finite reset modules in the NEXT factory proof, while native C remains protected. This receiver does not perform or grant those resets for free. A three-bank relabeling is possible only when the separate concurrent-factory receipt receives this entire dirty auxiliary domain and returns the required joint source margins. Until that compatibility is verified, no repeated-cycle theorem is claimed here.

If only warm delivery is chosen, replace e,b in T10 by the accepted larger postcontrol warm bounds and use the corresponding strict source barrier; a later receiving operation must pay the necessary relaxation. For the subsequent-cycle interface in this note, include the final fixed cooldown and use the restored safe chart.

## 6. Cost, primary comparator, and limits
For fixed polynomial compiler bounds and K=O(N), known stabilizer resource compilation, actual protected factory, Bell record processing and protected command computation take polynomial N physical time, space and locations at e^{-Omega(N)} bank error, with potentially enormous exponents. The helper processor is POLYNOMIAL-size, not merely O(N) three-bank hardware. Native waiting is charged for those actual runtimes. Threshold constants are uniform over the predetermined Clifford family after all fixed code, reset, routing and hardware choices are made.

Ordinary concatenated fault-tolerant computation can implement the same Clifford operations directly, and ordinary gate teleportation is the strongest relevant comparator. This proof claims no resource or practical advantage. Its earned purpose is a physical internally controlled logical Clifford operation on the native protected state under the received shared-noise/retained-history interface.

No non-Clifford universality, magic-state source, adaptive arbitrary program, autonomous clock, raw unknown-state encoding, final physical classical detector, finite-dimensional geometric layout or practical threshold follows. A concurrent resource supplier remains a separate premise until its accepted receipt is explicitly bound. The one-step result does not automatically authorize discarded-history renewal or arbitrary future nominal couplings.

## Frozen inputs
- Joint measurement/survivor/feedforward receipt: recovery_measurement_survivor_handoff_20261030/review/FINAL_HASH_RECEIPT.md, SHA fda7f5c7c2c993a8b3290edb14cf941599bf6f2d0d10896465a879e490eb7c76, governing proof SHA 3b902901c3807fc4c9cc49e11de37dc0e94764838648eeeba14faee0ef078e40.
- Actual feedforward receipt: recovery_native_feedforward_20261030/review/FINAL_HASH_RECEIPT.md, SHA 67887c84d47319837830cf52354a213c8b83f27c2c06e4702b448228be60f364.
- Actual protected measurement/erasure receipt: recovery_native_measurement_20261030/review/FINAL_HASH_RECEIPT.md, SHA ef9859149fb74ae4753588c2f22c2d0d17c5319f9bd224e51a587c88b4204e10.
