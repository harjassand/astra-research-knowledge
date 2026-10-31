# Independent executable affine sample learner review

## Verdict and source binding

**PASS for the promised classical chosen-input learner and its algebraic inference verifier.** I read the entire implementation and supplied test file, independently reran the supplied harness, and added separate confidence, parser, alias and model-boundary tests. No implementation defect was found. The crucial limitation is retained: a verified inference record is NOT a certificate of the unknown teacher's structural promise or of truth for that particular dataset.

Bound implementation: `learn_affine_source.py`, 7,330 bytes, SHA-256 `83f18f562b16ae490ff13de3c47305cc3127512f927cfd9e3ba9ee9a75805e3b`.

Executed supplied harness: `test_learn_affine_source.py`, 8,991 bytes, SHA-256 `f382c80d2853287454a7889c41b26749bb91d0e50f99b78e758ea38a3245a147`. Its report `learning_checks.json` has SHA-256 `b479de2ab288135a47eb3485b355b88a31fa01458fbfc9de60a706dd6a9fcccb`.

The mathematical theorem is separately bound to `CLASSICAL_SAMPLE_TO_REUSABLE_SOURCE_THEOREM.md`, SHA-256 `3f67b0ca192358e7af78636e3396fbb910766c41f42f60d7b560e88168fca303`, with independent receipt `SAMPLE_TO_REUSE_INDEPENDENT_REVIEW.md`, SHA-256 `43740c782662bc3b7e0e1ac9b4befb906f67984ce441781cfe8838b1f438b984`. The already reviewed exact affine compiler and repaired raw Clifford verifier are imported dependencies, not new learning oracles.

## 1. Exact query plan and input validation

The learner accepts the fixed-plan transcript fields n, failure_probability and outputs only. It requires positive integer n, an exact rational delta in (0,1), exactly the prescribed number of complete n-bit integer outputs, and no additional transcript fields. Boolean masks, floats/nonfinite values, malformed rational strings, wrong output counts, and out-of-range labels are rejected.

`query_plan` computes ell=ceil(log2(2/delta)) with integer bit lengths and exact shift comparisons, not floating-point logarithms. It then sets M=n+ell, queries zero M+1 times, and queries each basis vector once. The returned bound 2^{-ell} is precisely the universal recovery-failure bound 2^{n-M}, at most delta/2. The resulting number of one-step calls is 2n+ell+1. The conditional-admission bound is b/(1-b), where b=2^{-ell}, and is at most the requested delta.

`sample_and_compile` invokes only the caller-supplied classical one-step callback, at those inputs and in that order. It does not inspect hidden coefficients, make device/network calls, or acquire the physical reset/readout/clock interface by itself. All executed teachers in this review were synthetic. The callback contract, full-state observation, correct chosen resets and fresh independent uniform-subspace noise remain assumptions.

## 2. Inference matches the accepted proof

The sample span is computed from outputs relative to the shared first zero-input output. The kernel/transpose operations produce the quotient with exactly that span as kernel. The quotient offset and basis-state quotient columns are then lifted by an elimination-based right section. These are canonical choices of a transition-law representative, not recovery of invisible original coefficients or coins.

Rank-zero noise is handled by a full quotient; full-rank noise is handled by zero-dimensional quotient outputs and zero-valued section solves. No singular square inverse is attempted. The consistency assertion checks the supplied zero/basis observations in the learned quotient. Since this is an inference identity on the sample-derived quotient, it must not be advertised as testing the global affine/uniform-noise promise.

The learned model is sent to the separately verified affine realization compiler. The source circuit and return certificate are therefore acquired for the LEARNED law. On the mathematical recovery event that law equals the teacher globally; outside that event the deterministic circuit verifier still says nothing about teacher truth.

## 3. What record verification does and does not establish

`verify_learning_record` digest-binds the transcript, recomputes inference from it, compares all inferred objects, verifies the exact affine realization, and checks the confidence metadata and scope fields. Its boolean scope fields use identity checks, so replacing false with integer zero or true with integer one is not accepted as an accidental equality. Forged zero failure bounds, model edits, altered query plans and scope/postselection claims are rejected.

Some internal result lists are intentionally shared, notably the noise basis and learned G columns. Fresh inference recomputation prevents a mutation affecting both aliases from evading validation. The original transcript is not modified or aliased through those derived lists. This is an ordinary immutable-use/copy discipline issue, not a hidden statistical verification method.

The confidence statement remains frequentist over training transcripts for a fixed promised kernel, and over their conditional average after admission. It is not a posterior guarantee for every particular record or after rare later postselection. A truly uncontrollable promised model cannot falsely admit, as proved separately; erroneous rejection of a controllable model or admission with the wrong law can occur on the recovery-failure event. The code does not suppress or relabel those possibilities.

The record expressly states that the model-family promise is not verified from data, that clock access is separately required, that unknown quantum backaction/coupling is not identified, and that rare postselection is not covered. Public exact-law finite reuse is supported on the single successful recovery event, while numerical execution errors and actual consumer costs continue to accumulate.

## 4. Preserved negative evidence is load-bearing

The supplied file `examples/rare_wrong_admitted_transcript.json`, SHA-256 `22a6745ccc23d8d5fe9b97697608b3250c5f0257d0da26d6b44d567353dd365b`, is a positive-probability transcript of the promised full-noise teacher. It produces an admitted, algebraically verified model whose noise subspace is too small and whose global law is wrong. I checked that the verifier accepts that record and that the false truth claim is NOT made. This is the intended distinction between verifying the inference computation and certifying dataset-specific model truth, not an implementation bug to erase.

The supplied exact weighted enumeration has 320 inference records representing 65,536 equiprobable full-noise transcripts and conditional admitted wrong-law probability exactly 1/21 at requested delta=1/4. The grouping is sound: inference depends on the differences only through their canonical span, while Y0 and the two basis outputs are retained explicitly. Weighting each representative by the number of difference strings in its span class reproduces the full experiment.

My additional nonlinear boundary check exhibits a kernel that matches every training-input distribution but differs at an unqueried state. It can produce an admitted verified learned model, with the model-promise flag still false. This deliberately violates the affine promise and confirms that no distribution-free conclusion is being inferred from the verifier.

## 5. Executed tests

The supplied suite completed with exit zero:

- 100 hidden synthetic models, using 2,800 classical transition calls;
- larger symbolic hidden-coordinate models at n=8,16,32,64, with 150 calls and 9,600 observed bits at n=64;
- all 256 transcripts of a selected uncontrollable two-bit promised kernel, with no false admission;
- the exact full-noise weighted experiment and wrong-but-admitted record above;
- eleven malformed transcripts, five scope/model/confidence tamper cases, and four malformed records rejected.

Independent supplemental test `test_learning_independent_adversarial.py`, 6,452 bytes, SHA-256 `44dcdcd3d0845b7476f52bed1d2990ea5e07073a32f063b877fb820f1eb24b96`, also passed. Its result `learning_independent_adversarial_checks.json`, 572 bytes, SHA-256 `c88f49eb1960aac99545656d55d3b3ddc54b850edf47d17bd3ec604c00d0a78b`, records:

- 3,163 exact rational confidence-boundary checks, including large denominators through 500-bit scale;
- explicit zero-rank and full-rank quotient branches;
- alias edits, query-plan and claimed-confidence tampering rejected;
- eight boolean scope tamper checks, including integer substitutes;
- 27 malformed transcripts and eight malformed records rejected;
- all 32 transcripts of a one-bit full-noise example at non-dyadic delta=2/3, with 28 admitted and zero wrong among admitted;
- preservation of the verified-but-wrong promised transcript and the separate nonlinear outside-promise counterexample.

These are exact finite diagnostics and synthetic experiments, not evidence that an external device satisfies the promise. The general sample and lifetime guarantees remain the proved theorem.

## 6. Resource and consumer scope

Planning and transcript processing use exact rational comparisons, polynomial-size binary elimination and explicit matrices. The sample count is O(n+log(1/delta)); full observations and optional retained transcript storage are charged. The learned-model and realization compiler costs are polynomial in the explicit register and confidence-input sizes. The implementation does not enumerate the full state space, synthesize arbitrary coupling circuits, estimate a clock from one-step states, or run the downstream quantum simulation.

The reusable receiving guarantee remains restricted to the declared classical state process and allowed diagonal-algebra controls/couplings. Future coupling acquisition, centering, actual nonzero mean Hamiltonian action, prescribed instrumentation, and numerical execution budgets are separately paid. Arbitrary source-coherent interventions define a task for the newly chosen realization, not an equivalence learned from classical samples. No novelty, practical advantage, unknown latent-state learning or unrestricted source-learning claim is accepted.
