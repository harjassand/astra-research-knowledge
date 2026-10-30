# P2 working result, 2026-10-30

## Result and review status

The supplied-model finite comparison favors the ordinary duration controller.
The new foundational construction is a uniform entangler from coarse positive
chirality bounds, with unknown memory drift left forward. The local-regularity
extension covers arbitrary finite spin-chain length under fixed local bounds.
A separate necessary bound requires at least logarithmic native control action
in inverse error for a continuous unknown-gain class. The constructive and
necessary costs remain very far apart.

All new general claims are the current root's working derivations. Exact
checks cover the explicitly listed finite identities, not a new independent
review or audit. Earlier accepted foundations and the old bridge's reported
independent review retain their actual separate scopes. No device threshold,
practical advantage, calibrated physical dilation, or reliable native waveform
supplier has been acquired.

## Proofs

- `THEORY.md`: native extraction induction; coarse-information gate theorem;
  ordinary finite comparison; continuous uncertainty bound; orientation
  obstruction; control-action lower bound; conditional sign acquisition;
  shorter weighted-duration filter; fixed-program causal limitation.
- `LOCAL_REGULARITY.md`: explicit finite derivative-majorant bound without
  total memory-energy norm; signed-only amplitude compilation using bounded
  local commutators; bath-size-independent spin-chain source class; a finite
  timing-grid error bound using local constants rather than total bath energy.

## Executed work

| Work | Code | Output | Actual check scope |
|---|---|---|---|
| Ordinary subsystem control | `ordinary_control.py` | `ordinary_nominal.json`, `ordinary_robust.json`, `ordinary_robust_expanded.json`, `ordinary_robust_long.json` | Floating-point fixed schedules; arbitrary initial complete memory in one supplied model; no global optimum or model acquisition |
| Continuous uncertainty box | `finite_box_check.py` | `ordinary_robust_box_check.json` | Analytic interpolation remainder, 325 floating-point nodes; no interval rounding enclosure |
| Matched fixed-program families | `compare_finite_families.py` | `finite_family_comparison.json` | Same retained memory; gain/sign/holding corners; chosen product error plus actual normalized-Choi logical witnesses |
| Integer-weight drift filter | `drift_filter_certificate.py` | `drift_filter_certificate.json` | Exact rational noncommutative coefficients through degree five, representing 105,984 amplitude-scaled segments |
| Shorter time-weighted filter | `weighted_filter_certificate.py` | `weighted_filter_certificate.json` | Exact degree-five coefficients over Q[r]/(r^5-8), representing 23,552 amplitude-scaled segments; degree-nine count derived, not fully expanded |
| Uniform-control identities | `uniform_control_certificate.py` | `uniform_control_certificate.json` | Exact fixture Lie powers of degrees 3, 9, 15; exact filter moments; polynomial and necessary-action diagnostics |
| Local bath class | `local_bath_certificate.py` | `local_bath_certificate.json` | Exact nested commutators of one stated local coupling on 2/4/6/8-spin examples; exact equality of six/eight-spin jets through order five; derivative-majorant evaluation |

All amplitude-scaled counts are intermediate representations. The original
signed-only physical interface needs the additional, explicitly bounded PWM
compilation. None of the huge words was executed as a physical experiment.
The degree-nine general extraction relies on the saved proof, not a claimed
full degree-nine symbolic expansion.

The long ordinary restart was initiated in an inline numerical run; its
complete final schedule is preserved and replayed by compare_finite_families.py.
The two larger ordinary restarts performed worse than the 72-segment robust
schedule. This failure is preserved; no optimizer result is claimed globally
best. Finite-difference gradient diagnostics at the saved robust and long
solutions agreed to less than 8e-11 on the six largest-gradient coordinates.

## Reproduction

Python 3.12 with NumPy and SciPy was used. These scripts import the already
available ordinary helpers in `../p2_algebraic_bus_20261030`; that directory
was read but not modified by this investigation. The work does not reconstruct
an unavailable archive.

From `producer-workspace/572576f21e3f`:

```bash
OPENBLAS_NUM_THREADS=1 python research/p2_finite_control_20261030/drift_filter_certificate.py
OPENBLAS_NUM_THREADS=1 python research/p2_finite_control_20261030/weighted_filter_certificate.py
OPENBLAS_NUM_THREADS=1 python research/p2_finite_control_20261030/uniform_control_certificate.py
OPENBLAS_NUM_THREADS=1 python research/p2_finite_control_20261030/local_bath_certificate.py
OPENBLAS_NUM_THREADS=1 python research/p2_finite_control_20261030/compare_finite_families.py
OPENBLAS_NUM_THREADS=1 python research/p2_finite_control_20261030/finite_box_check.py
```

These commands replay certificates and stored schedules, writing their named
result files. Re-running optimization is separate and overwrites its ordinary
schedule output:

```bash
OPENBLAS_NUM_THREADS=1 python research/p2_finite_control_20261030/ordinary_control.py
OPENBLAS_NUM_THREADS=1 python research/p2_finite_control_20261030/ordinary_control.py --robust --iterations 2200
OPENBLAS_NUM_THREADS=1 python research/p2_finite_control_20261030/ordinary_control.py --robust --expand
```

## Numerical facts to preserve

- Ordinary nominal: 72 segments, duration 31.4528172603, joint product error
  9.409945e-6; worst admitted corner 0.0553693.
- Ordinary robust: 72 segments, duration 35.1906760553, worst tested corner
  0.01077135; analytic continuous-box bound evaluated numerically 0.01114428.
- Static box: global gain +/-0.005, negative-sign imbalance +/-0.001, and
  always-on X1 data holding coefficient +/-0.001.
- Basic word at duration 512.2121: an actual logical Choi trace-distance
  witness at least 0.44646155 at an admitted corner.
- Raised word at duration 5207.3205: corresponding witness at least 0.93803388.
- Shorter degree-five filter: 23,552 amplitude-scaled segments, same exact
  data term as the 105,984-segment integer-weight version.
- Shorter derived degree-nine filter: 154,533,888 amplitude-scaled segments
  before signed-only compilation and finite-angle repetition. This improves
  the original 33,804,288,000 count but supplies no practical advantage.

## Remaining substantive gap

The information contract is weaker: a logical entangler can be defined
uniformly from source geometry and local dynamics bounds without precise
chirality estimation or microscopic bath retrieval. Efficient execution under
actual waveform asymmetry and data holding is still unproved. The strong
ordinary controller remains the finite winner when its model is supplied;
physical model acquisition, SPAM, qualification, holding, reset duration and
entropy export must be charged wherever the actual task uses them.

The ordinary controller is also entitled to the new coarse promises and to
established ensemble control and dynamically corrected gates. No exclusivity
or priority claim is made for polynomial compensation. The selected primary
context and its access limits are recorded in THEORY.md.
