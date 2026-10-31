# Independent executable Clifford-source acquisition review

## Verdict and exact binding

**PASS for the repaired research prototype in its declared raw-circuit class.** I read the complete finder/verifier and original test file, independently reran the supplied suite, added and ran a separate dense/adversarial suite, found a real certificate-verifier defect, and verified its repair. This is an implemented exact certificate frontend, not an implementation of the downstream quantum simulation compiler.

Final bound sources in this directory:

- `acquire_clifford_source.py`: 12,463 bytes, SHA-256 `d838ceb019302861375671da683467ab82514cd45e6eff6e86a5990e8664b1f0`.
- `test_acquisition.py`: 8,830 bytes, SHA-256 `86adf1b6dd89e121d17543f8bf5c01378cd9077c4b8ac2de8557a70917b76823`.
- Supplied-suite result `acquisition_checks.json`: SHA-256 `156104571fc474c65e3e41238b9d8590c693b0eff228c97bc33d5d3e850b5f49`.
- Independent supplemental test `test_independent_adversarial.py`: 4,872 bytes, SHA-256 `3dc7718c4140a4b9730d47db1d4f6e5e5ff6f36583a0365e4a1670be20c79555`.
- Supplemental result `independent_adversarial_checks.json`: 629 bytes, SHA-256 `5494a5282aa659f3a305fbedd35caa183c294cf8c92a33b650941fe9219cbb50`.

The underlying mathematical acquisition proof remains separately recorded in `INDEPENDENT_ACQUISITION_PROOF.md`, SHA-256 `997140547b36e1edfe75e012d5da22306b733ee8e1b1113626b003cfa1867bae`. Tests supplement the code-to-proof audit; they do not replace the proof.

## 1. Declared input and source semantics

The admitted input specifies n>=1 source qubits, env>=0 zero-initialized environment qubits, and an explicit gate list over H, S, SDG, X, Z, CX and SWAP. The first n output qubits are retained and the others traced out. Validation checks list structure, opcode, arity, integer qubit indices, range and distinct two-qubit operands. Every gate is classified. Extra mathematical classes such as adaptive stabilizer measurements, arbitrary classical mixtures of stabilizer programs, or unknown-source learning are not acquired by this implementation. A pure stabilizer environment can be expressed only by including an actual allowed preparation circuit on zero ancillas.

The finder receives no proposed fixed state, environmental output state, or forgetting horizon. Its only source input is the raw program. NumPy/dense matrices occur only in tests, not in the finder or verifier.

## 2. Pauli map and exact forgetting

The representation i^p X^x Z^z and multiplication phase 2(z dot u) are consistent. H, S/SDG, X/Z, CX and SWAP conjugations correctly update this convention, including Y signs. Inverse gate order gives the adjoint channel map. A zero-ancilla Pauli expectation survives exactly when its environmental X mask is zero; environmental Z factors have expectation one. Thus `pauli_maps` acquires the linear source-label map F and survival constraints without discarding phase information from later stabilizer computations.

`image_step` computes the coefficient kernel of the restricted environment constraints, maps it into the current Pauli-label space, and applies F. This is precisely M_next=F(M intersect S). The image filtration is nested, its canonical GF(2) bases are exact, and a nonzero plateau persists. At most 2n strict dimension drops are possible. A zero image means an exactly constant channel power; a nonzero plateau certifies persistent nonidentity Pauli information. It is essential that source labels mapped to zero represent constants rather than a surviving nonidentity observable.

## 3. Constant-state purity and actual phase-aware circuits

After exact forgetting is found, the code propagates a maximally mixed source stabilizer state for the acquired horizon. It appends zero-ancilla Z generators, conjugates them through the actual circuit, and takes the kernel of all environmental X and Z coordinates before restricting to the source. This is the correct partial-trace stabilizer operation, not an assumed pure initial state. Independent rank n gives a pure constant state; smaller rank is reported as `mixed_reset`, not admitted as pure return.

The preparation routine performs signed stabilizer elimination, tracks phase corrections, and returns the inverse reduction circuit. Its generated state is checked again, as is fixedness under the source channel. For an accepted certificate the verifier checks the exact forgetting filtration, a valid pure preparation, and fixedness. Exact forgetting plus fixedness identifies the same unique constant output, so recomputing a dense constant density matrix is unnecessary.

The environmental preparation is the literal circuit `psi_prep + actual_U + inverse(psi_prep)` on clean source/environment work. It is not a preparation of an independently chosen stabilizer ray. Since W psi=psi tensor c, unpreparing psi leaves clean source work and the actual c, with its phase relative to U intact. The certificate is digest-bound to the complete gate program. Changing U by an invisible global phase changes the required c circuit and invalidates the old certificate even though the source channel is unchanged.

## 4. Actual discovered defect and repair

Original source SHA `ca74d79b2d450fd079081b0ce18114e8843da2fce34cbe404752bf4dc294d43e` incorrectly accepted a forged persistence certificate for a one-qubit SWAP reset. Replacing the filtration with `[M0,[0],[0]]` and declaring stabilization at step two passed because the verifier tested list nonemptiness rather than nonzero vector-space dimension. This was a genuine false negative-class certificate, not merely cosmetic validation. The original finder outputs were not observed to be wrong.

The repaired verifier requires each filtration row to equal its canonical basis and also tests a nonzero final basis for persistence. It rejects the exact reproducer. It now rejects nonmapping certificates before using `.get`; malformed program mappings and non-list gate collections are rejected explicitly. The original failure result is preserved in `independent_adversarial_checks_original_failure.json`, SHA-256 `893493c5c080a6e5c0fa05c3e124bc969cd696b2e835cc2fb2b652bbfb4694ec`. This receipt accepts only the repaired final source, not the original verifier.

## 5. Executed verification

The final supplied suite was independently rerun to exit zero. It covers nine named dense cases; 180 randomized dense cases; symbolically transformed history registers at n=8,16,32,64; certificate tampering; and malformed input cases. Dense tests compare all system Pauli adjoints, the constant-channel superoperator when applicable, constant-state rank, and the actual phase-sensitive c factorization.

The separate supplemental suite also completed successfully:

- 1,728 exhaustive single-gate/Pauli conjugation comparisons on three qubits, including both orders of CX and all mixed-Y phases.
- 120 additional randomized dense programs with an independent seed and source/environment sizes (1,2), (2,2), (3,1): 23 pure returns, 43 mixed resets and 54 persistent cases.
- 36 independently generated complex/entangled pure-reset preparations paired with a global-minus source change.
- Eight eighth-root global-phase checks using powers of (HS)^3, checking the actual c vector rather than only its density matrix.
- Rejection of the zero-only persistence forgery, six malformed top-level certificate forms without exceptions, and thirteen malformed raw programs.

The final source hash recorded by the supplemental test matches the receipt binding. Dense floating-point tolerances are diagnostics only; the finder/verifier itself uses exact integer masks, phases modulo four and GF(2) arithmetic.

## 6. Polynomial resources and limits

Let N=n+env and G be the explicit gate-list length. Pauli masks have O(N) bits. Map construction uses 2n gate propagations. The filtration has at most 2n transitions, each using finite GF(2) elimination on O(n) vectors. Stabilizer propagation uses at most N independent generators per step, with at most 2n steps; preparation elimination produces polynomially many gates. The stored filtration, maps, stabilizers and c template have polynomial bit size in N and G. No exponential density matrix or list of Kraus operators is generated by the frontend.

This is polynomial in the physical register count and explicit program size, not in log N if a huge register size is encoded as one integer. Verification is polynomial in the supplied program and certificate sizes. Python allocation limits, denial-of-service bounds for enormous inputs, packaging and production hardening are not certified here.

For this monomial-Pauli channel class, the independent proof establishes the connection between persistent Pauli information and failure of any strict uniform pure-return certificate. The executable frontend therefore acquires or rejects precisely this declared pure-return interface, including distinguishing exact mixed reset from pure reset. It does not decide general quantum mixing or stability. Downstream coupling operators may be non-Clifford; ordinary stabilizer simulability of the source alone does not make the full consumer a stabilizer computation. No novelty, practical advantage, unknown-source learning, full simulator implementation or automatic gate-complexity advantage is claimed.
