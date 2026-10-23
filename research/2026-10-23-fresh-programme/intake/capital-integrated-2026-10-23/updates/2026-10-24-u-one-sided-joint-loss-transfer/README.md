# One-sided joint classical–quantum loss transfer — 24 October 2026

This selected foundational unit preserves the current one-sided actual-instrument theorem, its named finite-tensor, channel-minorisation and standard-form commuting dependencies, source-reported challenge/correction files, and frozen predecessor snapshots. The [source manifest](source_manifest.json) records 21 byte-verified files from receipts 0317, 0337, 0357, 0417, 0437 and 0457. The broad receipts themselves are retained by hash and are not copied.

## Result and exact assumptions

The [0457 theorem](source/U0457/next_unit/foundational/passive_lag/ONE_SIDED_JOINT_LOSS_TRANSFER.txt) concerns a finite two-player game with payoff in `[0,1]`, one-round question law `μ(x,y)`, and `m ≥ 1` independently drawn question pairs. Players may use arbitrary full-string joint local measurements and an input-independent shared resource. Alice has an actual success sub-POVM; Bob's original full-string complete POVM is left untouched. The selected event may depend on Alice's full input string and actual instrument outcome, including its steering of Bob's system, but not on Bob's input or outcome. Write `p = Pr(E) > 0`, `L = ln(1/p)`, and `α` for the selected conditional mean fraction of coordinate losses. No pointwise-constant success probability is assumed.

The referee channel must have a positive common component on Alice inputs of positive marginal:

`μ(y|x) = δ ν(y) + (1−δ) κ(y|x)`, with `0 < δ ≤ 1`.

The maximal such `δ` is `Σ_y min_x μ(y|x)`. Its auxiliary reset flag is not exposed to the players. Free inputs have `δ = 1`. Alice and Bob can be interchanged.

For either the finite-tensor model or the unrestricted commuting model, the construction produces a legal strategy in that same model, with loss `β`, satisfying

`β ≤ (√α + √τ)²`, `ε ≤ (√α + √τ)²`, and `τ = ln(1/p)/(δm)`,

so `p ≤ exp(−δm(√ε−√α)₊²)`. In the finite-tensor theorem use `ε* = 1−ω*`; in the unrestricted commuting theorem use `ε_co = 1−ω_co`. Each formula uses only its own model's base value and gap; no identification is made between them.

When `α ≤ ε`, the theorem also gives the exact binary-affinity consequence

`ln(1/p)/(δm) ≥ −2 ln(√(αε) + √((1−α)(1−ε)))`.

For zero selected live loss this yields `p ≤ (1−ε)^(δm) = ω_model(G)^(δm)`. The `ε = 1` boundary is understood by limits. The affinity corollary is not asserted when `α > ε`, where the exponential bound is trivial. This is a one-sided event theorem, not a result for an arbitrary repeated all-win event that can depend on both players' answers.

## Actual operation and proof boundary

The [finite-tensor selector](source/U0437/next_unit/foundational/passive_lag/ONE_SIDED_INSTRUMENT_SELECTION.txt), [channel-minorisation theorem](source/U0457/next_unit/foundational/passive_lag/ONE_SIDED_CHANNEL_MINORISATION_SELECTION.txt), and [current commuting extension](source/U0457/next_unit/foundational/passive_lag/COMMUTING_ONE_SIDED_INSTRUMENT_SELECTION.txt) supply the operation. Conditioning Alice's actual success instrument leaves an assemblage on Bob's same system and preserves the product conditional question channel. For each offline history, the construction rebuilds complete Alice effects from that assemblage while retaining Bob's actual complete POVM. The [prefix rebuild and source-budget note](source/U0457/next_unit/foundational/luna_truncation/PREFIX_LOCAL_M1_REBUILD_AND_SOURCE_BUDGET.txt) records the construction and its cost boundary.

The new transfer charges the changed classical input law and Bob-state ensemble together in one block-vector calculation. The selected average cost is `d_r + χ_r`, where `d_r = D(q_r‖μ_X)` and `χ_r = Σ_x q_r(x) D_A(ρ_(r,x)‖ρ̄_r)`. The [joint CQ challenge](source/U0457/next_unit/foundational/luna_truncation/JOINT_CQ_LOSS_TRANSFER_ADVERSARIAL_CHECK.txt) and [Doeblin telescope audit](source/U0457/next_unit/foundational/luna_mark_correlation/DOEBLIN_REFERENCE_TELESCOPE_AUDIT.md) are source-reported checks under their stated hypotheses. The [Radon–Nikodym gate](source/U0457/next_unit/foundational/luna_truncation/STANDARD_FORM_RADON_NIKODYM_GATE.txt) and [entropy gate](source/U0457/next_unit/foundational/irregular_time_sources/commuting_standard_form_entropy_gate.md) identify the standard-form operator and entropy inputs.

For the unrestricted commuting statement, the construction uses one common standard form, natural-cone vectors, Alice Radon–Nikodym effects in `N′`, and Bob effects in `N`. It does not assume a finite trace, matrix density, or finite-dimensional approximation. The [0437 commuting draft](source/U0437/next_unit/foundational/passive_lag/COMMUTING_ONE_SIDED_STANDARD_FORM_DRAFT.txt) is retained separately as a historical draft with then-unchecked imports; it is not the current asserted commuting theorem.

## Frozen chain and corrections

The [0317 measured-event allocation](source/U0317/next_unit/foundational/passive_lag/SELECTION_CQ_ALLOCATION_AND_PURIFIER_GAP.txt) records the original information allocation and open payoff-reconstruction gap. The [0337 HJW check](source/U0337/next_unit/foundational/luna_truncation/HJW_CQ_INPUT_SUBSTITUTION_GATE.txt) and mixed-state gate, then the revised [0357 mixed-state gate](source/U0357/next_unit/foundational/passive_lag/CQ_SELECTION_MIXED_REBUILD_GATE.txt), specify the legal reconstruction and the still-open selection-to-state-family identification at those snapshots. The [0417 measured-history repair](source/U0417/next_unit/foundational/passive_lag/MEASURED_HISTORY_GATE_AND_WHOLE_VIEW_REPAIR.txt) is preserved with the earlier [0357 version](source/U0357/next_unit/foundational/passive_lag/MEASURED_HISTORY_GATE_AND_WHOLE_VIEW_REPAIR.txt); neither is edited to make it appear that its broader gate was already closed.

The 0457 correlated-input artifacts preserve both a [factorisation falsifier](source/U0457/next_unit/foundational/lag_executables/CORRELATED_INPUT_FACTORISATION_FALSIFIER.txt) and the [shared-history repair](source/U0457/next_unit/foundational/lag_executables/CORRELATED_INPUT_HISTORY_REPAIR_CHECK.txt), with their checker sources retained as data. The repair concerns iid rounds with a possibly correlated one-round pair law and the stated shared-history factorisation; it does not cover arbitrary dependence across rounds. The checkers were not executed in this integration.

These later files strengthen a scoped one-sided chain; they do not refute or overwrite the earlier weaker statements. The programme review read the joint argument, central factorisation, entropy telescope and common-commutant construction with prior source exposure. That is programme judgment, not independent proof certification. The 0457 adversarial and dependency audits are source-reported, not newly rerun here.

## Costs and unresolved scope

For finite original Bob dimension `d_B`, each offline branch uses at most `d_B` quantum dimension, but the number of branches can be as large as `Σ_i |X|^(i−1)|Y|^(m−i)`. Posterior weights, assemblages and averages may therefore require exponential description and computation. Numerical precision, efficient acquisition and a practical compiler are not established. The commuting construction may be infinite-dimensional and changes Alice's algebra to `N′`; no finite representation of that resource is supplied.

General Bob-dependent selection remains open. No physical performance or external novelty is established. The existing Jain representation and mixed-target analysis already discuss the recent conventional comparison; generic finite-dimensional repetition is not presented here as a newly solved result. No scientific replay, new literature assignment, or producer repackaging was performed. The other work in the broad producer snapshots is untouched and is not represented as complete or halted.
