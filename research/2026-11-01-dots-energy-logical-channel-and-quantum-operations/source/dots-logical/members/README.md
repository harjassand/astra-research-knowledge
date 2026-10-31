# Certified ordinary logical-channel reduction and exact CP acquisition

Local scientific checkpoint — 31 October 2026. This is separate from the
energy/clock/full-source checkpoint. No upload, publication, or external
delivery was performed in preparing it.

## Useful result and exact task

The result is **certified ordinary model reduction**, with an executable
exact-rational completely positive/trace-preserving (CPTP) qubit-channel
acquisition prototype. It is not a claim of historical novelty, a new
integrability result, or a practical quantum speedup.

The source is a **known** zero-field open-chain Glauber model. The final source
and its microscopic path are **discarded**. The retained output is the entire
system, arbitrary reference, and the admitted system-only control records.
The theorem allows arbitrary initial source/system/reference correlations,
not merely a stationary product start. For classical-source/quantum-system
inputs this follows from the complete-norm corrector theorem. For arbitrary
quantum source correlations it applies only to the specific native
direction-merged geometric source and source-diagonal coupling, through the
proved invariant observable algebra; it is not a theorem about arbitrary
quantum lifts of a classical law.

The theorem admits prescribed-time system-only CPTP instruments and uniformly
bounded record-controlled feedback. It does not admit source-conditioned
controls, source interventions/readout, microscopic jump records, or final
source output. The effective map starts with the same reduced system/reference
state, without receiving or estimating the source label.

The **executable fixture is narrower**: a succinct known uniform program
(n, site, positive rational Boltzmann ratio), H0=X, one localized coupling Z,
time one, and **no controls**. It does not learn a physical law or inspect an
unknown length-n data table. The global weak-bond certificate follows from
that known program; local radius acquisition does not magically validate
arbitrary distant input data. The final executable review explicitly checks
the code's |tanh J| condition without incorrectly identifying it with a bound
on |J|.

## What is acquired and paid

The main proof acquires one-/two-spin closure and a complete-norm
finite-rate model error. A local Neumann-tail estimate then bounds the cost
of using a small tridiagonal covariance solve for one localized coupling.
The executable computes that coefficient in exact rational arithmetic,
forms a rational Taylor/scaling-and-squaring approximation to the four-by-four
channel, and performs an explicit Choi repair. Positive exact Hermitian LDL
factors give four algebraic Kraus operators, not normalized postselection.

Stacking those operators supplies an eight-by-two Stinespring isometry.
Ordinary constant-dimensional unitary completion, two-level decomposition,
and finite-precision rotation synthesis are a **paid paper construction**.
The Python prototype does **not** generate or execute quantum gates. Its
optional synthesis error reserve does not mean those gates have been built.
Coefficient acquisition, exact fraction sizes, classical computation,
precision, and any eventual gate synthesis remain real costs.

## Current certificates and complete epsilon accounting

The current allocation is:

| Component | Budget |
|---|---:|
| Finite-rate model error | epsilon/2 |
| Local coefficient truncation | epsilon/4 |
| Exact CP-channel approximation | epsilon/8 |
| Optional actual gate synthesis, reserved but not executed | epsilon/8 |

The represented CP artifact uses the first three terms. Its combined bound
adds the gate reserve. Failed model admission returns ABORT; the method does
not reproduce corrections below its explicit finite-rate error floor.

| Current artifact | Input and local solve | Represented-channel bound | Including gate reserve |
|---|---|---:|---:|
| `effective_qubit_certificate.json` | n=16, site=8, lambda=10^8, epsilon=.01; radius 2, five sites | 0.004918042572 | 0.006168042572 < .01 |
| `effective_billion_spin_certificate.json` | n=10^9, site=5*10^8, lambda=10^12, epsilon=.0001; radius 4, nine sites | 0.00004128120869 | 0.00005378120869 < .0001 |

These numbers summarize exact rational upper bounds in the files. The current
artifacts occupy 158,572 and 389,807 bytes, respectively. The billion-spin
example exercises a succinct uniform-model code path, not a billion-site
experiment, arbitrary-data acquisition, or enumeration of source states.
Recorded acquisition runtimes are environment-dependent observations; this
package does not turn them into universal performance guarantees.

**Historical artifacts are deliberately not current full-record passes.**
`effective_qubit_certificate_1e4.json` is the older n=16, epsilon=.0001
artifact, with epsilon/4 allocated to CP approximation and no explicit gate
reserve. Its exact CP/TP factor remains valid, but the current `verify_record`
rejects it because it is not current deterministic output. Its embedded old
PASS string is historical, not a current full-record verdict.
`check_acquired_cp_channel_pre_gate_reserve.json` is likewise historical.
It does not bind the current certificate bytes or replace the final three-row
diagnostic. See `CERTIFICATE_STATUS.json` for exact hashes and meanings.

## Proofs, receipts, and evidence limits

Read these together:

1. `effective_logical_channel_20261031/COMMUTATOR_CONTROLLED_EFFECTIVE_CHANNEL.md`
   — final main source `4d6d102c...`, with
   `EFFECTIVE_LOGICAL_CHANNEL_INDEPENDENT_REVIEW.md`, `f9261c89...`.
2. `EXACT_RATIONAL_CP_ACQUISITION.md` — final CP proof `a9a8e801...`,
   `acquire_effective_qubit.py`, `c6d8134e...`, and
   `EFFECTIVE_QUBIT_CODE_INDEPENDENT_REVIEW.md`, `80e44e9f...`.
   The latter is the final executable receipt, received before this package
   was created. It binds the current code, proof, tests, independent checks,
   and two current saved certificates. The real bool/float-alias verifier
   defect and its final strict-type repair are preserved in that receipt.
3. The exact native diagonal-algebra lemmas and scoped receipts retained under
   `native_lyapunov_source_20261031` and `local_gibbs_lift_20261031`.
   Their use is limited to the stated generator/algebra identity. This package
   does not receive or repackage the entire earlier full-source simulator;
   see `DEPENDENCIES.md`.

`REVIEW_BINDINGS.json` indexes existing exact-source receipts. Inclusion does
not independently review every script, diagnostic, historical artifact, or
packaging file. Immutable source headings may still say candidate; the final
hash-bound receipts govern only their explicitly received versions/scopes.

The final `check_acquired_cp_channel.py` and JSON retain three comparisons:
both current artifacts and the historical n=16/.0001 artifact. Exact Choi,
TP, positive LDL, factor reconstruction, and **direct Kraus TP** are checked
with rational algebra. Floating SciPy Choi comparisons are diagnostics, not
certified numerical diamond bounds; the rigorous allowance comes from the
rational proof. A diagnostic field named `numerical_diamond_upper` must be
read with that numerical qualification. Other small dense CQ, native quantum,
and local-covariance checks retain their stated diagnostic scope.

`verify_channel` checks only exact CP/TP representation. `verify_record`
additionally recomputes the entire declared known-program record with strict
type-and-value comparison. Neither establishes that a physical black box
obeys the input model. An altered source/error assertion can pass the former
and fail the latter; this difference is intentional.

The main proof cites established ordinary Poisson-corrector, effective
Lindblad, and adiabatic-elimination literature. Those equally informed
ordinary methods are the constructive approach used here, not weak rivals
claimed beaten by a new quantum method.

## Integrity and reproduction

All 25 scientific files are unchanged byte copies. `ALLOWLIST.json` lists
their provenance roles. `FILE_LIST.txt` lists every ZIP member.
`MANIFEST.json` hashes all payloads except itself and `SHA256SUMS.txt`;
`SHA256SUMS.txt` additionally hashes the manifest and excludes only itself.
Hashes establish integrity, not scientific independence or signatures.

From an extracted archive root:

    python3 -B verify_checkpoint.py
    python3 -B check_checkpoint.py

The second command preserves archived outputs: it reruns 83 author assertions
and 93 independent checks in memory, verifies current/historical record
semantics, and runs the four separate diagnostic scripts in a disposable copy.
`CHECKPOINT_VALIDATION.json` records the packaging rerun. This is reproduction,
not a new independent mathematical review. Original benchmark timings and
diagnostics are preserved unchanged; floats and timings may differ by platform.

Exact JSON integers must be arbitrary-precision integers, **not IEEE doubles**.
Some exceed Python's default 4,300-digit parsing limit. The supplied checker
and acquisition module explicitly support these known finite certificates;
custom Python readers can call `sys.set_int_max_str_digits(0)` before parsing.
This is a per-process parser setting, not a system permission change. Avoid
applying unrestricted parsing indiscriminately to untrusted huge inputs.

Environment used: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, mpmath 1.3.0,
SymPy 1.14.0. No software installation was performed. Integrity verification
uses only the standard library. Original diagnostic entry points can rewrite
their adjacent JSONs; run them only in disposable extracted copies.

Caches, admin/private files, unrelated work, old archives, and the unreviewed
`quantum_effective_channel` candidate are excluded. No source files or previous
archives were edited or overwritten. This artifact is local only.
