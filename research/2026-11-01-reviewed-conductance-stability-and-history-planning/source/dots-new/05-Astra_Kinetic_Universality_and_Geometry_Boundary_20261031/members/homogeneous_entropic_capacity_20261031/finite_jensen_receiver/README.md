# Finite sub-1% full-conductance receiving

**Status: source-frozen, author-tested; independent whole review pending.**
No earlier accepted source or package was modified.

Useful operation: after acquiring a complete raw coupled-quartic polynomial,
compute ONE additional monotone scalar resistance. It receives a finite interval
for the FULL isotropic diffusion's equilibrium capacity/mass—without evaluating
its angular partition function, sampling its fibers or solving a high-dimensional
PDE. This is not merely a free-energy upper bound or an asymptotic approximation.

The executed 513-dimensional chain (3,069 raw expanded monomials) gives

    [2.369045057852262e-37, 2.384988210037886e-37]

with exact endpoint ratio 1.0067297800574877, strictly meeting a requested 1.01
ratio. Cost: 131,074 scalar evaluations, 1664-bit dyadic root precision, up to 33,793
bits in the additional point powers; 81.28 seconds observed producer time.
Verification actually replays the entire construction and pays comparable cost.
These displays/timings are diagnostic; finite_results.json carries exact values.

## Run and receive

Python3 standard library, with the sibling acquired_quartic_consumer preserved:

    python -B receive_jensen.py    # reproduces all finite examples, including m512
    python -B check_finite.py      # 2,458 assertions and all saved result replays

Programmatic example:

    from fractions import Fraction
    import receive_jensen as j
    raw = j.base.fixture(512)       # fixture generation is separate paid input work
    cert = j.certify(raw, quad_relative=Fraction(1,1000),
                     full_ratio=Fraction(101,100))
    receipt = j.verify(raw, cert, quad_relative=Fraction(1,1000),
                       full_ratio=Fraction(101,100))

full_ratio may be None to return the finite bracket without a requested maximum.
If supplied it must be a strict Fraction>1. The receiver binds it as an external
task; a width failure is UNKNOWN. The method does not promise every requested
accuracy, and does not silently refine forever to obtain one.

The code checks the exact accepted scalar source hash before import. It then
charges all raw/scalar work plus N+1 additional integrand evaluations against the
TOTAL caller point budget. New schema/method, source hash, raw/task records,
requested width, every exact interval endpoint and full width are recomputed.
Display, timing and operation-counter metadata are non-proof diagnostics.

## What changed

Set a=1+kappa and alpha=m/4. The accepted parallel proof, BEFORE its uniform
contraction estimate, gives the finite lower denominator

    R_plus = integral [a²/(2a-v(y))]^alpha dy.

Both R_plus's integrand and the old resistance integrand are monotone on the
half-slab. Consequently one exact integer-power/fourth-root Darboux operation
receives [1/(beta MA R_plus),1/(beta MA R0)]. No Gamma function or additional
normalization is numerically calculated. The old radial factor is still computed
as an unused inherited intermediate; all its costs/refusals remain real.

## Files and boundary

FINITE_JENSEN_PROOF.md gives the complete finite join and arithmetic directions.
COSTS_AND_SCOPE.md retains all acquisition, bigint, verification and ordinary
comparison costs. DEPENDENCIES.json binds the accepted raw/global-process and
parallel theorem receipts. EXECUTED_RESULTS.md and finite_results.json give the
actual finite runs. check_results.json records all 2,458 author assertions and
replays. FROZEN_SHA256.txt binds the exact construction for separate review.

This does not receive arbitrary positive forms or hidden coordinate changes,
noisy coefficient fits, physical calibration, angular mixing, arbitrary-start
passage times, first-hit CDFs, a sampler, or a general complexity separation.
Ordinary methods supplied this same finite Jensen theorem obtain the same result.
Historical priority and applicability to particular scientific systems remain open.
