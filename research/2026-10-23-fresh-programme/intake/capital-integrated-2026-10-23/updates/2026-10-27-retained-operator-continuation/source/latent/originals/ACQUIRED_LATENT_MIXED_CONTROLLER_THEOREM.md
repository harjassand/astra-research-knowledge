# Astra Pro3: shared-latent response acquisition and mixed-controller experiments

27 October 2026. Mathematical/computational research continuation of Pro3's `ACQUIRED_POSITIVE_OPERATIONS.md` and the cyclic-conjugate programme. The original source's measured reading is acquired; symmetry, spectral class, linearity and measurement-error contracts are **supplied**. No physical law is claimed to have been discovered. Classical antecedents include positive symmetric completion, Woodbury/Sherman–Morrison matrix identities, Sturm root isolation and optimal recovery. The specific contribution investigated is the **experiment-to-shared-latent-to-multiple-operations compiler**, its genuinely rational native execution, its adversarial-noise controls and an instrument-bias repair. An equally informed retaining method can implement all the same operations.

## 1. Reduction from a whole operator family to a small shared latent space

Let the exact acquired consistency family be the **entire** Loewner interval

\[\mathcal S=[S_L,S_U]=\{S:S_L\preceq S\preceq S_U\}.\]

This hypothesis is substantive. The source's spectral contract plus exact forward-vector readings establish such a family in the positive-completion theorem of the preserved predecessor note; a general noisy record does not necessarily have this form.

Set `D=S_U−S_L ⪰0` and `r=rank D`. Let `V` be any full-column-rank, **rational** basis of `range(D)` (when the endpoints are rational), and set

\[H=V^+D(V^+)^\top,\qquad V^+=(V^\top V)^{-1}V^\top.\]

Then `H` is an `r×r` positive definite rational matrix, and **every and only** compatible source is

\[\boxed{S=S_L+V\Theta V^\top,\qquad 0\preceq\Theta\preceq H.}\tag{1}\]

Proof. For `X=S−S_L`, `0⪯X⪯D` implies `ker D⊆ker X`, since a PSD matrix annihilates every vector with zero quadratic form. Therefore `X` has range contained in `range(V)` and equals `V(V^+X(V^+)ᵀ)Vᵀ`. The middle matrix is PSD and bounded above by `H`. Conversely any `Θ∈[0,H]` gives `0⪯VΘVᵀ⪯D`. This proves equality, including rank-deficient endpoint cases. **No irrational Cholesky factor or hidden query interface is necessary.**

The number of unresolved real symmetric parameters is at most `r(r+1)/2`, regardless of the ambient port count `n`. Rank `r=1` is the tractable case exploited below.

### One observation actually creates a rank-one posterior

Native source: choose a real vector `q` and receive the entire vector `Sq`; source class is real symmetric `I⪯S⪯3I`. One **charged exact** native call at `q=e₀` returns

\[S e_0=2e_0+e_1.\]

Put `T=S−2I`, so `T=Tᵀ` and `−I⪯T⪯I`, with `Te₀=e₁`. Since `I−T²⪰0` and

\[e₀^\top(I−T²)e₀=1-\|Te₀\|²=0,\]

positivity gives `(I−T²)e₀=0`. Consequently `Te₁=T²e₀=e₀`. Self-adjointness makes `span(e₀,e₁)` invariant and decouples its orthogonal complement. In three ports the **complete** family is therefore

\[\boxed{S(t)=\begin{pmatrix}2&1&0\\1&2&0\\0&0&t\end{pmatrix},\quad1\le t\le3.}\tag{2}\]

Every member obeys the spectral contract and reproduces the actual measurement. The second column `(1,2,0)ᵀ` was not queried and is nevertheless forced. The unknown third column has one scalar degree of freedom. The source-aware check chose `t=7/4`, which was **not** supplied to the compiler. Acquisition cost: **1 full-vector native call, 3 returned scalars**. The old contract is an assumption, not an empirical inference from one vector.

## 2. Exact late operations for different, potentially nonsymmetric feedback

Let a later task, unknown during acquisition, specify a matrix `K_j`, applied load `p_j` and output functional `l_j`. Its unique equilibrium solves

\[(S-K_j)x_j=p_j.\]

Assume the symmetric part of `S_L-K_j` is bounded below by a certified positive `μ_j I`. Then every `S∈𝓢` has `sym(S-K_j)⪰μ_j I`, ensuring unique solvability **even if `K_j` is nonsymmetric**. Its inverse norm is at most `1/μ_j`, by Cauchy–Schwarz and the accretivity inequality.

Write `B_j=S_L−K_j`, `W_j=B_j⁻¹`, `M_j=Vᵀ W_j V`, `c_j=Vᵀ W_jp_j`. Using the exact Woodbury identity, without requiring `Θ` to be invertible, solve the `r×r` known-parameter system

\[(I+\Theta M_j)y_j=\Theta c_j,\qquad x_j=W_jp_j-W_jVy_j.\tag{3}\]

The same `Θ` must be reused for **every** controller, load and subsequent operation: giving each controller an independent `Θ_j` invents sources not admitted by the retained experimental record. For fixed `r`, (3) replaces many ambient `n×n` uncertainty variables with a small latent parameter. It does not solve general multivariate semialgebraic optimization for `r>1`.

At rank one, write `S(t)=S_L+(t−1)vvᵀ`, `||v||=1`. Set

\[a_j=l_jᵀW_jp_j,\quad b_j=(l_jᵀW_jv)(vᵀW_jp_j),\quad h_j=vᵀW_jv>0.\]

Then

\[\boxed{l_jᵀx_j(t)=a_j-\frac{(t-1)b_j}{1+(t-1)h_j}.}\tag{4}\]

The strict positivity of `h_j` follows from the accretivity of `B_j`. A portfolio of `m` requested controller responses is a single rational function `f(t)` with no poles on `[1,3]`. Its extrema occur at the two endpoints and the stationary roots. Clearing the positive denominators of

\[f'(t)=-\sum_j \frac{w_j b_j}{(1+(t-1)h_j)^2}\]

produces a polynomial of degree at most `2(m−1)` when all `m` denominators are distinct. Thus **univariate real-root isolation** yields a complete globally valid optimization procedure for arbitrarily many differing controllers. Real roots can be isolated exactly by Sturm sequences; if roots are irrational, a derivative Lipschitz bound on each isolated interval gives a certified rational outer enclosure. In the executed test all relevant extrema were rational, so the saved bounds are exact.

This is a new *procedure-language transfer* within the declared model, not a new identity in algebra.

### Full worked test: sharp interior optimum with two skew-feedback controllers

Use the acquired family (2), `p=l=e₂`, and late controllers

\[K(k)=\begin{pmatrix}0&0&k\\0&0&0\\-k&0&0\end{pmatrix},\quad k=1,2.\]

These are genuinely nonsymmetric, but `sym(S-K(k))=S⪰I`. Direct exact symbolic inversion, independently checked against (4), gives

\[e₂ᵀ(S-K(1))^{-1}e₂=\frac3{3t+2},\qquad e₂ᵀ(S-K(2))^{-1}e₂=\frac3{3t+8}.\]

Consider the unforeseen joint contrast

\[f(t)=\frac3{3t+2}-\frac{49}{16}\frac3{3t+8}.\]

Its derivative factors exactly as

\[f'(t)=\frac{81(t-2)(33t+46)}{16(3t+2)^2(3t+8)^2}.\]

Thus the minimum is attained at **interior** `t=2` (value `−9/32`), while the maximum occurs at `t=1` (value `−207/880`). The complete sharp compatible range is

\[\boxed{-\frac9{32}\le f(t)\le-\frac{207}{880}},\quad\mathrm{width}=\frac{81}{1760}.\tag{5}\]

In contrast, using individually sharp intervals for the two controller responses but **forgetting they share `t`** gives the outer range `[-9/16,81/1360]` of width `423/680`. The width reduction from preserving shared source identity is **`2068/153 ≈13.52×`** at **zero additional source calls**. The true fixture had `t=7/4`, giving `−1719/6148` in (5), but the hidden `t` did not enter the inference.

The executable also evaluated a signed three-controller portfolio, a cross-port portfolio and a portfolio mixing symmetric and nonsymmetric controller matrices. Their respective width reductions against an independent-per-operation envelope were `14359/5854≈2.45×`, `3014/2069≈1.46×`, and `3421/163≈20.99×`. Each controller's coercivity and each symbolic inverse identity were checked using exact rational matrices. A **strong** equal-information retainer can use (1)–(4) and tie all results. The independent-controller envelope is a weaker comparator, not an optimal retaining programme.

### Future counterfactual policy (same latent parameter through branching)

A later specified two-stage policy first *calculates* the response under `K(1)` and checks if its third coordinate is at least `3/8`. This corresponds precisely to `t≤2`. It then chooses `K(2)` when true, or `K(3)` otherwise. The possible second-stage output is the disjoint union

\[\big[3/14,3/11\big]\ \cup\ \big[1/9,1/8\big),\]

where the first interval corresponds to `t∈[1,2]` and the second to `t∈(2,3]`. (The omitted upper endpoint in the latter branch follows from the strict test.) It is not sound to assign the original full latent interval independently to both branches. **No native stage-1 or stage-2 intervention was performed**: this is a certified counterfactual programme using acquired linear-source knowledge and a supplied controller-selection rule.

## 3. Failure of exact rank collapse with tiny noisy initial observations

This is the indispensable limitation. If the old reading is only known within Euclidean norm `ε`, the rank-one interval (2) generally is **not** the exact posterior.

Let `s=1/1000`, `β=(1−s²)/(1+s²)`, `γ=2s/(1+s²)` and

\[S_\pm=\begin{pmatrix}2&\beta&0\\\beta&2&\pm\gamma\\0&\pm\gamma&2\end{pmatrix}.\]

Both obey `I⪯S_±⪯3I` because `β²+γ²=1`. Both return the **same** first-column observation, within `ε=1−β=2/1000001≈2×10⁻⁶` of the displayed report `(2,1,0)`. Yet their unqueried `e₂ᵀS e₁` answers are `±γ=±2000/1000001`, separated by almost `0.004`. A decoder using only that noisy report cannot uniformly guarantee an error below `γ≈0.002` for that later question. The uncertainty is of **square-root order** in the original reading defect. This is a mathematical indistinguishability obstruction, not simply a loose error-propagation formula.

There is still a **valid robust transfer**, with reduced claims. For any symmetric `T=S−2I` satisfying `||T||≤1` and `||Te₀−e₁||≤ε≤1`, the positive contraction `I−T²` implies

\[\|Te₁-e₀\|\le\varepsilon+\sqrt{2\varepsilon}.\]

Set `t=e₂ᵀ S e₂∈[1,3]` and define `\widehat S(t)` by the ideal rank-one family (2). Symmetry and the bound above give

\[\boxed{\|S-\widehat S(t)\|_2\le\delta(\varepsilon):=\sqrt{2\{\varepsilon^2+(\varepsilon+\sqrt{2\varepsilon})^2\}}.}\tag{6}\]

Proof: the Frobenius squared difference is at most twice the sum of squared first-column and second-column differences; the latter is bounded using `||T(e₁−Te₀)||≤ε` and `||(I−T²)e₀||≤√(2ε)`.

For skew `K_j`, both `S−K_j` and `\widehat S−K_j` are 1-accretive. The resolvent identity gives

\[\big|l_jᵀ(S-K_j)^{-1}p_j-l_jᵀ(\widehat S-K_j)^{-1}p_j\big|\le\delta\|l_j\|\|p_j\|.\]

For the two-controller contrast in (5), the complete robust outer interval is (5) widened by `65δ/16`, approximately

\[\boxed{[-0.292752,-0.223725]}.\]

It **still certifies the sign of the unforeseen controller contrast as negative**, even though the exact rank-one result is no longer justified. The source-aware script tested both `S_+` and `S_-` against this outer interval. It is an enclosure, not the sharp noisy-source consistency set. The square-root obstruction proves that a linear-in-`ε` general repair would be unsound.

## 4. Next experiment: universal precision-optimal excitation

Given a genuine exact rank-one posterior `S(t)=S_L+(t−1)vvᵀ` with `||v||=1`, suppose the new native instrument can select `||q||≤1` and reports `S(t)q+e`, with adversarial `||e||≤η`. Let `c=vᵀq`. For `c≠0`, projection along `v` yields a guaranteed latent interval centred on the observed scalar and of radius **at most `η/|c|`** (clipped to the prior). This is sharp in the interior because the adversary can choose error parallel to `v`. Under the unit-input contract `|c|≤1`, and `q=v` attains the maximum signal.

**Minimax theorem:** away from prior endpoints, **one probe `q=v` achieves worst-case latent error `η`**, and no choice of input can do better. Even an arbitrary number of adaptive probes cannot improve that deterministic minimax floor with adversarial per-reading errors: two sources `t_0±η` can generate the *same entire transcript* by responding with the midpoint readings and choosing errors `∓η v(vᵀq)` for each chosen `q`. More restrictive independent stochastic-noise contracts can permit averaging; they are not assumed here.

The executed native-control comparison uses true `t=7/4`, a new bound `η=1/100`, and an actual nonzero sensor perturbation `(+η/3)e₂`:

| One new full-vector experiment | Certified latent width | Certified later contrast width |
|---|---:|---:|
| `q=e₂` (optimal excitation) | `1/50 = 0.02` | `14525/51886818 ≈ 0.00027994` |
| `q=(e₀+e₂)/2` | `1/25 = 0.04` | `512579475/930619624249 ≈ 0.00055079` |
| `q=e₀` (already-known direction) | `2` | `81/1760 ≈ 0.04602273` |

Each row is one separate counterfactual acquisition strategy with its own charged native call; their measurements are **not pooled**. The experiment direction was chosen from the previously acquired uncertainty, not from the hidden true value of `t`.

## 5. Further attack: self-calibration with a new biased instrument

Suppose the prior rank-one family has been acquired by an **earlier, separate, calibrated** reading, but a newly available instrument instead reports

\[y(q)=S(t)q+b+e,\]

with one unknown, **constant** additive vector bias `b` across its calls. Let the admissible source inputs be fixed-dose nonnegative mixtures `q_i≥0`, `Σq_i=1`. With arbitrary unknown bias, **one** new instrument reading does not distinguish any two latent values: adjust `b` to fit the same response. Repeated observations of only the same input do not remove the gauge.

However, take **two** native experiments, `q₀=e₀`, `q₁=e₂`. Their difference eliminates `b` exactly:

\[y(q₁)-y(q₀)-S_L(q₁-q₀)=(t-1)e₂,\qquad(e=0).\]

This identifies `t` and `b` with **two and only two** exact biased-instrument readings. Both inputs are nonnegative, unit-total-dose mixtures, and neither is an unsupported negative or transpose action. The executed source chose a nonzero hidden bias `(1/10,−1/5,3/10)` and recovered both the true `t=7/4` and the bias using the two actual observations.

With per-reading adversarial Euclidean error at most `η`, the difference yields a guaranteed latent radius `2η`. This is **minimax optimal even with arbitrarily many adaptive fixed-dose probes** if the same unknown bias remains and errors may be adversarial. For any `t_0` sufficiently interior, compare sources `t_±=t_0±2η` and biases `b_±=b_0∓η e₂`. For every admissible mixture `q`, their noiseless biased outputs differ by `2η(2q₂−1)e₂`, of norm at most `2η`; they admit identical reports using errors of norm at most `η`. Every adaptive observation history can therefore coincide, so worst-case estimation error cannot be below `2η`. The two endpoint-mixture measurements attain the bound.

**Interface boundary:** If the bias can drift between the two calls without a bound, this self-calibration argument fails. It exploits a supplied linear response and stable shared bias, not a general ability to calibrate arbitrary physical instruments. A same-information calibrated retainer also achieves the result.

## 6. Costs, boundaries, and scientific assessment

- The original one-action rank collapse **requires an exact historical reading** and independently warranted symmetry and spectral bounds; the noisy approximation never inherits an exact-posterior flag.
- Mixed-controller calls are **predicted operations** evaluated from the retained family. No controller was physically installed or exercised in the synthetic test. Independent source-aware evaluations exist only in checker code.
- The matrix inverses in the compiler are rational computations on supplied controller matrices and known posterior endpoints; they are **not native inverse queries**.
- Mixed-controller portfolios require the **same unknown source** across all controllers. This is the mechanism behind the large reductions versus an independent-per-operation interval. For a true source that changes with each controller or across time, a different joint contract is necessary.
- Rank `r>1` still has a compact shared latent matrix, but arbitrary multi-controller optimization over its Loewner interval need not be convex or polynomial-time. Univariate root isolation resolves only the rank-one case.
- The active one-probe guarantee assumes unit vector inputs and adversarial norm-bounded output error; biased-instrument self-calibration assumes fixed-dose nonnegative inputs and an invariant additive calibration bias. Their error floors differ because their information interfaces differ.
- No physical measurement, source-class learning, global discovery of linearity or real hardware advantage was demonstrated. These are fully auditable mathematics and executed synthetic-source operations. Historical originality of the classical matrix and root-isolation ingredients is not asserted.

## 7. Executable work and established references

- `acquired_latent_controller_compiler.py` → `acquired_latent_controller_results.json`: exact one-reading source-family acquisition; rank-one Woodbury compiler for four late portfolios; rational root isolation; interior optimum; noisy square-root impossibility and sound robust transfer; adaptive policy semantics.
- `active_latent_precision.py` → `active_latent_precision_results.json`: three independently charged new native probe strategies, actual nonzero bounded sensor errors, task intervals and indistinguishable-source lower bound.
- `bias_cancelling_experiments.py` → `bias_cancelling_experiments_results.json`: positive fixed-dose source queries, unknown common sensor bias, self-calibration and deterministic many-call lower bound.
- `verify_latent_research.py` → `independent_verification_results.json`: independent rederivation of the chief exact extrema and output identities plus cross-checks of all saved result files.

References for **established** algebraic techniques: Woodbury matrix inversion identity, e.g. <https://changkun.de/bobook/en/appendices/b-gaussian-identities.html>; Sturm root isolation and proof technology, <https://isa-afp.org/entries/Sturm_Sequences.html>. The earlier Astra positive family and near-saturation controls are in the supplied `ACQUIRED_POSITIVE_OPERATIONS(1).md` and related saved source; no priority claim is made. The new executable control was developed without restoring unavailable historical modules.
