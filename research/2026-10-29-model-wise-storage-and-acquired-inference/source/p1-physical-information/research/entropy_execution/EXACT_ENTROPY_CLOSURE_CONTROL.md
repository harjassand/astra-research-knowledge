# Exact rational control of the entropy-closure example

29 October 2026. Root owns the entropy-completion construction. This note supplies its deterministic implementation, exact arithmetic certificates, resource accounting, and an explicit weighted-L1 bound for the requested family.

## Result

The supplied analytic record is

\[
K_{12}(t)=e^{-t},\qquad K_{21}(t)=te^{-t}.
\]

Each port has unnormalized stationary weight one and conditional departure rate one. Each directed excursion has integrated unnormalized flux one, hidden mass is `V=3`, and total stationary weight is `W=5`. The observable unnormalized entropy is

\[
J=\int_0^\infty e^{-t}(1-t)(-\log t)\,dt=1.
\]

Actual stationary flux densities are `K_ij/5`; the corresponding intrinsic entropy rate has closure floor `1/5`. These normalization conventions matter.

All seven requested/optional controls, `lambda=2,4,8,16,32,64,128`, pass. At `lambda=128`, the construction has 1,986,690 hidden states, common phase rate approximately 127.6571865792, and

\[
0.976018403402799998<E<0.976018403402799999.
\]

The displayed decimal interval is rounded outward from a substantially narrower exact rational certificate. The stationary preparation divergence is approximately 0.2829883637; the expected microscopic jump count per native departure is approximately 192.4857798688. A rigorous bound for the sum of weighted-L1 kernel errors is less than 0.0369256608.

No draws, observed trajectories, equipment operations, or finite-data acquisition were used. The large state counts describe the realization; the verification never allocates a large state matrix. This example tests a variational completion theorem. Direct evaluation of the supplied source already gives `J=1`, so no sample or computational advantage is asserted.

## Finite family and exact constraints

Let `lambda` be a power of two, and put

\[
p=1/\lambda,\quad r=1-p,\quad
M=\lambda(\log_2\lambda+4),\quad N=M+1.
\]

For `1 <= n <= M`, set

\[
A_n=pr^{n-1},\qquad B_n=npA_n.
\]

The remaining component, assigned `N` phases, is

\[
A_N=r^M,\qquad B_N=r^M(1+Mp).
\]

Both coefficient sequences sum to one. Define

\[
m_0=\lambda^{-1}\sum_{n=1}^{N}n(A_n+B_n),\quad
d=3/m_0,\quad \lambda'=\lambda/d.
\]

The exact closed expression checked by the script is

\[
m_0=3-p-r^{M+1}(Mp+3),
\tag{1}
\]

so `d>1`. For each `n`, place an `n`-phase directed channel from port 1 to port 2 and its separate reverse partner. Entry rates are `A_n` and `B_n`; all hidden rates are `lambda'`. The unnormalized weight of each forward phase is `A_n/lambda'`, and similarly for `B_n`.

Every stationary flow balances exactly, each port escape rate is one, and

\[
\sum_n\frac{n(A_n+B_n)}{\lambda'}=3.
\]

Thus port weights, fluxes, native departure clocks, hidden mass, total weight, and mean native cycle duration `W/R=5/2` are preserved exactly.

Parity fixes the two ports and maps phase `k` of each channel to phase `n+1-k` of its partner. Every positive transition has its physical reversed partner. All paired escape rates agree. The native kernels are the finite mixtures

\[
K^{(\lambda)}_{12}(t)=\sum_n A_n g_{n,\lambda'}(t),\qquad
K^{(\lambda)}_{21}(t)=\sum_n B_n g_{n,\lambda'}(t),
\]

where `g_{n,lambda'}` is the Erlang density with `n` phases at rate `lambda'`.

The physical path ratio through a whole channel is exactly `A_n/B_n`, because the entry and exit factors telescope and the port weights agree. Hence

\[
E_\lambda=\sum_n(A_n-B_n)\log(A_n/B_n).
\tag{2}
\]

The ratios are rational and especially simple:

\[
A_n/B_n=\lambda/n\quad(n\le M),\qquad
A_N/B_N=\lambda/(\lambda+M).
\]

The stationary parity-preparation divergence, which must not be silently included in the rate, is

\[
D(\pi\Vert\pi^\Theta)
=\frac1{5\lambda'}\sum_n n(A_n-B_n)\log(A_n/B_n).
\tag{3}
\]

The finite-horizon stationary path KL is `D(pi || pi^Theta) + T E_lambda/5`.

## Why exact matching is different

For the target record, `K12(0)=1` and `K21(0)=0`. In a finite CTMC, positivity of `K12(0)` requires a two-edge itinerary `1 -> x -> 2`. Finite physical reversal divergence with parity fixing the ports would require `2 -> Theta(x) -> 1`, which would force `K21(0)>0`. Thus every exact finite completion in the stated class has infinite reversal divergence.

Every constructed approximant instead has

\[
K^{(\lambda)}_{12}(0)=1/d,\qquad
K^{(\lambda)}_{21}(0)=1/(\lambda d)>0.
\]

This removes the support obstruction at each finite stage. The exact short-time zero appears only in the limit. The infinity concerns path support in this ideal finite jump-model class; it does not establish infinite heat dissipation in a native physical source.

## An explicit full-record weighted-L1 certificate

Define

\[
\|f\|_{1,1}=\int_0^\infty(1+t)|f(t)|\,dt.
\]

Before truncating and dilating, the infinite coefficient families at phase rate `lambda` have exact laws

\[
\sum_{n\ge1}pr^{n-1}g_{n,\lambda}(t)=g_1(t),\qquad
\sum_{n\ge1}np^2r^{n-1}g_{n,\lambda}(t)
=(1-p)g_2(t)+pg_1(t),
\tag{4}
\]

where `g1=e^-t` and `g2=t e^-t`. This follows directly from their geometric Laplace sums.

The combined collapsed tail mass is

\[
\tau=r^M(2+Mp).
\]

Its new first moment is `(N/lambda) tau`; the lost first moment is

\[
\Delta=r^{M+1}(Mp+3).
\]

Replacing both original tails by their `N`-phase components therefore changes the two kernels by at most

\[
C=2\tau(1+N/\lambda)+\Delta
\tag{5}
\]

in the sum of weighted-L1 norms. This uses the sum of the old and new tail masses and first moments, so it does not assume disjoint densities or hidden access to individual paths.

Let `(D_v f)(t)=v^-1 f(t/v)`. For `v>=1`,

\[
\|D_v(f-g)\|_{1,1}\le v\|f-g\|_{1,1}.
\]

For a unit-rate gamma density of integer shape `k`, differentiation with respect to `v` gives

\[
\|\partial_v D_v g_k\|_{1,1}
=v^{-1}\mathbb E|k-X_k|+\mathbb E[X_k|k-X_k|].
\]

For shape one the right side is at most `8/e-1<2`; for shape two it is at most `44/e^2-2<4`. The strict elementary bounds follow from `e>8/3` and `e>65/24`, respectively. Direct integration also gives

\[
\|g_1-g_2\|_{1,1}=8/e-1<2.
\]

Using (4), dilating by `d`, and combining these inequalities yields the fully rational certificate

\[
\boxed{\quad
\|K^{(\lambda)}_{12}-g_1\|_{1,1}
+\|K^{(\lambda)}_{21}-g_2\|_{1,1}
\le dC+(6-2p)(d-1)+2p.
\quad}
\tag{6}
\]

Since `Mp=log2(lambda)+4`, the tail terms tend to zero, `p -> 0`, and (1) gives `d -> 1`. Thus (6) proves weighted-L1 convergence for this particular family, in addition to the exact preservation of the total mean. The finite set of Laplace checks is not used as a substitute for (6).

## Entropy and resource limits

For the uncollapsed terms in (2), put `x=n/lambda`. Then

\[
E_\lambda
=\frac1\lambda\sum_{n=1}^{M}r^{n-1}(x-1)\log x
+Mp\,r^M\log(1+Mp).
\tag{7}
\]

The sum is a Riemann approximation to

\[
\int_0^\infty e^{-x}(x-1)\log x\,dx
=\Gamma'(2)-\Gamma'(1)=1.
\]

The logarithmic singularity is controlled uniformly: below `a<1`, the nonnegative summand is bounded by the right Riemann sum for `-log x`, whose integral is `a(1-log a)`. For large `x`, `r^{n-1} <= exp(1/2) exp(-x)` gives an integrable exponential envelope for the remaining polynomial-logarithmic factor. The last term of (7) is at most `(Mp) exp(-Mp) log(1+Mp)`, which tends to zero. Hence `E_lambda -> 1`.

The same argument with an additional factor `x` in the sum proves

\[
D(\pi\Vert\pi^\Theta)
\longrightarrow\frac{\Gamma'(3)-\Gamma'(2)}5
=\frac{2-\gamma_{\rm Euler}}5.
\]

The preparation asymmetry remains finite and nonzero. It is distinct from the sustained entropy rate.

The realization has

\[
H=N(N+1)\quad\text{hidden states},\qquad
N(N+3)\quad\text{positive directed edges}.
\]

The expected microscopic jump count per native departure is

\[
L_{\rm micro}=\tfrac12\sum_n n(A_n+B_n)+1
=\tfrac12\lambda m_0+1.
\]

Consequently `lambda'/lambda -> 1`, `L_micro/lambda -> 3/2`, and
`H` grows as `lambda^2 (log2 lambda)^2`. These are execution resources of the explicit realization. They are not required by direct evaluation of the analytically supplied observable entropy.

## Arithmetic and verification

The executable uses only Python's standard library. Fractions store all coefficients, means, rates, masses, phase weights and transforms' inputs exactly.

For a positive rational logarithm, reduce `x=2^k y` with `1<=y<2` and use

\[
\log y=2\sum_{j=0}^{L-1}\frac{z^{2j+1}}{2j+1}+R_L,
\qquad z=(y-1)/(y+1),
\]

\[
0\le R_L\le\frac{2z^{2L+1}}{(2L+1)(1-z^2)}.
\]

The implementation retains 64 terms and rounds each integer quotient outward on a 160-bit dyadic grid. It checks each logarithm interval has width below `2^-128`, and each final entropy/preparation interval has width below `2^-120`. No floating-point result makes a certificate decision.

Laplace transforms are enclosed at rational `s=1/16,1/4,1/2,1,2,4,16`. The exact phase factor is `q=lambda'/(lambda'+s)`. Positive Horner evaluation with outward dyadic arithmetic certifies the polynomial transform without constructing its enormous literal denominator. For the two small cases, closed geometric formulas and exact native first-step recursions independently agree with these intervals.

For `lambda=2,4`, sparse generators with 134 and 652 total states are constructed. All stationary flow equations, holding rates, parity involution, reversed support, channel likelihood products and native cross/self-return transforms pass exact checks. Larger cases use the proved channel identities and matrix-free evaluation.

The largest reduced entry-coefficient denominator has 3,841 bits at `lambda=64` and 9,857 bits at `lambda=128`. The JSON separately reports numerator/denominator sizes for entries, hidden weights and normalized probabilities, plus a coefficient-manifest hash. These are exact storage requirements of the literal rational representation, not an information-acquisition count or a lower bound on necessary instrument precision. The integer recipe is compact; a finite-precision physical implementation would need its own error analysis.

## Files and reproduction

Run:

```text
python check_entropy_closure.py --include-128
```

Outputs are `ENTROPY_CLOSURE_CHECKS.json` and `ENTROPY_CLOSURE_TABLE.md`. The JSON retains exact interval endpoints, exact invariants, rational weighted-L1 bounds, resource counts, coefficient precision and the script hash. The companion root theorem is `../ENTROPY_COMPLETION_CONVERSE.md`.
