# Acquired partition-free quartic conductance

Useful result: from a complete raw rational polynomial, the consumer acquires
an aligned coupled-quartic family and certifies the FULL isotropic diffusion's
equilibrium capacity/mass. It never computes or samples the fiber partition
function. In the unit parameters the structural multiplicative factor is
**157/125**, independently of dimension, interaction graph or nonnegative
coupling strength. This is not a first-hit-time or angular-mixing result.

A 257-dimensional nonconvex coupled chain is enclosed at roughly
[1.73514e-18,2.19851e-18], using 6,145 exact scalar points and 1,533 raw monomials.
See results.json for the exact rational endpoints, operation diagnostics and
observed timing. Timings are not proof inputs or a controlled benchmark.

## Run locally

Python3 standard library; no package installation or external service:

    python -B compile.py        # raw fixtures -> results.json and dense graph
    python -B check.py          # 2,550 exact author assertions, receiver tests

Programmatic receiving:

    from fractions import Fraction
    from compile import certify, verify
    certificate = certify(raw_polynomial, beta=Fraction(1))
    receipt = verify(raw_polynomial, certificate, beta=Fraction(1))

The verifier pays the entire raw acquisition and exact scalar computation again.
The external task (including budgets) is strictly bound. A prior certificate is
not a free oracle. Optional binary64 displays and operation/timing diagnostics
are not verified proof fields. Exact rational endpoints are always authoritative.

## Files and status

- PROOF.md: full process, partition cancellation, transport capacity bound,
  dimension-free157/125 corollary, graph-insensitivity and exact arithmetic.
- compile.py: strict acquisition, finite-budget construction and exact receiver.
- check.py / check_results.json: author tests including extreme arguments,
  all-term mutations, nested alias rejection, non-square roots, graph changes.
- COSTS_AND_COMPARISONS.md: paid bit/input costs and strong ordinary alternatives.
- EXECUTED_RESULTS.md / results.json: fixed observed executions.
- dense_graph_raw.json / dense_graph_certificate.json: complete 234-term
  raw fixture with a nonfirst acquired axis and coupling 1,000,000.
- sources/: unchanged earlier candidate and independently reviewed theorem/
  sharper corollary. These do NOT independently review this executable.
- DEPENDENCIES.json: source hashes. No imported code dependency.
- FROZEN_SHA256.txt: precise current construction frozen for whole review.

Theoretical candidate and sharper corollary have independent reviews. The
consumer is author-tested; whole executable review is pending. No originality,
general positivity solver, arbitrary-coordinate grammar, noisy-input,
application, MFPT or general computational-hardness claim is made. Accepted
scalar and noncommuting Gaussian packages are preserved separately and unchanged.
