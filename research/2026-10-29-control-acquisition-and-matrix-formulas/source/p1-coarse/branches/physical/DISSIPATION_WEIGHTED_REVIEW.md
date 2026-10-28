# Review of the dissipation-weighted, corrected word bound

28 October 2026. Scope: the new source-dissipation theorem, its sharp constant,
its load-bearing acquisition premise, and the closest inspected primary
antecedents. The previously accepted signed compiler is used at its stated
scope. Its older conclusions are not re-audited here.

## Finding

The proposed second-order bound is sound. It admits a slightly sharper
finite-word version using the computational energy actually lost on that
word. The constant 2 is optimal under the stated assumptions, including
realizable fixed dictionaries and coupled forward and backward coefficient
trajectories. The factorization or range premise is essential: a bare
Moore–Penrose expression can certify a false result.

This is an application and extension of established energy, dilation and
dual-weighted residual machinery. No foundational novelty is claimed for
those ingredients or for a uniform switching error bound in general. The
specific addition to be assessed is the experimentally acquired,
source-dissipation-relative certificate for the existing signed word
compiler. Finite acquisition still needs information controlling its
unobserved source tail. Small ordinary echo intervals cannot supply that
information without an additional premise.

## 1. Precise assumptions and corrected output

Let H be a real or complex Hilbert space and A_i:H→H be contractions. Let
V:C^r→H be any bounded synthesis map, possibly with singular V*V, and let
b=Vc. Let W be positive definite on C^r. Define

\[
R_i=W-T_i^*WT_i\succeq0,\qquad
R_i^d=W-S_i^*WS_i\succeq0,
\]

\[
D_i=A_iV-VT_i,\qquad J_i=A_i^*V-VS_i.
\]

The safe source-dissipation premise is the existence of bounded maps K_i,L_i
such that

\[
D_i=B_iK_i,\quad B_i=(I-A_iA_i^*)^{1/2},\quad
K_i^*K_i\preceq\theta_f^2R_i,
\]

\[
J_i=C_iL_i,\quad C_i=(I-A_i^*A_i)^{1/2},\quad
L_i^*L_i\preceq\theta_b^2R_i^d.
\]

These are ordinary bounded factorizations; no inverse of V*V, hidden rank,
source spectral gap, or strict computational contraction is required for
the theorem below. Different actions may have different defects and may
be nonnormal or noncommuting. Their contraction property is in the same
physical Hilbert-space metric.

For a chronological word i_1,…,i_h, define

\[
\alpha_0=c,\quad\alpha_t=T_{i_t}\alpha_{t-1},\qquad
\beta_h=c,\quad\beta_{t-1}=S_{i_t}\beta_t.
\]

Write G=V*V. The exact signed corrected output is

\[
\widetilde f(w)=c^*G\alpha_h+
\sum_{t=1}^h\beta_t^*V^*D_{i_t}\alpha_{t-1}.
\]

All conjugations in this formula matter for complex data. Native real
reciprocal echoes are a special case. This mathematical expression must
still be enclosed using the acquired scalar intervals; the theorem does
not remove that separate observation error.

## 2. Ordinary proof, including the finite-word strengthening

Set

\[
u_t=K_{i_t}\alpha_{t-1},\qquad v_t=L_{i_t}\beta_t,
\]

and denote the two computational energy losses by

\[
\Delta_f=\|c\|_W^2-\|\alpha_h\|_W^2,\qquad
\Delta_b=\|c\|_W^2-\|\beta_0\|_W^2.
\]

Both are nonnegative. Direct telescoping of the finite coefficient
trajectories gives

\[
\sum_t\|u_t\|^2\le\theta_f^2\Delta_f,\qquad
\sum_t\|v_t\|^2\le\theta_b^2\Delta_b.                 \tag{1}
\]

Let x_0=b, x_t=A_{i_t}x_{t-1}, and define the actual primal error
e_t=x_t−Vα_t. Then e_0=0 and

\[
e_t=A_{i_t}e_{t-1}+B_{i_t}u_t.                       \tag{2}
\]

There is a useful short derivation of the exact corrected remainder. With
the inner product conjugate-linear in its first argument,

\[
\begin{aligned}
\langle V\beta_t,e_t\rangle
&=\langle A_{i_t}^*V\beta_t,e_{t-1}\rangle
  +\langle V\beta_t,D_{i_t}\alpha_{t-1}\rangle\\
&=\langle V\beta_{t-1},e_{t-1}\rangle
  +\langle J_{i_t}\beta_t,e_{t-1}\rangle
  +\langle V\beta_t,D_{i_t}\alpha_{t-1}\rangle.
\end{aligned}
\]

Summing this identity, using β_h=c and e_0=0, yields

\[
f(w)-\widetilde f(w)
=\sum_{t=1}^h\langle v_t,C_{i_t}e_{t-1}\rangle.       \tag{3}
\]

For every contraction A the Julia/Halmos block

\[
\mathcal U_A=
\begin{pmatrix}
A&(I-AA^*)^{1/2}\\
(I-A^*A)^{1/2}&-A^*
\end{pmatrix}
\]

is unitary. This is a standard operator-theoretic fact; an explicit primary
proof is Robinson [2], Theorems 0–2. Apply its norm identity at step t to
(e_{t-1},u_t), and put

\[
y_t=C_{i_t}e_{t-1}-A_{i_t}^*u_t.
\]

Summing the one-step identities gives the exact conservation law

\[
\|e_h\|^2+\sum_t\|y_t\|^2=\sum_t\|u_t\|^2.          \tag{4}
\]

The raw outputs in (3) are z_t=C_{i_t}e_{t-1}=y_t+A_{i_t}*u_t.
Consequently

\[
\|z\|_{\ell^2}\le\|y\|_{\ell^2}+\|(A_{i_t}^*u_t)_t\|_{\ell^2}
\le2\|u\|_{\ell^2}.                                \tag{5}
\]

Cauchy–Schwarz in (3), followed by (1) and (5), proves

\[
\boxed{\ |f(w)-\widetilde f(w)|
\le2\theta_f\theta_b\sqrt{\Delta_f\Delta_b}
\le2\theta_f\theta_b\|c\|_W^2.\ }                    \tag{6}
\]

Equation (4) also proves a state estimate,

\[
\|x_h-V\alpha_h\|\le\theta_f\sqrt{\Delta_f},
\]

and hence the uncorrected scalar estimate

\[
|f(w)-c^*G\alpha_h|\le\theta_f\|b\|\sqrt{\Delta_f}.
\]

The familiar energy mechanism underlying this first-order estimate is
already present in Veselić [1], Theorem 2. Calling it a new gap-free
perturbation principle would overstate the addition.

## 3. Sharpness within the actual dictionary setting

The generic causal operator in (5) has norm approaching 2. That observation
alone does not establish sharpness for coupled defects produced by fixed
V,T,S. A separate construction from the dynamic-representation reviewer
closes that issue.

Take H=R, A=a∈(0,1), b=1, coefficient dimension N, W=I, and the actual word
dictionary

\[
V=(a^{N-1},a^{N-2},\ldots,1).
\]

Let T=S be the backward shift, T e_j=e_{j-1} for j≥1 and T e_0=0. Let

\[
c=k(1,\ldots,1)^T,\qquad k=\frac{1-a}{1-a^N}.
\]

Then Vc=1, R=R^d=e_0e_0*, and D=J=a^N e_0*. The source factorizations
hold with equality for

\[
\theta_f^2=\theta_b^2=\frac{a^{2N}}{1-a^2}.
\]

After N repeated operations both α_N and β_0 vanish. Direct summation of
the actual remainder in (3) gives

\[
\frac{|f-\widetilde f|}{\theta_f\theta_b\|c\|_W^2}
=(1+a)\left(1-\frac{1-a^N}{N(1-a)}\right).             \tag{7}
\]

Set a=1−1/n and N=n². The right side tends to 2. Therefore no smaller
universal constant is valid under the theorem's assumptions, including
the sharper finite-loss version. This construction has a redundant
dictionary, which the theorem explicitly permits. The reviewer also gives
a full-rank diagonal-spectrum variant, so singularity is not the reason
for sharpness. See the separate proof and executable check in
`../dynamics/DISSIPATION_CONSTANT_CHALLENGE.md`.

This does not assert sharpness under additional restrictions such as an
orthonormal physical basis, W=V*V, or specially chosen Galerkin maps. Those
would define stronger hypotheses than the theorem reviewed here.

## 4. The source range condition cannot be discarded

In finite dimension the first factorization is equivalent to

\[
\operatorname{Ran}D_i\subseteq\operatorname{Ran}(I-A_iA_i^*)^{1/2},
\qquad
D_i^*(I-A_iA_i^*)^\dagger D_i\preceq\theta_f^2R_i,
\]

with the analogous dual condition. A displayed pseudoinverse inequality
without the range inclusion is insufficient.

For an exact counterexample, take A=V=W=1 and T=S=0. Then D=J=1 and
R=R^d=1, while I−AA*=0. Its Moore–Penrose inverse is zero, so the bare
quadratic expressions falsely permit θ_f=θ_b=0. At word length two the
true response is 1 and the signed corrected expression is 0. The missing
range condition is precisely what excludes this example.

In infinite dimension, orthogonality to a defect kernel does not suffice:
the range of a square root need not be closed. The bounded-factorization
formulation avoids confusing range closure with actual range, and avoids
undefined compositions with an unbounded generalized inverse.

## 5. Ordinary moment precision cannot certify the inverse source form

Here is a two-dimensional observable counterexample, stronger than adding
an entirely unobservable sector. Fix 0<ρ<1 and 0<δ<1. Compare scalar
spectral measures

\[
\mu_0=\delta_\rho,\qquad
\mu_\eta=(1-\delta)\delta_\rho+\delta\delta_{1-\eta},
\quad0<\eta<1-\rho.
\]

They have contraction realizations with unit reset vectors. Their scalar
responses obey, for every nonnegative word length n,

\[
\left|\int x^n\,d\mu_\eta-\int x^n\,d\mu_0\right|
=\delta|(1-\eta)^n-\rho^n|\le\delta.                 \tag{8}
\]

Thus even a complete family of absolute moment intervals of radius δ can
contain both sources. Use the one-column dictionary V=b and the proposed
map T=ρ. For μ_η the ordinary defect norm is

\[
D^*D=\delta(1-\eta-\rho)^2\le\delta,
\]

but its inverse-dissipation form is

\[
Q_\eta=D^*(I-A^2)^{-1}D
=\frac{\delta(1-\eta-\rho)^2}{1-(1-\eta)^2}
\longrightarrow\infty\quad(\eta\downarrow0).         \tag{9}
\]

No finite upper bound for this source form follows from the common
intervals. An independent source tail warranty, or a stronger observation
operation, is a real additional resource. Equation (8) also shows why this
is a limitation of this sufficient certificate rather than an
impossibility of accurate output prediction: the one-mode predictor is
already uniformly accurate to δ.

For a warranted strict source norm, the Neumann-series tail used in the
root construction is valid. On a known residual invariant subspace it is
enough to have the corresponding restricted warranty. Such a subspace and
its bound cannot be silently inferred from short noisy echoes. The separate
scalar review checks the implemented finite acquisition and its interval
arithmetic; this review does not duplicate that completed work.

## 6. Executed exact checks

`dissipation_weighted_checks.py` uses only standard-library rational
arithmetic. It verifies 510 switched words of lengths zero through seven
for two nonnormal, noncommuting rational contractions. Each action has
singular physical dissipation. It repeats the checks with coefficient
dimensions two and three; the three-column synthesis has a singular Gram
matrix.

For every word it verifies the exact signed-remainder identity, both
source factorizations, both matrix dissipation inequalities, the Julia
energy equality, and the refined bound (6). The chosen common constants
are θ_f²=θ_b²=1/48. It also verifies rational instances of (9): with
δ=10^−6 and ρ=1/2, decreasing η from 10^−3 to 10^−9 increases the weighted
form from about 0.00012456 to about 124.99999956 while the common moment
interval width stays fixed.

These are independent algebraic fixtures, not a physical experiment or a
demonstration that native source records supplied the assumed weighted
forms. The result file marks that boundary explicitly. The checker ran
successfully with exit code zero.

## 7. Closest inspected primary antecedents and attributable difference

**[1] Veselić (2004), Theorem 2.** The theorem bounds powers of two
contractions uniformly from a relative perturbation inequality involving
their two dissipation operators. Its proof telescopes energy losses. The
current first-order bound is a switched, mixed-space intertwining use of
that mechanism. The phrase “second order systems” in that paper's title
refers to differential equations; it is not a claim about the current
quadratic corrected remainder. Exact theorem and proof inspected.

K. Veselić, *Bounds for contractive semigroups and second order systems*,
https://arxiv.org/pdf/math/0404120.

**[2] Robinson (2018), Theorems 0–2.** These prove the defect-operator
intertwining identity and unitarity of the Julia and Halmos blocks. The
one-step unitary in the present proof is exactly this standard construction.
All three short theorems inspected.

P. L. Robinson, *Julia operators and Halmos dilations*,
https://arxiv.org/pdf/1803.09329.

**[3] Badea and Suciu (2017), Theorem 1.2.** Shmul'yan domination uses
factorizations of differences through contraction defect operators;
equivalence has a two-sided defect-factorization characterization. This
precludes presenting defect-weighted perturbation geometry itself as new.
The inspected theorem does not state the acquired signed word compiler.

C. Badea and L. Suciu, *Harnack and Shmul'yan pre-order relations for Hilbert
space contractions*, https://arxiv.org/pdf/1512.01990.

**[4] Qian, Grepl, Veroy and Willcox (2017), §3.2.2 and §3.3.** Definitions
5–6, Lemma 7 and Theorem 8 give primal/dual residuals, evolution energy
estimates, and a corrected output bound with products of residual estimates.
The construction uses a known full model, primal/dual snapshots, inner-product
solves and a warranted coercivity lower bound. Thus second-order corrected
output certification for dissipative evolution is already established.
Those exact sections, including the acquisition/computation requirements,
were inspected. The present acquisition interface and local contraction
defect forms differ from those model-access premises.

E. Qian, M. A. Grepl, K. Veroy and K. Willcox, *A Certified Trust Region
Reduced Basis Approach to PDE-Constrained Optimization*,
doi:10.1137/16M1081981. Author preprint:
https://www.igpm.rwth-aachen.de/Download/reports/grepl/QGVW_TRRB_preprint_2016.pdf.

**[5] Creusé, Nicaise and Tang (2023).** The publisher abstract explicitly
describes splitting a quantity-of-interest error into a computable
estimator and a remainder bounded by the product of primal and dual energy
estimators. Only the primary abstract and introduction were accessible in
this review; no exact equivalence of their theorem to the present algebra
is asserted.

E. Creusé, S. Nicaise and Z. Tang, *Goal-oriented error estimation based on
equilibrated flux and potential reconstruction for the approximation of
elliptic and parabolic problems*, doi:10.1016/j.camwa.2023.07.008,
https://www.sciencedirect.com/science/article/abs/pii/S0898122123003000.

**[6] Petreczky, Wisniewski and Leth (2013), Procedure 4 and Theorem 6.**
Common controllability and observability Gramian inequalities yield balanced
truncation with a uniform switched input-output error bound
2Σ_{k>r}σ_k. The theorem covers discrete and continuous time and arbitrarily
chosen external switching. The exact statement and its Gramian/model
premises were inspected. This establishes a strong existing comparator
for uniform switching guarantees. It does not, in the inspected operation,
construct those premises from bounded scalar word intervals of an unknown
unbounded-rank source.

M. Petreczky, R. Wisniewski and J. Leth, *Balanced truncation for linear
switched systems*, doi:10.1016/j.nahs.2013.03.007,
https://arxiv.org/pdf/1302.0221.

### Assessment

No inspected source was found to state the complete operation comprising
native bounded-error scalar words, arbitrary fixed coefficient maps,
signed primal-dual correction, independently bounded inverse-source
dissipation forms, and one certificate valid for every future word.
This is a scoped literature observation, not proof of priority.

The defensible addition is that exact combination and its acquisition
contract, including the ordinary proof above and sharp constant. Existing
model-reduction methods can adopt the same experimentally supplied forms;
that adoption does not erase the added construction, but it eliminates an
unwarranted claim of a new general energy principle or a superiority result
against equally informed methods.

The remaining consequential obligation is operational: obtain the weighted
forms, or a less conservative substitute, at complete cost competitive with
an equally informed strong method. The strict source warranty and the
precision needed by moment differencing remain paid premises in the
current executable acquisition. A finite number of scalar records does not
buy either premise.
