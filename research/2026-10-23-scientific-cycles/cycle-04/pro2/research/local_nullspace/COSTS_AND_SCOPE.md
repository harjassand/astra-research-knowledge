# Local-nullspace contribution cost and receiving scope

Read the owned next_bounded_degree.md and exact contract from the prior proof.
No prior witness, NIST, scalar-moment or molecular calculation was replayed.
The first recorded clock for this contribution was2026-10-21 20:16:55 UTC.
Mathematical reasoning, source reading, authoring and communication costs were
not fully instrumented and are additional, not zero.

One exact Python standard-library test body ran successfully. It covered
n=1,2,3,4,5,6,7,17,64,257 with the same formula and no optimization or tuning.
Body wall0.18110846800118452 seconds, CPU0.181035796 seconds, peak process
RSS13369344 bytes. Imports/interpreter start are outside the body timer.
Per-case timers are subsets, not additive overhead. No failed numerical run,
precision sweep, package installation, GPU use, spending or outreach occurred.
results.json is the unchanged receipt.

The exact seed is X=Z/sqrt(2), with integer period-six Z. Tests never replace
this by unnormalized Z: physical row energy is exactly one and actual action
noise squared is ||E0||F^2/2. The decoder's exact symbolic tests work on scaled
observations sqrt(2)Y. A floating implementation must charge that scaling,
query rounding and certified solver/local-map residuals. No such floating
implementation or original-input performance benchmark is claimed here.

decode_scaled in squared_path_decoder.py is an actual O(n)-arithmetic decoder
using cached local matrices of order at most four and a pentadiagonal LDL
solve. Four physical actions, O(n) seed/action storage, graph ordering/preparation
and acquisition costs remain required. Rational bit lengths can grow with n;
the arithmetic count is not a constant bit-cost claim. The scalar condition
number is analytically at most32/7, so a separately certified numerical solve
is plausible, but has not been benchmarked here.

The checked error bound is output Frobenius, stronger than the required
operator bound. Saved finite cases do not prove all sizes; the proof's exact
sum of squares and local Gram polynomials do. The finite tests do not constitute
an independent checker because they import the construction module. Parent
may use another contributor to challenge the algebra or receiving implementation.

Changed scientific boundary: the accepted all-design q3 squared-path lower
now has a matching explicit q4 stable decoder, and so does every support with
a supplied bandwidth-two ordering. The entire TW<=2, Delta<=4 question remains
unresolved by this contribution. A claim that every such graph has balanced
(2,2) neighbor colors is false: the admissible three-page book forces(3,1).
Long balanced ambiguity paths and unequal-gain localization are not excluded
by local full rank alone. These are retained restrictions, not silently
weakened hypotheses.

Historical priority is not established. This is a new construction relative
to the supplied owner checkpoint and actual receiving use of its lower family.
