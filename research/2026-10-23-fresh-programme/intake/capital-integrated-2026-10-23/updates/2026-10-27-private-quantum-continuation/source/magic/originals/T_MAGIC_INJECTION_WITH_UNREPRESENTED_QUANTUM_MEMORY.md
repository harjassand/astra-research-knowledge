# Astra / Interim Extra High 1 — Non-Clifford magic injection with unrepresented quantum memory

**Research continuation, 27 October 2026 (Brisbane).** Original derivations and computational checks of a specified model, not hardware results or a claim of priority. This continues the user-supplied acquired-task-integrity / composed-positive-service constructions and the saved `ACTIVE_CLIFFORD_GATE_FAULT_PATHS_WITH_QUANTUM_MEMORY.md` and `DEFERRED_CLIFFORD_FRAMES_WITH_ARBITRARY_QUANTUM_MEMORY.md`. Inherited claims have been used only with their declared physical-port and record-retirement assumptions.

## Scientific change

The previous Astra construction had exact fault-path accounting for completed Clifford gates despite a never-reset, noncommuting bath; a Pauli ledger alone did not traverse non-Clifford gates. The current result supplies **completed T-state injection** as a complementary exact positive fault service, with a *single-qubit* two-setting local-Pauli sacrificial test, a **one-bit Clifford twirl to permit fine injection records to be retained**, and a concrete conditional source compiler using the already-discussed type of finite-strength weak Pauli instrument. Composing T with the earlier noisy CZ fault service gives a finite universal gate-set **fault-path representation**. It does NOT establish universal fault-tolerant computation, a magic factory, a hardware capability or priority over standard magic-state injection and verification.

The constructive comparison is an ordinary controller with the **same** CNOT, calibrated weak Pauli instrument, source replacement, Clifford corrections, private coins and measurement ports. Such a controller can implement every identity and confidence update below. There is no unique Astra architectural advantage.

## 1. Exact completed T injection, including all quantum memory

Let `D` be a logical qubit, `B` a magic candidate, `M` the entire continuing bath and `E` an untouched reference. The `D:B:M:E` input can be arbitrarily correlated. Let

\[
T=\operatorname{diag}(1,e^{i\pi/4}),\quad S=\operatorname{diag}(1,i),\quad
|A_0\rangle=(|0\rangle+e^{i\pi/4}|1\rangle)/\sqrt2,
\quad |A_1\rangle=Z|A_0\rangle,\quad
\Pi_s=|A_s\rangle\langle A_s|_B.
\]

The **physical** injection applies directed CNOT `D->B`, destructively reads `Z_B` with raw outcome `m`, applies `S_D` if `m=1`, then physically retires `m`. Define source-block operators

\[
\rho_s=(I_D\otimes\langle A_s|_B\otimes I_{ME})\,
\rho_{DBME}\,(I_D\otimes|A_s\rangle_B\otimes I_{ME}).
\]

For each measurement outcome `m`, the actual linear map restricted to source sector `s` is
\[
L_m(I_D\otimes|A_s\rangle_B)=
\frac{e^{i m\pi/4}(-1)^{ms}}{\sqrt2}\,Z^sT.
\]
Summing the **completed** measurement outcomes cancels the off-diagonal `s != t` interference exactly. The complete logical-output/bath/reference channel is
\[
\boxed{\mathcal I_T(\rho)=\sum_{s=0}^1
(Z^sT\otimes I_{ME})\rho_s(T^\dagger Z^s\otimes I_{ME}).}\tag{1}
\]
Thus there are exactly two CP sectors: `s=0` is the ideal T operation conditioned on the source sector, and `s=1` is an additional logical Z fault. The source fault effect is `Q=Pi_1` on `B` tensored with identity on every other register. This is a **virtual mathematical refinement**, not an acquired label of the bath. Source-sector conditioning can steer initially correlated logical inputs; the theorem does not claim the normalized good branch preserves an unconditional input marginal.

**Independent execution:** `magic_injection_full_memory.py` compares complete superoperators on every matrix unit of `D:B:M`, for `dim(M)=2`, including arbitrary `D:B:M` correlations. It obtains residual `1.4043e-15` and correlated-state residual at most `2.49e-16`.

## 2. Exact sacrificial magic-fault instrument from local Pauli tests

A TEST uses the identical already-prepared candidate, privately measures either `X_B` or `Y_B` with probability `1/2` and reports *failure* if the measured eigenvalue is `-1`. All measured degrees of freedom are discarded. Its exact failure effect is
\[
F=\tfrac12\frac{I-X}{2}+\tfrac12\frac{I-Y}{2}
=fI+\nu Q,
\qquad \nu=1/\sqrt2,\quad f=(1-1/\sqrt2)/2=0.1464466094\ldots .\tag{2}
\]
This is an equality of **bath-update CP instruments** after discarding the candidate:
\[
\mathcal F_{\rm fail}=f\Phi_0+(f+\nu)\Phi_1,
\qquad
\mathcal F_{\rm pass}=(1-f)\Phi_0+(1-f-\nu)\Phi_1,
\quad\Phi_s(\sigma)=\langle A_s|\sigma|A_s\rangle_B.
\]
Here `sigma` can contain arbitrary bath/reference operators; **the source dynamics is not assumed iid**. The nonzero honest-state false-rejection probability `f` is an inherent measurement cost of this Pauli-only single-copy implementation.

Within the class of testers that select one `X`, `Y` or `Z` projective measurement per candidate and classically randomize its binary report, equation (2) is **contrast-optimal** among testers whose operator effect is of the exact homogeneous form `fI+nu Q`. To prove it, write any test effect as `aI+b_x X+b_yY+b_zZ`; axis weights `w_j` imply `|b_j|<=w_j/2` and `a>=sum_j |b_j|`. For `F=fI+nu Q`, `b_x=b_y=-nu/(2sqrt(2))` and `b_z=0`, so `nu/sqrt(2)<=1/2`, i.e. `nu<=1/sqrt(2)` and `f>=nu(1/sqrt(2)-1/2)`. Equation (2) saturates both inequalities. This *restricted-class* proof is not a general POVM or collective-measurement optimality theorem.

**Independent execution:** `magic_injection_full_memory.py` validates the *complete bath instrument*, failure and pass maps, with residual `5.028e-16`.

## 3. One private Clifford bit removes the raw-record retirement requirement

The Clifford operator
\[
C=(X+Y)/\sqrt2=e^{-i\pi/4}SX=\Pi_0-\Pi_1
\]
has the target magic state as a `+1` eigenstate, the opposite magic sector as `-1`. After a candidate is prepared and **before** the private TEST/USE choice, apply `I_B` or `C_B` with one fresh, conditionally independent private bit, then physically retire **that** bit. This actual local operation realizes the quantum instrument pinch
\[
\mathcal D_C(\rho)=\tfrac12(\rho+C_B\rho C_B)
=\Pi_0\rho\Pi_0+\Pi_1\rho\Pi_1.
\tag{3}
\]
Because the source-sector coherence was physically eliminated **before** injection, the *raw injection outcome* `m` can now remain in a classical future-accessible register without invalidating the positive resource-fault refinement. In fact, the whole flagged channel is
\[
\boxed{\mathcal J_T(\rho)=\tfrac12\sum_{m=0}^1|m\rangle\langle m|\otimes
\sum_{s=0}^1(Z^sT)\rho_s(T^\dagger Z^s).}\tag{4}
\]
The coarse `m` is uniform and independent of the output and retained bath under these exact operations. Subsequent allowed operations may read `m` without restoring cross-sector source coherence, though any new physical fault model must still be accounted for. The **twirl key** cannot be exposed or reused and cannot remain as a future-accessible control record. The two-bit output `m` and one-bit private key play completely different roles.

`magic_axis_twirled_flag.py` verified the full flagged-channel residual `6.058e-16` and maximal `m`-conditioned state discrepancy `1.26e-16` on correlated inputs. Without twirling, retaining `m` creates an exact counterexample with trace distance `0.0994987` for a coherent source with `q=0.01`. If the bath learns and undoes the twirl, the same failure returns. `magic_frame_key_reuse_no_go.py` uses two coherently correlated candidate resources `(A_0 A_0+A_1 A_1)/sqrt(2)` and shows one *reused* key leaves a `0.5` joint flagged-channel discrepancy from independent local twirls. Retiring both injection outcomes erases that discrepancy; this pinpoints the scope.

The `SX` magic-axis twirl is conventional magic-state randomization; the substantive programme consequence is **where** a real retirement requirement can be relocated while preserving the **entire quantum-memory** instrument.

## 4. Classical misreporting during T injection

Suppose the quantum `Z_B` measurement is ideal, but only its already-classical report is independently flipped with probability `r`, causing the physically applied conditional `S` correction to be wrong. **After coarse retirement of the raw corrected outcome**, summing the two equally likely underlying measurement outcomes makes the wrong correction an equal mixture of logical `I` and `Z` relative to `T`.

For a magic candidate with bad projector `Q`, the aggregate *completed* logical `Z`-fault effect is therefore
\[
\boxed{W_{\rm use}=gI+hQ,
\quad g=r/2,\quad h=1-r.}\tag{5}
\]
For `r=0.025`, `W=0.0125 I+0.975 Q`, not `r I+Q` and not an arbitrary coherent error. The complete superoperator identity passed six values of `r` through `0.5`, with worst residual `1.59e-15`, in `classical_readout_nonclifford.py`.

**Strict distinction:** (5) assumes an independently calibrated classical flip *after* a trusted projective measurement, applied conditional Clifford feedback, and final coarse retirement. If a raw `m` flag remains accessible, a wrong correction can be `S` or `S^dagger` conditional on `m`, not individually Pauli. If the Bell/Z measurement itself suffers coherent or bath-dependent faults, (5) is not licensed. Those branches need a separately certified terminal instrument or conservative complete-boundary allowance.

Independent test-report flips of probability `r_t` give the actual *test* failure effect `F_t=f_t I+nu_t Q` with
\[
f_t=r_t+(1-2r_t)f,\qquad \nu_t=(1-2r_t)\nu.
\tag{6}
\]

## 5. A centered non-iid quantum-memory fault-count certificate

The physical candidate is prepared **before** a fresh private TEST/USE coin, chosen with predictable test probability `p_i`. Let `B_n` count the positive virtual logical-Z faults on uses, including the independent calibrated classical report-error branches in (5). Retain only test fail/pass, permitted source records, completed-use count and the declared physical instrument table. All hidden dynamics and all virtual labels remain outside the received observer.

For a fixed `z>1`, on round `i` define
\[
k_i=\frac{(1-p_i)(z-1)h_i}{p_i\nu_{t,i}},\quad
 d_i=\frac{(1-p_i)(z-1)g_i}{p_i},\quad
b_i=1-d_i+f_{t,i}k_i,\quad a_i=b_i-k_i,
\]
with `a_i,b_i>0`. Weight USE-good by `1`, USE-bad by `z`, TEST-fail by `a_i` and TEST-pass by `b_i`. The *whole current-boundary weighted effect* is **exactly identity**:
\[
(1-p_i)[I+(z-1)(g_i I+h_iQ)]
+p_i[a_i(f_{t,i}I+\nu_{t,i}Q)
+b_i((1-f_{t,i})I-\nu_{t,i}Q)]=I.\tag{7}
\]
Therefore
\[
M_n(z)=z^{B_n}\prod_{\mathrm{TEST,fail}}a_i
\prod_{\mathrm{TEST,pass}}b_i
\]
is a nonnegative martingale on the *positive refined process*, **even with a persistent coherent quantum bath and adaptive controls**. Ville's inequality plus a predeclared finite grid `ZGRID`, splitting confidence `delta/K`, gives all-prefix bounds
\[
B_n\le U_n=\min_{z\in ZGRID}\frac{\log(K/\delta)
-\sum_{i\le n:\,\mathrm{TEST}}\log[a_i^{F_i}b_i^{1-F_i}]}{\log z},
\]
with probability at least `1-delta`. The sharp historical one-scalar envelope from the governing programme is still valid:
\[
V_0=0,\quad V_n=\min\{U_n,V_{n-1}+\mathbf 1_{\mathrm{USE}}\}.
\]
Admission when `V+1<=Budget` keeps all admitted **virtual fault-count** prefixes below budget on the confidence event. This is not a per-output guarantee, a steady-state guarantee or a generic quantum fault-tolerance threshold. The centered pass/fail factor is a minor algebraic alternative to the predecessor's one-sided `a^fail/c^round` supermartingale, not an invention of sequential estimation factors.

**Executed reference operation (actual NumPy density matrices):** 36 trajectories, 1,100-round cap, two-level never-reset noncommuting bath; source duration and private test probability adapt only to received outcomes. Perfect ideal terminal labels, 99% nominal all-prefix confidence and risk budget 75: mean `762.53` rounds, `444.19` completed T uses, `12.17` hidden virtual faults, `72.23` retained upper bound, zero observed confidence violations. On a looser budget 175, the centered bound averaged `87.04` versus `93.29` for the predecessor's one-sided factor, evaluated on the *same* paths; mean hidden faults `16.86`. No frequency of 36 simulated trajectories proves a 99% theorem; equation (7) does that under the supplied operator identities.

With *independently characterized* 2.5% classical flips on both TEST readout and USE correction, and the same fault budget 75, 36 trajectories averaged `631.5` rounds, `369.36` T uses, `15.28` virtual Z faults and upper bound `74.51`; no simulated all-prefix failures. These two ensembles experience **different actual bath histories**, so their means are model-controlled comparisons, not paired counterfactual predictions. Scripts: `adaptive_magic_service.py`, `noisy_magic_online_service.py` and executed JSON outputs.

## 6. The missing magic resource and a conditional native weak-measurement compiler

A Clifford circuit supplied only with stabilizer ancillas cannot generate `|A_0>`; any source of genuine magic must provide a nonstabilizer operation or state. The earlier Astra physical premise **does include calibrated finite-strength local weak Pauli instruments**, although it has not independently established that the complete Lüders form below is supplied and stably tunable at the requisite strength.

Assume a full physical **Lüders** weak-X instrument with actual Kraus operators
\[
M_\pm^X=\sqrt{(I\pm\eta X)/2},\quad 0<\eta<1,
\]
and a hard preparation/physical reset to `|0>`. On that input, the `+/-` outcomes occur with probability exactly `1/2`, and the postmeasurement pure Bloch vectors are `(±eta,0,sqrt(1-eta^2))`. Conditional `Z` feedback makes them **the same pure state**, regardless of the obtained outcome. A Clifford quarter-turn `R_X(-pi/2)=exp(+i pi X/4)` maps it to Bloch
\[
(\eta,\sqrt{1-\eta^2},0).
\]
At
\[
\boxed{\eta=1/\sqrt2,}
\]
this is exactly `|A_0>`. If the reset and complete weak instrument act locally without bath disturbance, the whole source is a **deterministic CPTP replacement**
\[
\rho_{BM}\longmapsto |A_0\rangle\langle A_0|_B\otimes \operatorname{Tr}_B\rho_{BM},
\]
for **arbitrary initially correlated** `B:M` inputs. The random weak outcome can be forgotten or retained, since its normalized target and bath states are identical after prescribed feedback.

For a calibrated but nonideal strength, the exact wrong-magic weight after the `SX` twirl is
\[
q(\eta)=\frac12\left[1-\frac{\eta+\sqrt{1-\eta^2}}{\sqrt2}\right]
=\sin^2\left[\frac{\arcsin\eta-\pi/4}{2}\right].\tag{8}
\]
It is **quadratically sensitive** to small strength error near `1/sqrt2`. For an *illustrative model value* `eta=0.6`, `q=0.00502525`; for `eta=0.88416`, `q=0.02222767`. These values are not claims about the strength of the actual Astra apparatus.

`weak_magic_resource_compiler.py` proved the complete replacement channel numerically to `6.28e-16` at the exact strength. `closed_loop_weak_magic_T.py` independently composes actual weak measurement branches, hard reset, physical feedback, magic-axis twirl and T injection and reproduces the complete `T/ZT` source-fault channel on **all initial `D:B:M` operators**, residual at most `2.85e-15`. Thus the mathematical construction need not be supplied an externally perfect magic state if it is instead supplied this genuinely non-Clifford **weak instrument**.

**Decisive physical-observation failure:** replace each ideal weak Kraus `M_±` by `Z M_±`. The two instruments have **identical POVM effects and all one-step outcome likelihoods**, but their output after the prescribed feedback has target magic fidelity **1/2**, not 1, at `eta=1/sqrt2`. Probability-only calibration cannot acquire a state-production instrument. Fortunately, **aggregate safety** of the online source audit does not require trusting weak source preparation: it tests the actual candidate after source production. Only predictable throughput and an asserted physical preparation law need the full instrument premise. A uniform complete-boundary noise allowance can be supplied separately if a stronger individual-source claim is required.

## 7. Composition across a non-Clifford gate set with the same bath

The existing Astra resource-based `CZ` service has 16 positive Pauli branches. Equation (1), or its magic-twirled fine-record version (4), gives a positive ideal-`T` or `ZT` branch for each completed injection. Because these are **CP identities on the complete retained system–bath boundary**, they compose through arbitrary state correlations, bath memory and allowed intervening CPTP maps.

`mixed_nonclifford_memory_circuit.py` independently implemented two actual magic-source interactions / injections and an actual two-qubit Pauli-framed, coherently faulty CZ, retaining the *same* noncommuting two-level bath throughout. The concrete circuit was `T(D1) -> CZ(D1,D2) -> T(D2)`. It enumerated **256 physical Kraus branches** and independently constructed **64 positive fault paths**, and matched the full 64-by-64 logical+bath Liouville superoperator to residual `1.1550e-14`. It also passed 32 arbitrary correlated input–bath state checks. This is a checked **finite universal-gate-set fault representation** (Clifford gates plus T), *not* efficient fault-tolerant processing and *not* a universal hardware computer.

Non-Clifford completion cannot inherit the previous **Pauli-only deferred-frame** theorem unchanged. A raw Pauli frame conjugated through `T` is generally a Clifford, not a Pauli. The present construction physically performs the trusted conditional `S` before moving on (or a separately justified generalized Clifford-frame compiler must be supplied).

## 8. Strong conventional comparisons, failures and operational ranking

**Pauli-only tester:** lowest source/test hardware overhead; requires no trusted magic reference, but an honest failure baseline `f=0.1464`. Within its single-copy measurement class its contrast is optimal, but the statistical overhead is large: the risk certificate can be several times the true hidden fault weight.

**Trusted magic reference:** a second, *trusted* `|A_0>` and a destructive singlet/Bell projection on candidate+reference give exactly `F=Q/2`, with **zero honest false failures** and contrast `1/2`, on the complete bath. `trusted_reference_tradeoff.py` checked residual `6.33e-16`. It consumes a scarce known-good magic reference and a joint Bell analyzer. Comparing two unknown source outputs with each other is **not** a substitute: two identical `|A_1>` wrong resources never produce a singlet and pass all such comparisons. This architecture is only attractive if that trusted reference is independently available and cheaper than the extra local-Pauli shots.

**Physical `SX` key reuse or exposure:** exact, constructed failures of positive fine-record paths. The privately randomized source must really retire the key, and sources cannot reuse it when correlated with an adversarial bath.

**Unknown terminal hardware:** physical readout preceding the classical latch, CNOT crosstalk, Clifford `S` feedback and imperfect `SX` twirls remain in the trusted physical interface or require complete-boundary error allowances. Assigning a measured classical flip probability to an unknown coherent analyzer error is invalid.

**No indefinite future prediction:** a finite calibration record cannot rule out the hidden autonomous-clock obstruction in the user-supplied governing original. Each declared statistical block has its own confidence budget, or a separately established physical uniform bound is required. Nothing here certifies an unrestricted source lifetime.

**No automatic fault tolerance:** a finite virtual count on gate calls does not ensure that an arbitrary downstream quantum algorithm works. Codes, decoding, correlated faults, physical routing, final readout and hardware resource requirements must be specified. A conventional equally informed controller can use every above tool.

## Primary science / priority comparison

- Bravyi and Kitaev (2005), *Universal quantum computation with ideal Clifford gates and noisy ancillas*, PRA 71, 022316, https://doi.org/10.1103/PhysRevA.71.022316 — magic-state supply is an established means of extending Clifford operations to universality; this is not a new discovery here.
- IBM Quantum Learning, *Error correction II*, https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/error-correction-ii — standard T injection and conditional Clifford correction.
- Abdul Sater, Garnier, Martinez, Ollivier, Chabaud (2025), *Efficient certification of intractable quantum states with few Pauli measurements*, https://arxiv.org/abs/2511.07300 — prior single-Pauli verification in non-iid magic-assisted computation.
- *Efficient Benchmarking of Logical Magic State* (2026), DOI `10.1103/fwjt-mw2c`, https://pubmed.ncbi.nlm.nih.gov/41723686/ — relevant lower bounds on single-copy magic benchmarking and routes using multiple copies; the present honest-failure baseline is consistent with those limits.
- Zhang, Seshadri, Knill (2026), *An efficient method for spot-checking quantum properties with sequential trials*, https://arxiv.org/abs/2602.08114 — general non-iid sequential evidence theory; the centered effect calculation is an instance, not new sequential-statistics foundational science.

## Next physics task

The mathematically strongest capability now has a clear experimentally decisive question: **does the supplied finite weak `X` probe actually produce the promised postmeasurement pure state with physically bounded bath backaction?** A proper assay is to hard-reset a candidate, perform weak `X`, apply the specified feedback, then destructively check its `X`, `Y`, `Z` Bloch components before and after the Clifford quarter-turn. At the ideal target setting the post-feedback pre-rotation Bloch vector must be `(1/sqrt2,0,1/sqrt2)` and the post-rotation Bloch vector `(1/sqrt2,1/sqrt2,0)`. This assay can expose the same-POVM/wrong-instrument counterexample, but cannot by itself give an operator-uniform bound against every possible unseen bath state. The most valuable follow-on is a **physically justified complete-instrument and key-isolation contract**, alongside the existing online sacrificial audit that does not require trusting the source mechanism.

## Executed preservation

All Python files named above are actual saved executables, accompanied by their JSON results in this archive. The scripts use NumPy and SciPy only and include assertions. `RUN_VALIDATIONS.sh` executes them; `validation.log` records outcomes and `SHA256SUMS.txt` hashes saved files. Individual simulations represent model reference histories with a mathematical bath **represented only inside validation**, not physical measurement of hidden quantum memory. No source code was pushed to GitHub.
