# A critical-window amplitude lower bound

Principal continuation: Astra PRO3. Scientific date: 22 October 2026.
This is a separate refinement following the completed first-order theorem.
The main source `BRANCHING_SHARPNESS.md` is unchanged. The statement below
has a focused independent source-bound review in `reviews/critical_window_review.md`;
the review's receipt controls its actual status.

## Statement

Keep exactly the native finite positive class, fixed K,alpha and proposal-start
kernel of `BRANCHING_SHARPNESS.md`. Assume additionally

\[
 r_0=\alpha e^{-K}/(1-\alpha)<1.
\]

Let c_*=F^{-1}(r_0) in (0,1), b_K=1-exp(-K), and fix a real s. For deterministic
across-run screens with

\[
 u_n:=\eta_n\log n=\frac{\log\log n}{c_*}+s+o(1),
\]

the actual minimax risk satisfies

\[
 \boxed{\displaystyle
 \liminf_{n\to\infty}(\log n)R_{\eta_n}(n)
       \ge \max\{K,b_K e^{-c_*s}\}.} \tag{CW1}
\]

This is a LOWER bound, not an exact critical prefactor or a limit-existence
theorem. The maximum is supplied by two legitimate lower families; their KL
budgets are not added. At s=0 the ordinary K lower is stronger because b_K<K.
For s sufficiently negative the new term is larger. The bound is consequential
inside the previously unresolved critical window, while leaving its upper
and exact value open.

## 1. A controlled varying-degree family

Let L=log n, u=u_n and set

\[
 v_*=-\log(1-c_*)/c_*,\quad
 m=\operatorname{round}(u/v_*),\quad
 D=\max\{2,\lceil u^2\rceil\},\quad
 b=b_K-u^{-2},\quad p=L^{-4}.
\]

For all sufficiently large n, b>0 and m>=1. Set

\[
 z=(p/(bnL^2))^{1/m},\quad s_{\rm scr}=(z/D)^{\eta_n},\quad
 f=\frac{\beta D}{2(D+1)}s_{\rm scr}.
\]

Use the SAME native D-ary tree probabilities and symmetric edge proposal as
in main equations (6)-(7). Unlike the main proof's strict-approximation lower,
this refinement lets D and b vary with n. Each Q,eta remains fixed during
its individual trajectory. No conclusion from the fixed-D asymptotic is
silently substituted: every needed error is controlled below.

Level q masses are bz^i and level target masses are p n^{-2(m-i)}. In
particular W_m=nL^2, W_(m-1)=L^2z/n and the common weights do not depend
on the level cardinality. Here m is of order u, u is of order log L and

\[
 \log(1/z)=[L+6\log L+\log b]/m\asymp L/u.
\]

Thus the nonroot tree q mass `S_q=sum_(i>=1)^m bz^i` is
O(exp(-a L/u)) for some fixed a>0. It is o(u^-r) for every fixed r>0.
Both q,pi remain strictly positive, and

\[
 q_\star=e^{-K}+u^{-2}-S_q.
\]

All preterminal weights are below one and the star is between them and W_m.
The main KL upper is valid with these varying parameters:

\[
 D(\pi\|q)\le p\log(nL^2)+\log(1/q_\star)
 = K-e^K u^{-2}+o(u^{-2})<K. \tag{CW2}
\]

Indeed the positive leaf term is O(L^-3)=o(u^-2), and Taylor expansion of
the logarithm around the fixed positive e^-K is uniform here. No rounded
normalization or singular instance is used.

The required branch inequalities hold: `D=O(u^2)`, `s_scr<=1`, and hence
`n^2/(D s_scr)>=1` eventually and `D s_scr/n^2<1`. Therefore forward local
acceptance is s_scr and reverse acceptance is D s_scr/n^2, exactly as before.
The symmetric finite graph has

\[
 1+\sum_{i=0}^m D^i=\exp[O(u\log u)]
   =\exp[O(\log\log n\,\log\log\log n)]
\]

vertices. The class permits this growth; it is explicitly larger than the
fixed-degree polynomial-in-log-n family used for the first-order theorem.

## 2. Screening and competition errors

Set `v_n=-log s_scr`. The exact identity from the main construction becomes

\[
 m v_n=u+\eta_n[6\log L+\log b]+m\eta_n\log D=u+o(1). \tag{CW3}
\]

The accumulated error is at most
O(u log L/L+u^2 log u/L), which tends to zero. It follows that v_n tends to
the finite positive v_* and f tends to `beta exp(-v_*)/2>0`.

The exact level-exit upper in main (11) still holds algebraically, for every
D. Its extra terms beyond f+alpha(1-b)/2 are O(n^-2) uniformly. The effective
competition parameter is

\[
 r_{b,D}=\frac{\alpha(1-b)(D+1)}{\beta D}
        =r_0+O(u^{-2}). \tag{CW4}
\]

Since m=O(u), replacing r_(b,D) by r_0 in a sum of m smooth log factors
costs O(1/u). Replacing v_n by u/m costs o(1) by (CW3). Thus the actual
capture factor in the finite lower obeys

\[
 \log[(f/E)^m]=-m\log(1+r_0 e^{u/m})+o(1). \tag{CW5}
\]

This estimate preserves the entire cumulative loss; an unspecified per-step
o(1) would not suffice when m grows.

## 3. Optimal rounding has no fixed loss

Let g(v)=log(1+r_0 exp(v)) and H_u(x)=x g(u/x). At the unique optimum v_*,
the variational identity in the main proof gives

\[
 g(v_*)=c_*v_*,\quad g'(v_*)=c_*,\quad
 H_u'(u/v_*)=g(v_*)-v_*g'(v_*)=0.
\]

For x within one of u/v_*,

\[
 H_u''(x)=u^2 g''(u/x)/x^3=O(1/u).
\]

Because the nearest integer m differs from u/v_* by at most one half,
Taylor's theorem yields

\[
 m\log(1+r_0 e^{u/m})=c_*u+O(1/u). \tag{CW6}
\]

This removes the main theorem's harmless but nonvanishing O(1) log-error.
Combining (CW5)-(CW6) and b->b_K, the marked capture mass before timing and
retention is `b_K exp(-c_*u)(1+o(1))`.

## 4. Actual time, retention and TV subtraction

The main finite event certificate, equation (14), applies to the present
parameters without modification. Its global escape lower
`D0=alpha q_star/2` tends to the positive constant alpha exp(-K)/2, and
H=floor(n/(2m)) has order n/u. Consequently
`m exp(-D0 H)->0`. Its waiting factor is 1+o(1) relative to capture.

The exact leaf escape is
`e_m=alpha(1-p)/(2nL^2)+f/n^2`, so n e_m->0. Its retention factor is also
1+o(1) relative to capture. Finally p=L^-4=o(L^-1), while

\[
 e^{-c_*u}=L^{-1}e^{-c_*s}(1+o(1)).
\]

Taking the TV event to be the complete leaf set gives
`liminf L R >= b_K exp(-c_*s)`. The unchanged Q=I two-state family gives
`liminf L R>=K`. Their maximum proves (CW1).

## 5. Consequence and next unresolved obligation

The main first-order limit is closed. This refinement begins the next question
with an actual additional theorem: the critical curve cannot lie below
`max(K,(1-exp(-K))*exp(-c_*s))` when r_0<1. At K=1,alpha=1/2, the branching
term exceeds one for

\[
 s<\frac{\log(1-e^{-1})}{c_*}.
\]

The current incoming upper has fixed strict c<c_* and loses control of this
prefactor as c approaches c_*. An exact critical law requires a uniform
bound on accumulated reachable first-hit mass, or a proved obstruction to
such a law, with the endpoint constants retained. The next investigation is
whether the displayed lower envelope is exact or whether a heterogeneous
branching/transport mechanism produces a larger amplitude. A proposal alone
does not count as resolving that question.

No claim is made for r_0>=1 in this refinement: its optimizing v is not finite
and the above Taylor argument would not apply. The main theorem still covers
that region. No numerical computation or sampler-speedup inference is used
in this critical-window proof. Active model/discovery costs are unknown and
must not be replaced by the runtime of the finite checks elsewhere.
