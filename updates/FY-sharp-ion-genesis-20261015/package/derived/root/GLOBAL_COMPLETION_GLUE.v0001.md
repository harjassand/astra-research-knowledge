# Full invariant completion projection: contact coverage and exact dependencies

Root synthesis and proof, 15 October 2026. This version records a theorem
conditional on successful independent review of the new generic-angle lemma.
It is not an integration status or historical originality claim. A later
version must explicitly adjudicate that obligation without replacing these bytes.

Let V be the real nine-dimensional space of homogeneous quartics on R^(2x2)
invariant under left SO(2). Put C A=(a-d,b+c), H(A)=|CA|^4. Let R and Q denote
its rank-one-convex and all-background quasiconvex cones; pi is quotient by
span H. The claimed conclusion is

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

The pinned classical finite-completion corollary first adds cH to make a
global strict LH inequality, then applies Iwaniec-Kristensen (2005), Theorem3.1
and Lemma4.1, with p=4 and the elliptic operator C. Its exact proof and constants
are in the preceding FX CLASSICAL_FINITE_COMPLETION_COROLLARY.md. It yields one
finite b, independent of background and test function, making G+bH QC. This
branch is classical, not a new discovery of this round.

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

For generic finite t!=0 put n=1+t²,L=t w-j+v. The new candidate theorem
classifies the stationary span

    H, L², v(j-2L/n), v².

For coefficients k,ell,m, finite ROC/QC completion is asserted equivalent to
the convex exception k=ell=0,m>=0 or

    m>|ell|/2,
    Delta=k n²(2m-ell)(2m+ell)
          -ell²[t²(2m+ell)+3(2m-ell)] >0.

The new necessity excludes every non-convex singular boundary using a second
rank-one kernel direction and a nonzero background acoustic derivative. The
strict part receives the pinned degenerate-flat analytic compiler. All weak
and zero cases must pass independent equation-first and analytic review.
This is the decisive new input for the full-space theorem; coverage alone
cannot discharge it.

Upon acceptance of that lemma, cases1-3 yield a finite QC coefficient for
Gtilde, and conjugation returns a finite coefficient for G. This proves the
claimed projection equality.

## 5. Consequences and limits

Once the theorem passes, any prescribed nu>0 can be reserved as additional
nuH after one finite QC completion. The classical H Bregman/elliptic estimate
gives margin4nu/1875 against integral |Dphi|⁴. The threshold depends on G and
can diverge near excluded boundaries. This does not resolve the uniform
margin of an unchanged sharp J_r or authorize its N866 storage transfer.

The inherited exact 8x8 acoustic Gram lift describes R with six skew auxiliaries.
Adding the free H coefficient and projecting therefore becomes an exact finite
PSD feasibility interface for *eventual QC completion*, if the theorem passes.
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

## 6. Verification state for this version

The root reconstructed the strict/conformal dichotomy and normalization proof
and read the entire generic-angle construction. A separate constructor and two
independent same-team audits are working on the load-bearing generic-angle and
coverage lemmas. Their agreement would remain internal verification. Historical
priority, external correctness and formal verification are UNKNOWN.
