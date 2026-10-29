# Approximate success probability and complete-batch cap
2026-10-29. Additive clarification; frozen candidate files are preserved.

The lower bound needed for approximate training acquisition is stronger than the loose statement p>=Delta/2. Directly from the selected parameters,
 t_min-delta_inst
 =Delta-Delta*epsilon/64-Delta*epsilon/[128(n+1)]-Delta*epsilon/[256(n+1)]
 >=Delta/2,
for n>=1 and epsilon<1. The ideal acceptance probability p>=t_min; diamond instrument error at most delta_inst changes its success probability by at most delta_inst. Thus the actual approximate success probability is at leastDelta/2. There is no subtraction from an already-saturated Delta/2 bound. check_robust_budgets.py verifies this inequality in all72 exact cases; the displayed formula proves it uniformly.

An attempt means acquiring the ENTIRE n-success batch. Its expected waiting time is at most2n/Delta, not the waiting time for a single record. A cap of L=ceil(4n/Delta) therefore fails with probability at most1/2 by Markov. On failure discard all partial records and controller states from that attempt; the next attempt restarts n-success acquisition using fresh source calls. The r_cap independent complete-batch attempts have joint failure probability at most2^(-r_cap). Neither single-record caps nor retaining a partial failed batch are needed for this bound.

With fixed identical Choi inputs, fresh auxiliary samples and a stationary memoryless source, each attempt is an IID instrument sequence. Conditional on its outcome flag, every successful output has the same normalized state. Therefore its waiting-time/flag sequence is independent of the retained success-state product. Conditioning on complete-batch readiness does not change that product state. This is the specific factorization used here, not a general assertion that postselection or runtime never biases quantum outputs.
