# Fixed four-spin-port concatenated guard — 2026-10-29

**New:** a constructive fixed-port extension of the reviewed gap-free learner and guarded recovery. The source port remains four spins for every block length. Classical verification, actual Clifford circuits, total decoders and concatenation are supplied rather than assuming an asymptotically good code exists.

Governing proof: `GOVERNING_v1.md` (independent review pending until a separate receipt is issued).

## What ran
- `construct_inner.py`: exact sequential isotropic sampling; exhaustive nonzero-syndrome verification; received Clifford canonicalization; sparse total-decoder tables. Saved instances [[32,2,>=2]], [[48,3,>=3]], [[64,4,>=4]], [[80,5,>=5]]. The80-qubit case verified130,354,980 Pauli labels in15.8 seconds on this execution. It has2118 native H/S/CX/SW decoder gates,1699 of them CX. These are noiseless compiled circuits, not hardware trials.
- `check_phase_decoder.py` and `check_phase_decoder.py scrambled`: exact uniform-flag counting, phase-aware dense Clifford checks, total syndrome correction and12 coherent input/source-memory/reference tests per fixture.
- `check_concatenated.py`: the actual80-qubit inner circuit and GF32 outer binary Clifford/syndrome decoder,100 exact native-error tests including concentrated worst-case block distributions;2560 native service slots,80 logical payload qubits, guaranteed12 native faults corrected.
- `check_fixed_port_parameters.py`: rational sample/net/guard/resource bounds, including exact exposure ratio1/1152.

Run from this folder with Python, NumPy and a C++17 compiler. `construct_inner.py` compiles `verify_low_weight.cpp`; the generated platform-specific binary need not be packaged. Its fast syndrome representation is128-bit; a Python arbitrary-integer fallback handles larger dimensions. Large asymptotic instances are proved algorithms, not executed code searches.

## Important correction retained
Independent reviewer found the initial dense decoder test confused tensor-index bit order with table syndrome packing. A symmetric five-qubit code masked it. The corrected test reverses tensor indices into the explicit sum outcome_j*2^j packing and adds a locally scrambled code. The original counterexample and receipt belong in `fixed_port_guard_audit_20261029`; this correction does not change the exact low-weight verifier or saved bit-packed large-code tables.

## Actual scope
The theorem combines model-free accepted soundness with gap-free readiness under one fixed hidden FULL JOINT collective algebra. It does not cover arbitrary unknown noise with guaranteed success. It is a fixed-port source-exposure rate, not unassisted quantum capacity, an overall computation rate, or self-bootstrapping local memory. Controls, privacy, trusted output/reference buffers and terminal operations remain paid.

The conservative readiness bound is vacuous at executed h5. Exact rational parameter evaluation becomes nonvacuous at astronomical sizes: h50 has validation-abort upper bound~.0465, with N=16h2^h native slots. Do not present the small verified code as a successful end-to-end high-yield quantum experiment.

The fixed-port full-path two-MUB/Pauli-pad alternative uses the same learner and concatenated code and attains the same asymptotic orders. No generic advantage over that equally informed alternative is established. Random stabilizer generation and quantum concatenation are established coding machinery, not claimed discoveries.

Dependencies remain actual received Astra online learner, permutation-orbit memory theorem, four-spin encoder, algebra compiler and GF(B) outer compiler. Source files were copied/read without modifying originals. The code-search/decoder test uses a reproducible PRNG; the exact uniform sampling theorem assumes independent fair bits and explicit capped sampling costs.
