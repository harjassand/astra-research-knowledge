# Checkpoint result and continuation decision

21 October 2026. Scientific owner: Astra PRO2. Repository integration owner: Max.

## Strongest result

An explicit finite-precision spectral-CDF certificate has been constructed,
proved, implemented and replayed against original public matrix coefficients.
Its central theorem turns an imperfect stored Krylov basis into an exact
self-adjoint quadrature operator without enumerating the omitted complement.
For checked recurrence and last-diagonal budgets r,z, its operator perturbation
is bounded by

    Esharp(r,z) = (z + 2 sqrt(z^2+3r^2))/3.

The constant is sharp for this explicit completion given those two budgets,
already in dimension two. An independently checked eigenvector-rotation
counterexample invalidates the tempting horizontal-shift-only CDF transfer.
The correct transfer includes a vertical allowance e/eta, or the sharper
projection-angle function proved in the local note.

The complete operation includes exact input conversion, guarded integer Gram
and residual products, integer Sturm root isolation, directed Christoffel
weight enclosures, finite-bit Gaussian coupling, a uniform concentration
theorem, and independent replay. Floating solver success is never a certificate.

## Scientific question and literature boundary

The question is whether fractions of eigenvalues below thresholds selected
after observing the data can be certified economically from Krylov computation.
Uniformity over thresholds is relevant whenever the threshold is selected
exploratorily; a pointwise confidence statement does not establish it.

CMS envelopes and uniform SLQ bounds already exist in Chen–Trogdon–Ubaru 2021.
Finite-precision nearby-probe theorems also exist in Chen–Trogdon 2023 under
their stated hypotheses. This packet does not claim either discovery. The
aggregate-normalized Gaussian radius used here follows from classical
Dirichlet spacings and DKWM; its precise historical priority is unknown.
The concrete contribution is the explicit checked combination and sharp
completion argument, with an actual error mechanism and cost comparison.

## Actual input and fixed experiment

The NIST Matrix Market bcsstk08 stiffness matrix has order 1074 and 12960
entries after symmetric expansion. Its bcsstm08 companion is positive and
diagonal. The exact target is

    A = M^(-1/2) K M^(-1/2) / 33554432.

Every printed decimal coefficient is interpreted exactly. This follows the
source's generalized eigenproblem, rather than treating stiffness eigenvalues
alone as physical frequencies. No finite-model-to-building error is claimed.

Before looking at spectra, the experiment fixed eight probes, Krylov depths
32 and 64 (prefixes of the same 64-step proposals), matrix/J denominator 2^32,
basis denominator 2^29, and a 15-value positive transfer-margin grid. The
full proposal uses two reorthogonalization passes per step. The random bit
block is saved once and is never redrawn. Details: notes/experiment_plan.txt.

The matrix-to-target norm allowance is 1.9332697082505917e-8 in scaled units.
Per-probe completed-operator allowances range from 6.0886e-8 to 6.2408e-8 at
32 steps and 8.5288e-8 to 8.7173e-8 at 64 steps. The verified dense comparator's
sorted-eigenvalue radius is 4.224215560941542e-8.

The candidate's sampling radius is approximately 0.024835471099692464; the
displayed CTU2021 equal-weight sphere bound gives 0.03776619067605834. Gaussian
conversion contributes at most 2.6227881161304467e-13 to the candidate CDF.
Each stochastic method has its own 0.01 failure budget under the stated iid-bit
model, plus the conservative radial-cell allowance 4296/2^64. A joint claim
about both stochastic bands would use 0.02 plus that common allowance. The dense
certificate is deterministic. Repeated-run coverage is not a posterior
probability assigned to these saved words or conditioned on favorable success.

## Accuracy comparison

Widths are fractions of the complete spectrum, not Hartree and not exact-rank
errors. Global maxima are computed over every breakpoint of the exact piecewise
envelopes, not inferred from a plotted grid.

| Operation | Maximum CDF interval width over all thresholds |
| --- | ---: |
| Weighted Gaussian SLQ, k=32 | 0.6944662996514789 |
| Classical equal-weight SLQ, k=32, same numerical guarantees | 0.7069364199999140 |
| Weighted Gaussian SLQ, k=64 | 0.6288212904932393 |
| Classical equal-weight SLQ, k=64, same numerical guarantees | 0.6419953364110548 |
| Verified full diagonalization | 9/1074 = 0.008379888268156424 |

Representative widths at thresholds taken between dense eigenvalue proposals
are below. Those data-dependent display choices are permitted by the uniform
guarantee. They are not separate independent tests.

| Display percentile | Weighted k64 width | Classical k64 width | Verified dense width |
| --- | ---: | ---: | ---: |
| 10 | 0.6103228540 | 0.6234653110 | 7/1074 |
| 50 | 0.6196777124 | 0.6327986973 | 2/1074 |
| 75 | 0.1020209159 | 0.1279755529 | 0 |
| 90 | 0.0614571717 | 0.0872748597 | 0 |
| 95 | 0.0609130439 | 0.0867277472 | 0 |

Width zero in the dense column means the certified count at that particular
threshold is exact. It does not claim that the eigenvalues themselves were
represented exactly. The candidate gives useful bounds in some upper portions
of the spectrum, but performs badly as a uniformly accurate whole-CDF method
on this input.

## The actual failure mechanism

The completed dense certificate proves that exactly 604 of 1074 eigenvalues
are at or below 1e-4 in scaled units. A large low cluster is compressed into
the first quadrature node. At k64, that node's certified weight is approximately
0.533 to 0.620 across the eight probes.

At the fixed median display threshold x=12983/536870912, exact node brackets
prove theta_1<x<theta_2 for every saved Jacobi matrix. Hence the CMS lower
envelope L_l(x-eta_l) equals zero for every eta_l>0. Its upper envelope at
x+eta_l contains at least the first two weights. Positive averaging,
nonnegative error allowances and intersection over margins cannot remove that
width. The independently verified lower bound is

    fixed saved k64 CMS-envelope width >= 0.594136495994455906.

The analogous k32 bound is >=0.662533215753441563. These are rigorous downward
decimal renderings; the JSON records exact rational bounds. This obstruction
holds even if the checker and sampling allowances are set to zero. It applies
to the stated lag/lead envelopes for these fixed Jacobi data, including
separate positive margins per probe. It is not a lower bound for every possible
method using the moments, nor a universal spectral-estimation impossibility.

At the k64 median threshold, the measured width decomposes as follows:

| Contribution | Width |
| --- | ---: |
| Saved CMS width at zero numerical and sampling error | approximately 0.594136495994456 |
| Numerical transfer and starting-vector allowance | approximately 0.000705745285051 |
| Sampling plus Gaussian conversion, with lower clipping | approximately 0.024835471099955 |
| Returned candidate interval width | 0.6196777123794612 |

The deterministic stored-probe band alone has width 0.5948422412795065. It
certifies the norm-weighted probe measure, not the unweighted spectral CDF.
Increasing checker precision cannot cure this retained-envelope floor.

## Resource result

The fixed experiment, including both depths, both stochastic comparisons,
the dense comparator, exact checks, margin optimization and serialization,
took **59.4415 s wall and 59.4303 s process CPU**, with **100147200 bytes** peak
process RSS. Threads were limited to one for the numerical experiment.

| Stage | Observed wall seconds |
| --- | ---: |
| Original-input interval construction | 0.25875 |
| Saved-bit Gaussian construction and coupling | 0.45941 |
| All eight 64-step Krylov proposals | 0.02991 |
| Integer residual checks for both depths | 0.41060 |
| Exact Jacobi nodes and interval weights for both depths | 27.60044 |
| Envelope construction, evaluation and global-width optimization | 27.98549 |
| Ordinary dense eigenvalue/eigenvector proposal | 0.17094 |
| Complete integer verification of dense proposal | 1.50491 |
| Remaining in-process serialization and orchestration | 1.02107 |

The Jacobi construction includes **18 insufficient-precision attempts**, costing
17.90240 s within the 27.60044 s total. The fixed weight-width goal was 1e-28;
six k64 certificates completed at 164 decimal digits/204 unscaled root bits,
and two at 196 digits/236 bits. These were bounded attempts to complete the
same exact small-matrix check, all charged, not new scientific Lanczos runs.
This implementation's overprecise weight target and literal rational envelope
optimization are expensive; the cost defeat is for the implemented operation,
not an optimized asymptotic lower bound on all certification methods.

The dense proposal plus verification costs 1.67585 s before the shared input
construction. That comparator is both much more accurate and much cheaper on
this matrix. Calling the 0.02991 s Krylov proposal the candidate's total cost
would give the wrong decision.

Independent replay used **33.14381 s wall**, **33.13715 s CPU** and **84217856
bytes** peak RSS. It drew no new probes and invoked no eigensolver. The exact
saved-J floor and cluster-count calculation used another 0.05351 s wall; its
separate arithmetic challenge used 0.07545 s. All child diagnostics, retrieval
failures, code repairs, repeated runs and unmeasured development costs are
retained in COSTS.md and the raw receipts. These process timings do not measure
model inference cost, energy, monetary cost or all external service latency.

## Verification status and repairs

Producer checks pass; full replay passes; separately owned challenges checked
the sharp completion theorem, projection-transfer theorem, random-bit coupling,
integer implementation, full-spectrum comparator and integrated CDF/floor.
The integer-code audit found and repaired unchecked input dtypes/symmetry,
negative allowances and silent integer truncation at public entry points. A
later integration audit bound probe dimensions and certificate counts during
replay. Directed Decimal absolute value was corrected before the small Jacobi
test run. All such failures and repairs remain in the source/audit records.

Small floating diagnostics test algebraic implementations; they do not prove
theorems or replace certificate arithmetic. The iid random-bit premise remains
a stated probabilistic assumption. Upload and local replay do not establish
Max's independent verification, integration, or scientific acceptance.

## Continuation decision

**Close the tested small-depth CMS-envelope operation as a practical whole-CDF
advantage on this input. Preserve the positive theorem, checkers and witnesses.**
There will be no default increase in k, probe count or floating precision to
chase this result. The existing floor shows why numerical polishing is the
wrong next mechanism, and ordinary computation already wins the actual test.

The next chosen question is the distinction between a coarse CMS staircase
and information genuinely missing from the retained moments: for the same saved
k64 Jacobi data and certified support, what is the sharp possible interval of
mass below the existing median threshold among positive measures matching the
retained moments? The next bounded step is an extremal truncated-moment
construction with both feasible measures and matching polynomial dual bounds,
expressed directly in the Jacobi/orthogonal-polynomial basis. It reuses existing
data and runs no new Lanczos calculation. Classical Markov–Krein/canonical
moment representations are the comparator and must be read before claiming
novelty. The decision is whether the present plateau is information ambiguity
or avoidable looseness of the particular envelopes. This is not yet executed
and no improvement is claimed. CONTINUATION.txt states the exact obligation.

The broader autonomous research mission remains active. Hidden-entropy, N33,
N557, IQM and other owners' programmes were not reassigned or repeated. The
closed molecular result and all earlier retired operations remain preserved.
