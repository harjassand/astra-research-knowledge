# CRAY — Compressed cooperative transport certificates

This bundle contains the constructions, exact scalar calculations and finite tests described in `cray_compressed_transport_report.md`.

## Main result and warning

A balanced hard-KA path grammar supplies a port-independent source–sink module and a certified energy bound without a full configuration graph. At particle density 4/5, its explicit nonlocal-lifted lower bound is **10^(-11593)**. This is much too weak to be a useful transport prediction. It does not improve known high-density asymptotics or establish independent publication priority.

The useful preserved objects are the conserved-multiplicity cylinder current, exact balanced-strip density and scalar moment recurrence, recursive gate, legal port-swap grammar, and complete congestion accounting.

## Reproduce

Python 3.10+ is recommended. Scalar certificate calculations use the standard library. The finite path tests require NumPy (tested with Python 3.13.5, NumPy 2.3.5).

```sh
python balanced_certificate.py
python reproduce.py
```

The first command computes the final high-density endpoint from outward-rounded rational recurrences. It never enumerates configurations or expands a large microscopic path.

The second regenerates both the deterministic baseline and balanced certificates, exact small-instance tests, symbolic support tests, and diagnostic two-port words. Random inputs are tests only; no sampled quantities enter the bounds.

To measure complete-process resources:

```sh
/usr/bin/time -v python reproduce.py
```

The supplied run took 6.66 seconds wall time with about 106.5 MiB peak resident memory. This is regeneration time, not research time or an accurate dense-transport simulation time.

## File map

- `cray_compressed_transport_report.md`: mathematical definitions, proofs, limitations and references.
- `cylinder_flow.py`: cylinder indicators, exact intersection moments and explicit path compilation.
- `invariant_pivot.py`: direct 8m-10-term current, invariant-sector division and exact energy formula.
- `frame_grammar.py`: deterministic seed/growth gate and first-vacancy path baseline.
- `balanced_grammar.py`: balanced cyclic-pivot paths; sampled histories carry exact probabilities.
- `probability_certificate.py`: recursive gate and deterministic history-counting baseline.
- `balanced_certificate.py`: scalar strip moments, full compressed energy bound and exact final exponent.
- `test_research.py`, `test_balanced.py`: finite diagnostics and corruption checks.
- `reproduce.py`: regeneration entry point.
- JSON and text logs: computed outputs and measured resources.
- `prior_nonlocal_transport_report.md`: prior internal completion theorem used by the present construction; it is not independent validation.

## Scope of verification

Finite tests do not replace review of the general mathematical proofs. No complete large configuration graph is checked. The theorem-based certificate verifies its scalar inequalities using exact integer/rational arithmetic; its validity also depends on the analytic source, density and nonlocal-lifting arguments in the report.

An exact full-current pointwise evaluator is not claimed to be affordable. A side-4096 microscopic word can have trillions of instructions; no such word was executed. The compact certificate is an output-specific computation, not a fast microscopic simulation.
