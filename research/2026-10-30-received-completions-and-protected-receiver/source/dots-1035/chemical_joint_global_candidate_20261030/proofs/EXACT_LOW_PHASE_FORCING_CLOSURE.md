# Exact low-phase forcing closes both extreme-composition sectors

Status: child adversarial audit passed; see INDEPENDENT_LOW_PHASE_FORCING_AUDIT.md. No whole-project independent review or global recurrence claim. This is an actual primal boundary-feedback construction for the coupled hard network, not a frozen average. It does not prove global recurrence.

## Network and base function
Use the rank-three network:
- 0→A+B→3A+4B→0, all connector constants1;
- the reversible chain 3C+4B ↔ A+2C+4B ↔2A+C+4B ↔3A+4B, forward constants6,1,7 and reverse constants12,1,1.

Fix 0<alpha<1 (the prior common alpha<1/2 is admissible). Set V0(A,C,B)=(A! C! B!)^alpha.

## Exact Poisson extension, not a closed-boundary assumption
For b>=4 put f_b(a)=(a! b!)^alpha. For b=3,2,1,0 recursively define

    f_b(a) = [(a! b!)^alpha + f_(b+1)(a+1)
                         + ab f_(b+3)(a+2)]/(1+ab).

Define F(A,C,B)=C!^alpha f_B(A) for B<4, and F=V0 for B>=4.

This is the exact stopped Poisson/Dirichlet construction until first reaching B>=4. At B<4 only immigration and activation are enabled; both increase B, so the stopping time uses at most4 jumps. A increases by at most8, C never changes, and each holding time has mean at most1. Thus the expression is finite and positive, with

    L F = −V0    at every B<4,
    F <= C_alpha ((A+8)! C!)^alpha    there.

No invariance, instantaneous equilibration, or unspecified boundary offset is assumed. F is normlike on the full state space.

## Sharp actual return asymptotics
Fixed-shift factorial ratios and the displayed recursion give, as a→infinity,

    f_b(a)=((a+2)! (b+3)!)^alpha [1+O(a^(alpha−1))], b=1,2,3;
    f_0(a)=((a+3)! 4!)^alpha [1+O(a^(−delta))],
    delta=min(1−alpha,3alpha)>0.

For example, activation dominates at b>=1; the immigration branch is only O(a^(alpha−1)) relative to it. At b=0 the exact formula is f_0(a)=a!^alpha+f_1(a+1), which produces the additional a^(−3alpha) term. These statements follow by descending substitution, not by stationary phase averaging.

Consider an actual clearing reaction from B=4, A>=3. It lands at (A−3,C,0), where the full return/holding correction is already included in F. The ratio is

    F(A−3,C,0)/V0(A,C,4)=1+O(A^(−delta)).

Thus the potentially dangerous leading clearing loss cancels with its actual neutral return; the positive remainder is only O(A^(3−delta))(B)_4 after dividing drift by V0. For B=5,6,7, the analogous return ratio is O(A^(−alpha)), so clearing is nonpositive for large A. For B>=8 both endpoints use V0 and clearing is automatically nonpositive. Incorporating finitely many small A values gives the uniform bound

    (positive clearing contribution)/F <= C (B)_4 [1+A^(3−delta)]

for all B>=4. This is the exact outgoing-feedback estimate missing from a mere local certificate.

## Fast conversion dominates at either composition endpoint
At B>=4, F=V0 and fast conversion keeps B fixed. Its two ratios are

    V0(A+1,C−1,B)/V0 = ((A+1)/C)^alpha,
    V0(A−1,C+1,B)/V0 = ((C+1)/A)^alpha,

when the corresponding reaction is enabled. The aggregate rates, divided by (B)_4, are

    birth = 6(C)_3 + A(C)_2 + 7(A)_2 C,
    death = 12A(C)_2 + (A)_2 C + (A)_3.

For C/A sufficiently large, the negative birth term is of order C^3; the positive reverse term is at most a constant times

    C^(2+alpha) A^(1−alpha)
      + C^(1+alpha) A^(2−alpha) + C^alpha A^(3−alpha),

which is smaller by a power of A/C. The symmetric estimate when A/C is sufficiently large gives a negative term of order A^3. Cases A=0 or C=0 are handled directly by the enabled one-way conversion rate. Hence there are constants M>1,c>0 and S0 such that, for S=A+C>=S0, B>=4, and either A<=C/M or C<=A/M,

    (fast contribution)/F <= −c S^3 (B)_4.

Immigration and activation contribute at most

    C (B)_4 [1+A^(1+2alpha)],

uniformly in B>=4: the B powers divide against (B)_4, and alpha<1. Both 1+2alpha and 3−delta are strictly below3. Combining the actual clearing-return estimate therefore gives, after increasing S0,

    L F/F <= −(c/2) S^3 (B)_4

throughout both extreme-composition sectors, uniformly over all B>=4.

## Earned scope and remaining global matching
We have one explicit, globally defined normlike F whose drift is strictly negative at EVERY B<4 and throughout BOTH extreme-composition sectors for large A+C. This includes the actual A-small/C-large endpoint implicated in the earlier adjoint numerical failures. It does not claim those old numerics have passed; they concern a different measure.

The remaining unearned region includes balanced composition A/C in [1/M,M] at intermediate B, and B→infinity with both A,C bounded. The prior bulk certificate, joint-shell Green transport, and finite-phase halo address pieces of these regimes but have NOT yet been glued into a global function. In particular F's clearing cancellation at B=4 removes the leading radial sink; the multistable fast-composition contribution can then be positive in the balanced cone. No recurrence conclusion is drawn from the present sector theorem.

## Decisive balanced-cone failure of this same F
This remaining issue is not merely lack of an estimate. At B=4 and A/C→r=5/2, the clearing leading term cancels by the exact return asymptotic, and immigration/activation plus the clearing remainder are o(C^3). The leading fast drift coefficient, divided by (B)_4 C^3, is

    H_alpha(r)=b(r)(r^alpha−1)+d(r)(r^(−alpha)−1),
    b(r)=6+r+7r^2, d(r)=12r+r^2+r^3.

At r=5/2, b=209/4 and d=415/8, so b−d=3/8>0. Since r^alpha>1,

    H_alpha(r)=(r^alpha−1)[b(r)−d(r)/r^alpha]>0

for EVERY alpha>0. Thus this exact Poisson-corrected factorial F has positive drift along that actual balanced ray for every admissible alpha. Reducing alpha or changing a threshold cannot make it a global certificate. A composition-adapted joint profile is genuinely necessary.

## Compatibility already earned with the bulk certificate
Choose alpha also admissible for the previously proved primal single-linkage bulk theorem. If B>=max(8,K_bulk) and A,C>=K_bulk, every reaction target has B>=4, so F=V0 at the state and every target. Therefore LF=LV0 exactly and the bulk inequality is inherited without gluing. This does not eliminate the explicitly listed uncovered cylinders.
