# Algebraic completion of the quaternion controller oracle — 2026-10-29

## What changed
The generic fixed-template theorem is accepted at its mathematical scope: a rational35-coefficient quartic can be globally optimized to additive epsilon using exact finite random perturbations and a fixed universal-resultant/derivative construction, with expected polynomial BIT cost. Governing text: GENERIC_TEMPLATE_THEOREM_DRAFT.md (filename retained after acceptance), frozen by GENERIC_TEMPLATE_SHA256SUMS.txt. Receiving review: ../quaternion_algebraic_completion_audit_20261029/REVIEW_RECEIPT.json. The universal template is not implemented; this is not an executed efficient controller or a practical timing claim.

## Executed evidence and outstanding work
- A small rational perturbation of a known non-SOS Choi–Lam quartic produced exact degree40 critical shape and excluded all projective boundary rays. All28 real roots were isolated. Global value certification completed: global_certificate_fast.json gives original-f gap1.29359831563e−5 < requested1e−4. Independent receiving review is pending.
- Original900s refinement timed out after15 roots. A durable-cache rerun preserves root progress; its redundant slow run was interrupted after the fast certificate completed. The exact library fast=True refinement removes the nearzero bottleneck (root15:0.021s versus>216s default). The fast successor uses separate partial/final files, avoiding concurrent-write confusion. A later exact fast=True initial-isolation diagnostic completed all28 roots in0.052s; see EXECUTION_COST_CORRECTION.md.
- macaulay_template.py implements classical220/112 matrix construction. Exact structured tests pass, including nontrivial dense factorable cubics against a principal-minor product reference. One actual-bank scalar resultant atlambda0 executed exactly in44.76s. These are implementation checks, not a generic resultant-polynomial/derivative optimizer.

## Dependencies and scope
Builds on accepted ../quaternion_oracle_controller_20261029 SOS/grid/FTPL core and the accepted one-bank algebraic certificate. None is superseded. The actual complete runnable all-input fallback remains the rational grid. The new theory removes inverse-accuracy dependence at a fixed-template mathematical scope; it does not establish useful constants, worst-case fast hardware clocks, empirical superiority over equally informed local optimizers, or historical novelty for resultant optimization. Candidate-dependent solver time/retries remain a physical-source privacy obligation.

GENERIC_RESULTANT_WORKING.md records derivation history, not a competing governing claim. New Macaulay notes and Choi–Lam data are separate from the accepted generic theorem receipt unless separately reviewed.

EXPECTED_BIT_CONTROLLER_COROLLARY_DRAFT.md is an additional author-only composition: fixed rational probe probability makes finite FTPL queries logarithmic-bit in the horizon, so the theoretical template yields expected polynomial-in-log-horizon computation per edge. It is a FIXED-COMPARATOR controller statement, not a replacement proof for the accepted drifting-frame master. Independent review is pending.
