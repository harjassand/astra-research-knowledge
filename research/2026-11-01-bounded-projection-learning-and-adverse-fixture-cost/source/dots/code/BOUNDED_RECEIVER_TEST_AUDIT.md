# Bounded-projection receiver test audit

2026-11-01. Independent implementation test pass, not a proof of historical novelty, practicality, a physical experiment, or the general theorem.

Command: `python scalar_return_acquisition_20261101/test_bounded_projection_receiver.py`

All seven tests pass; captured output is `TEST_BOUNDED_PROJECTION_OUTPUT.txt`.

- Rational selfadjoint noncommuting rank-two and rank-three contraction fixtures force dictionary growth to two and three actual descriptors. Length-four tasks are included because corrected scalar outputs can answer shorter tasks without completing the hidden linear span.
- A rational rotation with tangent parameter 10^-12 and its supplied inverse adjoint exercises a reachable near-collinear Gram determinant about 4e-24. The online learner retains two descriptors, not necessarily that near-duplicate pair; `bounded_projection_stress.py` separately tests an imposed dictionary containing the pair.
- Every emulated scalar return is checked against a hidden oracle confined to test code. Means lie on the specified binary-sample grid and within the requested error allowance, but **no such samples were drawn**.
- Every accepted optimizer result is independently checked using only its scalar-data quadratic: coefficients are dyadic and feasible, the returned Frank–Wolfe gap equals an independently recomputed exact gap, and it satisfies the required tolerance.
- Pair/precision jobs are unique; denominators are common within an epoch; total confidence allocation is bounded by beta; descriptors remain unique; repeated and genuinely new tasks reuse retained data without additional source jobs.
- Actual binary calibration is refused before any source callback when its theoretical budget exceeds ten reports. Bad PSD data, unexpected source exceptions and zero-budget generic optimizer fallback both latch terminal failure, with no reacquisition on subsequent requests.

The end-to-end tests execute the capped small active-face proposal accelerator, accepted only after rounded-grid feasibility/gap verification. They do not execute the generic rounded Frank–Wolfe loop. The zero-budget test verifies that its potentially astronomical proof cap is explicitly refused rather than silently executed or omitted.

Near-collinear rotation fixture: 27 validated unsampled means; theoretical unexecuted episode budget 1942191413052361932800000.
Rank-two reflection fixture: 18 validated unsampled means; theoretical unexecuted episode budget 918755082763113594880000.
Rank-three fixture: 66 validated unsampled means; theoretical unexecuted episode budget 108057086697066557603840000.

Physical episodes executed: **zero**. These budgets are not empirical sample counts or practical performance claims.

Source inspection found no unresolved implementation correctness blocker in the tested version. This finite audit does not establish a general physical-interface assumption, hidden-state model validity, optimality or literature novelty.
