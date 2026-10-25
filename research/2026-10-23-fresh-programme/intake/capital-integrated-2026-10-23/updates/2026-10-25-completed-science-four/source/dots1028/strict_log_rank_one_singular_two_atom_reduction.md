# Exact two-atom reduction of the rank-one singular survivor

2026-10-25. This is a dimension-independent reduction of the actual singular boundary survivor to an explicit two-variable scalar inequality. The final scalar inequality is not proved in this note.

## 1. Actual target and normalization

Let A=|u><u| with ||u||=1, B>0, Tr B=1 and A<=9B. Simultaneous positive scaling reduces every rank-one A with Tr A=Tr B to this case. The finite singular survivor on supp A is the scalar

L_p(B,u)=2<u,log[pA+(1-p)B]u>-<u,log B u>.

A positive L_p would lift to a faithful strict-cap counterexample by the singular-boundary compression theorem. To exclude every 0<p<1/4 it suffices to prove L_(1/4)<=0. Indeed f(p)=-<u,log[pA+(1-p)B]u> is convex by operator convexity of -log, nonnegative because pA+(1-p)B<=I, and f(1)=0. Every convex function on [0,1] with its minimum at 1 is nonincreasing. Therefore L_p increases with p. This argument also holds on a cyclic subspace where Tr B<=1.

Write the spectral decomposition B=sum b_i |i><i|, and w_i=|<i,u>|^2. Every b_i lies in (0,1], sum_i b_i=1, sum_i w_i=1. The cap is exactly

sum_i w_i/b_i <=9.

This follows by conjugating A<=9B with B^(-1/2): the only nonzero eigenvalue of B^(-1/2) A B^(-1/2) is <u,B^(-1)u>.

## 2. A convex functional of the spectral weights

Put t=p/(1-p), and

g_w(s)=sum_i w_i/(b_i+s), s>=0.

Sherman-Morrison and the logarithm resolvent integral give exactly

L_p(B,u)=2log(1-p)+integral_0^infinity [g_w(s)-2g_w(s)/(1+t g_w(s))+1/(1+s)] ds.

For completeness, first write pA+(1-p)B=(1-p)(B+tA). The u expectation of (B+tA+sI)^(-1) is g_w(s)/(1+t g_w(s)); inserting this in the difference of logarithmic resolvent formulas gives the expression. The 1/s terms cancel, and the integrand is O(s^-2) at infinity. At zero it is finite because B>0.

For fixed s, the nonlinear function

f_t(g)=g-2g/(1+tg)

has f_t''(g)=4t/(1+tg)^3>0. Since g_w is affine in w, L_p is convex in w. One can first integrate over [0,M], use convexity, then take M to infinity; the finite-spectrum logarithmic integral converges for every weight in the compact simplex.

## 3. Exact finite-support extremality

For fixed positive eigenvalues b_i, the permitted weights form the polytope

W={w_i>=0: sum_i w_i=1, sum_i w_i/b_i<=9}.

A convex function on a compact polytope is bounded above by its maximum over vertices. Its vertices have precisely the following forms:

1. A single atom at b_i>=1/9.
2. Two atoms at b_-<1/9<b_+, with sum_i w_i/b_i=9.

Degenerate repeated values and b_i=1/9 collapse to case 1. The support bound follows because a vertex with three positive weights admits a nonzero perturbation preserving both affine constraints. If the inequality is inactive, two positive weights already admit a feasible two-sided perturbation.

Case 1 is safe: its survivor is

2log[p+(1-p)b]-log b,

which is nonpositive for b in [1/9,1] and p<=1/4.

Thus all possible positive rank-one singular survivors are dominated by a two-atom, cap-saturated survivor. No matrix bath dimension remains in this extremal problem.

## 4. The exact two-dimensional receiving interface

On the two-atom cyclic subspace, B has two positive eigenvalues b_-,b_+ whose sum S is at most the full trace 1. In a basis with u=e1, write d=det B. The harmonic equality <e1,B^(-1)e1>=9 says B_22=9d. Therefore, after removing the phase of B_12,

B=[[S-9d, sqrt(d(9S-1-81d))],
   [sqrt(d(9S-1-81d)),9d]],

with

1/9<S<=1, 0<d<=(9S-1)/81.

The endpoints where a cyclic weight vanishes are obtained by continuity and are already safe single-atom cases. At p=1/4,

C=(1/4)|e1><e1|+(3/4)B,
Tr C=(1+3S)/4,
det C=9d/4.

Equivalently, put h=S-9d-1/9>=0 and v=9d>0. Then

B=(1/9)|e1><e1|+ww*, w=(sqrt h,sqrt v),
h+v<=8/9,
C=(3/4)[(4/9)|e1><e1|+ww*].

The remaining scalar target is exactly

2 [log C]_11 - [log B]_11 <=0

on this displayed domain. Conversely, a positive value in the interior can be embedded in a normalized B by adding a spectator eigenvalue 1-S (when S<1); this spectator is orthogonal to u and has no effect on the survivor. Thus the domain is a genuine receiving boundary, not an artificially relaxed parameterization.

## 5. What is and is not achieved

This proof removes arbitrary auxiliary dimension from the rank-one singular boundary. It does not claim the final two-variable inequality, and it does not reduce a general higher-rank singular A to rank one. Plain Jensen at the spectral-weight level is too weak: the scalar average can be positive under the inverse-moment budget even when the exact convex functional is not. The exact rank-one resolvent coupling must remain present.

Related file: strict_log_singular_boundary_compression_equivalence.md. The independent, bounded rank-two singular probe is only a diagnostic and is not used in this theorem.
