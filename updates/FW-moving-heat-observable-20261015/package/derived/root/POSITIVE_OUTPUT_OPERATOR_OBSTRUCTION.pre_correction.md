# The positive sharp branch excludes output mixing as well

15 October 2026. Root synthesis of the independently found flat-contact
identity and the full positive-input-diffusion separation. Status: internal
proof under separate same-team analytic/exact review; QC and priority UNKNOWN.

Let J_r=3rH/[8(r+2)]+r(r−1)u²/6+j²+ruj, r>0. The portable positive-input
proof excludes pointwise nonnegative corrected heat for every fixed positive
input diffusion and every homogeneous-quadratic closed two-form, without
an SOS restriction. The following argument excludes all constant real
strongly parabolic output-matrix generators as well.

## Exhaustive operator reduction

Write L v=sum C^{ij}partial_ij v, C^{ij}=C^{ji} real2×2, and assume
sym(sum n_i n_j C^{ij})>=kappa|n|²I, kappa>0. A certificate has density

    E_C(A,z)+omega_A(B1,B2),
    E_C=sum D²J_r(A)[Bi,C^{ij}Bj], d omega=0.

J_r is invariant under left SO(2) and under A→SAS, S=diag(1,−1).
Average a hypothetical certificate under these symmetries. Energy is fixed,
coefficients and forms are transported together, positivity and closedness
are preserved, and strong parabolicity is preserved by orthogonal congruence.
SO(2) averaging gives C^{ij}=a_ij I+b_ij J, J=[[0,−1],[1,0]]. The paired
reflection sends spatial A=(a_ij) to SAS and B=(b_ij) to−SBS. It removes
a12,b11,b22. Thus it is sufficient to exclude

    C11=d1I, C22=d2I, C12=C21=bJ, d1,d2>0.

No right-coordinate involution, conformal reduction of A, or symmetry of the
original output matrices is needed for this reduction. The averaged symmetric
principal symbol is(d1n1²+d2n2²)I, so both diagonal coefficients are positive.

## The flat contact forces b=0

Put y0=(A,z)=(I,(0,0,1,0,0,0)) in row-major A and compatible jet ordering
z=(phi1_xx,phi1_xy,phi1_yy,phi2_xx,phi2_xy,phi2_yy). Then B1=0,B2=e12.
The acoustic contact implies P(y0)=0 for the corrected density P.

Use the joint curve

    A(t)=[[1,−(r+1)t],[(r+1)t,1]], z(t)=(t²,t,1,0,0,0).

Here B1=tR_t,B2=R_t, R_t=e1 tensor(t,1), so every two-form vanishes.
The skew-output contribution vanishes because the rank-one target acoustic
matrix is diagonal on this curve; equivalently it is checked directly.
The scalar diffusion part is(d1t²+d2) times the exact acoustic value
(2/3)r(r+1)²(r+2)t⁴. Hence P(y(t))=O(t⁴).

If P>=0 for every A,z, its gradient at y0 is zero and its full joint Hessian
is PSD. Its tangent

    w=(0,−r−1,r+1,0; 0,1,0,0,0,0)

has zero Hessian quadratic value and must be in the Hessian kernel. The
A-components of Hess(P)(y0)w are exactly(0,0,−4b,0), as the standalone
symbolic check reconstructs. The form contributes zero to these components,
even without closedness: B1base=0 and B1prime=B2base=e12, so differentiating
its alternating pullback with respect to A still gives zero. Consequently b=0.

The averaged certificate is now an ordinary positive input-diffusion
certificate, contradicting the full r>0 input separation. Thus no operator
in the original arbitrary strongly parabolic output-matrix class works.

The root Peano tangent theorem then excludes continuous-at-zero adaptive
quasilinear operators with strongly parabolic tangent and local quadratic-
Hessian null corrections admitting a second coefficient jet. This remains
a local certificate obstruction. It gives no negative compatible-gradient
Jensen example, no failure of QC, no all-flow impossibility, and no exclusion
of singular/angular, degenerate, nonlocal or higher-jet mechanisms.

## Finite positive generation boundary

The J_r are extreme in the invariant ROC cone and are non-polyconvex.
Therefore no finite positive decomposition into left-invariant quartics
admitting the excluded heat certificates and homogeneous quartic polyconvex
addends can yield a positive-branch J_r. Average the PC addends under left
rotations if necessary; each nonzero averaged summand would be proportional
to J_r, impossible for a PC function. A homogeneous PC quartic is nonnegative
by its support at zero and amplitude scaling, so a PC addend with zero
rotation average was already zero. This is not a statement about coefficient
closures with unbounded operators or noninvariant heat energies averaged
jointly with different generators.
