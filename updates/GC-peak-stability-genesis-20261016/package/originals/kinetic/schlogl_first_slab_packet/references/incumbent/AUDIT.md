# Vo–Sidje certified-tensor incumbent audit

Audit date: 2026-10-16. Scope: primary texts and read-only inspection of public dependency source. No solver implemented, author code executed, models downloaded, or change made to the eight-site problem.

## Decision

**There is a genuine physical L1 a-posteriori internal-error bound in Vo–Sidje (2017), beyond its FSP leakage bound. It can include tensor truncation through the residual of the final stored tensor. However, this audit did not establish an existing end-to-end implementation that computes a rigorous, affordable full-L1 certificate, including rounding, at the requested ~1e-9 interior accuracy.**

The useful overlooked ingredient is an endpoint-only discrete residual certificate for a uniformization block. It avoids continuous-time residual quadrature. It does not turn an AMEn tolerance, a mass-conservation check, or an approximately maximal exit rate into a certificate. Availability of the algebraic AMEn building blocks is verified; availability of the paper's complete driver and a certified L1 verifier is not.

## Primary-paper facts

### Vo–Sidje 2017

[Journal DOI](https://doi.org/10.1063/1.4994917); [author-uploaded full text](https://www.researchgate.net/publication/318233496_An_adaptive_solution_to_the_chemical_master_equation_using_tensors).

The full text identifies Sidje as its uploader. Relevant locations: Theorem IV.2, Eqs. (16)–(17), (21)–(30), Algorithm 2, Section VII.

Assumptions: separable propensities; finite conservative generator; probability initial data; certified θ≥max_i(−A_ii). Let π_k=e^(−θτ)(θτ)^k/k! and S be the lower shift.

- (21) P=I+A/θ.
- (22), (23): w_m=Σ_(k=0)^m π_k P^k v; 1−Σπ_k≤Tol_unif·τ/t_f.
- (27): (I−S⊗P)f=e_0⊗v.
- (29): ŵ_m=Σπ_k f̂_k.
- (30): ŵ_m−w_m=Σ_(k=0)^m π_k Σ_(j=0)^k P^(k−j)r_j, where r=(I−S⊗P)f̂−e_0⊗v.
- Immediately afterward: ||ŵ_m−w_m||_1≤Σ_j||r_j||_1=||r||_1.

The independent FSP theorem assumes initial support inside H and exact boundary-absorbed probabilities p̄. It gives ||p−p̄||_1≤Σ_s e_s, e_s=2Σ_(i=1)^(ν_max^(s)) p̄^(s)(I_s−i).

Experiments use (ε_FSP,Tol_unif,Tol_AMEn)=(1e−4,1e−4,1e−5), TT-Toolbox 2.2 and Fortran AMEn. The rate parameter is estimated using tt_max. Step counts use ceil(θ·remaining_time/ω), with ω=10 or 100.

### Sidje–Burrage–MacNamara 2007

[Journal DOI](https://doi.org/10.1137/060662629); [author-uploaded full text](https://www.researchgate.net/publication/43475037_Inexact_Uniformization_Method_for_Computing_Transient_Distributions_of_Markov_Chains).

This is reference 31 of the 2017 paper. Theorem 3.1, Eqs. (8)–(9), derives the same accumulation bound for inexact products P f̂_(k−1)=f̂_k+ε_k, with exact starting vector: ||w−ŵ||_1≤Σ_k||ε_k||_1. Here w is the truncated uniformization approximation; Poisson truncation remains separate. Its practical relaxation selects generator columns using an ε-support. Section 3.2 bounds each skipped-column error by 2ε times the skipped support size; Theorem 3.3 consequently gives a coarse 2nℓε bound. This is an explicitly counted sparse-state mechanism, not a compressed-TT L1 evaluator. Section 3.3 also uses an approximate stationarity test. Neither that test nor unbudgeted early stopping should be imported into a rigorous finite-horizon certificate.

## What the public dependency actually checks

These are current repository sources, not a reconstructed/pinned 2017 executable.

- [tt_max.m](https://github.com/oseledets/TT-Toolbox/blob/master/core/tt_max.m) calls tt_max_abs and returns the tensor value at its selected multi-index. Its own description says the maximum is approximate. Thus its output is not a proved upper bound on every exit rate. For this Schlogl problem, an analytic maximum or analytic conservative upper bound from the exact rates can replace it. Excessively large θ increases work; underestimated θ invalidates stochasticity and the stated contractivity proof.
- [fort_amen_solve.m](https://github.com/oseledets/TT-Toolbox/blob/master/fmex/fort_amen_solve.m) defaults to residual truncation, 10 sweeps, kickrank 4, and returns only the tensor. It passes the tolerance to [fort_amen_solve_mex.F90](https://github.com/oseledets/TT-Toolbox/blob/master/fmex/fort_amen_solve_mex.F90), which dispatches to dtt_amen_solve.
- [ttamen.f90](https://github.com/oseledets/tt-fort/blob/master/ttamen.f90), dtt_amen_solve, computes local projected relative residuals using BLAS dnrm2. Its res_max is the maximum of those local ratios. Stopping uses res_max<tol or, with Frobenius truncation, a relative core-update criterion. Sweeps are bounded by nswp. These are Euclidean/local quantities, not the complete physical L1 norm of Eq. (30). The residual-enrichment tensor is also low-rank compressed.
- [amen_solve2.m](https://github.com/oseledets/TT-Toolbox/blob/master/solve/amen_solve2.m) independently confirms the distinction: local norm(B*sol−rhs)/norm(rhs), and either SVD/Frobenius truncation or local projected residual truncation. A projected residual may miss directions outside the current spatial basis.

The public [TT-Toolbox](https://github.com/oseledets/TT-Toolbox) and [tt-fort](https://github.com/oseledets/tt-fort) provide the relevant building blocks. Targeted title/DOI/author searches and the visible [Huy D. Vo profile](https://github.com/voduchuy) did not reveal a verified complete 2017 uniformization/FSP driver. That is an acquisition gap, not proof that no such code exists. The publisher route was not readable in this audit; author-uploaded text was readable. No review or third-party performance claim was used to validate the mathematics.

## Independent deductions: how a complete certificate would work

The following are direct algebraic deductions for the unchanged finite augmented generator, not assertions that the cited implementation already performs these checks.

### 1. A slightly sharper endpoint residual bound

For c_j=Σ_(k=j)^m π_k, exchanging the finite sums yields

E_block ≤ Σ_(j=0)^m c_j ||r_j||_1 ≤ ||r||_1.

All c_j lie in [0,1]. Late power-recurrence residuals can therefore receive smaller weights than the paper's coarse bound. No positivity of f̂ is required: contractivity belongs to the exact P, not to the approximation. This is important because ordinary TT rounding and AMEn do not enforce entrywise nonnegativity.

Let B_m=Σπ_kP^k, s_m=Σπ_k and Q_m=1−s_m. Let x_l be the exact probability state at step l, and let x̂_l be the computed state. If the computed outgoing vector differs from Σπ_k f̂_k by at most η_l in L1, then

E_(l+1) ≤ s_m E_l + Q_m + Σ_j c_j||r_j||_1 + η_l.

Reason: subtract B_m x_l, use ||B_m||_1=s_m, and bound the positive omitted Poisson tail applied to x_l by Q_m. Hence a safe global bound is

E_K ≤ E_0 + Σ_l[Q_m(l) + Σ_j c_(l,j)||r_(l,j)||_1 + η_l].

This form remains valid for signed computed incoming states because the tail acts on the exact probability state in the proof. For a standalone comparison against a signed operand v instead, the local tail bound is Q_m||v||_1.

### 2. Exactly where tensor rounding is included

Any rank truncations, inaccurate local solves, and tensor arithmetic used to produce the final f̂ are included automatically **if r is evaluated against the exact intended P and actual incoming x̂_l**. One need not sum every internal truncation separately in that case.

They are not included when the verifier uses an independently rounded residual without bounding what was discarded. Likewise, rounding the final contracted output, approximate Poisson weights, approximate initial data, and operator representation errors need explicit accounting.

If the solver uses P̃ and its residual is r̃_j=f̂_j−P̃f̂_(j−1), then

r_j=r̃_j+(P̃−P)f̂_(j−1),

so a valid extra charge is ||(P̃−P)f̂_(j−1)||_1, or the coarser ||P̃−P||_1||f̂_(j−1)||_1. For approximate weights π̃_k, charge Σ_k|π̃_k−π_k|·||f̂_k||_1. Floating-point contractions and tail calculations need outward error bounds, not only double-precision residual displays.

### 3. Why the norm is the hard part

A physical L1 residual is the sum of absolute entries of the entire state-by-power tensor. It is not its signed sum, not a marginal sum, not the L2 norm of TT cores, and not a sampled or projected residual. A cheap TT contraction yields a signed sum; cancellation prevents treating that as L1.

Even granting a rigorously evaluated global Frobenius residual, the universal conversion is

||r||_1 ≤ sqrt(n(m+1))||r||_2.

For the unpadded eight-site grid:

n=163^8=498,311,414,318,121,121;
sqrt(n)=163^4=705,911,761.

The two scalar sinks change that factor negligibly. A 1e−9 L1 budget would require a one-power L2 residual at most 1.4166e−18 under the generic conversion; the stacked-block allowance is smaller by sqrt(m+1), and multiple slabs divide the budget further. Zero-padding every site to 256 raises the naive factor to 256^4=4,294,967,296 unless the verifier proves that padded residual entries vanish. These numbers do not prove impossibility: they show why a nominal 1e−9 or 1e−12 AMEn tolerance is insufficient evidence.

A nonnegative TT envelope gives a computable upper bound: if r(i)=R_1(i_1)…R_d(i_d), then |r(i)|≤|R_1(i_1)|…|R_d(i_d)|, whose sum is contractible. It can be extremely loose because it destroys gauge cancellations. A strictly positive normalized weight q offers the alternative

||r||_1 ≤ (Σ_i r_i²/q_i)^(1/2), provided Σ_i q_i=1.

Obtaining a rigorous, tight weighted contraction is additional verifier work. These observations make the existing weighted-metric repair relevant; the paper does not make that need disappear.

### 4. Positivity and mass are separate

For a nonnegative stochastic P, exact powers P^k v are nonnegative probability vectors. The finite Poisson sum has mass s_m≤1. Inexact TT powers can have negative entries even when their signed sum is one.

The sparse-column relaxation in the 2007 predecessor has a useful structural property: replacing a selected column of P by the corresponding identity column leaves a nonnegative stochastic matrix, assuming θ bounds every exit rate. This proves positivity and mass conservation of that particular exact-arithmetic step. It does not transfer to a generic AMEn tensor approximation.

Even a genuinely nonnegative mass-one vector may be far from the desired distribution. A mass check cannot certify an approximately 3.8e−8 first-hit probability, and does not refute the reported ≥0.069 state-L1 diagnostic error.

### 5. Preserve the first-hit system and separate overflow

Apply the algebraic certificate to the existing 0–162 augmented process with separate success and overflow sinks. The success coordinate at T=1 is already the first-hit output; no continuous trajectory is needed solely to recover that coordinate.

Do not replace the current departure-to-overflow construction by freezing the highest in-grid layer, reflecting reactions, or enlarging the physical cap to a power of two. Padding for QTT must be a storage embedding with inaccessible dummy states. The paper's boundary-absorbed FSP theorem concerns a different finite process and assumes exact probabilities; evaluating its marginal formula on a signed approximate tensor does not establish leakage.

For the current task, keep the supplied independent overflow/event-error allowance 7.57e−10 and add the certified interior endpoint allowance once. A success-coordinate error is bounded by full-state L1. A factor 1/2 needs separately proved equal total masses and must not be assumed after Poisson truncation or rounding. No overflow constant was recomputed in this audit.

## Cost and acquisition conclusion

The block has n(m+1) physical entries but may have a compact state-by-power TT representation. That compactness, AMEn convergence, and the ranks needed at 1e−9 physical accuracy remain empirical for this problem. A small MPO rank does not imply small solution/residual ranks. Uniformization also retains dependence on the maximum exit rate through the number of slabs or power degree; there is no demonstrated stiffness-independent certificate here.

For a fixed power cap m and maximum candidate ranks, one can bound storage and algebraic work. Certification can nevertheless dominate: exact residual formation multiplies operator and solution ranks, while taking absolute values is not automatically rank-preserving. Local dense solves also grow rapidly with adjacent TT ranks. No justified runtime estimate for this eight-site target follows from the cited examples.

**Recommendation:** retain this as a mathematically valid alternative certificate interface and candidate-generation incumbent, not as evidence that the target has been solved or that switching solvers will meet the budget. An executable route would require (1) verified exact augmented generator and θ bound, (2) a state-by-power block approximation, (3) a rigorous full physical residual-norm bound, (4) Poisson/output-rounding accounting, and (5) cumulative error below the remaining budget. Steps (3)–(5) are the material gap. The ongoing weighted verifier repair remains justified.

## 2026-10-16 addendum: exact same-model uniformization parameter and Poisson degree

This specialization resolves the general `tt_max` concern for the **unchanged** eight-site cap-162 Schlogl model. It does not resolve residual-norm or tensor-accuracy questions. Only scalar integer/rational arithmetic was executed.

The existing model files specify

b(n)=2.676 n(n−1)+108.102,
a(n)=0.040 n(n−1)(n−2)+37.881 n,
d=8.2207.

Model cross-checks: `kinetic_conservative_slab/candidate.json` and `/workspace/shared/kinetic_inside/test_overwritten_dual.py`. All terminating decimal constants above are treated as exact rationals. For integer n≥0,

b(n+1)−b(n)=5.352n≥0,
a(n+1)−a(n)=0.120n(n−1)+37.881>0.

For a nonfrozen grid state, the full exit rate, including transitions to overflow, is

λ(n)=Σ_(i=1)^8[b(n_i)+a(n_i)] + dΣ_{undirected edges {i,j}}(n_i+n_j).

The ten-edge open 2×4 graph has twenty directed hopping channels. Every term is nondecreasing in every count, so the maximum occurs at all162. That state is outside the frozen target; freezing target columns or absorbing sink columns cannot increase the maximum. Importantly, jumps that overflow are retained in this diagonal count, not suppressed.

Exact arithmetic gives:

- b(162)=34,951,767/500=69,903.534.
- a(162)=86,530,761/500=173,061.522.
- 20d·162=6,658,767/250=26,635.068.
- θ=8[b(162)+a(162)]+20d·162=492,588,879/250=1,970,355.516.
- The integer θ_up=1,970,356 is also safe.

At h=1/10,000, the exact Poisson mean is μ=492,588,879/2,500,000=197.0355516. For the integer-ceiling rate it is μ_up=197.0356.

### A purely rational Chernoff certificate

Let N be Poisson(μ), and k=m+1>μ. Markov's inequality applied to (k/μ)^N yields

Pr(N≥k)≤exp(k−μ)(μ/k)^k.

A rational upper bound for e follows directly from its factorial series:

e < 8/3 + (1/24)Σ_(l=0)^∞5^(−l) = 8/3+5/96 = 87/32.

Because μ>197 and k is an integer, a sufficient rational bound is

B_k=(87/32)^(k−197)·[492,588,879/(2,500,000k)]^k.

The following comparisons were verified by Python standard-library `Fraction`, hence integer cross multiplication, with no floating CDF or floating exponential in the proof:

- For k=316, B_k < 733/10^16 = 7.33e−14 < 1e−13. Thus **m=315** suffices for a per-slab Poisson truncation allowance of 1e−13. The preceding k=315 fails this particular conservative bound.
- For k=321, B_k < 665/10^17 = 6.65e−15 < 1e−14. Thus **m=320** suffices for a per-slab allowance of 1e−14. The preceding k=320 fails this bound.
- Both degrees and displayed rational upper bounds remain valid using θ_up=1,970,356.

Diagnostic decimal values of B_316 and B_321 are approximately 7.326849124876e−14 and 6.644912946337e−15, respectively; these decimals are not the certificates. This establishes sufficient degrees, not minimal degrees for the true Poisson tail.

### Counts and error-budget implication

For one h=1e−4 slab, the two options require 316 or 321 power blocks f_0,…,f_m, respectively, or 315/320 applications of P in an uncompressed sequential implementation. Their binary power-mode storage can be padded to length512 (nine QTT cores). A simultaneous AMEn solve has a different operation count and no measured cost is implied here.

If the entire T=1 horizon were covered by exactly 10,000 such slabs, the certified sum of Poisson tails would be <7.33e−10 for m=315 or <6.65e−11 for m=320. These are only uniformization-series truncation charges; AMEn residuals, contractions, and rounding still require their own budgets. The corresponding sequential counts would be 3,150,000 or 3,200,000 matvecs, or 10,000 simultaneous block solves. Adaptive slab sizes change these counts and require recomputation of the scalar tail certificate.

Reproducible files: `check_poisson_specialization.py` and `poisson_specialization.json` in this audit directory. They perform only the scalar arithmetic above, with no solver, package installation, or author-code execution.
