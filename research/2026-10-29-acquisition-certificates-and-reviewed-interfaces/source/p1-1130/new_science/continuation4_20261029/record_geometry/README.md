# Preparation boundaries and actual finite-mean escapes

29 October 2026. Existing Astra P1 record-geometry role; no new branch or pool.

The main new result is FOUR_STATE_UNIVERSAL_PREPARATION_OBSTRUCTION.md.
An unknown family of four-state reversible kernels shares a known uniform
microscopic equilibrium and a common Doeblin constant of 3/8. Yet every
visible-only stopping rule exact for the same nontrivial microscopic tilt
throughout this family has infinite expected duration on its iid-visible
members. A rare-swap coupling and optional sampling prove this without
assuming higher stopping-time moments. Matching the completion-label mean
and the mean after one additional actual call already suffices for the
obstruction. A uniformly geometric finite-error construction is included
as a strong ordinary comparator.

REVERSIBLE_SCENERY_PREPARATION_BOUNDARY.md gives an independent known-kernel
obstruction, allowing even full microscopic observations. For the reversible
random walk on iid scenery, exact preparation has infinite mean. Finite
endpoint error epsilon requires mean native calls at least
(1−o(1))a^4/(64 pi² epsilon²). No matching upper bound is claimed.

ORDINARY_FINITE_MEAN_ESCAPES.md gives concrete sufficient interfaces:
independent baseline rejection, exact reverse label closure, entirely frozen
disorder with a common visible baseline and integrable hitting times, and
full finite-state recognition for the classical unknown-chain tree sampler.

PRIMARY_PREDECESSORS.md records inspected primary sources and their scope.
Historical novelty is unresolved. No apparatus or practical speedup is
claimed.

Run check_four_state_obstruction.py for the exact model checks. The saved
result contains 16 kernel fixtures and all 676 deterministic visible stopping
policies through three calls, with 2,028 exact first-order response checks.
The arbitrary-time impossibility is proved analytically, not by enumeration.
The JSON output pins its source and companion proof hashes; the manifest
pins all deliverables in this directory.
