# Completed bounded-projection online receiver

`bounded_projection_receiver.py` is separate from, and does not modify, the original `receiver.py`. It imports only exact arithmetic helpers, exception types and the genuine binary adapter from that file. The new mathematical model does not use the old inverse-Gram operation matrices.

## Implemented contract

```python
r = BoundedProjectionReceiver(
    alphabet=('a','b'), H=4, epsilon=Fraction(1,50),
    delta=Fraction(1,100), adjoints={'a':'a','b':'b'},
    adapter=source_adapter, max_fw_iterations=10000)
answer = r.request(('b','a','b'))
```

The source adapter provides only scalar pair means; no hidden features enter this receiver. The primary genuine `BinaryMeanAdapter` executes the calibrated fixed number of +/-1 report callbacks, with pre-job total-episode refusal. Physical preparation, conditional unbiasedness, actual adjoint identities and contraction premises remain external requirements, not properties the receiver can infer from visible fits.

The receiver implements the audited binary schedule exactly: beta=delta/(W+1)^64; Jmax=(E+1)(W1+1)^2; per-job allocation beta/Jmax; common n_b per precision epoch; canonical unordered-pair cache keyed by b; alpha=lambda/[128(b+4)b²]. Only needed pairs are acquired, not the entire descriptor universe.

It constructs Ghat/Khat/Hhat, checks PSD of Ghat+m alpha I exactly, performs bounded-coefficient projected forward and adjoint-reverse rollouts, evaluates the corrected scalar prediction and outward residual-product certificate, and scans only requested prefixes after rejection. A prefix is retained only with convex-distance lower bound >lambda/2. Retained descriptors are unique and horizon-bounded. Failed calibration, source exceptions, PSD guards, negative residual upper radicands, missing novel witnesses, optimizer caps and budget refusals permanently latch acquisition failure. Later requests cannot restart it.

## Optimizer and honest execution limits

Each QP uses the exact FW-gap stopping condition. The generic optimizer is the proved fixed-step, toward-zero dyadic rounded-FW algorithm, with its explicitly computed iteration cap. The configured `max_fw_iterations` is a PER-SOLVE execution budget: if the proof cap exceeds that budget and no already-certified solution is available, the receiver refuses BEFORE any fallback steps. `None` explicitly permits the full finite theoretical cap; tests do not use it to launch astronomical work.

For m<=4 only, a constant-size active-face enumeration proposes a solution from the ACQUIRED scalar matrices. It accesses no hidden vector. The candidate is rounded toward zero onto the same proved dyadic grid and independently accepted only when its exact FW gap is <=delta. Singular proposal systems are skipped. If the proposal fails, the rounded fallback or explicit budget refusal is used. This ordinary small-instance optimization accelerator is not claimed as a general polynomial solver; its dimension is hard-capped. Starting fallback from its feasible rounded candidate is sound because the objective-range bound is global.

`acquisition` and `deployment` separately count source jobs, theoretical required episodes, actually returned reports/attempts, descriptor controls, dictionary changes, rejected versus accepted optimizer work, proposals, FW checks, rounded steps and coefficient bitheight. The enormous theoretical FW caps are recorded separately from executed steps. `job_log` is finite acquisition data; `optimizer_log` retains only the most recent256 diagnostics so future deployment does not accumulate an unbounded per-solve log.

## Tests and what they establish

Run `python scalar_return_acquisition_20261101/test_bounded_projection_receiver.py`.

The end-to-end receiving fixtures use explicitly UNSAMPLED validated-mean emulators. Every returned mean is checked against an exact hidden oracle only inside the test, placed on an attainable n-shot binary grid, and verified within alpha. No claim is made that the theoretical n reports were drawn. Tests cover noncommuting rank2/rank3 systems, expansions and new-task source-free reuse, cache/confidence/common-denominator properties, unique retention, exact feasible dyadic solutions and independently recomputed FW gaps, and permanent source/PSD/optimizer-budget failure latches. Actual results are saved in `TEST_BOUNDED_PROJECTION_OUTPUT.txt`.

The rank2 fixture retains2 descriptors from18 validated emulated means; rank3 retains3 from66 means. The conservative theoretical unexecuted budgets are respectively about9.19e23 and1.08e26 one-bit episodes. Those are NOT experimental data or executed sampling. A real binary-adapter end-to-end test refuses before the first report because the required job is unaffordable. The accelerated QP proposals are the executed receiving-test solver path; no enormous generic FW fallback is run. A separate exact-rational `rounded_fw_stress.py` previously verified927 executed rounded steps and all descent/grid invariants on a small synthetic optimizer problem, not a physical source.

The older fixed-dictionary `bounded_projection_stress.py` diagnostic additionally covers a nearly collinear physical dictionary and rotation, with Gram determinant below alpha². Its active-face optimizer is a diagnostic, not evidence that large-dimensional QPs are cheap.

## Limitations

This is finite-horizon online f-return acquisition with supplied adjoint closure—not a general readout/state simulator, planner, or recognizable global predeployment completion certificate. A new task may require acquisition. Correctness relies on the simultaneous calibration event and physical premises; budgets may cause an explicit terminal refusal before completion. The polynomial worst-case bounds are conservative and do not establish practical episode or wall-clock efficiency. Historical novelty, a physical experimental bridge, and consequential scientific application remain unresolved. The code/tests close the constructive artifact only.
