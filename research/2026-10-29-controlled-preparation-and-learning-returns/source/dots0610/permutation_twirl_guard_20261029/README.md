# Physical permutation guard bridge, 2026-10-29

Governing proof: PHYSICAL_PERMUTATION_TWIRL_v3.md. Version 2 clarified the decoder-record
output boundary and canonical-frame gate order. Version 3 corrects the control
comparison: endpoint logical Pauli gates are cheap when encoding/decoding are
already paid; physical permutations are not a generic control-cost saving.
At creation this is an author construction awaiting a final independent receipt.
Read any independent review receipt at its actual scope, not as historical
novelty or hardware validation.

What changed:
- Actual physical permutation/inverse-permutation control on a singlet code
  yields an exact good/bad CP decomposition even with retained quantum memory
  and physical leakage. A private averaged key is essential.
- The good branch is logical identity times a memory operation. The bad branch
  has both input-independent probability and a closed memory marginal.
- A fixed power-of-two subcode may move through its physical permutation orbit.
  It need not be invariant. The matching-test coefficient becomes (n+2)/(n-1),
  removing the old d/K penalty through a changed physical code orbit. This is
  NOT a generic compilation advantage: endpoint logical Pauli gates cost only
  O(k) single-qubit operations, while physical permutations add SWAPs and key bits.
- An outer code correcting arbitrary t-block quantum errors can use this
  decomposition; it is not a stochastic-Pauli-only assertion.

The exact actual memory filter excludes new outer-decoder syndrome/trash
records. Keeping those records calls for the weaker dummy-input simulator.
Full source/control separation, calibration, secret random keys, encoder,
decoder and endpoint storage remain required. No positive yield for arbitrary
noise, hardware advantage, or historical priority is established.

Checks: check_joint_twirl_v1.py, output .json. Twenty arbitrary physical n=4
joint channels with two-dimensional input and three-dimensional output memory;
all 24 permutations. Complete CP/Choi decomposition, full memory-superoperator
closure on matrix units, and correlated carrier-memory inputs were checked.
Maximum Choi split residual 1.53e-15; maximum closure residual 2.09e-16.
These are floating-point diagnostics, not physical observations.

Counterexamples retained:
- Keeping the random key leaves a half-Choi distance 0.0998334 at theta=0.1,
  versus 0.00996671 after key retirement.
- If the input irrep occurs twice in the output, a coherent-copy isometry has
  half-distance 1/sqrt(2), despite raw infidelity 1/2. Multiplicity one matters.

Run: OPENBLAS_NUM_THREADS=1 python3 check_joint_twirl_v1.py
Dependencies: Python 3, NumPy, SciPy. No external data needed.
The matching-survival theorem is in ../matching_survival_20261029/.
Independent n=6 proper-subcode physical examples are in
../permutation_orbit_instance_20261029/. The separate outer-code construction
and sequential stopping proof must be read before claiming their complete
end-to-end instantiation. A proof of the bridge is not a new physical run.

## Completed internal review and control compiler
At 2026-10-29 04:25 UTC, the independent reviewer accepted governing v3 at its
scoped mathematical claims. Receipt:
../permutation_twirl_audit_20261029/THEOREM_REVIEW_RECEIPT_v3.json
with substantive INDEPENDENT_THEOREM_REVIEW_v2.md and RESOURCE_CORRECTION_v3.md.
This supersedes the earlier pending-review status, not any scope qualification.

compile_permutation_controls_v1.py/.json supplies explicit bounded fair-bit
sampling logic, unrestricted and line routing, inverse route, and three-CNOT
SWAP identity checks. All 46,232 permutations through n=8 and 400 sampled
routes at n=16,64,256,1024 pass. The Python random seed only provides numerical
reproducibility; certified private physical randomness remains an interface.

## Required prior-art correction
Read PRIOR_ART_CORRECTION_v4.md. Graydon–Skanes-Norman–Wallman,
arXiv:2201.07156, Theorems1&3 already establish generic unitary1design
stochasticization and the memoryless half-diamond/process-infidelity identity.
Our earlier covariance reference was less direct. No generic invention claim
survives this attribution correction; the explicit physical/memory/code-orbit
transfer retains only its stated scoped claims, with priority unresolved.
