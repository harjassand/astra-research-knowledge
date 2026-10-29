# An all-reference calibration margin for a synthesized release

30 October 2026, Brisbane. Root construction. General mathematical receiver;
ordinary weighted norm perturbation, with no historical novelty claim.
The finite source-margin compiler is separate from C's channel synthesis.
It does not alter or re-execute C's solver/certificate/producer files.

## Inputs and conclusion

L is a strictly positive invertible n-by-n stochastic reference channel.
K is a positive m-by-n stochastic release already qualified at budget c:

    J_K(rho,sigma)<=c J_L(rho,sigma)

for all admitted classical-quantum pairs and all finite complex references,
with J the defined conditional-Umegaki difference used in C's PROOF.md.
Use the accepted free-Umegaki representation at that declared boundary.
The actual reference is L'=L+E, stochastic, with the DETERMINISTIC acquired
entry promise |E_yi|<=delta L_yi, 0<=delta<1. This note supplies no statistical
calibration procedure or evidence that a physical channel meets that promise.

Set ell_y=min_i L_yi, u_y=max_i L_yi, and the rational scalar

    S=sum_yz [sum_i L_yi |(L^-1)_iz|]^2 u_z/ell_y.

If a=delta sqrt(S)<1, then the SAME release satisfies

    J_K <= c (1+delta)/(1-a)^2 J_L'.                  (1)

This holds with no quantum-reference dimension factor, no reference-state
sampling and no finite-side-information truncation. It is a conservative
robustification of an existing budget, not a stronger privacy definition,
guessing guarantee, uncertainty-free mechanism or new quantum capability.

## Proof at the free interface

Take any positive effects Q_i summing to I and vectors u_i summing to zero.
Write v_y=sum_i L_yi u_i and W_y=sum_i L_yi Q_i. The free quadratic form is

    F_L=sum_y ||W_y^-1/2 v_y||^2.

Positive channel entries imply ell_y I<=W_y<=u_y I, including boundary
effects. Let B=E L^-1. Then Eu=Bv exactly. On the weighted direct sum its
scaled block B_yz becomes W_y^-1/2 B_yz W_z^1/2, whose operator norm is at
most |B_yz| sqrt(u_z/ell_y). The entry premise gives

    |B_yz|<=delta sum_i L_yi |(L^-1)_iz|.

The operator norm of a block matrix is at most the norm of the scalar
matrix of its block norm bounds, which is at most its Frobenius norm.
Consequently ||Eu||_(W^-1)<=a ||Lu||_(W^-1). This is valid for arbitrary
complex reference vectors and noncommuting effects: only scalar upper and
lower operator bounds were used.

Also (1-delta)W_y<=W'_y<= (1+delta)W_y. Inverting the upper inequality
and using the reverse triangle inequality therefore gives

    F_L' >= (1-a)^2/(1+delta) F_L.                  (2)

Combining F_K<=c F_L with (2) and the inherited free/conditional-Umegaki
equivalence proves (1). No subtraction of separate entropy continuity
errors or division by a state-dependent small J_L is used. The same proof
also gives F_L'<=(1+a)^2/(1-delta) F_L. These estimates depend explicitly
on the nominal channel's conditioning; a nearly singular L is not made
stable for free.

## A finite rational receiver and its use

Compute S exactly from rational L, and choose an integer B0>=max(1,sqrt S)
by integer square-root comparison. With delta=1/(32 B0), one has a<=1/32.
For an existing nominal c=1/2 certificate, an exact robust upper budget is

    c_robust=(1/2)(1+delta)/(1-1/32)^2 <=528/961<3/5.

Thus a finite relative-entry calibration radius can be returned along with
the synthesized release, without solving another channel-design problem.
For a desired budget c_target one may instead run the original design at
c_safe<=c_target(1-a)^2/(1+delta); all ordinary/source-aware competitors
receive this same receiver and calibration margin.

compile_margin.py consumes only the saved rational L and nominal budget
and binds their source bytes. It calculates this margin; it does NOT
recheck the nominal K primal/dual certificate, sample a release/reference,
solve an SDP, simulate a channel or certify an actual calibration. Its
nominal-K conclusion is conditional on that separate accepted synthesis.
No speed or utility advantage follows from this added robustness argument.
