# Generic low-response-support streaming recovery: two physical bridges and the remaining obstruction

2026-10-29. Author derivation; independent receiving pending. This note does **not** claim a polynomial-cost generic additive-optimal streaming decoder, a quantum advantage, or historical novelty. It isolates two implementable primitives and the optimization operation that remains missing. Existing banked information-support recovery is the strongest task-level comparator, not full ambient tomography alone.

## 1. Actual source and objective

Let N be a fixed memoryless qubit-to-D channel. The source provides fresh states `ω_a±=N((I±σ_a)/2)` and `τ=N(I/2)`, independently and on demand, including while a payload is held. Put `Δ_a=ω_a+−ω_a−`, `K=Σ_aΔ_a²`, `P=supp K`, with supplied `rank P≤d`. Trusted coherent register exchange, clean controls, source preparation, and payload holding remain paid resources.

For every TP decoder R,

`Fe(RN)=1/4+(1/8)Σ_a Tr[σ_a R(Δ_a)]`.

The received information-support packet already gives a polynomial-cost **banked** additive-optimal solution via a coherent support filter and small-support learner. Replacing it with astronomical control-word search is only a memory/time trade, not an efficiency gain over that comparator.

## 2. A genuine constant-register low-rank source factory

### 2.1 Positivity and signal bounds

Since density matrices satisfy `ω²≤ω`,

`Δ_a²=(ω_a+−ω_a−)²≤2ω_a+²+2ω_a−²≤4τ`.

Define `B_a=sin(πΔ_a/2)` and

`Ω=Σ_a B_a τ B_a`.

Every B_a is supported on P. Also

`B_a τ B_a ≥ (1/4) Δ_a² sin²(πΔ_a/2) ≥ Δ_a⁴/4`,

because `||Δ_a||≤1` and `|sin(πx/2)|≥|x|` on `[-1,1]`. The operator square identity

`Σ_a (Δ_a²−K/3)² = Σ_aΔ_a⁴−K²/3 ≥0`

therefore proves

`Ω≥K²/12`,   `supp Ω=P`.

No false noncommutative inequality such as `ΣΔ_a K Δ_a≥K²` is used. The background τ may be full rank and noncommute with every response operator.

Let `S=Tr K`. The factory success probability below obeys

`p=TrΩ/3 ≥ TrK²/36 ≥ S²/(36d)`.

Conversely the constant-output decoder already has

`Fopt−1/4≤(1/8)Σ||Δ_a||1≤√(3dS)/8`.

Thus an arbitrarily weak response is not an unpriced inverse-eigenvalue case; it can be dropped at small additive objective cost.

### 2.2 Actual operation

For one attempt:

1. Choose a uniformly from x,y,z, and acquire a fresh τ target.
2. Prepare a clean control in `|+>`.
3. Implement `exp[−i(π/2) Z_control⊗Δ_a]` using signed fresh-state collision simulation with programs `ω_a+`, `ω_a−`.
4. Measure the control in the X basis; retain the target only on the `−` outcome.

The ideal accepted Kraus operator is `−i B_a`. Forgetting a, a successful attempt returns exactly `χ=Ω/TrΩ`. This is a rank-at-most-d state on the original carrier. No support basis, complement access, transpose, source inverse, purified preparation oracle, or large-dimensional maximally entangled input is used. The simulation is a bounded-time linear Hamiltonian primitive, not QPE of K.

### 2.3 Finite same-source budget

S can be estimated from nine overlap quantities using two-copy SWAP tests:

`S=Σ_a[Trω_a+²+Trω_a−²−2Tr(ω_a+ω_a−)]`.

Set `s0=ε²/d` and estimate S to absolute error `s0/2` with failure probability β, using `O(d² ε^-4 log(1/β))` source copies. If the estimate is at most s0, returning I/2 loses at most `√(9/2) ε/8<0.27ε` on the good estimation event. Otherwise `S>s0/2`, so

`p≥p_min=ε⁴/(144d³)`.

For a requested χ program, take a fixed cap `L≥p_min^-1 log(2/δ)` attempts, with an explicit failure flag if all reject. The ideal failure probability is at most δ/2. Simulate each complete attempt to half-diamond error at most `δ/(2L)`. The finite-clock hybrid then adds at most δ/2 **before conditioning**. This yields a δ-accurate flagged χ factory, rather than an unsupported exact-rank claim about imperfect accepted outputs.

A deliberately loose linear-collision accounting costs `O(L²/δ)` original-source programs per requested χ, independent of D apart from `O(log D)`-size exchange/control operations. Calibration is additional. If n outputs are needed, their individual errors and failure budgets must be divided by n; programs are not reusable for free. Two ambient registers suffice for the factory itself, or three if an independent payload is simultaneously held. The source must remain available throughout.

### 2.4 What this does not solve

χ is a low-rank **mixed** state in an unknown support, not a supplied purification or known coordinate system. Its small nonzero eigenvalues can still obstruct exact flattening. The bound `Ω≥K²/12` permits objective-weighted weak-sector truncation, but preparing a known-basis encoding or the optimal recovery Choi program does not follow merely from obtaining χ.

## 3. An optimal adjoint-Choi program can be physically read out without a large transpose

This section proves a conditional implementation theorem: the additional input is a fresh-state factory for the required program. It does not assert that the six-state source already supplies that factory.

Let R be any CPTP map from the s-dimensional support P to a logical k-dimensional output, with k=2 here. Define its unnormalized **adjoint** Choi operator

`X=Σ_ij |i><j|_Q ⊗ R†(|i><j|)_B`,

so `X≥0`, `Tr_Q X=P`, `Tr X=s`. Suppose fresh copies of `ξ=X/s` are supplied. Prepare a known `|Φ_k>` on clean output Q and auxiliary Q', and apply the positive operator `√ξ` to Q'B. Tracing Q'B after successful filtering gives

`R(ρ)/(ks)`

for every ρ supported on P, including inputs entangled with an untouched reference. Explicitly the Stinespring columns are

`W|ψ>=(1/√k) Σ_i |i>_Q ⊗ √ξ(|i>_Q'⊗|ψ>_B)`.

Their inner products give `W†W=P/(ks)`. The desired recovery is therefore encoded with an input-independent success amplitude. No transpose of an unknown B state occurs in this factorization.

A concrete existing sample-only primitive is Proposition 18 of [Utsumi et al., arXiv:2509.03619v3](https://arxiv.org/pdf/2509.03619): it approximates a unitary block-encoding `√ξ/(2√2)` and separately its inverse using fresh copies, with no-gap cost `O~(δ^-5)` and logarithmic live quantum space. Its literal normalization makes the success probability `1/(8ks)`, hence `1/(16s)` for a qubit.

Apply fixed-point oblivious amplitude amplification using the **known** initial Bell/flag reflection tensor identity on B and the known success-flag reflection. It uses `L_A=O(√(kd) log(1/ε))` forward/inverse unitary calls for s≤d. The inverse calls are fresh-sample approximations to the inverse **ideal block-encoding unitary**, not inverses of discarded-program channels. Allocating each call error `O(ε/L_A)` gives a loose no-gap cost

`O~(L_A^6 ε^-5)=O~((kd)^3 ε^-5)`

copies of ξ. This excludes the cost of making each ξ; that cost must be multiplied in.

### Outside-support completion

The initial reflection does not require P. The good singular value is `1/√(8ks)` on P and zero on P-perp. Amplification acts uniformly on the first and leaves the second unsuccessful. After the fixed amplification schedule, measure the success flag and output a fixed logical state on failure. The limiting complete channel is

`R(PρP)+Tr(Pperp ρ) θ`.

Cross-support coherences disappear, as appropriate for the objective-specific support reduction. All simulation/amplification comparisons concern the complete channel before postselection. No full-channel closeness to the original unfiltered N is claimed.

### Required program is not the ordinary channel Choi sample

A Choi sample of N is not ξ. Nor does an ordinary Choi sample of R automatically supply its adjoint Choi sample: relating the two representations involves a swap and full transpose. The optimizer should produce X directly as a physical state. This distinction cannot be hidden under the phrase “a Choi program.”

For the qubit response objective, the direct SDP is

`maximize (1/8)Tr(CX),  X≥0, Tr_QX=P`,

`C=Σ_a σ_a^T⊗Δ_a`.

Only the known logical Pauli is transposed. C is Hermitian, not generally positive. Equivalently `C=4J_N−2I_Q⊗τ` for the normalized Choi state J_N; neither that subtraction nor partial transposition is a physical state preparation. Signed Hamiltonian simulation of C is available directly from the six-state programs.

## 4. Why the named general solvers do not yet close acquisition

### 4.1 Mixed-sample Uhlmann and Petz

In [2509.03619](https://arxiv.org/pdf/2509.03619), Theorem 17's sequential canonical purification includes an ambient dimension factor; Proposition 35's synthesized Stinespring access retains output-dimension cost. Section 10 then builds Petz with further inverse-eigenvalue/amplification costs. The useful exception is its square-root block-encoding primitive used above; the dimension-free “variant” of Uhlmann acts on specified canonical-purification relationships, not arbitrary source encodings.

Even free exact Petz is not additive-optimal in this task. For the qubit depolarizing channel with Bloch contraction λ=1/2, optimal recovery is identity and `Fopt=5/8`. Its Petz map for I/2 is N itself, giving `Fe(N²)=7/16`; the gap is `3/16`. This is already a two-dimensional, well-conditioned example. A near-optimal multiplicative guarantee such as `F_Petz≥Fopt²` does not meet arbitrary additive ε.

### 4.2 Quantum SDP input access is stronger than fresh samples

[Brandão et al., arXiv:1710.02581](https://arxiv.org/html/1710.02581), Oracles D.1–D.3, require coherently indexed trace data and purified state-preparation unitaries **and their inverses**. Its `sqrt(m)` constraint-count dependence also matters. Writing `Tr_Q X=P` in the known ambient basis introduces D² scalar constraints; writing only d² constraints in an unknown support silently supplies the missing coordinate/control oracle. Ordinary six-state samples do not instantiate these assumptions. A low-rank Gibbs subroutine alone is not a full recovery-state optimizer.

### 4.3 Physical normalization is possible locally; efficient iteration is unproved

For a candidate X and available Hermitian C, a filtered update `Y=A X A†` with `A=I+ηC` can be performed on program copies by sample Hamiltonian/block operations. Copies of its marginal are obtained by discarding Q. If a known spectral floor is enforced, another sample-functional filter can apply the inverse square root of that marginal, producing

`X_new=(I_Q⊗S^-1/2)Y(I_Q⊗S^-1/2)`, `S=Tr_QY`.

This makes one normalization operation plausible and costable, but it does not prove an efficient optimizer. In particular:

- Congruence normalization is not automatically the relative-entropy Bregman projection required for a matrix mirror-descent regret theorem.
- Copies of X_new require multiple fresh copies of X. If X is supplied by recursively regenerating earlier updates, factory cost obeys `C_t ≳ m_t C_(t−1)` for that implementation. A polynomial number of matrix iterations can thus cost exponentially many original-source calls. This is a diagnosis of the naive construction, not an impossibility theorem for every algorithm.
- Keeping a population of previous quantum iterates can avoid recomputation but reintroduces a quantum bank; extracting a full classical matrix avoids it differently but is excluded here.
- Approximate marginal feasibility must be repaired and priced before applying Section 3; an objective value or abstract SDP witness is not an executable program.

The conventional comparator is already globally convergent under suitable initialization: [Ru et al., arXiv:2609.40203v1](https://arxiv.org/html/2609.40203) proves generalized Reimpell–Werner convergence from positive-definite inputs and per-fixed-instance asymptotic iteration bounds. Those results operate on explicit matrices; they do not supply a bounded-cost sample factory for every iterate. Their existence prevents presenting ordinary local-search avoidance as the new capability.

## 5. Efficient-capability verdict

The two concrete advances here are (i) a same-source, constant-register response-support state factory, and (ii) a physical readout of a supplied feasible adjoint-Choi state with polynomial overhead and no ambient transpose. Neither establishes acquisition of that near-optimal state with polynomial total source/control cost.

Consequently there is presently **no proved generic polynomial-cost constant-carrier-memory additive-optimal recovery theorem in this note**. The strong existing banked learner remains better than an astronomical control search on total acquisition/control cost. A consequential next result would need an efficient original-source factory for globally optimized feasible X, or a different direct protocol with a comparable end-to-end guarantee. No support-basis, purification, inverse, or continuing-source cost may be supplied by an unnamed oracle.

The anti-symmetrization paper [Watts et al., arXiv:2610.06737v1](https://arxiv.org/html/2610.06737v1) gives a useful support program, but its streaming memory is `O(d log D)` for rank d, not a constant number of carriers independent of d. Its support-state output is not free known-basis extraction. It may improve the bank architecture, but it does not by itself remove the stated optimization bottleneck.

## 6. Tests and limits

`check_constructions.py` / `.json` passed all nine records: three noncentral low-support channels mixed with full-rank backgrounds verify `Ω≥K²/12`, rank, and success bounds; three random CPTP recoveries verify adjoint-Choi factorization; two numerical Lie-closure checks support the separately developed control lemma; a depolarizing example records the Petz gap. These are sanity checks, not substitutes for the proofs or an implemented optimizer. The Lie test is not a novelty claim; accessor controllability has established literature.
