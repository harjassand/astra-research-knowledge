# Dynamic data-processing rigidity

**Research date:** 10 October 2026.  
**Status:** A complete internal mathematical argument is given below. Original priority, independent expert validation, and formal certification are not established. This record does not assert that the requested civilization-historic significance threshold has been reached.

## 1. The result

A divergence is a family of finite functions
\[
D_n:\Delta_n^\circ\times\Delta_n^\circ\longrightarrow[0,\infty),
\qquad D_n(q,q)=0,
\]
where \(\Delta_n^\circ\) is the strictly positive probability simplex. Different finite alphabet sizes are part of the same family. Probabilities are row vectors.

Assume **data processing**: whenever \(K\) is a rectangular stochastic matrix and its output distributions have full support,
\[
D_m(pK,qK)\leq D_n(p,q).
\tag{1}
\]
For each fixed \(q\), assume that \(D_n(\cdot,q)\) is continuous on the open simplex and twice continuously differentiable away from \(p=q\). In particular, neither differentiability at equilibrium nor any regularity in the reference argument is assumed.

A Markov generator \(L\) has nonnegative off-diagonal entries and zero row sums. Reversibility with respect to \(q\) means
\[
q_iL_{ij}=q_jL_{ji}.
\]

### Theorem 1 — Full reversible classification

Under these assumptions, the following statements are equivalent.

**(a)** For every finite alphabet, every full-support \(p,q\), and every irreducible \(q\)-reversible generator \(L\), the function
\[
t\longmapsto D_n(pe^{tL},q)
\]
is convex on \([0,\infty)\).

**(b)** There is a single function
\[
\Psi\in C([0,\infty))\cap C^2((0,\infty))
\]
such that
\[
\boxed{D_n(p,q)=\Psi\!\left(\chi^2(p\Vert q)\right)},
\qquad
\chi^2(p\Vert q)=\sum_i\frac{(p_i-q_i)^2}{q_i},
\tag{2}
\]
and
\[
\boxed{\Psi(0)=0,\qquad \Psi'(s)\geq0,\qquad
\Psi'(s)+s\Psi''(s)\geq0\quad(s>0).}
\tag{3}
\]
Equivalently, \(x\mapsto\Psi(e^x)\) is nondecreasing and convex. This is convexity **on the logarithmic argument scale**, not log-convexity of \(\Psi\).

No tensor-additivity assumption, trace-form assumption, or prescribed family of divergences is used in this theorem.

### Corollary 2 — The additive member is unique

If the divergence in Theorem 1 is also tensor-additive, then
\[
\boxed{D_n(p,q)=c\log\bigl(1+\chi^2(p\Vert q)\bigr),\qquad c\geq0.}
\tag{4}
\]
Thus it is a nonnegative multiple of order-two Rényi divergence.

### Corollary 3 — The third derivative already obstructs universal positive spectra

In this additive class, imposing in addition
\[
\frac{d^3}{dt^3}D_n(pe^{tL},q)\leq0
\]
for every finite reversible relaxation forces \(D=0\). Consequently no nonzero member is completely monotone along every reversible relaxation.

### Theorem 4 — Without reversibility there is no nonzero member

Under the regularity and data-processing assumptions above, requiring convex relaxation along **every** irreducible finite Markov generator with stationary reference distribution forces
\[
\boxed{D=0.}
\tag{5}
\]
Tensor additivity is not needed for this conclusion.

## 2. What state refinement supplies exactly

The key device is not an assumed form of the divergence. It is the exact behavior of derivatives under splitting a state into statistically identical copies.

### 2.1 Sufficient splitting is an equality

Split state \(b\) into \(m\) identical labels, replacing
\[
(p_b,q_b)\quad\text{by}\quad(p_b/m,q_b/m),\ldots,(p_b/m,q_b/m).
\]
Splitting and merging are stochastic maps, and their composition is the identity on the original experiment. Applying (1) in both directions gives equality of divergence, for all nearby original \(p\), not merely at one point.

For ordinary derivatives one may use the homogeneous extension
\[
F_q(x)=D_n\!\left(\frac{x}{\sum_i x_i},q\right)
\]
on positive vectors near the probability vector under consideration. Its restriction to probability tangent directions is the original function. Splitting preserves total mass, so all splitting identities also hold for this extension.

Fix \(p\neq q\), and write \(g_i=\partial_iF_q(p)\). At the equally split point, symmetry under permutations of the \(m\) clones implies that all clone gradient coordinates are equal. Differentiating the splitting equality identifies this common coordinate with \(g_b\); the other gradient coordinates remain unchanged.

### 2.2 Exact transverse Hessian scaling

Let \(\gamma_m\) denote the eigenvalue of the split Hessian on the subspace of clone variations whose coordinates sum to zero. Permutation invariance makes that restriction a scalar multiple of the ordinary Euclidean inner product. It also makes all mixed Hessian terms between this subspace and the permutation-invariant directions vanish.

Refine each of the \(m\) clones into \(k\) equal subclones. A transverse variation \(v_j\) is replaced by \(k\) entries \(v_j/k\). Differentiating the splitting equality twice gives
\[
\gamma_{mk}\sum_jk(v_j/k)^2=\gamma_m\sum_jv_j^2,
\qquad \gamma_{mk}=k\gamma_m.
\]
Comparison through a common refinement with two clones gives
\[
\boxed{\gamma_m=m\gamma_2/2.}
\tag{6}
\]
Moreover \(\gamma_m\geq0\): a transverse perturbation leaves the merged experiment fixed, so data processing makes the split divergence attain a local minimum on these perturbations at the equal-clone point.

Put
\[
\kappa=q_b\gamma_2/2\geq0,
\qquad \epsilon=q_b/m.
\]
Then \(\gamma_m=\kappa/\epsilon\). The number \(\kappa\) depends on the original experiment and the state being split, but **not** on \(m\).

For any split-space probability tangent vector \(v\), let \(Mv\) be its merged vector and \(V_b\) the sum of its clone components. The full Hessian identity is
\[
\boxed{
\operatorname{Hess}F^{(m)}(v,v)
=\operatorname{Hess}F(Mv,Mv)
+\gamma_m\sum_{j=1}^m(v_j-V_b/m)^2.
}
\tag{7}
\]
There is no hidden uniform-in-dimension smoothness hypothesis: (6) derives the required control from the finite Hessian at the two-clone experiment.

## 3. The rare-clone curvature identity

Choose three states of the original experiment with distinct ordered likelihood ratios
\[
r_a=a<r_b=b<r_c=c,
\qquad r_i=p_i/q_i.
\]
Here the state labels \(a,b,c\) and their displayed likelihood values are distinguished by context; \(q_a,q_b,q_c\) denote the original reference weights.

Split state \(b\) into \(m\) equal clones, and select one clone \(z\) with reference mass \(\epsilon=q_b/m\). Connect only \(a\leftrightarrow z\leftrightarrow c\), with symmetric conductances
\[
q_aL_{az}=q_zL_{za}=\epsilon k,
\qquad q_zL_{zc}=q_cL_{cz}=\epsilon\ell,
\qquad k,\ell>0.
\tag{8}
\]
Other states are temporarily isolated.

The convexity assumption extends to this reducible generator: add a positive multiple of the reset generator \(\mathbf1q-I\), apply the assumption, and let that multiple decrease to zero. At a fixed nonequilibrium point, the second derivative is continuous in the matrix entries of \(L\).

For reversible generators the likelihood-ratio column evolves by \(r_t=e^{tL}r\). Define
\[
X=k(b-a)>0,\qquad Y=\ell(c-b)>0,\qquad d=Y-X.
\]
At time zero,
\[
r_a'=\epsilon X/q_a,\qquad r_z'=d,\qquad
r_c'=-\epsilon Y/q_c.
\tag{9}
\]
All other clone velocities are zero. The merged probability velocity is \(\epsilon w\), where
\[
w_a=X,\quad w_b=d,\quad w_c=-Y,
\]
and all other entries vanish.

Direct application of the generator a second time gives
\[
\begin{aligned}
p_a''&=\epsilon k d-\epsilon^2kX/q_a,\\
p_z''&=-\epsilon(k+\ell)d+\epsilon^2(kX/q_a-\ell Y/q_c),\\
p_c''&=\epsilon\ell d+\epsilon^2\ell Y/q_c.
\end{aligned}
\tag{10}
\]

Define the two gradient chord slopes
\[
A=\frac{g_b-g_a}{b-a},\qquad
B=\frac{g_c-g_b}{c-b}.
\tag{11}
\]
Both are nonnegative. Indeed, a reversible transition on any single pair gives
\[
\frac d{dt}D(p_t,q)\bigg|_{0}
=w_{ij}(g_i-g_j)(r_j-r_i)\leq0
\]
by data processing, hence the gradient coordinates are ordered with the likelihood ratios.

Combining (7), (9), and (10) gives the **exact identity**
\[
\boxed{
\left.\frac{d^2}{dt^2}D_{n-1+m}(p^{(m)}e^{tL_m},q^{(m)})\right|_{t=0}
=\epsilon Q+\epsilon^2R,
}
\tag{12}
\]
where
\[
\boxed{
Q=(X-Y)\big[(\kappa+A)X-(\kappa+B)Y\big],
}
\tag{13}
\]
\[
R=\operatorname{Hess}F(w,w)
+\frac{AX^2}{q_a}+\frac{BY^2}{q_c}
-\frac{\kappa d^2}{q_b}.
\tag{14}
\]
All terms in \(Q\) and \(R\) are independent of \(m\).

For clarity, the first-order coefficient before factorization is
\[
\kappa(Y-X)^2+(Y-X)(-AX+BY),
\]
which is (13).

Convexity for all clone numbers implies \(Q\geq0\) for all positive \(X,Y\). This is possible only if
\[
\boxed{A=B.}
\tag{15}
\]
If \(\kappa+A>0\) and \(A\neq B\), set \(Y=1\) and
\[
X=\frac{2\kappa+A+B}{2(\kappa+A)}>0.
\]
Then
\[
Q=-\frac{(A-B)^2}{4(\kappa+A)}<0.
\tag{16}
\]
If \(\kappa+A=0\), then \(\kappa=A=0\), and \(B>0\) would make (13) negative for any \(X>Y\). Thus (15) follows in all cases.

This is also a constructive witness rule: when \(Q<0\), choosing any integer
\[
m>q_b\max(R,0)/(-Q),\qquad m\geq2,
\]
makes the exact curvature negative. A sufficiently small irreducible perturbation retains the strict negative sign.

## 4. From gradient chords to a global invariant

### 4.1 The gradient is affine in the likelihood ratio

Equation (15) holds for every triple of distinct likelihood values at every experiment. Therefore all points \((r_i,g_i)\) lie on one affine line.

Repeated likelihood values also have equal gradient coordinates. To see this, merge two equal-likelihood states and then split them back with their reference proportions. At the original point there is equality in data processing. A perturbation that preserves the merged distribution has a local minimum there, so its first derivative vanishes, giving equality of the two gradient coordinates.

Consequently, also when there are only two distinct likelihood values, there are scalars \(u,v\), depending on the experiment, with
\[
g_i=u+v r_i.
\tag{17}
\]
For probability tangent vectors,
\[
dF=\frac v2\,d\chi^2.
\tag{18}
\]
Thus \(D\) is constant along each connected piece of a fixed-\(\chi^2\) surface. It remains to address global connectedness and reference dependence; neither may be silently assumed.

### 4.2 Uniform reference: connectedness modulo permutations

Take the uniform reference on \(N\) points and write
\[
p=\frac1N\mathbf1+u,\qquad \sum_i u_i=0,\qquad \|u\|=R>0.
\]
By permutation invariance arrange \(u_1\geq\cdots\geq u_N\). Define the same-radius one-spike vector
\[
w=R\left(\sqrt{\frac{N-1}{N}},
-\frac1{\sqrt{N(N-1)}},\ldots,
-\frac1{\sqrt{N(N-1)}}\right).
\]
Its corresponding probability vector is strictly positive because
\(\chi^2=NR^2<N-1\).

The short great-circle arc from \(u\) to \(w\) stays in the ordered positive simplex. Here is an explicit verification. Let
\[
\cos\theta=\frac{u\cdot w}{R^2}
=\sqrt{\frac N{N-1}}\frac{u_1}{R},
\qquad 0\leq\theta<\pi/2.
\]
If \(u=w\) there is nothing to prove. Otherwise write the arc as
\[
u(t)=\cos t\,u+\sin t\,
\frac{w-\cos\theta\,u}{\sin\theta},
\qquad 0\leq t\leq\theta.
\]
It is a positive linear combination of \(u,w\), so coordinate ordering is preserved. Since every \(u_i\) lies between \(u_N\) and \(u_1\),
\[
(u_1-u_i)(u_i-u_N)\geq0.
\]
Summing and using the zero mean gives
\[
u_1(-u_N)\geq R^2/N.
\]
This implies \(u_N'(0)\geq0\) along the arc. The last coordinate remains negative as a positive combination of two negative last coordinates, and consequently
\(u_N''(t)=-u_N(t)>0\). Therefore the minimum coordinate never decreases. Strict positivity is preserved throughout the arc.

Equation (18) makes \(D\) constant on the arc. Every ordered point at this radius reaches the same one-spike vector, and permutations preserve \(D\). Hence for uniform reference
\[
D_N(p,\mathbf1/N)=\Psi_N(\chi^2(p\Vert\mathbf1/N)).
\]
For \(N=2\), the two points on each nonzero level are simply related by a permutation. The equilibrium level is fixed by normalization.

Each \(\Psi_N\) is continuous on \([0,N-1)\) and \(C^2\) on \((0,N-1)\).

### 4.3 One function across all alphabets and rational references

Splitting every state into \(M\) equal clones changes a uniform reference on \(N\) points into a uniform reference on \(NM\) points while preserving both divergence and \(\chi^2\). Thus \(\Psi_N=\Psi_{NM}\) on their common interval. Comparing \(N,M\) through \(NM\) gives one function \(\Psi\) on \([0,\infty)\).

If a reference vector \(q\) has rational entries, split coordinate \(i\) into \(Nq_i\) equal subcoordinates, for a common denominator \(N\). The refined reference is uniform, all likelihood ratios are unchanged, and sufficient splitting gives (2).

### 4.4 Irrational references: an exact data-processing sandwich

No continuity in \(q\) was assumed. Let rational full-support \(q_j\to q\).

There exist stochastic matrices \(K_j\to I\) with \(qK_j=q_j\): choose \(\delta_j\downarrow0\) sufficiently slowly that
\[
v_j=q+(q_j-q)/\delta_j
\]
is a probability vector, and set
\(K_j=(1-\delta_j)I+\delta_j\mathbf1v_j\).
Then
\[
D(pK_j,q_j)\leq D(p,q).
\]
The left side is known from rational-reference classification and converges to \(\Psi(\chi^2(p\Vert q))\).

Similarly choose \(H_j\to I\) with \(q_jH_j=q\), using the same reset form. For large \(j\), there is a full-support probability vector \(p_j\to p\) with \(p_jH_j=p\). Explicitly, if
\(H_j=(1-\eta_j)I+\eta_j\mathbf1w_j\), take
\(p_j=(p-\eta_jw_j)/(1-\eta_j)\).
Therefore
\[
D(p,q)\leq D(p_j,q_j)\longrightarrow
\Psi(\chi^2(p\Vert q)).
\]
Both bounds prove (2) for every full-support reference.

## 5. Exactly which scalar functions work

The reset trajectory has \(s(t)=s_0e^{-2t}\). Data processing gives
\[
-2s\Psi'(s)\leq0,
\]
and time convexity gives
\[
4s[\Psi'(s)+s\Psi''(s)]\geq0.
\]
Every \(s>0\) is realizable on a finite alphabet, so (3) is necessary.

Conversely, the output likelihood ratio under a stochastic map is the conditional expectation of the input likelihood ratio. Conditional Jensen gives contraction of \(\chi^2\). Since \(\Psi\) is nondecreasing, (2) satisfies data processing.

For a reversible generator, expand the likelihood deviation in a \(q\)-orthonormal eigenbasis:
\[
s(t)=\chi^2(p_t\Vert q)=\sum_j a_j e^{-2\lambda_jt},
\qquad a_j\geq0,\ \lambda_j>0.
\]
For \(s(t)>0\), Cauchy--Schwarz gives
\[
s''(t)-\frac{s'(t)^2}{s(t)}\geq0.
\]
Consequently,
\[
\frac{d^2}{dt^2}\Psi(s(t))
=
\left(\Psi''(s)+\frac{\Psi'(s)}s\right)s'^2
+\Psi'(s)\left(s''-\frac{s'^2}s\right)\geq0.
\]
At equilibrium the trajectory is constant. This proves sufficiency and completes Theorem 1.

Examples include \(\Psi(s)=s^\alpha\) for every \(\alpha>0\), \(\Psi(s)=\log(1+s)\), and \(\Psi(s)=e^s-1\). The fractional powers illustrate why smoothness at equilibrium was not imposed.

## 6. Additivity and the sharp finite-order obstruction

For independent pairs,
\[
1+\chi^2(p\otimes r\Vert q\otimes v)
=(1+\chi^2(p\Vert q))(1+\chi^2(r\Vert v)).
\]
Additivity is therefore equivalent to
\[
\Psi(s+t+st)=\Psi(s)+\Psi(t).
\]
The continuous function \(f(x)=\Psi(e^x-1)\) on \([0,\infty)\) satisfies Cauchy's additive equation there. Thus \(f(x)=cx\), with \(c\geq0\), proving Corollary 2.

For the third-order obstruction, use
\[
q=(1/10,9/10),\qquad p=(7/10,3/10),\qquad
L=\begin{pmatrix}-9/10&9/10\\1/10&-1/10\end{pmatrix}.
\]
This is irreducible and reversible, and
\[
D_2(p_t\Vert q)=\log(1+4e^{-2t}).
\]
At \(t_*=(\log2)/2\),
\[
\frac{d^3}{dt^3}D_2(p_t\Vert q)\bigg|_{t=t_*}=16/27>0.
\]
This proves Corollary 3 for \(c>0\). The second-order requirement is sharp in this sense: \(D_2\) passes it for every reversible chain but fails the next derivative sign.

There is also a nonlinear second-order obstruction. On a reset trajectory \(f(t)=\log(1+se^{-2t})\), writing \(z=se^{-2t}>0\),
\[
f f''-(f')^2
=\frac{4z}{(1+z)^2}[\log(1+z)-z]<0.
\]
Thus this profile is strictly log-concave, whereas a positive Laplace mixture is log-convex. This provides another direct obstruction to a positive relaxation-spectrum interpretation.

## 7. The nonreversible impossibility theorem

Requiring convexity for all stationary chains first imposes Theorem 1, since reversible chains are included. It remains to show that any nonconstant admissible \(\Psi\) fails on a three-state directed cycle.

Fix \(0<a<1<c\), and choose
\[
(a+c)/2<b<c.
\]
For small \(\epsilon>0\), give the three states likelihood ratios \((b,c,a)\) and reference weights
\[
q_1=\epsilon,
\qquad q_2=\frac{1-a}{c-a}-\epsilon\frac{b-a}{c-a},
\qquad q_3=\frac{c-1}{c-a}-\epsilon\frac{c-b}{c-a}.
\]
These satisfy \(\sum q_i=\sum q_ir_i=1\) and remain strictly positive.

Define a generator \(A\) **on likelihood-ratio columns** by
\[
(Ar)_i=\frac{r_{i+1}-r_i}{q_i}
\]
with cyclic indices. It has zero row sums and stationary row vector \(q\). The corresponding probability-row generator is its weighted adjoint
\[
L=Q^{-1}A^{\mathsf T}Q,\qquad Q=\operatorname{diag}(q).
\]
It is an irreducible directed cycle, and \(p_t=pe^{tL}\) has likelihood column \(r_t=e^{tA}r\).

Let \(\delta_i=r_{i+1}-r_i\), and put \(s(t)=\chi^2(p_t\Vert q)\). Direct differentiation yields
\[
s'(0)=-\sum_i\delta_i^2,
\qquad
s''(0)=2\sum_i\frac{\delta_i(\delta_i-\delta_{i-1})}{q_i}.
\]
The rare-state term is
\[
\frac{2(c-b)(a+c-2b)}\epsilon<0,
\]
while all other terms stay bounded. Meanwhile,
\[
s(0)\longrightarrow (1-a)(c-1),
\]
and \(s'(0)\) remains bounded.

Every positive value of \((1-a)(c-1)\) is possible. If \(\Psi'(s_*)>0\) for any \(s_*>0\), choose \(a,c\) with that limiting variance. Then
\[
\Psi''(s)s'^2+\Psi'(s)s''\longrightarrow-\infty,
\]
contradicting convexity. Therefore \(\Psi'=0\) on \((0,\infty)\). Continuity and \(\Psi(0)=0\) give \(\Psi=0\), proving Theorem 4.

The divergent rates do not require an unbounded-rate assumption: multiplying each generator by a positive scalar preserves the sign of time curvature, so each witness can be rescaled to have maximum jump rate one.

## 8. A regularity-free additive strengthening

This section has a different domain and an explicit established input. It must not be silently substituted into a theorem about divergences defined only on finite alphabets.

Consider divergences on probability pairs on all Polish spaces, possibly infinite-valued, normalized on identical pairs, additive, satisfying data processing, and finite whenever the likelihood ratio is bounded above and away from zero. Mu, Pomatto, Strack, and Tamuz, *From Blackwell Dominance in Large Samples to Rényi Divergences and Back Again*, Theorem 2, prove the representation
\[
D(P,Q)=\int_{[1/2,\infty]}D_\alpha(P\Vert Q)\,d\mu(\alpha)
+\int_{[1/2,\infty]}D_\alpha(Q\Vert P)\,d\nu(\alpha),
\tag{19}
\]
for finite positive Borel measures \(\mu,\nu\), on every bounded pair. This representation is prior work, not a contribution of this record.

Under that domain and those axioms, convex relaxation on **three-state reversible paths alone** forces \(D=cD_2\) on every bounded pair, with no regularity assumption on \(D\). A proof is in the companion file `regularity_free_additive_classification.md`. The third-order zero conclusion follows from the same two-state example.

## 9. Exact computations and scope

`check_dynamic_rigidity.py` checks the curvature factorization, its negative minimum, the clone-Hessian scaling identity, the rational Rényi-3 counterexample, the directed-cycle formulas, and the Rényi-2 third derivative.

For the reversible Rényi-3 example, take
\[
q=(2(1-\epsilon)/3,\epsilon,(1-\epsilon)/3),\quad r=(1/2,1,2),
\]
and path conductances \(17\epsilon/7\), \(\epsilon\). The exact curvature is
\[
D_3''(0)=\frac{27\epsilon(144\epsilon^2-4843\epsilon+77)}
{196(\epsilon-1)(7\epsilon-11)^2}.
\]
At \(\epsilon=1/1000\), this is
\[
-18039286/219093886837<0.
\]
These are exact algebraic checks, not a formal verification of the universal classification.

The classification concerns finite experiments and universal quantifiers over chains. It does not claim that KL or other divergences fail to be convex for every particular chain. It does not invalidate ordinary data processing or entropy monotonicity. The nonreversible theorem has no tensor-additivity assumption; the reversible theorem does have the stated regularity assumption. The regularity-free extension uses the separate all-Polish-space representation theorem and concludes only on bounded pairs.

## 10. Research status and comparison

The proof mechanism developed here combines exact sufficient-refinement Hessian scaling with a rare-clone curvature test, then supplies the global level-set and irrational-reference arguments needed for a full classification. The refinement step is related in spirit to classical monotone-metric arguments; no claim is made to invent Fisher geometry or data processing.

Closest comparison topics include characterization of additive divergences, universal Markov Lyapunov functions, and convex entropy decay for fixed generators. Focused searches did not locate this precise combined classification, but this is not a priority determination.

A separately investigated all-copy Werner-state route did not produce its indispensable rank-two partial-trace inequality. Linear-program relaxations of code enumerator constraints admitted negative values; those feasible relaxed data were not shown to come from quantum states and are not entanglement counterexamples. No NPT bound-entanglement claim is made.

**The completed theorems above do not establish that the requested civilization-historic breakthrough objective has been achieved.**

### References for established inputs and comparison

- X. Mu, L. Pomatto, P. Strack, O. Tamuz, *From Blackwell Dominance in Large Samples to Rényi Divergences and Back Again*, Econometrica 89 (2021); arXiv:1906.02838, Theorem 2.
- P. Caputo, P. Dai Pra, G. Posta, *Convex entropy decay via the Bochner–Bakry–Emery approach*, Annales de l'Institut Henri Poincaré, Probabilités et Statistiques 45 (2009), DOI 10.1214/08-AIHP183.
- A. N. Gorban, *General H-theorem and Entropies that Violate the Second Law*, Entropy 16 (2014), 2408–2432.
- The separate Werner investigation consulted J. Fu, L. Gao, S.-J. Park, *A solution to 2-copy distillability of Werner states*, arXiv:2607.21367v2, and the source-reported Astra flat-projection reduction at commit `a1107371549bebdfd8a8f23904007f1d9541fe08`, dossier N525. Neither was treated as an all-copy theorem.
