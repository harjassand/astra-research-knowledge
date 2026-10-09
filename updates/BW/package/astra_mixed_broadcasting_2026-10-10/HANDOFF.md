# Research handoff: maximal instability of approximate no-broadcasting

## Result to preserve

A finite-dimensional mixed-state family can be broadcast to any prescribed finite number of recipients with arbitrarily small uniform marginal half-trace error, while its distance from every common entanglement-breaking reconstruction and every commuting replacement family is arbitrarily close to one. The lower bounds already hold for one fixed finite prior. A corresponding single classical–quantum state is nearly maximally far from every state classical on the broadcast subsystem, while allowing arbitrarily accurate local and bilocal broadcasting.

This is a complete negative answer to a specified dimension-independent trace-distance stability question. **Historical priority, external correctness, formal certification, and a 9–10/10 significance assessment remain unestablished.** It is not an NPT-bound-entanglement or FEI solution. No unverified Astra theorem is used as a proof premise.

Read `RESEARCH_PROOF.md` for the complete theorem, constructive channel, every estimate, finite-prior construction, resource accounting, and precise remaining question.

## Exact mechanism and interfaces

Use a direct sum of symmetric copy spaces, with copy counts m, m², …, m^L and a uniform classical mixture over these levels. A physical channel divides the copies into m equal groups. Each marginal shifts the level distribution down by one, so its half-trace error is exactly 1/L. The optimized broadcasting error is only bounded above by 1/L.

A fixed decoder retains one elementary qudit. Any common measure-and-prepare reconstruction would then estimate an arbitrary d-dimensional pure state from at most m^L copies. The standard bound (k+1)/(k+d), reproved in the manuscript, gives the EB obstruction. A separate all-basis support-projection second-moment argument gives the commuting-family obstruction; EB outputs are not assumed to commute.

Only pure-state moments through degree 2m^L are needed. One finite weighted projective design suffices simultaneously for every comparator channel and every orthonormal basis. The proof gives both a finite convex-hull bound and an explicit algebraic stick-breaking/Gauss–Jacobi/phase cubature.

For binary broadcasting, L ≥ 1, K=2^L, d=4K²:

- constructed broadcasting error = 1/L;
- common EB reconstruction error ≥ 1 − (2K−2+L)/(4LK²);
- commuting-family distance ≥ 1 − 1/K;
- distance of the cq state from all states classical on H ≥ 1 − 1/√K.

These are analytic parameter bounds. The enormous matrices for large L were not instantiated.

## Scope controls that must accompany reuse

The input already contains genuine copies of an unknown elementary pure state, in a classically uncertain copy-number sector. It is not supplied for free from one unknown qudit. The direct-sum dimension, finite alphabet, and preparation costs are large. The output copies are correlated: the global cloning half-trace error is exactly 1−(L−1)/L^m. For L≥2, the marginal is maximally far from being globally idempotent in diamond norm: ||Φ−Φ²||diamond=2.

Both Holevo capacity and actual-prior Holevo loss are computed exactly in the proof and are large. **Do not mark N371 closed. Do not invalidate N368 or N534.** N368 has a bounded-capacity premise; N534 has a pure-family premise. This example violates both relevant restrictions.

## Single remaining question

For a self-compatible channel Φ and an arbitrary finite ensemble E, does δ=χ(E)−χ(ΦE)→0 force one common EB channel with prior-average trace error at most a dimension-independent g(δ)→0? The construction here has δ=[log D_K−log d]/L, which is large. The reservoir construction therefore cannot simply be relabelled as a counterexample to this information-loss version.

## Reproduce the checks

Use the versions in `requirements.txt` or compatible versions. The recorded environment was Python 3.13.5 on Linux. From this directory:

```sh
OPENBLAS_NUM_THREADS=1 python -O verify_construction.py
OPENBLAS_NUM_THREADS=1 python -O verify_finite_design.py
```

Both scripts write their receipts next to themselves. To retain the distributed receipts unchanged, run a copy of the package. Checks use explicit exceptions, not `assert` statements.

`verify_construction.py` completed 112 checks: exact combinatorial identities, exact low-order moments, full-domain channel fixtures, complex family identities, decoder, global-cloning and idempotence negative controls, and rational parameter bounds. `verify_finite_design.py` completed 44 checks: complete finite ensembles, moment matrices, attainable decoded state-estimation fidelity, and finitely many basis fixtures. Maximum floating residuals were below 4.45e−15 and 1.45e−15. The universal quantifiers are proved analytically, not certified by the finite checks. No proof assistant or external referee was used.

## Source revisions and ingestion

Astra was read at `8aed7fd74eb14622ed5a0a3635a799374296e32a`; openai/math at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. `SOURCE_REVISIONS.json` distinguishes complete wrapper reads, selected original-proof reads, and merely identified source paths. No raw-byte source hashes are invented.

At the pinned Astra revision, `00_START_HERE.txt` still routes through topic TSVs and current review wrappers. Its retrieved ingestion aids are static session and bridge templates. `SESSION.json` and the files under `bridges/` use those schemas as a local append-only handoff. **Nothing was written to either repository, no card status was changed, and no historical evidence was overwritten.** A future ingestion should create a new uniquely named record and preserve all earlier sources; it should not silently revise an existing claim.

`AUDIT_LOG.md` records implementation failures and discarded approaches. `history/` preserves earlier diagnostic scripts and receipts, not additional independent validation. `CLAIMS.json` records the logical dependencies and non-implications. `MANIFEST.sha256` hashes this local package, not the external source repositories.
