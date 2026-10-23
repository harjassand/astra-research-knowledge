# Audit of the finite compiled-library actual-risk theorem

Audited source: `../COMPILED_CONTROL_ACTUAL_RISK_THEOREM.txt` (24 October 2026). This is a proof-scope check, not a claim about the still-open inequality for all smooth bounded controls.

## Kernel, rank, and uniform constant

Conditioned on the stated exact active-zero-risk support theorem, the fixed-kernel step is sound. If `v in ker W_j(g0)`, positivity of the integrated death effect gives zero death rate throughout the primitive for initial state `|v><v|`. The support lemma then confines the trajectory to the safe face and makes the unknown coupling term `V` annihilate it. With the same initial vector, waveform, and local detector instrument, the trajectory is therefore unchanged at every `g`; reversing `g,g0` gives equality of kernels, not only inclusion. Zero `a`-occupation similarly gives `<v,A_j(g)v>=0`. Since `A_j(g)>=0`, this implies `A_j(g)v=0` and all cross-blocks with the kernel vanish.

The rank argument handles all finite-dimensional degeneracies. The kernel may differ between primitives, and its dimension may be any value from zero to the full active dimension; for each primitive it is fixed across the compact parameter interval. On its nonzero orthogonal complement, `W_j(g)` is positive definite at every `g`. Continuity of the finite-dimensional least eigenvalue and compactness then give a strictly positive minimum. If the complement is zero, `W_j=0` and the support lemma forces `A_j=0`; assign that primitive gain zero. Thus `A_j <= t_j Pi_j <= (t_j/lambda_j) W_j` is valid in every case. It is essential that the kernel is certified fixed; continuity alone would not prevent a positive eigenvalue from closing at a rank change.

The effect inequality tensorizes exactly: `A_j tensor I_R <= C_j W_j tensor I_R` for any untouched reference `R`, including entangled inputs. This does not cover a new active register, pulse, meter, or routing mechanism that is absent from the fixed library. Routing an old reference into the active register is covered only when that routing is part of the specified physical interface (and any sample interaction during it is charged).

## Adaptive composition and scope

For every history and selected primitive, the input live substate is positive and the operator inequality applies to it, whether or not that substate depends statistically on `g`. Summing its trace against the two effects over histories and attempts bounds expected accumulated `a`-occupation by `C_library` times the sum of first-death increments. Those increments are disjoint because death is absorbing. Monotone convergence extends the result to an unbounded sequence of attempts. The policy itself must be one physical, parameter-independent history-to-action rule; the theorem does not grant a controller direct access to `g`. All source acquisition, cleanup, readout, and reset actions that use the sample must be included. A mid-primitive stop is covered only if the truncated operation and cleanup are themselves represented by library primitives.

This proves a finite fixed-library result, not a result for an arbitrary finite program that can synthesize a changing family of durations, amplitudes, active arities, or measurements. The constant may worsen without bound as that library is refined. It also does not close the all-smooth-control window-domination question.

## Endpoint-risk factors in (7)--(9)

The substitution in (8) has the stated factor. From (7), `I_e,i = rho_i/gamma`, while (6) gives `I_a,i <= C_library rho_i`. Each of the two square-root terms is at most `sqrt(C_library rho_0 rho_1/gamma)`, yielding the factor `2 |Delta g| sqrt(C_library/gamma) sqrt(rho_0 rho_1)`. The maximum with zero is a valid trivial lower bound when the affine expression is negative.

For a binary test whose two error probabilities are at most `alpha < 1/2`, the output root fidelity is at most the classical root fidelity after the test, which is at most `2 sqrt(alpha(1-alpha))`. Combining this upper bound with (8) gives (9), with no missing factor of two. This is an endpoint statement: no risk condition at intermediate `g` is used. Uniform estimation at error `epsilon` supplies the binary test for any two parameter points more than `2 epsilon` apart. The argument presumes a common `g`-independent start, or that all earlier source experience is included in the same charged adaptive chain, and a completed returned-output test (nontermination is failure).

## Numerical-grid Lipschitz bound

The bound `||partial_g W_j|| <= 2 t_j ||V||` is valid under the specified terminal-death generator. Let `P_d = |dead><dead| tensor I`. The other terms of the generator leave `P_d` invariant, while the terminal jump gives `L^*_{g,s}(P_d) = gamma P_e`. Hence for the full CPTP evolution, including local working-register jumps,

```text
W_j(g) = integral_0^t_j gamma Phi^*_{j,g}(s)(P_e) ds
       = Phi^*_{j,g}(t_j)(P_d) - P_d.
```

Differentiate the final Heisenberg propagator by Duhamel. Its derivative inserts `i[V, .]`; the surrounding CPTP Heisenberg propagators contract operator norm and `||[V,O]|| <= 2 ||V|| ||O||`. Since `||P_d||=1`, integration over `t_j` gives the claimed bound. This identity avoids the looser direct integral estimate that would introduce a spurious `gamma t_j^2` factor. Given an independently certified fixed projector and a validated ODE operator-norm error, the stated grid subtraction is then valid by the nearest-node Lipschitz bound. It is conditional on those certificates; it is not an oracle for discovering the kernel or cheaply validating arbitrary black-box waveforms.

## Disposition

No counterexample found to the finite-library theorem or the endpoint constants at its declared interface. The conclusions remain conditional on the active-zero-risk support lemma and on each primitive being an actual finite-dimensional instrument with the stated local-jump form. No numerical value for `C_library`, favorable example, all-smooth-control theorem, or novelty claim follows from this audit.
