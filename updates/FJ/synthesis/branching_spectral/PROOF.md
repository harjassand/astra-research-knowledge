# Resolvent-tilted bounded correction sampler

**Frozen scope:** an exact mathematical construction for a scalar semilinear equation with positive resolvent, plus a finite two-state continuous-time Markov-chain certificate. The result is internal and not externally reviewed. It does not establish historical novelty, a physical acquisition route, or an advantage over deterministic or multilevel methods.

## 1. Equation and supplied data

Let (E) be a compact state space and (L) the generator of a conservative Markov process. For (Lambda>0), assume its positive resolvent

\[
R_\Lambda=(\Lambda-L)^{-1},\qquad K=\Lambda R_\Lambda
\]

is well defined; (K(x,dy)) is a probability kernel. The target is

\[
-Lu(x)+F(x,u(x))=s(x).
\]

Supply a predictor (v), and set

\[
r=s+Lv-F(x,v),\qquad V=\partial_uF(x,v),\qquad e=u-v.
\]

Assume (0\le V\le\Lambda) and that, on the proposed tube (|e(x)|\le h(x)),

\[
F(x,v+e)-F(x,v)-V(x)e=\sum_{m\ge2}c_m(x)e^m,
\qquad |c_m(x)|\le B_m(x),
\]

where (0<h_{\min}\le h\le h_{\max}<\infty), (B_m\ge0), and the series and its derivative converge absolutely and uniformly on the tube. Finite polynomials are included. Define (a_1=1-V/\Lambda\ge0).

Interpret the fixed-point equation below in the mild sense. For a classical equation, also require the usual generator-domain regularity for (v) and the resolvent solution. If (B_m(y)=0), then (c_m(y)=0), and the nonlinear return factor there is defined as zero.

The centered equation has the fixed-point form

\[
e=T(e):=K\!\left[\frac r\Lambda+a_1e-\sum_{m\ge2}\frac{c_m e^m}{\Lambda}\right]. \tag{1}
\]

## 2. Envelope and work certificates

For each type (x\), define positive measures and their masses

\[
\begin{aligned}
g_0(y)&=|r(y)|/\Lambda,& A_0(x)&=K g_0(x),\\
g_1(y)&=a_1(y)h(y),& A_1(x)&=K g_1(x),\\
g_m(y)&=B_m(y)h(y)^m/\Lambda,& A_m(x)&=K g_m(x)\quad(m\ge2).
\end{aligned}
\]

The **envelope certificate** is

\[
A_0(x)+A_1(x)+\sum_{m\ge2}A_m(x)\le h(x)\quad\text{for every }x. \tag{E}
\]

Equivalently, this is (R_\Lambda[|r|+(\Lambda-V)h+\sum_mB_mh^m]\le h). A sufficient PDE-form certificate is

\[
(-L+V)h\ge |r|+\sum_{m\ge2}B_mh^m, \tag{E'}
\]

when (h) is in the operator domain and the inverse is positivity preserving: applying (R_\Lambda) to ((\Lambda-L)h\ge |r|+(\Lambda-V)h+\sum B_mh^m) gives (E). The reverse implication is not asserted.

For a bounded nonnegative test function (f), define the **mean-progeny operator**

\[
\mathcal M f(x)=\frac1{h(x)}K\!\left[a_1hf+\sum_{m\ge2}\frac{mB_mh^m}{\Lambda}f\right](x). \tag{M}
\]

Supply a positive bounded vector/function (w), with (w_{\min}>0), and a number (0\le\alpha<1), satisfying

\[
\mathcal M w\le\alpha w. \tag{W}
\]

For a finite type space, exact rational (w,\alpha) and rowwise inequalities suffice. For an infinite type space, the bound must cover every point, not just a grid. (W) implies (\rho(\mathcal M)\le\alpha) in the weighted sup norm.

In a finite model, certify a proposed rational (w>0) by computing each row ratio ((\mathcal Mw)_i/w_i) exactly and taking (\alpha) to be their maximum; acceptance requires (\alpha<1). An approximate eigensolver may suggest (w), but only the exact full-row check is the certificate.

## 3. Sampler

At a node of type (x), choose one of these mutually exclusive events, then sample its endpoint from the associated tilted resolvent measure:

| Event | Probability | Endpoint law | Normalized return (Z_x) |
|---|---:|---|---|
| Source | (p_0=A_0(x)/h(x)) | (K(x,dy)g_0(y)/A_0(x)) | ({\rm sgn}(r(Y))) |
| One child | (p_1=A_1(x)/h(x)) | (K(x,dy)g_1(y)/A_1(x)) | (Z_Y) |
| (m\) children | (p_m=A_m(x)/h(x)) | (K(x,dy)g_m(y)/A_m(x)) | (-{\rm sgn}(c_m(Y))\frac{|c_m(Y)|}{B_m(Y)}\prod_{j=1}^mZ_{Y,j}) |
| Zero leaf | (1-p_0-p_1-\sum_mp_m) | — | (0) |

Omit an event with (A_j(x)=0); it has zero mass. The child trees are conditionally independent. The reported sample is (S_x=h(x)Z_x).

This is a change in how the same positive marked-resolvent measure is sampled: the branch mark is selected first, and the endpoint is drawn from its exact conditional law. For continuous diffusions, “draw from the tilted resolvent law” is a real algorithmic obligation. It is not supplied for free by writing the density.

## 4. Theorem and proof

Under (E) and (W), the procedure above is valid; every tree terminates almost surely with finite expected node count; (|S_x|\le h(x)); and

\[
\mathbb E_x S_x=e(x),
\]

where (e) is the unique solution of (1) in the tube (|e|\le h). The generation-(n) expected population is 

\[
\mathbb E_x N_n=\mathcal M^n\mathbf1(x),
\]

so

\[
\mathbb E_x N_{\rm total}
\le \frac{w(x)}{w_{\min}(1-\alpha)}. \tag{2}
\]

**Event probabilities.** By (E), the listed probabilities are nonnegative and sum to at most one.

**Bounded return.** Induct on the finite tree. The source return has magnitude one; a unary return copies a child value in ([-1,1]); and each nonlinear return has magnitude at most ((|c_m|/B_m)\prod_j|Z_{Y,j}|\le1). Hence (|S_x|\le h(x)).

**Mean-progeny operator.** Conditional on type (x), the unary event's child-type measure is

\[
p_1(x)\frac{K(x,dy)a_1(y)h(y)}{A_1(x)}
=\frac{K(x,dy)a_1(y)h(y)}{h(x)}.
\]

The expected number of children from an (m)-event is (mK(x,dy)B_m(y)h(y)^m/(\Lambda h(x))). Summing gives (M). Thus the expected generation populations satisfy the displayed iteration. Because (\mathbf1\le w/w_{\min}), positivity and (W) give (\mathcal M^n\mathbf1\le\alpha^nw/w_{\min}); summing proves (2). A nonnegative integer-valued total with finite expectation is finite almost surely.

**Identification and uniqueness.** The tilted laws cancel their normalizers against their event probabilities. Conditioning on the first event gives, for μ(x)=\(\mathbb E_xS_x\),

\[
\mu(x)=K\!\left[\frac r\Lambda+a_1\mu-\sum_{m\ge2}\frac{c_m\mu^m}{\Lambda}\right](x)=T\mu(x).
\]

Boundedness gives (|\mu|\le h). For any (e,f) in that tube, the polynomial/series difference bound gives

\[
|Te-Tf|\le K\!\left[a_1|e-f|+\sum_{m\ge2}\frac{mB_mh^{m-1}}\Lambda|e-f|\right].
\]

In the weighted norm 

\[
\|g\|_{hw}:=\sup_x\frac{|g(x)|}{h(x)w(x)},
\]

the right side is at most (\alpha\|e-f\|_{hw}h(x)w(x)) by (M) and (W). Thus (T) is a contraction on the closed tube, maps it into itself by (E), and has a unique mild fixed point there. Under the stated domain regularity, applying ((\Lambda-L)) to (1) recovers (-Le+Ve=r-\sum c_me^m), the original equation for (u=v+e).

The identity is for exact arithmetic, exact resolvent sampling, and exact random draws. Finite-precision path simulation needs a separate bias/error certificate.

## 5. Expected work, confidence, and acquisition

Let (c(x)) bound expected local work at a node, including evaluating coefficients, event selection, exact endpoint sampling from each tilted law, and all diffusion operations. If (c(x)\le Cw(x)), then

\[
\mathbb E_x[\text{tree work}]\le C\frac{w(x)}{1-\alpha}.
\]

If only (c\le C_{\max}) is known, use (2) to get (C_{\max}w(x)/(w_{\min}(1-\alpha))). Add the one-time costs (C_{\rm acquire}+C_{\rm verify}) for the predictor, residual, coefficient envelopes, (h), the full-domain envelope check, μ_j masses, tilted endpoint samplers, and the positive vector (w). Reuse across (M) independent queries only when the acquired objects really are shared. Then

\[
\mathbb E[\text{total work}]
\le C_{\rm acquire}+C_{\rm verify}+M C\frac{w(x)}{1-\alpha}.
\]

Since (S_x\in[-h(x),h(x)]), the empirical mean of (M) independent exact samples obeys

\[
\Pr\{|\widehat e_M(x)-e(x)|>\varepsilon\}
\le 2\exp\!\left(-\frac{M\varepsilon^2}{2h(x)^2}\right).
\]

If a tilted law is sampled by rejection from (K) using (g_j\le C_j), its expected number of endpoint proposals is (C_j/A_j(x)) conditional on that event. Its contribution to a node's expected endpoint cost is (p_j C_j/A_j=C_j/h(x)). Those proposals, endpoint generation, (A_j) evaluation, and any interval/refinement work must be charged. An exact finite-state table avoids rejection but its table construction/storage still belongs to acquisition cost. No dimension-free or sublinear-input claim follows.

## 6. Exact separation from the scalar certificate

Use the two-state CTMC

\[
L=\begin{pmatrix}-3&3\\3&-3\end{pmatrix},\quad \Lambda=2,
\quad K=2(2I-L)^{-1}=\begin{pmatrix}5/8&3/8\\3/8&5/8\end{pmatrix}.
\]

Set (v=0), (h_A=2,h_B=1), (r=(1,0)), (V=(1,2)), and (c_2=B_2=(1/2,0)). Thus (F_A(u)=u+u^2/2), (F_B(u)=2u). The exact envelope masses are

\[
(A_0,A_1,A_2)_A=(5/16,5/8,5/8),\quad
(A_0,A_1,A_2)_B=(3/16,3/8,3/8),
\]

whose totals (25/16\le2) and (15/16\le1) satisfy (E). Dividing by (h_A,h_B), the event probabilities (source, one child, two children, zero) are respectively

\[
(5/32,5/16,5/16,7/32)\quad\text{and}\quad
(3/16,3/8,3/8,1/16).
\]

All nonzero tilted endpoint laws are point masses at (A). The mean-progeny matrix is

\[
M=\begin{pmatrix}15/16&0\\9/8&0\end{pmatrix}.
\]

Its ordinary sup-norm operator bound is (9/8>1), and a type-(B) root has (9/8) expected children in its first generation. Yet (w=(1,6/5)) satisfies (Mw=(15/16)w), so ρ\(M)=15/16 and (W) holds with α=15/16. The exact expected total node counts are 16 from (A) and 19 from (B). This certifies true almost-sure termination even though one type initially produces more than one child on average.

The original global scalar enclosure cannot pass at any radius (t>0): with (R=1), (B_2=1/2), and λ\(=\min V=1),

\[
\sup_{t\ge0}(\lambda t-B_2t^2)=\frac12<R.
\]

At (t=2=\max h), the scalar values are (R+B_2t^2=3>2=\lambda t) and Γ\((t)=2B_2t=2\not<1). The exact solution in the certified tube is

\[
u_A=\frac{-22+6\sqrt{19}}{10},\qquad u_B=\frac35u_A.
\]

The exact checker `verify_certificate.py` independently verifies the resolvent identity, event probabilities, envelope inequalities, rational (M,w,\alpha), failed scalar enclosure for every radius, and expected node counts. It does not numerically sample the process.

## 7. Relation to N798/N804 and prior methods

The proof uses an explicitly acquired positive vector for a different operator, (M). N804's retained-vector pattern—round a proposed positive vector, verify its residual exactly, and derive a one-sided operator bound—is a valid *certificate-design analogue*. Its actual vector and α certify a lower spectral bound for the acquired kinetic reference form; they cannot be inserted as a contraction or offspring bound for (M). A legal implementation would need a rowwise/full-domain proof of (Mw\le\alpha w), including every omitted type, in the branching model's own representation.

N798's source/form comparison and residual Gram identity can certify source-response quantities for its stated reversible weighted form and fully covered load columns. They do not supply the pointwise envelope (h), the term masses (A_j(x)), or exact samples from the tilted resolvent laws here. A transfer would require a new theorem identifying those exact quantities and proving that its source basis covers all spatial types and nonlinear terms. The N798 warning that a projected residual can omit a large true component applies directly as a caution: a retained-only check of (M) is not a certificate without a full residual/complement bound. No N798/N804 theorem is composed into this result.

The broad ingredients are established. Agarwal and Claisse (2020), Proposition 3.4, use positive supersolutions to bound (q)-moments of elliptic branching functionals; their Section 3.3 explicitly says constant supersolutions are only one option and that nonconstant supersolutions can be found case by case. Branching PDE representations with marked, nonuniform coefficients and importance-sampling choices are also established. Huang and Privault (2026 revision), Sections 6–7, control multiplicative weighted progeny through stochastic dominance and Hamilton–Jacobi bounds. Those are close enough that historical novelty is **UNKNOWN**, and the present construction may be a specialization/recombination of known supersolution and multitype branching arguments. Its scoped theorem is the exact combination of (i) a positive tangent held in the resolvent, (ii) a variable envelope checked through the full resolvent, (iii) event-first tilted endpoint laws giving pathwise bounded output, and (iv) one positive vector for both contraction and expected-work control. Priority is not asserted.

References:

- Agarwal & Claisse, *Branching diffusion representation of semi-linear elliptic PDEs and estimation using Monte Carlo method*, arXiv:1704.00328, Section 3.3, Proposition 3.4: <https://arxiv.org/abs/1704.00328>.
- Huang & Privault, *Stability analysis of a branching diffusion solver for semilinear heat equations*, arXiv:2502.17853v2 (9 March 2026): <https://arxiv.org/abs/2502.17853>.
- Henry-Labordère et al., *Branching diffusion representation of semilinear PDEs and Monte Carlo approximation*, arXiv:1603.01727: <https://arxiv.org/abs/1603.01727>.

## 8. Limitations and exact next gates

- For a continuous diffusion, the tilted laws μ\(_{j,x}\) and their normalizers (A_j(x)) may be as expensive as the target response. Exact Brownian proposal/rejection costs can become large when (A_j) is small; exact finite-state success does not solve this.
- Building and checking a spatial (h) and a full-domain positive vector (w) may cost more than solving the original PDE. All support, precision, preprocessing, and omitted-state costs remain open until acquired.
- Random-tree finite expectation is not an efficiency advantage. No comparison was run against Newton/Krylov, deterministic discretization, multilevel Picard, or optimized branching on the same equation.
- Taylor bounds fail outside (|e|\le h); derivative-dependent nonlinearities, coupled systems, arbitrary boundary conditions, approximate path simulation, and physical molecular parameters need separate theorems and costs.
- This finite example uses exact rational transition probabilities but no stochastic replay or measured runtime. It establishes the mathematical mechanism and exact certificate scope only.
