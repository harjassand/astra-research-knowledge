# Astra scientific computational genesis — 2026-10-15

**Status: mathematical/implementation research capital, not a demonstrated new scientific capability.**

This packet contains a one-cell, real-input study of which finite-time linear battery responses can be bounded from incomplete impedance data. It includes a measurement-derived positive reweighting, continuum interval checks, exact-rational feasible countermodels, and a separate sparse-measurement-interface experiment.

Read **REPORT.md** for the complete argument and scientific limitations, **HANDOFF.md** for the exact restart state, and **sources/provenance.json** before interpreting any result as a physical measurement prediction.

## Reproduce

With Python and the dependencies in requirements.txt installed:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python code/reproduce.py
```

The replay needs no network and does not execute upstream software. Tested environment and measured replay cost are in results/runtime.json. This was run on a container CPU, not on the user's laptop.

Successful replay checks four continuum dual bounds, four exact-rational feasible models, six sparse-protocol continuum duals, and local mathematical unit checks. These are internal checks, not external scientific validation or a Lean proof.

## Scope that must not be lost

The narrow response bounds assume a positive distributed-RC model with series inductance/capacitance and a deterministic 0.1 mOhm error budget at 58 low-frequency samples. The full 70-point spectrum fails a tighter version of this model class. No finite-amplitude pulse prediction was validated. No strongest-incumbent speed or acquisition-cost win was demonstrated. The general positivity/duality strategy has substantial prior art.
