# Independent audit: coherent encoder discovery with unrestricted recovery

**Verdict: PASS_WITH_EXPLICIT_SCOPE.** 27 October 2026. No unresolved mathematical blocker was found in the reviewed version of `COHERENT_ENCODER_UNRESTRICTED_RECOVERY.md`. This is a constructive theorem conditional on its stronger, qualified coherent calibration interface and the already received collective reduction/purification primitives. It is not a hardware demonstration, complete implementation, practical-resource result, or new comparison lower bound.

## What was reviewed and replayed

The complete authored proof, both checker implementations, and the four local dependency proofs were read. The author's checker was replayed successfully (**174 checks**), the independent checker was replayed successfully (**220 checks**), and both Python files passed `py_compile`. The final receipt binds the exact proof, both scripts and results, this audit, and all four local dependency files by SHA-256. The dependencies themselves were not edited or re-proved externally.

The independent checker constructs channels from independent random Stinespring isometries and direct Kraus matrices; it does not merely rerun or parse the author's formulas. It checks normalized source Choi states, full decoder Choi matrices, coherent contractions, effect bounds, arbitrary-density SDP coefficients, root-fidelity inequalities, stationary-net geometry, scalar allocations, phase/rank counterexamples, and exact primal/dual certificates for reset-mixture channels. Random checks support the proof's algebra; the proof, not finite sampling, establishes uniform claims.

## Independent mathematical verification

### 1. Actual coherent source and uniform positive loss

With a retained two-qubit control and one-qubit logical reference, the physical Stinespring vector is `|Ψ⟩=(1/2)Σ_i |i⟩|ψ_i⟩`. Projection onto a real unit control direction gives the normalized ordinary encoder Choi state divided by four. Consequently

`Tr Γ·4|x⟩⟨x|⊗[I−(id⊗D†)(Φ₂)] = 1−F_e(D E_x)`.

The decoder adjoint is completely positive and unital, so the effect lies between zero and `4I`. This remains a positive risk for an arbitrary estimated density, even if that density violates physical Choi/control marginal constraints. Such estimated risks can reach four; treating them as at most one would be incorrect. The proof retains the correct larger constants.

The source call is not a free postselected ordinary Choi query. One complete coherent preparation costs one call, and the algorithm tomographs the whole state rather than conditioning on a control projection.

### 2. Rank and support promises are correctly inflated

The environment marginal is the average of the four anchor environment marginals. Its rank is at most the sum of their ranks, giving `rank Γ≤4R`. The physical marginal is the average of four anchor outputs, each of rank at most `2R`, giving common output support dimension at most `8R`. Linear combination of the anchor Stinespring vectors proves `rank J_x≤4R` throughout the encoder family.

The four-Bell-sector source saturates all these bounds with anchor rank one: coherent-state rank four, physical marginal rank eight, and generic encoder Choi rank four. Thus using `R_d=4R` for ordinary deployment is necessary under the stated anchor-only promise. Reusing `R` would not be justified.

### 3. Common-frame chronology is sound

Exactly one reduction acts on all physical `B` registers of the coherent bank, while the known `IA` registers remain untouched. The imported arbitrary-operator/reference identity yields a mixture of iid whole-`IAB` states in one common virtual frame. The entire homogeneous reduced state is then passed to actual random purification and Clifford tomography. Four separate anchor purifications or separately randomized `B` frames would not establish this claim.

Restriction and arbitrary-replacement extension of unrestricted CPTP decoders show that `ell_opt(x)` is independent of the unknown virtual output frame. These maps are comparison arguments, not implemented inverses or support oracles.

### 4. Bures transfer, global optimization, and SDP coefficients

The Uhlmann/reverse-triangle proof gives the simultaneous inequality `|√risk_Γ−√risk_τ|≤√(8δ)`. Two transfers and an additive empirical optimization gap yield the displayed excess `128m/α+4η/α`. The reasoning is uniform over all encoder/decoder pairs and does not require a grid union bound or estimator independence.

For fixed decoder the estimated encoder loss is a real quadratic with spectrum in `[0,4]`. A global minimizing pair makes its encoder a minimum eigenvector of that fixed-decoder quadratic. The error to a chord-`h` net point is therefore at most `4h²`. The eight cube-face net, `h²≤η/8`, and decoder optimization gap at most `η/2` give a genuine global `η`-optimal pair. The net-size factor is classical SDP work, not additional source acquisition.

For `σ_x=⟨x|τ|x⟩`, the coefficient in decoder input/output order is

`H_x=4[σ_B^T⊗I₂−Swap(σ_x^T)/2]`.

The transpose is full, not partial. The inequality `σ_AB≤2I_A⊗σ_B` implies positivity, operator norm at most four, and trace `6 Trσ_x≤6`. This establishes both the positive objective and its exact decoder-Choi normalization.

The finite SDP repair arithmetic was checked separately. Its displayed tolerances leave PSD margin at least `ζ_sdp/160`. The primal/dual gap increases by at most

`3κ+5λ+12e_round+kδ_dual+ζ_sdp/8 ≤ 0.4ζ_sdp`.

Exact rational objective comparison avoids an uncharged winner-selection error. No generic SDP solve or full net search was executed by the checkers; their role is finite identity/certificate verification. The polynomial weak-SDP existence and finite synthesis routines retain the received proof's scope.

### 5. Expected selector and genuine confidence event

The expected tomography bound and finite allocations give `m≤αe/512`; statistical and optimization contributions are each at most `e/4`. The implemented selector's output-law discrepancy contributes at most `ν_s/2` because the physical function `ell_opt(x)` lies in `[0,1]`. This proves the stated expected selection guarantee.

The optional confidence theorem is meaningful: its event is a deterministic, frame-invariant property of the exported classical encoder label. Total-variation transfer can therefore move it from the ideal common-frame analysis to the physical selector distribution. This does not claim a good decoder in every exposed record or a good realization of every subsequent bank. Confidence-scale accuracy `ν_s≤β` is explicitly charged and cannot be replaced by an accuracy merely of order `e`.

### 6. Fresh deployment and factor composition

The compressed discovery decoder is discarded. A new ordinary six-input bank is acquired for the selected encoder, then jointly reduced with the actual independent payload output. Conditional on the selected encoder this is exactly the received ordinary Bures recovery interface with rank bound `4R`. The selected encoder is reusable classical information; the physical decoder is not reusable across separately reduced future data.

The two factors multiply. The choices `α=θ=γ/3`, `e=ε/4`, and `e_d=ε/2` give `(1+γ/3)²≤1+γ` and additive error at most `5ε/6`. Both finite-implementation budgets are already included. The remaining `ε/6` is unspent rather than permission for unmodelled errors. The one-payload source bill is correctly `n_s+6n_d+1`; later payloads require fresh recovery banks unless a separate batch theorem is invoked.

### 7. Transfer/hardware boundaries are preserved

The final text explicitly retains the conditions raised during review:

- Individual anchor channel tests do not establish the relative phases of controlled anchor operations. Both checkers demonstrate this failure.
- A single-copy bound `||Γ̃−Γ||₁≤ξ` gives uniform policy-risk bias at most `2ξ`, but does not preserve rank or physical support. Arbitrarily small full-rank contamination is a counterexample.
- The actual calibration state needs its own valid rank/support bounds, and the actual deployed source needs its own valid rank bound. A uniform calibration/deployment loss-transfer premise is not a rank certificate.
- If all imperfect preparations are instead compared with an exact ideal protocol, the full copy-count-scaled preparation discrepancy must be paid.
- Finite output-law transfer of the physical optimum costs `ν_s/2`; direct transfer of the potentially four-valued calibration surrogate can cost `2ν_s`. The revised proof now distinguishes these cases explicitly.
- Ordinary qualification of a uniform transfer error of order `ε` can incur `ε⁻²` costs and physical-dimension dependence, erasing the conditional fast-query benefit. A selected-candidate holdout alone cannot establish uniform global optimality.

The equally informed coherent tomography/Gram learner and a fully known-channel unrestricted decoder benchmark receive fair treatment. No source-complexity separation, historical novelty, generic-noise scalability, or generic unframed diamond-optimality claim is made.

## Quantitative practicality guard

The explicit constants are extremely conservative. At `R=1`, `s=8`, `γ=ε=0.1`, the displayed end-to-end allocation requires:

- **91,079,201,785** coherent discovery calls;
- **9,128,499,168** fresh ordinary recovery-bank calls;
- **100,207,700,954** total source calls including one payload.

The independent checker binds this arithmetic. It is not an experimental prediction or lower bound. This result is a theoretical finite-cost bridge, not evidence of an immediately practical architecture.

## Final scope and stopping condition

The requested mathematical bridge, finite checks, independent replay, resource accounting, and explicit guard review are complete. No unresolved proof correction or authorization blocker remains. The collective circuits, arbitrary full global search, hardware qualification, and practical gate/memory engineering were neither executed nor certified. No external upload, source-proof edit, merge, or user-facing message was performed.
