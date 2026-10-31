# Guarded classical consumer and current-test binding

## Separate verdict and exact sources

**PASS for the guarded sparse-Pauli coupling wrapper and corrected test reporting.** This is a separate binding note; the frozen `AFFINE_EXECUTABLE_INDEPENDENT_REVIEW.md`, SHA-256 `d36858525bf54ae85350a9e925c9d6b78456454f839dba6ca58e82f17525812d`, is unchanged.

I read the complete new `acquire_affine_pauli_consumer.py`, 2,074 bytes, SHA-256 `ac0f48abfb4aa6ee61411c69c59afd65268ab6ec172ae11d188a4648fed93e03`. I inspected the changed harness, reran it to exit zero, and independently exercised the wrapper.

Current supplied harness: `test_affine_source.py`, 8,748 bytes, SHA-256 `2fb028caad5342d8080bdf8b0bd13cfc3fc2a9039646345f2196d2203753186e`. Current report: `affine_compiler_checks.json`, SHA-256 `ab9777276f1aba247bc293beae4526b3944ce95eb271db47223d45e28aea57e4`.

Unchanged imported implementation dependencies were hash-checked:

- Affine compiler: `b0b14aec3a9d4b5b62f13bbd541c3a9aa537dfdf812969b008c369edd85199d0`.
- Repaired Clifford finder/verifier: `d838ceb019302861375671da683467ab82514cd45e6eff6e86a5990e8664b1f0`.
- Exact sparse-Pauli acquisition: `983e5d59f2fa6057d3b953c7f4e92855563995d90675c5e0fdd0b3f0c820cb50`.

## 1. What the guard proves

The wrapper first requires a semantically verified positive affine realization. Invalid or outside-class realizations fail before any coupling output is produced. It uses the already reviewed rational parser/aggregator to combine identical full system/source Pauli keys and remove coefficients that cancel exactly. Only then does it require every remaining source X mask to be zero.

Hermitian Pauli strings form a linearly independent operator basis. Therefore this test precisely verifies computational-basis source diagonality for the explicit combined Pauli operator. Nonzero X masks cannot be canceled by a differently keyed system or source Pauli term. Conversely exact rational cancellation of identical terms should be accepted. No tolerance threshold may erase a tiny but nonzero coherence-sensitive coefficient; the implementation correctly uses exact arithmetic.

For accepted diagonal K, source-label-controlled Hamiltonian evolution preserves the system-operator-valued diagonal source algebra, including noncommuting system blocks. The separately acquired centered operator remains diagonal because its subtraction acts on source identity. This discharges the coupling part of the classical-realization receiving condition without pretending to verify anything about an unspecified control program.

In particular, a source-only off-diagonal term is still rejected: even if it is system identity, it can change public source-label dynamics. Likewise an off-diagonal term whose mean could be subtracted is not admitted on that basis. The guard is checked before centering and protects the original physical coupling, not merely its mean.

## 2. Explicit remaining consumer obligations

The result sets `source_diagonal_coupling_verified=True` but `future_control_instrument_algebra_verified=False`. It retains the exact classical-only equivalence scope and explicitly denies preservation of original coin records or an arbitrary old quantum dilation. These flags correctly distinguish the checked coupling from future, unprovided interventions.

An eventual classical controlled-process claim must still use prescribed outcome-retaining instruments whose adjoints preserve the relevant diagonal algebra, or separately verify that condition. Arbitrary coherent source controls can be simulated as a task for the newly chosen quantum realization under the existing quantum theorem, but are not automatically equivalent to controls of an earlier dilation. The wrapper itself does not implement such instruments, synthesize a quantum circuit, or run the downstream simulator.

## 3. Executed guard tests

The current supplied harness contains three guard cases: diagonal coupling acceptance, nonzero source-coherence rejection, and exact cancellation acceptance. Its full original affine acquisition and semantic-verifier suite also reran successfully.

I added `test_guarded_consumer_independent.py`, 2,595 bytes, SHA-256 `f2518a5f61eec81ba72b03ca9fd869b39d34eaed78832aa7d7429e92168c0021`. Its result `guarded_consumer_independent_checks.json`, 266 bytes, SHA-256 `5902ca69accfddcc8783aa4f0b3018310154af312acfacb80bcbb925f32981e8`, records:

- six valid diagonal/empty/exact-cancellation cases;
- nineteen rejected coherence-sensitive or invalid-realization cases;
- nonzero coefficients as small as 2^-300, with no tolerance-based admission;
- cancellation 1/3+1/6-1/2 across identical keys while retaining a genuine diagonal term;
- rejection when apparent cancellation uses different system or source Pauli keys;
- rejection of source-only coherence and false coin/quantum-dilation scope flags;
- explicit confirmation that future-control verification remains false.

No implementation defect was found.

## 4. Corrected reporting, without rewriting old evidence

The current harness now returns an explicit boolean from its dense helper and separately counts selected calls versus admitted cases that actually execute dense matrices. The rerun confirms 62 selected single-input calls with 23 actual admitted dense cases, and 504 multi/redundant-noise all-offset calls with 248 actual admitted dense cases, plus the separate XOR dense fixture. All outside-class calls remain useful exact rejection tests.

The original report is preserved as `affine_compiler_checks_original_reporting.json`, SHA-256 `4bb262cdb9928219db82d48f31059b64652cf2efdc670898246b07e536941fc0`. The old receipt already explained its misleading label. This note binds the corrected current report without changing old bytes or claiming that extra dense checks were run retroactively.

The resulting evidence supports an executable affine source-realization frontend plus an executable exact classical coupling-algebra guard. It does not establish a downstream quantum simulator implementation, practical advantage, novelty, general control-algebra inference, or arbitrary quantum-dilation equivalence.
