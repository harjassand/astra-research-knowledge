# Separate acquired-block feedback extension

Outside the accepted 18:24 source freeze and archive. Independent review is
currently pending; previous receipts do not cover these files.

Current result: an offline finite-horizon time-dependent acquired-block
Markov policy/value certificate for an explicit-state generative simulator.
Ordinary exact coarse-MDP Bellman planning is the planner, not a new DP method.
The transition operator certificate is acquired from retained observations.

- **Current polynomial admission:** `BLOCK_COMPARISON_PROOF.md`,
  `check_block_comparison.py` and `block_comparison_results.json` acquire
  m r² local residual bounds; `replay_polynomial_feedback.py` independently
  receives the count/probe arithmetic and exact DP/packed interface.
  `polynomial_feedback_received.json` is the current result.
- **Historical exponential alternative:** `check_feedback_norms.py` and
  `feedback_norm_results.json` enumerate m^r one-step policies.
  `plan_feedback.py`/`feedback_plan_results.json` are trusted-generation
  diagnostics using that alternative, not the final polynomial receiver.
  All historical acquisition remains paid.
- `check_feedback_algebra.py` exhaustively checks small exact cases.

Original interface: n4096, r4, m2, L24, epsilon .02, delta .001. Initial law
is block-uniform and terminal reward block-constant. The output does NOT
compete with microscopic or arbitrary history-dependent policies. Stored
block map, policy and original task masks cost 2060 packed bytes in addition
to the 468-byte coarse model, certificates/counts and metadata. A simulator
rollout must retain/observe destination microscopic labels and pay L forward
calls and L map/action lookups. Physical sensing/actuation is not supplied.
