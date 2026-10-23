# Independent review: exact normal separable initialization

Reviewer: `exact_initializer_review`, a fresh internal reviewer for the B2 R1 consolidation.

Date: 21 October 2026. Status: **the supplied exact-initializer argument survives this analytic review**, subject to precisely the model below. This is an internal mathematical assessment, not external certification or a priority determination. No numerical checks are used to establish this result.

## 1. Materials and scope

Read in full:

- `handoff/Astra_Agent_Assignments_20261021/seeds/R1_MODEL_AND_PROOF.txt`;
- `handoff/Astra_Agent_Assignments_20261021/sources/exact_initializer.txt`;
- `handoff/Astra_Agent_Assignments_20261021/protocol/AGENT_HANDOFF.txt`.

The first is the inherited proof reconstruction. The second is a transcript containing a substantial proof, not the producer's original TeX/PDF archive. The review below reconstructs the full argument from those supplied claims and checks its load-bearing infinite-dimensional steps directly.

Alice and Bob have finite-dimensional external ports. Their retained memory is the normal trace-class state space on a fixed separable Hilbert tensor product `C_A ⊗ C_B`. The device `Λ` is a fixed normal CPTP map implemented by a finite-round, finite-outcome LOCC protocol. Every outcome is included and all retained shared registers are counted as memory. A faithful product reference input `η=η_A⊗η_B` defines

\[
\Phi(\xi)=\operatorname{Tr}_{\rm out}\Lambda(\eta\otimes\xi).
\]

The complete external causal process after `n` calls from initializer `ξ` is `P_n^ξ`. Its distance is normalized as a full trace-norm strategy distance: any complete tester, including coherent/adaptive reference-assisted testers, is a CPTP experiment on `ξ`, and therefore

\[
\operatorname{dist}_{\rm str}(P_n^\alpha,P_n^\beta)
\leq \|\alpha-\beta\|_1. \tag{1}
\]

This estimate has constant one independent of `n`. If half-trace strategy distance is used, its left side is divided by two; one must not transfer constants unchanged.

`SEP` denotes the trace-norm closed convex hull of normal product states. All logarithms are natural. Define

\[
E_R(\rho)=\inf_{\gamma\in\mathrm{SEP}}D(\rho\Vert\gamma).
\]

## 2. The theorem that survives

**Exact common initializer theorem.** If a normal memory state `τ` is trace-norm recurrent under the reference channel,

\[
\liminf_{t\to\infty,\ t\in\mathbb N}\|\Phi^t(\tau)-\tau\|_1=0,
\]

then there exists one normal separable density operator `γ` on the original spaces `C_A⊗C_B` such that

\[
P_n^\gamma=P_n^\tau\qquad\text{for every finite }n\geq1. \tag{2}
\]

No finiteness of `E_R(τ)`, local entropy or energy is assumed. The device is unchanged. The conclusion concerns the complete causal processes, not merely separate output marginals or the particular reference-input experiment. It does not assert that `τ` is separable, that `γ` is stationary, or that `γ` has a finite preparation protocol.

The essential extra result is a compactness lemma for specifically chosen relative-entropy near-minimizers. Arbitrary normal separable approximating initializers would not automatically have a trace-norm convergent subsequence.

## 3. A no-escape lemma for separable near-minimizers

**Lemma.** Suppose `ρ_k→ρ` in trace norm, each `E_R(ρ_k)<∞`, and normal separable states `γ_k` satisfy

\[
D(\rho_k\Vert\gamma_k)\leq E_R(\rho_k)+\zeta_k<\infty,
\qquad \zeta_k\to0.
\tag{3}
\]

Then `{γ_k}` is relatively compact in trace norm. In particular it has a subsequence whose limit is a normal separable trace-one state. There is no uniform bound on `E_R(ρ_k)` in this assertion.

### 3.1 Four sectors are needed to preserve separability

Fix one pair `ρ,γ` satisfying (3) with slack `ζ`. Let `P_A,P_B` be finite-rank local orthogonal projections. Form the four mutually orthogonal product projections

\[
Q_{ab}=P_A^{(a)}\otimes P_B^{(b)},\quad
P_A^{(0)}=P_A,\quad P_A^{(1)}=I-P_A,
\]

and similarly for Bob. Index them by `i=1,…,4`, put

\[
\Delta(X)=\sum_iQ_iXQ_i,\quad
p_i=\operatorname{Tr}Q_i\rho,\quad q_i=\operatorname{Tr}Q_i\gamma.
\]

Whenever `p_i>0`, finite `D(ρ‖γ)` implies `q_i>0`. Set `ρ_i=Q_iρQ_i/p_i` and `γ_i=Q_iγQ_i/q_i` on these sectors. Every `γ_i` is normal and separable: continuous local filtering preserves the trace-norm closed cone of separable positive operators. This does not assume a countable product decomposition of `γ`.

Using one main projection `P_A⊗P_B` and its entire complementary projection as a two-sector *local* instrument would be unjustified: the complementary projector is not generally a product projector. Resolving all four product sectors avoids that problem.

Relative-entropy monotonicity and the finite direct-sum formula give

\[
D(\rho\Vert\gamma)\geq D(\Delta\rho\Vert\Delta\gamma)
=D(p\Vert q)+T,
\quad T=\sum_{i:p_i>0}p_iD(\rho_i\Vert\gamma_i).
\tag{4}
\]

In particular `T<∞`. Define the comparison state

\[
\widehat\gamma=\sum_{i:p_i>0}p_i\gamma_i\in\mathrm{SEP}.
\tag{5}
\]

All positive-probability sectors are retained. This comparison object is not a postselected output and is not inserted into the device.

### 3.2 Pinching identity without an entropy subtraction

For a finite pinching and any state `σ` that is block diagonal under it,

\[
D(\rho\Vert\sigma)
=D(\rho\Vert\Delta\rho)+D(\Delta\rho\Vert\sigma).
\tag{6}
\]

One rigorous derivation uses a finite phase twirl. Relabel the four sectors by `a=0,1,2,3` and put
`U=Σ_{a=0}^{3} exp(2πia/4)Q_a`, where `i` in the exponential is the imaginary unit. Then
`Δρ=(1/4)Σ_{j=0}^{3}U^jρU^{-j}`. Apply Donald's identity to this finite ensemble and the block-diagonal comparison state `σ`. Each ensemble term has the same divergence to `σ` and to `Δρ`, by unitary invariance. This proves (6) as an identity of extended nonnegative quantities. It uses neither `S(ρ)<∞` nor subtraction of infinite entropies.

For completeness the first term obeys

\[
D(\rho\Vert\Delta\rho)\leq H(p).
\tag{7}
\]

To prove (7), purify `ρ`. The four projected purification vectors are orthogonal and have squared norms `p_i`. The relative entropy from the original pure state to their mixture is exactly `H(p)`. Tracing out the purifying system gives (7) by data processing. This proof also avoids infinite entropy differences.

For `σ=γ̂`, the direct-sum term in (6) is exactly `T`, so

\[
D(\rho\Vert\widehat\gamma)=D(\rho\Vert\Delta\rho)+T<\infty.
\tag{8}
\]

Combining (3), (4), and admissibility of (5),

\[
D(p\Vert q)+T
\leq D(\rho\Vert\gamma)
\leq E_R(\rho)+\zeta
\leq D(\rho\Vert\widehat\gamma)+\zeta
=D(\rho\Vert\Delta\rho)+T+\zeta.
\]

Canceling the **already proved finite** quantity `T` gives

\[
\boxed{D(p\Vert q)\leq H(p)+\zeta.} \tag{9}
\]

This is the crucial inequality. Its right side does not contain `E_R(ρ)`.

### 3.3 An explicit tail bound

Let `P=P_A⊗P_B` and `δ=1−Tr(Pρ)`, so the main-sector probability is `1−δ`. The other three sectors have total probability `δ`, whence

\[
H(p)\leq h_2(\delta)+\delta\ln3.
\]

Classical Pinsker in nats is `D(p‖q)≥(1/2)‖p−q‖_1²`. The probability difference of one event is at most half the full ℓ1 distance. Consequently

\[
\boxed{
1-\operatorname{Tr}(P\gamma)
\leq\delta+
\sqrt{\frac{h_2(\delta)+\delta\ln3+\zeta}{2}}.
}
\tag{10}
\]

No factor of two is missing here. If the source projection tail is zero and the near-optimality slack vanishes, the comparison state cannot put any positive probability outside the source's local product subspace.

### 3.4 From the tail estimate to trace-norm compactness

Choose increasing finite-rank local exhaustions `P_{A,m}↑I`, `P_{B,m}↑I` and let `P_m=P_{A,m}⊗P_{B,m}`. Normality of `ρ` implies `δ_m=1−Tr(P_mρ)→0`. For each fixed `m`, trace-norm convergence gives

\[
1-\operatorname{Tr}(P_m\rho_k)\to\delta_m.
\]

Applying (10) and taking a limit superior in `k`, then letting `m→∞`, gives arbitrarily small eventual tails for `γ_k`. Each finite initial exceptional collection consists of normal states, so increasing `m` captures its tails as well. Thus

\[
\lim_{m\to\infty}\sup_k\left[1-\operatorname{Tr}(P_m\gamma_k)\right]=0.
\tag{11}
\]

The gentle compression bound

\[
\|\omega-P\omega P\|_1\leq2\sqrt{1-\operatorname{Tr}(P\omega)}
\tag{12}
\]

holds for every state and projection. It follows, for example, first for a purification and then by taking the partial trace. For fixed `m`, the compressed positive operators `P_mγ_kP_m` belong to a bounded subset of a finite-dimensional vector space, hence a relatively compact set. Equations (11)–(12) give uniform approximation by those compact sets. Therefore `{γ_k}` is totally bounded in the complete trace-class norm, proving the lemma. A norm limit is positive with trace one; the definition of `SEP` makes it separable. This proves normality and prevents mass loss explicitly.

## 4. Reconstructing the recurrent-state sequence

Every normal state `τ` has normalized local finite-support approximants `σ_k` with

\[
\|\sigma_k-\tau\|_1\leq1/k,
\qquad E_R(\sigma_k)<\infty.
\tag{13}
\]

For example compress to sufficiently large `P_{A,m}⊗P_{B,m}` and normalize. A product maximally mixed comparison on the finite local supports gives a finite relative-entropy upper bound.

For fixed `k`, define

\[
r_{k,t}=E_R(\Phi^t(\sigma_k)).
\]

Because `Φ` is LOCC after feeding a separable product input and discarding outputs, these are finite, nonnegative, and nonincreasing in `t`. Every such sequence converges. Hence for sufficiently late `t`,

\[
r_{k,t}-r_{k,t+k}\leq1/k.
\]

Recurrence provides arbitrarily large times satisfying `‖Φ^t(τ)−τ‖_1≤1/k`; choose one beyond that threshold and call it `t_k`. Put

\[
\rho_k=\Phi^{t_k}(\sigma_k).
\]

Contractivity yields

\[
\|\rho_k-\tau\|_1\leq2/k,
\quad
E_R(\rho_k)-E_R(\Phi^k(\rho_k))\leq1/k.
\tag{14}
\]

Select `γ_k∈SEP` with

\[
D(\rho_k\Vert\gamma_k)\leq E_R(\rho_k)+1/k<\infty.
\tag{15}
\]

Only existence of a near-minimizer of a finite infimum is needed; an exact closest-state theorem is unnecessary in this construction.

## 5. Why one sequence approximates the complete causal process

Finite-dimensional external ports and a faithful product input permit a finite informationally complete product ensemble averaging exactly to `η`, followed by local informationally complete output measurements at every slot. For example conjugating a spanning collection of rank-one preparations by `η_A^{1/2}` and `η_B^{1/2}` preserves its span because faithfulness makes these maps invertible. The preparation probabilities can be chosen to average to `η`.

Keep all preparation and measurement labels. The resulting `n`-slot instrument has a finite classical transcript law `p_n^ξ`; forgetting its labels leaves `Φ^n(ξ)` on memory. Each conditional memory operation preserves separability. The product spanning preparations and output effects determine the finite-dimensional process Choi operator, including all its temporal correlations. A complete comb/process equality follows, so every finite-horizon strategy norm has a finite reconstruction constant `K_n` with

\[
\operatorname{dist}_{\rm str}(P_n^\alpha,P_n^\beta)
\leq K_n\|p_n^\alpha-p_n^\beta\|_1.
\tag{16}
\]

This informational completeness is the reason the result is about all external input strategies and reference systems, even though recurrence itself uses just the one faithful reference input.

Apply the transcript-and-memory instrument to `ρ_k,γ_k`. Relative-entropy data processing and the classical/quantum chain rule imply

\[
D(\rho_k\Vert\gamma_k)
\geq D(p_n^{\rho_k}\Vert p_n^{\gamma_k})
 +\sum_y p_yD(\rho_{k,y}\Vert\gamma_{k,y})
\geq D(p_n^{\rho_k}\Vert p_n^{\gamma_k})
 +E_R(\Phi^n(\rho_k)).
\tag{17}
\]

Every subtraction now involves finite resource values. For `n≤k`, (14)–(15) and monotonicity give

\[
D(p_n^{\rho_k}\Vert p_n^{\gamma_k})\leq2/k,
\quad
\|p_n^{\rho_k}-p_n^{\gamma_k}\|_1\leq2/\sqrt{k}.
\]

Together with (1), (14), and (16),

\[
\operatorname{dist}_{\rm str}(P_n^\tau,P_n^{\gamma_k})
\leq\frac{2}{k}+\frac{2K_n}{\sqrt{k}}
\qquad (n\leq k).
\tag{18}
\]

No uniform estimate on `K_n` is assumed or needed.

## 6. One normal initializer, every horizon, unchanged device

By (14)–(15), the tightness lemma applies to this **same** near-minimizing sequence. Take a single trace-norm convergent subsequence `γ_{k_j}→γ∈SEP`. It is selected in the original memory state space, once, without reference to a horizon. For any fixed `n`, eventually `k_j≥n`; hence

\[
\operatorname{dist}_{\rm str}(P_n^\tau,P_n^\gamma)
\leq \frac{2}{k_j}+\frac{2K_n}{\sqrt{k_j}}
 +\|\gamma_{k_j}-\gamma\|_1\to0.
\tag{19}
\]

This proves (2). There is no exchange of an uncontrolled supremum in `n` with the limit. The sequence is chosen once and each finite `n` is then treated as arbitrary. The projections, pinching, and reweighting in the compactness proof are comparison objects only; `Λ` is not altered.

**Additional consequence.** The original near-minimizer sequence satisfies

\[
\sup_{n\geq1}\operatorname{dist}_{\rm str}(P_n^{\gamma_k},P_n^\tau)\to0.
\tag{20}
\]

If this failed, a subsequence would have a positive supremum error. Relative compactness would yield a further subsequence converging in trace norm to `γ_*`. Equation (19) shows that `γ_*` matches every finite horizon exactly. Equation (1), uniformly in `n`, then bounds the purported positive supremum by `‖γ_k−γ_*‖_1→0`, a contradiction. This supplies no computable rate, and it does not make the later dynamics finite dimensional.

## 7. Adversarial checks and scope restrictions

1. **No hidden `∞−∞`.** For each `k`, (15) is finite. Equation (4) therefore proves `T<∞` before cancellation. None of the argument evaluates a difference of infinite entanglement values at the limiting state `τ`.
2. **Zero-probability sectors.** Terms with `p_i=0` are omitted from (5) and contribute zero to `T`. Terms with `p_i>0,q_i=0` are excluded by finite relative entropy. A state with a zero projection block has no off-diagonal coupling to that block by positivity; no unsupported source component is introduced by dropping zero-weight sectors.
3. **Normality is essential.** `ρ_k→τ` in trace norm gives a normal source limit whose finite product projections capture its mass. A singular limiting functional would not satisfy the tail argument.
4. **Ordinary boundedness is insufficient.** Trace-one positive operators are not trace-norm compact in infinite dimension. Equation (11), not mere boundedness or Banach–Alaoglu alone, is what makes the conclusion valid.
5. **The separable cone rather than a countable decomposition is used.** Local filtering, finite convex mixing and trace-norm closure suffice; non-countably decomposable normal separable states are allowed.
6. **There is one initializer.** A different `γ_n` for each horizon would be strictly weaker. A single subsequence of the common sequence gives the same `γ` for all `n`.
7. **The device is unchanged.** No local truncation is inserted into `Λ`. The comparison projections are not a modified simulation algorithm.
8. **All histories are included.** The tomography and data-processing steps use complete outcome distributions, not success-conditioned branches. Finite-round/finitely many outcomes ensure a finite instrument tree at fixed horizon.
9. **Nonfaithful reference input is outside this conclusion.** A nonfaithful input can fail to probe directions of the external process. The full-rank conjugation establishing a spanning preparation ensemble would fail.
10. **Fixed error is not recurrence.** A fixed `‖Φ(τ)−τ‖_1≤ε>0` does not produce the arbitrarily accurate late returns used in (14).
11. **Separable initialization is an existence statement.** `γ` need not be a finite mixture or finitely preparable state. The theorem does not provide an efficient initializer, a finite memory bound, or uniform finite-dimensional implementation of the fixed dynamics.
12. **No external certification.** This reviewer has reconstructed the argument, but neither internal agreement nor repeated finite checks proves historical originality or substitutes for external mathematical scrutiny.

## 8. Primary-literature boundary

The following primary sources were inspected directly on 21 October 2026:

- Ludovico Lami and Maksim E. Shirokov, *Attainability and Lower Semi-continuity of the Relative Entropy of Entanglement and Variations on the Theme*, Annales Henri Poincaré **24** (2023), 4069–4137, DOI `10.1007/s00023-023-01313-1`; full text <https://link.springer.com/article/10.1007/s00023-023-01313-1>; preprint <https://arxiv.org/abs/2105.08091>. Relevant locations: Theorem 5(a)–(d), Proposition 18, Remark 19, Corollaries 20 and 22. The paper establishes closest-state attainability/lower semicontinuity and compactness for a finite resource value. Proposition 18 and Remark 19 concern source sequences whose resource values converge to a finite limiting value. These conditions do not directly cover the divergent-resource sequence used here. When the resource value itself is infinite, attainment alone is vacuous for extracting equality in an entropy-drop argument.
- M. E. Shirokov, *Lower semicontinuity of relative entropy disturbance and its consequences*, Sbornik: Mathematics **215**(11) (2024), 1549–1581, DOI `10.4213/sm10107e`; full text <https://www.mathnet.ru/php/archive.phtml?jrnid=sm&option_lang=eng&paperid=10107&wshow=paper>. Equation (2.19) states Donald's identity for positive trace-class operators, without finite-entropy assumptions; the finite-ensemble version follows by iteration. Equation (2.18) gives the orthogonal direct-sum identity. These are established tools used in (4) and (6).

The countable local-exhaustion method is standard, as is the gentle compression estimate. The inherited seed supplies the finite informationally complete instrument and the resource-drop construction of the common sequence. The extra internally established step in the exact-initializer branch is the separability-preserving block reweighting estimate (9)–(10) and its use when `E_R(ρ_k)` has no uniform bound. This bounded search did not establish historical priority for that lemma or for the complete recurrent-process theorem. The claim should therefore be described as an internally reconstructed theorem with a credible new strengthening, pending a dedicated priority check.

## 9. Recommendation

Close the exact-initializer existence question affirmatively in the stated model and integrate this proof once. The stronger quantifier and operation are substantive: one normal separable initializer on the same memory spaces reproduces every finite causal process of the unchanged device, including the case of infinite initial relative-entropy entanglement.

Do not allocate another foundational branch merely to re-prove compactness, improve `K_n`, or convert this existence theorem into an unsupported efficient implementation claim. Further investment would need a specified unresolved operation, such as an effective simulator with quantified resource restrictions, and evidence that those restrictions describe an important task. No such computational or physical capability follows from this proof alone.
