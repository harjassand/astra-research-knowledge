# A finite variance refinement for the common-bank interval score certificate

28 October 2026. Candidate refinement, separate review required. The all-length localization source and its sound guard remain unchanged. This only replaces the conservative coefficient confidence radii using an exact conditional second moment of the ACTUAL ordinary measurement record.

## 1. Exact noise-independent conditional variance budget

Use the same common bank, private current settings and scalar coefficient record X for an input axis and a nonidentity output Pauli word of weight k:

 X=3^(k+1) 1_input_axis 1_matching_output_axes s product outcomes.

Let L_k=3^(k+1). Since squared binary outcomes and s are one, private independent input/output setting choices give EXACTLY

 E[X^2|past]=L_k.

The conditional mean c_t=Tr(P C_(t,j)) lies in[-1,1], because C_(t,j) is half the difference of two output states of a CPTP channel. Thus D_t=X_t-c_t has conditional mean zero,

 E[D_t^2|past]<=L_k, |D_t|<=b_k=L_k+1.                     (1)

Neither environment reset nor a stationary source is needed beyond the parent source's current-coin independence and valid conditional CPTP maps. This variance is not estimated from favorable observed outcomes.

## 2. Self-contained bounded-martingale Bernstein radius

For any centered D with |D|<=b and E[D^2|past]<=v, power-series expansion and r!>=2*3^(r-2) for r>=2 imply, for0<=lambda<3/b,

 E[exp(lambda D)|past]
 <=exp(lambda^2 v/[2(1-lambda b/3)]).

Multiplying conditional bounds over N records and choosing lambda=s/(Nv+bs/3) gives two-sided tail probability at most

 2 exp[-s^2/(2(Nv+bs/3))].

With t=log(2M/beta), s=sqrt(2Nv t)+(2/3)bt is sufficient. Union over the parent's M coefficient experiments therefore gives simultaneous radii

 eta_k=sqrt(2 L_k t/N)+2 b_k t/(3N).                       (2)

The means are the SAME predictable average global channel as before. Every data-dependent interval comparison remains covered by this one simultaneous event. Randomness cap failures and control/record-law discrepancies remain separately paid.

## 3. Weight-resolved local score interval

An interval of length ell has binom(ell,k)3^k Pauli words of weight k. Pauli orthogonality and the Frobenius bound for any feasible decoder image give the valid score halfwidth

 h_ell=(3/4) sqrt[sum_(k=1)^ell binom(ell,k)3^k eta_k^2].     (3)

Use this h_ell in the existing verified primal/dual score intervals and the SAME strict disjoint-competitor guard. No changes to oracle-normal-cone premises, interval enumeration, physical generator fitting or recovery transfer are implied.

Its leading N^-1 squared-width term is

 h_ell^2=(27/8)(10^ell-1)t/N+O(N^-3/2)

for fixed ell,t. A fully finite, simpler upper bound is

 h_ell^2 <= (27/4)(10^ell-1)t/N
  +[9(28^ell-1)+6(10^ell-1)+(4^ell-1)]t^2/(2N^2).          (4)

Equation(4) follows from(a+b)^2<=2a^2+2b^2 in(2); the actual tighter certificate uses(2)-(3). No large-N approximation is used by the acceptance guard.

## 4. Exact consequence on the declared two-output example

For n=2,w=1, M=18, beta=.05, target score halfwidth .05, the conservative parent Hoeffding calculation required959255 common-bank source calls. The exact finite variance radius(2)-(3) meets this target at82202 calls. This is about11.67-fold fewer calls for this PARTICULAR formal confidence requirement, not an observed recovery advantage or a generic optimal complexity claim.

These are source-call budget calculations, not executed confidence-acceptance experiments. The target channel, local solver feasibility/slack, physical readouts and other error budgets are unchanged. Strong equally informed conventional methods can use the identical variance calculation. The method is the familiar bounded-martingale Bernstein/Freedman principle, with the exact record variance and Pauli-weight sum supplied here; no historical novelty is asserted.
