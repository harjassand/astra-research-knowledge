# Independent receipt: fixed-time one-use recovery from shorter calibration

28 October 2026. Reviewer: `producer-workspace/review_recovery_depth_obstruction`.

**ACCEPT at the explicitly fixed-time, identity-input, one-use, forward-only interface.** All new load-bearing claims in the recovery corollary pass. In particular, every permitted short quantum calibration strategy produces the same complete accessible state, while some world has expected Bell-loss and half-diamond-error regret at least `9/512` for the prescribed late one-use service. This is a mathematical acceptance, not a novelty certificate, experiment report, near-correctable lower bound, or general unknown-noise-recovery impossibility theorem.

This receipt binds the corrected `SHORT_EPISODE_ONE_USE_RECOVERY_LOWER_BOUND.md`, SHA256 **`122f5e11b1d2b2ce284515f8b9276dcaf82e775a678ba444ba8930ff008d20bc`**. I read the complete source and governing physical construction/receipt, independently derived the new CP/decoder arguments, and executed a separate deterministic exact diagnostic. No mathematical correction was required.

## 1. Documentary correction and preserved evidence

The initial assigned source had SHA256 `705a9de6aac6dca1e1747260d5364d4a40b79c88c9c88ecb5bf40b33a3d4e7ff`. It asserted that author checks were recorded in `short_episode_one_use_recovery_check.py/.json`, but neither artifact was present at review. Those files were **not** retrospectively created or treated as evidence.

With root's explicit narrow authorization, the initial source was preserved byte-for-byte as `SHORT_EPISODE_ONE_USE_RECOVERY_LOWER_BOUND_pre_evidence_correction.md`. Only the last evidence sentence of the active source was changed: it now states that the author artifacts were unavailable and not relied on, and identifies the actually executed separate reviewer checks. All mathematical statements, interface conditions, constants, and prior-art disclaimers are unchanged. This receipt applies to the corrected evidence statement, not by automatic inheritance to the archived predecessor.

The governing Singer source remains SHA256 `fb24c0a5e0e2033276c823363f52dbfa0e514790835a18cf4f13698fee81665f`. Its full receipt manifest, and the short-word-modulus and raw-core receipt manifests, were reverified with zero hash mismatches. They were not edited. The new corollary does not inherit coherent guarantees from the classical short-word theorem.

## 2. Centering and physical maps

Write `k*=r-2`, `A=alpha^(r-2)` and `v=Ar/(8d^2)`. Independently averaging the two late probabilities gives

    mu=1/2+1/(4d)+A(r-2)/(16d^2).

Subtracting this common midpoint from E gives the late probabilities `f_1=1/2-v/2` and `f_2=1/2+v/2`. The tau value is `1/2-A(r-2)/(16d^2)`. The source's interval argument proves `I/4<=F<=3I/4`; no world-dependent effect or hidden estimation oracle is introduced. The early differences remain exactly zero because the affine identity term has equal normalized expectation in the two worlds.

For any positive memory effect G, `R_G(Y)=Tr(GY)tau` has Choi matrix `G^T tensor tau` and is CP. The two terms defining `V_F` are therefore CP on the **full** input algebra, not only on product inputs. Their trace effects sum to identity. Every output term has the same final memory tau; hence the memory is tensor-product with the entire accessible output and any untouched reference, even when the input was correlated. The full replacer mixture preserves this property and is exactly TP.

The unnormalized Choi convention matters. V has input and output dimension `2d`, while the forward channel has dimension d. The replacer's output density is `I_Q/2 tensor I_M/d`, so its Choi eigenvalues are exactly `1/(2d)`. Thus `J(V)>=I/(8d)` when `lambda=1/4`, and separately the forward floor is `1/(2rd)`.

An independent spectral calculation is useful. In a memory-effect eigenbasis with eigenvalue f, each memory-input/output block of V's Choi matrix has eigenvalues

    lambda/(2d), lambda/(2d),
    lambda/(2d)+2(1-lambda)(1-f)/d,
    lambda/(2d)+2(1-lambda)f/d.

This confirms the lower bound and its normalization; the minimum is attained in the unused qubit Bell directions. Strict interiors are real here, but the forward floor still shrinks as `Theta(d^-3)`.

## 3. Complete quantum calibration equality

The fresh whole-process start makes memory `rho_j` independent of every retained learner system. Before the first USE the only source operations are forwards on memory, with deterministic accessible records. At an allowed early time, the complete input/output qubit channel is the same `N_f` in both worlds; extending by identity covers arbitrary references and inputs correlated with earlier calibration output.

After that first USE, the global accessible state is equal in the two worlds and memory factors as tau. All subsequent operations therefore remain equal, including recycled outputs, unmeasured quantum records and adaptive choices. This proves equality of episode supermaps, not only scalar probabilities. Iteration over independent starts proves equality for arbitrary finite adaptive calibration; an almost-surely finite stopping rule follows by equality of finite stopped output blocks. The stronger claim is supplied by the explicit physical reset structure, not inferred from the imported classical word equality.

The decisive cutoff is correct: an episode of at most `r-2` native calls can first USE only after at most `r-3` forwards. The prescribed deployment needs `r-2` forwards **plus** the USE, or `r-1=d^2-d` total calls. An earlier USE, a preliminary memory reset, an inverse, or an uncharged waiting interval would alter the problem and is not allowed.

## 4. Arbitrary CPTP decoders and both losses

Set `Delta=(1-lambda)v`, `c=1/2-lambda/4`, `t=lambda/4`. The late Pauli weights are `(c+Delta/2,c-Delta/2,t,t)` and their I/X swap. For any CPTP decoder with Kraus operators K_l,

    a_P=(1/4) sum_l |Tr(K_l P)|^2 >=0,
    sum_P a_P=(1/2) sum_l Tr(K_l^dagger K_l)=1.

Thus the decoder score on a Pauli channel is a convex combination of its Pauli weights. I and X attain the respective largest weights, proving the full-CPTP oracle optimum, not only optimality inside a guessed recovery family. Both oracle losses are `L*=1-c-Delta/2`.

Because calibration has the same state in both worlds and deployment is fresh, inserting that state into a common joint decoder gives one effective CPTP map on the payload output. No retained quantum calibration register avoids this reduction. The two-world mean fidelity is at most c, so mean regret is at least `Delta/2`; at least one world's expected regret is no smaller. Since `v>=3/64` and `1-lambda=3/4`, this is `9/512`.

For arbitrary channels, the Bell input and Bell-projector test give half-diamond error at least Bell loss. For Pauli channels, the Bell input and the convex decomposition into identity/nonidentity Paulis give equality, `1-w_I`. Consequently the I/X corrections attain the same half-diamond oracle value `L*`. Subtracting **that same proved optimum** legitimizes the half-diamond regret claim. No general conversion from fidelity regret to diamond regret is being assumed; it works because both benchmark optima coincide for these channels.

The source correctly keeps a substantial oracle noise floor. It does not imply an impossibility near perfect correction, allow an encoding bypass, or compare with an oracle using a different circuit. Fixed-rate abort clocks also do not preserve the undiluted late-time constant.

## 5. Independent exact diagnostics

The separately authored `short_episode_recovery_independent_check.py/.json` was executed successfully and replayed after the documentary correction. It imports no author recovery diagnostic. Checks include:

- eight prime powers `q=2,3,4,5,7,8,9,16` and exact rational centering, effect spectra, late Pauli weights, oracle losses, regret constants and Choi margins;
- **550** early complete-qubit-channel equalities, represented by their full Pauli-transfer action;
- the exact **36 by 36** USE Choi spectrum at d=3 and TP/factorization identities for all **36 input matrix units**;
- six exact Kraus-channel checks, including non-Pauli rotations, amplitude damping, reset and dephasing, verifying the Pauli-simplex score identities;
- exact integer-recurrence decision risks at `n=0,1,2,4,8,16,32,64` for the separately proposed constructive addendum.

The general claims are proved algebraically; finite diagnostics are not extrapolated into a theorem. Floating point is used only to display supplementary decimal summaries, never to establish PSD, equality, or inequalities. Source calls, actual episodes, random-number draws, acquired counts, hardware executions, environment tomography and generic quantifier-elimination runs are all zero. The unavailable author checks remain unavailable.

## 6. Constructive implication and literature boundary

The separate `DEPTH_ENABLED_BELL_PROBE_RECOVERY.md` shows what changes when calibration may reach `r-1` calls: paid Bell-pair endpoint probes can learn the I/X correction preference without observing the environment. It gives the candidate exact minimax formula

    R_n=(Delta/2)[1-TV(w_1^(tensor n),w_2^(tensor n))],

and a finite confidence budget `n>=(2/Delta^2)log(1/eta)`. Its proof treats classical Pauli labels only as an information upper-bound relaxation; actual allowed Bell probes attain them. It preserves the original deployment task. **This reviewer-derived constructive note is not independently received by this receipt.** It needs a separate receiver for its adaptive-calibration sufficiency and exact minimax extension.

I directly consulted [Morales-Hashemi–Smith–Cao, arXiv:2610.03545v1](https://arxiv.org/html/2610.03545v1), Sections III.3/V and Appendices B/H/I. Its recovery-regret and delayed-calibration results are close governing prior art, not generic background; the constructive note explicitly credits them. This receipt certifies no novelty of a calibration/recovery conflict, quantum-program-state reduction, or experiment-depth advantage.

The harmonic mechanism remains credited to Singer and the close Mereghetti–Palano / Bertoni–Mereghetti–Palano automata antecedents documented in the unchanged governing source and receipt. I did not newly obtain their historical full texts. Mathematical verification here is independent of a priority determination. **No unresolved mathematical blocker remains for the corrected lower-bound source hash above.**
