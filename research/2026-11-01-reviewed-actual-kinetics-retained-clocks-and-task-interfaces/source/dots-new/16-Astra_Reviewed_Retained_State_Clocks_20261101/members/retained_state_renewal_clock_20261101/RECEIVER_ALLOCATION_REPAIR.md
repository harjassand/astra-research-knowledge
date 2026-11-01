# Allocation guard correction after the pending checkpoint

The pending recovery-v3 ZIP remains immutable at SHA
`da5b27e206bd5349428070e407b355acc7608a47044cd0b35aafd1e31f5c2c99`.
It was explicitly NOT a whole executable acceptance. Its receiver fixed deep
recursion/cycles, but the reviewer correctly noted that it built a child list
before checking its size and omitted already queued nodes from its nominal
allocation check. Mathematical endpoints and valid-input receiving were not
affected. That exact source/check/descriptor are retained in
`tree_guard_v3_history/`, and the complete pending ZIP remains unchanged locally.

Recovery-v4 appends children incrementally. Before each append it checks
`visited_nodes + pending_nodes + 1 <= 100000` and the depth-64 bound. List
length is also checked against the remaining global pending budget before its
iteration. Dictionary keys are checked one by one, with a separate 100,000-key
scan budget, including keys whose diagnostic values are ignored. No oversized
child list is constructed. Ignored diagnostic values themselves remain
untraversed, consistently with proof comparison.

Focused tests include a saturated pending-stack case and the ignored-value key
scan budget. All 2,503 original author checks and 22 guard checks were actually
rerun. The new current descriptor is `FROZEN_SHA256_RECOVERY_V4.json`. The
original scientific proof, all numerical formulas and task scope remain
unchanged. The replacement whole audit must bind this exact current source.
