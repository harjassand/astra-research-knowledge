# Read and replay ledger

## Pins and scope

- Worker instructions: work/FO_WORKER_CONTRACT.txt, all 13 lines, SHA256 9b2e4424660e44b95a6d8d8c72f8dae8d34c674c3a107ebc932648878b210ee7.
- Required pin: work/FO_PIN.json, all 29 lines, SHA256 3e33623d46231fbf7479574f73a63f7fd9c8e0ca8d9999efb9c18d8bce30ec56. It records main and checkout as 1c45f77e32d6fbd72483aed5014061c7bda4f372, publication namespace FO, incoming intake manifest, and next card identifiers N817–N819. A direct git rev-parse HEAD attempt returned “not a git repository”; the pin's checkout revision could not be independently checked in this workspace.
- Incoming source manifest: work/FM-sources/INTAKE_MANIFEST.json, all 192 lines, SHA256 3d8a4bdbb70978074beb6bba8587c50186d2524c36759a2eafa5a1c3969d82ea. It pins 23 original payloads/165,959 bytes and identifies the source profile file and exact bytes.
- Source package manifest: work/FM-sources/resonant/MANIFEST.json, all 85 lines, SHA256 9a48c53735d156bb713851a64134e5db8c8b6eeddbe671e09521b47badfd8b58.
- No capital, original source, prior output, memory, or other FO worker file was written or executed. All writes are under work/FO-circulation-audit/.

## Instructions and mathematical capital read

| Source | Pin / size | Read depth and use |
|---|---|---|
| work/astra-capital/00_START_HERE.txt | SHA256 4a91985ece91557af12ba5c216e7fe17cf5dd000596e9a0c73b0b6705498f360; 8 lines | Full. Retrieval, proof-scope, and UNKNOWN rules. |
| work/astra-capital/AGENTS.md | SHA256 581cdda103fed0c87acdb0ee527bd5ba174f55b1baa0cbfe60b177d52027ee7d; 7 lines | Full. Applicable capital handling rules. |
| work/astra-capital/agent/COMPOSITION.txt | SHA256 b31cf8c3344df112b66840455244ff9c4b4f590d44713582027f82b50c83c46b; 31 lines | Full. Used to distinguish a scoped compatible result from a general implication. |
| work/astra-capital/state/CONTINUITY.md | SHA256 040c4ac42162802bd2fb4f9e8069e6ca034ccbee63cffc7b43f4c745dac0b297; 40 lines | Full. Read; no handoff or publication was attempted. |
| work/astra-capital/technology/README.md | SHA256 ed7cab65d78be8f3ca4734befe3c868203d7d6e30ba1ed875a8084c87b76f89e; 134 lines | Full. Read for evidence and capability boundaries; no technology record was created. |
| work/astra-capital/frontier/dossiers/N794.txt | SHA256 bdd17cc2ca4802a5e935fe5aeddd53a1b23bfcb56d45b04a3f113cba5db00a63; 113 newline-terminated lines | Read scope/status, semantic notice for N812, open gates and the historical N794 summary (lines 1–57), plus the N794 card summary. |
| work/astra-capital/cards/N794-left-invariant-quartic-classification-and-closed-heat-certificate.txt | SHA256 c215f2d34c0f6e8119757a3849fa86ece6b5c7bf94a4ffd58657363806b5a576; 19 lines | Full. Compared the acoustic criterion, nine-moment completion, Fstar heat result and open full-cone obligation. |
| work/astra-capital/updates/FE/package/quartic/ASTRA_META_GENESIS_Morrey_quartics.md | SHA256 7c88a08aa6aef88786751fde9671b7568e97676c516824028c3aac9d9859725b; 449 lines | Read lines 1–32, 230–427. Scope, exact 8x8 acoustic condition, Fstar status, nine-moment completion, and resonance exclusion. |
| work/astra-capital/frontier/dossiers/N812.txt | SHA256 523627d823b1c93be90a6197e8d8e07d2a78360e11de81c0309170794721d2a4; 172 newline-terminated lines | Read the current scope, route, and open-gate summaries. |
| work/astra-capital/cards/N812-global-modulation-and-curved-phase-moment-certificates.txt | SHA256 5f91facc7a85f9ca0ef4e1e554aec930705190e9867ca5d82ce3bdac90a688ea; 15 lines | Full. Compared the modulation, mu/12, envelope, and packet-assembly scopes. |
| work/astra-capital/updates/FL/package/global/GLOBAL_COMPATIBILITY.md | SHA256 bddd6149e1523a8e73fdd26a3d8820dadc3ebad023eb319878ff77ca64f32eee; all 444 lines | Full. Reconstructed the N812 modulation theorem, quartic coercivity, packet assembly, exact G example, and stated limits. |
| work/astra-capital/updates/FL/package/global/verify_global_compatibility.py | SHA256 00eb94a94ae587a4ab09640bbfa94dba189657dc9c3b0bad4e0317692ac0d5fb; 249 lines | Read lines 1–90, including exact G acoustic Gram and determinant-balanced witness. Not executed; the incoming source's own verifier reconstructs the G Gram. |
| work/astra-capital/frontier/gates/G-FE-N794-REVIEW.json | SHA256 bab72e2cbd05a53794ebd634ab099a136f8d60bd653db14fd25706309d0a1e06; 30 lines | Full. Open external review and general heat-certificate/completion obligation. |
| work/astra-capital/frontier/gates/G-FL-N812-REVIEW.json | SHA256 cb9c7ab478b4b3e45835ebac769feeac8254fb05c967e96bded541987f2c47e2; 30 lines | Full. Open full-moment and external review obligation. |
| work/astra-capital/frontier/gates/G-FL-N812-CAPABILITY.json | SHA256 58d1a9a0dbebd5f5f03e7a76e02e0836b14355f72eb857544e1bb28f15853075; 30 lines | Full. Same underlying completion/review gate; no capability claim inferred. |

## Incoming proof and exact source package

| Source | Pin / size | Read depth and use |
|---|---|---|
| work/FM-sources/resonant/README.md | SHA256 d013ff24b75caf639f0e946d4574e28f83c8e6b6ad90d4f1ce196ebd1da2c4b7; 44 lines | Full. Established the declared replay command and which exploration files are unnecessary. |
| work/FM-sources/resonant/PROFILE_CIRCULATION.md | SHA256 881b80eac0bcfd04113dcba7226b9faee324dda66d44ffee5ae3ea097b072622; 378 lines, 26,697 bytes | Full. Proof and exact examples reconstructed section-by-section; source lines are cited in REPORT.md. |
| work/FM-sources/resonant/verify_circulation.py | SHA256 324780f0de1d7bc89d395e04f7a903cc0cfec73993dc2f41fa31ae152690f416; 115 lines | Full. Inspected all operations and output writes before copying; replayed only the copy. |
| work/FM-sources/resonant/profile_algebra.py | SHA256 5472dc38d87e195dca55782eec773d8555827495a3b25d4ca9b3a9768ed613be; 98 lines | Full. Inspected Laurent average and rational path/edge integration helpers before copying. |
| work/FM-sources/resonant/check_loop_examples.py | SHA256 cb07406755699aef8f5ed4657766742db9fb241525349644417b2c06c24f16ab; 37 lines | Full. Inspected and replayed the example generator only in the copy. |
| work/FM-sources/resonant/certify_profile_graph.py | SHA256 03235da8b9edb6c28f3f5a6783c341b61c669aedce9c53289e5ffd498d5c158f; 65 lines | Full. Inspected exact edge enumeration, shortest-path potential and all-edge verification before copying. |
| work/FM-sources/resonant/loop_examples.json | SHA256 f189282235c386d7f87f7b6352461e8fdaf3b5fbc758943968752b48f857fa30; 456 lines | Read the exact reported covariance, Hessian, cubic, constants, optimizer and gap fields; the copied replay regenerates and matches the JSON. |
| work/FM-sources/resonant/circulation_verification.json | SHA256 01abb473b08acc63fceb58a0cbb1feebe3c2ba79732fd0d60ec0de4815fcf2ca; 220 lines | Read its status/groups/details and re-created it in the copy. |
| work/FM-sources/resonant/profile_graph_certificate.json | SHA256 f9782aafd2828375c06d0bd08f9ff7dfdb38655da714ebd5b1a60979bf86d1da; 435 lines | Read scope and certificate fields; independent checker consumed and checked all exact potential entries against independently recomputed costs. |
| work/FM-sources/resonant/circulation_replay.log | SHA256 9f9e7826b4c20fe5d7369c8ef2306b9faeee70511807b93d0fe6550b5f6c24b7; 12 lines | Full. Producer replay provenance for the incoming verifier. |
| work/FM-sources/resonant/prior_replay.log | SHA256 1d4c0548bf5c2ebc4921ff5cdb9c395585b31bb5808d344c434a269b48e1a052; 10 lines | Full. Prior N812 modulation replay provenance only; not treated as a premise or as this audit's replay. |

The exact input package was copied to source-copy/ before execution. Its preserved MANIFEST.json validates all 11 copied package entries by byte count and SHA256. The five exploration files named in that manifest were not copied; the package README says they are exploratory, use floating outputs, and are not needed for reproduction. Replayed JSON outputs are preserved separately in replay-output/; the source-copy JSON files were restored to the original pinned bytes after replay.

## Commands and observed results

Environment: /Users/harjas/Documents/Codex/2026-10-14/astra-research-capital-integration-synthesis-breakthrough/work/FE-hidden-gate/venv/bin/python; Python 3.14.3; SymPy 1.14.0. No optimizer or external service was used.

1. In source-copy/, ran the pinned interpreter on verify_circulation.py. Exit 0, measured wall time 3.72 s. All nine groups passed; graph replay found 81 vertices, 32,805 edge/width choices, 104 negative raw-energy strips, 2,046 negative adjusted strips, 93 tight inequalities, and minimum integer slack zero. Output log: replay_verify_circulation.log.
2. In source-copy/, ran the pinned interpreter on check_loop_examples.py. Exit 0, measured wall time 1.16 s. Exact forward/reverse examples and eight-loop affine optimizer reproduced. Output log: replay_check_loop_examples.log.
3. In the owned root, ran the pinned interpreter on independent_checks.py. Exit 0, measured wall time 15.37 s. This implementation imports no supplied helper module. It checks 40 direct path line moments over positive and negative translations; the small-area/large-background example; a same-period exact energy non-preservation example; and every one of the 32,805 graph inequalities using an independently derived cos(2y) action formula and rational segment integration. Results are in independent_checks.json; stdout is independent_checks.log.
4. Compared each generated JSON file with its preserved source counterpart, recursively dropping only runtime elapsed_seconds fields. circulation_verification.json, profile_graph_certificate.json, and loop_examples.json all matched exactly after that normalization.
5. Attempted git rev-parse HEAD to check the supplied checkout pin. It failed because this workspace is not a Git repository; no current HEAD claim is made.

No primary literature was opened. The incoming proof's bibliography is a provenance and priority context, not a premise in this audit. The source's external correctness and historical novelty remain UNKNOWN. No physical acquisition, experimental validation, or material property was claimed. CPU-energy, inference-token, and financial costs were not measured and remain null.
