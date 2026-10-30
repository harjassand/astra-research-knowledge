# Astra P2 — causal logical recovery

Working checkpoint: 30 October 2026, Brisbane. Existing root role only.

## Result and status

THEORY.md is the complete working proof and resource account. It develops
necessary-and-sufficient causal CP constraints for committed, uniformly
heralded quantum recovery from a known fixed source's coherent outputs.
The logical-subsystem version allows an arbitrary physical gauge process;
full microscopic-state retrieval is a special case.

The explicit noncommuting qubit source has incompatible separately optimal
early and late full-state extraction. An exact rational certificate proves
the gap. A second exact rational certificate puts the optimum mean number of
source calls for complete unknown-qubit retrieval in (2.83885, 2.83890).

A stronger ordinary mechanism solves the actual logical-damage fixture in
one source call: two native syndrome measurements and a conditional Pauli,
with no coherent history archive. A coherent version and permitted native
replay were also constructed. The original dirty register is retained.
These wins are part of the result; the full-state receiver does not beat them
on that weaker logical task.

All new results are root derivations and root-run checks. There is no new
independent review or priority determination. The old accepted foundations,
reported bridge review, attracting-controller result and their negative cases
retain their earlier scopes. No device threshold or practical computing
advantage has been acquired.

## Files

| File | Purpose |
| --- | --- |
| THEORY.md | Definitions, proofs, source/access contract, whole-task costs, negatives and prior art |
| causal_receiver.py | Small finite-horizon primal/dual SDP and constant-rank channel representation |
| causal_plans.json | Saved finite plan proposals |
| exact_certificate.py / exact_certificate.json | Exact rational two-deadline obstruction |
| check_information_rescue.py / physical_checks.json | Full physical isometries, complete entangled-input checks and dirty-reuse negatives; JSON includes actual control matrices |
| check_logical_contract.py / logical_contract_checks.json | Stronger one-call logical-only alternatives and syndrome-fault negative |
| solve_waiting.py / waiting_plans.json | Numerical proposals for the complete expected-call objective |
| certify_waiting.py / waiting_certificate.json | Exact rational prefix/dual certificates plus a physical geometric tail |
| explore_rescue.py | Shared linear algebra and original exploratory search; the patched random search was not rerun |

## Reproduction

The finite checks use Python 3 and NumPy. The exact certificate verifiers use
the standard library and saved candidate data. Run from this directory:

```bash
python exact_certificate.py
python certify_waiting.py
python check_logical_contract.py
python check_information_rescue.py
```

To propose new numerical plans, use causal_receiver.py or solve_waiting.py;
then run the corresponding exact verifier. The solver is a research log-det
implementation, not a general SDP package. Its numerical primal/dual gaps
are explicit. The exact certificate does not trust optimizer convergence.

Full unitary completion on unused inputs affects the physical dirty fault
case. The currently saved physical matrices specify the current test. A prior
completion's distinct negative is retained as a historical observation in
physical_checks.json and THEORY.md. A clean-sector map does not specify a
physical dirty-input extension.

## Scope that must survive continuation

- Source optimality assumes a fixed upstream process, full declared returning
  memory, coherent output access, and no source-changing feedback. Native
  replay and other permitted feedback remain stronger ordinary competitors.
- A committed early output may be used by the recipient. Tentative coherent
  extraction can be undone when the output is unused; on-demand recovery at
  one selected deadline is a different information contract.
- A small archive does not supply reliable compression gates or holding.
  Actual source-dilation acquisition, calibration, initialization, flags,
  timing, transfers, finite reset duration and entropy export remain costs.
- Logical release can precede apparatus readiness only if the real released
  system is excluded from later regeneration couplings. A returning bath or
  dirty recycled register remains a fault at its actual location.
- The earlier kappa=p(1-q)^3 apparatus-attraction bound cannot be promoted to
  a full quantum-retrieval Doeblin component without an additional proof.
- Positive physical CP minorants must not be replaced by a Hermitian
  relaxation. Finite-time amplitude damping remains a sharp exact-extraction
  negative despite asymptotic approximate recovery.
- Only this new directory is available. The old directories are absent; the
  earlier interrupted second save remains unconfirmed. No old archive was
  reconstructed, and no transfer or denied-route retry was performed.

The live physical gap is a native implementation whose acquisition and
error budget make logical release useful, including later module reuse.
The current theory identifies the correct logical information contract and
the optimal stopping constraints; it does not invent a reliable supplier.
