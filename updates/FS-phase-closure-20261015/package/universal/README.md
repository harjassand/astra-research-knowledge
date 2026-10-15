# Astra: continuum profile-storage obstructions

Research checkpoint: 15 October 2026.

**No universal quasiconvexity proof and no negative compatible closed cycle are claimed.**

Start with `UNIVERSAL_PROFILE_OBSTRUCTIONS.md`. It contains complete arguments for first-derivative local-storage rigidity, the oriented critical trace obstruction, exact failures of a Poisson-extension candidate, and convex timing elimination. `RESTART.md` states the unresolved mechanism and excludes rediscovery of the same failed approaches.

## Reproduce the exact checks

The standalone scripts require Python 3 and SymPy:

```sh
python verify_universal_obstructions.py
python certify_free_cycle.py
```

The first writes `universal_verification.json` and checks ten finite-algebra groups. It does not use optimization outputs or prior verification files. The second reconstructs a five-profile compatible periodic cycle from `rational_free_cycle.json`, computes all moments, and minimizes all four affine directions using rational arithmetic. It proves

\[
19/20 < \Delta_G(D\varphi)/\mathbb E|D\varphi|^4 < 24/25.
\]

This is a **positive** exact witness, not an estimate of a global minimum. Its rational durations are not asserted to be exactly optimal. It does not improve the earlier campaign's positive witness near 0.615.

The supplied logs record execution. `prior_replay.log` records the nine-group replay of the preceding profile-circulation package, including all 32,805 finite-library inequalities. That replay does not turn a finite graph into a continuum theorem.

## Exploratory data

`exploration/` contains the actual discovery scripts and retained JSON states. These require NumPy, SciPy and/or PyTorch in addition to SymPy; they are not dependencies of the standalone finite verifications.

- `free_cycles_N3_K5.json`: three completed 1,200-update fixed-G runs. Every geometry uses five complete complex profiles with frequencies -3 through 3 and all four affine backgrounds. Durations are reoptimized at fixed geometry/background.
- `fullcone_cycles_N3_K5_s0.json`: four completed outer rounds. `fullcone_cycles_N3_K5_s1.json`: two completed outer rounds. Each outer round uses 900 profile updates. Only these six saved rounds are evidence; a planned longer batch was interrupted.
- `poisson_*.json`, `fullcone_c*.json`: candidate-storage residual searches. **Negative residuals are not negative compatible closed-cycle energies.** Exact replacements for two decisive failures are in the main verifier.

The acoustic cone solver uses the exact algebraic Gram structure, but its numerical matrices are not exact general certificates. Only the explicitly reconstructed integrand G's acoustic certificate is claimed exact. Search coefficient floors, regularizers and finite iterations are described in the proof note and source.

`manifest.json` lists SHA-256 hashes and byte sizes of files in this checkpoint, excluding itself. No third-party research manuscripts, fonts, credentials or external account content are redistributed. No repository write was performed.
