# Routing rigidity at the quantum-memory broadcasting ceiling

This is a package-level continuation of the consolidated [quantum-memory family](../../../DC/package/quantum_memory_family/README.md), which retains the earlier broadcasting and fixed-width results together with cumulative-resource and stopping-time work. It adds the source-reported near-ceiling routing-rigidity theorem, its exact counterexample and endpoint reduction. It creates no additional frontier card and does not promote a claim status.

## Fast route

Open the byte-preserved [research handoff](RESEARCH_HANDOFF.txt):

| Question | Lines |
|---|---:|
| Near-ceiling routing-rigidity theorem and depolarizing-memory application | [1–62](RESEARCH_HANDOFF.txt#L1) |
| Complete success-distribution proof, including multi-success and unique-success estimates | [63–176](RESEARCH_HANDOFF.txt#L63) |
| Why routing rigidity does not determine the asymptotic reliability exponent | [177–206](RESEARCH_HANDOFF.txt#L177) |
| Exact counterexample to the proposed positive-correlation shortcut | [207–249](RESEARCH_HANDOFF.txt#L207) |
| Clifford-twirled endpoint reduction and unresolved one-layer quantity `s_0` | [250–296](RESEARCH_HANDOFF.txt#L250) |
| Source-reported verifier scope and explicit completion status | [297–322](RESEARCH_HANDOFF.txt#L297) |

## Result boundary

For a complete channel with input dimension `q`, `K` receivers and possibly correlated success flags, the report assumes each receiver succeeds with probability `p > 0` and has conditional Bell fidelity at least `1 - ε`, where `Kp ≥ 1 - δ`, `0 ≤ δ < 1`, and `0 ≤ ε ≤ 1/20`. It claims an exclusive uniform routing channel `R` with

`(1/2)||ω - ω_R||_1 ≤ δ + 2√ε + 12ε`,

and for the complete channels a half-diamond bound at most `q(δ + 2√ε + 12ε)`. The Choi-state bound is independent of `K`. The depolarizing-memory application uses `K = 4^N` and is conditional on success near the prefactor ceiling, `p ≥ (1 - δ)4^{-N}`. The router is a mathematical comparison channel; the physical memory user does not gain access to its additional receivers or environment.

The source explicitly does **not** derive the requested matching reliability law. A sequence such as `p_N = 4^{-N}/N` has exponent `log 4` while its prefactor `4^N p_N` tends to zero, so it falls outside the near-ceiling stability hypothesis. The exact two-input Bell example rejects the proposed product lower bound for joint acceptance only; it is not a high-fidelity memory code and does not refute all collision inequalities. The Clifford reduction preserves `p` and `F` and yields an exact flagged-erasure endpoint distance, but leaves `s_0 = lim_{η↓0}s(η)` undetermined and does not remove adaptive quantum memories.

## Evidence and limits

The attached text contains a proof narrative and reports exact rational/Gaussian-rational checks, two byte-identical verifier outputs, and bounded diagnostic counts. The referenced complete ZIP, standalone manuscript files, and executable verifier were not available in the accessible filesystem during intake. No source code was run, no proof was independently reconstructed, and no cited literature or historical priority was checked. The reported finite checks are not independent proof certification. The original report is preserved verbatim; the guide is navigation only.

The earlier [DC quantum-memory family](../../../DC/package/quantum_memory_family/README.md) remains the route for the prior fixed-deadline, fixed-width, cumulative-resource and stopping-time claims. This continuation does not merge distinct mixed-family broadcasting results into the theorem or assert a transfer beyond the stated depolarizing-memory application.

## Provenance

- [RESEARCH_HANDOFF.txt](RESEARCH_HANDOFF.txt) is copied byte-for-byte from the user's pasted attachment.
- [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) records its digest, source path, missing linked artifacts and intake boundaries.
- The intake repository revision is `587032ada52146a373f6fe6ddcea26488a5398fe`.
- This guide summarizes source claims; it is not a proof audit.
