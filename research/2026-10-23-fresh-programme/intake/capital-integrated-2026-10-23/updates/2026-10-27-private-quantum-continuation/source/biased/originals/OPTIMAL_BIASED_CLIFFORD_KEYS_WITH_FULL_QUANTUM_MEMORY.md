# ASTRA / Interim Extra High 1 — Sharp positive fault accounting with biased secret Clifford keys

**Scientific continuation, 27 October 2026 (Australia/Brisbane).** This document records original derivations within Astra plus executed finite-dimensional reference checks. **No quantum device was operated.** The mechanism is an application of the established theory of completely positive maps, Schur multipliers, Pauli/Clifford twirling, teleportation and non-iid sequential estimation. Priority is not established.

## Scientific choice

The prior completed T-gate Choi resource construction handles coherent factory errors and retains raw teleportation outcomes by pinching the four Choi-error sectors using two secret Clifford bits. For imperfect key distribution `p`, its previous safe CP decomposition retained an exact clean suboperation of weight `r=4 min_g p_g`. That method first extracted a physical uniform-key *submixture*, assigning all remaining keys to faulty branches. It was rigorous but left useful complete-positivity structure unused.

I attacked the strictly stronger question: **What is the maximum universal good-sector completely positive suboperation contained in the ACTUAL biased-key twirl, when the key is truly retired but the teleportation outcome is retained?** The result is the **harmonic coefficient** below. It also applies to full coherent T operations wrapped by Pauli input/Clifford output frames, without a separate Choi resource.

## Theorem 1. Optimal universal sector extraction for a biased character twirl

Let `G` be an abelian check group with `d` distinct one-dimensional characters and common eigenbasis `|j_s>`, `s=0,...,d-1`. Write `s=0` for the desired ideal logical sector, and assume every `g` has an accurately implemented character action `g|j_s>=chi_s(g)|j_s>`. The private key is drawn independently of the **entire current apparatus quantum state** from a known probability vector `p_g>0`, and its value is physically inaccessible to every later permitted process. The averaged complete operation is

\[
\mathcal D_p(X)=\sum_g p_g D_g X D_g^\dagger,
\quad D_g=\sum_s\chi_s(g)\Pi_s.
\]

Define the specified **good CP filter** `P_0(X)=Pi_0 X Pi_0`. Then

\[
\boxed{\mathcal D_p=\alpha_*\mathcal P_0+\mathcal R_*},\quad
\mathcal R_*\ \text{completely positive},\qquad
\boxed{\alpha_*=\frac{d^2}{\sum_g p_g^{-1}}}.
\tag{1}
\]

No coefficient larger than `alpha_*` admits this **same universal sector-projection CP submap**. If some key has probability zero, the universally guaranteed coefficient for this projection filter is zero. This is an optimality statement within this exact CP-order problem, not a claim of optimality over other physical verification schemes.

**Proof.** In the `j_s` basis, `D_p` is a Schur multiplier with correlation matrix

\[
C_{st}=\sum_g p_g\chi_s(g)\chi_t(g)^*,\quad
C=H^\dagger\operatorname{diag}(p)H,\qquad H^\dagger H=dI.
\]

The residual map `D_p-alpha P_0` is CP on all input/reference systems iff `C-alpha e_0 e_0^\dagger` is positive semidefinite (the Choi-matrix criterion for Schur multipliers). For full support `p`, the inverse exists and the rank-one positive downdate condition is

\[
\alpha\le \frac{1}{e_0^\dagger C^{-1}e_0},\quad
C^{-1}=\frac1{d^2}H^\dagger\operatorname{diag}(p^{-1})H,
\quad e_0^\dagger C^{-1}e_0=\frac1{d^2}\sum_g\frac1{p_g}.
\]

The inverse bound gives (1), including equality. Explicit nonnegative Kraus operators for `R_*` are obtained by eigendecomposing `C-alpha_* e_0e_0†` and using the eigenvectors as coefficients of *diagonal resource operators*. Tensoring every Kraus with identity on arbitrary reference and memory systems preserves complete positivity. If `p_g=0` for any `g`, then the nullspace of `C` overlaps `e_0`, making any strictly positive rank-one subtraction nonpositive.

The physical key must actually disappear from the future-accessible output. The residual Kraus representation may mix **discarded** key alternatives coherently as a mathematical positive refinement; it is **not** a classically observed subset of random-key outcomes. If the raw key label is retained as a physically accessible flag, each conditioned key channel has rank-one Choi support and this projector subchannel generally has no nonzero weight.

**Small bias.** If `p_g=1/d+epsilon_g` with `sum epsilon=0`, then

\[
\alpha_*=1-d\sum_g\epsilon_g^2+O(\|\epsilon\|^3).
\]

The conservative previous coefficient `d min p` suffers a first-order bias penalty; the sharp coefficient suffers a quadratic penalty. For `d=4`, `p=(.26,.24,.25,.25)` it is `alpha_*=.9991993594875902`, versus `r=.96`.

## Theorem 2. Exact completed T-resource and retained-outcome fault paths

Prepare a possibly coherent, bath-correlated Choi resource for `T`, with orthogonal resource-error projectors `Pi_s=|j_s><j_s|`, `j_s=(I tensor TP_s)|Phi+>`. A test destructively measures one of five local Pauli products and physically discards the candidate; a use Bell-measures the actual input, applies the Clifford correction `TP_mT†`, and may **retain** the raw Bell outcome `m`. Apply the independently drawn and retired four-key Clifford stabilizer twirl before the private test/use decision.

Composing Theorem 1 with the entire Bell outcome instrument produces an exact positive refinement of **each** retained outcome, with the complete quantum bath and arbitrary input/reference correlations carried throughout. Summing the good outcomes gives

\[
G^*(I)=\alpha_*\Pi_0,\quad
B^*(I)=(1-\alpha_*)I+\alpha_*Q,\quad Q=I-\Pi_0.
\tag{2}
\]

The `G` branch is the specified ideal T action on the conditioned input, together with a bath operation; `B` is arbitrary and need not be a Pauli-diagonal residual. A selected virtual good branch does not imply that the normalized incoming input is unsteered by conditioning if it initially correlated with the resource.

The existing destructive five-setting local resource test has a **complete bath effect**

\[
F=fI+\nu Q,\quad \nu=(\tfrac12+\sqrt2)^{-1}\approx .52240775,\quad
f=(\sqrt2-1)\nu/2\approx .10819419.
\tag{3}
\]

It remains invariant under every Clifford check separately, so biased keys do not change its physical test effect. No nondestructive resource verification is inferred.

**Complete numerical verification:** full `D:A:B:M` matrix units (`16 × 16`, with two-dimensional bath), all four retained Bell outcomes, three unequal key scenarios and one zero-support case. Explicit CP Kraus residuals and good/bad trace effects agree within `6.2e-16` for individual flagged-channel matrix units and `5.6e-15` for trace effects. These are numerical checks of the exact algebra, not empirical evidence of gate quality.

## Theorem 3. An alternative: frame the entire untrusted completed T port

Suppose an actual complete CPTP service `E: L(DM)->L(BM')` is available, and its input and output logical qubits can be addressed by trustworthy local frames. Expand each entire physical Kraus operator—including any factory, analyzer, raw classical flags, coherent crosstalk and memory—in the Pauli basis relative to the requested T action:

\[
K_\lambda=\sum_{s=0}^3 (TP_s)\otimes B_{s\lambda}.
\]

Apply `P_g` to the input and the **matched Clifford** `TP_gT†` to the output. Retire a fresh independent key drawn from `p`. The complete effective operation then has an exact positive ideal-T branch with Kraus `sqrt(alpha_*) (T tensor B_{0lambda})`, plus a CP residual. Its bad effect is

\[
(1-\alpha_*)I+\alpha_*\left(I_D\otimes\sum_{s\ne0,\lambda}B_{s\lambda}^\dagger B_{s\lambda}\right).
\]

The corresponding five-setting direct input/output local-Pauli tester measures `f I + nu W` on the **actual retained bath**, even for biased keys. This yields a second route that does **not** assume a trusted internal Bell analyzer. It instead needs reliable local input Pauli frames, matched output Clifford frames, input test preparation, terminal readout, and a completed physical call whose dynamics do not receive a separate role-dependent side signal.

The `entire_T_port_full_memory.py` model contains two noncommuting coherent system–bath processes and an internal raw classical flag deliberately retained in `M'`. All complete physical-channel matrix units and test bath instruments passed under the biased distributions `(.26,.24,.25,.25)` and `(.4,.3,.2,.1)` and uniform control, with maximal residual `1.90e-16`. Thus this is a task-boundary **alternative** to the Choi-resource method, not an additional assumed physical gate.

## Sequential consequences (no iid bath assumption)

With current candidate effect (2), choose private predictable test probability `q_i` after all source settings, before the candidate's test/use choice. Let `z>1` and set

\[
a_i=1-\frac{(1-q_i)\alpha_i(z-1)}{q_i\nu},\qquad
c_i=1+(1-q_i)(1-\alpha_i)(z-1)-q_i f(1-a_i),
\]

requiring `0<a_i<1` and `c_i>0`. The weighted current effect is exactly `c_i I`:

\[
(1-q_i)[I+(z-1)((1-\alpha_i)I+\alpha_iQ)]
+q_i[I-(1-a_i)(fI+\nu Q)]=c_iI.
\]

For virtual non-good USE count `B_n` and actual failed-test bits `A_i`, `z^{B_n} prod_tests a_i^{A_i}/prod_i c_i` is a nonnegative unit-mean martingale (or a supermartingale under correctly directed test-effect inequalities) even with arbitrary quantum memory and adaptive controls. A finite predeclared `z` grid with divided confidence budgets, Ville's inequality, and the transport register `V_n=min(U_n,V_{n-1}+1_USE)` give simultaneous finite-run virtual fault certification. The improvement in the extracted good submap can be nested at the CP level: `(alpha_*-r)P_0` is itself CP, so the new virtual bad branch can be coupled as a subset of the old virtual bad branch, though **numerical confidence bounds need not improve on every individual noisy test transcript**.

### Executed online physical reference

The simulator carries the two-dimensional noncommuting bath through the actual **coherently biased source**, local destructive test (selected five-setting Pauli parity), or Bell teleportation and measured `X` query. It samples the public retained Bell result and the query outcome. The observer sees neither bath nor virtual branch labels. Both controllers receive the same key distribution and seeded physical histories (up to their potentially different stopping prefixes), and differ only in the defensible clean coefficient.

These numbers are from **16 individually completed trajectories per controller/setting**, with an 85-fault admission budget, 600-candidate cap and a 99% nominal all-prefix certificate.

| Keys | Prior `4 min p`: mean uses | Sharp harmonic: mean uses | Status |
|---|---:|---:|---|
| `.26,.24,.25,.25` | 237.81 | **259.81** | Completed reference |
| `.40,.30,.20,.10` | 91.12 | **150.94** | Completed reference |

The 16-trajectory online figures are exploratory computational comparisons, not independent proof of statistical coverage or guaranteed improvement on every run. The hidden accumulated number reported in the source JSON is a *sum of conditional virtual fault probabilities*, not a sampled virtual fault count. Several larger trajectory reruns exceeded their execution windows; only the completed small ensembles are used here. The operator theorem supplies coverage under its assumptions.

The optimized implementation **precompiles** every physical source/test/Bell-outcome/query Kraus instrument into a four-by-four bath superoperator. A 16-trajectory comparison reproduced the slower full-density execution numerically. Only the fast, completed 16-trajectory ensemble is in the consolidated validation.

## Sharp failures and physical qualification

1. **Key retained or leaked to the bath.** Every key-conditioned channel is a rank-one unitary-conjugation Choi map and has no positive `Pi_0` projector subchannel for generic coherent resources. A concrete `sqrt(.99) j_I+sqrt(.01)j_Z` input differs from the falsely assumed flagged good/bad map by half trace distance `0.0994987437` if both key and Bell outcome remain future-accessible. Retiring the key reduces the same distance to `2.18e-16`. This is a complete-channel distinction, not merely a question of key secrecy from outside attackers.
2. **Missing keys.** If any `p_g=0`, the universal coefficient `alpha_*=0`. Even two *individually unbiased* key bits may have `p=(.5,0,0,.5)` and fail completely. Marginal bit frequencies do not certify joint private randomness.
3. **Biased physical keys plus unknown side information.** The theorem requires a fixed conditionally independent classical key distribution, not just favorable observed marginal frequencies. Conditional distributions that depend on hidden quantum memory, a recorded key side channel, an autonomous future clock or hardware that changes its own error channel according to the key invalidate the claimed physical averaged map.
4. **Untrusted endpoint gates.** If the actual frame pulses depend coherently on the hidden bath or leak their value during the call, the exact simple character representation fails. The method does not manufacture calibrated Clifford operations.
5. **Coherent terminal errors.** An unrandomized coherent final unitary can have zero nontrivial ideal clean CP subchannel despite small diamond distance; moving the entire completed port inside the twirl is one conditional repair, not a proof that the boundary frames work.

## Classical key calibration and a simple alternative

For a stationary, iid classical key source, with observed frequencies exactly `(1/4,...,1/4)` and simultaneous confidence bounds `p_g in [1/4-epsilon,1/4+epsilon]`, `sum p_g=1`, convexity of `sum 1/p_g` gives the **sharp** robust clean coefficient

\[
\boxed{\inf_{p\text{ in this simplex-box}}\alpha_*=1-16\epsilon^2}.
\]

Its worst distribution has two probabilities `1/4+epsilon` and two `1/4-epsilon`. For `epsilon=.02`, `alpha_* >=.9936`, compared with the old `4 min p>=.92`. Using a union Hoeffding interval at confidence 99%, `epsilon=.02` requires **at least 8,356 iid classical key draws** to guarantee each population probability lies within that radius of its observed frequency. This calibration uncertainty must have a separate confidence budget if combined with the quantum fault certificate. Crucially, finite samples do **not** establish iid, independence from quantum memory, or unrestricted future stationarity.

If each of two independent key bits has bias `e` from a fair coin, a two-bit frame has `alpha=(1-4e²)²`. XORing *two independent raw sources* for each frame bit gives effective bias `2e²` and `alpha_XOR=(1-16e^4)²`. At `e=.06`, the key-induced conservative fault allowance falls from `0.02859264` to `0.000414677` without extra quantum gates. This elementary classical preprocessing is **not a quantum-proof extractor against arbitrary correlated side information**. Perfectly correlated raw bits produce deterministic XOR output. Compare the established literature on two-source extractors with quantum side information before attempting a hardware implementation.

For `d=4^n` Clifford-check keys with independent raw bit biases `e_k` (`2n` bits), the exact formula factorizes:

\[
\alpha_*=\prod_{k=1}^{2n}(1-4e_k^2).
\]

For a two-qubit gate resource (16 keys), 1% independent bit biases give `alpha_*=.998400959744` versus the earlier `.92236816` uniform-submixture coefficient. This is a cost improvement in **certified key-induced fault allowance**, not proof that all real multi-qubit stabilizer corrections are physically available.

## Scientific comparison and recommended attack

A well-equipped conventional quantum controller supplied with identical completed ports, Clifford frames, tested preparations, true private randomness and memory-inclusive calibrations can apply every theorem above. No unique AI-research advantage or newly demonstrated hardware capability is asserted.

Compared with the prior certificate, the new CP-order refinement is strictly stronger within its declared information class, with a particularly large benefit under modest classical key bias. It also broadens the scope of *exact* complete-port certification to include untrusted live T operations if trustworthy matched endpoint frames exist. It does **not** remove the final physical trust anchor.

The next consequential experimental attack is therefore to establish a **complete-boundary causal randomization interface**: verify frame operation timing and waveform symmetry, prevent raw keys and role bits from reaching the interacting bath (including deferred feedback), and bound frame-gate coherent errors as a full quantum instrument. Only after that can source/test and whole-port certification be meaningfully compared on hardware. A hidden autonomous clock remains a counterexample to extrapolating finite data to an unrestricted lifetime.

## Literature and earlier Astra basis

- Earlier governing source: `T_MAGIC_INJECTION_WITH_UNREPRESENTED_QUANTUM_MEMORY.md` (supplied prior work); `COMPLETE_FACTORY_MAGIC_GATE_WITH_QUANTUM_MEMORY.md`, especially Sections 1–6, used as a research foothold. The previous `r=4 min p` minoration is safe; (1) sharpens it in the more general CP-order cone.
- Gottesman and Chuang, gate teleportation / Clifford hierarchy, 1999. See [Caltech thesis, section 2.2.6](https://thesis.caltech.edu/17297/2/ChristopherPattison2025Thesis.pdf).
- [González-Castillo et al., *General Gate Teleportation and the Inner Structure of Its Clifford Hierarchies*, 2025](https://onlinelibrary.wiley.com/doi/10.1002/mma.70066).
- [Wallman and Emerson, *Noise tailoring for scalable quantum computation via randomized compiling*, PRA 94, 052325 (2016)](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.94.052325).
- [IBM Quantum, channel/Choi CP equivalence](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/representation-equivalence) and [Schur-multiplier channel background](https://www.nature.com/articles/s41534-022-00550-2).
- [Miller, Sandfuchs, Ferradini, *Improved Two-source Extractors against Quantum Side Information*, 2025](https://arxiv.org/abs/2503.05528) and [Li et al., *Real-time seedless post-processing for QRNGs*, 2024](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/qtc2.12118) for the distinct stronger extraction problem.
- Sequential non-iid estimation-factor infrastructure: Zhang, Seshadri, Knill (2026), https://arxiv.org/html/2602.08114.

## Executable preservation

The files in this folder include the two original reference mathematical models (copies of prior source scripts), their current new harmonic/whole-port extensions, the fast and slow complete-bath trajectory runners, independent retained-key and 16-key checks, classical calibration, XOR conditioning, exact JSON results, and `RUN_VALIDATIONS.sh`. Run from this folder with Python/NumPy/SciPy. **Neither a GitHub commit nor a hardware test was made.**
