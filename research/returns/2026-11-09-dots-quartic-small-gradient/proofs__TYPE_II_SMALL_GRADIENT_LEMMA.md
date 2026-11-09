# Type-II small-gradient Jensen lemma

Date: 9 November 2026.
Status: analytic candidate, not independently cleared. No numerical run, global quasiconvexity claim, or novelty claim. This is a separate extension; the frozen original-J_r note (SHA256 56bda4a48ac763013df9f5110e2ada9dd6d680a94edf5b6bebf8738b32566830) is unchanged.

## 1. Exact terminology and contract

A small-gradient Jensen inequality at each fixed affine mean is called weak quasiconvexity by Morrey and by Kristensen, On the non-locality of quasiconvexity, Ann. IHP C 16 (1999), pp. 3–4. Kristensen uses local quasiconvexity for the stronger property of agreeing with a globally quasiconvex function near that mean. This note proves only the explicitly stated small-gradient inequality, not a quasiconvex extension.

Let F be a homogeneous quartic polynomial on real 2 by 2 matrices with

    F(X) >= c_* |X|^4,   c_*>0.

Fix an affine mean A and a determinant multiplier mu such that the exact Taylor expansion is

    F(A+X)-F(A)-DF(A):X-mu det X = Q(X)+C(X)+F(X),

where Q is a nonnegative quadratic form and C is homogeneous cubic. Suppose that in fixed compatible coordinates X=[[a,b],[c,d]], there are lambda!=0, nu_*>0 and kappa with

    r=d-lambda a,
    Q(X)>=nu_*[c^2+r^2],
    C(a,b,0,lambda a)=kappa a^3,
    partial_b^2 C=0 on all matrix space.                    (1)

The coordinate maps are fixed invertible left/right matrix maps preserving gradients after a domain change. All constants below may depend on these maps. The theorem does not assume that any pointwise component projection is itself a gradient.

CLAIM. There are finite constants C1,C2, depending on the displayed polynomial and coordinate data, such that for every periodic Lipschitz vector field phi,

    |int C(Dphi)|
      <= C1 epsilon^(1/2) M^(1/4) Qbar^(3/4)
          +C2 epsilon Qbar,                                (2)

where epsilon=||Dphi||_infinity, M=int |Dphi|^4 and Qbar=int Q(Dphi). Constants are independent of the square side length and Fourier bandwidth. Consequently, for a positive radius epsilon_* depending only on these fixed data,

    int [F(A+Dphi)-F(A)] >= Qbar/2+c_*M/2
    whenever ||Dphi||_infinity<=epsilon_*.                 (3)

There is no restriction r=0 or c=0 on the admissible gradients, and no moving-mean uniformity is claimed.

## 2. Finite-p Hodge construction

Work initially with a smooth periodic vector field. Write X=Dphi. For p in {2,3,6}, let H_p be a finite norm for the following order-zero periodic multiplier:

    phi1^0=phi1+(1/lambda) partial_1 Delta^(-1) r,
    phi2^0=phi2-partial_2 Delta^(-1) r,
    E=Dphi^0-Dphi,
    ||E||_p <= H_p ||r||_p.                                (4)

The mean of r is zero. These are finite-p Calderon-Zygmund bounds; no L-infinity bound for E is used. The corrected gradient satisfies d0=lambda a0. After removing irrelevant constant vectors, there is a periodic scalar psi such that

    phi1^0=psi_2/lambda, phi2^0=psi_1,
    a0=psi_12/lambda, b0=psi_22/lambda, c0=psi_11.            (5)

Declare L_lambda=1+|lambda|. From (1),

    ||c||_2, ||r||_2 <= nu_*^(-1/2) Qbar^(1/2),
    ||r||_infinity <= L_lambda epsilon,
    ||r||_3 <= L_lambda^(1/3) nu_*^(-1/3)
                  epsilon^(1/3) Qbar^(1/3),
    ||r||_6 <= L_lambda^(2/3) nu_*^(-1/6)
                  epsilon^(2/3) Qbar^(1/6),
    ||X||_6 <= epsilon^(1/3) M^(1/6).                       (6)

Therefore, with declared finite constants K0,K1,K2,

    ||psi_11||_2 <= K0 Qbar^(1/2),
    ||psi_22||_6 <= K1 epsilon^(1/3)M^(1/6)
                    +K2 epsilon^(2/3)Qbar^(1/6).           (7)

For example, K0=(1+H_2)nu_*^(-1/2), K1=|lambda|, and
K2=|lambda|H_6 L_lambda^(2/3)nu_*^(-1/6) are valid.

## 3. Mixed derivative and the tangent coordinate

The finite-exponent mixed derivative inequality is

    ||psi_12||_3 <= I ||psi_11||_2^(1/2)||psi_22||_6^(1/2).  (8)

Its proof is identical to the displayed complex-interpolation proof in the frozen original-J_r note: remove coordinate-zero modes, interpolate |D1|^(2z)|D2|^(2(1-z)) between L2 and L6 with Gaussian damping of the polynomial imaginary-power bounds, then apply the two coordinate Hilbert transforms. The exponent identity is 1/3=(1/2)(1/2)+(1/2)(1/6). This is standard finite-p harmonic analysis, not an L-infinity endpoint estimate. Isotropic scaling makes I independent of square size.

Combining (4)–(8), and using a=a0-E_a, gives finite A1,A2 with

    ||a||_3 <= A1 epsilon^(1/6)M^(1/12)Qbar^(1/4)
                 +A2 epsilon^(1/3)Qbar^(1/3).               (9)

One explicit choice is

    A1=I sqrt(K0 K1)/|lambda|,
    A2=I sqrt(K0 K2)/|lambda|
          +H_3 L_lambda^(1/3)nu_*^(-1/3).

Hence, with A=epsilon^(1/2)M^(1/4)Qbar^(3/4) and
B=epsilon Qbar,

    int |a|^3 <= 4 A1^3 A+4 A2^3 B.                        (10)

The notation A in (10) denotes an auxiliary scalar only; the fixed affine mean in Section 1 is unchanged.

## 4. All remaining cubic monomials

Put N=|c|+|r|. In the independent coordinates (a,b,c,r), the polynomial C-kappa a^3 vanishes at c=r=0, so it belongs to the ideal generated by c and r. The identity partial_b^2 C=0 implies that it contains no monomial with two or more factors b. Every remaining cubic monomial therefore either has at least two normal factors or has one normal factor, one a, and one other factor. Since (a,b,c,r) is a fixed linear coordinate system, there is an explicitly computable finite coefficient sum L_C with

    |C(X)-kappa a^3|
       <= L_C [N^2 |X|+N |a| |X|].                        (11)

Here L_C may be defined as the absolute sum of the finitely many coefficients in those coordinates, multiplied by the elementary coordinate norm-equivalence factor. No positivity optimizer or oracle is involved.

The first term has

    int N^2 |X| <= (2/nu_*) epsilon Qbar.                  (12)

For the second, use exactly the Holder exponents 2,3,6:

    int N |a| |X|
       <= ||N||_2 ||a||_3 ||X||_6
       <= sqrt(2/nu_*) [
             A1 A + A2 epsilon^(2/3)M^(1/6)Qbar^(5/6)].     (13)

The extra monomial in (13) is A^(2/3) B^(1/3), including when any quantity vanishes, so weighted Young gives

    epsilon^(2/3)M^(1/6)Qbar^(5/6) <= (2/3)A+(1/3)B.        (14)

Equations (10)–(14) prove (2), with the fully declared finite constants

    C1=4|kappa| A1^3
          +L_C sqrt(2/nu_*)[A1+(2/3)A2],
    C2=4|kappa| A2^3
          +L_C[2/nu_*+(1/3)sqrt(2/nu_*) A2].

They can be enlarged to positive constants if either is zero. No numerical value of the multiplier constants or radius is claimed.

## 5. Absorption, domains, and fixed-coordinate changes

For a periodic gradient, both the linear Taylor term and det Dphi integrate to zero. By strict quartic positivity,

    Jensen gap >= Qbar+c_* M-C1 sqrt(epsilon)M^(1/4)Qbar^(3/4)
                               -C2 epsilon Qbar.

The choice

    epsilon_* = min{1,(2c_*/C1)^2,1/(9C1^2),1/(4C2)}

is sufficient, by M^(1/4)Qbar^(3/4)<=(M+3Qbar)/4, to yield (3).

Periodic mollification extends the result to Lipschitz fields. Zero extension into a square gives the same result for compactly supported or admissible zero-boundary Lipschitz tests. A fixed compatible left/right transformation changes the domain and norm constants by fixed finite factors; zero extension handles its transformed domain without pretending that a nonintegral transformation preserves a chosen periodic lattice.

## 6. Type I and the conditional class consequence

For a Type-I contact, assume Q(X)>=nu_*|Y|^2, where Y is the component transverse to the rank-one kernel, and C has at most one power of the kernel coordinate. Then directly

    |C(X)|<=K |X| |Y|^2,
    |int C(Dphi)|<= (K/nu_*)epsilon Qbar.

This gives the small-gradient Jensen inequality with no mixed interpolation.

N806 CONTACT_COMPENSATION.md classifies acoustic contacts of non-polyconvex rank-one-convex homogeneous planar quartics invariant under left SO(2) into exactly Type I or Type II with the cubic identities used above. CONDITIONAL ON THAT COMPLETE CLASSIFICATION, every STRICTLY COERCIVE member of this cone has the small-gradient Jensen property at each affine mean: Type I or II handles acoustic contacts, strict Legendre-Hadamard handles noncontacts, and quartic positivity handles the zero mean. Polyconvex members already satisfy the unrestricted Jensen inequality.

This note does not re-audit that complete algebraic classification. Strict coercivity F(X)>=c_*|X|^4 is an explicit hypothesis; it is NOT inferred for all members of the cone. The independent original-J_r proof supplies this hypothesis for every r>0 and does not need the whole-cone classification for its particular mean classification.

## 7. Comparison and actual remaining operation

The primary ordinary strict-Legendre-Hadamard small-gradient argument is classical; Kristensen 1999 states it and proves a stronger local-extension result in that strict setting. It does not itself handle the Type-II rank-two calibrated quadratic form here.

Astra N806 already supplied the algebraic Type-II normal form and the differential Hodge/mixed L4–L2 cubic compensation. The present analytic increment is the finite L6–L2 interpolation combined with a small ORIGINAL gradient supremum, plus the L2–L3–L6 treatment of the normal cubic ideal. It supplies an epsilon gain despite the absence of an ordinary gradient-norm coercivity gap. It is not a new general harmonic-analysis method.

Neither small-gradient stability at every mean nor the conditional cone statement establishes arbitrary-amplitude quasiconvexity. At a fixed mean of a homogeneous quartic, the unrestricted question can be phrased as the sharp integrated discriminant

    (int C(Dphi))^2 <=4 (int Q(Dphi))(int F(Dphi))

for every compatible test. The displayed proof does not establish that sharp inequality.

Sources:
- Original-J_r small-gradient candidate: LOCAL_QC_DEGENERATE_CONTACT.md, SHA256 56bda4a48ac763013df9f5110e2ada9dd6d680a94edf5b6bebf8738b32566830.
- N806: updates/FJ/package/quartic/CONTACT_COMPENSATION.md at Astra pin bb16dbf0e9c9b9ecaacfd10f577aedef51bd2e0e, SHA256 f47796d9088b9a4b75c43d31f93b05d36dbe025c4db9d6a8ec02dbd6d0a8ca28. Sections 2.3, 3 and 4 were directly reread for this implication.
- Jan Kristensen, On the non-locality of quasiconvexity, Ann. IHP C 16 (1999), 1–13, https://www.numdam.org/item/AIHPC_1999__16_1_1_0.pdf. Definitions on pp. 3–4 and Proposition 1 on p. 6 directly read.
- Bruno–Pasqualotto, Quasiconvexity for the Dacorogna–Marcellini Energy, arXiv:2608.06367v1. Its global bi-SO(2) result remains a stronger global theorem in a different symmetry class; it is not imported here.

Independent review of this generic implication is pending. No scientific computation was performed.
