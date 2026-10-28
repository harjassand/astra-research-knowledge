# A necessary scale tradeoff for smooth representatives of F+epsilon norm-square

This is a universal necessity statement, complementary to an explicit tube
radius for one construction. It does not duplicate that radius or claim an
optimal constructive scale. F is the accepted quartic with no local C2
convex representative.

Let epsilon_j decrease to zero. Let g_j be globally finite convex
representatives of W_j(A)=F(A)+epsilon_j|A|^2. Suppose g_j is C3 on an
Euclidean ball B_R5(0,r_j), and put

    L_j=sup_(|z|<=r_j) |D(partial_ss g_j)(z)|,

allowing L_j=+infinity. The following two asymptotic properties cannot
both hold:

    r_j/sqrt(epsilon_j) -> infinity,
    L_j sqrt(epsilon_j) -> 0.                         (1)

In particular, if all g_j are C3 on one fixed ball, then the vertical
curvature's Lipschitz constant has an asymptotic Omega(epsilon_j^(-1/2))
lower bound. Indeed a subsequence violating that lower bound would
satisfy (1). No explicit best constant is asserted.

## Proof

The graph energy fixes g_j(0)=0 and its derivative in the first four
coordinates to zero. Write k_j=partial_s g_j(0). Its supporting tangent
on the scaled graph yields

    epsilon_j |A|^2>=k_j detA.

The sharp planar determinant bound gives |k_j|<=2epsilon_j. Subtract the
affine function k_j s from g_j; the result is still convex, is nonnegative,
and has zero value and gradient at zero. This subtraction does not change
partial_ss or its derivative.

Under (1), choose a scale rho_j with

    sqrt(epsilon_j)<<rho_j<<min(r_j,1/max(1,L_j),1).

Such scales exist because each entry of the right-hand minimum divided
by sqrt(epsilon_j) tends to infinity. For example, take the geometric mean
of that minimum and sqrt(epsilon_j).

Form weighted blowups

    H_j(B,s)=rho_j^(-4)[g_j(rho_j B,rho_j^2 s)-k_j rho_j^2 s].

Their graph values converge on compact sets to F(B), since both
epsilon_j/rho_j^2 and k_j/rho_j^2 tend to zero. Nonnegativity and the
two-graph averaging bound give uniform compact upper/lower bounds, so a
subsequence converges locally uniformly to a finite convex H.

The vertical second derivatives satisfy

    partial_ss H_j(B,s)=partial_ss g_j(rho_j B,rho_j^2s).

Their difference from c_j=partial_ss g_j(0) tends uniformly to zero on
compact sets by L_j rho_j->0. The c_j are nonnegative and bounded: the
second vertical difference at (0,+1),(0,0),(0,-1) is c_j+o(1), while those
values are uniformly bounded by the compact graph averages. Passing to a
further subsequence gives c_j->c>=0 and hence H_ss=c.

The same elementary equal-s convexity argument used in the accepted
classification makes H(B,s)=a(B)+s b(B)+(c/2)s^2 with b affine. Its
nonnegativity and quartic graph F kill the affine b. Thus

    F(B)=a(B)+(c/2)det(B)^2,          a convex,

contradicting the accepted no-C2 classification. This proves the tradeoff.

## Meaning and limits

The represented energies W_j converge to F in C-infinity on compact sets.
Their lifted geometry cannot retain both a broad smooth neighborhood and
a slowly varying determinant curvature. One of those scales must degrade.
This quantifies a representation-resolution loss that smooth convergence
of the stored energy itself does not reveal.

The explicit h in PROOF.md has constant partial_ss h=2M. Its graph
neighborhood of convexity is therefore allowed to shrink; the theorem
does not assert a common positive radius. This is consistent with the
construction rather than a contradiction to it.

The result concerns this raw five-minor interface and exact graph matching.
It does not assert a neural-network size bound, a physical stiffness law,
or QC for the non-PC target family.
