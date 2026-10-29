# Runnable work and its exact evidentiary scope

29 October 2026. These checks support normalization and finite generator
algebra. The analytic receiving proofs, actual reviews and physical
premises remain separate.

## Finite-time tilted-generator calculation

Run from this directory:

```bash
python3 check_rare_transport.py
```

This writes `RARE_TRANSPORT_CHECK.json`. The executed environment had
NumPy 2.3.5 and SciPy 1.17.0. The code uses sparse matrix exponentials,
not Monte Carlo samples. It computes N^-1 log E exp(N lambda Q_N) for
N=4 and 6, two nonlocal frozen amplitude tables, lambda=-3,+3, physical
time N^2 times 0.3, and independent sign rates 0,0.5,2,8,32. Initial
occupancy is alternating half filling and all retained signs are +1.

| N | Joint states | Largest absolute error from exact finite-N SSEP, frozen signs | Largest error at sign rate 32 |
|---|---:|---:|---:|
| 4 | 96 | 0.0314653569081 | 0.00273639971759 |
| 6 | 1280 | 0.104716687519 | 0.00356714426993 |

These are errors in the per-site log MGF, maximized over both frozen
contexts and both displayed multipliers. They are floating-point
population values. The rate dependence need not be monotone for each
finite context and initial state.

The exact finite-N SSEP comparator at lambda=3 is 0.489897454002 for
N=4 and 0.430485889279 for N=6. The large-N formula is 0.3375.
Their sizable finite-size difference is retained deliberately: the
fixture does not validate an asymptotic exponent at these small N.
The appropriate finite-bath comparison is the exact finite-N model.

The executable also checks zero-tilt row sums, detailed balance of
the joint generator, and exact reduction to the ordinary finite-N
SSEP MGF when modulation is zero. The largest observed row-sum
residual was 6.76e-14, symmetry residual zero, and zero-modulation
reduction discrepancy below 1.5e-15. A tilted generator must retain
the original escape diagonal; replacing it with the tilted escape
would compute a different object and force an incorrect MGF.

## Exact conserving-ring identities

```bash
python3 check_common_clock_identities.py
```

This writes `COMMON_CLOCK_IDENTITIES.json`. Python rational arithmetic
checks all occupancy/common-sign states for N=4,6,8 at c=2/3 and
alpha=3/5, and separately at alpha=1. It verifies wrap-bond parity,
own-swap detailed balance, total exit intensity, zero corrected-current
drift, its exact quadratic variation, and the native/clock increments
of the pathwise current decomposition. At alpha=1 every permitted
native event has zero corrected-current increment.

The six enumerations cover 1,344 joint state cases in total. All
listed equalities are exact at those rational parameters. Enumeration
does not prove the all-N theorem; the saved analytic identities do.
No experimental samples, confidence intervals or apparatus errors
were inferred from either executable.

## Review versus experiment

The existing two complementary roles read actual proof files and
preserved exact reviewed versions with hashes. The occupation/tilted
hydrodynamic receiver is explicitly reconstructed. The substantive
corrections concern initial-profile uniformity and the complete
conditional future generator; three missing displayed plus signs
were also repaired in the receiver, with its earlier copy retained.

The construction has no acquired end-to-end finite-N precision budget,
fabricated apparatus, energy comparison or demonstrated practical
speedup. It is a collection of proved population mathematical results,
internal constructive challenges and reproducible finite-model checks.
