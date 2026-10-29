# Genus-one rounded relative arithmetic: executable phase receipt

**2026-10-29. Experimental evidence, not certified end-to-end arithmetic.**

## Result first

On `y²=(x²−4)(x²−1)`, physical oval `[-1,1]`, origin `D0=(0,2)`,
28 executed calls produced **22 admitted numerical results and six correctly rejected
low-precision results**. All seven cases at 160 matrix-rounding bits with perturbation
scale `2^-24` passed disjoint-zero matching and physical-oval checks, including inputs
within `2^-100` of the conjugate origin. Twelve successive admitted calls satisfied
the independently evaluated direct-Abel error budget `e_next <= 2e+delta` numerically.
This is positive evidence for the actual rounded-kernel mechanism, not a uniform proof.

Crucially, the six rejected calls could have excellent final Abel errors. Matching
is load-bearing: a plausible final divisor is not sufficient evidence that the
prescribed zero-removal step was valid. The saved general prototype returns
`CHECKED_NOT_CERTIFIED` even for failed matching; this adapter explicitly overwrites
those outcomes with `ADMISSION_FAILED`. No claim is made that this metadata issue
invalidates the existing genus-two chain, which independently checked admission.

## Artifacts and reuse

- `genus_one_relative_doubling.py/.json/.log`: 28 trials, four exact section regressions,
  independent specialized Abel quadrature and scalar DOP853 ODE comparison.
- `genus_one_doubling_chain.py/.json/.log`: twelve calls and independently computed
  exact-power phase target; cumulative error budget.
- Reuses `rounded_relative_doubling.py` rational rounded matrix/nullspace and rational
  polynomial root isolation, separation, matching and projection. Does **not** alter it.
- Adapter replaces numerical comparison of two square-root sheets by the coprime
  quotient `y=-Ar/Br`. Common factors contribute both sheets, with ramification
  multiplicity; infinity orders are computed separately. Zero occurrences, not only
  unique roots, are retained.
- Separate `relative_interface_20261029/INDEPENDENT_INTERFACE_AUDIT.md` addresses the
  deterministic perturbation and precision interfaces. Its four numerical cases
  are complementary, not substituted for the phase comparisons here.

Reproduce from this directory with `python genus_one_relative_doubling.py` and
`python genus_one_doubling_chain.py`. The first completed in approximately 17 seconds
on this run. This is not a benchmark or complexity claim.

## Exact origin and multiplicity checks

Signed physical coordinates are `x=cos(theta)`,
`y=sin(theta)*sqrt(4-cos(theta)^2)`, hence `D0` has `theta=pi/2`.

For `D=D0`, the exact section is `f=x²`, whose norm is `x⁴`. Its section zero divisor
is `2D0+2iota(D0)`. Removing `2D0+iota(D0)` leaves `iota(D0)`; the required final
involution returns **exactly `(0,2)`**. Treating norm multiplicity four as four zeros
on a single sheet would fail this test.

For `D=iota(D0)`, the section `f=2−5x²/4+y` has norm `9x⁴/16`; all four occurrences
are at `(0,-2)`. Removing three leaves that same point and again returns `(0,2)`.
This checks an exact quadruple local zero without splitting it numerically.

The additional section `x²+y` has norm `5x²−4` and infinity orders `(0,2)`.
The section `x−1` has a double ramification zero at `(1,0)` plus infinity orders
`(1,1)`. All four regressions count exactly four section zeros.

## Executed precision and phase evidence

Inputs: origin, exact conjugate, conjugate offsets `2^-40` and `2^-100`, both branch
endpoints, and generic angle `1.3`. Each ran at `(epsbits,qbits)` equal to
`(12,32),(12,96),(24,64),(24,160)`.

The rejected calls were exactly the three conjugacy cases at `(12,32)` and `(24,64)`.
At `(24,160)` all seven passed. Largest original-target direct-Abel error was
`6.8825515412e-8`, attained at the branch endpoints; this is chiefly the intentional
point perturbation, not root computation error. The generic call's error against
the perturbed target was `2.8049976689e-42`. The near-conjugate `2^-40` case had
perturbed-target error `8.8233608528e-24`: do not conceal this difference by reporting
only the generic case.

Independent phase evaluation uses the specialized scalar integral
`A(theta)=-integral_0^theta du/sqrt(4-cos(u)^2)` and its full real period. Independently
integrating `dtheta/dtau=-sqrt(4-cos(theta)^2)` for signed time
`A(theta)-A(pi/2)` gives the relative doubled target. DOP853 uses ordinary float64,
so differences near `7.3e-13` on conjugacy tests are a comparator floor, not evidence
of a certified 13-digit bound. Generic and branch errors in angle are around
`1.2e-7` to `1.4e-7`, consistent with the deliberate perturbation.

The twelve-call chain begins at angle `1.3`, keeps the origin fixed, and uses
`(epsbits,qbits)=(24,160)` throughout. Every call passed admission. Independent
quadrature compares output with `2^j A(initial)−(2^j−1)A(D0)` modulo the period.
At step twelve the error is `0.00025401928326282621672823068975087316`, below its
numerical cumulative budget `0.00025401928326282621672823068980959822`. The tiny slack
is not an interval certificate; the checker allows `1e-29` absolute numerical slack.
A fixed per-step perturbation naturally amplifies by doubling. Requested final
accuracy would require reducing the per-step perturbation with the chain length.

## Exact evidence boundary

The rounded matrix and normalized rational kernel, gcds, norm polynomial,
squarefree multiplicities, rational isolating intervals, and infinity series are
exact algebra. Kernel coefficients are not asserted to approximate a uniquely
conditioned exact interpolation kernel.

Transcendental row evaluation, conversion of isolators to multiprecision midpoints,
quotient evaluation, matching, collar admission, projection, quadrature and error
comparisons are **noncertified floating calculations**. Matching uses float64 cost
entries; its enormous margins in the passing tests are useful diagnostics, not
rigorous inequalities. The code does not implement the theorem's full conservative
q schedule or certified analytic root neighborhoods. No arbitrary-genus bit audit,
raw-to-spectral acquisition theorem, complete Toda decoder theorem, full
fast-forwarding guarantee, novelty or comparative speedup follows from these tests.
