# Executed nonproduct 2D result — 2026-10-27

**ACHIEVED at the specified finite-model scope:** an exact deterministic
excursion-probability interval for the 8x8 periodic square-lattice Gibbs
heatbath source w(x)=(1/4)^n(x)*(9/8)^e(x), obtained by ordinary local
Galerkin with the full backward residual.

An outward decimal enclosure is

    3.6776584e-32 <= p_exc <= 3.6779362e-32.

The rational endpoints in `CERTIFICATE_8x8.json` are the authoritative
certificate; `approx` values are display approximations. The exact ratio
of upper to lower endpoints minus one is approximately
7.551615959787677e-5. Thus the requested 1e-3 multiplicative-width target
is met. The corresponding I interval is approximately
[0.02202263456649026, 0.02202429763127695].

## Model and structural proof

- All 2^64 states, 64 single-site unit clocks, 128 square-lattice edges.
- rho=9^128/2^512, approximately 1.0367724023455627e-32.
- R_a=64/5. The output includes the true continuous-time exit-law factor.
- Analytic gap >=57746297/63718265, approximately 0.9062754141218378,
  proved by exact local influences and common-uniform coupling.
- Conditional adjacent-pair cross ratio 9/8 disproves a site-bit product
  invariant. Adjacent/separated two-site states disprove count lumpability;
  a line/L three-site pair disproves even (occupied-count,occupied-edge-count)
  lumpability. See `PROOF.md` and exact checks in `INDEPENDENT_CHECKS.json`.

## Actual certificate costs and unresolved widths

The authoritative run was one unoptimized Python 3.14.3 process on the
recorded macOS host; this is a cost receipt, not a benchmark. Its timing
excludes source selection, coding, proof writing and literature retrieval.
The source parameters and geometry are supplied exact mathematical
inputs; no physical acquisition or calibration was performed or costed.

| Galerkin degree | Residual states | Relative interval width | Cumulative seconds |
| --- | ---: | ---: | ---: |
| 1 | 130 | 0.3155162832345769 | 0.0005465 |
| 2 | 4,162 | 0.003956182007957621 | 0.0117885 |
| 3 | 87,490 | 0.00007551615959787677 | 0.3306892 |

Degrees one and two produce valid deterministic bounds but do not meet
the requested 0.001 width. They are retained, without implying that the
degree-three success is generic.

Total successful certificate elapsed time was 0.3317102 seconds, peak
process RSS 70,680,576 bytes. It generated weights for 87,490 states and
evaluated 4,294 source rows / 274,816 directed flip contexts. The rate
denominator has 40 bits, weight scale 513 bits, largest recorded moment
1702 bits, and largest final Galerkin coefficient numerator/denominator
1751 bits. The full 18,446,744,073,709,551,616-state source was not
enumerated. The residual state count is the full radius-three union,
2*(1+64+2016+41664).

## Independent exact checks

`independent_checks.py` uses an independently built source and exact
Fraction forward elimination/back substitution for full small systems.
All checks pass in `INDEPENDENT_CHECKS.json`.

| Full small 2D control | Enumerated states | Killed-equation p (display) | Pinned-Poisson I (display) |
| --- | ---: | ---: | ---: |
| open 2x2 | 16 | 0.02053874635365328 | 0.3808081249338551 |
| open 2x3 | 64 | 0.001936432234366935 | 0.23962060464481263 |

For both controls the killed/Poisson potential identity is exact. Every
sparse backward power agrees with the full independently constructed
matrix. For all three degrees, direct full-state residual norm, the
completion-of-square identity, and containment of exact I and p agree
exactly.

For the 64-site source, the checker independently generates Hamming balls
and evaluates complete backward rows (pulls) rather than production's
reverse-rate column spreading. All powers through degree three agree
exactly. It directly recomputes the Gibbs weights of all 87,490 states
and matches every moment. The final check process took 1.8771 seconds
and 104,284,160 peak RSS bytes, including small controls, the large source
cross-check, structural witnesses, and the analytic comparator check.

## Comparator and claim boundaries

The exact operation is standard Galerkin/Krylov potential theory and is
available unchanged to an equally informed ordinary comparator.
Golub–Meurant already explicitly relates residuals to inverse quadratic
forms and energy error. `PROOF.md` links the primary sources, including
the heatbath/influence, capacity, sparse polynomial and CG antecedents.
No superiority or priority claim is made.

The positive-gap potential-kernel Monte Carlo comparator already has a
sample/event bound without 1/p under the same structural promises. The
JSON retains one conservative analytic bound at epsilon=0.001 and
failure probability 0.05; it is explicitly marked **not executed** and
is neither an optimal cost nor a benchmark. There is no new generic
rarity tractability class here.

## Failures and reproducibility

The first attempt stopped in output serialization: converting the
unnormalized scaled residual norm to a float raised `OverflowError`.
No certificate was emitted from that attempt. The display encoder now
stores `approx: null` for overflow while retaining exact numerator and
denominator strings. The arithmetic formulas were unchanged, and the
successful certificate and independent checks were rerun. The initial
failed process was reported by the shell at approximately 0.355 seconds;
its peak memory was not captured.

Run from this directory, with no third-party Python dependencies:

    python3 nonproduct_certificate.py
    python3 independent_checks.py

`nonproduct_certificate.py` supports small open-grid controls as well as
the fixed 8x8 fixture. The `--epsilon` option controls the stopping target;
an unmet degree cap is explicitly reported as
`CERTIFIED_BUT_TARGET_NOT_MET`. Exact singular Krylov systems raise an
error rather than fabricating an inverse.

This is mathematical/finite-model evidence. Input calibration, uncertain
source boxes, physical preparation or measurement, general low-degree
convergence, practical advantage, publication and priority remain
unestablished. No external service or publication was changed.
The executed parameters lie in the proved strong-mixing regime; this
does not resolve critical or metastable two-dimensional regimes.
