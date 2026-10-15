# PR92 phase-clock theorem: independent scoped review

15 October 2026. Read-only audit of head **5eb2441c93011d4fefb819b6f751f33537427dc3**, base **b7cada92d2eb304578be5ed974f1e44b10a89928**, in `/Users/harjas/Documents/ChatGPT/ultra/work/astra-pr92-audit-20261015`.

Principal source: `updates/FT-foundational-capability-20261015/package/workers/foundational_math/PHASE_CLOCK_THEOREM.md`, SHA256 **2fba7583a2f91d63366e39a2c0810a6a0bd0660d812947f3e90a7be3394195d4**. Its full proof, the actual package root review, worker report, targeted audit and diagnostic script were read. Their agreement was not used as a proof premise. No source, PR, repository or earlier frozen review was modified; no GitHub message was sent.

**Verdict:** the positive-error state theorem and zero-error prefix bounds survive independent reconstruction in the stated finite-state model. Two precision/computability sentences need the append-only scope clarification below. No substantive dependency connecting this phase theorem to the current G heat proof was found. This is internal mathematical review, not external certification, priority clearance or a practical quantum advantage claim.

## 1. Exact model and conclusion

The target is p_k=(1+cos(2παk))/2. A single horizon-specific triple(μ,P,f) supplies g_k=μPᵏf at every integer0≤k≤T: P is real row-stochastic, μ is a probability row, and0≤f≤1. The same P andf apply at all k, and μ cannot be chosen separately for each requested k. Parameters may depend onT,ε. There is no externally supplied elapsed-k input or continuous classical phase register.

For irrationalα with ∥qα∥_(R/Z)≥κ/q for allq≥1, and each **fixed**0<ε<1/4, the source proves

    Nα(T,ε)=Θ_(α,ε)((T+1)¹/³).

It does not assert a uniform Θ law as ε→0 withT, or an optimal error threshold1/4. Atε=0, irrationality alone givesT≤Nα(T,0)≤T+1 forT≥1. The lower count concerns stochastic states, not an unrestricted classical algorithm or a binary-memory separation.

## 2. Conditioning-free lower proof reconstructed

Source lines58–123. For z=e^(2πiα), letδ_n=min_(1≤q≤n)|1−z^q|. Given a complex vectorv with∥v∥∞=1, choose|v_i|=1 and letη=∥(zI−P)v∥∞. Stochastic contraction and telescoping give∥Pᵗv−zᵗv∥∞≤tη. For the Markov chain started ati,

    E|v_(X_t)−zᵗv_i|²≤2tη.

Positivity is essential in this expectation step. For eacht=0,…,n choose one coordinatej_t within√(2tη) ofzᵗv_i. These choices need not lie on one sample path. Two ofn+1 coordinates coincide, yieldingδ_n≤√(8nη). Thus(zI−P) is invertible and its complex∞-operator inverse norm is at most8n/δ_n². No eigenbasis, conditioning, irreducibility, stationary distribution or mixing bound is hidden.

Witha=2f−1, ∥a∥∞≤1 and2g_k−1=μPᵏa. The finite geometric-series resolvent and∥P^(T+1)∥∞=1 give

    |Σₖ₌₀ᵀz⁻ᵏ(2g_k−1)|≤16n/δ_n².

For the target, the sum is(T+1)/2+(1/2)Σz⁻²ᵏ. The second term is bounded in modulus byCα=1/|1−z²|. Uniform probability errorε perturbs this centered sum by at most2ε(T+1). Its modulus is therefore at least(T+1)(1/2−2ε)−Cα.

For0≤d≤1/2,2sin(πd)≥4d. Henceδ_n≥4κ/n, and the upper witness bound becomesn³/κ². The resulting source inequality

    n³≥κ²[(T+1)(1/2−2ε)−Cα]

has the correct constants. It is nontrivial only once its bracket is positive. The entire prefix, rather than a sampled set of lags, is necessary for this argument.

## 3. Matching construction and angles

Source lines125–181. Choose a continued-fraction convergentp/N, N≥3, h=2π/N, d=2π|α−p/N|<h/N, ands=sign(α−p/N). Mix row shiftsj→j+p andj→j+p+s with second weight

    t=sin d/[sin d+sin(h−d)].

For either sign of the convergent error, the first Fourier character's eigenvalue is

    (1−t)e^(2πip/N)+te^(2πi(p+s)/N)=rz,
    r=cos(h/2)/cos(d−h/2)∈(0,1).

The sign determines which adjacent shift to mix; replacing it by one fixed direction would be incorrect. The source uses the correct orientation. Sincecos(h/2)≥1/2,

    1−r=2sin(d/2)sin((h−d)/2)/cos(d−h/2)
         ≤d(h−d)≤dh<4π²/N³.

Starting at0 withf_j=(1+cos(2πj/N))/2 givesg_k=(1+rᵏcos(2παk))/2, and error≤k(1−r)/2≤2π²T/N³. ThusN≥max{3,(2π²T/ε)¹/³} suffices. Consecutive denominators obeyκ/q_j≤|q_jα−p_j|<1/q_(j+1), so their ratio is less than1/κ. The first denominator above the threshold is consequentlyO_α((T/ε)¹/³).

For the explicit golden phaseα=(√5−1)/2, the source'sκ=1/3 is valid: for nearestp, p/q∈[0,1], the nonzero integerp²+pq−q² and conjugateβ=−(√5+1)/2 give|α−p/q|>1/(3q²). Fibonacci denominator ratios are bounded by2.

The real qubit rotation angle is **πα**, not2πα: |⟨0|R(πα)ᵏ|0⟩|²=cos²(kπα)=p_k. The audit's alternative|+⟩,diag(1,z),|+⟩ formulation is equivalent. Both describe one terminal read, or separate preparation–wait–read experiments; neither proves a repeated nondisturbing readout joint law or autonomous ticking-clock performance.

## 4. Exact-prefix argument

Source lines230–248. Suppose an exactn-state realization hasn≤T−1. Its real characteristic polynomialq hasq(1)=0, and Cayley–Hamilton gives the recurrence at shiftss=0,1 using only indices throughn+1≤T. Substituting the target yieldsReq(z)=0 andRe[zq(z)]=0. Becausez is nonreal, these implyq(z)=0. This contradicts the resolvent lemmaδ_n>0 for irrationalα. Thusn≥T. The deterministic path ofT+1 states with readoutp_k realizes the prefix exactly. No rank-collapse, hidden-spectrum theorem or stochastic peripheral-spectrum citation is needed.

## 5. Append-only precision and computability clarification

Two source sentences should receive a semantic notice while the original bytes remain intact.

**Computability:** PHASE_CLOCK lines185–186 say that the ideal real parameters are computable. The theorem's generic irrational/Diophantine premise is not a computability or numerical-access contract. Retain the generic state-existence theorem, but read algorithmic construction claims as applying to the explicitly specified golden phase, or to a supplied computableα with a specified approximation oracle. The worker REPORT lines126–135 already state a supplied computable phase. An exact real phase or gate in the abstract model is not automatically a finite acquired input.

**Precision:** PHASE_CLOCK lines48–52 say finite implementation “must” maintain accuracy of orderε/(T+1), while lines183–195 and REPORT lines126–129 correctly invoke direct error composition. A safe clarification is: “Per-wait gate errorO(ε/(T+1)) is a sufficient worst-case direct-composition budget, withO(log((T+1)/ε)) precision bits; no universal necessity or optimal calibration-cost theorem is claimed.” The target probabilities are unchanged underα→1−α, so absolute parameter closeness is not even a global necessity without a phase convention and local error model.

Rounding the classical mixing weight byΔt changes each transition row in total variation by at most|Δt|. Coupling/telescoping bounds a terminal probability error byT|Δt|; a uniform readout roundingη adds at mostη. Reserving an ideal approximation margin therefore gives rational finite parameters withO(log((T+1)/ε)) bits per rounded number. This is sufficient, not a claim of optimal bit constants. Computing those numbers requires the phase precision needed by the formulas; total description, source access and calibration costs are separate from the state count.

The diagnostic script reserves half the error for the ideal construction and explicitly labels the million-step lag checks as sampled. Its exact Fraction propagation only certifies the rounded Markov propagation; its comparison with irrational targets uses high-precision numerics. The analytic bound, rather than those samples, covers all lags. I did not execute the producer script in its source directory.

## 6. Actual dependencies and relation to G/heat

The principal theorem depends on stochastic positivity/contraction, finite-dimensional linear algebra, the displayed Diophantine premise, elementary trigonometry and continued-fraction approximation. The exact-prefix corollary adds Cayley–Hamilton. Its package root review is a separate reconstruction, not a premise. The branch's exterior-power rank-collapse and hidden-spectrum counterexample are separate outcomes, not dependencies. Historical comparator papers were reported by the source; I did not independently repeat their priority search.

No G polynomial, quasiconvexity theorem, compatible spatial-gradient constraint, closed two-form, heat Gram certificate or critical-trace storage is used. Conversely, the current G proof uses none of the finite-state phase resolvent or Diophantine denominator bounds. Its positive Gram matrix is not a stochastic transition matrix, and rank18 is not a phase-clock state count. Generic words such as phase, positivity or evolution do not establish a mathematical transfer.

State-address memory islog₂n=(1/3)log₂T+O_(α,ε)(1), while an ordinary counter and numerical cosine evaluation also useO(logT) memory bits. The source explicitly preserves this comparator. No speed, energy, learning, fabrication, readout, physical coherence or complete-resource separation has been proved.
