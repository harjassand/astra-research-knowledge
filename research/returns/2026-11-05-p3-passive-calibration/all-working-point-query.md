# A chosen-deadline first-failure query from the all-working state

This separate [completed mathematical derivation](package/next2_root/early_allworking_bridge_notes.txt) extends the distribution question to **independent binary exponential edges initially all working**. It is not the [equilibrium-safe whole-curve theorem](reliability-curve-certificate.md), not a general interacting-port result and not an implemented or singly precomputed all-working curve.

The graph starts connected. Edge rates `a_i,b_i>0` are supplied, `gamma_i=a_i+b_i`, `A=sum gamma_i`, `g=min gamma_i/A`. For a supplied positive binary rational deadline T, the construction seeks a relative first-disconnection interval without inverse event-probability or lifetime execution cost. Static access is the priced all-terminal counting/conditional sampler, not a free arbitrary-predicate oracle. Natural mechanism completeness and physical rate acquisition remain separate.

## Early grid, forced snapshot and finite bridges

Choose N grid snapshots with width `delta=T/N` and `A delta<=alpha`. The probability G_T of a failed grid state satisfies `exp(-A delta)F_work(T)<=G_T<=F_work(T)`: after first failure, no refresh before the next snapshot has at least that probability. This is a relative continuous-to-grid correction, not an additive error that overwhelms a tiny failure probability.

Each snapshot law is product with down probability `a_i/gamma_i * (1-exp(-gamma_i j delta))`. Estimate each static failed-snapshot probability p_j, choose j proportional to p_j, sample that snapshot conditioned on failure, then generate its independent-component Markov bridges backward to the exact all-working initial state and forward to the remaining snapshots. If C is the number of failed snapshots, inverse multiplicity `1/C` is bounded and has mean `G_T/sum_j p_j>=1/N`. Finite relative static tolerances and conditional-path errors therefore cost polynomial N factors rather than inverse rarity.

The proof uses positive rational approximations to each tiny refresh probability, builds an **exact rational** two-state product chain and computes its snapshot/bridge laws with integer powers. Whole-path multiplicative distortion, conditional-sampler bias, proposal-weight distortion, concentration and the continuous-grid correction are explicitly allocated. Each forced path pays `O(mN)` component transitions, N predicate evaluations, static access, random bits and capped rejection.

## Late-time bridge and exact scope

A pointwise product-law comparison after a gap-scale burn B0 and monotone common-refresh coupling give, for sufficiently late T, `(1-alpha)^2 F_pi(T)<=F_work(T)<=F_pi(T)`. Here `F_pi` includes initial stationary failures: `F_pi=p+(1-p)F_safe`. The late branch uses the new genuine continuous-time stationary-safe certificate **with that certificate's own premises and static-access costs**. It does not substitute a fixed-tick chain's mean-matched generator for deadline probabilities.

The early/late split bounds needed grid size polynomially in numerical `g^-1`, inverse accuracy and log graph factors. Per-query work is polynomial in supplied graph/rate/deadline bit lengths, `g^-1` as a value, inverse accuracy and log inverse confidence, including the actual static calls. The supplied result has not been implemented. Adaptive chosen deadlines can allocate confidence over queries; a single materialized curve at every positive time still requires additional work and is not claimed here.

Physical accuracy is especially delicate at early all-working deadlines. Two redundant independent edges have first-failure probability of order `a^2 t^2`; an omitted simultaneous-failure intensity v adds order `v t`, an unbounded relative change as t approaches zero. The equilibrium-safe intensity/initialization error theorem is therefore not transferred to this start. Exact/structured model-error control or a declared minimum deadline is essential for physical relative guarantees. No arbitrary interacting local-port extension, hidden-cause exclusion, practical superiority or historical-priority finding is established. [Original package and status](SOURCES.json).
