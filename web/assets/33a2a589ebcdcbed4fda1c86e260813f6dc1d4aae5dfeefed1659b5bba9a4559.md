# Large compact sets with universal linear-recurrence rigidity

**Research draft — 9 October 2026**

**Status.** This manuscript contains a newly derived proof candidate, including the continuum-parameter estimate on which the result depends. It has not been independently refereed or formally verified. The accompanying exact computations check specified finite mechanisms, not the infinite theorem. Historical priority has not been exhaustively established. No claim of resolving the full Erdős similarity conjecture is made.

## Abstract

We construct compact sets of arbitrarily large Lebesgue measure in the unit interval with the following property: every real constant-coefficient linear recurrence sequence taking all its values in the set is eventually periodic. Equivalently, on these positive-measure alphabets, a sequence has finite Hankel rank if and only if it is eventually periodic. In particular, one set excludes every nontrivial affine infinite geometric progression, simultaneously for all ratios. The construction also excludes stable recurrence trajectories with a prescribed vanishing relative error, including all orders of asymptotically linear recurrences with Hölder-small nonlinear remainder. The proof combines a finite random-routing construction from the October 2026 geometric-similarity manuscript with a new selection of test points by the logarithmic size of a Lyapunov state norm. Polynomial sign-condition bounds then control continuously varying recurrence coefficients, initial states, and Lyapunov metrics. A contrasting elementary construction shows that every positive-measure set contains a nondegenerate C¹ image of every fixed geometric progression; consequently, the quantitative regularity restriction cannot simply be omitted.

## 1. Statements and the question settled

Write |E| for Lebesgue measure. A real linear recurrence sequence is a sequence satisfying

\[
 u_{n+d}=\sum_{i=0}^{d-1}c_i u_{n+i}
 \qquad(n\geq0)
 \tag{1.1}
\]

for some finite d and real coefficients. Allowing this identity only for all sufficiently large n gives the same class, because a finite initial segment can be absorbed into a recurrence with additional zero characteristic roots.

### Theorem 1 — Universal recurrence rigidity

For every 0<ε<1 there is a compact, perfect, nowhere-dense set E⊂[0,1], with |E|>1−ε, such that every real linear recurrence sequence that is not eventually periodic has infinitely many terms outside E.

Thus, for every sequence (u_n) with u_n∈E for all n,

\[
 \boxed{
 (u_n)\text{ is a linear recurrence sequence}
 \iff (u_n)\text{ is eventually periodic}.
 }
 \tag{1.2}
\]

The order, coefficients, initial values, and eventual period are not fixed in advance.

### Corollary 2 — Simultaneous geometric avoidance

The same set satisfies

\[
 \forall x\in\mathbb R\ \forall c\ne0\ \forall q\in(0,1),
 \qquad x+cq^n\notin E\quad\text{for infinitely many }n.
 \tag{1.3}
\]

This is a negative answer to Question 1 of Burgin–Goldberg–Keleti–MacMahon–Wang [B], which asks whether every positive-measure measurable set contains some affine infinite geometric progression, with the ratio also free to vary. It is stronger than proving, separately for each fixed q, that there is a q-dependent avoiding set. The latter is the quantifier order in [O].

This does **not** settle the full Erdős similarity conjecture for an arbitrary prescribed infinite set. In particular, the argument below does not treat arbitrary superlacunary null sequences.

### Theorem 3 — Prescribed-modulus robustness

Let ω:[0,1]→[0,∞) be nondecreasing, with ω(0)=0 and ω(t)→0 as t↓0. For every ε>0, E in Theorem 1 can also be chosen to have both of the following properties.

**(a) Perturbed stable orbits.** Let A be an invertible real companion matrix with spectral radius less than one. Let v≠0, w_n=A^n v, and s_n=e_1ᵀw_n. For any x∈ℝ and errors satisfying, eventually,

\[
 |e_n|\leq C\|w_n\|_2\,\omega(\|w_n\|_2),
 \tag{1.4}
\]

where C<∞ may depend on the sequence, the sequence x+s_n+e_n has infinitely many terms outside E.

**(b) Asymptotically linear recurrences.** Suppose s_n→0, the sequence is not eventually zero, and

\[
 w_n=(s_n,\ldots,s_{n+d-1})^T,
 \qquad
 s_{n+d}=\sum_{i=0}^{d-1}c_i s_{n+i}+\xi_n,
 \tag{1.5}
\]

where the companion matrix A of c is invertible and has spectral radius less than one. If, eventually,

\[
 |\xi_n|\leq C\|w_n\|_2\,\omega(\|w_n\|_2),
 \tag{1.6}
\]

then x+s_n has infinitely many terms outside E for every x∈ℝ.

The set depends on ε and on the prescribed modulus ω, but not on d, A, v, x, C, or the individual error sequence. Expressions involving ω are required only once the state norm is at most one.

An important single choice is

\[
 \omega(t)=\frac1{\log(e/t)}\quad(0<t\leq1),\qquad \omega(0)=0.
 \tag{1.7}
\]

It dominates every positive power t^α near zero, up to a constant depending on α. Therefore one E works simultaneously for all α>0 and all remainders O(‖w‖^{1+α}).

## 2. What is inherited and what changes

The proof uses the ordered finite tree, fresh selector entries, first-default argument, local descendant-grid counting, and exceptional-center repair of [O, Sections 3–5]. Those mechanisms are not discoveries of this manuscript. The older random-cell and covering antecedents are discussed explicitly in [O, Section 1].

The additional mechanism here is the following.

1. Windows are indexed by **logarithmic state size**, not by consecutive sequence indices.
2. A Lyapunov norm forces every state-size level to contain an observable scalar value of comparable magnitude, even when scalar terms oscillate or vanish.
3. A finite list of polynomial signs determines both which times are selected and which local grid keys they use, uniformly over all recurrence parameters.
4. The number of these sign patterns has exponential growth only in the *local* window length, multiplied by a polynomial in the global horizon. Increasing the branching number beats that local exponential growth.
5. Open hitting sets have uniform finite-horizon margins. A diagonal choice of physical scales converts those margins into robustness for any prescribed relative-error modulus.

The standard external inputs are a polynomial sign-condition bound [S], finite-dimensional linear algebra, compactness and regularity of Lebesgue measure, and Kronecker's approximation theorem in the final bounded-recurrence reduction. We reproduce the probabilistic and analytic arguments needed here rather than assuming the main theorem of [O].

## 3. A compact normalized family

Fix an order d≥1 and constants

\[
 0<a\leq b<1,\qquad K\geq1,\qquad T\geq1.
\]

For c=(c_0,…,c_{d−1}), set

\[
 A(c)=
 \begin{pmatrix}
 0&1&0&\cdots&0\\
 0&0&1&\cdots&0\\
 \vdots&&&\ddots&\vdots\\
 0&0&0&\cdots&1\\
 c_0&c_1&c_2&\cdots&c_{d-1}
 \end{pmatrix}.
\]

For d=1 this means the 1×1 matrix (c_0). Let Θ=Θ(d,a,b,K,T) consist of triples θ=(c,P,v), where P is symmetric and

\[
 I\preceq P\preceq KI,
 \quad
 a^2P\preceq A^TPA\preceq b^2P,
 \quad
 1\leq v^TPv\leq T^2.
 \tag{3.1}
\]

The family is compact. Indeed, P and v are bounded; moreover

\[
 \|Az\|_2\leq\|Az\|_P\leq b\|z\|_P
 \leq b\sqrt K\|z\|_2,
\]

so the matrix entries, and therefore c, are bounded. All defining inequalities are closed. It is also semialgebraic, though the counting argument only needs its inclusion in a finite-dimensional real parameter space.

Put

\[
 w_n(\theta)=A^nv,\quad
 s_n(\theta)=e_1^TA^nv,\quad
 h_n(\theta)=\|A^nv\|_P.
\]

The companion structure gives

\[
 w_n=(s_n,\ldots,s_{n+d-1})^T,
 \qquad a h_n\leq h_{n+1}\leq b h_n.
 \tag{3.2}
\]

In particular, h_n is strictly decreasing, is never zero, and tends uniformly to zero on Θ.

### Lemma 4 — Uniform periodic hitting

For every ζ>0, there is an open 1-periodic set H, a finite union of intervals per period, of density

\[
 \rho(H)=|H\cap[0,1]|<\zeta,
\]

such that

\[
 \forall x\in\mathbb R\ \forall\theta\in\Theta,
 \qquad x+s_n(\theta)\in H\quad\text{for some }n\geq0.
 \tag{3.3}
\]

When Θ is nonempty and ζ<1, there are also an integer N_H and δ_H>0 such that every pair (x,θ) has an n≤N_H with

\[
 \operatorname{dist}(x+s_n(\theta),\mathbb R\setminus H)>\delta_H.
 \tag{3.4}
\]

The rest of Sections 4–8 proves this lemma.

## 4. Selecting separated points by state size

Set

\[
 \kappa=\frac1{Kd},\qquad \mu=a\kappa.
\]

For t>0, let n(t) be the first n for which h_n≤2^{−t}. Since h_0≥1, n(t)≥1. The preceding state has h_{n(t)−1}>2^{−t}, so

\[
 a2^{-t}<h_{n(t)}\leq2^{-t}.
 \tag{4.1}
\]

At least one coordinate of w_{n(t)} has magnitude at least κh_{n(t)}: in fact the stronger lower bound h_{n(t)}/√(Kd) follows from P≼KI. Choose the first such coordinate, with index r(t)∈{0,…,d−1}, and set

\[
 z_t=s_{n(t)+r(t)}.
\]

Then

\[
 \mu2^{-t}<|z_t|\leq2^{-t}.
 \tag{4.2}
\]

This selection is deterministic once θ is specified. It does not assume any fixed sign of s_n and does not require s_n to be nonzero at every time.

Choose an integer ℓ≥1 such that 2^{−ℓ}≤μ/4. At levels separated by ℓ, (4.2) implies

\[
 |z_{t+\ell}|<\frac14|z_t|.
 \tag{4.3}
\]

Thus selected values at these levels are distinct even if their signs vary.

There is a uniform time bound. Since h_n≤Tb^n,

\[
 n(t)\leq
 \left\lceil\frac{t\log2+\log T}{-\log b}\right\rceil.
 \tag{4.4}
\]

The distinction between **level t**, which measures magnitude, and **time n(t)**, which depends on θ, is essential.

## 5. Ordered windows and nested grids

Fix temporarily a branching number M≥2, tree height D≥1, gap g≥1, and base window width R_0≥1, all integers. Consider the complete ordered M-ary tree of height D. Its edges are listed in preorder: each edge is followed immediately by all the edges below its child before the next sibling edge is listed.

Give every edge leaving a vertex of height h a log-size window [A_e,B_e] of width R_h. Place the windows in preorder, with a gap g between consecutive windows. Their first left endpoint is A_*=4. The widths are chosen from the leaves upward:

\[
 R_1=R_0,\qquad \Sigma_1=MR_1+(M-1)g,
\]

and, for h≥2,

\[
 R_h=\max\{R_0,g+\Sigma_{h-1}\},\qquad
 \Sigma_h=M(R_h+g+\Sigma_{h-1})+(M-1)g.
 \tag{5.1}
\]

Here Σ_h is the total span of a height-h subtree. If B_e^* is the last endpoint in the block consisting of edge e and its child subtree, then

\[
 B_e^*-A_e\leq2R_h.
 \tag{5.2}
\]

For a leaf child this is immediate. Otherwise the span is R_h+g+Σ_{h−1}≤2R_h. For fixed M,D,g, all R_h and all endpoints are O(R_0+1), with constants independent of R_0.

In edge e's window select the levels

\[
 A_e,\ A_e+\ell,\ldots,
 A_e+\lfloor R_h/\ell\rfloor\ell.
 \tag{5.3}
\]

The number of tests on this edge is

\[
 m_h=\lfloor R_h/\ell\rfloor+1\geq R_h/\ell.
 \tag{5.4}
\]

Choose an integer C_g≥8/μ. Attach to endpoint B a dyadic grid with

\[
 N_B=2^{\lceil\log_2(C_g2^B)\rceil},
 \qquad C_g2^B\leq N_B<2C_g2^B.
 \tag{5.5}
\]

Define its periodic key by

\[
 J_B(y)=\lfloor N_B\{y\}\rfloor.
\]

All these grids are nested. A finer key determines every coarser one, including at boundaries under the half-open-cell convention.

### Separation

For one edge, its selected translations, together with zero, are pairwise separated by at least a fixed multiple of μ2^{−B_e}. Specifically, consecutive magnitudes decrease by at least a factor four, so distinct selected translations differ by at least (3μ/4)2^{−B_e}, and each differs from zero by more than μ2^{−B_e}. Their entire range is in [−2^{−A_*},2^{−A_*}], of length at most 1/8. Circular and ordinary distances therefore agree. Since the grid width is at most μ2^{−B_e}/8, these translations from any center have distinct keys at the edge grid. They remain distinct at all finer grids.

### Stability of earlier keys

For a noninitial window e, let B' be its predecessor's endpoint. Call a center x stable if

\[
 \operatorname{dist}(x,N_{B'}^{-1}\mathbb Z)>2^{-A_e}
\]

for every such e. If K_tree is the number of tree edges, the unstable centers have periodic density at most

\[
 4C_gK_{\rm tree}2^{-g}.
 \tag{5.6}
\]

Indeed, the forbidden neighborhood of a predecessor grid has density at most 2N_{B'}2^{−A_e}≤4C_g2^{−g}, and a union bound gives (5.6).

At a stable x, translating by any test point in a later window changes no earlier grid key, because its magnitude is at most 2^{−A_e}. The two-sided distance condition treats positive and negative translations alike.

## 6. Random routing and the exact local failure law

For every nondefault edge (P,i), 1≤i<M, give its grid cells independent fair selector bits. There is no selector on child M, which is the default child. For each leaf L, give the cells of its incoming-edge grid independent Bernoulli-p terminal bits. All bits in all tables are independent.

Route a point y by selecting, at each internal vertex, the first nondefault child whose selector at y is one. Select child M if all preceding selectors are zero. Declare y∈B precisely when the terminal bit at its routed leaf and grid key is one.

For every fixed y, conditional on all selectors, its terminal bit is still Bernoulli-p. Hence

\[
 \mathbb E\rho(B)=p.
 \tag{6.1}
\]

Fix a center x. Expose its addressed entry in **every selector table**, including tables not on its route, and let F_x be the generated sigma-field. These addresses are fixed by x and the deterministic grids, not by θ. The exposed bits determine the center's route.

The probability that this route never uses a default child is

\[
 (1-2^{1-M})^D.
 \tag{6.2}
\]

Suppose an atom of F_x has first default at U, whose height is h. Let e_i=(U,i) for 1≤i<M. Each selector on e_i is zero at x. For a test translation z belonging to e_i's window, define Q_i(x+z) to be the product of its selector on e_i and the terminal bit reached by routing from child i downward.

At a stable center, the actual route of x+z reaches U and rejects children 1,…,i−1: all relevant earlier keys agree with the center's keys. Consequently,

\[
 Q_i(x+z)=1\ \Longrightarrow\ x+z\in B.
 \tag{6.3}
\]

Fix θ. The (M−1)m_h own-edge selectors used by all these tests are mutually independent fresh fair bits conditional on F_x. Within one edge their keys are distinct and avoid the center's key; different edges use different tables.

Now condition on all selectors. The terminal addresses used by the tests are pairwise distinct. Different child subtrees have different leaf tables. Within one child subtree, different leaves also give different tables. If two test points reach the same leaf, that leaf's grid refines their own-edge grid and therefore still distinguishes them. This argument does not require independent downstream routes.

Writing A_ν for the fresh own-edge selectors, the conditional probability that every test fails, given all selectors, is (1−p)^{ΣA_ν}. Averaging these independent selectors gives the exact identity

\[
 \mathbb P(\text{all local tests fail at }\theta\mid F_x)
  =(1-p/2)^{(M-1)m_h}
  \leq\exp\left(-\frac{p(M-1)}{2\ell}R_h\right).
 \tag{6.4}
\]

This is a statement for each fixed parameter θ. The next section makes it simultaneous over the entire compact family without charging the globally finest grid to every test.

## 7. Polynomial signs control the parameter continuum

We use the following classical fact in its all-signs form, so zeros are included.

### Polynomial sign bound

For fixed k, the number of realizable sign vectors of S real polynomials in k variables of degree at most D_alg is at most

\[
 C_k(SD_{\rm alg})^k,
 \tag{7.1}
\]

after harmlessly increasing C_k to cover small S and degrees. See [S, Theorem B]. A weaker fixed-dimension polynomial bound would also suffice, with a correspondingly larger branching number. Counting only strict signs would not suffice at threshold and grid boundaries.

The parameter space (c,P,v) has

\[
 k=2d+\frac{d(d+1)}2
 \tag{7.2}
\]

real coordinates. Let B_max be the last endpoint in the whole tree and set

\[
 N_0=\left\lceil\frac{B_{\max}\log2+\log T}{-\log b}\right\rceil,
 \qquad N=N_0+d.
 \tag{7.3}
\]

All selected scalar values occur at times at most N. For fixed tree parameters other than R_0, N=O(R_0+1).

The scalar s_n is a polynomial in (c,v) of degree at most n+1. The squared norm

\[
 h_n^2=v^T(A^n)^TPA^nv
\]

has degree at most 2n+3 in (c,P,v).

Fix a stable x and an F_x-atom with first default U of height h. Write R=R_h. A finite list of polynomial signs fixes every local test point and its relevant key as follows.

**Selection signs.** For every level t used by a local edge, include the polynomials

\[
 h_n^2-2^{-2t}\qquad(0\leq n\leq N_0),
\]

and include the coordinate-selection comparisons

\[
 s_{n+r}^2-\kappa^2h_n^2
 \qquad(0\leq n\leq N_0,\ 0\leq r<d).
 \tag{7.4}
\]

Their signs determine the first crossing n(t) and first admissible coordinate r(t), with ties handled by the specified ordering.

**Local grid signs.** The entire local test Q_i(y), for any realization of the tables, is determined by the finest grid key J_{B_{e_i}^*}(y) in edge e_i and its child subtree. A selected translation on this edge lies in [−2^{−A_{e_i}},2^{−A_{e_i}}]. This interval meets at most

\[
 2+2N_{B_{e_i}^*}2^{-A_{e_i}}
 \leq2+4C_g2^{2R}
 \tag{7.5}
\]

translated grid boundaries, by (5.2). For each possible scalar time m≤N and each such boundary k_0/N_{B_{e_i}^*}, include

\[
 x+s_m-\frac{k_0}{N_{B_{e_i}^*}}.
 \tag{7.6}
\]

The integers k_0 here range over the actual boundaries in x+[−2^{−A_{e_i}},2^{−A_{e_i}}]; x is fixed. Signs of these polynomials determine the key of the *selected* value. Values at other times outside this interval need not have their keys determined.

Combining these lists, the number S of polynomials can be bounded by

\[
 S\leq C(M-1)(R+1)(N+1)2^{2R},
 \tag{7.7}
\]

and their degrees by 2N+3. The constant may depend on the normalized family but not on R_0.

A sign vector realized in Θ fixes all selected times and all relevant finest keys, hence fixes the complete vector of local test results **for every possible realization of the random tables**. Choose one representative θ for each realized sign vector. These representatives depend on x, U, and deterministic data, but not on any still-unexposed random entry.

By (7.1), and because R and N are O(R_0+1), their number is at most

\[
 C'(R_0+1)^{3k}\exp(2k(\log2)R).
 \tag{7.8}
\]

The constant C' may depend on M, the tree height, and the gap. These are all fixed before R_0 is increased.

If some θ misses B at every time 0,…,N, then all of its local tests fail. The same is true for the representative of its sign vector. Applying (6.4) separately at those representatives gives

\[
 \mathbb P\left(
 \exists\theta\in\Theta\ \forall n\leq N:\ x+s_n(\theta)\notin B
 \ \middle|\ F_x
 \right)
 \leq
 C'(R_0+1)^{3k}e^{-\gamma R_h},
 \tag{7.9}
\]

where

\[
 \gamma=\frac{p(M-1)}{2\ell}-2k\log2.
 \tag{7.10}
\]

This is the central estimate. Global time contributes only a polynomial factor; the exponential contribution comes from the local edge-and-descendant span.

### Choosing the parameters in a noncircular order

Choose p>0 small enough that 6p<ζ. Then:

- Choose M so that γ>0.
- Choose the tree height D so that (6.2) is less than p.
- With this tree fixed, choose g so that (5.6) is less than p.
- Finally choose R_0 sufficiently large that the right side of (7.9) is less than p at every possible height.

The last choice exists: R_h≥R_0, the number of heights is finite, and C'(R_0+1)^{3k}e^{−γR_0}→0. The potentially very large constants produced by the earlier choices do not depend on R_0.

At every stable x, the probability of some normalized parameter missing all times 0,…,N is now at most 2p: at most p for a route with no default, and at most p conditional on the complementary event.

## 8. Repairing all exceptional centers

For each outcome enlarge B to an open periodic finite union B⁺ with

\[
 \rho(B^+)\leq\rho(B)+p.
\]

Define the set of still-exceptional centers using the **fixed** time set 0,…,N:

\[
 R=\{x:\exists\theta\in\Theta,
           \ x+s_n(\theta)\notin B^+\text{ for every }0\leq n\leq N\}.
 \tag{8.1}
\]

It is important not to define R using the discontinuously parameter-selected times. Formula (8.1) instead defines a closed periodic set: modulo one it is the projection of a closed subset of the compact product (ℝ/ℤ)×Θ.

The finite probability space and the bound just proved imply

\[
 \mathbb E\rho(R)\leq3p,
 \qquad
 \mathbb E\rho(B^+)\leq2p.
 \tag{8.2}
\]

For the first inequality, integrate the 2p bound over stable centers and use the density bound p for the unstable centers. Choose an outcome with ρ(R)+ρ(B⁺)≤5p. By outer regularity and compactness on the circle, cover R by an open periodic finite union of intervals V with ρ(V)≤ρ(R)+p. Then

\[
 H=B^+\cup V,
 \qquad \rho(H)\leq6p<\zeta.
 \tag{8.3}
\]

If x∉R, every θ has a hit in B⁺ at one of the fixed finite times. If x∈R, then x∈V and s_n(θ)→0, so x+s_n(θ)∈V for all sufficiently large n. This proves (3.3).

Finally the open sets

\[
 \{(x,\theta):x+s_n(\theta)\in H\},\qquad n\geq0,
\]

cover the compact space (ℝ/ℤ)×Θ. A finite subcover supplies N_H. The continuous function

\[
 (x,\theta)\longmapsto
 \max_{0\leq n\leq N_H}
 \operatorname{dist}(x+s_n(\theta),\mathbb R\setminus H)
\]

is positive everywhere on this compact space, so its minimum is positive. Taking a smaller positive number as δ_H proves (3.4), and finishes Lemma 4.

## 9. One set for all orders, coefficients, scales, and prescribed errors

Fix ε∈(0,1) and ω as in Theorem 3. For every integer j≥2 and each 1≤d≤j, apply Lemma 4 to

\[
 a=1/j,\quad b=1-1/j,\quad K=j,\quad T=j,
 \tag{9.1}
\]

with density budget ε2^{−j}/j. Ignore empty families. Taking the union of these finitely many hitting sets gives an open 1-periodic finite union H_j with

\[
 \rho(H_j)<\varepsilon2^{-j}.
 \tag{9.2}
\]

There is a common finite horizon N_j and margin 0<δ_j≤1 for all the nonempty normalized families at this j.

Choose decreasing dyadic scales r_j=2^{−m_j} so that r_j→0, jr_j≤1, and

\[
 j^5\omega(jr_j)<\delta_j/2.
 \tag{9.3}
\]

This is possible because δ_j>0 is fixed before r_j is chosen and ω(t)→0. Define

\[
 O=\bigcup_{j\geq2}r_jH_j,
 \qquad E_0=[0,1]\setminus O.
 \tag{9.4}
\]

Each r_j is the reciprocal of an integer. Therefore [0,1] comprises an integer number of periods of r_jH_j and

\[
 |(r_jH_j)\cap[0,1]|=\rho(H_j).
\]

Consequently E_0 is compact and

\[
 |E_0|\geq1-\sum_{j\geq2}\rho(H_j)>1-\varepsilon.
 \tag{9.5}
\]

### Exhausting every stable invertible companion matrix

For such a fixed A, the matrix

\[
 P=\sum_{n\geq0}(A^n)^TA^n
 \tag{9.6}
\]

converges and satisfies P−AᵀPA=I. Since A is invertible, AᵀPA is positive definite. Thus, for some constants K_0<∞ and 0<a_0≤b_0<1,

\[
 I\preceq P\preceq K_0 I,
 \qquad a_0^2P\preceq A^TPA\preceq b_0^2P.
 \tag{9.7}
\]

For all sufficiently large j, this same (A,P) satisfies (9.1).

### Proof of Theorem 3(a)

Let h_n=‖A^nv‖_P. For large j choose k_j as the last time h_{k_j}≥r_j. Then

\[
 1\leq h_{k_j}/r_j<1/a_0\leq j.
 \tag{9.8}
\]

Also k_j→∞. The initial state A^{k_j}v/r_j is therefore in the normalized j-family. At center x/r_j, one of its ideal scalar outputs with m≤N_j lies at distance greater than δ_j from H_jᶜ.

For all m≥0, monotonicity of h_n and ω gives

\[
 \frac{|e_{k_j+m}|}{r_j}
 \leq Cj\,\omega(jr_j)
 <\frac{C\delta_j}{2j^4}<\delta_j
 \tag{9.9}
\]

for sufficiently large j. The actual output is still in H_j after normalization, hence x+s_{k_j+m}+e_{k_j+m}∈r_jH_j⊂O. Since k_j→∞, there are infinitely many such terms. This proves part (a).

### Proof of Theorem 3(b)

In state form the recurrence is

\[
 w_{n+1}=Aw_n+e_d\xi_n.
 \tag{9.10}
\]

Use the same fixed P as in (9.6) and set h_n=‖w_n‖_P. Since ‖e_d‖_P≤√K_0,

\[
 (a_0-C\sqrt{K_0}\omega(h_n))h_n
 \leq h_{n+1}
 \leq(b_0+C\sqrt{K_0}\omega(h_n))h_n.
 \tag{9.11}
\]

As h_n→0, for all sufficiently large n this yields

\[
 (a_0/2)h_n\leq h_{n+1}\leq((1+b_0)/2)h_n.
 \tag{9.12}
\]

The state is nonzero at every sufficiently late time. Indeed, if it were zero after the error estimate begins, (9.10) and the zero error bound would make all subsequent states zero, contrary to the hypothesis.

Choose k_j as the last late time with h_{k_j}≥r_j. For large j,

\[
 1\leq h_{k_j}/r_j<2/a_0\leq j,
 \qquad h_{k_j+m}\leq jr_j\quad(m\geq0).
 \tag{9.13}
\]

Compare the actual tail with the ideal orbit starting from its exact current state. Iterating (9.10) gives

\[
 w_{k_j+m}-A^mw_{k_j}
 =\sum_{\nu=0}^{m-1}A^{m-1-\nu}e_d\xi_{k_j+\nu}.
\]

Since P≼jI and ‖A‖_P≤1−1/j for large j,

\[
 \sup_{m\geq0}
 \frac{\|w_{k_j+m}-A^mw_{k_j}\|_P}{r_j}
 \leq Cj^{5/2}\omega(jr_j)
 <\frac{C\delta_j}{2j^{5/2}}<\delta_j.
 \tag{9.14}
\]

Here one factor √j bounds ‖e_d‖_P, one factor j bounds the normalized actual state size, and one factor j bounds the geometric sum of operator norms. No constant depends on the chosen finite hitting horizon.

The scalar observation has error at most this P-norm error because P≽I. Apply the normalized margin for H_j to the ideal orbit. Its corresponding actual scalar term still lies in r_jH_j. Again k_j→∞, proving infinitely many escapes. This completes Theorem 3 for E_0.

## 10. From stable recurrences to all bounded recurrences

We first justify that every nonconstant convergent recurrence is covered by the stable invertible case after taking a tail and, when necessary, lowering its order.

### Lemma 5 — Removing inactive and transient modes

If a real linear recurrence u_n converges to x and is not eventually constant, then some tail of s_n=u_n−x is a nonzero scalar recurrence with an invertible companion matrix of spectral radius less than one.

**Proof.** Subtracting the limit preserves a homogeneous recurrence: if the original coefficient sum differs from one, the limit must be zero. Alternatively, multiplying an annihilating polynomial by z−1 always annihilates the difference.

Form the original companion state and its cyclic span generated by the initial state. Pass to the eventual image of the transition map; the nilpotent part is removed after finitely many steps and the restricted map is invertible. The orbit tends to zero, so the powers of the restricted map tend to zero on a spanning collection of vectors. In finite dimension they tend to zero as operators; all its eigenvalues have modulus less than one.

The scalar observation is observable on this reduced cyclic space. If all future scalar observations of a state vanish, its original consecutive-coordinate state vanishes. Cayley–Hamilton implies that finitely many observations, no more than the reduced dimension, already detect it. Taking the first reduced-dimension consecutive observations as coordinates therefore gives an invertible companion representation. Non-eventual constancy excludes the zero-dimensional case. ∎

Theorem 3(a) with zero errors now excludes every non-eventually-constant convergent recurrence from E_0, in every tail. In particular E_0 contains no interval, since every interval contains a nontrivial convergent geometric progression.

### Lemma 6 — Bounded recurrence dichotomy

If a bounded real recurrence has all its values in a closed set F with no interval, then it is a periodic sequence plus a recurrence tending to zero, up to a finite initial segment.

**Proof.** On the cyclic state space, the powers of the transition matrix are bounded: each state coordinate is bounded, and finitely many orbit states form a basis. Thus its eigenvalues have modulus at most one, and its unit-circle eigenvalues have no nontrivial Jordan blocks. The Jordan decomposition gives

\[
 u_n=p_n+z_n,
 \qquad z_n\longrightarrow0,
 \tag{10.1}
\]

where z_n is a stable recurrence and p_n is a finite linear combination of unit-modulus exponentials.

Write their phases as θ_i. Choose a rational basis 1,τ_1,…,τ_t for the rational span of 1 and the θ_i, and clear the denominators by an integer m. On each residue class modulo m the sequence p_{mn+r} has the form F_r(nτ_1,…,nτ_t), where F_r is a real continuous trigonometric polynomial on a connected torus. Kronecker's approximation theorem makes the argument sequence dense on that torus. Hence the limit-value set of u_{mn+r} is the interval F_r(𝕋^t). It is contained in F by closedness and z_n→0. Because F has no interval of positive length, F_r is constant. Thus p_n is periodic. The case t=0 is already periodic. ∎

This is the standard unit-circle mechanism underlying recurrence value-set results such as [G]; the argument above only uses the bounded case.

### Proof of Theorem 1

Suppose a recurrence has a tail in E_0. It is bounded. Apply Lemma 6 to obtain u_n=p_n+z_n, with p_n periodic and z_n a stable recurrence. Along each residue class of a period of p_n, the original sequence is a convergent recurrence. By Lemma 5 and the stable avoidance already proved, each such residue-class sequence must be eventually constant. Its stable remainder must therefore be eventually zero. There are only finitely many residue classes, so u_n is eventually periodic.

Contraposition proves that every non-eventually-periodic recurrence escapes E_0 infinitely often.

Finally let E be the support of Lebesgue measure restricted to E_0. Then E⊂E_0 is compact, |E|=|E_0|, and E has no isolated points: an isolated support point would carry a positive atom of Lebesgue measure. It is nowhere dense because E_0 contains no interval. All avoidance properties pass to subsets. This proves Theorems 1 and 3 with the stated perfect-set conclusion. ∎

## 11. Structural and dynamical consequences

### 11.1 Finite Hankel rank and rational generating functions

For u∈E^ℕ, consider the infinite Hankel matrix

\[
 \mathcal H_u=(u_{i+j})_{i,j\geq0}.
\]

Finite rank means the span of its columns is finite-dimensional. The shift sends the j-th column to the (j+1)-st column. It is well defined on their span, since shifting any identically zero linear combination gives another zero linear combination. Cayley–Hamilton therefore supplies a constant-coefficient recurrence for u. Conversely a recurrence makes that column span finite-dimensional. Equivalently, the formal power series ∑u_nz^n is rational: multiplying by the recurrence polynomial leaves a polynomial, and the converse follows by comparing coefficients.

Consequently, for this one positive-measure alphabet,

\[
 \boxed{
 \operatorname{rank}\mathcal H_u<\infty
 \iff \sum_{n\geq0}u_nz^n\in\mathbb R(z)
 \iff u\text{ is eventually periodic}.
 }
 \tag{11.1}
\]

Eventual periodicity cannot be removed from the statement: every set containing two points contains a nonconstant periodic sequence, and every periodic sequence satisfies a constant-coefficient recurrence. Thus the permitted recurrence class is the smallest one that any nontrivial alphabet can allow.

This is a structural theorem, not an efficient recognition algorithm from finite samples.

### 11.2 Nonlinear images of geometric progressions

Take ω from (1.7). If f is defined near zero and

\[
 f(t)=x+ct+O(|t|^{1+\alpha}),\qquad c\ne0,\quad\alpha>0,
\]

then f(q^n) is a power-small perturbation of x+cq^n. Theorem 3(a) shows that infinitely many of these values lie outside E, simultaneously for all q∈(0,1), all α>0, and all such f.

If f is nonconstant and real analytic near zero, its first nonzero Taylor term has some finite order m:

\[
 f(t)=x+ct^m+O(|t|^{m+1}),\qquad c\ne0.
\]

Apply the same result to ratio q^m and exponent 1/m. Thus E contains no full tail of a nonconstant real-analytic image of any geometric progression, even when f'(0)=0.

For a C¹ germ with derivative modulus η, a Dini condition ∫_0^1η(t)dt/t<∞ gives η(t)≤C/log(1/t) for small t, since η is nondecreasing. The integral formula for the Taylor remainder then puts a nondegenerate Dini-C¹ germ in the same class. Arbitrary C¹ germs are different; see Section 12.

### 11.3 Stable nonlinear recurrences of every finite order

Let F be C^{1,α} near (x,…,x), with F(x,…,x)=x. Let A be the companion matrix whose last row is DF(x,…,x). Assume A is invertible and has spectral radius less than one. Any non-eventually-constant solution of

\[
 u_{n+d}=F(u_n,\ldots,u_{n+d-1}),\qquad u_n\longrightarrow x,
\]

has, after subtracting x, a remainder O(‖w_n‖^{1+α}) in (1.5). Theorem 3(b) excludes a full tail of this solution from E. This is simultaneous over d, α, F, and x.

For d=1, E therefore cannot contain a nonstationary orbit converging to a hyperbolic attracting fixed point of any C^{1,α} map with nonzero derivative at that fixed point. Superattracting derivatives and arbitrary flat behavior are not covered.

### 11.4 A quantitative nonlacunary consequence

Suppose a_n>0 decreases to zero and

\[
 0\leq a_n-a_{n+1}\leq C a_n^{1+\alpha}
\]

eventually, for some α>0. For a fixed q∈(0,1), let n(k) be the first index with a_{n(k)}≤q^k. The preceding term is eventually at most 2q^k, since its relative drop tends to zero. Hence

\[
 a_{n(k)}=q^k+O(q^{(1+\alpha)k}).
\]

For large k these crossings occur at distinct indices, because the relative gaps tend to zero whereas successive target levels have fixed ratio q. Theorem 3(a) excludes a full tail of x+c a_n, for every c≠0. Thus the same E also simultaneously excludes, for example, all translates and nonzero dilates of (n^{−β}) for all β>0.

This does not cover arbitrary decreasing sequences with ratio tending to one without a prescribed rate, and it does not assert an equivalence for all such sequences.

## 12. Why unrestricted C¹ perturbations cannot be excluded

### Proposition 7 — C¹ geometric universality

For every measurable F⊂ℝ of positive measure and every fixed q∈(0,1), there is an increasing C¹ diffeomorphism φ:ℝ→ℝ such that

\[
 \phi(q^n)\in F\quad(n\geq1),\qquad \phi'(0)>0.
 \tag{12.1}
\]

**Proof.** Choose a Lebesgue density point x∈F. There are b_n∈F with

\[
 b_n=x+q^n+o(q^n).
 \tag{12.2}
\]

To see this directly, write D_n=|[x-2q^n,x+2q^n]\setminus F|/q^n→0. Choose η_n→0 with 2η_n>D_n and η_n<1 eventually. The interval centered at x+q^n of radius η_nq^n lies in the displayed larger interval and cannot be disjoint from F.

The secant slopes of these selected points satisfy

\[
 \frac{b_n-b_{n+1}}{q^n-q^{n+1}}\longrightarrow1.
\]

Choose a sufficiently late tail and relabel its targets: y_n=b_{N+n}. Its secant slopes σ_n on [q^{n+1},q^n] converge to c=q^N>0 and can all be arranged to satisfy |σ_n−c|≤c/4.

Let ψ(t)=6t(1−t) on [0,1]. It has integral one, vanishes at the endpoints, and lies between zero and 3/2. On [q^{n+1},q^n], define

\[
 g(t)=c+(\sigma_n-c)
 \psi\left(\frac{t-q^{n+1}}{q^n-q^{n+1}}\right).
\]

Set g(0)=c and set g=c on (−∞,0] and [q,∞). This is continuous, since it takes the value c at every joining point and σ_n→c. It satisfies g≥5c/8>0.

Define φ(t)=x+∫_0^t g(s)ds. The integral of g over each interval is exactly y_n−y_{n+1}; telescoping toward zero gives φ(q^n)=y_n∈F. The positive derivative and affine behavior outside a bounded interval make φ an increasing global C¹ diffeomorphism. ∎

Consequently the prescribed modulus in Theorem 3 cannot be replaced by an unspecified o(‖w‖) that ranges over all rates at once. The quantifier order

\[
 \forall\omega\ \exists E_\omega
\]

must not be exchanged for

\[
 \exists E\ \forall\omega.
\]

There is also a dynamical formulation. The C¹ map

\[
 T=\phi\circ(t\mapsto qt)\circ\phi^{-1}
\]

has a hyperbolic attracting fixed point φ(0), with derivative q there, and its orbit through φ(q) lies in F. Thus the contrast between the constructed set and arbitrary positive-measure sets persists for attracting C¹ dynamics, not just for pointwise interpolation.

## 13. Construction, checks, and remaining verification status

The construction is an existence construction with a specified order of choices: finite normalized classes, finite trees and random tables, finite polynomial-sign representatives, open exceptional-center repair, then a countable union at sufficiently small dyadic scales. Its parameter sizes are enormous. No practical complexity bound or explicit numerical materialization of E is asserted.

The companion script `verify_mechanisms.py` performs exact rational checks of the following finite mechanisms:

- Lyapunov identities and strict two-sided norm bounds for repeated-root, oscillatory/zero-containing, and mixed-sign recurrence fixtures.
- Log-size selection, separation, and periodic-grid distinctness on those fixtures.
- 14,796 edge-and-descendant span checks over 144 tree-parameter choices.
- Enumeration of 65,536 selector/terminal configurations, recovering the exact four-test failure probability (1−(1/3)/2)^4=625/1296.
- The exact interpolation integrals and positivity constant in Proposition 7.

All these diagnostics passed in the recorded run. They do not check the whole construction or independently certify Lemma 4. The mathematically decisive audit targets are the uniform sign-pattern estimate (7.8), the conditioning order in Section 6, and the fixed-time compact projection in Section 8. Their derivations are included in full above.

The claimed scope is the theorem stated here, not a blanket historical-importance assessment. The complete arbitrary-sequence Erdős similarity conjecture, practical construction complexity, formal verification, independent referee validation, and exhaustive priority review are not established by this manuscript.

## References and source versions

**[B]** Alex Burgin, Samuel Goldberg, Tamás Keleti, Connor MacMahon, and Xianzhi Wang. *Large sets avoiding infinite arithmetic / geometric progressions.* arXiv:2210.09284v1, 17 October 2022; Question 1. Primary HTML text accessed 9 October 2026.

**[O]** OpenAI mathematical manuscript collection. *The geometric case of the Erdős similarity conjecture.* 5 October 2026. Repository `openai/math`, commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Original TeX sections `01-introduction.tex`, `01-history.tex`, `03-windows.tex`, `04-routing.tex`, and `05-scales.tex` under `preprints/The-geometric-case-of-the-Erdos-similarity-conjecture-October-5-2026/build/sections/` were read. The fixed-ratio main theorem is not used as a black box; the routing mechanism is explicitly credited and reconstructed.

**[S]** Saugata Basu and Laxmi Parida. *Bounds on the realizations of zero-nonzero patterns and sign conditions of polynomials restricted to varieties and applications.* arXiv:2411.11729v2, 4 April 2025. Theorem B records the classical all-sign-condition bound used in (7.1).

**[G]** Stefan Gerhold. *The Shape of the Value Sets of Linear Recurrence Sequences.* arXiv:0903.4043v1, 2009; Journal of Integer Sequences 12 (2009), Article 09.3.6. The bounded unit-circle mechanism and its Kronecker-theorem foundation are relevant background for Lemma 6.

**Astra source scope.** Repository `harjassand/astra-research-knowledge`, commit `f22f2cd448ad9660d37dda979d0b115faaaed577`. The entry instructions, topic routing, and scoped frontier were consulted. No Astra candidate mathematical theorem is assumed as a premise of this proof. The new branch arose from direct examination of [O], rather than continuation of an Astra quantum or Liouville candidate.
