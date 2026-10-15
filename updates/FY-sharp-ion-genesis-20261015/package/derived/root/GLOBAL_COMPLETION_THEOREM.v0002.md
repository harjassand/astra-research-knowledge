# Full invariant completion projection: contact coverage and exact dependencies

Root synthesis and proof, 15 October 2026, version 2. The generic-angle lemma
and full-space composition have now passed independent same-team reconstruction.
This is an internally established analytic theorem with the dependencies below;
external correctness, formal verification and historical originality remain
UNKNOWN. Version 1 is preserved as the conditional research checkpoint. All new
claims retain source_derived_unreviewed status. Git integration is not proof.

Let V be the real nine-dimensional space of homogeneous quartics on R^(2x2)
invariant under left SO(2). Put C A=(a-d,b+c), H(A)=|CA|^4. Let R and Q denote
its rank-one-convex and all-background quasiconvex cones; pi is quotient by
span H. The internally established conclusion is

    pi(R)=pi(Q).

Equivalently, for every G in V,

    exists finite a: G+aH is ROC
      iff exists finite b: G+bH is QC.

No equality a=b, least coefficient, original-coefficient QC, full planar
Morrey theorem or classification of the unprojected QC cone is asserted.

## 1. The easy direction and the immutable acoustic interface

QC implies ROC for continuous quartic integrands by the classical necessary
Legendre-Hadamard condition. H is convex and D²H(I)=D³H(I)=0. Suppose G+aH is
ROC. Then q(R)=D²G(I)[R,R]>=0 for every rank-one R. All compactness and contacts
below concern this exact supplied polynomial, not a numerical approximate zero.

## 2. Strict conformal branch: a classical theorem

If q(R)>0 for all nonzero rank-one R, compactness on unit rank-one matrices
gives mu>0 with q(R)>=mu|R|². Every nonzero conformal U=sQtheta satisfies

    D²G(U)[R,R] = s² D²G(I)[Qtheta^T R,Qtheta^T R]
                 >=(mu/2)|U|²|R|².

Here |I|²=2 accounts for the factor1/2. Left invariance and quartic homogeneity
are indispensable; this is not a claim for arbitrary quartics.

A direct classical Fourier/Taylor/Young absorption proof is reproduced in
workers/fy_contact_independent_audit/STRICT_CONFORMAL_COMPLETION.md. With
q=one-half D²G(I), q(R)>=delta|R|² on rank-one R, and M bounding the polarized
quartic tensor, it gives the sufficient coefficient

    b >= 25144 M²/delta + (9391/4) M.

Fourier rank-one gradients imply integral q(Dphi)>=delta integral|Dphi|².
For B=sI+E, the exact quartic Taylor expansion is bounded below by
(delta/2)s² integral|Dphi|² minus
(288M²/delta+8M)|E|² integral|Dphi|² and
(32M²/delta+3M) integral|Dphi|⁴. The H remainder controls both losses via
integral|CDphi|²=integral|Dphi|² and the inherited finite Cauchy-Riemann L4
bound. These estimates hold for every background and extend by W^(1,4)
density. This strict branch uses classical elliptic absorption machinery;
it is not a new discovery of this round. The Iwaniec-Kristensen 2005 primary
Theorem 3.1 and Lemma 4.1 are separately acquired and credited; a stronger
unadmitted preprint is not a premise.

## 3. Nonstrict branch: exhaustive normalization

Otherwise there is a nonzero rank-one R=eta tensor xi with q(R)=0. Choose
P in SO(2) with P^T xi=|xi|e1 and set Gtilde(A)=G(P A P^T). Then its contact
is Rtilde=P^T R P=(P^T eta) tensor(|xi|e1). Nonzero rescaling of a rank-one
direction preserves the zero. Writing the transformed target vector as
(c1,c2) gives exactly three cases:

1. c2=0: Rtilde is a multiple of e11 (parallel contact).
2. c2!=0,c1=0: Rtilde is a multiple of e21 (trace-free contact), which a
   quarter-turn conjugation sends to a multiple of e12.
3. c1*c2!=0: Rtilde is a multiple of (t,1) tensor e1, t=c1/c2 finite and nonzero.

These cases include all rank-one contacts at I. No classification of contacts
at singular/nonconformal backgrounds is needed: failure of the strict branch
already produces a contact at invertible I.

Orthogonal conjugation preserves I,H,left-SO(2) invariance and ROC. To verify
QC rather than assume it, for y=P x put psi(y)=P phi(P^T y). Then
Dpsi(y)=P Dphi(P^T y)P^T, detP=1, and the transformed domain is P Omega.
Zero trace, W^(1,4) regularity, Frobenius norms and Lebesgue measure are preserved.
Thus the all-domain/all-background QC inequalities transport in both directions.
H(P A P^T)=H(A) follows from H=(|A|²-2detA)². Reflections are unnecessary for
exhaustive coverage, although they also preserve this interface.

The known contact-span arguments use ROC stationarity in all background/output/
input directions, not the single scalar contact equality alone. They therefore
apply to Gtilde+aH, yielding its appropriate four-dimensional form. Since H is
one of the span generators, Gtilde belongs to that same span.

## 4. The three boundary dependencies

For trace-free e12 contacts, the existing complete finite-H shear projection
already proves pi(R_shear)=pi(Q_shear), including positive-delta *sufficient
high-coefficient* completion. The stronger negative-delta sharp theorem is
not required to improve any positive sharp coefficient here. Its actual
pinned proof, not the absent new producer ZIP, is the receiving premise.

For parallel e11 contacts, pinned N873 supplies the exact nonshear finite-H
projection: convex exception k=ell=0,m>=0, or k>0,ell+2m>0,
2km-kell-ell²>0, in the basis H,w²,vj,v². Every finite ROC-completable member
there receives a finite QC completion.

For generic finite t!=0 put n=1+t²,L=t w-j+v. The new internally audited theorem
classifies the stationary span

    H, L², v(j-2L/n), v².

For coefficients k,ell,m, finite ROC/QC completion is equivalent to
the convex exception k=ell=0,m>=0 or

    m>|ell|/2,
    Delta=k n²(2m-ell)(2m+ell)
          -ell²[t²(2m+ell)+3(2m-ell)] >0.

The new necessity excludes every non-convex singular boundary using a second
rank-one kernel direction and a nonzero background acoustic derivative. The
strict part receives the pinned degenerate-flat analytic compiler. All weak
and zero cases passed independent equation-first and analytic reconstruction.
This is the decisive new input for the full-space theorem; coverage alone
cannot discharge it.

With that lemma accepted internally, cases1-3 yield a finite QC coefficient for
Gtilde, and conjugation returns a finite coefficient for G. This proves the
projection equality.

## 5. Consequences and limits

By this theorem, any prescribed nu>0 can be reserved as additional
nuH after one finite QC completion. The classical H Bregman/elliptic estimate
gives margin4nu/1875 against integral |Dphi|⁴. The threshold depends on G and
can diverge near excluded boundaries. This does not resolve the uniform
margin of an unchanged sharp J_r or authorize its N866 storage transfer.

The inherited exact 8x8 acoustic Gram lift describes R with six skew auxiliaries.
Adding the free H coefficient and projecting therefore becomes an exact finite
PSD feasibility interface for *eventual QC completion*, with the theorem now established internally.
The new block-range criterion gives its singular-boundary interpretation:
C(z)>=0 and ker C(z) subset ker B^T for some one conformal skew and four mixed
skews. These are exact mathematical interfaces. Weak infeasibility, irrational
certificates, coefficient/contact acquisition and finite precision are not
removed by an approximate solver return. No practical solver advantage or
general QC decision algorithm follows.

The completed projection remains nonclosed, with the already proved boundary
example w²+epsilon v² tending to w². Its closure is the conformal-LH cone,
already a classical receiving corollary. Nonspectrahedrality and non-hyperbolicity
of the unprojected ROC cone are classical consequences of the inherited
nonexposed rays; neither rules out its existing PSD lift.

## 6. A necessary completion cost

The generic-angle family t=1, ell=m=1, k=1/2+eta, eta>0, is finitely completable.
A fixed rank-one direction at backgrounds I+sE gives an exact quadratic whose
discriminant forces every ROC (and hence every QC) completion to obey

    alpha >= 1/(32 eta) + 13/80 + 47 eta/200.

The explicit sufficient compiler is O(1/eta), so the divergence has the same
order in both directions. This is intrinsic, rather than merely loss in a
conservative sufficient estimate. No sharp leading coefficient or least-alpha
claim follows. Source: constructor REPORT.md equation25 and independent audit
FULL_PROJECTION_AUDIT.md, pinned to final constructor bytes below.

## 7. Verification state for this version

The root reconstructed the strict/conformal dichotomy and exhaustive contact
normalization, read the generic construction and independent audits, and
adjudicated the universal analytic arguments rather than counting agreements.
The contact constructor REPORT.md SHA-256 is
c09ce5c78d725886ff86fcbdb80c385a77fa49b36ef7874e0cd63c6e5e079715 (363 exact
assertions). Independent contact reconstruction supplies the separate strict
proof and checks the discriminant lower bound. A second independent full-space
audit supplies FULL_PROJECTION_PROOF.md, 40 exact checks and a protected-input
receipt. These are internal reconstruction and finite algebra checks, with
distinct scopes; they are not external verification.

Pinned dependencies at inspected repository revision
b32943eeb62d0d79929a9e572a344219a785ebf9: N872 trace-free/shear finite-completion
projection, N873 parallel projection and degenerate-flat analytic compiler,
and their exact source records. Current-round paths are workers/
fy_contact_angle_genesis, fy_contact_independent_audit, fy_global_projection_audit,
and fy_global_cone_geometry; the selected preservation manifest supplies exact
file hashes. No unavailable producer ZIP is a dependency.

All QC conclusions mean every bounded planar Lipschitz Omega, every real affine
B, every phi in W0^(1,4)(Omega;R²), plus the periodic analogue. If an initial
coefficient a is ROC, a QC coefficient b>=a can be chosen by further convex H
padding. The proof does not show b=a, fixed-alpha cone equality, Morrey's full
conjecture, efficiency against a measured solver, physical regularization or an
acquired measurement operation. Historical originality and external correctness
remain UNKNOWN. The separate primary-preprint construction counterexample is
recorded independently and is not needed for this theorem.
