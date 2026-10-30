# Independent review: nominal false-token exponential energy

2026-10-30. **Scoped PASS: raw nominal operator inequality only.** The previously accepted stochastic native LOCC theorem is unchanged. No useful-rate estimate, continuous-noise threshold, initialization theorem or bare-output result is promoted by this receipt.

## Frozen sources

- Root `semantic_defect_energy_root_20261030/RAW_NOMINAL_OPERATOR_SUPERMARTINGALE_V1.md`: `5ee644bc79ca64a4e1555912208b07ba9db537bbdc73074fb4afa7ca57e6824b`.
- Root `semantic_defect_energy_root_20261030/ACTUAL_FALSE_TOKEN_LEDGER_V1.md`: `b479668e835db3fa1460106d29181bb7a048167691b350ae8686bb88ad5283bc`.
- Governing/completing compiled proof `native_locc_continuous_operator_20261030/FULL_NOMINAL_RAW_EXPONENTIAL_INEQUALITY.md`: `3fe5a8145e48a649591f8688eb688c50d496e5f40c9e580912f0733396a86898`.

Exact machine/payload/energy dependencies and preserved snapshots are in `SOURCE_MANIFEST.json` and `SOURCE_SHA256.txt`. The governing proof uses the previously frozen actual gate and reset instance, not an arbitrary dilation having the same clean instrument.

The accepted statement, in the exact full-Hilbert forest frame, is

`E=U+R_t D_false+R_A sum B_A+R_B sum B_B`,

`L_nominal^* exp(sE) <= 0`, for every s>0,

when `R_t>K_B`, `R_B>K_B`, and `R_A>K_A+R_t J_A`, with the structural bounds defined below. Strict negative terms are earned at the declared consuming/healing/improving source projectors. False-token predicates are mathematical observables of actual registers and Alice raw stabilizers, not instantaneous truth sensors or extra physical feedback.

## 1. Token bookkeeping survives every actual phase and transition

Count HOLD(DATA) and WANT in ALL engine phases, every occupied DATA response slot, and Bob P in precisely A/C/B and R(parent A/C/B). P is absent in I/Q and R(parent I/Q). These distinctions matter on malformed states, not just reachable clean histories.

- Failed-test Hamiltonians connect p to its distinct R_(p,j) with identical program validity. In particular R(A) is valid and R(I/Q) is not. A shared R leaf would not suffice.
- Acquisition, computation and rollback preserve validity and immutable P. I-to-A0 LOAD is a reset, not a Hamiltonian edge; it consumes WANT and creates the same-value valid P. An old idle P is never counted or reused without overwrite.
- In malformed C+READ_WAIT, accepting DATA consumes one FIFO token and creates WANT, while the preexisting valid P remains counted. No false token is hidden by the malformed outer phase.
- HOLD enqueue empties HOLD and requires I. FIFO moves empty their sources; accepted DATA moves to WANT; unused replies are discarded. SYNC, READ and ACK do not carry syndrome-value tokens.
- PREFIX watchdog retains P/validity and can only discard an outer cache by setting DRAIN. Complete T removes the private token and Bob cache. READY keeps P invalid on both sides. COMMIT preserves valid P. W refresh in A preserves P.

Thus no nominal copying or validity toggle creates uncharged debt. For Alice SUCCESS, the held output is a real workspace-resolved pointer, not access to an unmodeled environment. Dirty Alice can create false pointers or change the truth of already existing tokens, which is paid separately rather than declared impossible.

## 2. Hamiltonian commutation and other-owner defects

The exact forest removes every native payload/rollback Hamiltonian from DATA. Failed-test leaves inherit the parent frame; live-prefix ownership cannot change. Mechanical projectors are preserved, and the validity checks above show that every remaining controller Hamiltonian commutes D_false. Raw U is DATA diagonal and unchanged. Actual label monitors act only on clock/tag labels and monitor registers, so they also give zero drift. Therefore `[H_nominal,E]=0` termwise on malformed as well as consistent sectors.

A complete h reset changes no other mechanical B_g. This can be shown more strongly than good-range preservation: after forest conjugation its Kraus legs are diagonal in the owner tags, act on h's private registers and actually h-owned DATA, and act on no g workspace/clock. The forest Q_g is DATA independent and diagonal in those tags. Hence the legs commute Q_g exactly. The reset's own Q0,W0 output is universally good.

Resource cleanup z_h-to-free has unchanged owner mask and identity DATA action; it only preserves or heals structural inconsistency. I/A/Q workspace resets also have identity frames and preserve/heal B. COMMIT has identical A_k/C0 consistency, READY identical Qk/I consistency. These non-T cases do not need a fictitious strict mechanical-healing charge.

## 3. The full workspace normalizer is genuinely stronger than clean correctness

Let sigma denote the COMPLETE raw stabilizer syndrome, not just the local read list or unary energy values. For one check, the actual circuit H-controlled-S-H acts on arbitrary workspace input b as X^r(sigma). Thus Alice's complete circuit has the exact label map

`(sigma_A,b) -> (sigma_A,b XOR r_h(sigma_A))`.

For Bob retain ALL syndrome and correction-mask scratch registers. With program a,

`b'=b XOR r_h(sigma_B)`,

`c'=c XOR enc[f_h(a XOR b')]`,

`(sigma_B,b,c,a) -> (sigma_B XOR delta(c'),b',c',a)`.

This is a bijection: undo the Pauli syndrome shift, recover b, then undo the table XOR. The controlled Pauli shifts every affected global raw check, including unmeasured checks. It may act nontrivially within logical/gauge degeneracy, but that does not change the abelian syndrome/workspace label algebra. Physical Pauli operators preserve realizability of syndrome sectors.

Consequently the FULL completed circuits normalize the algebra needed by U, all token truth comparisons, and workspace/program computational labels. Clean W=0 instrument identities alone would not establish this result. The displayed inverse also covers arbitrary dirty mask-workspace c, not just the clean scratch value.

## 4. Complete SUCCESS good/dirty cross blocks vanish

At full ownership, pull the output V through the actual complete terminal overwrite. Its workspace outcome dependence, including Alice's new held value, is diagonal in final workspace labels. Old worker/master/cache/program values are fully source-resolved when overwritten. Other mechanical flags and ownership labels are diagonal spectators. Section 3 therefore makes the pulled weight diagonal in INPUT W/P labels.

It commutes the clean source projector W=0. Thus the good/dirty off-diagonal block of the complete gain is exactly zero. V itself also commutes that projector, so the clean and dirty Loewner estimates can actually be combined.

Distinct ownership-mask blocks do not interfere: the reset and forest preserve tags and V is tag diagonal. In an incomplete-ownership source there is no good subspace at all. Every R source is wholly bad. At B0 the forest is identity for every mask; I/A/Q frames are also identity. These observations cover the remaining reset classes without pretending that an intermediate prefix normalizes the syndrome/workspace algebra.

## 5. Dirty spectral envelopes are operator comparisons, not classical probability claims

For each reset collect ALL raw-energy terms whose structural DATA support it may affect. Their summed spectral range gives K_A or K_B. Do not prune by accidental commutation of a particular prefix. For Alice, J_A counts ALL physical token locations whose comparison checks meet that structural footprint, plus the possible held-output write. Counting only neighboring Bob hubs would miss their FIFO, cache and private-program multiplicity. Bounded degree and finite capacities make these constants independent of N.

Factor out unaffected commuting terms using the Kraus bimodule identity. For a normalized complete bad Bob source, output local weight is at most exp(s K_B), while source weight is at least exp(s R_B); its consumed program/cache debt is nonnegative and need not be used. For Alice the output local maximum is exp[s(K_A+R_t J_A)] and the source minimum exp(s R_A). Completeness gives

`P_bad Phi_B^*(V) P_bad <= exp[-s(R_B-K_B)] P_bad V`,

`P_bad Phi_A^*(V) P_bad <= exp[-s(R_A-K_A-R_t J_A)] P_bad V`.

No product-state assumption or inverse-positive-map step is involved. Correlated syndrome constraints do not invalidate the bounds: the sum of touched term ranges is a uniform scalar range, while the unaffected positive factor commutes through the legs. Partial-prefix instruments need not be monomial for this argument.

In particular, saying Bob leaves Alice unchanged must NOT mean that every normalized Bob reset outcome leaves the conditional Alice distribution unchanged; entanglement permits steering. The correct statement is that Bob Kraus legs commute untouched Alice comparison operators and the COMPLETE source-normalized instrument has its specified effect. This exact operator bimodule property is sufficient here and remains valid with arbitrary reference correlations.

## 6. Clean source inequalities, actual losses and combination

On W=0, Alice writes the true current value and leaves all raw checks unchanged, so it cannot increase the token sum or U. Bob with true P performs the exact ordinary GPT table move, globally nonincreasing in the reviewed integer U. On a strictly improving source it lowers U by at least one. With false P it raises U by at most K_B but consumes at least one false token, giving ratio at most exp[-s(R_t-K_B)]. A clean inverse-prefix abort is DATA identity and deletes its program token. The remaining reset/transport cases are pointwise moves, deletions or mechanical healing as checked above.

Each complete equal-rate source-resolved quantum bundle has actual total source effect `kappa P_source`, not a dimension-multiplied coefficient-norm bound. Its forest-transformed loss still commutes V. Thus its entire dissipator is

`kappa[Phi_source^*(V)-P_source V]`.

The good/dirty cancellation in Section 4 allows the clean and bad bounds to be added on that complete source. Fine dirty-prefix workspace outcomes need not obey the same inequality individually; summing their real gains AND losses is essential. A coherently summed eraser or modified unequal-rate instrument would require a fresh calculation and is not silently substituted.

The resulting charge formula in the governing proof is valid: dirty T sources contribute factors `1-exp(-s delta_A/B)`; clean false-program Bob SUCCESS contributes `1-exp[-s(R_t-K_B)]`; true improving Bob SUCCESS contributes `1-exp(-s)`. The corresponding projectors commute V, so each displayed charge is positive. True improving and false-program clean sources are disjoint, and dirty sources are disjoint from clean ones. Summing other nonincreasing jumps and the zero Hamiltonian drift proves the claimed full Loewner inequality.

## 7. Regression and scope

I reran an independent copy of the full-workspace regression. All 448 source cases passed, including all four ownership masks and all dirty workspace columns. Maximum full-terminal good/dirty cross norm was 4.28e-16; minimum source-minus-gain eigenvalue was -6.42e-15, consistent with roundoff. The partial-prefix cross norm was 2.29, an important negative check: terminal normalizer cancellation cannot be extended to prefixes. These tests support the exact algebra and do not replace it.

The result is stronger than a clean-sector scalar ledger but weaker than a memory theorem. It gives no uniform rate at which a false token reaches consumption, an engine reaches healing, or a useful corrector reaches SUCCESS. It does not supply a positive local service credit, perturbative noise-transfer estimate, killed basin, or final continuous-noise logical bound. It is an all-Hilbert operator fact, not a guarantee that arbitrary initial E is small or that arbitrary dirty initialization is protected. No ideal truth measurement/control has been introduced. The existing stochastic native LOCC receipt remains intact and separate.

No counterexample remains in the frozen compiled raw lemma under its stated complete-reset convention. Author sources were not edited by this audit; snapshots and exact hashes are preserved. No permission or external-action blocker occurred.
