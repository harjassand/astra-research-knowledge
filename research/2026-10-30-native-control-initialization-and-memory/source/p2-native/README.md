# P2 working result: useful gates with a dirty mediator

2026-10-30 UTC. **Root working derivations and root exact/numerical checks. No independent review or priority claim.** Earlier accepted work and reported review scopes remain distinct.

The useful task is a two-qubit entangling unitary. The complete memory stays in the process, with its drift running forward. The new construction does not recover a bath history or purify the mediator.

Read [THEORY.md](THEORY.md) for the physical contract, proofs, failures, acquisition/resource accounting, and primary-source comparison.

## Main completed results

- A 96-segment signed-native-control word produces a clean cubic entangling Hamiltonian plus memory-only evolution. It uses an uninitialized spin mediator coupled to a continuing environment.
- A local commutator-regularity bound avoids charging the norm of the entire bath Hamiltonian. Its regularity premises are explicit.
- A native sign projection and forward-time composition raise the useful accuracy order without reversing the bath. An integer-clock version replaces the separate irrational timing ratio with repetitions and doubled intervals.
- A retained-sector example has an exact fifth-order conditional logical phase. Its lower bound is on actual logical channels after memory is discarded. Ordinary common-angle calibration cannot remove it. The raised word cancels this term without identifying the sector.
- In the original easier fixture, ordinary logical-angle retuning wins. That successful alternative and its acquisition limitations are preserved at full strength.
- Coplanar mediator couplings have an antiunitary obstruction in the stated access class. This is a separate genuine obstruction, not an interpretation of a conservative error bill.

## Runnable checks

Python 3 with NumPy and SciPy suffices. Exact arithmetic uses the Python standard library. Run from the shared workspace, or use the scripts' absolute paths. Each script writes results beside itself.

| Script | Saved result | Scope |
|---|---|---|
| `explore_word.py` | `word_series.json` | Exact rational noncommutative series through degree four; failed ordering retained |
| `check_bus.py` | `bus_checks.json` | Complete 16-dimensional memory evolution; actual sign, holding and outer-offset negatives; benign inner-offset correction |
| `harmonic_series.py` | `harmonic_series.json` | Exact rational Fourier/Dyson calculation; failed six-tone guess and qualified nine-tone replacement |
| `check_harmonic.py` | `harmonic_checks.json` | Same-memory harmonic gate; numerical integration convergence and resource/access limits |
| `check_order_raising.py` | `order_raising_certificate.json`, `order_raising_checks.json` | Exact abstract identities and full-memory numerical execution |
| `exact_sector_check.py` | `sector_certificate.json`, `word_degree5.json` | Exact rational coefficient of the retained-sector logical phase |
| `check_comparators.py` | `comparator_checks.json` | Ordinary angle fitting, actual duration retuning from an exactly estimated signal, two-sector logical-channel witness, and seven-pulse calibrated special case |
| `check_integer_clock.py` | `integer_clock_checks.json` | Native integer-clock composition on the same retained-sector fixture |
| `check_coplanarity.py` | `coplanarity_checks.json` | Generator symmetry and actual reduced-channel checks for the coplanar obstruction |

For example:

```bash
python research/p2_algebraic_bus_20261030/explore_word.py
python research/p2_algebraic_bus_20261030/exact_sector_check.py
python research/p2_algebraic_bus_20261030/check_order_raising.py
python research/p2_algebraic_bus_20261030/check_comparators.py
python research/p2_algebraic_bus_20261030/check_integer_clock.py
```

The smooth-waveform control-action quadrature may report a roundoff warning at its requested tolerance; that optional integral is separate from the Schrödinger integration and its recorded refinement check. Numerical results are not interval certificates. A polar-factor memory gauge is a chosen comparison unitary, not an acquired reset or a certified optimum in operator norm.

## Important outcome limits

Signed stable native couplings, their physical interface algebra, timing, and bounded local drift regularity are premises. No unavailable physical supplier is inferred from a scalar calibration. Data preparation, measurement, holding, controller errors, finite-shot acquisition and any entropy outlet must be supplied and charged in an actual device.

The order-raising result improves an asymptotic bound. The long native words have substantial costs and nonmonotone finite-duration behavior. No practical computing advantage, noisy-control threshold, or globally optimal ordinary comparison has been established.

The prior native syndrome-recovery solution remains preferred for its original logical-repair task. Logical release remains distinct from apparatus readiness. The previous dirty-register, passive-inverse, bath-return and concurrency failures are unchanged.

These are ordinary new local proof/code files. No external export, transfer, helper, model change, independent audit, or Capital intake is claimed.
