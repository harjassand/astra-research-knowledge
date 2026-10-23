# Actual receiving use of accumulated science

## What was used and what changed

The Cycle8 intrinsic atom theorem and Cycle9 one-mark projection were already
completed source. They supplied a real coloring for one actual degree-two root,
with distinct neighbor colors and at most one far-repeat flag. Cycle9 did not
justify independently choosing profiles at every attachment site. The new
one-message induction turns this exact guarantee into a global bounded-component
operation. That expands the proved intrinsic class to all connected bridgeless
chordless width-two degree-four graphs, with arbitrary block depth and adjacency
of marks. This is the substantive receiving consequence.

The fixed tables were read and reused. Their old closure search was not rerun.
The inherited exact coordinate LS decoder was reused on NEW full original
supports; its incidence mechanism is established Hessian recovery machinery.
The inherited signed-amplitude coordinate lower is used only to establish the
coordinate minimum on the new class. It supplies no new all-real lower bound.

## Native inputs and operation

`inputs/adjacent_marks_mixed_theta_57.json` is a native 57-vertex, 73-edge,
seven-block graph with depth three, actual consecutive marks, mixed path
lengths and both marked-root cases. `inputs/mixed_non_theta_adjacent_marks.json`
is a native 30-vertex, 39-edge, seven-block graph with depth two. Its original
nine-vertex non-theta atom has actual adjacent marks 6 and 8; its C4/theta/C3
attachments force a real message to be used. Native preparation receives n
and the original edge list. Construction records are provenance, not an
expression oracle consumed by the main algorithm.

The two constructions on the first graph use identical supported coefficients
and identical four-column noise. In original IDs, the exact free diagonal is
((37i+11) mod 31 - 15)/13; the coefficient on ordered edge u<v is
((23u+17v+5) mod 43 - 21)/17; E_ij is
((11i+7j+3) mod 19 - 9)/101. All individual quantities are serialized as
exact fractions in results/RECEIVING.json.

Each operation constructs all original DX, adds E, performs noiseless and
noisy reconstruction, projects the action residual and records sparse output.
No reduced graph or unknown-entry shortcut is used. The actual source has
cheap explicit matrix entries, so these checks do not show a runtime advantage
over direct assembly.

| Operation | Noise norm squared | Matrix Frobenius error squared / noise squared | Nonstar components | Projected numerical residual |
| --- | --- | --- | ---: | --- |
| Main reset on 57v theta graph | 6840/10201 | 8673097/12312000 | 2 | Exactly zero |
| Explicit theta on same graph, D and E | 6840/10201 | 1246573/2052000 | 4 | Exactly zero |
| Main reset on 30v mixed graph | 3618/10201 | 132977/260496 | 2 | Exactly zero |

All have largest bichromatic component order five and maximum cut balance
Gamma=6/5. Raw observation residuals are nonzero and retained separately.
The theorem gives squared Frobenius bound 3+sqrt(5), independent of these
observed ratios. The mixed graph's actual compulsory message is from edge
(6,11), at outgoing cut 11, forbidding color 3 in child block 5. The next
child's actual neighbor support omits that color.

## Independent verification and its boundary

The independent verifier imports only the Python standard library. It
reconstructs maximal blocks using articulation deletion rather than the
producer's low-link algorithm; independently expands original support
expressions; enumerates all cycles of these small blocks for chordlessness;
constructs width-two elimination bags; recomputes actual color supports,
flags and message transitions; and verifies every global spider center/arm.
Its inverse uses exact Fraction normal equations, not subtree sums.

All original coefficients, actions, noise, observations, outputs, projections,
raw residuals and exact error inequalities passed. The three receiving uses
are source-bound in verification/independent_receiving/VERDICT.json. The
gate also binds the reviewed PROOF.md bytes. No old scientific suite or
producer receiving program was rerun to perform this independent check.

This is internal proof review plus independent finite realization checking.
It is not historical-priority assessment, external acceptance, a downstream
application benchmark or evidence that Max has read or integrated the result.
Transport receipts are external to this frozen archive and document a
different event.
