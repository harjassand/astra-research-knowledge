# Independent pilot audit: ordinary hidden-orientation calibration

28 October 2026. **PASS for accounting, implemented simulation law, and same-environment reproducibility.** No author source or output was changed; no bug or correction was required.

## What the author actually ran

`hidden_orientation_ordinary_pilot_20261028.py` fixes one quaternion proportional to (1,2,3,4), twelve parameter cells `p in {0.001,0.01,0.1,1}` and `N in {128,512,2048}`, and 64 runs per cell. Thus there are exactly 768 runs and

    4*64*(128+512+2048)=688128

individually RNG-simulated calibration calls. These are not physical source calls and not aggregate multinomial-count draws. Each call generates an input axis/sign, source flag, measurement axis, and binary outcome. Original JSON retains per-run leakage counts, fitted losses and physicality residuals, not the entire per-call label/outcome stream. The fixed seed and source code permit regeneration of that stream.

The simulated flag is input-independent Bernoulli(p). Conditional output mean is `s R_aj` on flag1 and `s delta_aj` on flag0. This is the declared ordinary qubit channel's Pauli Born law. All calls, including flag0, enter the fixed-N ledger. The fit uses only the measured labels and outcomes; p and R are used by the simulator and scoring, not as fit inputs.

The matrix is the integer signed-count statistic times 9/N. For SVD `M=A diag(sigma) B`, the implemented determinant-corrected `A diag(1,1,det(AB)) B` is the conventional proper-Procrustes solution in exact arithmetic. The pilot executes it in binary64. The evaluated loss is `p ||Rhat-R||_F^2/8`, the unitary qubit loss formula, subject to that finite floating approximation.

## Independent reproduction and checks

The independent replay script first copies the exact author Python bytes to a temporary directory and runs them there, so original files cannot be overwritten. Its output JSON is byte-identical to the retained author JSON in Python 3.12.14 / NumPy 2.3.5.

A second independent pass regenerates all per-call RNG draws in their declared order. It accumulates exactly integer signed statistics, instead of the author's floating `np.add.at`, and verifies every run's leakage count and recomputed loss. It also checks the fixed rotation against a physical SU(2)/Pauli calculation and cross-checks every fitted SO(3) objective against the largest eigenvalue of its quaternion K matrix. All twelve means, mean leakages, theoretical caps and standard errors are recomputed. The denominator eight in the author's standard error is correctly sqrt(64), not a variance or confidence-bound substitution.

Maximum observed diagnostics:

- Loss recomputation difference: `2.78e-17`.
- Floating rotation physicality residual: `4.22e-15`.
- SVD/quaternion objective discrepancy: `5.78e-15`.

The replay JSON records per-run hashes of the regenerated signed-byte record arrays and their integer sufficient statistics. It also records one combined record-stream SHA. These hashes attest the regenerated stream, not historical raw records that the original JSON never retained.

Reviewer work consists of two 688,128-call simulation passes: 1,376,256 regenerated calls total. They repeat the same seeded experiment rather than enlarge its independent statistical sample. The original study count remains 688,128 calls and 768 runs. There are zero hardware/source calls.

## Boundaries of this receipt

The pilot is a binary64 numerical diagnostic, **not** execution of the received finite rational Jacobi compiler. Its rotations are approximately physical at floating precision, not exact rational certificates. Its Monte Carlo means and standard errors do not prove the theorem's expected-risk bound or any high-probability statement. Only one fixed source orientation and the declared finite grid are exercised. No generic noise robustness, hardware practicality, or conventional-comparator advantage follows.

Byte-identical reproducibility is asserted only for the recorded environment; different NumPy/LAPACK/platform versions may choose different degenerate SVD representatives or floating results. The deterministic mathematical ordinary-source theorem is separately received at source SHA `86bedf2c311caa38e8066d99e51b240b056734f67381d86d7d53a11e16ed7502`. This pilot receipt neither replaces that proof nor broadens its interface.
