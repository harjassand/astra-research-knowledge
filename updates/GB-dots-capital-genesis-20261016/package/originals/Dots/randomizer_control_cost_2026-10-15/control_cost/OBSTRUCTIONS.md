# Exact obstructions to weaker control interfaces

These are finite-dimensional counterexamples or elementary support arguments. They are not empirical device claims.

## 1. A tiny coherent error has no positive exact-ideal CP branch

Let the reference gate be identity and the actual gate be `U_theta=exp(-i theta X)`, with `theta` nonzero modulo pi. Its channel has rank-one Choi matrix `|U_theta>><<U_theta|/d`.

If `Ad(U_theta) - s Id` were CP for any s>0, positivity would force the Choi vector of identity into the span of the Choi vector of U_theta. That would require U_theta to be a scalar multiple of identity. It is not. Thus no decomposition `(1-epsilon) Id + epsilon R_bad` exists for any epsilon<1, even as theta tends to zero.

Explicitly, let u and v be normalized Choi vectors of U_theta and I. Project v orthogonally off u and normalize the result to w. Then

`<w|[|u><u|-s|v><v|]|w> = -s sin(theta)^2 < 0`.

Ordinary average gate infidelity is only `(2/3)sin(theta)^2` for this qubit unitary. Small infidelity, and even small diamond distance, therefore does not supply the exact-ideal CP contamination parameter. A separate coherent-action theorem is needed.

The same obstruction is not limited to unitary noise. For amplitude damping with p in (0,1], Kraus operators are `K0=diag(1,sqrt(1-p))` and `K1=sqrt(p)|0><1|`. Identity is not in their linear span. Its Choi vector is therefore outside the channel's Choi support; no nonzero exact identity CP subchannel exists. This does not deny the physical jump/un-jump instrument. Its no-jump operation is a filter, not an exact ideal operation.

## 2. Perfect reduced data controls can reveal the frame to one bath qubit

Take data D and a bath qubit B initially in |0>. The laboratory Hamiltonian is fixed,

`H=J Z_D Z_B`.

Choose a private uniform initial bit f. Implement the intended initial data frame X_D^f together with the extra bath action X_B^f. At every intended telegraph update, apply `X_D X_B`. At the end, remove only the correct tracked data frame `X_D^(f+N mod 2)`.

Every control has EXACTLY the desired reduced data action, on arbitrary data-bath inputs: a bath-only unitary disappears under partial trace. Thus a metric inspecting just the data control can report zero error. However the bath carries the current frame bit. Because `X_D X_B` commutes with H, for every count and every update-time trajectory the corrected joint output on bath input |0> is

`exp(-i Jt Z_D)|psi> tensor |f+N mod 2>_B`.

There is no randomization-rate suppression. On data input |+>, the trace-norm error from the identity output is `2|sin(Jt)|`, independent of gamma. The bath is only two dimensional; no hidden infinite record is used.

This invalidates the proposed interface “good gate = correct data Pauli tensor some bath map” if that bath map can depend on the chosen private operation. Its bad CP effect could be declared zero under that weak definition, while the claimed suppression fails. The full joint/private compiler premise is substantive.

## 3. Marginal CP effects do not imply a spatial product

Let an independent hidden classical coin Z be one with probability epsilon. If Z=1, apply local faults to every parent; otherwise apply none. Every parent’s full-horizon fault effect is exactly `epsilon I`. But for any nonempty selected set,

`effect(all selected parents faulty)=epsilon I`,

not `epsilon^|S| I`.

The causal uniform-hazard premise excludes this example: after a first observed fault, the next conditional fault probability is one. A marginal per-location CP effect cannot be substituted for a causal instrument bound or an actual joint-subset theorem.

## 4. A character-effect bound does not establish zero-character correctness

Set the reference interaction to zero and introduce the local residual `R_i(f_i,eta_i,t)=uX`, independent of every private coordinate. Then the actual propagator is `exp(-iutX)` for every seed. All nonzero initial-frame Fourier coefficients vanish. Every nonzero-character effect bound is therefore satisfied, including a zero bound, while the memory undergoes a nontrivial rotation.

This lies within the algebraic “depends at most on its own seed” residual class. It is excluded by the stronger initial-frame conjugation/character-to-memory-support requirement. The coherent residual theorem in REPORT.md deliberately distinguishes these two levels.

## 5. Positive-width controls cannot realize every ideal Poisson path serially

For any positive aggregate rate and positive gate width, an ideal Poisson process has positive probability of two arrivals closer than that width, and positive probability of more updates than any finite reservation can hold. A finite-width serial implementation must specify its overlap/overflow behavior.

Dropping or delaying events changes the control law. A valid comparison either rederives the reference theorem for that new law, charges the exceptional parent locally with its actual probability, or uses a pre-separated finite schedule. Replacing the update count by its mean or merely adding “one gate error per expected pulse” does not establish path feasibility or the same telegraph kernel.

Even accepted nonoverlapping schedules require a joint waveform error bound: a non-Pauli intermediate rotation can change the coupling throughout the ramp. Endpoint compensation by itself does not make that difference vanish.

## 6. What the existing noisy-core theorem does and does not supply

The existing qualified noisy-Clifford-core model supplies global control-character subset effects under its fixed-core, full-support conjugation/deletion premise, with exact or separately qualified wrappers and protected records. For a fixed schedule, union over control slots gives a control-only parent parameter `sum_e a_e^2`.

It does not automatically supply mixed weak-telegraph/control-character effects. A zero-control-character branch can still filter the bath in a path-dependent way; separately proved subset bounds cannot simply be multiplied. Nor does randomizing each wrapper with another unqualified wrapper close the implementation model.

The coherent residual theorem gives a nonrecursive alternative when the actual whole-controller Hamiltonian already satisfies its common-dilation and initial-frame covariance conditions. If neither that model nor the exact CP-contamination model can be established, the honest output is the remaining interface obstruction, not a paid spatial threshold.
