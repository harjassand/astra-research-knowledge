SPARSE AUTONOMOUS PROCESSOR — RESEARCH PACKAGE
5 November 2026

Start with report.txt. It contains the strongest new statements, proofs,
assumptions, costs, limitations, existing-method comparison and sources.
accepted_reusable_report.tex is the full preceding construction imported
as machinery, with its original scope unchanged.

Finite implementations:
  python sparse_adapter.py --self-test
  python framed_transfer.py --self-test
Use --help for the available arguments.
NumPy is required; recorded checks used NumPy 2.3.5.

finite_checks.json and framed_checks.json contain executed results.
These are finite adapter and transaction checks, not physical-code or
threshold simulations. Logical protected controllers in the transaction
harness are charged analytically by the compiler theorem.

Main new exponents, r=alpha-d>1, fixed small positive intensity:
  installed registers: T^(1/r+o(1))
  diameter:            T^(1/r+o(1))
  all-register-time:   T^(1+1/r+o(1))
The register and work exponents improve the preceding dense construction;
the diameter exponent was already attained. Matching lower exponents
apply to static bounded-range register devices with all storage counted.

Scope: sparse static patterned hardware, fixed synchronous local channel,
known noisy controller initialization, compact raw unknown input,
local raw final delivery, fixed nontrivial error. No filled-lattice area,
asynchronous, translation-invariant, thermal, or energy-optimal claim.

The restart theorem concerns a DIFFERENT stronger initialization contract:
a fixed prescribed finite seed must work from EVERY outside mutable state.
It forces linear capacity in delay. It does not invalidate prepared reuse.

The new results are research derivations based on imported accepted
machinery; primary citations are not claims of prior publication of the
new theorems. The code is a finite implementation of the new operations,
not a complete physical concatenated-code compiler.
