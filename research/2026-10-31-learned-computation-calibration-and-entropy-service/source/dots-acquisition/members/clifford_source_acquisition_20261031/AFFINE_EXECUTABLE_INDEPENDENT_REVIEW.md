# Independent polynomial affine-source compiler review

## Verdict and source binding

**PASS for the executable classical-law-preserving realization frontend.** I read the entire implementation and test file, reran the supplied suite, and added independent semantic/adversarial tests. No implementation or semantic-verifier defect was found. A reporting distinction between selected test calls and actual admitted dense checks is documented below; it does not alter the mathematical result.

Bound implementation: `compile_affine_source.py`, 13,657 bytes, SHA-256 `b0b14aec3a9d4b5b62f13bbd541c3a9aa537dfdf812969b008c369edd85199d0`.

Executed supplied test: `test_affine_source.py`, 7,381 bytes, SHA-256 `08c94cc81da27aeb305523a78d9b7c5ccfaa16c1d7fd25554a30f4ef5b5bf333`. Its output `affine_compiler_checks.json` has SHA-256 `4bb262cdb9928219db82d48f31059b64652cf2efdc670898246b07e536941fc0`. The original summary-label ambiguity is corrected explicitly in Section 5 of this receipt; it is not treated as an implementation failure.

The separate mathematical source is `AFFINE_PROGRAM_REALIZATION_SPECIFICATION.md`, SHA-256 `9e810f64f08ead6182627693747d71dc34f767fdf0797d8d00df3f9628340f0e`, independently reviewed in `AFFINE_REALIZATION_INDEPENDENT_REVIEW.md`, SHA-256 `502a18056312b1ace057f461626788672bbd0cff274ec9838547edb1ca6678bc`. The actual emitted raw source certificate uses the frozen repaired Clifford finder/verifier SHA-256 `d838ceb019302861375671da683467ab82514cd45e6eff6e86a5990e8664b1f0`.

This is an implemented affine realization compiler, not a downstream dynamics simulator. It preserves only the declared classical state-label process and admitted outcome-retaining diagonal algebra. It explicitly does not preserve an arbitrary prior coherent quantum dilation or the original public coin record.

## 1. Input and controllability

The parser requires exactly the four fields n, F_columns, G_columns and offset, with positive integer n, n binary state columns, an explicit noise-column list, and in-range integer masks. Boolean integers, malformed containers, missing or extra fields, and out-of-range masks are rejected. Empty or zero noise lists are well-formed inputs, but cannot satisfy this full controllability criterion and are reported outside the declared class.

`controllable_space` exactly forms the span of G, FG, ..., F^(n-1)G using binary elimination. Rank deficiency yields only `outside_controllable_uniform_class`. It does not claim that no other useful quantum realization exists, that a nonuniform reset is impossible, or that the source is unstable or unsimulable. Duplicate/zero random bits are compressed to the same image subspace without changing the uniform classical noise law.

## 2. Reverse fibres and nilpotent feedback

The transpose/kernel operations correctly compute quotient columns R with kernel im G, the reverse constraint H=RF, a solution A0 of HA0=R, and a basis B for ker H. `solver_table` and `solve` are elimination-based linear solves, not exhaustive searches. Dimensions and ranks are checked.

If the section A0 is already nilpotent, using it is valid and avoids unnecessary feedback. Otherwise `deadbeat_section` implements the proved finite candidate cyclic construction and exact feedback. Its control-column update toggles coordinate zero by the k-row bit, which is exactly addition of e1 k over GF(2). The computed last-row functional agrees with w A1^n. The code independently verifies both nilpotence and the reverse-fibre identity after feedback. This implements the polynomial construction, unlike the earlier deliberately brute-force small diagnostic.

## 3. Actual gate orientation and semantic verification

The compiler completes the rows [A B] to an invertible matrix M for the inverse fibre map. Its physical forward map is M^{-1}. To implement the inverse of v -> Mv+(Ab,0), the code applies the translation to the INPUT and then the inverse linear circuit. That ordering is correct; reversing those operations would generally be wrong.

`linear_gate_program` performs Gaussian row reduction, records SWAP/CX operations, and reverses the self-inverse gates to implement the requested column map. The emitted program begins with exactly g Hadamards on the fresh environment, followed only by positive affine permutation gates. It therefore prepares the required uniform private random input with actual gates and retains the all-plus global phase convention.

The verifier is substantially stronger than a digest check. It extracts the actual affine map and translation by propagating basis columns and offset through the supplied gate list, requires the fair-bit preparation prefix, and rejects non-affine gates after that prefix. It inverts that actual map, derives its source section/fibres/offset, and compares them with the certificate. It checks HA=R, HB=0, full fibre rank, the affine quotient offset, nilpotence, and an independent forward-kernel criterion: actual noise image must equal im G and the actual deterministic map/offset must agree modulo that noise image.

Finally it runs the separate repaired raw Clifford verifier on the actual emitted program and requires its pure fixed state to be exactly the all-plus stabilizer state, with horizon at most n. Thus neither a forged return certificate nor correct-looking classical metadata is enough for acceptance. The semantic checks also reject false coin-record or arbitrary-quantum-dilation equivalence flags.

## 4. Correct equivalence is broader than byte identity

Changing F columns or the offset by vectors in im G preserves the same conditional uniform affine kernel. Similarly reordering or adding redundant/zero private random bits preserves the noise image. After updating the input digest and applicable bit-count metadata, the same realization can legitimately verify for these equivalent raw laws. The verifier correctly allows this; rejecting every such representation change would confuse raw syntax with the declared classical task.

Conversely changes outside the quotient must fail even when the attacker updates the digest. My tests also changed an ACTUAL emitted gate, reacquired a valid source certificate, and refreshed all actual inverse-map metadata. A target translation along the noise image remained valid, while a translation outside it was rejected. Thus the final law check is not merely relying on a stale subordinate digest to catch mismatches.

## 5. Executed evidence

The supplied suite completed with exit zero. It checks 4,164 exhaustive single-input pairs through n=3, including zero columns: 1,370 admitted and 2,794 outside the class. It also runs all-offset multi/redundant-noise cases, hidden-coordinate symbolic sources through n=64, the XOR-noise naive-dilation contrast, malformed inputs, tampered proof/scope flags, and wrong offsets despite an updated digest.

Reporting precision: the original summary's 62 selected single-input calls include outside-class early returns; only 23 execute admitted dense matrix checks. Likewise its 504 multi/redundant-noise all-offset calls include 248 actual admitted dense checks. The XOR fixture adds one further dense check. Outside-class calls remain useful exact rejection/verifier tests, but are not counted as executed dense dynamics. This distinction was independently computed and reported before acceptance.

My supplemental `test_affine_independent_adversarial.py`, 4,933 bytes, SHA-256 `c70a6b1a9c0bbdcdca93be0fe152bdc8a3e7b006aa9af3fab67e9805e6507017`, completed successfully. Its result `affine_independent_adversarial_checks.json`, 498 bytes, SHA-256 `ecb507ba29c642ba36b150e645a51673c7d659f00f55dde9426ab8b102c988f1`, records the bound implementation hash and:

- 12 accepted same-law quotient/redundant-noise changes;
- three rejected different-law changes despite refreshed input digest or fresh source proof and actual inverse metadata;
- acceptance of a valid noise-direction physical gate change;
- 16 rejected malformed/false-scope certificates and 13 rejected malformed programs;
- three empty/zero-noise outside-class cases, including rejection of forced positive status;
- 90 additional random inputs, with 43 admitted cases checked by actual dense gate/Kraus forward-law and pure-return comparisons.

The mathematical proof and exact verifier carry the general result; finite dense tests do not establish asymptotic correctness by themselves.

## 6. Resource and receiving boundaries

The implementation uses finite integer-mask Gaussian elimination, matrix products/powers, linear solves, polynomial feedback search, and O((n+g)^2)-scale affine gate synthesis. No state-space enumeration is used in the compiler or verifier. The emitted program and certificate are polynomial in the physical register dimensions and explicit input matrix sizes. Its invocation of the repaired raw Clifford acquisition routine retains that routine's polynomial resource and phase-safe circuit guarantees. Dense matrices and exhaustive input enumeration occur only in tests.

This frontend now acquires an actual program and proof from the controllable affine specification, rather than assuming a supplied source certificate. Existing sparse-Pauli centering and pure-return simulation theorems may receive the emitted operations within their established assumptions and actual circuit costs. They do not thereby acquire arbitrary Boolean means, implement the full quantum simulator, establish quantum/classical hardness, or preserve the old dilation on coherent source inputs. No novelty or practical-advantage claim is made.
