# Editorial and path provenance

All three `candidate.npz` files and their `candidate.json` manifests are byte-for-byte copies of the original exports. No basis deduplication or numeric transformation was performed during packaging. Verification code, experimental source code, acquired proof evidence, and exact certificate JSON files are unchanged.

User-facing report copies were edited only as follows:

- Coordination and approval wording was replaced by scientific descriptions of the documented follow-up tests. The third test is described as occurring after the first two results, not as specified in advance of them.
- The historical experiment paths in `verification/REPORT.md` were mapped to this packet's `experiments/` and `references/cap_source/` directories.
- Detailed preliminary method reports were replaced by the consolidated `reports/METHODS_AND_COSTS.md`, which retains the executed method, resource figures, residual distinctions, limitations, and provenance.
- The descriptive `method` and `full_residual_upper` strings in the third `construction.json` were updated for the final documented status. Its numerical fields were not changed. That record is a construction diagnostic, not an exact certificate.
- `verification/SOURCE_MANIFEST.sha256` preserves the original source manifest. `verification/MANIFEST.sha256` updates only the report-copy hash; code hashes are unchanged. The packet-wide manifest is authoritative for delivered file identities.

Historical names that remain in unchanged diagnostic/certificate metadata map as follows:

| Historical directory | Packet directory |
|---|---|
| kinetic_conservative_slab | experiments |
| kinetic_conservative_slab/weighted_repair | experiments/weighted_repair |
| kinetic_conservative_slab/constrained_test | experiments/constrained_test |
| kinetic_residual_challenge | verification |
| kinetic_cap_source | references/cap_source |
| certified_tensor_incumbent | references/incumbent |
| tamen_incumbent_audit | references/tamen_source_text |

Absolute historical paths in preserved execution metadata are provenance only. The portable entry point uses paths relative to its own packet root and writes replay outputs to the requested output directory. It copies write-beside-script verifiers into a temporary directory. No candidate solver, MATLAB source, or other acquired program is executed during replay.

The replay compares authoritative exact fractions, candidate hashes, and status fields. Execution paths, elapsed times, RSS, and descriptive decimal displays are not mathematical evidence and can differ between machines.
