# Polynomial local-strength replacement for the finite-cone bound

2026-10-29. **Proved; independent audit PASS**, recorded in `PHYSICS_LOCAL_STRENGTH_AUDIT.md`. This replaces the exponentially loose `M=k+...+k^c` constant in the earlier thermal proof. It is an application of established local-strength nested-commutator machinery, not a new foundational locality theorem. The adaptive sparsification cap is a separate construction and is not silently inferred from an earlier/coarser cap.

## 1. Precise statement, including arbitrary weights

Let `H=sum_e h_e=sum_{j=1}^c H_j`, with every `h_e` Hermitian, supported on at most `k` spins. Each layer consists of disjoint-support terms. Define

\[
L=\sum_e\|h_e\|,\qquad
J_j=\max_{e\text{ in layer }j}\|h_e\|,\qquad
K=k\sum_{j=1}^c J_j.
\]

Empty-layer maxima are zero; scalar terms can be extracted exactly. No lower bound on term weights, uniformity of weights, sign condition, geometric assumption, or bound on the raw degree is needed for this theorem. With a uniform term-norm bound `J_s`, one has `K<=kcJ_s`.

Set

\[
E_j(t)=e^{-tH_j/2},\quad Q(t)=E_c(t)\cdots E_1(t),\quad
P(t)=Q(t)^\dagger Q(t).
\]

For `0<=K delta<1`,

\[
\boxed{\|\log P(\delta)+\delta H\|
\le2L\left[\frac{\operatorname{atanh}(K\delta)}{K}-\delta\right]
\le\frac{2LK^2\delta^3}{3(1-K^2\delta^2)}.} \tag{1}
\]

At `K=0` the right sides mean their zero limit. Consequently, if `r>K beta`,

\[
\boxed{\frac{1}{n}\left|\log\operatorname{Tr}P(\beta/r)^r
-\log\operatorname{Tr}e^{-\beta H}\right|
\le\frac{2(L/n)K^2\beta^3}{3r^2[1-(K\beta/r)^2]}.} \tag{2}
\]

Divide (2) by `beta` for free-energy-density error. The dependence is polynomial in `K`, rather than exponential in color count.

**Do not replace `sum_j J_j` by the local strength of `H` without further proof.** In general a sum of layer maxima is not the maximum of the sum. The application described by the parent obtains `cJ_s=O(kg)` from a separately established, adaptive sparsification cap.

## 2. Time-ordered local-strength coefficient lemma

More generally, let `A(s)=sum_X a_X(s)` for `s in [0,1]`, with each term supported on at most `k` spins, and with integrable local strength

\[
a(s)=\max_i\sum_{X\ni i}\|a_X(s)\|.
\]

For the propagator `U_t'(s)=t A(s)U_t(s)`, `U_t(0)=I`, let

\[
F(t)=U_t(1)hU_t(1)^{-1},\qquad |\operatorname{supp}h|\le k.
\]

Its Taylor coefficient of degree `p` is the ordered-simplex integral

\[
F_p=\int_{0\le s_1\le\cdots\le s_p\le1}
\operatorname{ad}_{A(s_p)}\cdots\operatorname{ad}_{A(s_1)}(h)
\,ds_1\cdots ds_p. \tag{3}
\]

For finite-dimensional, piecewise-constant `A` this is an identity between entire functions, so there is no formal-series assumption.

Expand each nested commutator termwise. A nonzero branch only uses a new term that overlaps the current branch support. After `ell` commutators that support has size at most

\[
k+\ell(k-1)\le k(\ell+1).
\]

For a branch currently supported on `S`, the sum of norms of the available next interaction terms is at most `|S|a(s)`. The commutator adds a factor at most `2`. Applying this successively, using the **incoming** support before the `m`th commutator, gives

\[
\|\operatorname{ad}_{A(s_p)}\cdots\operatorname{ad}_{A(s_1)}(h)\|
\le\|h\|\prod_{m=1}^p[2a(s_m)(k+(m-1)(k-1))]
\le\|h\| (2k)^p p!\prod_{m=1}^p a(s_m). \tag{4}
\]

There is no leftover factor `p+1`: the `m`th commutator sees support at most `km`, not `k(m+1)`.

Although the operator integrand in (3) is not symmetric, its scalar majorant in (4) is. Thus

\[
\int_{s_1\le\cdots\le s_p}\prod_m a(s_m)\,ds_1\cdots ds_p
=\frac1{p!}\left(\int_0^1a(s)ds\right)^p.
\]

Combining (3) and (4),

\[
\boxed{\|F_p\|\le\|h\|\left(2k\int_0^1a(s)ds\right)^p.} \tag{5}
\]

This remains valid with arbitrary term weights, because all weights enter the absolute local-strength sums.

## 3. Apply the coefficient lemma to the layer product

Choose `A(s)=-cH_j/2` on slice `[(j-1)/c,j/c]`. Its endpoint propagator is exactly `Q(t)`, and disjointness implies

\[
a(s)\le\frac{cJ_j}{2},\qquad
2k\int_0^1a(s)ds\le k\sum_jJ_j=K.
\]

The same bound holds for every suffix `U_{>j}=E_c...E_{j+1}` by putting zero generators on its omitted slices. Hence, for a local term `h_e`, all those conjugations have Taylor coefficients bounded by `||h_e||K^p`.

For Hermitian `h_e`, because every factor is a Hermitian exponential for real `t`,

\[
U(-t)=U(t)^{-\dagger},\qquad
(U(t)h_eU(t)^{-1})^\dagger=U(-t)h_eU(-t)^{-1}.
\]

Only even coefficients contribute to the Hermitian part. For `K|t|<1`, the absolutely convergent geometric majorant yields

\[
\boxed{\|\operatorname{Herm}(U(t)h_eU(t)^{-1})-h_e\|
\le\|h_e\|\frac{(Kt)^2}{1-(Kt)^2}.} \tag{6}
\]

## 4. Relative left generator, positive sandwich, logarithm

As in `PHYSICS_THEOREM.md`, put `R(t)=Q(t)e^{tH/2}`. Direct differentiation gives

\[
G(t)=R'(t)R(t)^{-1}
=\frac12\sum_j[\operatorname{Ad}_{Q(t)}H_j
-\operatorname{Ad}_{U_{>j}(t)}H_j].
\]

Use (6) termwise; each local term contributes twice with prefactor `1/2`, so

\[
\|\operatorname{Herm}G(t)\|
\le L\frac{(Kt)^2}{1-(Kt)^2}.
\]

The Rayleigh-norm differential inequality for `R'=GR` yields

\[
e^{-2b}I\preceq R(\delta)^\dagger R(\delta)\preceq e^{2b}I,
\quad b=L\int_0^\delta\frac{(Kt)^2}{1-(Kt)^2}dt
=L\left[\frac{\operatorname{atanh}(K\delta)}K-\delta\right].
\]

Congruence by `e^{-delta H/2}` followed by operator-monotonicity of the logarithm gives `||logP+delta H||<=2b`. Finally,

\[
\int_0^\delta\frac{K^2t^2}{1-K^2t^2}dt
\le\frac{K^2\delta^3}{3(1-K^2\delta^2)},
\]

proving (1). Applying log-trace-exponential Lipschitzness to `r logP(beta/r)` and `-beta H` proves (2). At no point are powers taken in Loewner order.

## 5. Conditional interface to the NEW adaptive-cap sparsifier

The physical theorem does not itself establish sparsification or trimming. If a separately verified construction provides a rounded Hamiltonian with

\[
L'\le2ng,\qquad cJ'\le20kg,\qquad K'=kcJ'\le20k^2g,
\]

then taking an integer

\[
r\ge\max\left\{2K'\beta,\frac83K'\beta\sqrt{g/\tau}\right\}
\]

ensures product-formula free-energy-density error at most `tau/4`. Indeed the denominator in (2) is at least `3/4`, and the resulting free-energy bound is at most `16g(K')^2 beta^2/(9r^2)`.

This interface must use the separately proposed cap based on the **actual** sampling parameter `lambda=q_s g/L`; the earlier frozen coarse cap does not automatically imply these premises. No statement about a vanishing-accuracy counting runtime is inferred here without the corresponding size/precision analysis.

## 6. Primary credit

**Kuwahara, Mori, Saito, _Floquet-Magnus Theory and Generic Transient Dynamics in Periodically Driven Many-Body Quantum Systems_ (2016), arXiv:1508.05797v3, Appendix B, Lemma 3, Eq. (B2); specialization Eq. (B6).**

https://arxiv.org/pdf/1508.05797

Their lemma bounds nested commutators of distinct few-body, locally extensive generators by the product of their local strengths and growing support sizes. Equation (B6) gives the factorial bound used here. Our time-sliced application and scalar simplex integration directly use this established machinery; there is no claim that the nested-commutator ingredient is new.

**Arad, Kuwahara, Landau, _Connecting global and local energy distributions in quantum spin models on a lattice_ (2016), arXiv:1406.3898v3, Lemma 3.1 and its proof.**

https://arxiv.org/pdf/1406.3898

This is related primary precedent for short imaginary-time conjugation bounds based on bounded local interaction strength rather than raw graph degree. Its assumptions/conventions differ, so our constants are established explicitly above rather than silently imported.
