# Fresh-feed causal test for pulsed Pd hydrogenation

Date: 2026-10-16. Source pin supplied by the parent: `3dde9ce74d829a93388e64032d27351b36dd2221`.

**Decision: REDESIGN the physical-capability claim; retain one bounded laboratory acquisition test. No new physical operation has been demonstrated.**

The strongest obtainable addition is to put the electrical intervention **before a fresh carbon label is admitted**, then recover the complete fate of that tagged feed during an identical read and chase. A difference in new-feed chemical fate can rule out direct release of old product and downstream sampling delay. It does not identify electronic catalyst memory: reactive gas transport, hydrogen inventory, adsorbate blocking, and membrane state can change later turnovers too.

The supplied aggregates have no new-feed transient, complete current waveform, acquired reservoir bound, local exposure record, or calibrated molar-flow trace. They therefore cannot execute this test. All numerical examples here are arithmetic from supplied aggregates or exact synthetic countermodels, explicitly separated.

Read:

- [CAUSAL_IDENTIFICATION.md](CAUSAL_IDENTIFICATION.md): exact identification statement, finite-record bounds, and nonidentification results.
- [EXPERIMENT.md](EXPERIMENT.md): minimum paired intervention, source-resolved extension, electrical/material requirements, and stop rules.
- [COMPARATORS.md](COMPARATORS.md): dynamic catalysis, SSITKA, current process comparators, and the complete work boundary.
- [SOURCES.json](SOURCES.json): live primary literature and access limits.
- [CLAIM_LEDGER.json](CLAIM_LEDGER.json): evidence and claim status.
- [countermodels.py](countermodels.py) and [countermodels.json](countermodels.json): replayable exact fixtures, not measured Pd kinetics.

Run `python3 countermodels.py` from this directory. It reads the supplied `results.json` without modifying it and writes only this directory's `countermodels.json`.

The specific design is a causal combination of established isotope transients, randomized pulse/hold controls, complete mass balance, and common-read preparation. Historical novelty of that combination is **UNKNOWN**. Generic isotope source attribution and programmable catalytic selectivity are already prior art. The original dynamic Pd result belongs to Xu and coauthors.

No laboratory work, gas handling, instrument control, external communication, source-repository modification, or Git mutation was performed.
