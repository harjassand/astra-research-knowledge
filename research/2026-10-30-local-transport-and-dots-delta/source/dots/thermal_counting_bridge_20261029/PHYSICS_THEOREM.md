# Volume-uniform imaginary-time product-formula control

**Status (2026-10-29): proved below; independently audited.** This is an elementary derivation, not a claim of literature novelty. It establishes the physical approximation obligation only. It does not establish any counting-algorithm or bit-complexity claim.

## Statement

Let `H = sum_a h_a` act on `n` finite-dimensional spins. Assume:

* every `h_a` is Hermitian and supported on at most `k >= 1` sites;
* `||h_a|| <= J`;
* each site occurs in at most `D` terms, with `k,D,J` independent of `n`.

Extract scalar/empty-support terms and handle their exponential exactly. Then the number `m` of remaining terms is at most `nD`. Local spin dimensions may be arbitrary for the operator statement, but a fixed bound `d` is used for the ground-energy consequence.

Color the term-overlap graph using `q <= k(D-1)+1` colors. Each layer `H_j` is a sum of terms with pairwise disjoint supports. Put

\[
E_j(t)=e^{-tH_j/2},\quad Q(t)=E_q(t)\cdots E_1(t),\quad P(t)=Q(t)^\dagger Q(t),
\]

and

\[
M=\sum_{\ell=1}^{q}k^\ell,\qquad x=JM\delta.
\]

Thus `P` is a positive, symmetric, local-factor product; explicitly it has the palindromic sequence `E_1 ... E_q E_q ... E_1` and is a second-order formula. For every finite `n` and every `delta >= 0`,

\[
\boxed{\|\log P(\delta)+\delta H\|
\le {2m\over M}\,[\sinh(JM\delta)-JM\delta].} \tag{1}
\]

Consequently, for every `beta > 0` and positive integer `r`,

\[
\boxed{
{1\over n}\left|\log\operatorname{Tr}e^{-\beta H}
-\log\operatorname{Tr}P(\beta/r)^r\right|
\le {2Dr\over M}\,[\sinh(x)-x]
\le {D J^3 M^2 e^x\over3}\,{\beta^3\over r^2},
\quad x={JM\beta\over r}.} \tag{2}
\]

There is no restriction on the interaction graph other than the incidence bound: expanders are allowed. No positivity of individual matrix entries, stoquasticity, geometric block cutting, clustering, gap, high-temperature restriction on `beta`, or thermodynamic limit is used.

For target normalized log-partition error `eta`, it suffices to choose

\[
r\ge\max\left\{JM\beta,\sqrt{\frac{eD J^3M^2\beta^3}{3\eta}}\right\}.
\]

The rounding to an integer is understood. For fixed parameters this is constant in volume.

### Sufficient first-order fallback

The even-coefficient refinement is not needed for the bridge. Bounding the full conjugation difference by `J(exp(JMt)-1)` instead gives directly

\[
\|\log P(\delta)+\delta H\|
\le {2m\over M}(e^{JM\delta}-1-JM\delta),
\]

and normalized log-partition error at most

\[
{2Dr\over M}(e^x-1-x)
\le D J^2M e^x\frac{\beta^2}{r}.
\]

Thus even the simpler first-order argument already supplies a constant-in-volume step count.

## Proof

### 1. Finite active cones under disjoint-layer conjugation

Take a local operator `a` supported on at most `k` sites. Conjugation by one disjoint layer only involves gates whose supports intersect the current support. At most the current support size many gates are active. Their union with the current support has size at most `k` times that support size.

Therefore conjugation by any ordered subsequence of at most `q` layers can be written, on this particular operator, as a product of at most `M = k + ... + k^q` active local conjugations. The active cone depends only on supports, not on `t`, and works identically for `t` and `-t`.

Each such conjugation is the superoperator

\[
e^{-t\,\operatorname{ad}_{h_b}/2},\qquad
\|\operatorname{ad}_{h_b}/2\|_{\mathrm{op}\to\mathrm{op}}\le J.
\]

Let `U(t)` be any such ordered layer product, and let `F(t)=U(t)aU(t)^{-1}`. Expanding this *finite product* of entire superoperator exponentials gives, coefficient by coefficient,

\[
\|[t^p]F(t)\|\le\|a\|\frac{(JM)^p}{p!}. \tag{3}
\]

This is an absolutely convergent series bound, not a truncated BCH argument. It follows by summing the multinomial coefficients for the finite product of exponential series.

When `a` is Hermitian, each layer factor is Hermitian for real `t`, so

\[
U(-t)=U(t)^{-\dagger},\qquad F(t)^\dagger=F(-t).
\]

Hence the Hermitian part of `F` consists only of its even Taylor coefficients. Since `F(0)=a`, (3) implies

\[
\|\operatorname{Herm}F(t)-a\|
\le\|a\|[\cosh(JMt)-1]. \tag{4}
\]

### 2. A relative evolution with no full-Hamiltonian imaginary conjugation

Set

\[
R(t)=Q(t)e^{tH/2},\qquad G(t)=R'(t)R(t)^{-1}.
\]

Product differentiation gives

\[
G(t)=Q'(t)Q(t)^{-1}+\tfrac12Q(t)HQ(t)^{-1}
=\tfrac12\sum_{j=1}^q\left[
\operatorname{Ad}_{Q(t)}H_j-
\operatorname{Ad}_{U_{>j}(t)}H_j\right], \tag{5}
\]

where `U_{>j}=E_q ... E_{j+1}` (empty product is the identity).

The crucial point is that (5) contains only finite-depth layer conjugations. It contains no `e^{tH} a e^{-tH}`. Thus extensive operator norms do not appear inside an exponential bound.

Expand every `H_j` into its local terms, subtract and add each original `h_a`, and use (4). Since there are `m` terms and the prefactor is `1/2`,

\[
\|\operatorname{Herm}G(t)\|
\le mJ[\cosh(JMt)-1]=:g(t). \tag{6}
\]

### 3. Singular-value comparison, then the operator logarithm

For every vector `v`, `R'=GR` implies

\[
\frac{d}{dt}\|R(t)v\|^2
=2\langle R(t)v,\operatorname{Herm}G(t)R(t)v\rangle.
\]

By the scalar differential inequalities from (6), with `R(0)=I`,

\[
e^{-2a(\delta)}I\preceq R(\delta)^\dagger R(\delta)
\preceq e^{2a(\delta)}I,
\quad
a(\delta)=\int_0^\delta g(t)dt
={m\over M}[\sinh(JM\delta)-JM\delta]. \tag{7}
\]

Since `R^dagger R = e^{delta H/2} P(delta) e^{delta H/2}`, congruence gives

\[
e^{-2a(\delta)}e^{-\delta H}
\preceq P(\delta)
\preceq e^{2a(\delta)}e^{-\delta H}. \tag{8}
\]

The matrix logarithm is operator monotone on positive definite matrices. Applying it to (8) yields

\[
-\delta H-2a(\delta)I
\preceq\log P(\delta)
\preceq-\delta H+2a(\delta)I,
\]

which is (1).

**Important:** powers of (8) are not taken in Loewner order; that would be invalid. The logarithm is taken first.

### 4. From the effective generator to the partition function

For Hermitian `A,B`,

\[
|\log\operatorname{Tr}e^A-\log\operatorname{Tr}e^B|\le\|A-B\|.
\]

For completeness, interpolate `B+s(A-B)`; the derivative of its log-trace-exponential is the expectation of `A-B` in a positive normalized Gibbs state, so its absolute value is at most `||A-B||`.

Apply this with `A=r log P(beta/r)` and `B=-beta H`. Equation (1) and `m<=nD` give the first inequality in (2). For `x>=0`, Taylor's integral remainder gives `sinh(x)-x <= x^3 e^x/6`, proving the second.

## Free energy and ground-energy density

Let `f_beta=-(beta n)^{-1} log Tr e^{-beta H}` and let `e_0=E_0(H)/n`. If each local spin dimension is at most `d`,

\[
e_0-\frac{\log d}{\beta}\le f_\beta\le e_0.
\]

The product formula estimates `f_beta` with error at most the right side of (2) divided by `beta`. Thus taking `beta >= 2 log(d)/epsilon` and choosing `r` to make that free-energy-density error at most `epsilon/2` gives an `epsilon`-additive ground-energy-density estimate, provided the approximate product partition function can itself be evaluated to sufficient log-density accuracy.

No claim is made here that arbitrary signed local tensor weights can already be compiled into fixed-width exact #SAT with acceptable precision/size. That is a separate obligation.

## Why low-temperature ordering does not obstruct this bound

The argument compares the logarithm of a *single positive step* to `-delta H`, then takes powers in the logarithm. It never transports local errors for imaginary time `beta`, and never requires locality of the exact effective Hamiltonian `-(1/delta) log P`. Low-temperature Gibbs correlations and expander geometry therefore do not enter. Constants can be very large in `k,D`, but are independent of `n`.
