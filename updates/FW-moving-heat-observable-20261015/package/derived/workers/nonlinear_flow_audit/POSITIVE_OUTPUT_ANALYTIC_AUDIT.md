# Positive sharp branch: independent all-output certificate audit

15 October 2026. Separate append-only continuation. Same-team analytic
review; external correctness, formal verification, priority and positive-
branch quasiconvexity remain unresolved.

Final root proof reviewed and snapshotted as `POSITIVE_OUTPUT_ROOT_REVIEWED.md`:
SHA-256 `2a921ee1a7666a3d8b7afca78126c73140b1a284655d3a2ae34c0b3e5485aa96`.
Portable all-positive input report:
SHA-256 `458687d7e96a8dfe6bd9f31bc4c14829fec5d2e62ee6a487d3bd11e6808b78db`.
Portable input equality-dual JSON:
SHA-256 `0bcf59a92b2a82c07a95c99b17966524ef62daa125cdc5c91072ad8927080669`.
Independent exact input-audit receipt:
SHA-256 `2fe479938f202bfcc0f600fe6889355e267550739ef8f8a32adce4402975ff13`.
Preserved root correction record:
SHA-256 `7d54208a2ba1253a3b2f750d70dab9fb8ac29fc57618bc7a5822c5572d9217d4`.

**Verdict:** the final root proof is correct in its specified pointwise
corrected-dissipation class. The all-output averaging, non-SOS flat-contact
argument forcing the mixed output-skew coefficient to vanish, smooth/Peano
transfer, and finite-positive-generation argument are valid. No required
correction remains at the reviewed final hash. The initial claim that the
skew term vanished along the flat curve was false; its corrected order-t^4
formula is independently verified here and is sufficient. The erroneous
draft and failure are preserved by the root rather than silently overwritten.

## 1. Averaging is exhaustive and preserves strong parabolicity

Fix r>0 and J_r. Start with any constant real output matrices C^(ij),
spatially symmetric, with

    sym(sum n_i n_j C^(ij)) >= kappa |n|^2 I, kappa>0.

Use the constant-generator energy representative
E_C=sum D2J_r(A)[B_i,C^(ij)B_j], with a homogeneous-quadratic closed
two-form correction and pointwise nonnegativity for every A,z. Smooth local
corrections are reduced to this class below.

Under target rotation R, the output matrices transform by R^T C^(ij) R.
Averaging the certificate preserves J_r, pointwise positivity, polynomial
degree, closedness and the same strong-parabolic lower bound. Each averaged
matrix is a_ij I+b_ij J, where J=[[0,-1],[1,0]]. The symmetric symbol is
then (sum a_ij n_i n_j)I, so the spatial scalar matrix a is positive definite.

For the paired target/input reflection S=diag(1,-1), J_r(SAS)=J_r(A),
and SJS=-J. The operator action is

    C^(ij) -> s_i s_j S C^(ij) S.

Thus the scalar spatial matrix changes as a->SaS and the skew spatial
matrix as b->-SbS. The average kills a12,b11,b22 and leaves

    C11=d1 I, C22=d2 I, C12=C21=b J, d1,d2>0.

The form transforms by minus pullback under A->SAS, the minus sign coming
from the input reflection's orientation. Exterior differentiation commutes
with this pullback. The reflection normalizes the target rotation group,
so left-invariance of the already averaged density is preserved. No right
involution or nonorthogonal input change is required for this all-output
reduction. The remaining mixed skew symbol does not contribute to its
symmetric part and is not bounded or removed by ellipticity alone.

## 2. The flat contact forces b=0 without an SOS hypothesis

At x0=(I,z0), z0=(0,0,1,0,0,0), B1=0 and B2=e12. The corrected density
P vanishes. Along

    A(t)=[[1,-(r+1)t],[(r+1)t,1]],
    z(t)=(t^2,t,1,0,0,0),

write R_t=e1 tensor(t,1). Then B1=t R_t and B2=R_t, so every alternating
form vanishes. The output cross term is not zero: directly,

    D2J_r(A(t))[R_t,J R_t]
      =-(2/3)r(r+1)(r+2)t^3.

The full heat value is therefore

    P(A(t),z(t))
      =(2/3)r(r+1)(r+2)t^4[(r+1)(d1 t^2+d2)-2b].

This is O(t^4) for every b. Since P is globally nonnegative and smooth,
its gradient at x0 is zero and its joint ten-variable Hessian H0 is PSD.
The curve tangent

    w=(0,-r-1,r+1,0; 0,1,0,0,0,0)

satisfies w^T H0 w=0, hence H0 w=0. This conclusion uses only pointwise
nonnegativity, not a PSD Gram on the 24 bilinear features.

The four A-components of the uncorrected Hessian-times-tangent are

    (H0 w)_A=(0,0,-4b,0).

Any C2 alternating form contributes zero to these components, even if it
is not closed: along the proportional-jet curve its pullback is identically
zero for every A, so its A gradient and the curve derivative of that gradient
are identically zero. Equivalently, at the base B1=0 and B1'=B2=e12.
Thus b=0 follows from H0 w=0. The independent
`check_output_mixing_bridge.py` verifies the rotation/reflection identities,
the complete curve formula, the four background components, and the zero
contribution of six arbitrary smooth alternating coefficient functions.

## 3. Composition with the all-r positive input separation

After b=0, the surviving operator is positive scalar input diffusion
diag(d1,d2). The independently audited 411-by-62 input equality dual uses
all sixty closed quadratic-form coefficients, necessary symmetries and
contact equations. It forces the compatible bad-jet value

    P(e21,(0,1,0,0,0,0))
       =-r(r+1)(2r+1)d2/(r+2)<0,

for every r>0. There is no exceptional positive r=1 and no SOS premise.
The 48 rational equality multipliers have no positive-branch poles.

The input proof's additional new-zero argument is valid: at (I,e_z2),
the flat tangent ((r+1)J,e_z1) and invariant target-rotation zero tangent
(J,e_z5) both lie in the joint Hessian kernel. Their difference is
(0,e_z1-(r+1)e_z5). Since the zz Hessian is twice the jet quadratic matrix
and independent of base z, this forces the density to vanish at that new
jet. Global nonnegativity then forces its A gradient to vanish, giving
the additional necessary linear equalities. This argument again needs no
ambient bilinear SOS representation.

The input symmetry involution is a valid separate averaging step: for
M=[[0,h],[1,0]]/sqrt(h), h=(2r+1)/3>0, J_r(AM)=J_r(A), and D transforms
by M D M^T. Reflection and M generate a finite group up to input sign.
Thus the input proof may enforce d1=h d2 without losing positive diffusion.
This involution is needed only inside the portable input obstruction, not
to remove the general output coefficient b.

## 4. Taylor and quasilinear transfer

For a fixed constant generator and a C2 closed form near A=0, positivity
first forces its constant pullback to vanish: it is PSD in z and zero on
the spanning pure Hessian jets. Injectivity of the six planar wedge minors
then kills the constant form. Positivity at both tA and -tA kills the linear
coefficient. Dividing by t^2 gives a globally nonnegative homogeneous
quadratic Taylor correction; differentiating closedness at the origin
shows that Taylor form is closed. The polynomial no-go therefore also
excludes this smooth local form class. Only local positivity near A=0 is
needed before the homogeneous reduction.

More generally the root Peano tangent theorem applies to
u_t=sum C^(ij)(Du)u_ij with C continuous at zero and strongly parabolic
C(0), and any local null correction quadratic in the Hessian whose
coefficients admit a second-order Peano jet. It yields a global constant-
C(0), A^2 z^2 null-corrected canonical density. The previously verified
explicit identity P_C-E_C=d eta_C(B1,B2), plus the planar polynomial null
classification, converts it to a closed quadratic corrected E_C density.
The all-output no-go just proved contradicts that certificate.

No invalid variable-C substitution is used. No existence or relaxation
claim for the quasilinear equation is required. Degenerate C(0), singular
angular coefficients, absent coefficient jets, nonlocal operations, higher
jets and integrated methods without a pointwise correction remain outside.

## 5. Finite positive generation with arbitrary PC addends

The final root revision correctly collects all PC addends into one P.
Suppose J_r is a finite positive sum of left-invariant homogeneous quartic
polynomials admitting the excluded heat certificates and arbitrary
polyconvex addends. Absorb positive weights into their functions.

Every heat energy is ROC. On a pure Hessian jet its acoustic matrix S and
output symbol C satisfy C^T S+SC>=0. Strong parabolicity gives exponential
decay of e^(-Ct), and

    S=integral_0^infinity e^(-C^T t)(C^T S+SC)e^(-Ct) dt>=0.

The same implication applies to a smooth adaptive certificate after its
constant tangent reduction. Hence all heat energies belong to the invariant
ROC cone. The collected P is polyconvex by positive-sum closure and equals
J_r minus a sum of invariant quartic polynomials. It is therefore itself
an invariant homogeneous quartic polynomial, even if its individual PC
summands were neither polynomial nor invariant. Polyconvexity implies ROC.

Invariant extremality now forces every nonzero heat summand and P to be a
positive multiple of J_r. A heat multiple would give a certificate for J_r
after division by that scalar, contradicting the new no-go. A PC multiple
would make J_r PC, contradicting the independently proved support-gap
obstruction for all r>0. Thus no such finite decomposition exists.

This argument does not require a claim about each PC summand's rotation
average, and it does not assert closure separation with unbounded operator
coefficients or allow noninvariant heat energies whose simultaneous energy/
operator averaging need not factor into a single certificate.

## 6. Final scope

The final root hash is analytically cleared. This is an all-constant-output
and specified smooth-adaptive *local certificate* obstruction on every
positive sharp parameter. It is not a quasiconvexity counterexample, a
failure of all heat monotonicity arguments, or an impossibility for all
nonlinear flows. Positive-branch QC remains UNKNOWN.
