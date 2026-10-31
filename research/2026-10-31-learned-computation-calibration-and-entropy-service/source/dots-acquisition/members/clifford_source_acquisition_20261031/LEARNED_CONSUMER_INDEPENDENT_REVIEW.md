# Independent executable learned-consumer composition review

## Verdict and exact binding

PASS for the scope-preserving classical specification wrapper only. I read the complete wrapper and supplied harness, re-read the actual learning-record verifier and classical coupling guard at the join, reran the harness, executed independent adversarial checks, and compared CLI output byte-for-byte with the generated expected example. No code defect or additional scientific premise was found in this composition.

Bound source:
- `acquire_learned_pauli_consumer.py`: SHA-256 `1558463ef9ae78f37dbb6cff009afe68d1d6ff6f524605bbb59bfcc6cbf9e41c`.
- `test_learned_consumer.py`: SHA-256 `140c47283996e01b36d89427ecb19444ed6cc33b22f872047347710d5f1a1cd1`.

This is a new review of this wrapper, not a claim that earlier module reviews automatically imply correctness of every future composition. The underlying learner, affine realization, signed sparse-Pauli acquisition and source-diagonal guard retain their separately reviewed scopes and unchanged source bindings.

## Actual join

1. The wrapper calls `verify_learning_record(transcript, learning_record)` before using the inferred model. That verifier recomputes the prescribed inference from the supplied transcript, checks its digest, every required scope field, realization and exact confidence arithmetic. It does not verify the stochastic teacher promise.
2. The wrapper passes the verified inferred model and realization to `acquire_classical_coupling`. This guard requires a verified positive uniform pure-return realization; therefore an algebraically valid nonadmitted learning record does not reach a consumer.
3. The guard combines exact rational Pauli terms before checking that every surviving source-X mask vanishes. Thus exact cancellation is allowed, but even arbitrarily small nonzero source-coherence-sensitive terms are rejected. This is the previously earned classical-task coupling restriction, not permission to replace arbitrary source-coherent quantum dynamics.
4. The wrapper copies the verified transcript digest, actual prescribed acquisition query count, unconditional inference-failure bound, and conditional admitted-transcript-average bound. It installs the fixed SCOPE fields rather than propagating arbitrary extra user-provided claims. It explicitly sets `downstream_simulation_executed=False`.
5. The separately generated `future_control_instrument_algebra_verified=False` survives this update: SCOPE does not overwrite it. The wrapper checks the supplied coupling only; a later control/instrument program is still a separate obligation. It does not preserve old hidden coins or an arbitrary original quantum dilation.

The result is an exact classical specification for the inferred admitted model, plus its statistical limitations. It is not a compiled quantum simulation or an execution of that simulation. The wrapper adds only a constant number of calls to the previously polynomial verifiers/acquirers and output metadata handling; no new sampling oracle, state-label access, rate-learning procedure or quantum circuit synthesis is hidden here.

## Statistical boundaries remain load-bearing

The fresh independent uniform-subspace noise, affine fixed law, correct complete labels, chosen-input/reset access and known clock remain model/access promises. Verification certifies the inference algebra, not those promises or exact teacher truth. Confidence is frequentist over training transcripts and, conditional on admission, their average. It is not posterior correctness of each observed dataset, nor a guarantee surviving arbitrary rare future postselection. Numerical simulation errors and execution costs remain separate and accumulate under reuse.

In particular, the preserved wrong-but-admitted transcript is intentionally accepted by the wrapper. The independently established hidden-model comparison says its inferred law can be wrong; its exact record nevertheless verifies. The output still states that the model promise was not verified, rare postselection is not covered, and downstream simulation has not occurred. This is an essential negative boundary test, not a defect to conceal or a dataset to promote to truth.

## Executed evidence

The supplied harness passed: one successful scoped consumer, five rejected boundary cases, wrong-but-admitted acceptance with limits, and correct metadata. Its generated report `learned_consumer_checks.json` has SHA-256 `1253bfe6d34a6bd0d1e0cd5e8385cd99a66c901727d478a94effe82dc46bf824`.

Independent test `test_learned_consumer_independent.py` has SHA-256 `78d220179a605ac987edea96d213c27fcf5c53740371cb40fa0e94304b49a129`. Its report `learned_consumer_independent_checks.json` has SHA-256 `67b96aef1db89b83c5336a0adb2c802059c6c30dd7e74c04cd0204c26aef5c71`.

Those additional tests passed 24 rejected cases spanning malformed records/transcripts/couplings, strict boolean scope tampering, changed unconditional/conditional confidence, and a nonzero off-diagonal coefficient of size 2^-300. Exact rational cancellation of opposing off-diagonal terms was accepted. Inputs were not mutated. Injected extra claims of posterior truth or completed simulation were not propagated; the output explicitly retained no-simulation status. The rare wrong admitted record retained all required limits.

The CLI was then executed with the saved transcript, `learned_history.result.json`, and coupling; its stdout matched `learned_history.acquired_coupling.json` byte-for-byte. An initial reviewer command used a nonexistent `.record.json` filename and failed before loading data; correcting it to the actual `.result.json` completed the check. This was a reviewer path typo, not a wrapper issue.

## Final scope

Accepted for packaging as a reviewed research-prototype receiving wrapper composing already reviewed executable acquisition modules. No source/model-learning scope expansion, teacher-truth validation, future-instrument checker, unknown quantum-backaction identification, complete simulator implementation, practical performance or novelty claim is earned by this receipt. Frozen underlying modules were not edited.
