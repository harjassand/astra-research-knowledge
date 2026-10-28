# Independent review: accessible endpoint rational SDP and compiler

2026-10-28. Reviewer: `producer-workspace/review_repeated_service_factorization`.

**PASS, scoped: finite theoretical accessible-endpoint mechanism.**
Received source SHA-256:
`5a688f7fae8eb58110ac802247ac40b335327e3663f8e614cc46708af5801399`.
No unresolved mathematical/algorithmic obligation was found within this
endpoint contract after the corrections described below. Author sources
were not edited by this reviewer; the author preserved earlier versions. This is a mathematical/algorithmic
review plus independent exact fixtures, not execution of a general-purpose
SDP solver, a gate compiler, calibration calls or hardware.

## 1. Endpoint optimization: independently checked

The full-domain claim starts from a finite rational Hermitian signed Choi
matrix, not from a physical hidden realization. The source correctly permits
non-TP/non-CP inputs and an error allowance greater than one. Its two output
channel variables have exactly the intended dimensions and unrestricted
CPTP feasible sets. The recovery composition formula is correct in the
input-first Choi convention, including complex off-diagonal entries. Applying
coefficientwise Cauchy--Schwarz gives the advertised Frobenius Lipschitz bound
`ell = p`; no decoder positivity assumption is needed for that linear bound.
The physical first-stage service supplies `||Jtilde||F <= p`.

The TP affine basis spans precisely the partial-trace kernel. Its dimension
is `m^2(n^2-1)`, with the empty block correctly handled when `n=1`. The stated
Gram/norm inequalities are conservative. With the Hermitian Z coordinates
and t, the body is genuinely full-dimensional in the stated M coordinates;
there is no missing Slater assumption in a larger equality-constrained space.

I checked all inner-radius perturbations, including the scalar t caps, and
all outer-radius terms. Both Z inequalities imply `Z >= 0`, so the trace cap
really bounds its Frobenius norm. Each physical C admits an oversized scalar
Z below the t cap; the cap cannot remove an optimizer. Compactness and the
explicit inner ball hold even for an arbitrarily bad signed input. The
radii depend only on supplied data and accessible dimensions.

The rational negative-diagonal, zero-diagonal and Schur-complement witness
rules are correct over Q(i). In the zero-diagonal case the stated vector
has expectation `-|h|^2(d+2)/(d+1)^2 < 0`. Schur witnesses lift by an exact
rational congruence. Fraction-free arithmetic/minor bounds justify polynomial
intermediate and witness encoding lengths. The resulting scalar affine row
is a genuine separator, not an approximate eigenvalue-sign heuristic.

### Finite-bit weak optimization import

I inspected the primary [GLS paper, Sections 1--3, Theorems 2.4 and
3.1](https://ir.cwi.nl/pub/10046/10046D.pdf). Its weak optimization output
contract is the distance-to-body plus additive-objective contract used here.
Section 2 specifies rounded ellipsoid updates; Section 3 accounts for binary
length and polynomial time. The supplied center/radii, rational objective
and exact separator instantiate that import. An objective sign/constant
rescaling is harmless. The claimed `O(M^2 alpha)` query scale and polynomial
bit-cost form are appropriate; this is not an interior-point runtime claim.
This paragraph relies on that published finite algorithm, not an executed
local GLS implementation.

## 2. Rational repair and two-stage bit dependencies

For exact TP C with minimum eigenvalue at least `-aC`, its negative mass is
at most `mn aC`. The rational repair is exactly TP and has the stated positive
floor. Directly,

`||Cphys-C||1 <= 4mn aC (1+n aC)/(1+2n aC) <= 4mn aC`.

Thus the source's looser displacement constant is safe. It pays the same
half-diamond displacement after composition with the physical learned
service, without an extra input-dimension multiplier. Near-feasible Z is
shifted before claiming an objective bound; C itself is not mislabeled
physical. The epigraph residual and repair coefficients sum to `(W+1)/2`,
and `e <= sigma/(4W)` leaves ample slack. All chosen quantities are rational.

The optional non-TP normalization repair is also correct under its stated
smallness condition. It is not required for the main algorithm and therefore
does not introduce irrational coefficients into the second SDP. The first
rational output's polynomial encoding length supplies polynomial-length
composition coefficients for the second call. No exact optimizer or large
algebraic-number field is required. Nonrational controller/input rounding
must be paid before using the rational endpoint contract.

## 3. Compiler mechanism checked during review

The initial draft's reference to an imported stable completion procedure was
insufficient: the cited local imports did not actually give the quantitative
completion routine required here. I requested a concrete mechanism. The
author replaced that step with pivoted complex row-Givens QR, not a claim
that an arbitrary complement varies continuously.

The known Choi square-root residual, clipping and scalar-root tolerances give
Frobenius error below eW in the reshaped isometry. The gap-free square-root
bound costs eW/4; the scalar-root and total matrix-arithmetic allowances are
properly distinguished. This does not divide by a small Choi eigenvalue.

For `A=QR`, `R=I+H`, write `F=A* A-I`. In the real-diagonal upper-triangular
space, the inverse of `H -> H+H*` has Frobenius norm at most one. Hence
`||H||F <= ||F||F + ||H||F^2`. Along the positive Cholesky homotopy, the bound
`||F||F < 1/8` forbids crossing 1/2 and yields `||H||F <= 2||F||F`. This proves
the advertised `||Q-W||F <= 7eW` without comparing arbitrary unitary
complements. The exact QR product itself completes Q.

Every remaining column has distance from the previous span at least
`sigma_min(A) > 1/2`: minimizing `||A x||` with the new coefficient fixed to
one proves this directly. Therefore approximate pivot selection can certify
the stated inverse-polynomial floor. Givens denominators never approach an
uncertified zero. The source's deliberately loose operation count and
per-operation amplification bound support a polynomial precision-bit budget;
no backward-stability theorem is silently assumed.

The one-qubit normalization must occur **after** resolving controlled-gate
relative phases. Only the final primitive gates' common global phase can be
ignored. The revised comparison uses that physically correct convention.
For non-power-of-two output dimension, merely truncating leakage is not TP.
The revised known predicate/flag/reset channel is a real CPTP cleanup and
fixes the target logical subspace. Reusing reset environment workspace keeps
the peak qubit bound; its control cost must remain in the gate ledger.

The known two-level/multicontrol reduction is the appropriate use of
[Barenco et al., Sections 7--8](https://arxiv.org/html/quant-ph/9503016).
The source is dense accessible-system synthesis, not poly(log dimension)
control, unknown-environment inversion, or a delivered pulse-level circuit.

## 4. Finite precision in fixed-gate compilation: corrected and checked

[Dawson--Nielsen, Section 3](https://arxiv.org/html/quant-ph/0505030v2)
distinguishes compressed recursion output from writing the expanded gate
list and explicitly leaves finite-precision arithmetic out of its displayed
runtime analysis. I flagged both points. Its ideal-arithmetic recursion
cannot by itself be cited as a polynomial bit-time proof. The final source instead gives a separate finite-bit robustness argument,
which I checked rather than crediting it to the ideal-arithmetic paper.

The strict fixed coarse-net mesh/enumeration construction has a finite
termination justification and a paid gate-set-dependent constant. Its very
small fixed radius is not a practical preprocessing claim. The dyadic
recurrence satisfies
`4096 eta_prev^(3/2) <= eta_next <= 8192 eta_prev^(3/2)` and decreases from
`eta_0=2^-64`. Guarded omission handles tiny residuals; on every normalized
branch the Pauli-vector and chosen cross-product have the stated known
floors. The constructed vectors obey `f cross g = -h/2`, so the Pauli
commutator has the correct sign. An exponential-series remainder bound is
well below `100 ||h||^(3/2)`. Replacing two near-identity unitaries by
approximants costs at most `4 epsilon r + 2 epsilon^2`; the resulting
constant is below 512, comfortably inside the 4096 recurrence allowance.
Exact rational stereographic rounding keeps recursive targets unitary.

Every potentially small denominator is guarded by a power of the requested
local accuracy. Fixed-dimensional interval log, root and trigonometric
calculations therefore cost polynomial precision bits, not a reciprocal
accuracy search. The recursion has logarithmic-logarithmic depth,
`O(3^j)` nodes and `O(5^j)` expanded gates. Allowing polynomial-bit arithmetic
and gate-list output gives the claimed conservative polynomial bit bound;
it does not retain 2.71 as a bit-time exponent. No actual coarse net or
compiled gate list is claimed to have been produced here.

I also checked the additional known-target arithmetic, which is now
explicitly separate from the QR budget. Among four phase charts, two unitary
eigenvalues can exclude at most two radius-.7 neighborhoods because
`2*.7 < sqrt(2)`. Thus a chart with `sigma_min(I+zeta U)>1/2` has constant
selection slack. The displayed Cayley matrix is Hermitian with norm at most
four, and the square of its stated root is exactly zeta U. The positive
inverse-root matrix has spectrum in [1,17]. Controlled scalar phases are
retained. Guarded Euler/phase charts pay small-entry omissions inside the
assigned target error. These are finite known-matrix operations, not an
assumed eigengap or exact trigonometric oracle.

For the rational Jacobi import I inspected the actual Section 2 contract
and its independent statistics receipt: the source hash is
`8b5859b44e398d5d97d5b14580041bd9232b9fe59188a9c090634d6a4dbab0b6`.
Scaling `C_R/(2k)` meets its known PSD norm-at-most-one-half domain; rescaling
the requested residual gives exactly the square-root input accuracy needed
here. Only that accepted known-matrix primitive is imported, not any of the
source's statistical, Gaussian-rounding or effect-optimization conclusions.

## 5. Comparator transfer, records, and scope

The true service is a feasible first-stage competitor, giving distance at
most `2 eta + xi` between it and the learned physical service. Comparing
both the selected decoder and an unrestricted true-service optimum costs
that allowance twice. The second slack and actual compiler error are added
once, giving `4 eta + 2 xi + zeta + nu`. The argument is complete-norm and
has no Pauli/noise/Bell-loss restriction.

The deterministic theoretical optimizer works on every finite rational
input and needs no optimization-success probability. A separately capped
practical solver can still abstain and must pay that event outside statistical
beta. The module does not remove reset/full-core assumptions, core-test
abstention, data-rationalization errors, or the distinction between a
record-averaged deployed channel and an expectation of conditional diamond
norms. A whole-process implementation debit is not charged twice.

The accepted full-core predictor and direct-service-tomography comparison
remain unchanged. This endpoint mechanism does not create an advantage over
end-to-end IC tomography when comparable full-service calibration episodes
are allowed. It supplies a specified accessible endpoint operation for the
signed predictor; it is not a hidden-model reconstruction, low-rank,
infinite-horizon, hardware, novelty, or practical-speed claim.

## 6. Independent executed checks

`accessible_endpoint_independent_check.py` imports no author checking code.
It uses exact SymPy rational/complex algebra and reports:

* 16 affine-basis/dimension cases, including scalar input/output edges;
* 729 exact center-radius/slack checks;
* complex zero-diagonal and congruence negative witnesses;
* a signed Pauli service whose nearest unrestricted CPTP distance is 1/7;
* three complex rational TP repairs with exact PSD-floor/trace-norm checks;
* fully depolarizing qubit recovery with unrestricted CPTP optimum 3/4;
* complex input-first Choi composition checked against actual Kraus products,
  and its full linear Frobenius operator bound;
* a complex Fourier isometry times a known near-identity triangular factor,
  independently recovered by exact five-rotation QR, including unitarity,
  thin-isometry agreement and the Cholesky perturbation inequality;
* an explicit padded-output CPTP cleanup fixing every logical matrix unit;
* 10,000 dimension/ancilla inequalities;
* six exact Pauli-log commutator identities, exact rational unit-quaternion
  rounding, 20 dyadic recurrence levels and their slack/node bounds;
* four guarded Cayley-root cases, including a branch cut and a near-cut
  unitary, with exact root-square identities and spectral floors.

These fixtures do **not** execute generic rounded ellipsoid optimization,
finite universal-gate compilation, source acquisition, or physical control.
They supplement, rather than substitute for, the general proofs above.

## 7. Receiving conclusion and preserved obligations

The companion closes the signed full-core theorem's previously explicit
**theoretical finite accessible SDP/compiler mechanism**, at the supplied
rational signed-service interface. The old signed-core receipt remains
unchanged; this is an additional module with its own source binding. The
optimization and compiler are deterministic finite algorithm constructions,
not free oracles. The compiler's large dense-control costs and fixed-net
preprocessing are part of the mechanism, not a claim of practicality.

Production solver software, a production finite-gate compiler, actual
calibration and deployment remain unexecuted. Core acquisition and input
rationalization remain the outer theorem's responsibility. Hardware-native
routing, storage and noise require their own resources/error ledger. No
new comparator advantage, collective-decoder optimum, threshold, low-rank
inference or hidden-environment realization is received.

The machine-readable receipt binds the final source, this audit, independent
script/results, author evidence, relevant local interfaces and preserved
source versions. The primary pages were read during this review; failed
screenshot extraction is not presented as visual inspection.
