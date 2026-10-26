# ASTRA — Exact fault paths for active Clifford operations with quantum memory

**26 October 2026 | Interim Extra High 1, Pro1 quantum operations.** Original derivations and executed finite-dimensional reference computations. No device operated, no hardware noise calibrated and no priority claim for established quantum teleportation, Pauli twirling or optimal stabilizer-state verification.

## Scientific decision

The immediately preceding `PRIVATE_SEGMENT_TWIRL_AND_MEMORY_SAFE_FLAG.md` proved exact positive Pauli fault paths for *idle* encoded-flag intervals, but supplied only a complete-channel-distance bound for *active* coupled logical gates. Its Kraus-support counterexample really defeats a positive *ideal-gate* branch under the **four paired frames commuting with the continuously implemented `ZZ` Hamiltonian**. It does not rule out changing the physical protocol.

The strongest new construction changes the operational boundary: build a two-qubit **Clifford** gate resource before loading an unknown input, then choose privately between destructive verification and completed gate teleportation. This gives a positive ideal-CZ branch even if the source gate has coherent control errors and an arbitrarily correlated, unrepresented quantum memory. An alternative with the same complete channel is to use all sixteen gate-matched physical Pauli input/output frames. The resource version moves the most demanding randomization to late, classical teleportation outcomes and avoids exposing a private key during the untrusted gate call.

A specifically improved test consists of six destructive local Pauli-product measurement settings. Its worst-case fault contrast is `2/3` (rather than `8/15` for one uniformly chosen nontrivial stabilizer), proved optimal *among a single round of local Pauli-projective measurements* by an exact integer six-setting primal witness and an exact three-error dual witness. The general stabilizer-state optimum `2/3` is **already established prior science** (Dangniam--Han--Zhu, 2020). Here the useful programme-level result is the **complete-memory CP-instrument inequality and its active, adaptive service implementation**, not discovery of that bound.

A stronger proposed use, nondemolition verification of each resource followed by successful use of that same resource, meets a decisive remote LOCC obstruction. This is not interchangeable with the affordable, destructive statistical test.

## 1. Complete physical boundary

Two logical qubits `D=D1D2`, the source outputs `B=B1B2`, and `M` comprising every memory register (including internal classical records physically accessible later). An arbitrary untouched reference `E` may be entangled with `D,M`. Let `G=CZ=diag(1,1,1,-1)`; this is a representative entangling Clifford, not a generic continuously parametrized `ZZ` rotation.

A completed physical call, *including* its noisy gate, has Kraus operators `K_lambda : D M -> B M'`. `M` need not be finite in the abstract theorem. For `P_s in {I,X,Y,Z}^{tensor 2}`, expand

```
(G^dagger tensor I) K_lambda = sum_s P_s tensor B_{s,lambda}
Phi_s(sigma)=sum_lambda B_{s,lambda} sigma B_{s,lambda}^dagger
W=sum_{s != II} Phi_s^*(I_M) ; 0 <= W <= I_M.
```

The whole instrument must use the same physical source operation for TEST and USE. **Two independent, fresh Bell pairs** are prepared between local protected halves `R1,R2` and the input halves of the source gate. Apply the untrusted physical call to the latter halves *before* selecting the private late role. `R`, the produced `B`, and any user message not yet consumed must be appropriately isolated during subsequent operations. No assumption of a classical bath sign, bath mixing rate, bath reset, or independent error draws is required.

### Theorem 1 — completed gate teleportation has exact positive paths

For USE, perform two genuine Bell measurements between the unknown input `D` and the protected `R`, apply the known output Pauli corrections computed from `CZ` and the Bell outcomes, and **physically retire the fine Bell records**. The complete resulting quantum channel, including memory and any untouched reference, is

```
T_use(rho_DM) = sum_s (G P_s tensor I) (id_D tensor Phi_s)(rho_DM)
                            (P_s G^dagger tensor I).
```

Each term is completely positive. The `s=II` branch is an *ideal CZ operation* on the data together with a memory CP filter `Phi_II`, and `W` is the trace effect of all other virtual branches. A branch label is a mathematical refinement and is not physically observed. Conditioning on that label can steer a user input initially entangled with the bath; no unconditional original-input marginal is promised on a postselected branch.

**Proof.** Write `|J(K_lambda)> = (I_R tensor K_lambda)|Phi_4>`, with `|Phi_4>=1/2 sum_j |j j>`. For every two-qubit Pauli Bell-measurement outcome `mu`, direct contraction through the *actual* Choi resource gives the corrected Kraus operator

```
T_{mu,lambda} = (1/4) (G P_mu^T G^dagger tensor I_M)
                     K_lambda (P_mu^* tensor I_M).
```

The full channel is the sum over the sixteen values of `mu`. Expanding `K_lambda` into Pauli components, the orthogonality of all sixteen Pauli conjugation characters deletes every cross term with distinct `s`. This equality holds on the full `DM` linear map and therefore on any extension by `E`. It is **not** a generic Choi-state teleportation simulation of the original arbitrary channel: it is the *Pauli-twirled* completed service. Fine `mu` may be available to the local correction controller transiently, but must not leak to a future-accessible bath/control record. Retaining it changes the flagged channel.

### Theorem 2 — direct keyed active gate is operationally equivalent

Alternatively sample a fresh, independent, private `P_mu` uniformly from the sixteen two-qubit Paulis. Apply it physically to the input before the untrusted gate and the matched output Pauli `G P_mu^dagger G^dagger` afterward, then retire the private key. The whole averaged channel is **identical** to Theorem 1, including the bath maps `Phi_s`. For Clifford `G`, the matched output correction remains a tensor-product Pauli. The physical device must not see advance key information via pulses, classical side channels or another quantum port; the calls must otherwise be key independent.

For a completely generic noisy two-qubit gate, Pauli subgroup randomization with fewer than sixteen keys cannot cancel *every* identity-versus-error coherence. Let `H_{s,k}=(-1)^{[s,k]}` be the 16x16 symplectic character table. The constraints `sum_k H_{s,k} p_k=0` for all fifteen `s!=II` plus normalization have the unique solution `p_k=1/16`. This is a **Pauli-frame-group uniqueness statement**, not a universal four-bit lower bound over arbitrary verification architectures or structure-restricted errors. A two-bit twirl on the first data qubit leaves an `IZ` logical coherent fault untouched; the executed corrected-channel superoperator discrepancy was `2.40948` (Frobenius norm) in a controlled example.

### A fault-effect bound without bath-bandwidth information

Suppose the desired complete reference call is `G tensor U_M`, where `U_M` is arbitrary, and the *actual complete joint unitary* differs because of a Hamiltonian perturbation of uniform norm at most `v` during a window of length `tau`. Duhamel gives `||U_actual-G tensor U_M|| <= v tau`. Projecting the process-vector onto all nonidentity logical Pauli components gives

```
W <= (v tau)^2 I_M.
```

No `||H_M||`, mixing or bath-bandwidth constraint enters. This is a supplied physical **norm premise**; good-looking test records alone cannot establish it. A destructive Bell-resource test can instead statistically acquire aggregate fault effects over a finite run. In five independent reference calculations with `v tau=.192`, the largest current-memory fault effect ranged from `.00452` to `.01312`, below the `.036864` ceiling.

## 2. Destructive tests matching the actual task fault

The ideal four-qubit resource is `|J_G>=(I_R tensor CZ_B)|Phi_4>`. Its stabilizers are

```
S_Q = Q_R^T tensor (CZ Q_B CZ),  Q in {I,X,Y,Z}^{tensor 2}.
```

Their common +1 eigenspace is exactly `|J_G>`. The four-qubit states `|J_{GP_s}>` have mutually orthogonal stabilizer syndromes. On TEST, make *only local* Pauli measurements on `R1,R2,B1,B2`, discard these candidate qubits, retain only the selected setting and a coarse pass/fail bit, and retire the individual physical readout outcomes. The resulting test-bath CP map is diagonal in the virtual Pauli sectors; it may therefore be composed with the USE-positive paths without assuming a classical bath.

**Simple control.** Choose one of the fifteen nontrivial stabilizers uniformly and check its sign. Exactly eight stabilizers anticommute with each nonidentity `P_s`, so

```
F_fail^(simple) = (8/15) sum_{s!=II} Phi_s,
E_fail^(simple) = (8/15) W.
```

**Stronger six-setting local product test.** Choose uniformly from the following measured local bases, in `R1 R2 B1 B2` order:

```
XYYX, XZXZ, YXXY, YZYZ, ZXZX, ZYZY.
```

In each setting, infer **every** stabilizer whose single-qubit factors agree with the measured axes (allowing `I`), using its known ideal sign. Mark FAIL if any inferred stabilizer has the wrong sign. The exact relative detection counts among these six settings are

```
P_s = XX or YY: 6/6.
Every other nonidentity P_s: 4/6.
```

Consequently, on the **full retained bath instrument**,

```
F_fail^(6) = (2/3) sum_{s != II} Phi_s
                    + (1/3)(Phi_XX + Phi_YY).
```

This is a completely-positive **lower bound**, not exact equality to `(2/3) * sum_bad`: the positive excess matters. Thus `E_fail^(6) >= (2/3) W` for every possible bath state, including earlier virtual-fault-conditioned states.

**Exact optimality within the specified physical measurement class.** Enumerating the 81 choices of single-qubit `X/Y/Z` readouts in a one-round product-basis measurement, **no** choice detects all three equally-weighted Pauli error sectors `IZ, ZI, ZZ`; each detects at most two. Therefore every randomized mixture of such choices has worst-case detection contrast at most `2/3`. The six-setting schedule gives at least four detections for each of the fifteen errors, and achieves `2/3`. An independent integer-only symplectic enumeration establishes this primal/dual certificate, without floating-point linear programming. More general separable-measurement `2/3` verification results are established by Dangniam, Han and Zhu (2020); this calculation is a specific hardware menu and full-memory implementation, **not new priority**.

An independent Choi-resource Kraus simulation of the *actual physical local-test projectors* matched the bath CP map above with Frobenius residual at most `1.19e-16` across five noncommuting-bath examples. A second independently coded ideal-resource-projector test extracted exactly the clean bath subinstrument.

## 3. Finite noisy measurements and an adaptive all-prefix fault budget

Actual destructive local weak and projective measurement implementations need separately justified full physical instruments. As one model-controlled case, assume independent `2.5%` classical report flips on every measured qubit and otherwise ideal destructive local projective reads. The calibrated aggregate failure-effect identity becomes

```
F_fail >= f I + nu W
```

where `f` is the correct-resource false-positive baseline and `nu` the minimum extra failure contrast of a nonidentity Pauli branch:

| Calibrated finite-readout test | `f` | `nu` |
|---|---:|---:|
| One uniformly random stabilizer | 0.07544896 | 0.44583500 |
| Six local-basis settings | 0.09470729 | 0.55729375 |

These are exact consequences *within the declared independent report-flip model*, not laboratory calibrations. The second protocol has a larger false-positive rate and a stronger true-fault contrast.

At candidate `i`, prepare the entire resource before a late private TEST/USE choice with predictable TEST probability `p_i`. Let `B_n` count positive virtual nonidentity Pauli branches on *completed USE* services, and `A_i` the received TEST failure indicator. For any `z>1`, choose

```
a_i = 1 - (1-p_i)(z-1)/(p_i nu),    0<a_i<1,
c_i = 1 - p_i f (1-a_i)>0.
```

At the current full physical memory boundary, the weighted TEST/USE effect is

```
(1-p_i)[I+(z-1)W_i] + p_i[I-(1-a_i)F_i] <= c_i I.
```

Therefore `z^{B_n} prod_{i TEST} a_i^{A_i}/prod_i c_i` is a nonnegative supermartingale through arbitrary retained quantum memory and past adaptive choices, provided the complete TEST/USE physical boundary is matched. Ville's inequality gives one simultaneous all-prefix event at confidence `1-delta` with

```
B_n <= U_n = [ln(1/delta)+sum_i ln(c_i)-sum_{i TEST} A_i ln(a_i)]/ln(z).
```

Retain historical numerical certificates without storing the bath, `V_n=min(U_n,V_(n-1)+Delta R_n)` with `V_0=0`, where `R_n` is the count of completed uses. Before authorizing another candidate, require `V_n+1<=B_max`. This is a finite virtual fault-budget admission rule, not certification of a particular next output, indefinite lifetime, or a direct guarantee for arbitrary downstream algorithms.

### Executed reference controllers

Both source settings are *physical* two-qubit CZ reference Hamiltonians with unreset, noncommuting two-level quantum memory and bounded coherent perturbations. Settings and test probability `.40/.55` respond only to received test records; the validation simulator additionally samples the hidden positive Pauli label, never supplied to the observer. `z=1.24`, `delta=.01`, `B_max=30`, 1,200-candidate cap. Each comparison has **128 independently seeded model trajectories**, with differing outcomes and bath histories between methods:

| Ideal-test method | Mean completed gate uses | Mean hidden virtual faults | Mean received fault upper | Bound violations |
|---|---:|---:|---:|---:|
| One random stabilizer (`8/15`) | 524.97 | 3.80 | 27.88 | 0 / 128 |
| Six-settings (`2/3`) | 630.23 | 4.45 | 27.45 | 0 / 128 |

With independently flipped local report bits at 2.5% per qubit (64 trajectories per method, same other model settings):

| Finite-readout method | Mean completed gate uses | Mean hidden virtual faults | Mean received fault upper | Bound violations |
|---|---:|---:|---:|---:|
| One random stabilizer | 61.55 | 0.27 | 29.60 | 0 / 64 |
| Six-settings | 99.78 | 0.39 | 29.46 | 0 / 64 |

The large throughput loss under this deliberately conservative fault budget is a **substantive failed economical regime**. The simulated zero violations do not prove confidence coverage; the operator supermartingale supplies that theorem. These trials are reference simulations, not hardware tests, and not identical-bath-history paired trials. A conventional controller with the identical physical ports and observations achieves the same benefits.

## 4. Stronger single-resource heralding and the remote no-go

If an actual trusted **nondemolition projective measurement** of all four commuting Choi stabilizer generators is available, its accepted outcome is exactly

```
Pi_G = |J_G><J_G|,
Phi_accept(sigma)=Phi_II(sigma).
```

After postselection, the resource is exactly `|J_G>` times a bath state; using it through trusted completed teleportation implements an ideal `CZ` on a user input that is independent of the bath (and implements `CZ` on the appropriately filtered input when initially correlated). This is a potentially useful heralded perfect-gate operation, with acceptance effect `I-W`. Under the *separately justified* Hamiltonian norm bound in Section 1, acceptance is at least `1-(v tau)^2` at every current bath state. No independent-bath assumption is used. However, this is a **much stronger hardware primitive** than the destructive local verifier and cannot be acquired from its classical test statistics.

**Decisive LOCC obstruction.** `|J_G>` is maximally entangled across remote `R|B` with Schmidt rank four. A full local Pauli projective measurement of all four qubits produces a mixture of product states. Its overlap fidelity with the original `|J_G>` is at most `1/4` (indeed, the six basis settings yield `1/8` or `1/4`). The candidate is spent.

More generally, suppose an accepted LOCC/separable CP map has product Kraus operators `A_j tensor B_j` and perfectly preserves this pure maximally entangled target upon acceptance. Each nonzero accepted branch satisfies `B_j A_j^T = c_j I` in locally conjugated target coordinates. For every competing maximally entangled `|Phi_U>=(I tensor U)|Phi_4>`, AM--GM on the singular values yields

```
||B_j U A_j^T||_F^2 /4 >= |c_j|^2.
```

Summing accepted branches shows **every other maximally entangled resource is accepted at least as often as the intended target**. Hence no such target-preserving separable acceptance can preferentially verify `|J_G>` against arbitrary erroneous maximally entangled Pauli-Choi resources. Nondemolition perfect-resource heralding across a remote cut requires an extra nonlocal interaction/entangled resource or strictly weaker hypotheses. An executable four-dimensional product-filter control confirms the inequality on all fifteen nontrivial Pauli Choi states. This is established quantum information/information--disturbance structure applied to the present four-qubit service, not a priority claim.

## 5. Additional decisive boundary: retaining fine teleportation outcomes

Theorem 1 is an equality only after the terminal Bell-measurement and correction outcomes are physically retired from the future interaction boundary. The individual fine-`mu` branches of gate teleportation generally contain coherent cross terms that are absent from the coarse positive Pauli-refined map. In four full-memory reference gates, the **coarse** completed-channel residual was below `8.5e-16`, while the discrepancy between the retained-outcome flagged map and a fictional *independent* Pauli-fault label reached `0.45` in superoperator Frobenius norm. A copy of `mu` in the future bath is not retired merely because the software discards its local variable.

Other limitations: trusted Bell-pair preparation and isolation, terminal Bell analyzers, Pauli corrections, source/test role privacy and their complete instruments must be independently established. The saved differential-parity and protected-meter constructions supply conditional ways to approximate some operations, not proof that this complete two-gate resource apparatus exists. Errors after the last audited boundary require additional allowances. A finite calibration cannot exclude a hidden autonomous clock that changes the hardware later. Generic non-Clifford gate teleportation does not retain Pauli-only Clifford corrections.

## 6. Scientific comparison and continuation judgement

- **Direct active-gate frames:** no extra 4-qubit resource, but four fresh secret bits per generic two-qubit gate, physically trusted pre/post local Paulis, and frame-key isolation during a potentially untrusted gate. Exact positive paths; the active gate is actually modified to one with different frame controls.
- **Deferred gate resource:** two Bell pairs, an untrusted gate applied *before* the role coin, two terminal Bell analyzers plus corrections on USE, and destructive local source tests. Exact same positive paths; avoids a private key during the untrusted gate call and can protect the unknown input until resource verification. Costs qubits, memory, physical routing, and terminal port reliability.
- **Nondemolition perfect Choi-resource filtering:** would give a heralded exact gate, but cannot be implemented as the same cheap local measurement on a remote split resource. Its verification hardware may be as difficult as the desired entangling gate.
- **A strong conventional quantum controller** with the same real operations, local measurements, secrecy and calibration assumptions implements all three. Astra has no exclusive hardware or verified advantage. The novel-looking 2/3 optimization is substantial published prior work in stabilizer-state verification; the result here is a task-specific full-bath instrument and finite-run application.

**Most consequential unresolved scientific/physical problem:** produce and calibrate a *complete* Bell-measurement, correction and resource-isolation boundary in the declared native hardware, and bound its effect on the future-accessible bath. Continued optimization of tests can help statistical cost, but not replace that interface. For remote services, resolve the nonlocal nondemolition-verification cost before claiming per-resource perfect-gate heralding.

## 7. Reproducibility and sources

Run `bash RUN_VALIDATIONS.sh` from this directory. Ten executable scripts emit their own JSON results; `validation.log` and `SHA256SUMS.txt` preserve actual execution and hashes. `clifford_gate_fault_instrument.py` and `physical_stabilizer_and_minimal_keys.py` independently check gate teleportation, direct twirl, Choi test and clean projector. `local_basis_integer_certificate.py` is an integer-exact primal/dual test. `optimized_product_test_instrument.py` verifies the actual six-setting local instrument, not only its eigenvalues. The 128-trajectory and 64-trajectory simulations contain only mathematical reference executions. No device operated and no push to GitHub occurred.

**Source premises:** `PRIVATE_SEGMENT_TWIRL_AND_MEMORY_SAFE_FLAG.md` (latest predecessor, physically available in this session); governing user-supplied `ACQUIRED_TASK_INTEGRITY_WITH_QUANTUM_MEMORY` and `COMPOSED_POSITIVE_SERVICE_FAULTS`; Astra N1004 source/packet at pinned git revision `56d4aebfb8a43cd1a31fdf0f4e14da765ed6f950` from the present conversation. These are conditional research premises, not measurements. Archived instructions were not treated as current research commands.

**Relevant prior work:**

- Dangniam, Han, Zhu, *Optimal verification of stabilizer states*, Physical Review Research 2, 043323 (2020), https://doi.org/10.1103/PhysRevResearch.2.043323. Existing `2/3` optimum and local-Pauli verification machinery.
- Wallman, Emerson, *Noise tailoring for scalable quantum computation via randomized compiling*, Physical Review A 94, 052325 (2016), https://doi.org/10.1103/PhysRevA.94.052325. Existing Clifford-matched twirling.
- Kattemölle, Gulácsi, Burkard, *Non-Markovianity induced by Pauli twirling*, npj Quantum Information 12, 138 (2026), https://doi.org/10.1038/s41534-026-01345-5. Do not infer hidden-bath Markovianity from Pauli-form outputs.
- Cope, Hetzel, Banchi, Pirandola, *Simulation of non-Pauli channels*, Physical Review A 96, 022323 (2017), https://doi.org/10.1103/PhysRevA.96.022323. Generic Choi-state teleportation does not directly simulate arbitrary non-Pauli channels.
- Zhang, Seshadri, Knill, sequential quantum spot-checking and estimation factors (2026), https://arxiv.org/html/2602.08114. Established non-iid sequential evidence theory used in the controller.
- Gate teleportation and stabilizer resource verification are general established quantum-computation mechanisms; this study asserts no novelty in their foundations.
