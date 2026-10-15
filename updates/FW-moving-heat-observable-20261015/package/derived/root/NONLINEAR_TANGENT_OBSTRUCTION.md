# A tangent obstruction for smooth adaptive local flows

Root derivation, 15 October 2026. Initial main pin:
`33c1ff7ebd9411e9b8b4b0f951f62e36e631cb5d`.
Status: internally derived mathematical argument, submitted to a separate
same-team adversarial analytic audit. External correctness and priority UNKNOWN.

## The actual operation and its exact restriction

Let F be a homogeneous quartic polynomial on R^{m×n}. Write A=Du and
z=(u_{alpha,ij}), with z symmetric in its spatial indices. Consider

    u_t = G(A,z) = sum_{i,j} C^{ij}(A) z_{ij},

where C^{ij}=C^{ji} are real output matrices, continuous near A=0. This is
a quasilinear nondivergence-form equation; no existence, convergence, or
boundary-value result for its flow is assumed or claimed here.

Its canonical energy-dissipation density is

    P_C(A,z) = sum_{alpha,k,beta,l}
      F_{alpha k,beta l}(A) z_{beta,lk} G_alpha(A,z).

Indeed, for the relative energy integral [F(B+Dphi)-F(B)], integration by
parts once gives its first variation along the equation as -integral P_C
for a smooth compactly supported variation about an affine map. Variable
coefficients must occur inside G here. Substituting C(A) into the usual
constant-coefficient heat density does not give this identity.

Let N(A,z) be a homogeneous quadratic polynomial in z, with coefficients admitting a
second-order Peano expansion at A=0 (C² coefficients suffice). Assume N is
locally null: its integral on (B+Dphi,D²phi) is zero whenever these arguments
stay in its coefficient neighborhood, for every compactly supported smooth
phi and every admissible B. Suppose

    P_C(A,z) + N(A,z) >= 0

for every z and every A in a neighborhood of zero. The requirement is
pointwise positivity of a corrected local density. An integrated inequality
without such a local correction is outside this statement.

## Tangent theorem

Under these assumptions there is a homogeneous A-quadratic, z-quadratic
null density N2 such that

    P_{C(0)}(A,z) + N2(A,z) >= 0 for every A,z.

Thus this smooth local adaptation cannot certify a quartic whose tangent
constant operator is excluded from the entire polynomial null-correction
class. No ellipticity is needed for the tangent theorem itself.

### Proof

Write the coefficient expansion N=N0+N1+N2+o(|A|²), with Nj homogeneous
of A-degree j. At A=0, P_C=0, so N0 is a positive semidefinite quadratic
form on the compatible Hessian space. Scaling phi by epsilon in the null
identity at B=0 shows that integral N0(D²phi)=0. Fourier or localized
plane-wave testing gives N0(a⊗xi⊗xi)=0 for every a,xi. Such rank-one
Hessian jets span R^m⊗Sym²(R^n). A PSD quadratic form vanishing on a
spanning set is zero. Hence N0=0.

For each A,z, P_C(tA,z)=O(t²). Positivity at both tA and -tA, divided by
positive |t| and followed to zero, gives N1(A,z)=0. Consequently the
linear coefficient is identically zero as a quadratic form in z.

For t>0 divide positivity at tA by t². Homogeneity gives
P_C(tA,z)/t²=P_{C(tA)}(A,z), which tends to P_{C(0)}(A,z) by continuity
of C. The Peano remainder tends to zero for each fixed A,z. This proves
the desired inequality. Since tA is local for sufficiently small t,
the conclusion holds for all A.

Finally, fix B,phi. Apply the local null identity to tB,tphi. Quadratic
homogeneity in z and N0=N1=0 give

    0 = t^(-4) integral N(t(B+Dphi),tD²phi)
      -> integral N2(B+Dphi,D²phi).

The coefficient expansion is uniform on the compact range of B+Dphi;
the Hessian is compactly supported. Thus passage to the integral is
justified. N2 is a polynomial null density. QED.

## Conversion to the constant heat certificate

For constant output matrices C^{ij}, put Bi=partial_i Du and

    E_C(A,z) = sum_{i,j} D²F(A)[Bi,C^{ij} Bj].

For u=Bx+phi, the infinitesimal variation G=sum C^{ij}partial_ij phi
can be evaluated in two ways. One integration by parts gives -integral P_C.
Commuting the constant matrices with spatial differentiation and integrating
in i gives -integral E_C. Therefore P_C-E_C is an integral null density.
It is homogeneous A²z², and no output symmetry of C is required. It follows
that E_C+[N2+(P_C-E_C)] is pointwise nonnegative with a polynomial null
correction. In the planar two-output case the prior exact classification
identifies every such null correction with a closed quadratic two-form.
This conversion is necessary; the variable-coefficient E_C shortcut is invalid.

In the planar case there is also an explicit conversion, independently
derived by the adversarial auditor. Put q_k=(F_{alpha k})_alpha and

    eta_C = [(C12)^T q1-(C11)^T q2] dot dA_1
           +[(C22)^T q1-(C12)^T q2] dot dA_2.

Then P_C-E_C=d eta_C(A)[B1,B2] pointwise. Expanding the divergence of
the pulled-back one-form cancels every third derivative. Since eta_C is
cubic, d eta_C is a closed quadratic-coefficient two-form. For the other
summand N2 the prior planar polynomial null classification is still used.

## Consequence for Astra's exposed ray

In updates/FV-positive-consequences-20261015, the exact exposed ray is

    F=u²+v²+(166/3)uv-(460/9)w²-(52/9)j(u-v),

where u=|A e1|²,v=|A e2|²,w=Ae1·Ae2,j=det A.
Its source proof excludes E_C plus every homogeneous-quadratic closed
two-form for every constant C whose output principal symbol satisfies

    sym(sum n_i n_j C^{ij}) >= kappa |n|² I, kappa>0.

Combining that exact internally checked source theorem with the tangent
theorem excludes a local pointwise corrected-dissipation certificate for
this F for every adaptive C(A) continuous at zero with strongly parabolic
C(0), and every Peano-second-order null correction N as above.

This is a precise additional obstruction to a proposed escape from the
previous fixed-flow no-go. It does not decide quasiconvexity or polyconvexity
of F. It does not exclude singular/angular coefficients at zero, integrated
nonlocal estimates, higher-jet mechanisms, time dependence, or flows whose
tangent at zero is degenerate. Smooth lower-order terms are outside the
stated operation and have not been silently absorbed into this argument.

## Attribution and research value

The new synthesis is the quasilinear tangent consequence with the correct
canonical dissipation. It combines the incoming Taylor argument with the
previous exact all-constant-operator separation. The limiting argument is
elementary scaling, not a new general analytic principle. Historical priority
is UNKNOWN. Its value is to reject a whole smooth adaptive local escape
route and specify which operation would actually have to change.
