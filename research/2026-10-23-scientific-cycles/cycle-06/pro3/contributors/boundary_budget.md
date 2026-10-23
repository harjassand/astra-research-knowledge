# Boundary information allocation and weighted capture challenge

Contributor: `/root/critical_budget`. Scientific date: 22 October 2026,
Australia/Brisbane. This continues the accepted Cycle5 source and does not
reopen its interior theorem. Principal owns the new weighted capture
construction. This contribution proves the allocation reduction and checks
the exact new finite estimate supplied by the principal; final source-bound
review of the principal's full theorem is a separate action.

## 1. Native scope and conditional allocation question

Keep finite positive pi,q, population `D(pi||q)<=K`, fixed alpha in (0,1),
beta=1-alpha, symmetric stochastic target-independent Q, proposal-start G
and the two-factor screened local L_eta. Q and eta are fixed within a run.
All support sizes are admitted; the target normalizer remains unavailable
to the sampler. Define the same actual low-weight and high-weight regions

\[
 A=\{W<h\},\quad B=A^c,\quad H=\{W>R\},\quad
 b=q(A),\quad a=\pi(H),\quad k=-\log(1-b),
\]

and

\[
 r_b=\frac{\alpha(1-b)}\beta,
 \qquad r_0=\frac{\alpha e^{-K}}\beta\ge1.
\]

At the proposed boundary scale, write L=log n and

\[
 u=\eta L=\log L+s+o(1),\qquad s\in\mathbb R\text{ fixed}.
\]

Suppose the finite transport argument yields the uniform instance bound

\[
 d_n:=\|qC_\eta^n-\pi\|_{\rm TV}
 \le a+\{b/r_b+o(1)\}e^{-u}+o(L^{-1}). \tag{1}
\]

The exact question assigned here is how (1) combines with the single KL
budget, including r_b near one and b near zero. The result is

\[
 \boxed{\limsup L R_{\eta_n}(n)
 \le\max\{K,(\beta/\alpha)(e^K-1)e^{-s}\}.} \tag{2}
\]

This is an upper reduction; a valid native lower remains a separate
obligation. No countermechanism based on mixed information allocation can
exceed this candidate if (1) holds. The finite lemma supplied by the principal
passes the analytic checks in Section 5 below.

## 2. Uniform cutoffs and the already accepted budget lemma

Use proof parameters

\[
 h=u^{-4},\quad R=n/L^4,\quad d_{\rm test}=L^{-2},\qquad
 N=\left\lceil\frac{8}{\alpha e^{-K}}\log L\right\rceil.
\]

For all sufficiently large n, h<1/2, R>e, N<n and eta<=1/2. Define

\[
 B_h=\frac{K+H_2(h)}{1-h},\quad
 a_R=\min\{1,K/(\log R-1)\},\quad
 E_n=(h+a_R)(B_h+1)+h\log(1/h).
\]

Cycle5's accepted information lemma gives, without another proof campaign,

\[
 k+a\log R\le K+E_n,\qquad k\le B_h,\qquad a\le a_R. \tag{3}
\]

Here the finite hypothesis h+a_R<=1 holds eventually. Since
`log R=L-4log L`, put

\[
 \delta_n=E_n+4a_R\log L.
\]

This is explicit, nonnegative, depends only on n and the fixed policy and
parameters, and tends to zero. More specifically,

\[
 \delta_n=O_K(u^{-4}\log u+\log L/L)=o(1),
 \qquad \boxed{k+La\le K+\delta_n.} \tag{4}
\]

The error bound has no support-size or minimum-atom constants. It is uniform
near both k=0 and k=K. In particular k lies in `[0,K+delta_n]`.

## 3. Mixed allocation cannot exceed the endpoints

The capture coefficient has the exact identity

\[
 \frac b{r_b}=\frac\beta\alpha\frac b{1-b}
             =\frac\beta\alpha(e^k-1). \tag{5}
\]

Let `C_n=(beta/alpha)L exp(-u)`, so `C_n->C=(beta/alpha)exp(-s)>0`.
From (1), (4), (5), with uniform remainders,

\[
 Ld_n\le K+\delta_n-k+C_n(e^k-1)+o(1). \tag{6}
\]

For `k in [0,K+delta_n]`, the right-hand expression without its remainder
is a convex function of k, with second derivative `C_n exp(k)>0`. It is
therefore bounded above by the maximum of its two endpoint values:

\[
 Ld_n\le\max\{K+\delta_n,
 C_n(e^{K+\delta_n}-1)\}+o(1). \tag{7}
\]

Every term and error is uniform over the native class, so taking the class
supremum and then the limsup proves (2). No near-extremizer selection or
subsequence compactness is necessary for this reduction.

For a fixed interior limiting allocation 0<k<K, the limiting sum

\[
 K-k+C(e^k-1)
\]

is strictly below the chord connecting its endpoint values. Thus even a
native construction that simultaneously realizes both its ordinary-tail
budget and its capture budget could not improve the proposed extremal
amplitude. This is a statement about the proved upper allocation, not a claim
that every intermediate allocation can actually be realized by a sampler.

### Difference from the closed interior regime

Here the transport exponent is one throughout the global-dominant region.
A positive amount of entropy slack need not make transport disappear at
scale 1/L. The interior proof's selection of a larger c cannot be copied:
c>1 is unavailable for the local screen bound. What replaces that argument
is the convexity of the remaining ordinary-tail plus capture allocation.
Merely writing a sum and declaring it to be a maximum would be invalid;
(4)--(7) establish the maximum with the actual shared budget.

## 4. Boundary and small-mass qualifications

### r_b can lie slightly below one

At r_0=1 the entropy bound only gives

\[
 r_b\ge\frac\alpha\beta\exp(-B_h)
      =1-O_K(h\log(1/h)).
\]

It does not give r_b>=1 at every finite n. A proposed estimate that assumed
a fixed positive r_b-1, or used a denominator r_b-1 without uniform control,
would fail precisely at the desired boundary. A proof with bounded weights
and a small positive energy deficit is sufficient; it is the one the
principal supplied.

### b may approach zero arbitrarily fast

The desired coefficient is continuous:
`b/r_b=(beta/alpha)(exp(k)-1)->0` as b->0. Relative error claims obtained by
dividing by b would not be uniform. The weighted lemma instead produces
`(b/w)^(1-eta)` with `w>=1`. For every `x in [0,1]`,

\[
 0\le x^{1-\eta}-x\le\eta. \tag{8}
\]

One can check the maximum exactly at `x=(1-eta)^(1/eta)`; its value is
`eta(1-eta)^((1-eta)/eta)<=eta`. Thus (8) is a uniform additive estimate,
including x=0. Since w=max(1,r_b)>=r_b,

\[
 (b/w)^{1-\eta}\le b/w+\eta\le b/r_b+\eta. \tag{9}
\]

For the upper bound no approximation of w by r_b is even required. This
avoids both a small-b singularity and the slight r_b<1 boundary excursion.
The coefficient b/r_b is uniformly bounded because `1-b>=exp(-B_h)`.

## 5. Independent algebraic challenge of the principal's exact finite lemma

The following operation was supplied by the principal for challenge. Its
construction is the principal's work, not an independent discovery claimed
by this contributor.

For E subset B, e=q(E), form the Cycle5 first-hit counter P^E: keep the actual
A rows into A union E, kill exits to B\E without renormalization, and absorb
E. Write `D=diag(q^eta)`, `p=1/(1-eta)`, `w=max(1,r_b)` and

\[
 \mathcal E_w(v)=\sum_A|v_x|^p+w\sum_E|v_x|^p.
\]

The proposed multiplier is

\[
 \Delta=[\beta-\alpha(1-b)]_+,\qquad
 \Gamma_w(e)=\frac12+\frac{2^{p-1}}2
                    (1+\Delta+\alpha w e). \tag{10}
\]

**Challenge verdict:** the inequality

\[
 \mathcal E_w(vDP^ED^{-1})\le\Gamma_w(e)\mathcal E_w(v) \tag{11}
\]

holds by the supplied argument, and the first-hit bound is exactly

\[
 \Pr_q(X_0\in A,\tau_B\le N,X_{\tau_B}\in E)
 \le (b/w)^{1-\eta}e^\eta\Gamma_w(e)^{N(1-\eta)}. \tag{12}
\]

The checks are as follows.

1. **Local columns and weighted rows.** At theta=eta the transformed
   off-diagonal entries are directly at most Q_xy, since
   `min(1,r^eta)r^(-eta)<=1`. There is no substitution c=1 into a theorem
   whose hypotheses require c<1. Counting column sums remain at most 2,
   including absorbed E columns. After Jensen, multiply each output coordinate
   by its weight 1 or w. The resulting weighted output-row sum is at most
   `L_xx+w sum_(y!=x)Q_xy<=1+w` on A, and exactly w on E. Here w>=1
   is essential to this simple bound. The actual local diagonal is retained;
   the inequality only bounds it above by one.
2. **Global columns and weighted rows.** The q-density columns remain at
   most 2b on A and exactly 1+b on E. This uses the actual G diagonal
   `G_yy<=b` and acceptance of all A-to-B proposals. Weighted Jensen is
   applied before multiplication by the output weight. Its weighted row sum
   is exactly b+w e on A and w on E.
3. **Mixture balance.** Convexity with weights 1/2,alpha/2,beta/2 gives A
   coefficient
   `1/2+2^(p-1)/2[1+beta w-alpha(1-b)+alpha w e]`.
   By definition of w, `beta w-alpha(1-b)=Delta` exactly. The E coefficient
   relative to its already weighted energy is `1/2+2^(p-1)/2`, so (11)
   follows. There is no denominator r_b-1.
4. **Initial mass and Holder.** The initial measure is q 1_A, with energy b.
   E energy controls its counting p-norm after division by w. Holder with
   q(E)=e and 1/p=1-eta gives (12), including the exponent on w. E mass
   records the first-hit event; subsequent actual propagation must still
   use the full C, as in the Cycle5 decomposition.

The estimates are uniform in support size and every positive atom mass.
Empty A or E is handled directly with zero first-hit mass.

## 6. Checking the scale needed for the allocation reduction

With the same bounded-test union construction as Cycle5, one has

\[
 \bar e=\min\{1-b, a/R+(N+1)(M/h+1)J/d_{\rm test}^2\},
 \quad M=e^{2K+1},\quad J=\frac2{\alpha(2(n-N)+1)}.
\]

The cap is eventually inactive. Uniformly,

\[
 \bar e=O(n^{-1}L^4u^5),\qquad
 \log\bar e=-L+O(\log L),\qquad
 \bar e^\eta=e^{-u}(1+o(1)).
\]

As r_0>=1,
`Delta<=alpha[exp(-K)-exp(-B_h)]_+=O(h log(1/h))`.
Also `1<=w<=max(1,alpha/beta)`, a fixed bound. An explicit convenient
estimate is

\[
 \Gamma_w(e)^{N/p}
 \le\exp\{N[\eta\log2+\Delta+\alpha w e]\}. \tag{13}
\]

Indeed `Gamma_w<=2^(p-1)(1+Delta+alpha w e)` and
`(p-1)/p=eta`. The exponent in (13) tends to zero uniformly, since
`N eta=O(u^2/L)`, `N Delta=O(log u/u^3)`, and `N bar e->0`.
Combining (9), (12) and the union-set smoothing certificate therefore
supplies precisely the conditional bound (1). The anchor, residual waiting
and direct initial E terms are all o(1/L) at these cutoffs. Actual direct
G hits are retained in the finite global coefficient alpha w e; they are
not silently deleted.

This confirms the analytic compatibility of the principal's finite lemma
with the allocation reduction. The principal's complete final theorem must
still be source-bound reviewed, including its full TV decomposition and
matching native lower. This note does not replace that review.

## 7. Failed routes, scope and resources

- Reusing the interior argument by choosing c>1 is invalid. The boundary
  allocation instead has a nontrivial sum, controlled by convexity.
- Assuming r_b>1 with a uniform margin would omit r_0=1 and finite excursions
  just below one. The exact max-weight and positive deficit handle those.
- Relative errors divided by b could fail when the low-weight proposal mass
  vanishes. The uniform additive power estimate (8) avoids this.
- A norm coefficient alone would not imply a mixing lower. The separate
  one-crossing contributor must prove reachability, competition, retention
  and positive native KL admission. None is inferred from this upper.

Read sources: `cycle5_pro3/research/CONTINUATION_SEED.md` and the complete
`cycle5_pro3/research/CRITICAL_ENDPOINT_THEOREM.md` (18,790 bytes, SHA256
4a459d8ee78253564a849b3033abc25e548224dc695fbb819cd9860e3a5c9014).
The old information proof was used as accepted capital, not re-proved as a
new result. No numerical job, matrix search, simulation, historical replay,
new data or external literature search was performed. Active inference costs,
model tokens, monetary costs and total research costs are unknown. Parent
acceptance and final source-bound review remain separate statuses.
