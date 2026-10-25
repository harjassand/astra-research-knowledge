# The binary trace-entropy transfer cannot be extended to three positive sources

25 October 2026. Exact nearby counterexample to an overbroad mathematical
extension. This is not a WH3 counterexample or a matrix-SDPI separation claim.

For scalar entropy s(t)=-t log t, every a,b,c>=0 satisfies
s(a+b+c)-s(a+b)-s(a+c)-s(b+c)+s(a)+s(b)+s(c)>=0.
For positive arguments this is the third finite difference of s, equal to
integral_0^a integral_0^b integral_0^c [1/(u+v+w)^2] du dv dw>=0.
The integrable corner singularity and boundary cases follow by positive
regularization or continuity. The combination is balanced in each of a,b,c.

Take three real qubit trine projectors Pi=|psi_i><psi_i|, with
psi0=(1,0), psi1=(-1/2,sqrt3/2), psi2=(-1/2,-sqrt3/2).
They are positive, have unit trace, and sum to(3/2)I2. Every pair has spectrum
(3/2,1/2), while each individual projector has spectrum(1,0). Consequently the
same balanced matrix trace-entropy expression is
(3/2)log(3/4)<0.
Thus a universally valid balanced THREE-source scalar entropy inequality can
fail on2x2 matrices. This is a precise obstruction, not just lack of a proof.

Faithfulness does not repair it. Replacing every Pi by Pi+epsilon I gives the
exact expression
2s(3/2+3epsilon)
 -3[s(3/2+2epsilon)+s(1/2+2epsilon)]
 +3[s(1+epsilon)+s(epsilon)].
It remains negative for sufficiently small positive epsilon by continuity; the
companion outward-interval certificate checks the fixed epsilon=1/100.

The binary testing-measure theorem is therefore sharp in its source-count
qualification. It provides an abstract scalar representation for TWO fixed
positive operators and their nonnegative mixtures, not a common scalar model
for an arbitrary family. The three-source obstruction does not contradict the
older arbitrary-classical-channel/qubit-reference GLOBAL MI theorem: that
statement has a different functional and permits a modified prior. Nor does
this example establish a t log t fixed-prior matrix-SDPI separation, which would
require an actual compatible channel and prior.

Historical novelty is not claimed. The purpose is to prevent an invalid
receiving use of the new binary transfer and to identify the genuinely
multi-source noncommuting frontier of the coherent WH3 construction.
