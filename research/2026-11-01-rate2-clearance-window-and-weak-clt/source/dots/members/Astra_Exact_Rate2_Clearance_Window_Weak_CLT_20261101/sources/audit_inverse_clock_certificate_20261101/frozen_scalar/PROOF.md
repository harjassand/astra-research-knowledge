# A validated inverse-time clearance-clock scalar

**Author construction; not an independent receipt and not a stochastic clearance theorem.**

## Result first

The maximal solution of

\[
 e'(s)=2(s+3e(s)^2/4)^2,\qquad e(0)=0
\]

has a finite blow-up time satisfying the **rationally certified**, outward-rounded enclosure

\[
 \boxed{1.106580521912579472\ \le s_*\ \le 1.106580521912579663.}
\]

The exact rational interval in `CERTIFICATE_FINE.json` has width less than
`0.000000000000000189576600`. The printed decimals are deliberately rounded
outward. No binary floating-point value, floating transcendental function,
non-rigorous numerical solver, or assumed initial datum enters this certificate.
The implementation uses Python integers and `fractions.Fraction` only. Its
recorded elapsed wall time is diagnostic, not part of the proof.

This is the scalar needed by a **candidate** corner clearance clock on the scale
`T=N^(1/5)`. It is not itself evidence that a finite count chain clears at this
time. Its source is the author mesoscopic law
`../return_path_construction_20261101/rate2_activation_debt/RATE2_MESOSCOPIC_RETURN_LAW.md`,
which is not silently promoted to an independently received theorem here. The
already received uniform actual-removal construction has a much coarser
`1+10^8 sqrt(N)` budget and does not supply the desired sharp corner clock.

## 1. Existence, finite blow-up, and inverse regularization

The polynomial forward field is locally Lipschitz. Its unique solution stays
nonnegative and is strictly increasing for positive time. Since
`e'(s)>=2s^2`, one has `e(s)>=2s^3/3` as long as the solution exists.
If it exists to 1, then `e(1)>=2/3`; subsequently
`e'>=(9/8)e^4`. Integrating `d(e^-3)/ds<=-27/8` shows that it cannot remain
finite after time 2. If it blows up before 1, the same conclusion is immediate.
Thus `s_*<=2`. A bounded solution at a finite maximal time could be extended
by local existence, so `e(s)` actually diverges as `s` increases to `s_*`.

For `e>0` its inverse `s=s(e)` satisfies

\[
 s'(e)=f(e,s)=\frac1{2(s+3e^2/4)^2},\qquad
 f_s(e,s)=-(s+3e^2/4)^{-3}<0.                 \tag{1}
\]

The inverse is singular only at the original corner `(e,s)=(0,0)`. Section 2
constructs a certified positive starting point instead of postulating one.
After that point, every positive initial `s` produces a global increasing
inverse solution at every finite `e`, since its derivative is bounded above
by its initial positive denominator.

If two inverse solutions start at the same `e`, then their order is preserved
and their distance cannot increase: where their difference is nonzero, the
sign of its derivative is opposite to its sign, by (1). Consequently

\[
 |\Phi_{a,b}(u)-\Phi_{a,b}(v)|\le |u-v|.      \tag{2}
\]

There is **no positive Gronwall exponent** in this propagation. This is a
standard one-dimensional monotonicity argument, not a new integration method.

## 2. Paid forward startup

Work on `0<=s<=s0=1/2`. The code recursively constructs the degree-78 Taylor
polynomial `P`, with `P(0)=0`, using the exact polynomial identity

\[
 f_{\rm forward}(s,e)=2s^2+3se^2+\tfrac98e^4.
\]

Its coefficients are nonnegative: each next coefficient is a nonnegative
polynomial in earlier coefficients, divided by a positive integer. Define

\[
 R(s)=2s^2+3sP(s)^2+\tfrac98P(s)^4-P'(s).
\]

The recurrence cancels every coefficient of degree less than 78. All remaining
coefficients are nonnegative. The implementation explicitly checks both facts
using exact fractions. Hence `0<=R(s)<=R(1/2)=:R0`, and `P` is a subsolution.
On the rectangle `0<=s<=1/2`, `0<=e<=1/4`,

\[
 \partial_e f_{\rm forward}=6se+\tfrac92e^3
 \le L=105/128,\qquad Ls_0=105/256<1.
\]

Put `delta=R0/(1-Ls0)` and `U(s)=P(s)+delta*s`. The code checks exactly that
`U(s0)<1/4`. Nonnegative coefficients then ensure this rectangle bound for the
entire segment, and

\[
 U'-f_{\rm forward}(s,U)
 \ge\delta-R_0-L\delta s\ge0.
\]

Scalar comparison, also excluding blow-up before `s0`, gives

\[
 P(s_0)\le e(s_0)\le U(s_0).
\]

Let `a` be `U(s0)` rounded **up** to the next multiple of `2^-120`. Since the
forward derivative is at least `2s0^2` after `s0`, its hitting time of `a` obeys

\[
 s_0\le s(a)\le s_0+\frac{a-P(s_0)}{2s_0^2}.          \tag{3}
\]

The endpoints of (3) are again rounded outward to `2^-120`. The exact startup
interval width is recorded in the certificate and is less than `4.4*10^-28`.
The complete degree, rational residual, barrier constant, and input endpoints
are included: the initial value is earned, not inferred from a decimal solver.

## 3. Executable interval arithmetic and Taylor quadrature

An interval is stored as two signed integers `[L,H]` representing
`[L/2^120,H/2^120]`. Addition is exact. Multiplication takes the min/max of
all four endpoint products and divides by `2^120`, using floor for the lower
endpoint and ceiling for the upper endpoint. Reciprocal, only for intervals
not containing zero, is monotone decreasing and rounds its two rational
endpoints outward. Every operation encloses its exact real counterpart.
No rounding mode of the host floating-point unit is relevant.

For completeness, the formal power-series recurrence that the code evaluates
with these intervals is explicit. At an initial pair `(a,u)`, write

\[
 s(a+h)=\sum_{j\ge0}c_jh^j,\quad c_0=u,\quad
 w(h)=s(a+h)+\tfrac34(a+h)^2=\sum w_jh^j,
 \quad w(h)^{-1}=\sum q_jh^j.
\]

Then

\[
\begin{aligned}
 w_j&=c_j+\tfrac34[(a+h)^2]_j,\\
 q_0&=1/w_0,\qquad
 q_j=-q_0\sum_{k=1}^jw_kq_{j-k},\\
 c_{j+1}&=\frac1{2(j+1)}\sum_{k=0}^jq_kq_{j-k}.
\end{aligned}                                                   \tag{4}
\]

With point intervals for `(a,u)`, recurrence (4) encloses the Taylor
coefficients. With rectangular interval inputs, it encloses the corresponding
coefficients for **every** pair in that rectangle. Repeated dependency only
widens the interval; it cannot invalidate inclusion.

For a proposed step of length `h`, the exact inverse solution started at the
center `u` lies in the simple verified tube

\[
 a\le e\le a+h,\qquad u\le s(e)\le u+h f(a,u),                  \tag{5}
\]

because it is increasing while `f` decreases in both arguments. The upper
endpoint in (5) is computed outward. Evaluate (4) once at the point to order
`p`, and once on tube (5) to order `p+1`. Taylor's theorem gives

\[
 \Phi_{a,a+h}(u)\in
 \sum_{j=0}^p[c_j]h^j+[c_{p+1}]_{\rm tube}h^{p+1}.             \tag{6}
\]

Polynomial evaluation and all products in (6) also use outward intervals.
The remainder coefficient is `s^(p+1)/(p+1)!`, so no factorial is missing.
The field is smooth on (5); the usual scalar Taylor remainder applies.

If the previous certified interval has center `u` and radius `r`, enlarge the
interval (6) by `[-r,r]`. Inclusion follows from (2). The center is chosen on
the dyadic grid; at most one extra grid tick is charged if endpoint parity
requires it. Thus startup error, local remainder, arithmetic rounding, and
center rounding are added—not multiplied by an exponential.

The fine run uses `p=12`, `h=2^-7` while `e<2`, and thereafter
`h=2^floor(log2(e))*2^-7`, clipping the final step at `E=256`. The code chooses
the dyadic scale by exact integer comparisons, not by a floating logarithm.
It takes 1,142 steps. The radius ledger is the actual endpoint width, not an
asymptotic error estimate. Integration and rounding contribute less than
`1.781*10^-16` to final width.

## 4. Paid analytic tail to infinity

For any `E>0`, let `s_E=s(E)`. From nonnegativity,

\[
 0<s_*-s_E\le T_0(E):=\frac8{27E^3}.                        \tag{7}
\]

Using `s(e)<=2` gives the explicit baseline lower bound

\[
 s_*-s_E\ge \max\{0,T_0(E)-128/(135E^5)\}.                  \tag{8}
\]

No special functions need to be evaluated. The elementary inequalities,
valid for every `x>=0`, are

\[
 1-2x\le(1+x)^{-2}\le1-2x+3x^2.                          \tag{9}
\]

Multiplication by `(1+x)^2` proves them immediately with nonnegative remainder
polynomials `3x^2+2x^3` and `4x^3+3x^4`.

The finer certificate retains the computed information: if
`s_E in [L,H]`, then on the entire tail `L<=s(e)<=U:=H+T0(E)`.
Substitute `x=4s/(3e^2)` into (9), integrate powers of `e`, and use monotonicity
in `s` to get

\[
\begin{aligned}
 T_-&=T_0(E)-\frac{64U}{135E^5},\\
 T_+&=T_0(E)-\frac{64L}{135E^5}+\frac{128L^2}{189E^7},\\
 L+T_-&\le s_*\le H+T_+ .                                  \tag{10}
\end{aligned}
\]

The run checks `0<T_-<=T_+<=T0(E)` exactly. At `E=256`, the tail *width* is
less than `1.152*10^-17`; the tail itself is about `1.77*10^-8` and is **not
omitted**. Equations (7)–(10) explain the difference between a small tail and
a tightly known tail.

## 5. Conditional finite-N perturbation interfaces—not a claim they hold

If an absolutely continuous approximation satisfies

\[
 \widehat s'(e)=f(e,\widehat s(e))+r(e)
\]

and both solutions remain in the positive inverse domain, the same sign
argument as (2) gives the deterministic bound

\[
 |\widehat s(E)-s(E)|
 \le |\widehat s(a)-s(a)|+\int_a^E|r(v)|\,dv.                 \tag{11}
\]

For a finite-variation cumulative forcing, replace the last integral by its
total variation, including jump magnitudes. There is still no growing
Gronwall factor. A stochastic martingale estimate for the supremum of a
primitive is **not** automatically an estimate of its total variation, so
(11) alone must not be applied to a raw counting-process path. Also, the count
`E` has downward jumps: simply calling it an inverse coordinate does not
construct an admissible time change. A monotone hitting-level or corrected
process, with its residuals and stopping events actually proved, is required.

A complementary deterministic time-shift estimate is available if actual
nonnegative paths on a stopped interval obey the precise identities

\[
 l_N(s)=s+\tfrac34e_N(s)^2+\xi(s),\quad |\xi|\le d,
 \qquad e_N(s)=2\int_0^s l_N(u)^2du+\eta(s),\quad |\eta|\le\epsilon.
\]

Put `a=d+(3epsilon/2)^(1/3)` and `w=e_N-eta`. Then `w` is absolutely
continuous and nondecreasing. Comparison of `w+epsilon` to `e(s+a)` gives
`e_N(s)<=e(s+a)`, since `e(a)>=epsilon`. For the lower bound,

\[
 w'\ge2[(s-d)+\tfrac34(\max(w-\epsilon,0))^2]_+^2,
\]

hence `w(a)>=2(a-d)^3/3=epsilon`; comparing `w-epsilon` after time `a`
gives `e_N(s)>=e(s-a)`. Thus, while the upper comparison exists and before
all specified stops,

\[
 e((s-a)_+)\le e_N(s)\le e(s+a),\quad
 l((s-a)_+)\le l_N(s)\le l(s+a).                           \tag{12}
\]

For the `l` bounds use `a>=d`; no monotonicity of `e_N` is assumed. The exact
stochastic residual identities, their simultaneous probability budgets,
entrance matching, continuation, and macroscopic service are **external
obligations**. Neither (11) nor (12) proves them.

### General deterministic remaining-time function

For a current state `(l,e)` with `l>0,e>=0`, put `w0=l-3e^2/4` and solve

\[
 u'(v)=1/[2(u(v)+3v^2/4)^2],\qquad u(e)=w_0.
\]

The denominator starts at `l>0` and increases along `v>=e`.
Define `b(l,e)=u(infinity)-w0`; this is the remaining forward ODE blow-up time.
For positive time the same forward blow-up comparison ensures it is finite.
Differentiating with respect to initial value yields

\[
 J_\infty=\exp\{-\int_e^\infty(u(v)+3v^2/4)^{-3}dv\}\in[0,1],
\]

and ordinary initial-condition/initial-point differentiation gives

\[
 b_l=J_\infty-1\in[-1,0],\qquad
 b_e=\tfrac32e(1-J_\infty)-\frac{J_\infty}{2l^2}.
\]

These formulas satisfy

\[
 (1+3l^2e)b_l+2l^2b_e=-1.
\]

They are an explicit deterministic clock representation with a bounded
`l`-derivative, not a hidden value-function oracle. At `l=0`, these inverse
formulas are singular; use a proved forward startup and variational flow
instead of substituting zero. This scalar deliverable does **not** validate
all derivatives needed for a finite-jump generator corrector, nor does it
supply the stochastic residual estimates required to use one.

## 6. Costs, comparisons, and scope

The fine run uses 120-bit grid endpoints, degree-78 exact startup, order-12
Taylor coefficients, 1,142 inverse steps, and a rational analytic tail. The
recorded operation counts are 401,984 interval additions, 454,516 interval
multiplications, and 30,834 interval reciprocal calls (the solver counters exclude
the arithmetic self-test and exact-fraction startup operations). Endpoints stay at fixed precision; temporary products
use ordinary arbitrary-size integers. The startup uses exact fractions with
larger numerators/denominators, an explicitly paid finite cost. On this local
executor the fine run took roughly 1.55 seconds. That is not a complexity bound,
benchmark against other solvers, or hardware-speed claim.

This is entirely ordinary validated polynomial/rational ODE machinery plus
an advantageous inverse representation. Established validated Taylor methods
could perform the same deterministic calculation. No superiority over them,
novel numerical principle, generic sparse-network result, or efficient
finite-N stochastic algorithm is asserted.

What this adds to the current construction is a **reusable, numerically sharp,
fully charged scalar target** and a stable deterministic perturbation
interface. The potentially newly possible physical/computational capability
is boundary-aware prediction of actual macroscopic clearance time **after**
the actual-chain entrance, near-blow-up continuation, and service-time
interfaces are earned. Merely computing this scalar, simulating the ODE,
preparing a favorable state, or proving recurrence does not provide that
operation. The separate actual-chain proof must connect it to the observed
stopping time with explicit accuracy, probability, and preparation costs.
