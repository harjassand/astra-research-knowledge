# Executed nonreversible capacity operation

Status: TARGET_MET for the actual 32-bit and 64-bit local generators.
Both exact primal/dual certificates passed separate complete-residual
audits. Small independently assembled full-state killed, Poisson and
adjoint controls also passed. These are mathematical/computational results
for the explicit supplied source. Physical performance, acquisition,
novelty, practical superiority and arbitrary hidden-shock robustness were
not established.

The source has product Gibbs weights w(x)=4^(-|x|), unit single-spin heat
baths and directed cycles on EVERY adjacent pair, with gamma=1/2. Cycles
overlap. Boundary stationary net current is 1/32 before normalizing by
Z=(5/4)^n, so the generator is nonreversible. Context-dependent flip rates
make the dynamics interacting. The invariant Gibbs law has product form;
no nonproduct law is claimed. The symmetric gap is analytically at least
1. All rates share the exact denominator 160.

## Certified answers

The target was p_upper/p_lower<=1+1/1000, with degree cap THREE. Target
decisions and endpoints are exact rational computations. Decimal intervals
below are rounded outward; exact JSON endpoints are authoritative.

| n | Full state count | Exact rho | R_a | Rmax | Certified p_exc, outward display | Relative endpoint width |
|---|---:|---|---:|---:|---|---:|
| 32 | 4,294,967,296 | 2^-64 | 7.36875 | 41.1 | [2.9984258990e-19, 2.9991903790e-19] | 0.000254960419774139 |
| 64 | 18,446,744,073,709,551,616 | 2^-128 | 14.76875 | 82.7 | [1.6389554373e-38, 1.6390563676e-38] | 0.0000615820399248671 |

This is the actual exit-law probability, not stationary mass rho/Z. The
I intervals are approximately [0.02452914558,0.02453539955] for n=32 and
[0.01214011852,0.01214086614] for n=64; p_exc=rho/(R_a I).

Lower degrees did NOT meet the target. Their intervals and costs remain
in each result's `degrees` array:

| n | Degree 1 relative width | Degree 2 relative width | Degree 3 relative width |
|---|---:|---:|---:|
| 32 | 0.941498382945 | 0.010268296422 | 0.000254960420 |
| 64 | 0.952173051953 | 0.005106642810 | 0.000061582040 |

No degree beyond three was attempted. These successes are not a uniform
degree guarantee.

## Arithmetic, memory and time costs

The routine uses ordinary weighted GMRES for BOTH H and H*. Small exact
normal equations minimize full weighted residuals over each Krylov space.
Every predecessor is included in sparse backward action. The enclosure
uses a corrected goal estimate and BOTH full residual norms; it does not
import the reversible one-sided lower-bound formula.

| Cost | n=32 | n=64 |
|---|---:|---:|
| Largest support per primal/dual residual | 10,978 | 87,490 |
| Trial support per primal/dual at degree 3 | 1,058 | 4,162 |
| Stored vector entries, both chains and all degrees | 24,208 | 183,568 |
| Sparse local-term evaluations, both chains | 141,876 | 1,090,676 |
| Largest weight/source scale W bits | 65 | 129 |
| Largest integer Krylov value bits | 103 | 170 |
| Largest Gram entry bits | 205 | 339 |
| Largest coefficient numerator / denominator bits | 301 / 312 | 503 / 515 |
| Certificate computation seconds | 0.03908 | 0.36589 |
| Certificate process peak RSS, decimal MB | 26.36 | 58.29 |
| Independent gather audit local-term evaluations | 1,383,228 | 22,222,460 |
| Gather audit seconds, INCLUDING certificate regeneration | 0.36975 | 5.55799 |
| Independent audit process peak RSS, decimal MB | 36.52 | 117.28 |
| Full-residual common-denominator bits | 314 | 515 |
| Largest independently assembled residual numerator bits | 361 | 623 |

The certificate timer includes source/weight construction, both Krylov
chains, Gram/cross terms, exact solves, interval arithmetic and cost-record
preparation. It excludes Python startup and final JSON I/O. Observed first
CLI process wall times were 0.427 s and 0.725 s. Audit timers include
reading the saved result and regenerating the certificate, but exclude
startup/final I/O. Peak RSS values are whole-process maxima. These local
measurements used macOS 26.4 arm64 and Python 3.14.3; they are not portable
latency guarantees or a hardware advantage claim.

The final expanded small-control run took 0.27817 s, including the
three-state counterexample (CLI process 0.627 s). The earlier pass without
that counterexample took 0.25329 s. Both large audits rerun the certificate,
so those costs are additional to the initial runs. Source research and
agent proof work are outside machine timing. Main certificates use the
standard library only. Small dense controls use the already installed
python-flint 0.9.0 dependency read-only from the sibling source directory;
no installation or paid compute was performed.

The source is a compact exact mathematical specification: n,theta,gamma,
the adjacent-pair rule and known Gibbs law. For a variable explicit local
source, its complete description and arithmetic bit lengths would also be
input costs. Computing rho=4^-n has O(n) represented bits and is included.
An empirical user who lacks the invariant law or gap has not supplied
this operation's premises. Physical estimation, preparation, acquisition
and physical-clock calibration are not represented as free or completed.

## Independent controls and falsification checks

`controls.py` independently assembles literal state tuples and local
cycle order, without the sparse operator's transition tables. For
n=2,3,4,5 with theta=1/4,gamma=1/2 and n=4 with theta=2/5,gamma=3/7,
these exact rational checks passed:

- Nonnegative off-diagonal rates, zero row sums, invariant weighted
  column sums, and net current exactly gamma theta^2.
- EVERY column of H and independently weighted-transposed H* agrees
  with sparse backward action: 152 columns across five fixtures.
- Killed hitting-probability solves and Poisson/adjoint solves agree
  through I=rho/(R_a p_exc).
- Exact product base eigenfunctions confirm its gap; exact semidefinite
  elimination confirms the added symmetric form is positive semidefinite.
- Full residuals match scaled Gram norms; the corrected estimate and
  exact error identity agree; intervals contain the full-state answers.
- Four powers of rational uniformisation kernels verify the quartet
  kernel identity.

The fixtures contain 4+8+16+32+16=76 states, hence 152 operator columns
and 76 product base eigenfunctions. The second theta also tests the
nontrivial N=p^n normalization rather than only the default N=1 case.

At n=32 and n=64 a separate implementation forms the actual rational
trial vectors and gathers outgoing differences at EVERY row in their
full single-flip closure. Directly summing squared residual values
matches both Gram norms and the corrected goal estimate exactly. All
10,978 / 87,490 candidate rows per residual are included, weighted mean
zero is checked, and the error radius is verified outward. This does
not enumerate 2^n or claim an independent large full Poisson solve.

The parent suggested a three-state clockwise-2/counterclockwise-1
counterexample, which was independently assembled and executed here.
Its I_hat=87/196 exceeds true I=3/7, disproving the reversible one-sided
claim, while radius 1/63 covers the error. It also disproves merging
cross terms. Those adverse controls remain in CONTROLS_SMALL.json.

## Ordinary comparator boundary

GMRES, nonreversible potential theory and primal/dual residual estimation
are established ordinary methods; primary sources and direct proofs are
in PROOF.md. Every ordinary solver receives the full same construction.

The equally informed lazy-uniformisation Monte Carlo construction in
PROOF.md has polynomial sample/event/expected-bit cost in size, inverse
gap and inverse accuracy when Rmax/g is polynomially bounded, without
1/p. Conservative sufficient epsilon=1/1000, failure-probability=1/100
budgets were calculated with an exactly checked log(200)<6 bound:

| n | Maximum sampled integer time L | Sufficient samples | Maximum P-steps |
|---|---:|---:|---:|
| 32 | 2,422 | 18,035,493,888,000,000 | 87,363,932,393,472,000,000 |
| 64 | 5,113 | 80,342,003,712,000,000 | 821,577,329,958,912,000,000 |

These are conservative theoretical confidence budgets, not measured
necessary costs or executed simulations: ZERO Monte Carlo samples were
run. Exact resource-budget arithmetic took 0.01185 s, excluding startup
and file I/O. Such loose budgets do not prove a practical advantage over
informed ordinary methods, which can use this same deterministic GMRES
certificate. They refute a generic 1/p barrier under the stated promises.

## Reproduction and files

Run in this directory with Python 3.14 and the already present FLINT
dependency for small dense controls:

```sh
python3 -B nonreversible.py --n 32 --degree-cap 3 --output RESULT_N32_CAP3.json
python3 -B nonreversible.py --n 64 --degree-cap 3 --output RESULT_N64_CAP3.json
python3 -B controls.py --output CONTROLS_SMALL.json
python3 -B controls.py --large RESULT_N32_CAP3.json --output CONTROL_N32_FULL_RESIDUAL.json
python3 -B controls.py --large RESULT_N64_CAP3.json --output CONTROL_N64_FULL_RESIDUAL.json
```

Result JSON records every degree's coefficients, exact endpoints, costs
and target status. Large controls regenerate and compare saved endpoint
fields before the independent gather audit. The separate theoretical
budget is ORDINARY_MC_RESOURCE_BOUND.json, which explicitly records zero
Monte Carlo samples executed.
