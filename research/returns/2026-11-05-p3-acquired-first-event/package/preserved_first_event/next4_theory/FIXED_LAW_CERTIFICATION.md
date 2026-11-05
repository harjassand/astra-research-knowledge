# Certifying an unknown dynamical law from finitely many experiments

## Result and status

**Question.** Given finitely many measured transitions, a trusted global Lipschitz bound, and a proposed sequence of controls, what can be guaranteed about the trajectory of the same unknown physical law? Can an unsuccessful certificate produce an actual compatible law, rather than merely a pessimistic uncertainty tube?

**Answer.** For deterministic, fully observed, time-homogeneous Euclidean dynamics, all finite-horizon ambiguity has an exact finite interpolation description. Keeping every pairwise consistency constraint produces a Gram semidefinite program (SDP). The SDP always gives an upper bound; it is exact when an optimal Gram matrix embeds in the physical dimension. This happens automatically when the physical dimension is at least the known-vector span dimension plus the number of unknown vector values. A feasible Gram matrix of allowable rank gives a realizable trajectory, and the dual gives a checkable algebraic certificate. For strict contractions with exact data, possible equilibria are exactly an intersection of explicitly known balls. This gives an additional exact second-order cone program (SOCP) and a geometric tail bound that turns finite-horizon analysis into a complete procedure for safety questions having a positive margin.

A sharp calculation exposes a substantial loss from forgetting that the law is fixed. From the single observation `f(0) = -e`, with `||e|| = 1`, the exact largest value of `⟨e,f(f(-e))⟩` in dimension at least two is

\[
 B_{\ge2}(L)=
 \begin{cases}
 -1+\dfrac{L(1+L)}{1+2L},&0\le L\le\tfrac12,\\[5pt]
 L^2-\tfrac78,&L\ge\tfrac12.
 \end{cases}
\]

Both branches have explicit attaining maps and exact sum-of-squares certificates below. In one dimension the exact answer is

\[
 B_1(L)=
 \begin{cases}
 -1+\dfrac{L(1+L)}{1+2L},&0\le L\le\varphi,\\[5pt]
 L^2-L-1,&L\ge\varphi,
 \end{cases}
 \qquad \varphi=\frac{1+\sqrt5}{2}.
\]

For `L = 1`, a stepwise relaxation permits `1`, the exact answer in dimension at least two is `1/8`, and the exact scalar answer is `-1/3`. Thus a safety threshold of `1/2` is certified by fixed-law consistency and missed by the stepwise relaxation.

**Priority and scope.** Lipschitz interpolation and Gram SDP performance estimation are established machinery, particularly Kirszbraun's theorem and operator performance estimation [1–3]. Their use here must not be presented as a new general optimization principle. The closed-form envelope, its dimensional phase diagram, and the complete finite-data certification synthesis were derived in this work; historical novelty of these particular statements has not been established. This is a proved construction and an explicit example, not evidence of a new physical law, an empirical benchmark win, or a civilization-scale breakthrough.

---

## 1. The precise physical model class

Let the unknown law be

\[
 f:\mathbb R^{d+m}\to\mathbb R^d,
 \qquad \|f(x,u)-f(x',u')\|
 \le L\sqrt{\|x-x'\|^2+\|u-u'\|^2},
 \tag{1}
\]

where `L ≥ 0` is given. The system evolves according to

\[
 x_{t+1}=f(x_t,u_t),\qquad t=0,\ldots,H-1,
 \tag{2}
\]

from a known `x₀`, with an already specified open-loop control sequence. Measurements are

\[
 \mathcal D=\{(a_i,v_i,\bar b_i,\eta_i):i=1,\ldots,N\},
 \qquad
 \|f(a_i,v_i)-\bar b_i\|\le\eta_i.
 \tag{3}
\]

Inputs are exact; output errors are bounded. Exact observations have `ηᵢ = 0`. There is a **single** law `f` for all observations and all future steps. We assume the class is nonempty; emptiness is an inconsistency diagnosis, not a safety result.

The model includes nonlinear laws and arbitrary learned proposal models, but it does not include unobserved state, time-varying dynamics, arbitrary stochastic innovations, or an unproved global regularity bound. A change of physical units changes the norm and therefore the meaning of `L`. An anisotropic metric can be used if it is fixed and represented correctly, but the Euclidean theorem should not be silently applied to arbitrary norms or independently asserted physical properties.

A learned model can provide a fixed reference rollout `x̂₁,…,x̂_H`, a proposed control sequence, and candidate dangerous directions. Certification then optimizes over the physical class (1)–(3). The learned model does not need to be trusted or to belong to that class. In particular, the worst possible squared discrepancy `||x_H-x̂_H||²` is a linear Gram objective once `x̂_H` is fixed.

The analysis is for a **fixed plan**. If controls are feedback values depending on unknown future states, or if controls are optimized jointly, the resulting constraints need not be linear in a Gram matrix. Those cases require an additional valid representation; they do not inherit this SDP claim automatically.

## 2. Exact finite interpolation replaces the unknown function

Introduce unknown true measured outputs `wᵢ` for records with nonzero uncertainty, and form a finite graph with `N+H` vertices:

\[
 (X_\alpha,U_\alpha)\mapsto Y_\alpha.
\]

The first `N` vertices are `(aᵢ,vᵢ) ↦ wᵢ`, with `wᵢ=b̄ᵢ` when the record is exact. The other vertices are `(x_t,u_t) ↦ x_{t+1}`.

### Theorem 1 — exact finite-graph characterization

A proposed measured-output assignment and trajectory are produced by some global law satisfying (1)–(3) if and only if

\[
 \|w_i-\bar b_i\|^2\le\eta_i^2,
 \tag{4}
\]

and, for every pair of graph vertices,

\[
 \|Y_\alpha-Y_\beta\|^2
 \le L^2\bigl(\|X_\alpha-X_\beta\|^2
                    +\|U_\alpha-U_\beta\|^2\bigr).
 \tag{5}
\]

This includes data–data, data–future, and future–future pairs. Duplicate inputs necessarily have the same output. No continuity, smoothness, or interpolation approximation is hidden in the sufficiency direction.

**Proof.** Necessity follows from (1). For sufficiency it is enough to prove the finite Euclidean extension theorem, with inputs `pᵢ` and outputs `qᵢ` satisfying `||qᵢ-qⱼ|| ≤ L||pᵢ-pⱼ||`.

To add one new input `p`, minimize the strongly convex coercive function

\[
 \Phi(y)=\max_i\{\|y-q_i\|^2-L^2\|p-p_i\|^2\}.
\]

At its minimizer `y*`, the subgradient optimality condition supplies nonnegative weights `λᵢ` on the active indices, summing to one, with `y*=Σᵢλᵢqᵢ`. All active expressions equal `Φ(y*)`. Weighted variance identities therefore give

\[
\begin{aligned}
 \Phi(y_*)&=\sum_i\lambda_i\|y_*-q_i\|^2
                 -L^2\sum_i\lambda_i\|p-p_i\|^2\\
 &=\frac12\sum_{i,j}\lambda_i\lambda_j\|q_i-q_j\|^2
   -\frac{L^2}{2}\sum_{i,j}\lambda_i\lambda_j\|p_i-p_j\|^2
   -L^2\left\|p-\sum_i\lambda_i p_i\right\|^2\\
 &\le0.
\end{aligned}
\]

Consequently `y*` belongs to every ball `B(qᵢ,L||p-pᵢ||)`. Add the points of a countable dense subset of input space one at a time. Every finite stage remains `L`-Lipschitz. The resulting map on that dense set and the original inputs extends uniquely by continuity to the whole input space, retaining the same Lipschitz constant. This also covers unequal input and output dimensions. If `L=0`, all outputs coincide and the constant extension suffices. Applying this to the finite graph proves the result. ∎

This is a self-contained proof of the specific Kirszbraun machinery needed here [1,2]. It is a constructive extension through a sequence of convex one-point problems; it is **not** a claim that an arbitrary global extension has a short closed-form expression or can be evaluated without any representation choices. A compatible finite graph plus this theorem already proves that a counterexample trajectory is physically realizable within the stated class.

### Why future–future pairs matter

An envelope queried separately at each state only checks compatibility of each new output with the original data. It can therefore choose outputs that cannot simultaneously be values of one function. Those extra trajectories are mathematical artifacts. Equation (5) is the exact condition that removes them. Some existing set-membership methods retain more global model information; this distinction should be made at the level of a specified algorithm, not assumed for all reachability methods.

## 3. Gram optimization, exactness, and proof objects

Let the span of all known state-space vectors occurring in the problem have dimension `r`. Include measured inputs, exact measured outputs or uncertain-output centers, the initial state, and all reference or direction vectors needed by the objective. Choose a fixed orthonormal basis `E₁,…,E_r` of this span.

There are `K` unknown vectors: `x₁,…,x_H` and one true output for each uncertain measurement. Thus `K=H` for exact data and at most `H+N` in general. Form the Gram matrix

\[
 G=\operatorname{Gram}(E_1,\ldots,E_r,z_1,\ldots,z_K).
\]

Every graph vector has a known coefficient vector in these formal columns. If `v=ΣⱼvⱼZⱼ`, then `||v||²=vᵀGv`. Hence (4)–(5) become linear inequalities in `G`:

\[
 A_e\mathbin\bullet G\le b_e,
 \qquad G_{1:r,1:r}=I_r,
 \qquad G\succeq0.
 \tag{6}
\]

Here `A•G=tr(AᵀG)`. Fixed control distances enter the scalar right sides. Any fixed quadratic expression in known and unknown vectors is linear in `G`, including a directional terminal value, a squared terminal prediction error, or a weighted sum of such expressions.

### Theorem 2 — exactness with the physical dimension retained

For a linear Gram objective, the original worst-case problem is exactly (6) with the additional constraint

\[
 \operatorname{rank}G\le d.
 \tag{7}
\]

Dropping (7) always gives a valid upper bound. If an SDP optimizer satisfies (7), its optimum is attainable by an admissible law in the physical dimension. In particular, the SDP is automatically exact whenever `d ≥ r+K`.

**Proof.** Any physical configuration produces a feasible Gram matrix with rank at most `d`. Conversely, factor a feasible rank-at-most-`d` matrix as inner products of vectors in `Rᵈ`. Its first `r` vectors are orthonormal. An orthogonal transformation sends these vectors to the specified known basis, so every known vector has exactly its required value after the transformation. The resulting measured outputs and trajectory satisfy (4)–(5), and Theorem 1 supplies the law. Finally, every `(r+K)×(r+K)` Gram matrix has rank at most `r+K`. ∎

The automatic dimension condition is sufficient, not necessary. The sharp example below uses a `3×3` Gram matrix but has rank two. In a lower fixed physical dimension the rank restriction is real; the scalar example proves that discarding it can change the answer. Solving the remaining rank-constrained polynomial problem is generally nonconvex. For rational input data and algebraic specifications it is a finite semialgebraic problem and can in principle be decided by real quantifier elimination; that is a computability statement, not an efficient algorithm.

### Finite bounds and dual certificates

Suppose at least one measurement is available. Choose record `j`, and set

\[
 \beta_j=\|\bar b_j\|+\eta_j,\qquad R_0=\|x_0\|,
\]

\[
 R_{t+1}=\beta_j+L\bigl(R_t+\|a_j\|+\|u_t-v_j\|\bigr).
 \tag{8}
\]

The triangle inequality and (1) prove `||x_t||≤R_t`. Also `||wᵢ||≤||b̄ᵢ||+ηᵢ`. Consequently the redundant constraint

\[
 \operatorname{tr}G\le T
 :=r+\sum_{t=1}^H R_t^2+
       \sum_{i:\eta_i>0}(\|\bar b_i\|+\eta_i)^2
 \tag{9}
\]

makes compactness explicit without changing the admissible set. It is valid in any realization dimension.

For a primal objective `C•G+c₀`, any numbers `λ_e≥0`, `ρ≥0`, and a symmetric `r×r` matrix `Y` satisfying

\[
 S:=\operatorname{embed}(Y)+\sum_e\lambda_eA_e+\rho I-C\succeq0
 \tag{10}
\]

give the rigorous upper bound

\[
 C\mathbin\bullet G+c_0\le
 \operatorname{tr}Y+\sum_e\lambda_eb_e+\rho T+c_0.
 \tag{11}
\]

Indeed, subtracting the left side from the right side gives exactly

\[
 S\mathbin\bullet G+
 \sum_e\lambda_e(b_e-A_e\mathbin\bullet G)+
 \rho(T-\operatorname{tr}G),
\]

whose terms are nonnegative. This is the proof object, independent of how its multipliers were found.

The trace cap allows a strictly feasible dual by taking positive inequality multipliers, sufficiently large `ρ`, and any suitable `Y`; thus standard finite-dimensional conic duality gives no primal–dual gap for a nonempty feasible primal. The primal optimum is attained by compactness. **The dual infimum need not be attained:** degeneracy is possible with exact data. Arbitrarily accurate dual upper bounds nevertheless exist. Strict safety margins allow approximation; an exact equality-threshold conclusion can require a separate analytic certificate.

A floating-point solver's objective, status, small residual, or eigenvalues are not a formal certificate. Multipliers and PSD claims require exact algebra or verified numerical bounds before making a proof-level claim. The identities in Section 4 avoid this issue entirely. The accompanying implementation returns numerical candidates and labels them accordingly.

### Experimental and computational price

The certificate consumes `N` measured transitions, the claimed regularity constant, an initial condition, the plan, and an objective. It does not ask the physical system to execute the predicted horizon. Its SDP has a PSD matrix of order `r+K` and at most `(N+H)(N+H-1)/2` interpolation inequalities, plus output-error and anchor constraints. The cost grows with horizon and number of records; this is not a constant-cost oracle.

In the real-arithmetic convex model these are standard SDP instances. Bit complexity, conditioning, degeneracy, and the requested certification margin still matter. No uniform practical polynomial-time guarantee for exact real-valued answers is asserted. Low physical dimension can also require the nonconvex rank restriction.

A useful architecture is therefore: a learned model proposes inexpensive plans; a certificate solver checks a finite selection; a checked dual certifies a guarantee; a rank-valid primal witness identifies a compatible failure mechanism. If the result is inconclusive because of a missing prior, insufficient data, rank relaxation, or numerical precision, that reason remains part of the answer.

## 4. A solved sharp prediction problem

The next theorem is an exact test of the method, with no appeal to numerical optimization.

Let `e` be a unit vector and suppose the sole observation is

\[
 f(0)=-e.
\]

Starting at the observed output `-e`, put

\[
 a=f(-e),\qquad b=f(a).
\]

Theorem 1 says these values are possible exactly when

\[
 g_1:=\|a+e\|^2-L^2\le0,
\]

\[
 g_2:=\|b+e\|^2-L^2\|a\|^2\le0,
\]

\[
 g_3:=\|b-a\|^2-L^2\|a+e\|^2\le0.
 \tag{12}
\]

### Theorem 3 — the exact vector envelope

For every `d≥2` and `L≥0`,

\[
 \sup_{\operatorname{Lip}(f)\le L,\ f(0)=-e}
       \langle e,f(f(-e))\rangle=B_{\ge2}(L),
\]

with the piecewise formula stated at the start.

**Proof, small-L branch.** For `0<L≤1/2`, define

\[
 s=-\frac{1+L}{1+2L},\qquad
 t=-1+\frac{L(1+L)}{1+2L},\qquad
 z=a-se,\quad w=b-te.
\]

Direct expansion, using `||e||=1`, gives the exact identity

\[
 \boxed{
 \langle e,b\rangle=t+\frac{g_2+g_3}{2L}
 -\frac1L\left\|w-\frac z2\right\|^2
 -\frac{1-4L^2}{4L}\|z\|^2.}
 \tag{13}
\]

All subtracted coefficients are nonnegative, so the objective is at most `t`. To attain it, define a scalar function

\[
 h(x)=
 \begin{cases}
 s,&x\le-1,\\
 s+L(x+1),&-1\le x\le s,\\
 t-L(x-s),&s\le x\le0,\\
 -1,&x\ge0.
 \end{cases}
 \tag{14}
\]

The breakpoints satisfy `-1<s<0`, the pieces meet because `t=(1+L)s+L` and `t+Ls=-1`, and every slope has magnitude at most `L`. Thus `f(x)=h(⟨e,x⟩)e` is globally `L`-Lipschitz, with `f(0)=-e`, `a=se`, and `b=te`. For `L=0`, the constant map attains `-1`.

**Proof, large-L branch.** For `L≥1/2`, define

\[
 p=\frac12-\frac1{8L^2}\ge0,
 \qquad q=\frac1{4L^2}.
\]

A second exact identity is

\[
 \boxed{
 \langle e,b\rangle=L^2-\frac78+p g_1+qg_2+qg_3
 -\frac1{8L^2}\|a-2b+(2L^2-1)e\|^2.}
 \tag{15}
\]

It proves the upper bound. To attain it, let `Q` be a rotation of a plane containing `e` with

\[
 \cos\theta=-\frac1{4L},
\]

and act orthogonally on its perpendicular complement. Set

\[
 f(x)=LQx-e.
 \tag{16}
\]

This map has global Lipschitz constant `L`. Its second future state is

\[
 b=-e-LQe-L^2Q^2e,
\]

so

\[
 \langle e,b\rangle=-1-L\cos\theta-L^2(2\cos^2\theta-1)
                  =L^2-\frac78.
\]

The angle exists in this branch, and the two formulas agree at `L=1/2`. ∎

The transition at `L=1/2` is a geometric change in the extremal mechanism. Below it a scalar piecewise-linear law is extremal. Above it an affine rotation attains a larger value than any scalar law until the scalar regime changes again. The two optimal branches can meet with different derivatives because several distinct geometries are optimal at the transition.

### Exact specialization at L = 1

Choose a unit vector `w` orthogonal to `e`. An attainer has

\[
 a=-\frac34e+\frac{\sqrt{15}}4w,
 \qquad
 b=\frac18e+\frac{\sqrt{15}}8w.
\]

Its Gram matrix is

\[
 G_*=
 \begin{pmatrix}
 1&-3/4&1/8\\
 -3/4&3/2&3/8\\
 1/8&3/8&1/4
 \end{pmatrix},
\]

which is PSD of rank two and makes all three constraints tight. The rational certificate is

\[
 \langle e,b\rangle=
 \frac18+\frac38g_1+\frac14g_2+\frac14g_3
 -\frac18\|e+a-2b\|^2\le\frac18.
 \tag{17}
\]

The multipliers and Gram matrix are rational. The square roots occur only in a coordinate realization; no floating-point arithmetic is needed to verify optimality.

### Theorem 4 — the exact scalar envelope and dimensional obstruction

For `d=1`, orient `e=1`. The exact answer is `B₁(L)` stated above.

**Proof.** The first constraint gives `a∈[-1-L,-1+L]`. Given this `a`, the largest compatible `b` is

\[
 U(a)=\min\{-1+L|a|,\ a+L|a+1|\}.
 \tag{18}
\]

The intervals defining the two conditions on `b` have a common point: this follows either directly from `|a+1|≤L` and the triangle inequality, or from the one-point extension proof. Hence maximizing (18) is exact.

On `[-1,0]`, its two affine pieces cross at

\[
 a=s=-\frac{1+L}{1+2L},
\]

with value `t=-1+L(1+L)/(1+2L)`. This point is within the permitted interval for every `L≥0`.

On the permitted part of `a≤-1`, if `L≤1` the second upper bound is at most `-1`. If `L>1`, both affine upper bounds decrease with `a`, and their maximum over that interval occurs at `a=-1-L`, with value `L²-L-1`. The interval `a≥0` occurs only when `L≥1`; there the first bound is smaller and increases with `a`, giving the same endpoint value `L²-L-1` at `a=L-1`.

Thus the answer is `t` for `L≤1`, and `max{t,L²-L-1}` for `L≥1`. The two expressions cross at `L=φ`, because after division by positive `L` their equality is `L²-L-1=0`. The scalar function (14) attains `t` for every `L>0`; for `L≥φ`, the globally Lipschitz function `h(x)=L|x|-1` attains `L²-L-1`. ∎

At `L=1`, the scalar bound is `-1/3`, whereas the unconstrained Gram SDP gives `1/8`. This proves that a rank restriction cannot in general be removed in a prescribed low physical dimension.

### The exact cost of a stepwise relaxation

If the future–future constraint `g₃≤0` is dropped, the exact relaxed answer is

\[
 R(L)=-1+L+L^2.
 \tag{19}
\]

Indeed, `||a||≤1+L` and `⟨e,b⟩≤-1+L||a||`. Equality holds at

\[
 a=-(1+L)e,\qquad b=(-1+L+L^2)e.
\]

For every `L>0`, this chosen pair violates the omitted condition: `||b-a||=2L+L²`, while the allowed value is `L||a+e||=L²`. It is not a trajectory of any admissible fixed law.

The vector relaxation gap is therefore exactly

\[
 R(L)-B_{\ge2}(L)=
 \begin{cases}
 \dfrac{2L^2(1+L)}{1+2L},&0\le L\le1/2,\\[5pt]
 L-1/8,&L\ge1/2.
 \end{cases}
\]

This comparison is against the precisely defined relaxation (19). It is not an empirical comparison against ForeReach, all zonotope methods, or all set-membership approaches.

## 5. Exact equilibria and an unlimited-horizon certificate

Now take an autonomous map `f:Rᵈ→Rᵈ`, or hold the same control fixed throughout and use observations taken at that control. Assume `0≤L<1` and exact observations `f(aᵢ)=bᵢ`. The observations satisfy all pairwise Lipschitz conditions.

### Theorem 5 — the exact set of data-compatible equilibria

The set of equilibria of all admissible maps is exactly

\[
 \mathcal X_* = \bigcap_{i=1}^N
 B\left(
 \frac{b_i-L^2a_i}{1-L^2},
 \frac{L\|b_i-a_i\|}{1-L^2}
 \right).
 \tag{20}
\]

Every point in this intersection is the unique equilibrium of at least one compatible global contraction.

**Proof.** Add the graph vertex `x↦x` to the measured graph. The new interpolation conditions are precisely

\[
 \|x-b_i\|\le L\|x-a_i\|.
\]

Completing the square gives the balls in (20). Necessity follows from the contraction inequality. Sufficiency follows from Theorem 1. The resulting extension is a contraction of complete Euclidean space, so Banach's theorem makes its fixed point unique. ∎

For a linear observable `h(x)=cᵀx`, its exact worst equilibrium value

\[
 M_* = \max_{x\in\mathcal X_*}c^Tx
 \tag{21}
\]

is an SOCP in the actual physical dimension. There is no Gram-rank relaxation in (20)–(21). The intersection is nonempty because the data have a contraction extension; it is compact when at least one record is present. This equilibrium statement is restricted to exact observations. Bounded-noise outputs can be included in the finite-graph formulation, but one must not simply intersect balls around the reported centers and call that exact.

### Theorem 6 — finite computation controls the infinite horizon

Let `h` be `κ`-Lipschitz and `x₀` known. Define

\[
 V=\sup_{f\in\mathcal F(\mathcal D,L)}\sup_{t\ge0}h(f^t(x_0)),
\]

\[
 M_H=\max_{0\le t\le H}\sup_{f\in\mathcal F(\mathcal D,L)}h(f^t(x_0)).
\]

Choose any observed pair `(aⱼ,bⱼ)` and let

\[
 R=\|x_0-a_j\|+\frac{\|b_j-a_j\|}{1-L}.
 \tag{22}
\]

With `M* = max_{x∈X*}h(x)`,

\[
 \boxed{
 \max\{M_H,M_*\}\le V\le
 \max\{M_H,M_*+\kappa R L^{H+1}\}.}
 \tag{23}
\]

**Proof.** Each admissible contraction has a unique fixed point `x*`. Since

\[
 \|x_*-a_j\|\le\|x_*-b_j\|+\|b_j-a_j\|
 \le L\|x_*-a_j\|+\|b_j-a_j\|,
\]

we obtain `||x₀-x*||≤R`. Thus

\[
 |h(f^t(x_0))-h(x_*)|\le\kappa R L^t.
\]

For `t>H` this gives the upper bound in (23). The finite-horizon lower bound is immediate. Every feasible equilibrium is realized by a compatible contraction, whose trajectory from `x₀` converges to it; continuity of `h` supplies the equilibrium lower bound. ∎

For `0<L<1`, an absolute tail tolerance `ε>0` requires any nonnegative integer `H` satisfying

\[
 H+1\ge\frac{\log(\kappa R/\epsilon)}{-\log L}
 \tag{24}
\]

when `κR>ε`; smaller tolerances are unnecessary when `κR≤ε`. For `L=0`, the trajectory is constant after one step. As `L↑1`, the guarantee becomes expensive: `R` itself can scale as `(1-L)^{-1}` and the required horizon scales as roughly `(1-L)^{-1}` times a logarithm. The result does not hide this loss.

For linear `h`, (21) is an SOCP and each finite-horizon directional problem has the exact rank-constrained formulation of Theorem 2. The relaxed SDP can prove safety at any dimension, but completeness requires exact finite-horizon optima, rank-valid witnesses, or a relaxation that is known exact. A large physical dimension need only support the horizon actually needed for the specified margin; it cannot satisfy `d≥r+H` for arbitrarily large `H` at fixed `d`.

**Positive-margin completeness.** Suppose the safety requirement is `h(x_t)≤c` for all `t`. If the true robust supremum satisfies `V≤c-δ` for some `δ>0`, exact finite-horizon and equilibrium calculations eventually prove safety via (23). If `V>c`, a finite violating trajectory exists and increasing the horizon eventually finds one. The equality case `V=c` need not terminate under an approximate-certificate procedure. This is a restricted positive theorem under strict contraction and effective finite optimization; it neither contradicts general undecidability premises nor certifies arbitrary physical laws from data alone.

## 6. What is gained, and what existing methods already provide

### Established interpolation and performance estimation

Kirszbraun's Euclidean extension theorem is the exact interpolation result behind Theorem 1. Ryu, Taylor, Bergeling, and Giselsson use interpolation and Gram SDPs to obtain tight operator-splitting performance bounds; their Fact 2 is the same Lipschitz interpolation condition [2]. PEPit implements Lipschitz-operator pairwise constraints and automated performance estimation [3]. This work's general Gram formulation belongs to that family. Its emphasis is on fixing measured physical transitions, retaining one law along a forecast, exposing physical dimension, and providing an exact solved prediction problem plus an equilibrium-tail completion.

Adding several individually valid interpolation conditions for different operator classes is not automatically sufficient for their intersection. Ryu et al. explicitly exhibit this failure for combined Lipschitz and monotonicity conditions [2]. Consequently one cannot claim that adding conservation, monotonicity, passivity, invertibility, or thermodynamic inequalities to (5) preserves exactness without a corresponding joint extension theorem.

### Data-driven reachability

Alanwar et al. propagate sets of dynamics compatible with noisy data using matrix zonotopes and extend the treatment to nonlinear systems with Lipschitz information [4]. Such methods can be more scalable than retaining an increasingly large joint Gram problem. Their guarantees and this exact construction address related uncertainty, but different representations and assumptions make universal dominance claims unjustified.

Huang et al.'s 2026 ForeReach paper is especially close in purpose: it certifies a fixed control sequence under scarce one-step target data, constructs a set-membership model-error envelope under supplied componentwise regularity, and propagates zonotopic tubes. Its abstract also emphasizes that finite data can refute but cannot establish the global regularity prior, and reports a finite-plan projected-width lower bound [5]. The publicly retrieved abstract supports those comparisons; a full-text comparison was not available in this session. The present theorem uses a global Euclidean Lipschitz law, an exact joint interpolation characterization, and a physical-dimension condition. It proves a loss for one explicitly defined stepwise relaxation, not a performance advantage over every implementation of ForeReach.

### Certificates learned from trajectories

Learning Lyapunov or contraction certificates from data is another established route to global behavior under its own assumptions [6]. The present procedure does not require learning a candidate Lyapunov function: it optimizes the worst outcome over all compatible Lipschitz maps. It pays for this completeness through horizon-dependent joint optimization and the trusted prior.

| Capability | This construction | Important qualification |
|---|---|---|
| Exact finite data consistency | All graph pairs, by extension theorem | Euclidean globally Lipschitz class |
| Worst finite rollout | Gram SDP plus physical rank | SDP alone exact only when rank embeds |
| Checkable safety proof | Nonnegative multipliers and PSD remainder | Numerical solver output must be checked |
| Realizable failure | Rank-valid finite graph and global extension | Not necessarily a short explicit global model |
| Arbitrary learned forecast comparison | Fixed nominal rollout as an objective reference | Adaptive or jointly optimized policies need more structure |
| Exact worst equilibrium | Intersection of Apollonius balls | Strict contraction and exact data |
| Infinite-horizon approximation | Explicit geometric tail | Cost deteriorates as contraction weakens |
| Certification of the regularity prior itself | Not provided | Finite unrestricted measurements do not establish it |

## 7. Why the assumptions cannot be made free

The result separates three resources that are often conflated:

1. **Physical information:** measured transitions and justified error bounds.
2. **Structural information:** a globally applicable Lipschitz or contraction assumption, a sufficient observed state, and a stationary law.
3. **Computation:** a joint optimization and a checked proof object.

Finite measurements alone do not justify the second resource. For a finite set of input points, choose an unobserved open ball and add a smooth compactly supported perturbation of arbitrarily large amplitude to any smooth compatible candidate, leaving every measured value unchanged. Its derivative can be arbitrarily large inside that ball. Thus even restricting to smooth maps does not let finite point measurements establish a particular global Lipschitz constant. This is a direct indistinguishability argument; it is not a claim that physically derived bounds are unavailable.

This construction can certify a proposed surrogate rollout much more tightly than independent pointwise envelopes when the same-law constraints are informative. It can also explain why a claim remains unsupported, and produce a specific compatible counterexample. Its broad scientific consequence is a precise interface between a predictive model and the experiments that support a claim: the certificate states exactly which global assumptions, records, physical dimension, horizon, and computation it uses. It does not identify an unknown mechanism uniquely or remove the need for those assumptions.

## 8. Reproducibility and verification

The accompanying `certify_fixed_law.py` builds the finite-horizon Gram SDP, returns primal and dual numerical candidates, computes exact-data equilibrium balls, and reconstructs a Gram realization. `verify_results.py` checks the two symbolic identities and the exact `L=1` certificate, tests the attaining maps, and compares numerical SDP values to the proved formula. Its output is recorded in `verification_results.json`. Run it with

```bash
python next4_theory/verify_results.py
```

The completed audit verified the two general sum-of-squares identities, the equilibrium completing-square identity, the exact rational rank-two witness, ten vector parameter cases, nine scalar parameter cases, the stepwise gap, squared forecast error, and a controlled noisy-data instance. The largest numerical value error was `2.32×10⁻⁷`, at the degenerate case `L=0`; all positive-`L` cases had error below `1.1×10⁻⁹`. CLARABEL marked `L=0` as `optimal_inaccurate`, which has no effect on its separate constant-map proof. These measured errors describe the numerical run, not a general numerical error guarantee.

The example `L=1/2`, `f(0)=-e`, `x₀=-e` has exact equilibrium support `M*=-2/3` and uniform initial-to-equilibrium bound `R=3`. A tail target `ε=0.01` is met with prefix `H=8`, since `3·(1/2)^9=0.005859375`. This tail calculation does not by itself certify the finite prefix; that remains a separate optimization.

The symbolic identities and explicit maps prove the sharp theorem. The numerical calculations are consistency checks and a demonstration of the general construction, not substitutes for those proofs. No physical data were acquired, no claimed mechanism was learned from hidden data, and no benchmark-based performance claim is made.

## Primary references

[1] M. D. Kirszbraun (1934), *Über die zusammenziehende und Lipschitzsche Transformationen*. Fundamenta Mathematicae 22, 77–108. Original record: <https://eudml.org/doc/212681>. The needed finite-dimensional statement is proved in Section 2 above.

[2] E. K. Ryu, A. B. Taylor, C. Bergeling, P. Giselsson (2020), *Operator Splitting Performance Estimation: Tight Contraction Factors and Optimal Parameter Selection*. SIAM Journal on Optimization 30(3), 2251–2271. <https://doi.org/10.1137/19M1304854>; author preprint <https://arxiv.org/abs/1812.00146>. The retrieved preprint's Fact 2 gives Lipschitz interpolation; its discussion of joint interpolation cautions against simply intersecting separate conditions.

[3] B. Goujaud, C. Moucer, F. Glineur, J. M. Hendrickx, A. B. Taylor, A. Dieuleveut (2024), *PEPit: computer-assisted worst-case analyses of first-order optimization methods in Python*. Mathematical Programming Computation 16, 337–367. <https://doi.org/10.1007/s12532-024-00259-7>; <https://arxiv.org/abs/2201.04040>. Source implementation of the Lipschitz pair constraints: <https://pepit.readthedocs.io/en/0.5.0/_modules/PEPit/operators/lipschitz.html>.

[4] A. Alanwar, A. Koch, F. Allgöwer, K. H. Johansson (2021), *Data-Driven Reachability Analysis Using Matrix Zonotopes*. Proceedings of Learning for Dynamics and Control, PMLR 144. Primary paper: <https://proceedings.mlr.press/v144/alanwar21a/alanwar21a.pdf>.

[5] Y. Huang, Z. Zhang, H. Ahmad, W. Wu, P. Xie, Z. Zeng, A. Alanwar (2026), *Certifying Plans under Model Mismatch: A Trilemma for Reachability from Scarce Data*. <https://arxiv.org/abs/2608.02453>. Comparison above is limited to the retrieved abstract, not an independently audited full implementation.

[6] N. M. Boffi, S. Tu, N. Matni, J.-J. E. Slotine, V. Sindhwani (2021), *Learning Stability Certificates from Data*. Proceedings of the Conference on Robot Learning, PMLR 155. <https://proceedings.mlr.press/v155/boffi21a.html>.
