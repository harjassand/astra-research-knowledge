# Whole inactive states and the actual noisy classical interface

[Available-return guide](README.md) · [Exact incomplete source](P1_FIXED_FACTORY_20261106_RETURN.txt) · [Resource accounting](resources-and-entangled-family.md)

## Permanent cells avoid random inter-site switches

For an open chain, at most `NB` permanent source cells and `NB(B+1)/2` candidate rails cover every interval of length at most `B`. Source cells use separate registers and fixed lanes and finish before site selection. The sampled partition changes classical command distributions rather than turning inter-site source couplers on and off. Quantum preparation maps include noisy command injection, quantum gates, idles and discarded workspace.

Each site selector is a fixed noisy circuit consuming at most `K=B(B+1)/2` candidate rails. It may entangle candidates or choose the wrong input. Every actual control wire, gate and idle is included in its map.

Conditional on the intended partition and acquired parameters, private source commands are sampled independently and never control a selector; selector addresses depend only on the partition. Every inactive source's whole averaged output is exactly product identity, including intervals crossing intended block boundaries. Contracting those independent identity factors into the actual selectors leaves a tensor product of local selector channels acting on each compensated active block.

Identity one-site marginals are insufficient: an inactive Bell pair can retain cross-block correlations exposed by faulty selectors. The entire averaged inactive state must be product identity, and private command records/garbage must be discarded or their actual correlated extension retained in the output specification.

## A finite palette of actual outputs

A trace-norm `gamma`-net of pure projectors with physical outputs within `gamma` has a convex hull containing the interior state body `rho>=a I/d` when `2 gamma(d-1)<=a`. The excerpt proves this with support functions and chooses fixed finite-template margins.

The palette covers both compensated active states and exact inactive identity. Classical convex feasibility finds nonnegative command probabilities with rounding slack. The derived local selector channels satisfy the accepted inverse-radius contract; the resulting known positive states can be prepared by the actual palette. No inverse channel acts on arbitrary unknown quantum inputs. Increasing global accuracy changes classical mixture descriptions rather than growing coherent synthesis precision or quantum lifetime.

## Noisy classical computation and final commands are included

The reported classical-only controller remains diagonal under the specified basis gates and Pauli faults. Repetition-five gadgets copy all coordinates into private columns before evaluating majority/gates, then apply a second restoration stage. The source supplies correctness on valid inputs and validity on arbitrary inputs with arbitrary lower-level syndromes. The recursive bound `q_(ell+1)<=A q_ell^2` yields polylogarithmic overhead in the requested logical discrepancy.

Protected fanout and separately restored descent produce local-stochastic raw command errors. The accepted ternary history-erasing regenerator bounds replacement discrepancy by `q_c alpha^h`, yielding `O(p)` residual root channels. All physical source and selector maps include those root errors. Independence belongs to the explicitly bounded comparison process, rather than being assumed for actual correlated control histories.

Encoded copies, descent, roots, routes, storage, gates, time and reset count. No final setting bit is perfect. Actual probe/capture randomness, capped extraction timeouts and acquired shared component parameters are included in the available operation. The original proof and executable checks are pending delivery; Capital did not rerun or independently audit the construction.
