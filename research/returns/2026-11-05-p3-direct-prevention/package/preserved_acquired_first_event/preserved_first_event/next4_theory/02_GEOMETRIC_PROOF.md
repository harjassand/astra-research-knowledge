# An executed finite-bit compiler for an enormous geometric clock

## Completed operation and scope

The module at **next4_execution/finite_geometric.py** takes exact rational
\(0<r\le1\) and \(0<\varepsilon<1\), and returns an integer whose law is within
\(\varepsilon\) in total variation of
\[
 \Pr(K=k)=r(1-r)^k,\qquad k=0,1,\ldots.
\]
The value \(r^{-1}\) does not control a loop, a table size, or the length of an
exact rational numerator. The compiler stores only logarithmically many
fixed-point powers. One draw uses a finite, prescribed number of fair bits and
a bounded binary search.

The guarantee assumes independent unbiased bits. The executed checks use
seeded Python PRNGs and label their empirical statistics as diagnostics.
The mathematical guarantee comes from the exact error analysis below, not
from the apparent quality of those statistics.

The module contains no floating-point arithmetic. Its input validation rejects
floating probabilities rather than silently interpreting their rounded values.
The special case \(r=1\) returns zero exactly and consumes no random bits.

This operation closes the calendar-clock implementation in the first-event
construction. It does not replace the separate proof that the first-event law
is approximated by an independent geometric index and a conditional success
block, or the calibration proof for the estimated parameter \(r=\widehat q\).

## API

Compile once when making several draws:

    from fractions import Fraction
    import random
    from finite_geometric import GeometricClockCompiler

    clock = GeometricClockCompiler(Fraction(1, 2**100), Fraction(1, 2**20))
    rng = random.Random(20261105)  # reproducible execution diagnostic
    K, metadata = clock.sample(rng)
    further_indices = [clock.draw(rng) for _ in range(1000)]

The required convenience function is:

    sample_geometric(
        r: Fraction, epsilon: Fraction, rng: random.Random
    ) -> tuple[int, dict]

The convenience function recompiles on each invocation. Reusing the class
retains its power table. The class also exposes an exact rational error
certificate, a JSON-safe copy through its certificate method, and deterministic
auditing methods. Returned metadata includes worst-case and actual counts.
Large integers in metadata are strings; numbers above 4096 bits use
hexadecimal strings to avoid Python's decimal-conversion digit limit.

For the root theorem's existing notation, pass
\[
 \varepsilon_{\mathrm{clock}}=\varepsilon_{\mathrm{root}}/128.
\]
The implemented cap then equals the cap already displayed in
next4_root/finite_compiler.tex. The module's entire error is at most
\(\varepsilon_{\mathrm{root}}/128\), which fits inside that report's
\(\varepsilon_{\mathrm{root}}/64\) clock allocation.

## Parameters, all computed exactly

Assume \(0<r<1\). Define
\[
\begin{aligned}
 t&=\left\lceil\log_2(1/\varepsilon)\right\rceil,\\
 M&=\left\lceil t/r\right\rceil,\\
 D&=\operatorname{bitlength}(M)
   =\left\lceil\log_2(M+1)\right\rceil,\\
 B&=\left\lceil\log_2(8M/\varepsilon)\right\rceil,\\
 A&=\left\lceil\log_2(16M^2/\varepsilon)\right\rceil,\qquad S=2^A.
\end{aligned}
\]
Here \(t\ge1\), \(M\ge1\), and \(A\ge B\). The code obtains all ceilings of
binary logarithms by integer bit lengths followed by an exact comparison.
It never calls a floating logarithm.

The output belongs to \(\{0,\ldots,M\}\). The cap is exactly the requested
\(\lceil\lceil\log_2(1/\varepsilon)\rceil/r\rceil\), with no additional
inverse-rarity factor.

The compiler reports the following rational error bounds:
\[
\begin{aligned}
 \beta_{\mathrm{tail}}&=\frac{3}{4\,2^t},\\
 \beta_{\mathrm{grid}}&=\frac{M}{2^B},\\
 \beta_{\mathrm{pow}}&=\frac{M(M+1)}{2^A},\\
 \beta_{\mathrm{total}}&=
 \beta_{\mathrm{tail}}+\beta_{\mathrm{grid}}+\beta_{\mathrm{pow}}
 \le\varepsilon.
\end{aligned}
\]
The last comparison is checked with exact Fraction arithmetic during
compilation, in addition to its proof below.

## Construction

Write \(q=1-r\). First compile integer approximations to the successive
survival powers:
\[
 P_0=\lfloor S q\rfloor,\qquad
 P_{j+1}=\left\lfloor P_j^2/S\right\rfloor,
 \quad 0\le j<D-1.
\]
All \(P_j\) lie in \([0,S]\). Their list has length \(D\).

For an exponent \(1\le n\le M\), read its binary digits. Start an accumulator
at \(S\). For every nonzero digit \(j\), replace the accumulator by
\[
 V\leftarrow\lfloor V P_j/S\rfloor.
\]
Call the final integer \(V_n\). Division by \(S\) is an integer right shift.
The code does not calculate \(q^n\) as an exact rational.

For a draw, request exactly \(B\) fresh fair bits, giving a uniform integer
\(J\in\{0,\ldots,2^B-1\}\). Binary search the candidate index interval
\([0,M]\). At midpoint \(k<M\), take the left interval when
\[
 \frac{J}{2^B}<1-\frac{V_{k+1}}S,
\]
and the right interval otherwise. The code compares the integers
\[
 J\,2^{A-B}\quad\hbox{and}\quad S-V_{k+1}.
\]
Thus all comparisons are exact, including their strict/non-strict convention.
The terminal index is returned. The endpoint \(M\) implicitly collects the
tail; no survival probability at a larger exponent is required.

There is no claim that every rounded threshold is automatically monotone.
The coupling proof below does not require that additional property.

## Proof of the total-variation guarantee

### 1. Capping costs at most the reported tail bound

Let \(K\) have the target geometric law and \(K^c=\min(K,M)\). Coupling these
variables directly gives
\[
 d_{\mathrm{TV}}(\mathcal L(K),\mathcal L(K^c))
 =\Pr(K>M)=q^{M+1}.
\]
Because \(\log(1-r)\le-r\), \(rM\ge t\), and
\(e>1+1+\tfrac12+\tfrac16=\tfrac83\),
\[
\begin{aligned}
 q^{M+1}
 &\le e^{-t}
 <(3/8)^t\\
 &=(3/4)^t\,2^{-t}
 \le \frac34\,2^{-t}
 =\beta_{\mathrm{tail}}
 \le \frac34\varepsilon .
\end{aligned}
\]
Only \(t\), whose value is proportional to the input precision, appears in
this bound. The implementation does not evaluate the exponential or the
target power to certify it.

### 2. Every compiled power has a one-sided error bound

Put \(p_j=P_j/S\). Downward rounding and induction give
\[
 0\le q^{2^j}-p_j\le (2^{j+1}-1)/S.
\]
For \(j=0\), this follows directly from the floor. If it holds at \(j\), then
\[
 q^{2^{j+1}}-p_j^2
 =(q^{2^j}-p_j)(q^{2^j}+p_j)
 \le 2(q^{2^j}-p_j).
\]
The new floor loses less than \(1/S\), proving the induction.

For numbers in \([0,1]\), the error of a product is at most the sum of the
factor errors. Each additional rounded multiplication adds at most \(1/S\).
If \(n=\sum_{j\in I}2^j\), the multiplication procedure therefore satisfies
\[
\begin{aligned}
 0\le q^n-\frac{V_n}{S}
 &\le\sum_{j\in I}\frac{2^{j+1}-1}{S}
       +\frac{|I|}{S}\\
 &=\frac{2n}{S}.
\end{aligned}
\]
This intentionally allows a rounding error on the first multiplication,
although multiplying the initial integer \(S\) by \(P_j\) and shifting is
exact. The resulting bound is conservative.

Consequently, for \(0\le k<M\), the computed threshold
\(\widehat F(k)=1-V_{k+1}/S\) obeys
\[
 F(k)\le\widehat F(k)\le F(k)+2(k+1)/S,
 \qquad F(k)=1-q^{k+1}.
\]

### 3. A coupling controls the whole discrete law

Take a continuous \(U\sim\operatorname{Unif}[0,1)\) and set
\[
 J=\lfloor 2^B U\rfloor,\qquad U_B=J/2^B.
\]
Then \(J\) has exactly the implementation's fair-bit distribution, and
\[
 U_B\le U<U_B+2^{-B}.
\]
Exact binary search using \(U\) and the true thresholds \(F(k)\) returns
\(K^c\). At any threshold, an ideal left decision implies a finite left
decision, since
\[
 U<F(k)\ \Longrightarrow\
 U_B\le U<F(k)\le\widehat F(k).
\]
If the two decisions differ, the finite algorithm went left while the exact
one went right. This requires
\[
 F(k)\le U<
 F(k)+2(k+1)/S+2^{-B}.
\]
The probability of this event is at most the length of the displayed
interval.

Apply a union bound over all \(M\) possible thresholds, whether or not a
particular run queries them. If none of these events occurs, every queried
comparison agrees, the search paths agree, and the output indices agree.
Thus the finite output \(\widehat K\) satisfies
\[
\begin{aligned}
 d_{\mathrm{TV}}(\mathcal L(\widehat K),\mathcal L(K^c))
 &\le
 \sum_{k=0}^{M-1}\left(2^{-B}+\frac{2(k+1)}S\right)\\
 &=\frac{M}{2^B}+\frac{M(M+1)}S\\
 &=\beta_{\mathrm{grid}}+\beta_{\mathrm{pow}}.
\end{aligned}
\]
This argument remains valid if rounded thresholds violate monotonicity.
Only the true thresholds are used to identify the ideal inverse transform.
The proof charges all possible ambiguous thresholds while the algorithm
actually evaluates only logarithmically many.

### 4. The allocated budgets sum to at most the requested tolerance

The choices of \(A\) and \(B\) imply
\[
 \beta_{\mathrm{grid}}\le\varepsilon/8,\qquad
 \beta_{\mathrm{pow}}\le
 \frac{2M^2}{2^A}\le\varepsilon/8.
\]
Together with the tail estimate and the triangle inequality,
\[
 \boxed{
 d_{\mathrm{TV}}(\mathcal L(\widehat K),\operatorname{Geom}_0(r))
 \le\beta_{\mathrm{total}}\le\varepsilon.}
\]
The conclusion is total variation of the entire integer law. It is not
merely agreement of a few moments, an asymptotic approximation, or a
Kolmogorov/CDF-distance guarantee.

## Worst-case operations and bit cost

The construction provides the following deterministic limits.

| Quantity | Limit |
|---|---:|
| Stored fixed-point powers | \(D\) |
| Setup squarings | \(D-1\) |
| Fresh random bits per draw | Exactly \(B\) |
| Binary-search CDF queries per draw | \(D\) |
| Exponent-bit inspections per draw | \(D^2\) |
| Fixed-point multiplications per draw | \(D^2\) |
| Fixed-point operand size | At most \(A+1\) bits |
| Product size | At most \(2A+2\) bits |
| Power-table payload | At most \(D(A+1)\) bits |
| Returned index | At most \(D\) bits for \(M\ge1\) |

A binary search starts with \(M+1\) candidates. Every comparison leaves at
most the ceiling of half the previous number, so it terminates within
\(\lceil\log_2(M+1)\rceil=D\) comparisons. Each exponent contains at most
\(D\) bits and at most \(D\) nonzero bits, proving the per-draw counts.
The metadata reports both bounds and actual counts.

For a bit-cost statement, let \(b\) bound the bit lengths of the numerator
and denominator of \(r\), and let \(e\) do the same for \(\varepsilon\).
Then
\[
 t\le e,\quad
 D=O(b+\log(e+1)),\quad
 B=O(D+e),\quad A=O(D+e).
\]
Every setup intermediate also has polynomial bit length: the largest base
conversion numerator has \(O(A+b)\) bits, while the precision-selection
integers have \(O(D+e)\) bits. Rational certificate reductions are ordinary
integer greatest-common-divisor operations on numbers of these sizes.

Writing \(\mathsf M(A)\) for integer-multiplication cost, the draw uses
\(O(D^2\mathsf M(A))\) bit work, including shifts and comparisons, with
\(O(DA+b+e)\) stored bits apart from language-object overhead. The elementary
schoolbook bound gives \(O(D^2A^2)\) bit operations. Compilation uses
\(O(D\mathsf M(A))\) for its power table, plus polynomial-cost exact divisions,
parameter selection, and certificate arithmetic. These bounds are polynomial
in the input bit lengths; \(M\) can be exponentially larger.

The convenience function includes compilation on every call. Reusing a class
instance is the intended interface for a batch of 1000 event records.

## Why calendar-time encoding does not amplify the clock error

Fix the calibrated rational parameter \(r\), and let \(Z\) be an independent
conditional success block. Replacing \(K\) by \(\widehat K\) changes the joint
law of \((K,Z)\) by at most the clock's TV error. Applying any deterministic
record map cannot increase TV.

In the root construction, that map includes
\[
 (K,Z)\longmapsto 2b+K(L+b)+s(Z)
\]
and the mark/recent-history record. The integer multiplication and addition
are exact. At a fixed dyadic timestamp resolution they require only the
integer's bit length, so the enormous value of \(K\) introduces neither a
numerical time error nor an inverse-rarity simulation loop.

Parameter-estimation error, conditional-block error, and finite-block
timestamp error remain separate entries in the root theorem's ledger.
The clock compiler does not hide them in its own certificate.

## Executed checks

Run:

    python next4_theory/02_GEOMETRIC_CHECKS.py

The completed evidence is **next4_theory/02_GEOMETRIC_CHECKS.json**.
All checks passed using Python 3.12. No third-party package is required.

### Exact finite-distribution audits

Ten cases include \(r=1\), \(1/2\), \(1/3\), \(2/7\), \(1/10\), \(1/100\),
\(19/20\), \(1/64\), \(3/17\), and \(1/257\), with different rational
tolerances, including tolerances near one.

For each small case, an independent decision-tree interval count computes the
exact number of finite-bit strings returning every possible output.
It compares that exact distribution against the exact geometric probabilities
and accounts for the infinite target tail analytically. All full-law TV
distances and capped-law numerical TV distances satisfy the reported rational
certificates. Every survival exponent up to the audit cap is also checked
against its exact one-sided error bound.

Selected cases additionally enumerate every finite-bit input and confirm the
decision-tree counts. Each nonempty decision-tree leaf is checked at both
integer endpoints. There are also 1600 exact tests of the integer binary-log
ceiling, six rejected invalid inputs, and a seeded equality check between the
cached and convenience interfaces.

The small reference audit deliberately performs work proportional to its
small cap and constructs exact powers there. Those operations exist only in
the independent verifier, never in the production sampler.

### Enormous-index execution

All rows below use \(\varepsilon=2^{-20}\). Times are observed execution
measurements in this workspace, not worst-case runtime guarantees.

| Success probability | Draws | Uniform bits/draw | Fixed-point precision | Maximum CDF queries | Observed batch seconds |
|---|---:|---:|---:|---:|---:|
| \(2^{-100}\) | 1000 | 128 | 233 bits | 105 | 1.0025 |
| \(10^{-25}\) | 1000 | 111 | 199 bits | 88 | 0.8478 |
| \(2^{-1000}\) | 2 | 1028 | 2033 bits | 1005 | 2.1551 |

For \(r=2^{-100}\), the cap is
\[
 M=25\,353\,012\,004\,564\,588\,029\,934\,064\,107\,520.
\]
The observed maximum multiplication count in one draw was 3738, below the
proved bound \(105^2=11025\). The minimum and maximum sampled indices were
approximately \(1.26\times10^{27}\) and \(7.62\times10^{30}\).
Compilation took about \(6.1\times10^{-5}\) seconds.

For \(r=10^{-25}\), the cap is \(2\times10^{26}\); the observed maximum
multiplication count was 4174, below \(88^2=7744\).

The 1000-draw empirical CDF discrepancies were about 0.0397 and 0.0225.
They are ordinary seeded-PRNG diagnostics with sampling noise. They do not
estimate, certify, or replace the approximately \(10^{-6}\) analytic TV
guarantee. Two draws at \(r=2^{-1000}\) are solely a bit-complexity stress
execution and provide no meaningful distribution validation.

## Review of next4_root/finite_compiler.tex

No material error was found in the existing huge-geometric-index subsection.
Its looser mesh and power-error choices suffice under the stated
union-over-boundaries coupling. Its capped tail is correctly bounded with a
binary-log ceiling; using natural exponential decay only makes that bound
smaller.

The following implementation details are now made explicit:

1. Base rounding is included in the fixed-point induction.
2. All rounded powers stay in \([0,1]\), and downward rounding provides a
   one-sided threshold error.
3. Possible loss of monotonicity after rounding does not invalidate the
   binary-search coupling.
4. The finite uniform draw is a left endpoint, and strict integer comparisons
   implement its convention exactly.
5. The cap, number of CDF comparisons, multiplier operand sizes, and consumed
   bits are all prescribed before sampling.
6. The finite sampler targets the exact supplied rational \(r\). Estimation
   of the physical parameter remains the separate calibration step.

The other finite-compiler subsections were also checked for consistency with
this clock interface. The displayed mean-bias/concentration constants,
acceptance cap, timestamp union bound, and final error-ledger sum do not
require a change for this implementation. In the marked Poisson branch,
an event-count cap \(n\le k_U\) should be implemented by truncating its
unmarked count to \(M\le k_U-1\); this is the intended meaning of the existing
extra-one allowance, not a new error term.

The ready-to-insert LaTeX proof is
**next4_theory/02_GEOMETRIC_INSERT.tex**. The root report and the earlier
fixed-law package have not been modified.
