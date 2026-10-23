# Prepared-row rare-event frontier and robust CQ anchor

This update preserves two independent source units with distinct premises and claims. The selected source bytes and their provenance are recorded in the [source manifest](source_manifest.json).

## 1. Rare-event frontier acquisition and spatial obstruction

The [frontier acquisition source](source/rare_event/FRONTIER_ACQUISITION.txt) assumes a supplied finite-horizon, topologically ordered network of `M` local gates over `q`-valued wires, with maximum in-degree `a`. Unknown local rows have fresh conditional noise, remain unchanged during calibration, and have entries that are either zero or at least a known `p_min`. Preparing, sampling, resetting, and reading each component row is an allowed paid operation with cost `C_row`; it is stronger than observing only whole-network trajectories. The architecture and its fresh-noise premise are supplied. No architecture acquisition is claimed.

For at most `R = M q^a` unknown rows and `D = M q^(a+1)` entries, the source gives the sufficient per-row sample count

`N >= 3/(p_min eta^2) log(2D/delta)`.

With probability at least `1-delta`, all entries satisfy the stated multiplicative bounds and the empirical support is recovered. The source then uses exact rational backward message passing over at most `M q^w` states, where `w` is the width of a supplied, verifiable causal-frontier schedule. It constructs lower and upper tables for the true event probability; at a state with positive empirical message their ratio is `[(1+eta)/(1-eta)]^(M-k)`. Taking `eta = epsilon/(8M)` gives a computed ratio at most `1+epsilon`. This is a confidence-qualified interval for the unknown model. It is not an exact true-model Doob sampler. Direct message passing is the stronger conventional output. The stated polynomial acquisition regime also requires fixed `q,a`, `w=O(log M)`, inverse-polynomial `p_min`, polynomial `C_row`, and the other encoded costs. Optimal schedule discovery is not free, and the bound does not establish physical affordability or advantage.

The separate [spatial path obstruction](source/rare_event/SPATIAL_PATH_OBSTRUCTION.txt) considers known local updates on a path, including fair-coin overwrites and deterministic radius-one Boolean updates. A universal polynomial-time relative-`1/4` catastrophe estimator with confidence at least `3/4`, even on strictly positive probabilities in the stated class, would imply `RP=NP`. This rules out inferring a universal certificate guarantee from spatial locality and treewidth one alone. It is not a sharp causal-width lower bound for every compiled program and does not cover additional restricted dynamics.

## 2. Robust CQ anchor localization

The [checked payoff-repair source](source/cq_anchor/CHECKED_CQ_ANCHOR_PAYOFF_REPAIR.txt) is the exact prerequisite captured under dispatcher receipt `U_IN_PROGRESS_mission_unit_0638_20261024`. The later [robust CQ anchor result](source/cq_anchor/ROBUST_CQ_ANCHOR_LOCALIZATION.txt) is the final file captured under receipt `U_IN_PROGRESS_mission_unit_0658_20261024`; it is distinct from the unavailable originally named `_DRAFT` path and pin. The manifest records this identity correction and both source hashes.

The robust result assumes the two-sided functional order

`e^(-s) tau0_(k|c) <= tau_(k|c,X) <= e^s tau0_(k|c)`

on the full Bob algebra for supported `X,k,c`, together with the complete original preselection support condition `R2`. It locally normalizes on that support and then drops Alice's near-identity conclusive filter to obtain the Bob-only event. The source provides event-mass and conditional-loss bounds under these premises. Event rarity or a measured classical table does not supply the required operator order. Its repetition consequence is conditional and restricted; useful nonredundant anchor families and general floor/operator-order acquisition remain open. No general advantage is established.

## Provenance and review boundary

The two CQ source receipts are marked `IN_PROGRESS` and describe individual source reads, not an atomic tree freeze. The rare-event pair arrived with user-specified local source pins and no dispatcher receipt; both source files and copied bytes match those pins. A bounded upstream documentary review reported that the queued summaries matched the source scopes and identified the missing payoff-repair prerequisite. It did not certify proofs or review this authored integration. This handoff preserves and summarizes the selected sources; it does not perform scientific script execution, proof replay, novelty assessment, physical validation, or research-model acquisition. Repository and PR integrity checks establish the publication scope and byte preservation only.
