# Exact finite receiving and paid arithmetic

Status: author construction, independently unreviewed. This file accompanies the
full mathematical proof; execution does not promote an asymptotic expression to a
finite bound. The final requested TOTAL interval width is checked rationally.

## Scalar quadrature

The four integrands are l^-m, u^-m, l^m, and
[u0^(2p)/(2u0^p-u^p)]^(m/p). All are monotone on their stated intervals from the
main proof. Both masses use[1/2,1] and geometric pieces[1,2],[2,4],... toT. Both
resistances use[0,1/2] and double by evenness. Endpoint Darboux lower/upper sums
are exact rational bounds. Analytic full-infinite-tail upper bounds are added
only to the corresponding mass uppers. Before addition, each analytic tail upper
is rounded UP to scale2^P. This sound extra rounding is charged by the numerical
product test and avoids irrelevant huge rational tail denominators in output.
For T=2^J, the final four-type grid has
(2J+4)N+4 points. Separate integrand cache keys count as separate evaluations;
shared scalar profiles do not pretend those powers were free. The actual cache
cap also includes seed/intermediate-refinement points.

A lower seed from u^-m on[1,5/4] must be positive before any cutoff loop. Fixed
precision, positive typed cutoff/grid/evaluation limits and the finite Bernstein
budgets guarantee termination with a result or UNKNOWN. Refinement requires the
product of all four upper/lower integral ratios to be<=1+quad_relative. Then the
full endpoints are exactly

    low=1/(beta * MA(l)_upper * Rplus(u)_upper),
    high=1/(beta * MA(u)_lower * R0(l)_lower).

The externally requested TOTAL high/low is checked separately. A missed target
is UNKNOWN; intrinsic profile uncertainty or Jensen slack cannot be erased by
refining forever. This is a sufficient consumer, not arbitrary-accuracy solving.

## Outward dyadic repeated powers

All fractional scalar inputs and low-degree profile arithmetic are exact.
Let S=2^P. For positive rational x, form floor(xS) and ceil(xS) using integer
division. Positive interval multiplication [a,b]/S *[c,d]/S is enclosed by
[floor(ac/S),ceil(bd/S)]/S. Binary repeated squaring therefore encloses x^n at
every step by induction, using O(log n) directed multiplications. Negative
exponents first replace x by its exact reciprocal. Exponent0 returns[1,1].
The final implementation implements division/remainder byS as bit shifts/masks;
this is an exact integer identity, not floating-point rounding.

Reduce n/d by gcd before selecting a root, d in{1,2,4}. For d>1, an intermediate
interval[a,b]/2^P encloses the integer power. Its d-th root is enclosed at scale2^P
by floor_root(a*2^((d-1)P)) below and ceil_root(b*2^((d-1)P)) above. Integer square
root, or two nested integer square roots, supplies those endpoints. Exact-power
comparison decides whether the upper root needs+1. This is NOT necessarily a
one-ulp final interval: all directed multiplication error is retained and later
charged by the actual integral-width test.

Products, shifted numerators, denominators and root operands are checked against
max_power_bits before the guarded large operations. Low-degree rational profile
arithmetic, normalization, final reciprocals and serialization still have their
ordinary paid finite costs. The output max_guarded_integer_bits is the largest
tracked guarded-operand/result proxy, not every intermediate in the whole program
or process peak memory. Bernstein coefficients have their separately documented
stored-coefficient bound; it is not a claim that every transient Fraction numerator
in a subdivision addition was guarded beforehand. Fixed multiplication counts and
scalar evaluation counts are diagnostics, not proof-bearing certificate fields.

## Raw input and positivity work

Every exact numerator monomial and exponent is read. The coefficient-program
finder checks its complete schema, atom shapes, axis, denominator, anchor and
nominal proposal, then EVERY profile inequality on[0,infinity). Supplied delta
is an external proposed defect budget; it is not treated as measured truth or a
minimal defect oracle. The producer must actually certify both inequalities.
The verifier recomputes against the original external task, not certificate-
selected budgets. Different atom scales are divided out only after their complete
raw coefficients are read and positive anchor coefficients have been acquired.

Let R be raw monomials, n physical dimension, B coefficient bit size and D<=24
profile degree. Raw reading/hashing costs O(Rn), with sorting O(Rlog R) keys of
length n. Each UNIQUE normalized profile requires at most the global budgeted
number of O(D^2) rational de Casteljau operations; cache reuse cannot bypass any
raw term or changed input hash. The worst permitted node count is explicit and
may produce UNKNOWN even on a nonnegative polynomial. No unrestricted positivity
or factorization complexity is hidden behind a subroutine name.

Numerical work is O(number of admitted scalar evaluations * log m) directed
fixed-point multiplications, plus exact low-degree profiles, roots, Darboux
summation and tails. The tracked operand lengths are O(P+m log u0) on the slab,
and also reflect the finite cutoff and input coefficient lengths. This is a paid
polynomial ledger in actual budgets, NOT a general polynomial guarantee in desired
physical accuracy or arbitrary input coefficients. A poorly resolved seed or
unfavorable conditioning may be UNKNOWN. Reading the full raw program remains
necessary here; empirical unknown-model acquisition is not supplied.

## Preserved preliminary work

`pre_fixedpoint_attempt/` preserves the original exact Fraction-power source and
its first3 completed cases. Its513D attempt was interrupted, exit130, before a
certificate. `pre_shift_attempt/` preserves the first dyadic implementation and
its unit checks/first3 cases; that large attempt was likewise explicitly stopped
before a certificate. The final version uses the exact shift/mask implementation.
The initial1/2000 numerical product request was changed to1/1000, while the TOTAL
requested ratio remains1.01. No incomplete attempt is counted as a successful
full prediction or a proved budget rejection. No accepted predecessor changed.

`pre_tail_rounding_attempt/` additionally preserves the four completed cases before
a well-sensitive513D result returned UNKNOWN at Python exact-string serialization.
That denominator-growth refusal was sound; the final upward dyadic tail rounding
removes this avoidable output obstacle without changing the mathematical tail.
All five final cases and their receiving tests are regenerated after that change.
