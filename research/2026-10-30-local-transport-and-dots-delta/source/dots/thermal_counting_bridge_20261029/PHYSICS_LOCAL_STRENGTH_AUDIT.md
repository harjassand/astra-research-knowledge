# Independent audit: local-strength improvement of the thermal product bound

Date: 2026-10-29 UTC.
Auditor: `test_thermal_counting_bridge/audit_uniform_trotter`.

## Verdict and scope

**PASS.** The stated local-strength Dyson-coefficient argument is valid,
including its constants, support counting, ordered-simplex integration,
Hermitian-parity cancellation, and allowance for arbitrary nonuniform local
term strengths. It replaces the earlier finite-cone constant M by

\[
K=k\sum_{j=1}^{c}J_j,
\qquad J_j=\max_{e\text{ in layer }j}\|h_e\|.
\]

The maximum of an empty layer is defined to be zero. No claim of novelty is
made. This is an audit of the analytic thermal approximation, **not** an audit
of counting complexity, weight compilation, local gate approximation, or the
parent's separate sparsification assertion (cJ_s=O(kg)).

## Exact assumptions

Let (H=\sum_e h_e) on a finite tensor-product Hilbert space. Each (h_e)
is Hermitian with a nonempty support of size at most (k\ge1). Let

\[
L=\sum_e\|h_e\|.
\]

Partition the terms into c layers, each having pairwise disjoint supports, and
write (H=\sum_{j=1}^{c}H_j). Set

\[
E_j(t)=e^{-tH_j/2},\quad
Q(t)=E_c(t)\cdots E_1(t),\quad P(t)=Q(t)^\dagger Q(t).
\]

Scalar/empty-support terms may instead be removed and treated exactly. There
is no positivity assumption on the individual terms or their entries. Different
terms may have different norms, signs, or complex Hermitian matrix entries.

For (\delta\ge0) and (K\delta<1), the accepted bound is

\[
\boxed{
\|\log P(\delta)+\delta H\|
\le 2L\left(\frac{\operatorname{atanh}(K\delta)}{K}-\delta\right)
\le \frac{2LK^2\delta^3}{3(1-K^2\delta^2)}.
}
\]

If K=0, all non-scalar terms vanish and the right side is interpreted by its
continuous limit, zero. All norms here are spectral operator norms.

## 1. Exact normalized-time representation

For (s\in((j-1)/c,j/c)), define

\[
A(s)=-\frac c2 H_j=\sum_{e\text{ in }j}a_e(s),
\qquad a_e(s)=-\frac c2 h_e.
\]

Let (W_t(0)=I) and (\partial_s W_t(s)=tA(s)W_t(s)). This piecewise
constant differential equation gives (W_t(1)=Q(t)) in exactly the required
order. For a local h,

\[
F_t(s)=W_t(s)hW_t(s)^{-1},\qquad
\partial_sF_t(s)=t[A(s),F_t(s)].
\]

Thus the coefficient of (t^p) in (F(t)=Q(t)hQ(t)^{-1}) is precisely

\[
\int_{0<s_1<\cdots<s_p<1}
\operatorname{ad}_{A(s_p)}\cdots\operatorname{ad}_{A(s_1)}h\,
ds_1\cdots ds_p.
\]

This is an ordinary finite-dimensional Dyson expansion; discontinuities of A
at layer boundaries have measure zero and cause no problem.

## 2. Branchwise support and norm counting

Define the instantaneous local strength

\[
a(s)=\max_i\sum_{e:\,i\in\operatorname{supp}(a_e(s))}\|a_e(s)\|.
\]

If an operator X is supported on S, then terms supported disjointly from S
commute with X. The remaining terms satisfy

\[
\sum_{e:\,\operatorname{supp}(a_e(s))\cap S\ne\varnothing}
\|[a_e(s),X]\|
\le2\|X\|\sum_{i\in S}\sum_{e:\,i\in\operatorname{supp}(a_e(s))}
\|a_e(s)\|
\le2a(s)|S|\|X\|.
\]

Overcounting terms that intersect S in more than one site only strengthens the
inequality. Along any nonzero branch of a termwise-expanded nested commutator,
each newly used term intersects the existing support and adds at most k-1
sites. If the initial support size is at most k, its size after ℓ commutators
is at most (k+\ell(k-1)).

Applying the preceding inequality recursively, for fixed ordered times the sum
of branch norm bounds is at most

\[
\|h\|\prod_{\ell=0}^{p-1}
\left[2a(s_{\ell+1})\big(k+\ell(k-1)\big)\right].
\]

This proves the asserted integrand bound without replacing any local strength
by the extensive norm of A(s).

## 3. Why the simplex factor is exactly (1/p!\)

Although the original nested commutator is time ordered and noncommutative,
the upper bound after taking termwise norms contains the symmetric scalar
integrand (\prod_{i=1}^{p}a(s_i)). Therefore

\[
\int_{0<s_1<\cdots<s_p<1}\prod_{i=1}^{p}a(s_i)\,ds_1\cdots ds_p
=\frac1{p!}\left(\int_0^1a(s)\,ds\right)^p.
\]

There is no illicit permutation of noncommuting operators: the permutation is
used only after replacing their integrand by the symmetric scalar majorant.

Furthermore,

\[
\prod_{\ell=0}^{p-1}\big(k+\ell(k-1)\big)
\le\prod_{\ell=0}^{p-1}k(\ell+1)=k^p p!.
\]

Combining these gives

\[
\|[t^p]F(t)\|
\le\|h\|\left(2k\int_0^1a(s)\,ds\right)^p.
\]

In a disjoint-support layer, each site belongs to at most one active term.
Consequently (a(s)\le cJ_j/2) on interval j and

\[
2k\int_0^1a(s)\,ds\le k\sum_{j=1}^cJ_j=K.
\]

Hence ‖[t^p]F(t)‖≤‖h‖K^p, exactly as proposed. The same argument applies
to every suffix (E_c\cdots E_{j+1}): put zero generators in omitted
intervals, or use its own smaller sum of layer maxima. The full K remains a
valid bound for every suffix.

## 4. Hermitian parity and the even geometric tail

For any such ordered product U(t) of Hermitian exponentials,

\[
U(-t)=U(t)^{-\dagger}.
\]

For Hermitian h and real t this implies

\[
(U(t)hU(t)^{-1})^\dagger=U(-t)hU(-t)^{-1}.
\]

Thus the Hermitian part keeps exactly the even Taylor coefficients. For
(|Kt|<1),

\[
\|\operatorname{Herm}(U(t)hU(t)^{-1})-h\|
\le\|h\|\sum_{p\ge1}(Kt)^{2p}
=\|h\|\frac{(Kt)^2}{1-(Kt)^2}.
\]

The entire matrix function has not been claimed to have a finite radius of
convergence. Only this convenient geometric majorant requires (|Kt|<1).

## 5. Relative generator and integration

Set (R(t)=Q(t)e^{tH/2}). With
(U_{>j}(t)=E_c(t)\cdots E_{j+1}(t)), exact differentiation yields

\[
R'=GR,\qquad
G=\frac12\sum_{j=1}^{c}\sum_{e\text{ in }j}
\left(\operatorname{Ad}_{Q(t)}h_e-
\operatorname{Ad}_{U_{>j}(t)}h_e\right).
\]

Applying the even-tail estimate separately to the two terms and canceling
their zeroth-order (h_e)'s proves

\[
\|\operatorname{Herm}G(t)\|
\le L\frac{(Kt)^2}{1-(Kt)^2}.
\]

There is no additional factor of two: the two tail bounds cancel the outer
factor (1/2). For any vector v,

\[
\frac{d}{dt}\|R(t)v\|^2
=2\langle R(t)v,\operatorname{Herm}G(t)R(t)v\rangle.
\]

Two-sided scalar Grönwall therefore gives

\[
e^{-2b}I\preceq R(\delta)^\dagger R(\delta)\preceq e^{2b}I,
\quad
b=L\int_0^\delta\frac{K^2t^2}{1-K^2t^2}\,dt
=L\left(\frac{\operatorname{atanh}(K\delta)}K-\delta\right).
\]

Congruence by (e^{-\delta H/2}) followed by operator monotonicity of log,
exactly as in `PHYSICS_AUDIT.md`, gives ‖log P(δ)+δH‖≤2b. Finally,

\[
\int_0^\delta\frac{K^2t^2}{1-K^2t^2}\,dt
\le\frac{K^2\delta^3}{3(1-K^2\delta^2)},
\]

which confirms the proposed rational upper bound and all its constants.

## Consequence and limits of what was audited

For β≥0, positive integer r with (K\beta/r<1), and
(Z_r=\operatorname{Tr}P(\beta/r)^r), log-trace-exp spectral-norm Lipschitz
continuity gives

\[
\frac{|\log\operatorname{Tr}e^{-\beta H}-\log Z_r|}{n}
\le\frac{2(L/n)K^2\beta^3}{3r^2(1-(K\beta/r)^2)}.
\]

This is volume-uniform whenever both L/n and K are bounded independently of
volume. An arbitrary nonuniform collection of bounded-strength Hermitian terms
is allowed, but **the proof does not itself establish a favorable bound on the
sum of layer maxima**. In particular, (K=k\sum_jJ_j\le kcJ_s) is valid
when all term norms are at most (J_s), whereas obtaining small (cJ_s) by
splitting/sparsification is a separate claim requiring its own proof.

If (g=\max_i\sum_{e\ni i}\|h_e\|), then nonempty supports imply
(L\le ng), but this fact alone does not replace K by kg for an arbitrary
coloring. No such replacement is silently made here.

No numerical evidence is needed for these algebraic checks. This receipt
establishes neither the completeness nor the arithmetic cost of any associated
signed-counting algorithm.
