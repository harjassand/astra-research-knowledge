# Stronger partition-free conductance: parallel channels

**Status: constructed, source-frozen and author-tested; independent whole review
pending.** The earlier radial consumer remains unchanged and separately frozen.

For the same acquired raw coupled-quartic family, this continuation certifies

    k_free / sqrt((16+23*kappa)/(14*(1+kappa))) <= k_full <= k_free.

The structural factor is independent of beta, d_min, fiber dimension and angular
interaction graph/strength. At kappa=1 it is sqrt(39/28), about 1.1802. For every
positive kappa it is below 13/10. The target remains full isotropic equilibrium
capacity/mass, not an arbitrary-start passage time, angular relaxation or an
exact projected Markov process.

The mechanism is stronger than the radial certificate: integrate a one-dimensional
weighted Cauchy bound separately on fixed fibers, use homogeneous energy scaling,
then Gamma/Jensen and a physical slab contraction. No Gamma integral, partition
function, current field or fiber sampler is actually evaluated by the program.

A raw 257D chain is received in
[1.846591188057168e-18,2.198502327566721e-18], including <1% quadrature width.
The 1,533 monomials and 6,145 exact scalar points are paid. Timing is diagnostic.

## Run

Python standard library only. The relative sibling directory must be present:

    python -B receive_parallel.py
    python -B check_receiver.py
    python -B check_contraction.py

receive_parallel.py checks the SHA256 of ../acquired_quartic_consumer/compile.py
before importing it. That frozen module reacquires all input structure and
computes the exact scalar integrals with finite budgets. The new module adds one
outward integer square root, changes the structural theorem/method/schema, and
recomputes the lower endpoint. Its verifier repeats the entire construction and
strictly binds all task/acquisition/proof fields and exact endpoints.

The original scalar module also calculates its old radial factor as an unused
intermediate; this cost is paid. Consequently the wrapper inherits that module's
incomplete budget/serialization behavior, even if a standalone parallel-only
implementation could succeed. Independence of the mathematical kinetic factor
is NOT a claim of zero input-bit or acquisition cost when d_min or beta changes.

## Source-bound files

- PARALLEL_CHANNEL_CANDIDATE.md: complete separate proof, SHA05eee3b8... .
- receive_parallel.py / check_receiver.py / receiver_checks.json: new receiver;
  77 additional author assertions. The inherited 2,550 tests remain separate.
- check_contraction.py / contraction_checks.json: 62,730 rational checks of the
  pointwise contraction, not an independent proof or a large model benchmark.
- parallel_results.json: exact endpoints and actual executions for m=2–256.
- SOURCES_AND_COMPARISONS.md: genuine prior fixed-channel/entropic-capacity work,
  ordinary primitives, and what is newly derived versus historically unresolved.
- ASYMPTOTIC_CONSEQUENCE_CANDIDATE.md: separately unreviewed qualitative limit;
  the finite executable does not silently claim its fixed 1% interval is exact.
- DEPENDENCIES.json: exact inherited source/process/theorem provenance.
- FROZEN_SHA256.txt: this current construction, ready for whole review.

A full accepted release additionally needs the underlying quartic whole audit
and this parallel theorem/receiver audit. No publication or upload was performed.
