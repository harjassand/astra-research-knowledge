# Independent challenge: initial IMH low-weight tails

Reviewer: `/root/prefix_upper_challenge`, 21 October 2026. This is a new
initialization lemma for the owner's proposed continuation, not a rerun of the
completed joint-KL theorem. No historical-priority claim is made.

## Verdict

The proposed bound is valid. The informal argument based on a single downward
crossing is insufficient, because the chain can descend through intermediate
weights. A first-high-proposal decomposition proves the bound without that
argument. It also gives a useful exact subprobability decomposition on arbitrary
measurable spaces.

## Definitions

Let `pi` and `q` be equivalent probability measures, let `W=dpi/dq` be positive
and finite outside their common null set, and let `G` be ordinary independence
Metropolis-Hastings with proposal `q` and target `pi`. Let

\[
\mu_m=qG^m,\qquad N=m+1,\qquad A=\{W<h\},\qquad b=q(A),
\]

where `m` is a nonnegative integer and `h>0`. Write `q_lo=q|A` and
`q_hi=q|A^c` as unnormalized restrictions. Each update uses a fresh independent
`q` proposal and fresh independent uniform acceptance variable. The initial
candidate is also an independent `q` draw.

Define a sub-Markov kernel `G_lo` by keeping only proposal draws in `A`:

\[
G_{\rm lo}(x,E)=\int_A q(dy)\left[
 a(x,y)1_E(y)+(1-a(x,y))1_E(x)\right],
\quad a(x,y)=\min\{1,W(y)/W(x)\}.
\]

Its row mass is `b`. Let `nu_m=q_lo G_lo^m`. Then `nu_m` has total mass
`b^N` and is supported on `A`.

## Exact first-high-proposal identity

For every nonnegative integer `m`,

\[
\boxed{\quad
\mu_m=\nu_m+\sum_{j=0}^{m}b^j q_{\rm hi}G^{m-j}.
\quad}                                                     \tag{1}
\]

Index the initial candidate by zero and the subsequent proposals by
`1,...,m`. If all `N` candidates lie in `A`, the unnormalized output law is
exactly `nu_m`. Otherwise let `j` be the first candidate outside `A`.
The preceding `j` candidates lie in `A`, an event with probability `b^j`.
The state immediately before candidate `j` must therefore have weight `<h`.
The new candidate has weight `>=h` and is accepted with probability one.
Thus its unnormalized reset law is `b^j q_hi`. The remaining `m-j` ordinary
updates have output law `b^j q_hi G^(m-j)`. The events are disjoint and cover
all sample paths. This proves (1); no conditional distribution on a point
or disintegration is required.

The identity also applies for `m=0` and for `b=0` or `b=1` under the ordinary
conventions for zero measures and an empty sum.

## Low-weight consequence

On `A^c`, `q_hi<=pi/h` as measures. Invariance of `G` therefore gives

\[
q_{\rm hi}G^k\le \pi/h \quad(k\ge0).
\]

Let `D` be any measurable subset of `A`. Since `q_hi(D)=0`, the `j=m`
summand in (1) vanishes on `D`. Consequently

\[
\boxed{\quad
\mu_m(D)\le b^{m+1}+\frac{\pi(D)}h\sum_{j=0}^{m-1}b^j
\le b^{m+1}+\frac{m\pi(D)}h.
\quad}                                                     \tag{2}
\]

The geometric-sum version is sharper and remains defined at `b=1`.
In particular, for `0<delta<h` and `D={W<delta}`,

\[
\mu_m(W<\delta)\le q(W<h)^{m+1}+m\delta/h,                  \tag{3}
\]

because `pi(D)<=delta q(D)<=delta`. This proves the exact proposed tail
lemma with `m`, not merely `N`, in the additive term. Gradual downward
motion after the first high proposal is already covered by measure domination
and invariance; it cannot invalidate (2).

## Consequence under both KL budgets

If `D(q||pi)<=J`, choose `delta=1/B`, `h=1/sqrt(B)` with `B>e^2`.
The standard binary entropy tail bound gives

\[
q(W<h)\le \frac{J}{\tfrac12\log B-1}.
\]

For one initial global transition, (3) yields

\[
\mu_1(W<1/B)\le
 \left(\frac{J}{\tfrac12\log B-1}\right)^2+B^{-1/2}.         \tag{4}
\]

This is `O_J((log B)^-2)`. It supplies the second-order low-weight tail
needed by the owner's anchored smoothing argument. It does not itself prove
the complete hybrid mixing theorem, an algorithmic speedup, or a conclusion
for a different schedule.

## Consequence using forward KL alone

For `0<h<=1/2`, let `a=pi(A)<=h b<=h`. Binary data processing and the
binary entropy `H_2` give

\[
K\ge d(a\Vert b)
 =-H_2(a)+a\log(1/b)+(1-a)\log(1/(1-b))
 \ge -H_2(h)+(1-h)\log(1/(1-b)).
\]

Therefore

\[
b\le b_K(h):=1-\exp\left[-\frac{K+H_2(h)}{1-h}\right],
\qquad b_K(h)\longrightarrow 1-e^{-K}\quad(h\downarrow0).
                                                               \tag{5}
\]

This is a convenient explicit bound, not an asserted exact extremizer at
positive `h`. Together with (2), it supports a logarithmic prefix length:
for any fixed `c>1/[-log(1-e^-K)]`, choose a sufficiently small **fixed**
`h` so that `c[-log b_K(h)]>1`. Then `m=ceil(c log(1/eps))` satisfies
`b^(m+1)=o(eps)` uniformly over the forward-KL class. If the subsequent
hybrid's cutoff `B` is exponential in `1/eps`, `m/(Bh)=o(eps)` too.
There is no need to make `h` vary with `eps` for the strict-above-threshold
claim. The owner must separately establish the hybrid smoothing bound and
the matching lower obstruction.

## Another useful elementary bound

The output after `m` IMH updates is one of the `N=m+1` proposals, including
the initializer. Hence for every measurable `E`,

\[
\mu_m(E)\le Nq(E),\qquad d\mu_m/d\pi\le N/W.               \tag{6}
\]

This union bound, together with (2), is enough to control a weighted core
integral and both outer masses. Monotonicity of the density as a function
of `W`, and any exact uniform-priority representation, are unnecessary for
these bounds.

## Limitations and rejected shortcut

The invalid informal implication was: “after reaching weight `h`, a later
visit to `D` must use an acceptance probability at most `W(y)/h`.” That
fails if intermediate accepted states have weight below `h`. The exact
reset-law decomposition is the repair. No upper bound has been assumed on
`W`, `dq/dpi`, or an initial `L2` norm. The prefix uses ordinary IMH and
fresh proposal randomness; adaptive changes to its proposal law are outside
this argument. All statements concern ideal-real kernels. The full
comparison to pure IMH and physical computation costs remain the owner's
responsibility.

An accompanying exact-rational finite-state check tests identity (1) and
inequalities (2), (6). Its purpose is to expose implementation/sign mistakes,
not to prove the general measurable-space statement above.

## Second challenge: the owner's stronger low-set oscillation lemma

The owner subsequently supplied a stronger mechanism. The following checks
are separate from the preceding initial-tail argument. Let

\[
C=(I+H)/2,\quad H=\alpha G+\beta L,\quad \beta=1-\alpha,
\quad g=C^t1_F,
\]

where `L` is fixed and `pi`-reversible, `0<alpha<1`, and `F` is measurable.
Use the previously proved anchor `A0={W<=M}`, `s0=pi(A0)>0`,
`m0=pi(g 1_A0)/s0`, with `0<=m0<=1`. Take `B,R>e`,
`D={W<1/B}`, `E={W>R}`, `S=(D union E)^c`, `b=q(D)`, `a=pi(E)`.
The accepted smoothing proof gives

\[
\int (g-m_0)^2/\max(W,M)\,d\pi
 \le [\alpha s_0(2t+1)]^{-1},
\]

and `|g-Hg|<=eta_t` pointwise. With

\[
\Delta=\sqrt{[M(B+1)+R]/[\alpha s_0(2t+1)]},
\]

the q-core estimate and `q(E)<=a/R` imply

\[
\left|q(g1_{D^c})-(1-b)m_0\right|\le\Delta+a/R.              \tag{7}
\]

### Exact restricted-kernel identity

For every `x` in `D`, all proposals in `D^c` are accepted. A proposal in
`D` leaves the updated state in `D` regardless of acceptance or rejection.
Therefore `G(x,D)=b` exactly. If `b>0`, define the Markov kernel on `D`

\[
P_D(x,A)=G(x,A\cap D)/b.
\]

Then, for `x` in `D`,

\[
Gg(x)=bP_Dg(x)+q(g1_{D^c}).                                \tag{8}
\]

Let `v=g-m0` and
`e0=alpha(Delta+a/R)+eta_t`. Equations (7), (8) and near-harmonicity give

\[
v=\alpha bP_Dv+\beta(Lg-m_0)+e,\qquad |e|\le e_0
\quad\hbox{on }D.
\]

Taking the ordinary supremum and infimum of the bounded function `v` on
`D`, and using `0<=Lg<=1`, proves

\[
-\kappa_b m_0-\delta_t\le g-m_0
 \le\kappa_b(1-m_0)+\delta_t\quad\hbox{on }D,               \tag{9}
\]

where

\[
\kappa_b=\frac{\beta}{1-\alpha b},\qquad
\delta_t=\frac{\alpha(\Delta+a/R)+\eta_t}{1-\alpha b}.
\]

The denominator is at least `beta>0`. No attainment of either extremum
is required. The `b=0` case contributes zero to all `q`- or `mu_m`-integrals
and can be omitted. The improvement over the previous small-`b` estimate
comes from retaining the exact repeated-return probability `alpha b`.

### Measurable-space and version qualifications

Take actual bounded kernel iterates `g=C^t1_F`; all `H^j1_F` have values
in `[0,1]`, so the binomial identity and near-harmonic estimate are pointwise.
Assign `W` any positive finite value on its common null exceptional set when
defining the IMH kernel there. Then ordinary suprema on `D` apply directly
to bounded functions, without a regular conditional distribution or a
measurable maximizer. The spectral statements involve only their `L2(pi)`
classes and their integrals agree with these versions.

Alternatively, using `pi`-essential extrema causes no gap: `pi`-invariance
of `G` implies that it gives zero mass to a `pi`-null set for `pi`-almost
every starting point. The restricted kernel `P_D` inherits that property.
Equivalence transfers the almost-everywhere qualification to `q`, and
`mu_m<<q` by (6).

### Outside integration for a general prefix law

Let `mu=mu_m` and `z=mu(D)`. No sign assertion about `mu-pi` on `D`
or `E` is needed. By (9), the upper bound for the outside signed integral is

\[
\int_{D\cup E}(g-m_0)(d\mu-d\pi)
 \le \kappa_b z(1-m_0)+a m_0
       +\delta_t z+\pi(D)+\mu(E).
\]

For the lower bound, apply the same estimates to the negative of the
integral; this exchanges `m0` and `1-m0`. In both cases the first two
terms are a convex combination of `kappa_b z` and `a`. Therefore

\[
\left|\int_{D\cup E}(g-m_0)(d\mu-d\pi)\right|
 \le \max\{\kappa_b z,a\}+\delta_t z+\pi(D)+\mu(E).         \tag{10}
\]

Both discarded masses are small: `pi(D)<=1/B` and
`mu(E)<=Nq(E)<=Na/R`.

For the core write `f_mu=dmu/dpi<=N/W`, by (6). Splitting at `W=M`,

\[
\int_S\max(W,M)(f_\mu-1)^2\,d\pi
 \le M(N^2B+1)+N^2+R=:U_N.                                \tag{11}
\]

Below `M`, use `(f_mu-1)^2<=f_mu^2+1` and `W^-2<=B/W`.
Above `M`, use `W(f_mu-1)^2<=N^2/W+W`, whose two integrals are at
most `N^2` and `R`. The anchor Cauchy-Schwarz bound therefore gives

\[
\boxed{\quad
\operatorname{TV}(\mu_m C^t,\pi)
 \le \max\{\kappa_b z,a\}+\delta_t z+
       \sqrt{U_N/[\alpha s_0(2t+1)]}+1/B+Na/R.
\quad}                                                     \tag{12}
\]

All constants and multipliers in the owner's stated estimate check out.

### Verified upper consequence, not the lower theorem

For a fixed finite prefix length `m`, under `D(pi||q)<=K`, set
`M=exp(2K+1)`, `s0>=1/2`, `B=R=t/(log t)^4`, and use (2) with
`h=B^-1/2`. Then `a`, `delta_t`, the core term and both small masses
vanish uniformly. Equation (5) bounds both `b` and the first-high bad mass,
and its right side tends to `b_K=1-exp(-K)`. Thus (12) proves

\[
\limsup_{t\to\infty}\sup_{\text{admitted forward-KL class}}
 \operatorname{TV}(qG^m C^t,\pi)
 \le \frac{\beta b_K^{m+1}}{1-\alpha b_K}.                 \tag{13}
\]

This reviewer verifies the upper bound and its uniformity, not the proposed
matching lower family, which is assigned separately. The limit order keeps
`m`, `K`, and `alpha` fixed here. Deriving growing-prefix minimax mixing-time
claims requires their own parameter accounting; (13) must not be substituted
for that argument.

### Diagnostic receipt

`check_prefix_tail_exact.py` passed on its first recorded execution, using
`fractions.Fraction` without a tolerance: 30 positive finite chains,
5 thresholds each, and prefix lengths 0 through 7. This produced 1,200
exact reset-identity checks and 1,200 exact tail checks; 403 checks had
positive tail mass and an upper bound below one. Observed script wall time
was 0.205299 seconds, CPU time 0.205293 seconds, and peak RSS 9,344 KiB.
The extra oscillation and general-measure estimates in (7)--(13) are checked
algebraically above; no second numerical run was needed to settle those
proof obligations.
