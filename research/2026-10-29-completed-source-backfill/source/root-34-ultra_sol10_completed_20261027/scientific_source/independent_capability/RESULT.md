# Exact waiting-loss acquisition for a coarse-detector photon factory

The completed construction is a compiler for a supplied finite-Fock,
single-mode optical model. It returns the entire retained photon-number
distribution, expected raw-source attempts and elapsed native clocks, and
photon/cost covariances, including vacuum/multiphoton source outputs,
every failed fusion restart and unbounded waiting time. It is not an
acquired photon factory or an
established advantage over the strongest ordinary transform method.

The independent model-side review passes at its stated scope.
`../factory_independent/PROOF.md` independently derives the controller,
costs, phase-type spectral reduction, nested finite closure and renewal
denominator. A separately built literal 103-state n4 chain agrees exactly
at lambda=.999,.99999,1
for every output probability, every photon/source and photon/time first
moment, and every tested shifted-PGF value. The independent phase-type
derivation recovers the same spectral shift formula. See the receipts in
`../factory_independent/results/`, especially
`comparison_n4_lambda999_1000.json`. The original acquisition JSON status
strings are preserved; this later independent check has separate provenance.

## Operation and finite closure

The source probabilities are `(99/500,4/5,1/500)` on `|0>,|1>,|2>`, and the
bucket efficiency is `19/20`. Raw preparations take one clock, with photons
created at the end. For n=2^k, prepare two half-size children sequentially,
retain the first throughout the second's complete preparation, apply one
clock of pair loss and balanced fusion, and keep port0 only on a no-click
result at port1. A click discards both children and restarts that node.
Ancestors continue waiting during all these clocks. Every stored photon
survives each clock independently with probability lambda. The fixed clock
includes its stated reset/readout/latency interface.

The joint state/source/time PGF is

    H_n(r;z,u)=E[1_(N=r) z^T u^C].

A first child's i photons, waiting t clocks for the second child, undergo
binomial thinning. Expanding `(1-lambda^t)^(i-l)` evaluates that second
child's complete PGF at `z lambda^(l+s)`. Success and failure use a literal
Fock beamsplitter/no-click kernel, and a renewal denominator charges every
failed retry. The first source/time derivatives are evaluated jointly with
the probability vector. The implicit full PGF is specified, but the code
does not emit all coefficients of the unbounded cost/time law.

At root z=1 all required arguments are lambda^e with

    0<=e<=2n-2<2n.

For k=log2(n), the complete cached scalar-argument node count is
`(2n+1)k-2n+3`. The scalar probability-vector entry count is
`[8n²+6n(k-1)+3k+7]/3`; the implementation carries three times this number
to include both derivatives. These are the exact unpruned counts for
0<lambda<1; at lambda=1 identical arguments collapse to one node per level.
Separate fusion and beamsplitter caches are
O(n³), and the supplied contraction has a conservative O(n^6) arithmetic
bound. Exact rational bit size is not inferred from that node count.

The proof, pole bound, precision scope and full clock convention are in
`WAITING_LOSS_PROOF.md`. `BOSONIC_FACTORY.md` derives the separate positive
integral lossless control and records why brightness did not establish a
useful non-Gaussian resource.

## Actually acquired finite records

Every number below uses the same raw source, detector and fixed policy.
Different lambda values give different output states, so their raw costs
are not a comparison at a matched delivered-state target.

| n | Survival/clock | Mean photons | Fano | Expected raw sources | Expected clocks | Cov(N,T) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | .999 | 2.915817809395 | .376349240894 | 19.3356956644 | 31.5560389544 | -.0270528205725 |
| 8 | .999 | 5.650297705841 | .442942988886 | 138.201325252 | 229.119610834 | -2.14876170718 |
| 16 | .999 | 10.1582468257 | .591855777915 | 1422.00447539 | 2362.64097791 | -159.771551794 |
| 32 | .999 | 14.3688953489 | 1.67846170024 | 52972.2193454 | 88031.2434968 | -3441.11644466 |
| 32 | .99999 | 22.8651019657 | .439938699797 | 20249.6003610 | 33648.1994424 | -560.453642231 |
| 32 | 1, ideal control | 23.1754935689 | .4284230341 | 20307.9398339 | 33745.1021222 | not acquired in the separate integral control |

The n4 and n8 `.999` acquisitions use exact Fractions. Maximum cached PGF
numerator/denominator sizes were 1836/1833 bits and 32107/32101 bits,
respectively; the n8 run took 4.87 seconds. Larger values have directed
dyadic enclosures, not just agreement between floating calculations:

| n, lambda | Precision | PGF nodes / derivative entries | Kernel entries / BS probability cache | Max e | Recorded interval operations | Recorded integer bits, stored / intermediate | Seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16, .999 | 512 | 103 / 2355 | 11184 / 4913 | 30 | 990688 | 536 / 1048 | 2.64 |
| 32, .999 | 512 | 264 / 8982 | 81969 / 35937 | 62 | 17616558 | 558 / 1212 | 46.22 |
| 32, .99999 | 192 | 264 / 8982 | 81969 / 35937 | 62 | 17616558 | 246 / 1403 | 30.59 |

For the 512-bit n32 record, interval widths are below `1.04e-139` for mean,
`3.18e-139` for Fano, `6.96e-136` for raw sources and `1.16e-135` for clocks.
The 192-bit higher-survival n32 record has respective widths below
`6.13e-41`, `1.78e-40`, `1.08e-37`, `1.78e-37`. All dyadic endpoints are
stored as exact integers divided by the displayed power of two. The n4
interval replay encloses every component of the exact Fraction result.
The intervals cover arithmetic rounding, with no physical input uncertainty
or calibration confidence interval included. The independent reviewer also
checked 36 literal-chain components inside its separate 256-bit n4 replay.

The integer-bit counters instrument the dyadic operations and rational-to-
dyadic conversions, not every temporary Fraction operation during kernel
construction. Operation counts likewise count the implemented directed
arithmetic calls, not every Python operation. Kernel construction is inside
the reported elapsed acquisition times. Peak RSS and a strongest-method
runtime comparison were not measured. The n32 `.999` kernel-entry metadata
was corrected separately from input-pair count to full coefficient count;
its certificate explicitly records that correction without attributing a
new run. The n16 and higher-survival n32 rows use actual corrected-counter
runs.

## Strong ordinary comparison and prior scope

The literal finite absorbing chain on the depth-first protocol stack and
stored photon counts is already exact, with no waiting-time cutoff. Its
transient state count obeys

    M_1=1, M_n=(n+1)²+(n+2)M_(n/2),

giving 13,103,1111,20287,690847 states for n2,4,8,16,32. These are counts of
that explicit representation, not a lower bound on ordinary algorithms.
A factored or spectral phase-type solver can exploit the same spectrum.

The deeper ordinary prior is
[Kuzmin et al.2019, SM E.2 Eqs.19–25](https://arxiv.org/html/1905.00335v2)
and [Kuzmin–Vasilyev2021, Sec.III.2 Eq.7](https://arxiv.org/html/2009.10415v1):
joint state/time transforms, memory-generator spectral shifts and geometric
failure resummation. This work applies those ideas to exact nested discrete
joint laws for a state-dependent bucket-herald factory. Its documented
finite shift set and numerical enclosures are concrete deliverables;
generic transform novelty is not claimed. Exact non-Monte-Carlo statistics
also have the closer recent
[Goodenough–Coopmans–Towsley2025](https://arxiv.org/html/2404.07146v5) prior.
`SOURCE_SCOPE.md` records exact primary sections and the policy/physics
boundaries, including established non-recycled/recycled Fock fusion.

## Physical and discovery status

The exact source tail/support, independence, common optical mode,
uniform pure-loss memory, detector law, native clock duration, reset/readout
latency and repeated-fusion mode matching have not been measured here.
These are essential unacquired inputs to a physical operation. Existing
single/two-photon memory demonstrations do not qualify this larger factory.
The physical primary-source record also separates laser repetition,
heralded production rate and electronics latency; borrowing one as the
native clock while omitting the others would not implement this interface.

The lossless factory has linear-in-n mean and sub-Poisson limiting Fano,
but its attained total Wigner-negative volume decreases strongly. More
negative rings or exact Fock rank therefore does not supply a robust
computational resource. Those volume estimates are numerical diagnostics;
exact root counts and negative-point signs are preserved separately.

The earlier phase-only logical-gate branch is preserved in `PHASE_GATE.md`
and parked: equally informed ordinary holonomic control and two-axis
synthesis use its admitted interface, with no established advantage.

Historical priority: UNKNOWN. Strongest ordinary-method advantage: UNKNOWN.
Physical implementation: NOT_ACQUIRED. Useful approximate quantum resource:
UNKNOWN. Civilisation-changing capability: NOT_ACHIEVED.

## Reproduce the acquired records

From the workspace root, with the existing scientific runtime:

```sh
work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/independent_capability/bucket_factory.py
work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/independent_capability/bucket_wigner.py
work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/independent_capability/waiting_loss_factory.py
work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/independent_capability/certify_waiting_loss.py 4 512
work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/independent_capability/certify_waiting_loss.py 16 512
work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/independent_capability/certify_waiting_loss.py 32 512
work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol10_constructive_frontier_20261028/independent_capability/certify_waiting_loss.py 32 192 99999/100000
```

The first three scripts regenerate files within this directory's `outputs/`;
their imports can also regenerate the separate ideal-control replay.
The certificate script includes a survival tag in nondefault-lambda output
filenames. Replays can update elapsed time and metadata; prior measured
timings are observations of their recorded runs, not guaranteed benchmarks.

The separate exact n8 record can be reconstructed without overwriting the
original acquisition:

```sh
work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python - <<'PY'
import sys, json
sys.path.insert(0, 'work/sol10_constructive_frontier_20261028/independent_capability')
from waiting_loss_factory import Acquisition, OUT
row = Acquisition('999/1000', exact=True).acquire(8)
(OUT/'WAITING_LOSS_EXACT_N8_REPLAY.json').write_text(json.dumps(row, indent=2)+'\n')
print({key: row[key] for key in ['mean', 'expected_raw_source_attempts', 'expected_wall_clocks']})
PY
```
