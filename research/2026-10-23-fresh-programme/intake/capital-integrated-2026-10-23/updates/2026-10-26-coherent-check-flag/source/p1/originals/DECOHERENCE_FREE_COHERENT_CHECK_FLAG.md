# ASTRA Pro1 continuation — decoherence-free coherent symmetry-check flag

**26 October 2026, Australia/Brisbane.** Scientific research record; analytical constructions and executed finite-dimensional quantum reference calculations, **not hardware experiments** or claims of novelty. All relevant numeric evidence is stored beside the executable scripts, not inferred from filenames.

## 1. Scientific decision and strongest result

The preceding staged receiver uses a coherent controlled-Pauli `T=X_p X_q Z_a` check before and after an arbitrary uncontrolled system–bath operation, then a code-occupancy projector. Its mathematical accepted operation is `P (K+T K T)/2 P`. This depends on *coherence of the check flag across the entire unknown operation*. A bath that learns the flag path can turn an otherwise rejected odd fault into an accepted wrong report. Prior proof: `astra_quantum_coherent_symmetry_filter_20261026/COHERENT_SYMMETRY_FILTER_AND_STAGED_CLIFFORD_RECEIVER.md` (read in full).

**Construction:** replace the one physical check flag by a two-physical-qubit *dual-rail encoded flag*, `|0_F>=|01>`, `|1_F>=|10>`. Prepare `|+_F>`, use the first physical flag spin as the control of the same before/after `T` gates, and measure `|+_F>` at the end. Every operation is within the two-spin single-excitation code. Arbitrarily strong and noncommuting *collective flag dephasing* of the form `(Z_f+Z_g) tensor B_M(t)` is now **exactly invisible to the coherent filter**, even while the underlying call and the finite physical check pulses proceed. It does not require a bath state, reset, mixing time, total bath Hamiltonian bound or a model of other dynamics.

The price is one added physical flag qubit plus encoded preparation and readout, **not** an additional six data-controlled Pauli gates. A conventional controller equipped with the same gates and information can implement the identical construction. The dual-rail DFS and coherent Pauli checks are established prior art; the contribution within Astra is their complete-bath combination at this specific completed quantum-task boundary and its task-relative perturbation/error budget.

## 2. Exact full-memory theorem

Let `S=pqa` be the physical receiver system, `M` include *all* retained quantum bath degrees of freedom, earlier records and untouched references. Set `T=X_p X_q Z_a`, acting trivially on M, so `T=T†`, `T²=I`. Let `K_l:S M -> S M'` be **each** Kraus operator of the whole uncontrolled completed physical call; no factorization or Markov assumption. The flag `F=fg` is freshly prepared and independent of this boundary in

`|+_F>=(|01>+|10>)/sqrt(2)`.

Define the code projector `P_F=|01><01|+|10><10|`, and the physical controlled gate

`C_T=|0><0|_f tensor I_SM + |1><1|_f tensor T_SM`.

The spectator flag qubit `g` is unaffected by this gate, while the flag code remains invariant. After the second `C_T`, perform an encoded plus measurement on the flag. The accepted (unnormalized) Kraus operator on *the entire system and bath* is

```
<+_F| C_T (I_F tensor K_l) C_T |+_F>
       = (K_l + T K_l T)/2 .                       (1)
```

Equality (1) holds Kraus by Kraus, including bath outputs. The orthogonal encoded outcome gives `(K_l - T K_l T)/2`. If the final measurement explicitly reads both flag spins, off-code outcomes are treated as **erasures**, not accepted check syndromes. Summed outcome branches remain trace preserving for an ideal flag-preserving operation. The source's physical pointer-code projector and initial-code conditions remain exactly those in the preceding staged receiver; changing the flag encoding does not cure an incorrectly prepared pointer.

Since the physical controller uses the same `C_T` on both sides, equation (1) implies all downstream source Bell tests, completed-teleportation Pauli paths and bath updates are **identical to the existing ideal single-flag service**, including arbitrary input–bath–reference entanglement. This is an equality of complete CP instruments, not merely output probabilities. All previously declared *role secrecy, measured-record retirement, terminal routing and trusted Bell-resource premises* are still required.

### Arbitrarily large collective flag–bath dynamics

On the flag code,

```
P_F (Z_f+Z_g) = 0 = (Z_f+Z_g) P_F .               (2)
```

Let the real continuous-time Hamiltonian be

`H(t)=H_0(t)+(Z_f+Z_g) tensor B(t)`,

where `H_0(t)` preserves `P_F` and implements the specified intended target/flag controls, potentially with an arbitrarily large noncommuting bath Hamiltonian. Restricted to the flag code, the second term in H is exactly zero. Uniqueness of time-dependent Schrödinger evolution therefore gives

`U_H(t) P_F = U_H0(t) P_F` **as complete system–bath operators**, with no commutativity or norm restriction on B. In particular, this remains true while the actual controlled gates run for finite time, provided their **entire generators preserve the flag code**. The uncontrolled target–bath interaction *during those finite gates* still needs its own genuine physical model or port-error allowance; DFS cancellation is not a claim that gate operations commute with arbitrary target–bath Hamiltonians.

### Explicit native-style preparation and readout

Define encoded `X_F=(X_f X_g+Y_f Y_g)/2`, `Z_F=(Z_f-Z_g)/2`. Both preserve `P_F` and commute with collective `Z_f+Z_g`. Starting from the independently prepared state `|01>`, apply

```
U_prep = exp[-i(pi/4) Z_F] exp[-i(pi/4) X_F] .
```

The resulting state is `e^{-i pi/4}|+_F>` (irrelevant common phase). After the sandwich, apply `U_prep†` and destructively read both physical flag occupations. `01` denotes the accepted plus syndrome, `10` the minus syndrome and `00/11` off-code erasures. This adds an exchange quarter-pulse and a differential-Z quarter-pulse for preparation, their inverses for readout, plus a second flag spin. All remain protected against collective Z dephasing under the stated control law. This does **not** imply they are protected against differential control error or number-changing leakage.

## 3. Stronger task-relative perturbation bound

A naive complete Stinespring-amplitude error bound is linear in *all* flag faults. But the completed task **projects the flag back onto its code**. Pure flag-code leakage cannot contribute at first order to an accepted syndrome.

Let `P=P_F tensor I_SM`, `Q=I-P`. Consider a time-dependent Hamiltonian with reference `H_0(t)` block-diagonal in P/Q. On P, `H_0` contains the intended encoded controls and *arbitrary shared bath dynamics*. On Q, `H_0` may contain an arbitrarily large Hamiltonian. Write the actual additional Hamiltonian as

```
H-H_0 = D(t) + V(t),
D=P D P,                 P V P=Q V Q=0,
V=P V Q+Q V P.
```

Define the integrated **in-code** and **code-leaking** magnitudes

```
d = integral ||D(t)|| dt,
l = integral ||Q H(t) P|| dt = integral ||Q V(t)P|| dt.
```

Take the complete physical unitary propagators U (real) and U0 (reference), including every bath mode, and project at the end. The second-order Duhamel identity gives

```
||P U(T) P - P U0(T) P|| <= d + l²/2.             (3)
||Q U(T) P|| <= l.                               (4)
```

**Proof:** First compare with U_D generated by `H_0+D`, which preserves P. The in-code difference to U0 is at most d by ordinary unitary Duhamel. Then compare U to U_D. Since V is purely offblock, the leading Dyson contribution to `P(U-U_D)P` vanishes. More explicitly, `||Q U(t) P||<=integral_0^t ||Q V(s)P||ds`; insert this into `P(U-U_D)P = -i integral_0^T P U_D(T,t)V(t)Q U(t)P dt` to obtain `l²/2`. Neither argument uses the norm of `Q H_0 Q` or requires bath commutativity. These are operator-norm estimates valid for arbitrary input correlations and bath dimension whenever the Hamiltonian and integrated coupling norms are well-defined.

Controlled T stages and encoded preparation/readout preserve the flag code in the reference; applying their ideal unitaries on either side cannot enlarge (3). Therefore the **accepted coherent-check Kraus** has full-memory amplitude deviation at most

`xi=d+l²/2` from the ideal fully symmetry-filtered accepted operation.

If the finished service includes the specified completed teleportation/Bell-sector retirement and the original ideal accepted check has no forbidden logical Pauli components, then the norm/Parseval argument on the *complete Stinespring map* gives a positive **unnormalized** fault effect

```
W_forbidden <= xi² I_M = (d+l²/2)² I_M.           (5)
```

If d=0, this is quartic in integrated flag leakage (`l^4/4`). The detectable off-code erasure allowance is still second-order (`l²`). If d is nonzero, the advantage can be lost: in-code differential noise creates first-order accepted amplitudes. Equation (5) does **not** imply a conditional-on-acceptance error of xi² without a separate lower bound on acceptance probability. Multiple Kraus branches must be included in a **single full-Stinespring operator error budget**; independently bounding each Kraus and summing without a joint budget is unsound.

## 4. Decisive failure mechanisms

**Differential (noncollective) dephasing.** `(Z_f-Z_g)/2 tensor B` acts as a logical Z_F *inside* the flag code. An adversarial odd physical service `U_bad=X_a` anticommutes with T, so an ideal coherent flag rejects it exactly. Under a differential phase `theta Z_F tensor Z_M`, the accepted fault effect is *exactly* `sin²(theta) I`. For `theta=pi/2` the device accepts the symmetry-violating operation with probability 1, despite every flag remaining in the code. DFS is not universal quantum error correction.

**Single physical flag spin echo is not a uniform substitute.** With two time windows and a fixed, noncommuting bath `H_M=Omega X_M`, coupling `g Z_f Z_M`, the two flag histories have bath unitaries

`V_+=exp[-it(Omega X-gZ)] exp[-it(Omega X+gZ)]` and `V_-` in reverse order. The symmetry-odd accepted amplitude is `(V_+-V_-)/2`. With `g=0.8`, `t=0.6`, `Omega=1`, this gives worst-case false accepted probability 0.2220, even though the same echo cancels perfectly when `Omega=0`. The encoded flag cancels collective Z noise exactly, independent of Omega.

**No all-axis protection with only two flag spins.** The commutant of collective su(2) noise on two spins has dimension 2 (singlet and triplet projectors), with no M2 protected logical factor. Three spins have a multiplicity-two spin-1/2 sector and commutant dimension 5, potentially protecting one subsystem logical qubit against fully collective X/Y/Z noise. But ordinary controlled-T gates driven by one **physical** flag spin are not in that three-spin commutant, so the present cheap Clifford compilation does not automatically transfer. This is established noiseless-subsystem representation theory, not a new bound on universal quantum computation.

**No empirical extrapolation.** A finite visibility measurement on the particular bath states encountered during calibration cannot certify an operator-uniform differential coupling bound for every later bath state. The autonomous hidden-clock failure in the governing work still applies. A real device needs a physically justified symmetry/noise algebra, a measured/calibrated complete-boundary control allowance with its scope, or a finite operational horizon with explicit statistical assumptions.

## 5. Executed numerical checks and matched comparator

The five programs and their JSON outputs are preserved locally. Main checks:

| Complete-boundary validation | Result |
|---|---:|
| 14 randomly generated entire target/bath operators vs encoded sandwich | maximum `2.81e-16` residual |
| Noncommuting time-dependent bath; collective noise strength 250 | `8.96e-15` residual |
| Finite-time controlled pulses; collective noise strength 70 | `1.87e-15` residual on the encoded input subspace |
| Encoded flag preparation/readout with bath transverse strength 1.7 and collective coupling 300 | `4.49e-15` residual |
| Pure flag leakage h=0.08 over T=0.8, symmetry-odd service | actual bad effect `1.044e-6`, upper `4.194e-6` |
| Pure flag leakage h=0.16 over T=0.8 | actual bad effect `1.666e-5`, upper `6.711e-5` |
| Mixed in-code differential + leakage bound, arbitrary Q energies up to 140 | all 16 instances satisfy `error<=d+l²/2` |
| Single physical flag, noncommuting bath echo worst-case false acceptance | `0.2220` at selected fixed parameters |

All are simulated Hamiltonian and Kraus models, not hardware measurements. Strong B noise was varied independently of bath Hamiltonians. One coherent target/bath channel served as its own fully informed reference. The observer need not represent the bath; the simulator does to *audit mathematical claims*.

**Strong conventional controller:** A conventional coherent-check controller already having a protected encoded flag, the same controlled-Pauli ports, encoded exchange/phase preparation and full physical noise assumptions can run exactly this construction. There is no algorithmic advantage relative to that equally informed controller. The gain is identifying a control interface whose **unbounded collective dephasing drops out of the certification problem**. If the hardware's dominant noise is instead differential or transverse with high strength, this architecture may be worse than a single actively echoed flag.

**Physical cost:** one added flag spin; **six** data-controlled two-qubit CNOT/CZ operations around U, unchanged from the prior staged checker; the prior output P code-parity measurement still costs **two** additional entangling gates; one exchange and one differential-Z preparation pulse (plus their inverses on readout); both flag spins measured. Preparation/measurement durations, calibration, routing, extra idle noise and hardware-level correlated controls are not free.

## 6. Further constructive attack: all-axis noise and a two-body-control no-go

The two-spin encoded checker is the most hardware-economical result for dominant **collective dephasing**. I then independently attacked the more ambitious task of surviving *unbounded collective X, Y and Z noise*. Representation theory gives a precise answer, including a severe implementation tradeoff.

### Three flag spins: a protected logical multiplicity and a gauge bath

For three spin-1/2 flag particles, the representation of collective SU(2) is

```
(C²)^tensor3 = H_(3/2)  direct_sum  (C²_logical tensor C²_gauge).
```

The spin-1/2 sector occurs with multiplicity **two**. Write its encoding isometry `V: C²_L tensor C²_G -> (C²)^tensor3` so that for each collective generator `J_alpha= sigma_alpha^(f1)+sigma_alpha^(f2)+sigma_alpha^(f3)`,

```
V† J_alpha V = I_L tensor sigma_alpha^G .
```

The logical two-path check remains invisible to any arbitrary collective noise Hamiltonian `sum_alpha J_alpha tensor B_alpha(t)`, including arbitrary noncommuting, time-dependent bath operators: all such noise acts on the expendable **gauge** and bath, not on the logical check path. The bath may be correlated with the gauge subsystem and target quantum input. This is the established noiseless-subsystem mechanism.

A concrete **symmetry-preserving logical controlled-T operator** is available algebraically. Let `S_12=SWAP(f1,f2)` and `Q_s=(I-S_12)/2` project onto a singlet of flag spins 1 and 2. Within the spin-1/2 code, `Q_s` selects one logical branch. Then

```
C_T^(3) = Q_s tensor I_target + (I-Q_s) tensor T_target,
```

commutes with all `J_alpha`. The coherent sandwich using this controlled operator yields exactly `(K+T K T)/2` after accepting logical flag `+`, now treating the **gauge plus physical bath** as the unrepresented memory. The full 128-dimensional reference calculation verified both gauge-output matrix blocks for noncommuting bath couplings up to strength 150; the largest full-boundary residual was `2.565e-14`. All inputs into this comparison share the proper logical code and isolated initial logical `+`; there is no assertion that physical SU(2) noise automatically prepares it.

### Why this does not replace the cheaper two-spin design

The price is an encoded **singlet-controlled target gate**, not just a third flag spin. The existing single-physical-spin-controlled CNOT/CZ operations fail to commute with the collective `J_alpha` and therefore no longer support an unbounded-noise guarantee.

A short restricted-control no-go makes this precise. Consider any two-body *cross coupling* in the span of `sigma_alpha^(f_i) tensor sigma_beta^(target)` for all three flag spins `i` and Pauli indices `alpha,beta`. This is a 27-dimensional physical-Hamiltonian space. Requiring ` [H_cross,J_x]=[H_cross,J_y]=[H_cross,J_z]=0` forces `H_cross=0`: the adjoint action of collective SU(2) on the flag-side one-body operators is a direct sum of vector irreducible representations, none containing a scalar. An independent linear-algebra audit found rank **27 out of 27** for these commutator constraints. Flag-only Heisenberg exchange *does* commute with collective SU(2), but cannot couple the protected logical flag to the target alone.

Thus an **instantaneously SU(2)-protected** entangling logical control requires at least a more complex flag-pair/target interaction, or an architecture that permits small finite control errors and charges them. This is not a no-go against all hardware implementations or stroboscopic bounded-noise protocols. The physical gate was constructed as a mathematical operator, **not synthesized from Astra's existing native CNOT/CZ ports**. A credible programme should prefer the two-spin implementation until that additional control capability is acquired.

### Source and originality boundary

Noiseless-subsystem multiplicities and the representation-algebra necessity of commuting protected gates are standard quantum-error-avoidance theory. Relevant experimental work includes *Dynamically generated decoherence-free subspaces and subsystems on superconducting qubits* (2024), https://pubmed.ncbi.nlm.nih.gov/39059436/, and *Universal quantum computation in decoherence-free subspaces with hot trapped ions* (2007), https://doi.org/10.1103/PhysRevA.75.052337. The new Astra work here is an explicit task-specific comparison and full-memory numerical validation, not invention of SU(2) noiseless subsystems.

## 7. Further worthwhile scientific attacks

1. **Acquire, rather than merely postulate, collective flag dephasing** in a physical device, quantifying common/differential correlations throughout the entire CNOT/CZ pulse windows, including both flag spins and all future-accessible memory.
2. Engineer encoded controlled-Pauli gates that suppress strong *collective transverse noise* without violating their own protection algebra. The three-spin multiplicity-two DFS is a mathematically legitimate route but demands a different control compiler.
3. Benchmark finite-run *accepted usable throughput* with actual native gate error/measurement times; an arbitrarily rejecting coherent checker can be perfectly sound but useless.
4. If operator-level differential bounds cannot be established, retain the simpler conservative frame-free error theorem or full Bell tests. Do not infer exact positive fault paths from high visibility in a finite calibration sample.

## Sources

Primary local sources were read, especially `COHERENT_SYMMETRY_FILTER_AND_STAGED_CLIFFORD_RECEIVER.md`, `LIBRARY_RENDERED_ACQUIRED_TASK_INTEGRITY_WITH_QUANTUM_MEMORY(1).txt` and `LIBRARY_RENDERED_COMPOSED_POSITIVE_SERVICE_FAULTS(1).txt`.

- Gonzales et al., *Quantum error mitigation by Pauli check sandwiching*, Scientific Reports **13**, 2122 (2023), https://www.nature.com/articles/s41598-023-28109-x. Strong prior art for coherent symmetry sandwiching, and sensitivity to checks becoming noisy.
- Altepeter et al., *Experimental Investigation of a Two-Qubit Decoherence-Free Subspace*, Physical Review Letters **92**, 147901 (2004), https://doi.org/10.1103/PhysRevLett.92.147901. Two-spin collective-dephasing DFS and its limits.
- *Dynamically generated decoherence-free subspaces and subsystems on superconducting qubits*, Reports on Progress in Physics (2024), https://pubmed.ncbi.nlm.nih.gov/39059436/. Current experimental context and existing encoded controls.
- van den Berg et al., *Single-shot error mitigation by coherent Pauli checks*, Physical Review Research (2023), https://research.ibm.com/publications/single-shot-error-mitigation-by-coherent-pauli-checks. Hardware/coherent-check prior art.

## Reproducibility

Run `bash RUN_VALIDATIONS.sh` in this directory; requires NumPy/SciPy and Python 3. Results are written to the matching `*_results.json` files, and the full execution log is saved. This archive has **not** been pushed to GitHub; no laboratory apparatus or external workflow was operated.
