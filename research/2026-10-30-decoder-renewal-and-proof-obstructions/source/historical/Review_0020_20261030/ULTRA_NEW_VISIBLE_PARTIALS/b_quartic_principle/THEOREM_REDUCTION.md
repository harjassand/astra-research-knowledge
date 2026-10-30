# A quartic endpoint at which polyconvex extraction has no budget

This is a construction/reduction, not a quasiconvexity counterexample.
The final ordinary-heat question in Section 6 remains OPEN. The separate
`POLYNOMIAL_BARRIER.md` resolves it negatively only for polynomial
primitives, and more generally for 2-form coefficients C² at the origin.

All matrices and coefficients below are real. Set

    A=[[a,b],[c,d]], T=a²+b²+c²+d², q=ad−bc,
    x=a²+c²−b²−d²,
    F*(A)=T²+12q²+4qx.                                      (1)

The cone in Sections 1–3 consists of ALL 35-dimensional homogeneous
quartic POLYNOMIALS on R²ˣ². Summands have no imposed objectivity,
even-Hopf structure, or symmetry. A polyconvex summand can use an
arbitrary convex representative on the minors; its lift need not be
polynomial. Nonpolynomial homogeneous summands are not covered.

## 1. Rank-one convexity and positivity

Write y=2(ab+cd), z=2q. Then T²=x²+y²+z² and

    F*=x²+y²+2xz+4z².

The quadratic form on (x,y,z) is positive definite, so F*>0 off zero.
For quartics, D²F(A)[R,R]=D²F(R)[A,A]. Therefore it suffices to check
the whole Hessian at rank-one R. The literal acoustic calculation in
sol9/hopf/PROOF.md §1, specialized to beta=1,r=4, gives after positive
Schur elimination

    N=[[1−s,−2 sin(theta)], [−2 sin(theta),7−3s]],
    s=cos²(theta), det N=3(1−s)², 0≤s≤1.

N is positive semidefinite, including s=1. This proves ROC everywhere.
No strict ROC margin is asserted. The accepted sol9 calculation is an
input; the exact endpoint/face work below is new to this packet.

## 2. Two acoustic zero orbits expose a two-dimensional face

For an arbitrary quartic G, let

    f_G(A,eta,xi)=D²G(A)[eta⊗xi,eta⊗xi].

Let R_theta=[[C,−D],[D,C]], without requiring C²+D²=1; homogeneity
pays arbitrary C,D. Direct substitution into (1) gives f_F*=0 at

    A=[[-D,C],[C,D]], eta=(C,D), xi=(1,0);            (orbit 1)
    A=[[C,−D],[D,C]], eta=(C,D), xi=(0,1).            (orbit 2)

Suppose F*=G+H with G,H ROC quartics. Then f_G,f_H≥0 and both vanish
on both displayed orbits. Every first derivative of each nonnegative
polynomial with respect to the eight variables (A,eta,xi) vanishes
there. Expand the eight derivative identities for each orbit in C,D.
They are linear constraints on the 35 coefficients of G.

The complete integer matrix, with duplicate rows removed, is stored in
`EXTREME_FACE.json`. It has 64 rows, exact rank 33, and kernel

    span { q², T²+4qx }.                                  (2)

This is not a sampled acoustic check. `extreme_face.py` expands all
monomial derivatives symbolically. Independently, `qualify_face.py`
uses only integer monomial differentiation and Fraction elimination;
it reconstructs the whole matrix, rank 33, and the two independent
kernel vectors, importing no symbolic producer. The explicit pivot
columns and complete matrix make the finite linear claim replayable.

Thus G=alpha(T²+4qx)+b q². Rank-one values force alpha≥0. If alpha=0,
ROC forces b≥0. If alpha>0 put delta=b−12alpha. At A=[[0,1],[1,0]],
xi=(1,t), its acoustic matrix is

    [[(64alpha+2delta)t², (32alpha+2delta)t],
     [(32alpha+2delta)t, 16alpha(1+t²)+2delta]].

Its determinant has t² coefficient 32alpha delta. Hence delta≥0.
Conversely alpha F*+delta q² is ROC if alpha,delta≥0. The exposed
face (2) therefore has precisely the rays q² and F*.

If F*=G+H, write both as nonnegative combinations of these two rays.
The q² coefficients must sum to zero. Consequently G,H are nonnegative
multiples of F*. In particular:

**F* generates an extreme ray of the full cone of ROC quartic
polynomials.** This is extremality in the full 35-dimensional space,
not merely the six-parameter even-Hopf slice.

## 3. It has no nonzero polyconvex quartic summand

A polyconvex F finite and differentiable on the minors graph has at
each A a scalar k_A with

    F(A+X)−F(A)−DF(A):X−k_A det X≥0 for all X.             (3)

This permits any convex lift. Such a lift is finite on all R⁵ because
every (B,s) is the mean of the graph points B±Y when det Y=s−det B;
it consequently has a touching affine support. Quartic polarization
and minimization over a line imply the necessary cut

    k_A det R≤c2−c1²/(4c0),

where F(R+tA)=c0+c1 t+c2 t²+... and c0>0. This is precisely the
unrestricted support lemma already proved in sol9/hopf/PROOF.md §2.

At A=I use R+=[[0,200],[−1,0]], R−=diag(1,−2). Literal coefficients
for F* are

    R+: c1=0, c2=4808, det R+=200;
    R−: c0=97, c1=−8, c2=−48, det R−=−2.

Thus (3) would require simultaneously

    k_I≤601/25,     k_I≥2336/97,
    2336/97−601/25=103/2425>0.                          (4)

F* is not polyconvex. If F*=P+G with P a polyconvex quartic polynomial
and G a ROC quartic polynomial, extremality makes P a multiple of F*;
(4) forces that multiple to vanish. The same holds for any finite sum
of such summands. The argument rules out arbitrary convex minor lifts,
not just SOS/polyconvex Gram parameterizations.

The assertion does NOT extend automatically to nonpolynomial functions
P,G whose angular dependence cancels in their sum. No claim of
extremality in that infinite-dimensional cone is made.

## 4. Exact-form certificates and symmetry transport

For ordinary heat, the pointwise completion inequality is

    C(A)[h]=D²F(A)[B1,B1]+D²F(A)[B2,B2]+Omega_A(B1,B2)≥0,
    B1=(h0,h1,h3,h4), B2=(h1,h2,h4,h5), Omega=d alpha.  (5)

For another constant real second-order operator L, use its usual
integration-by-parts heat density Q_F,L, linear in L. This packet
admits the full angular exact-form class from the accepted ROOT26
framework: coefficients of Omega are homogeneous degree 2, smooth
away from zero; equivalently alpha can be homogeneous degree 3 with
C² coefficients at zero. The stricter origin regularity in the
companion barrier is an additional restriction, not this full class.

Under a gradient symmetry Phi(A)=C A R with C,R orthogonal, an exact
correction transports as

    alpha_new=det(R) Phi* alpha.                          (6)

Indeed the pair of spatial derivatives transforms by R and its wedge
picks up det R. Formula (6) keeps both positivity and exactness; the
sign for a spatial reflection must not be omitted. Averages over a
compact symmetry group retain both properties and regularity.

F* is invariant under all left row rotations, column swap, and
A→C A C with C=diag(1,−1). The last two operations normalize the
rotation group and commute after its central sign is averaged.

## 5. Every constant-flow certificate reduces to ordinary heat

Assume a constant-flow exact-form certificate for F* and assume the
flow converges to the mean on every finite Fourier polynomial. Thus
the eigenvalues of L(xi) have positive real part at every nonzero
integer xi. This is enough for the usual energy proof of periodic QC;
no unstated uniform parabolic existence theorem is needed here.

Left rotation averaging projects each real output matrix onto span{I,J},
where J=[[0,−1],[1,0]]. The reflection A→C A C removes its scalar
off-diagonal spatial entry and its J diagonal entries. Column swap equalizes the remaining scalar
diagonals. Consequently the averaged symbol is

    Lbar(xi)=ell |xi|² I+2nu xi1 xi2 J,
    ell=(Tr L11+Tr L22)/4>0.                              (7)

Positivity of the two traces follows at xi=e1,e2 from mean convergence.
We do not assume that the Hurwitz matrix cone is convex: the explicit
averaged operator (7) itself has eigenvalues with real part ell|xi|².

On any rank-one Hessian symbol h=eta⊗xi⊗xi all wedge corrections vanish.
Hence sym[B_F(A,xi)Lbar(xi)] must be positive semidefinite. At
A=[[0,1],[1,0]], xi=(1,t), the literal acoustic matrix is

    B=[[64t²,32t],[32t,16(1+t²)]].

The exact determinant after (7) is

    256t²(1+t²)[4ell²t⁴+4ell²t²−9nu²t²−nu²].           (8)

Its t² coefficient is −256nu², so positivity for all small t forces
nu=0. `flow_rigidity.py` acquires the literal matrix/determinant for
arbitrary real ell,nu,t, without sampled diffusion coefficients.
Rescaling by ell leaves an ordinary-heat certificate. Conversely
ordinary heat is an allowed constant mean-converging flow.

Thus **F* has a constant mean-converging exact-form certificate iff it
has an ordinary-heat exact-form certificate**, at every origin
regularity level retained by symmetry averaging.

## 6. Consequence for the proposed combined operation

Suppose a finite decomposition of F* uses polyconvex homogeneous
quartic POLYNOMIAL parts and homogeneous quartic POLYNOMIAL parts
with actual constant mean-converging exact-form heat certificates.
Every heat part is QC and hence ROC; extremality makes it a
nonnegative multiple of F*. All polyconvex parts vanish by (4).
Therefore this decomposition exists if and only if F* itself admits
an ordinary-heat certificate.

The companion proof shows that this is impossible if the correction
coefficients are C² at zero, even for nonhomogeneous polynomial
primitives of arbitrarily high degree. Therefore the combined
**PC-quartic + origin-regular heat** operation is incomplete.

The full angular/rational case remains OPEN. A rational homogeneous
primitive P5(A)/T is ordinarily only C² at zero, with Omega merely C¹;
it escapes the proven regularity barrier. The ROOT25 positive non-PC
heat example uses exactly that legitimate escape. Its existence is
not contradicted here. Nor has a negative heat trajectory or negative
all-angular conserved current for F* been acquired.

Affine minor/null-Lagrangian terms can be added and removed without
changing heat dissipation or QC. They supply no independent homogeneous
quartic null term in real 2×2. In the polynomial scope this last fact is
elementary: rank-one affinity along each coordinate makes the polynomial
multiaffine, so a homogeneous quartic would be a multiple of abcd.
Affinity along E11+E12 then forces that multiple to be zero.
This is not a proof about arbitrary
nonhomogeneous/nonpolynomial cancellations between summands.

The precise next missing operation is consequently an angular closed
selection for this extreme endpoint, or an actual distributed dual
obstruction. Increasing a polynomial primitive's degree cannot acquire
it. Generic SDP failure, local jet compatibility, or a positive
finite Fourier search cannot decide which alternative is true.
