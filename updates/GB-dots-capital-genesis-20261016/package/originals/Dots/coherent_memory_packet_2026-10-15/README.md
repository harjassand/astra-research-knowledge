# Coherent post-correction memory bridge

This scientific packet distinguishes three ideal models and provides the supporting proofs, interface reviews, exact examples, and executable finite checks. Start with HANDOFF.md and STATUS.md, then read bridge/BATH_MARKED_PROPOSAL_THEOREM.md for the composed result.

## Three models

1. **Original active-jump Pauli model.** The original seven active correction jumps, independent single-face Pauli noise, exact initialization and ideal final decoder. Its asymptotic theorem covers six logical qubits at compatible sizes L=bM. It does not establish arbitrary coherent perturbation robustness.
2. **Refined completed memory-only model.** Additional local-stabilizer refinement and ideal fresh randomization of a fixed, frame-independent memory-only U yield a full-input CP mixture. One may choose q=||U−I||²≤δ² when ||U−I||≤δ<1. More generally any q≥||U−I||² below 1 is permitted. The separate independent-stream reduction uses clean rate κ(1−q), bad rate κq, and charges the whole correction-plus-fault gadget to the bad patch. See bridge/REPORT.md and bridge/INDEPENDENT_AUDIT.md.
3. **Unrefined completed joint-bath instrument model.** A joint norm bound ||U−I⊗V||≤δ and exact joint fresh-frame averaging bound every conditional bad-character probability by δ². Actual marks may depend on outcomes and the bath; only their dominating reference marks are independent. Every κ-rate correction remains. Good records form a trace-nonincreasing bath-factorized map; completing its bath defect gives the 2ε diamond bound. See bridge/BATH_MARKED_PROPOSAL_THEOREM.md, bridge/BATH_QUANTUM_AUDIT.md, and classical/SAME_ATTEMPT_LABEL_COMPARISON.md.

The last two are completed-proposal models and cannot be silently identified with the original active-jump generator on syndrome coherences.

## Layout and source integrity

- originals/: three original scientific source documents, copied byte-for-byte. Their dates, historical status sentences, provenance references and out-of-packet references remain untouched; they are not the current status. Original source files are distinct from later reconstruction notes.
- bridge/: current coherent-error statements and mathematical audits, with portable local references.
- classical/: reconstructed support, forcing, probability, domination, torus/history and channel interfaces.
- checks/: unchanged executable examples and microscopic checker.
- verification/: captured outputs, runtime versions and review of the finite-test scope.
- PROVENANCE.json: source-file hashes and explicit copy/edit classification.
- SHA256SUMS: integrity of every other included file. The manifest does not hash itself.

Source names sweep/MONOTONE_ENVELOPE.md, sweep/HOMOLOGY_AND_SLAB_TRANSFER.md and lead/STOPPED_TORUS_REPLAY.md map to their technical editions in classical/ with slash separators replaced by underscores. Their original hashes and the verified public repository/source locators are retained in PROVENANCE.json; raw originals with routing metadata are not redistributed. lead/READOUT_CONSTRUCTION.md maps to originals/lead_READOUT_CONSTRUCTION.md. THEOREM_AND_PROOF.md maps to originals/original_theorem.md. Historical audit files not present in this packet are not needed by the executable checks and are not asserted to have been reproduced here.

## Replay

Python 3.12 was used. In an environment with the packages in requirements.txt installed, run from the extracted packet directory:

    python3 verify_manifest.py
    python3 replay.py

To rebuild the archive without changing source bytes, run `python3 build_archive.py /path/outside/packet/rebuilt.zip`. Sorted entries, fixed archive timestamps and fixed file modes make archive generation deterministic in the same Python/zlib environment.

The replay uses only relative paths resolved from its own location, writes no files, accesses no network, and runs all four checks. Exact rational checks use SymPy; the floating-point illustration uses NumPy and SciPy. No packages are installed automatically. Python assertions must remain enabled; the runner rejects optimization mode.

The numerical examples test small constructed channels. The microscopic checker enumerates local configurations. None simulates a finite-noise large memory, computes a practical threshold, or formally verifies the full theorem. Independent scientific review and novelty review remain necessary. Published papers are cited by links; no full copyrighted PDFs are redistributed.
