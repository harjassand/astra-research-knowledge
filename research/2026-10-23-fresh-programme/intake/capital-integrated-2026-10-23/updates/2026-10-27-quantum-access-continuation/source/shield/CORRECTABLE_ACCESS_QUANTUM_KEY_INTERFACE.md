# ASTRA / Interim Extra High 1 — Correctable-access quantum-key interface

**27 October 2026 (Australia/Brisbane).** Original programme-specific synthesis and complete-boundary reference checks. The underlying four-qubit code, Knill–Laflamme error conditions, erasure recovery, quantum one-time-pad twirling and operator norm perturbation bounds are established theory. This is **not** a hardware measurement or a scientific-priority claim.

## Scientific decision

The latest `COHERENT_DELAYED_FRAME_FULL_MEMORY.md` assumed direct flag-to-bath interaction is absent for the entire noisy gate. That is a strong architectural premise. The present continuation replaces it with a **correctable-access contract**: the uncontrolled core may interact arbitrarily and coherently with a limited physical subset of an encoded two-bit control flag, including through the same retained noncommuting bath and the data qubit. A final trustworthy syndrome measurement and recovery remove that flag disturbance *on the complete quantum-memory boundary* before the private frame is decoded.

The smallest standard four-spin quantum error-detecting code encoding two logical key bits provides two distinct options:

- **No exposed-site information:** if every full-call core Kraus operator lies in the linear span of flag operators of Pauli weight 0 or 1, postselecting the two stabilizer syndromes `++` yields the exact positive quantum-service fault instrument. Rejected resources must not be silently retried if an unknown payload has already been consumed.
- **One known exposed physical flag spin `j`:** all four syndrome outcomes are correctable, not merely detectable. Arbitrarily strong and noncommuting interactions of `F_j` with **data + the entire persistent bath** are admissible. After syndrome recovery, the encoded flag is exactly restored and the effective data–bath instrument is independent of its logical state. The syndrome may remain as a classical record for future adaptive control; the *actual decoded Pauli key* must be retired.

For a bounded one-site perturbation, full-boundary channel error after recovery is second order in integrated coupling even if the unexposed data–bath Hamiltonian is arbitrarily large. The decisive no-go is a two-contact bath that copies a logical flag parity while passing both checks. Therefore the **union of accessible flag sites over a full call**, not the instantaneous number of sites touched, must be constrained.

## 1. Explicit two-logical-qubit code and its operational privacy

Take four physical flag qubits, stabilizer generators

\[
S_X=X_1X_2X_3X_4,\qquad S_Z=Z_1Z_2Z_3Z_4,
\qquad P=\frac{(I+S_X)(I+S_Z)}4.
\]

There are four orthonormal codewords, with logical Pauli basis

\[
\bar Z_1=Z_1Z_2,\quad \bar X_1=X_2X_3,
\qquad \bar Z_2=Z_2Z_3,\quad \bar X_2=X_3X_4.
\]

The code has parameters `[[4,2,2]]`. Every nonidentity Pauli on an individual physical flag spin anticommutes with one of the two stabilizers. Consequently, for each site `j` and `a∈{X,Y,Z}`,

\[
P\sigma_j^aP=0. \tag{1}
\]

For *every* quantum input `rho_(L,R)` on the two logical flag bits `L` and arbitrary `R` (including the data, bath and an untouched reference), encoding by the isometry `V` gives

\[
\operatorname{Tr}_{F\setminus j}[(V\otimes I_R)\rho_{LR}(V^\dagger\otimes I_R)]
=\frac{I_{F_j}}2\otimes\operatorname{Tr}_L\rho_{LR}. \tag{2}
\]

Thus accessing **one** physical flag spin supplies no additional information about either coherent control bit even when those bits are initially correlated with the data and hidden memory. Bath information obtained indirectly from the data is not excluded and is already part of the reference quantum channel. The code does not protect two-spin access: e.g., `Z_1Z_2` is a logical `Z` observable and reveals the first bit.

The quantum Singleton inequality `n-k≥2(d-1)` says four is the minimum number of physical qubits for a standard two-logical-qubit distance-two code. This is not a statement that the whole physical service (including reliable controls) is minimum-cost.

## 2. Full-memory theorem: a known exposed site is correctable

Let `D` be the data qubit and `M` the entire arbitrary retained quantum bath (possibly entangled with `D` and other untouched references). Assume the **completed** untrusted physical instrument acts nontrivially on flag site `j` and on `D,M`, but on no other physical flag site during the call. It may contain arbitrary internal coherent operations and reports retained inside `M'`. Expand each full-core Kraus operator as

\[
K_\lambda=\sum_{a\in\{I,X,Y,Z\}}\sigma_j^a\otimes B_{a\lambda},
\quad B_{a\lambda}:D M\to D M'. \tag{3}
\]

No factorization between `D` and `M` is assumed. If the physical core is trace preserving, then `Σ_(a,lambda) B_(a,lambda)^† B_(a,lambda)=I_(DM)`.

For known `j`, the four syndrome subspaces

\[
P_{j,a}=\sigma_j^a P\sigma_j^a
\]

are mutually orthogonal and sum to the full four-flag Hilbert space. The physical instrument *measure the two stabilizers, infer `a`, and apply `sigma_j^a`* obeys the operator identity

\[
(\sigma_j^aP_{j,a}\otimes I)K_\lambda(P\otimes I)
=(P\otimes B_{a\lambda}). \tag{4}
\]

The equation is an identity on **all** input operators and entangled references, not just on a chosen bath state. Each retained `(a,lambda)` label has a positive CP map `B_(a,lambda)(·)B_(a,lambda)^†` on the complete data–bath boundary. The corrected logical flag is exactly unchanged; all bath backaction remains in the `B` maps. Nothing about the bath's dimension, norm, stationarity or commutativity is needed.

The physical input frame uses both encoded key bits `k=(k_1,k_2)`:

\[
C_{FD}=\sum_k|k_L\rangle\langle k_L|\otimes P_k,
\qquad P_k=X^{k_1}Z^{k_2}.
\]

Prepare `|+,+>_L`, apply `C`, run the common untrusted core, recover the known-site error, measure the two logical keys, correct the output by `P_k^†`, and physically retire the key. The branch with retained `(a,lambda)` and measured-but-retired `k` has Kraus operator

\[
R_{a\lambda k}=\frac12(P_k^\dagger\otimes I)B_{a\lambda}(P_k\otimes I). \tag{5}
\]

Let `B_(a,lambda)=Σ_s P_s ⊗ A_(s,a,lambda)` be the Pauli expansion in the data indices. The accepted complete service, **conditional on each retained `(a,lambda)`**, obeys

\[
\sum_k\operatorname{Ad}_{R_{a\lambda k}}
=\sum_{s\in\{I,X,Y,Z\}}\operatorname{Ad}_{P_s\otimes A_{s,a\lambda}}. \tag{6}
\]

All right-side summands are completely positive. They compose through arbitrary later quantum operations and feedback using the syndrome/report history, while the same bath is reused. They are virtual fault labels, not observed classical Pauli draws.

For a random signed `X/Y/Z` sacrificial test through **the same actual core and recovery**, the failed-test bath CP instrument conditional on `(a,lambda)` is

\[
\mathcal F_{a\lambda,\mathrm{fail}}(\mu)
=\frac23\sum_{s\ne I}A_{s,a\lambda}\mu A_{s,a\lambda}^\dagger. \tag{7}
\]

Hence the original hidden-memory sequential fault-count factor can be used without changing the bath representation. A calibrated classical detector-flip probability or a mismatched test-only operation must be paid separately. Ordinary syndrome measurements are **not** substitutes for a matching data fault test.

### A non-Clifford `T` gate

For a declared ideal `T=diag(1,e^{iπ/4})`, use the same encoded *input* Pauli keys and trusted output Clifford corrections `T P_k^† T^†`. Expand the recovered physical call relative to `T` in the conjugated Pauli basis. Equation (6) becomes positive branches with logical operators `T`, `TX`, `TY`, and `TZ`, and the complete bath retained. This does **not** create a `T` operation or guarantee its high fidelity; the untrusted core must actually contain a useful non-Clifford resource.

## 3. Unknown exposed site: exact *heralded* shield

Let a full-call Kraus operator be in the operator **linear span** of identity and weight-one physical flag Paulis, each tensored with arbitrary `D:M` operators, even when the bath coherently controls which one-spin site is exposed:

\[
K_\lambda=I_F\otimes B_{0\lambda}
+\sum_{j,a\ne I}\sigma_j^a\otimes B_{j,a,\lambda}. \tag{8}
\]

Equation (1) immediately gives

\[
(P\otimes I)K_\lambda(P\otimes I)=P\otimes B_{0\lambda}. \tag{9}
\]

Thus postselecting the `(++ )` stabilizers produces the same *accepted* positive task instrument with unknown single-spin site. No knowledge of `j` is needed. If input preparation puts the real unknown payload into this attempt, rejection has already exposed it; safe retry generally requires an entanglement-first design in which the payload remains protected until acceptance.

**Critical quantifier:** a Hamiltonian that touches only one flag qubit *at each instant* need not yield a completed Kraus operator of weight ≤1. Sequential visits to different sites produce weight-two products. A bath-controlled direct sum of one-spin calls can meet (8), but switching between sites within one call generally does not.

## 4. Quantitative perturbation theorem with an arbitrarily fast bath

In the known-site configuration, suppose a unitary core is generated by

\[
H(t)=I_{F_j}\otimes H_{DM}(t)+V(t),\qquad
\operatorname{Tr}_{F_j} V(t)=0,\quad
\varepsilon=\int_0^T\|V(t)\|dt. \tag{10}
\]

`H_DM(t)` may be arbitrarily large and noncommuting at different times. In the `H_DM` interaction picture, `Tr_j V_I(t)=0`. Duhamel expansion with unitary remainder gives

\[
\left\|B_0-U_{DM}(T)\right\|\le\frac{\varepsilon^2}{2}, \qquad
\sum_{a\ne I}B_a^\dagger B_a\preceq\varepsilon^2 I. \tag{11}
\]

The first inequality is the absent identity coefficient of the *first-order* Dyson term. The second bounds amplitude leaving the code before syndrome correction. For the deterministic corrected channel `N_recovered(ρ)=Σ_a B_a ρ B_a†` and unperturbed `U0(ρ)=U_DM ρ U_DM†`, even with arbitrary references,

\[
\boxed{\tfrac12\|\mathcal N_{\mathrm{recovered}}-\mathcal U_0\|_\diamond
\le \min(1,\varepsilon^2).} \tag{12}
\]

This is a full data-plus-bath accuracy guarantee, not just flag privacy or a small observed output marginal. **The bound uses only the local coupling norm, not the bath bandwidth**, and does not label its residual as an exact stochastic fault process in an uncorrected circuit.

For the executable control `ε=0.248`, actual maximum syndrome rejection weight was `0.0074627` versus the universal `0.061504` ceiling; actual good-Kraus amplitude deviation was `0.0046398` versus `0.030752`. In 16 additional instances with bare bath Hamiltonian norm as high as 150, all random correlated-input/reference trace distances obeyed (12).

## 5. Exact failure: an apparently local bath learns a logical key

Because `\bar Z_1=Z_1Z_2`, a bath spin starting in `|0>` can copy the logical key with **two successive CNOTs** `F_1→M` and `F_2→M`. Each individual gate touches only one flag spin. The combined circuit preserves both stabilizers, produces no syndrome alert, and leaves the bath carrying `k_1`.

Let that bath spin then control a `Z_D` interaction of angle `θ=π/8`. The incoming encoded key `k_1` determines the sign of `Z_D`, while the input Pauli `X_D^{k_1}` also reverses that sign. The two signs cancel after output correction, leaving the **coherent rotation** `exp(-i θ Z_D)`, rather than the falsely inferred Pauli mixture `cos²θ id+sin²θ Ad_Z`.

For a `|+>` data input, the half trace-distance difference is exactly

\[
\boxed{\frac12|\sin2\theta|=\frac{1}{2\sqrt2}=0.3535533906,}
\]

although the encoded syndrome accepts with probability 1. The bath can separately retain a copy of the key while current output checks appear plausible. The original instruction to certify the **entire interval and memory boundary** remains essential.

If the site is unknown and correction is attempted without location information, `X_1` and `X_2` give the same syndrome but differ by a nontrivial logical operator on the code. The four-spin code detects either error yet cannot deterministically correct both without additional location knowledge.

## 6. Physical implementation and honest comparator

I compiled the ideal four-flag operations explicitly into ordinary Clifford primitives:

| Task | Entangling operations |
|---|---:|
| Prepare encoded logical `|++>` from `|+++0>` | 3 CNOT |
| Apply `X^{k_1}Z^{k_2}` using four physical flag controls | 2 CNOT + 2 CZ |
| Measure `ZZZZ` and `XXXX` nondestructively with coherent ancilla(s) | 8 CNOT |
| **Subtotal per call** | **15** |

The key can be extracted by measuring all four flags in `Z` and computing `k_1=b_1⊕b_2`, `k_2=b_2⊕b_3`. An additional random global-complement bit carries no further task information *under the ideal code instrument*. This readout adds four physical measurements; error recovery adds at most one known-site physical Pauli, and output correction adds data-local gates. Trusted ancilla preparation, measurement, connectivity, timing, reset and control errors are additional costs. If bath coupling continues during stabilizer extraction, ideal syndrome projectors cannot be inferred from the ideal gate endpoints.

A strong conventional controller with an independently trusted private classical RNG, isolated key storage and endpoint Pauli frames is **much cheaper**. Such a controller also obtains exact positive fault paths under the same common-call conditions. The present code is useful only when **hardware locality of quantum flag exposure can be justified more credibly than perfect flag isolation**; this is a trade of additional reliable Clifford gates for a different physically enforceable noise assumption. No architectural performance advantage is asserted.

**Availability:** the unknown-site postselected construction can reject every attempt for a perfectly permitted strong local error. Known-site recovery avoids that rejection, but cannot rescue arbitrary degradation of the data by the exposed physical core. Any claimed throughput, quantum capacity or fault-tolerance threshold must additionally cover resource quality, terminal corrections, gate faults, logical routing, and finite confidence/time budgets.

## 7. Executed evidence (not hardware)

All listed outputs arise from the actual scripts in the archive; no numerical data were given to a real quantum device.

| Program | Verified result |
|---|---|
| `four_spin_flag_shield.py` | 20 arbitrary one-site full-memory unitaries: accepted positive-path residual ≤ `3.04e-16`, physical failed-test instrument residual ≤ `2.07e-16`; direct two-site logical attack produces `0.35355339` trace-distance failure |
| `known_site_recovery.py` | 20 different coherent-memory unitaries, all four stabilizer syndromes corrected: maximum conditional syndrome/test CP-instrument residual `5.91e-16`, full trace-preservation residual `3.32e-15` |
| `composed_memory_and_sequential_access.py` | Two-round channel with syndrome-dependent feedback and same bath: 16 conditional output-instrument residuals ≤ `2.62e-16`; sequential key-copy counterexample |
| `local_privacy_marginals.py` | 100 random correlated logical/data/bath/reference states, one-spin decoupling residual ≤ `1.28e-16` |
| `native_four_spin_compiler.py` | Actual CNOT/CZ gate matrices and coherent stabilizer extraction implement the declared complete instruments to ≤ `6.29e-16` |
| `multikraus_branch_audit.py` | Noisy three-branch CPTP core with retained internal report and syndrome: instrument residual ≤ `3.46e-16` |
| `uniform_weak_local_bound.py` | 16 `H0,V` models, each with 26 correlated-reference input probes, satisfy second-order full-channel and rejection bounds |
| `nonclifford_T_local_shield.py` | 80 syndrome-conditioned `T`-gate full-memory channel checks, maximum positive-path residual `6.49e-16` |
| `coherent_unknown_site_detection.py` | Bath-coherent unknown exposed location, positive-path residual `5.11e-16`, nonzero bad effect `0.09383` |

### Governing premises and prior science

- User-supplied latest: `astra_quantum_delayed_flag_20261027/COHERENT_DELAYED_FRAME_FULL_MEMORY.md`; earlier `LIBRARY_RENDERED_ACQUIRED_TASK_INTEGRITY_WITH_QUANTUM_MEMORY(1).txt` and `LIBRARY_RENDERED_COMPOSED_POSITIVE_SERVICE_FAULTS(1).txt`. The earlier exact completed-service identity and latent fault estimator are retained at their actual scope, not assumed to hold for an arbitrary leaked-key process.
- Knill and Laflamme (1997), *Theory of quantum error-correcting codes*, https://doi.org/10.1103/PhysRevA.55.900. The fundamental error-correction/erasure mechanism is not new.
- Linke et al. (2017), *Fault-tolerant quantum error detection*, https://doi.org/10.1126/sciadv.1701074. The specific `[[4,2,2]]` code is experimentally established prior art.
- Quantum Singleton bound, e.g. Dehmel and Li (2026), https://arxiv.org/abs/2602.20186; `n-k≥2(d-1)` is standard and used only to compare code size.
- White et al. (2022), *Non-Markovian Quantum Process Tomography*, https://doi.org/10.1103/PRXQuantum.3.020344. General complete process tomography is an established, measurement-intensive comparator, not supplied automatically by the present fault certificates.

## Next credible physical attack

Build a small **complete-instrument** experiment with four physical flags, one data qubit and one retained spectator memory qubit. Prepare encoded flags, execute the four preframe gates, deliberately couple the memory to (i) one known flag spin, (ii) one unknown but fixed spin, and (iii) two spins sequentially, then carry out actual `XXXX/ZZZZ` syndrome circuits, recovery, classical key retirement and a second memory-sensitive data challenge. The sharp outcome is whether the complete output-plus-memory instrument matches the source's proposed one-spin geometry; equal current-output probabilities alone are insufficient. In real hardware, certify the full timing and cross-talk support of the core and the stabilizer meters; this cannot be inferred from finite success frequencies against an otherwise unrestricted hidden clock.

**Boundary:** Mathematical exactness under correctable access is acquired here. A hardware certification of that access geometry, gate fidelity, syndrome coherence, private key retirement, and useful non-Clifford output **is not** acquired.
