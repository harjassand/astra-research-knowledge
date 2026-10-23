# Joint low-weight / high-weight information budget

Contributor: `/root/critical_budget`. Scientific date: 22 October 2026,
Australia/Brisbane. This is a new finite information lemma and an asymptotic
reduction for the owner's critical-window question. It is not an endpoint
transport theorem and makes no historical-novelty claim.

## Native setting and notation

Let `pi,q` be strictly positive probability vectors on a finite space and put
`W=pi/q`. Assume `D(pi||q)<=K`, where K>0 is fixed. For `0<h<1/2` and
`R>e`, define

\[
 A=\{W<h\},\quad H=\{W>R\},\quad
 b=q(A),\quad t=\pi(H),\quad k_b=-\log(1-b).
\]

These sets are disjoint. Necessarily b<1 since `E_q W=1`. Empty sets are
allowed, with `0 log 0=0`. All quantities in this note concern the actual
native distributions; no target values are revealed to the sampler.

## 1. A finite joint budget

**Lemma 1.** If `h+t<=1`, then

\[
 D(\pi\|q)\ \ge\ t\log R+hb\log h+
 (1-hb-t)\log\frac{1-hb-t}{1-b}. \tag{1}
\]

Consequently,

\[
 k_b+t\log R
 \le K+(h+t)(k_b+1)+h\log(1/h). \tag{2}
\]

In particular, put

\[
 B_h=\frac{K+H_2(h)}{1-h},\qquad
 a_R=\min\{1,K/(\log R-1)\}.
\]

Whenever `h+a_R<=1`, the following entirely uniform finite inequality holds:

\[
 \boxed{\quad k_b+t\log R\le K+E(K,h,R),\quad
 E(K,h,R)=(h+a_R)(B_h+1)+h\log(1/h).\quad} \tag{3}
\]

No support-size, minimum-probability, reverse-KL or spectral quantity enters
(1)--(3).

**Proof.** Let `a=pi(A)<=hb` and `c=q(H)`. On H the actual log density is
larger than `log R`, so its entropy contribution is at least `t log R`.
Log-sum on A and on the remaining set, and `q((A union H)^c)=1-b-c<=1-b`,
give

\[
 D(\pi\|q)\ge t\log R+a\log(a/b)
 +(1-a-t)\log\frac{1-a-t}{1-b}. \tag{4}
\]

For b>0 the derivative of the last two terms with respect to a is

\[
 \log\frac{a(1-b)}{b(1-a-t)}.
\]

It is nonpositive for `a<=b(1-t)`. Our assumptions give
`a<=hb<=b(1-t)`, so (4) is minimized over `0<=a<=hb` at `a=hb`. This
proves (1). If b=0, then a=0 and (1) follows directly from (4).
Endpoint cases follow by continuity.

Write `x=hb+t`. The right side of (1) is

\[
 t\log R+(1-x)k_b+hb\log h+(1-x)\log(1-x).
\]

For `0<=x<=1`, `(1-x)log(1-x)>=-x`. Also `x<=h+t`, and
`hb log(1/h)<=h log(1/h)`. Rearrangement yields (2).

For completeness, binary log-sum on A gives

\[
 K\ge -H_2(a)+(1-a)k_b\ge-H_2(h)+(1-h)k_b,
\]

because `a<=h<1/2`; hence `k_b<=B_h`. Binary log-sum on H, using
`t/c>R`, gives

\[
 K\ge t\log R+(1-t)\log(1-t)\ge t(\log R-1),
\]

so `t<=a_R`. Inserting both bounds into (2) proves (3). QED.

### Sharp meaning of the two budget terms

The first term `k_b=-log(1-b)` is the limiting entropy expense of a low-weight
region with proposal mass b and vanishing target mass. The second term
`t log R` is entropy already committed to the high-weight tail. Formula (3)
proves that they share one budget, with an explicit vanishing remainder.
It is not legitimate to give both terms an independent budget K.

## 2. Critical scaling and a useful uniform remainder

Assume the owner's nondegenerate critical regime

\[
 r_0=\alpha e^{-K}/\beta<1,\qquad c_*=F^{-1}(r_0)\in(0,1),
 \quad F(c)=c(1-c)^{(1-c)/c},\quad \beta=1-\alpha.
\]

Let `L=log n` and

\[
 u_n=\eta_n L=\frac{\log L}{c_*}+s+o(1)
\]

for a fixed real s. Use the actual instance-dependent sets with deterministic
cutoffs

\[
 h_n=u_n^{-4},\qquad R_n=n/L^4.
\]

For all sufficiently large n these cutoffs satisfy the hypotheses above.
Writing `b_n=q_n(W_n<h_n)`, `t_n=pi_n(W_n>R_n)` and
`k_n=-log(1-b_n)`, (3) gives

\[
 \boxed{\quad k_n+t_n\log R_n\le K+e_n,\qquad
 e_n=O_K(\log u_n/u_n^4+1/L)=o(u_n^{-2}).\quad} \tag{5}
\]

Indeed `B_(h_n)=K+O_K(h_n log(1/h_n))` and `a_(R_n)=O_K(1/L)`.
Also `t_n=O_K(1/L)` and `log R_n=L-4log L`, so

\[
 k_n+L t_n\le K+o(1),\qquad 0\le k_n\le K+o(1). \tag{6}
\]

In particular, if `k_n->K` (equivalently `b_n->1-exp(-K)`), then
`L t_n->0`. A sequence saturating the available low-weight proposal mass
has no positive leading `1/log n` target-tail entropy left.

More quantitatively, if `delta_n=(1-exp(-K))-b_n->0`, then Taylor expansion
at the fixed positive `exp(-K)` and (5) show

\[
 t_n\log R_n\le e^K\delta_n+O_K(\delta_n^2)+e_n. \tag{7}
\]

Negative delta is permitted in this formula; it is itself limited by (5).

## 3. Information slack makes the strict transport theorem sufficient

The following is a new consequence of the accepted incoming finite killed-
operator certificate, not a new proof of that certificate. We retain its
actual local rejection diagonal, killed-G row mass, full first-hit measures
and all post-hit returns. Native `Q,eta` remain fixed within every run.

**Theorem 2 (critical endpoint reduction).** Consider any sequence of native
finite instances with fixed K,alpha and the critical screens above. Let

\[
 d_n=\|q_n C_{\eta_n}^{\,n}-\pi_n\|_{\rm TV}.
\]

If along a subsequence `k_n->k<K`, then

\[
 \limsup L(d_n-t_n)\le0,\qquad
 \boxed{\ \limsup Ld_n\le K-k.\ } \tag{8}
\]

If instead `k_n->K`, then `Lt_n->0` by (6), but (8) is not claimed. It is
exactly this entropy-saturating case that still needs endpoint transport
control.

**Proof.** Since k<K and `F(c_*)=alpha exp(-K)/beta`, choose a fixed
`c in (c_*,1)` so close to c_* that

\[
 F(c)<\alpha e^{-k}/\beta.
\]

Choose a fixed `delta_0` strictly between `beta F(c)/alpha` and `exp(-k)`.
Eventually `q_n(A_n^c)=exp(-k_n)>=delta_0`. The incoming killed-operator
proof uses a lower bound on that actual safe-set proposal mass; its entropy
expression for the bound is only one sufficient way to obtain it. Therefore
its proof applies with this `delta_0` and with the actual cutoffs h_n.
All contraction and summed-first-hit constants can be fixed uniformly in n:

\[
 H_0=1-\alpha\delta_0+\beta F(c)<1,\quad
 \bar\theta=\min\{1/2,-\log H_0/(2\log2)\},\quad
 \rho=(1+\sqrt{H_0})/2<1,\quad S=1+[2(1-\rho)]^{-1}.
\]

Here H_0>0 because `alpha delta_0<1`. For n large,
`theta_n=min(c eta_n,bar theta)=c eta_n`. Reading Section 6 of the
accepted proof before replacing its actual tail by the entropy envelope
provides

\[
 d_n\le t_n+\rho_0^{\lfloor n/2\rfloor}
 +S\left[(t_n/R_n)^{\theta_n}
 +\{(M/h_n+1)\bar J_n\}^{\theta_n}\right]
 +\sqrt{(M+R_n)\bar J_n}, \tag{9}
\]

where `rho_0=1-alpha delta_0/2<1`, `M=exp(2K+1)`, and
`bar J_n=2/[alpha(2(n-floor(n/2))+1)]`. The anchor still uses K and is
unchanged. No constant in S depends on n or support size.

Since `t_n=O(1/L)`, both powered terms in (9) are bounded by
`exp(-c u_n+o(1))`. The contribution of `log(1/h_n)=4 log u_n` is
`eta_n log(1/h_n)=O(u_n log u_n/L)=o(1)`. Thus

\[
 L e^{-c u_n+o(1)}
 =e^{-cs+o(1)}L^{1-c/c_*}\longrightarrow0.
\]

The exponential waiting term vanishes after multiplication by L, and the
square-root term is `O(L^-2)`. Hence `limsup L(d_n-t_n)<=0`. Finally (6)
gives `limsup Lt_n<=K-k`, proving (8). QED.

### Consequences for the remaining full-class problem

1. On every subsequence with positive information slack, the critical-scale
   risk is bounded by the **remaining** ordinary-tail budget `K-k`, not by
   an independently available K plus a transport amplitude.
2. If `Lt_n->tau>0`, then (6) ensures a fixed positive slack in k_n. The
   strict killed-operator proof alone consequently gives
   `limsup Ld_n<=tau`. Any critical transport contribution is then
   negligible at the `1/log n` scale.
3. To prove the conjectured full-class upper
   `limsup L R_(eta_n)(n)<=max(K,(1-exp(-K))*exp(-c_*s))`, it suffices to
   prove the transport upper on sequences satisfying
   `k_n->K` and `Lt_n->0`. This reduction is rigorous by subsequence
   compactness: k_n lies in `[0,K+o(1)]`, and every convergent subsequence
   either has k<K, covered by (8), or has k=K, covered by the proposed
   endpoint theorem. Near-maximizing finite instances can be chosen at each n
   even if the class supremum is not attained.

The reduction does **not** establish that remaining endpoint theorem. Nor
does it exclude more complicated transport or post-hit-return geometry in
entropy-saturating instances. It supplies the precise budget division needed
before an endpoint transport argument could yield the maximum envelope.

## 4. Source dependencies, status, and measured work

Read native sources:

- `cycle4_pro3/research/CONTINUATION_SEED.md`.
- `cycle4_pro3/research/CRITICAL_WINDOW_LOWER.md`.
- `cycle4_pro3/research/sources/incoming_operator/control/PROOF_OR_OBSTRUCTION.txt`,
  especially Sections 4--6. The exact source hash is recorded in the companion
  receipt. Its old pre-sharpness status text is historical; its finite
  certificate is the already accepted dependency.

Lemma 1 is a direct finite log-sum calculation. Theorem 2 uses the accepted
finite certificate at a strict c>c_* made possible by actual information slack.
It never substitutes c=c_* into a strict theorem. No matrix powers, empirical
fit, external data, random tests or numerical jobs were used. Code is not
needed for the proof. Active inference cost, total model cost and prior
programme costs are unknown. Parent owner acceptance is pending.
