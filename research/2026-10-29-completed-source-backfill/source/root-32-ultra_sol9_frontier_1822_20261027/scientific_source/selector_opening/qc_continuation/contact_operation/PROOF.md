# Strict QC contacts: exact neighborhood transport and a finite Hopf cover

**No new target QC claim is made.** This note supplies the missing rigorous
operation from strict point contacts to every affine background. It proves
explicit contact radii, equivariant transport, and an exact rational cover
test. Actual target contacts must be acquired and verified separately.

## 1. Point contacts and the integrated implication

Let F be a homogeneous quartic on real 2x2 matrices. For a differentiable
energy G, write

    B_G(A,X)=G(A+X)-G(A)-DG(A):X.

Suppose H is a globally QC polynomial, A0 is fixed, and a,b>0,k are scalars
such that, for every real X,

    B_F(A0,X)-B_H(A0,X)-k detX
        >=a|X|^2+b|X|^4.                              (1)

The model H may be a positive sum of shifted, transported known QC quartics.
For a smooth zero-boundary perturbation phi, integrate (1) with X=Dphi.
The derivative terms and determinant null-Lagrangian have zero integral;
QC of H at A0 gives

    integral [F(A0+Dphi)-F(A0)]
        >=a integral |Dphi|^2+b integral |Dphi|^4.      (2)

The model and k are fixed for this affine background. No cancellation of
a spatially varying model or selector is used. Quartic growth and strong
W1,4 density extend (2) to W1,4_0 on bounded Lipschitz domains.

There is also an explicit touching QC lower contact. Define

    L_A(B)=H_A(B)+F(A)-H_A(A)
       +[DF(A)-DH_A(A)-k cofA]:(B-A)
       +k(detB-detA).

Its difference from F is B_F(A,X)-B_(H_A)(A,X)-k detX, X=B-A.
It touches at A and is QC, since adding an affine function and a constant
multiple of the determinant preserves the QC integral inequality. If such
contacts exist at every A, F=sup_A L_A and F is QC by choosing the touching
contact at the tested background. This direct proof uses Morrey QC.

## 2. Recenter a point model without reacquiring its coefficients

Given (1), for a nearby background A set

    H_A(B)=H(B-A+A0).

Then H_A is QC and

    B_(H_A)(A,X)=B_H(A0,X).                            (3)

All model shifts are simply translated by A-A0. Its positive coefficients
and input/output maps remain unchanged. Therefore the only change in (1)
is B_F(A,X)-B_F(A0,X), not a derivative of the acquired model.

Let C be the l1 norm of F's coefficients in the ordinary 35-monomial
quartic basis. Assume |A|=|A0|=1 and put d=|A-A0|. Product differentiation
of a degree-four monomial gives

    ||D3F(B)||<=24C|B|,       ||D4F||<=24C.

Quartic Taylor expansion and integration along the segment between the two
unit matrices, whose norm is at most one, yield

    |B_F(A,X)-B_F(A0,X)|
       <=12Cd|X|^2+4Cd|X|^3
       <=Cd(14|X|^2+2|X|^4).                         (4)

The quartic-in-X term cancels exactly. Thus (1), with H_A from (3) and
the same k, retains at least half its two margins whenever

    |A-A0|<=r,
    r<=min(1/2,a/(28C),b/(4C)).                       (5)

This is a continuum statement for every X, including arbitrarily large
increments. It does not extend a contact merely from a bounded X sample.

For a nonzero, unnormalized center A0 with T0=|A0|^2, use the exact
normalization

    A0_unit=A0/sqrt(T0),
    H_unit(B)=T0^(-2) H(sqrt(T0) B),
    a_unit=a/T0, b_unit=b, k_unit=k/T0.

Then (1) holds at the unit center with these normalized data. Its Hopf
normal h(A0)/T0 is rational when A0 is rational, even when the normalized
matrix or some normalized shifts are algebraic.

## 3. Symmetry and homogeneous transport

For the accepted even-Hopf targets, F is invariant under left row rotations
and the spin flip

    J([[a,b],[c,d]])=[[-b,a],[d,-c]],
    h(JA)=-h(A).

Both are orthogonal maps of the form Q(A)=P A S, with P,S orthogonal.
Write chi=detP detS in {+1,-1}. A contact model at A0 transports to

    A0'=Q A0,       H'(B)=H(Q^(-1)B),       k'=chi k.

Its two margins are unchanged. QC of H' follows by the corresponding
change of independent/dependent variables. The positive shifted-model
class is closed under this operation: shifts become Q(C_j), while the
left/right matrices are multiplied by P^(-1),S^(-1).

Scaling to rho A, rho>0, uses

    H_rho(B)=rho^4 H(B/rho),       k_rho=rho^2 k.

The quadratic margin becomes rho^2 a and the quartic margin remains b.
For homogeneous quartic model generators, this only scales their shifts
by rho; their positive coefficients and linear maps can be retained.

Consequently, a finite cover of the unit backgrounds by transported
contact balls proves QC at every nonzero background. With half-margins
from (5), take a*=min_i a_i/2 and b*=min_i b_i/2. The result is the uniform
compatible-gradient bound

    integral [F(A+Dphi)-F(A)]
       >=a*|A|^2 integral |Dphi|^2+b* integral |Dphi|^4.

Letting A tend to zero proves the same inequality there, by quartic
continuity and integrability. No model at the zero matrix has to be guessed.

## 4. Exact quotient distance and cap thresholds

For unit matrices A,B let n_A=h(A), n_B=h(B), both on S2. Treating the
two real columns as a complex spinor, the exact identity is

    |<spinor(A),spinor(B)>_C|^2=(1+n_A dot n_B)/2.

Left rotations are multiplication of that spinor by a complex phase.
Therefore

    min_(R in SO2) |A-RB|^2
       =2-2sqrt((1+n_A dot n_B)/2).

Including the J orbit replaces the dot product by its absolute value.
For a unit center with contact radius r<=1/2, its entire symmetry orbit
therefore covers exactly the Hopf cap pair

    |n dot h|>=kappa(r),
    kappa(r)=1-2r^2+r^4/2.                            (6)

All thresholds in (6) are rational for rational r^2. Here kappa>=17/32>0.
Given a covered direction, one selects the sign of the cap, aligns the
complex phase, recenters using (3), and transports back. The complex inner
product in this step is nonzero, because the chosen cap has positive
threshold. Thus this is an explicit pointwise contact selection rule.

## 5. Cover S2 by checking a rational three-dimensional polytope

For finitely many cap pairs (n_i,kappa_i), with unit n_i and kappa_i>0,
form

    P={v in R3: |n_i dot v|<=kappa_i for every i}.     (7)

If the normals do not span R3, a nonzero common orthogonal vector gives
an uncovered unit direction. Otherwise P is a bounded, full-dimensional,
origin-symmetric polytope containing zero in its interior.

**Exact cover criterion.** The closed cap pairs in (6) cover all of S2
if and only if every vertex of P has squared norm at most one.

Proof: if all vertices have norm at most one, convexity of the norm puts
all P in the unit ball. A unit vector strictly outside every closed cap
would satisfy all inequalities in (7) strictly. Since all kappa_i>0, it
could be scaled slightly beyond norm one while staying in P, a
contradiction. Conversely, if a vertex v has |v|>1, then v/|v| satisfies
all slab inequalities strictly, and hence misses every closed cap.

A vertex has three linearly independent active planes. Enumerate triples
of normals and their eight possible signs, solve the 3x3 systems, and
retain the solutions satisfying all the slabs. All steps use rational
arithmetic. With N caps, at most 8 binomial(N,3) candidate systems and
O(N^4) rational arithmetic operations suffice. This is a fixed-dimensional
cover verifier, not a claim that few contact patches will suffice.

When the maximum squared vertex norm is greater than one, the verifier
returns an exact rational v and the algebraic uncovered direction
v/sqrt(|v|^2). This witnesses a missing contact neighborhood; it is not
a violation of QC. Equality at one is correctly accepted for closed caps.

An uncovered unit Hopf vector n=(x,y,z) gives an explicit next matrix
background: if x>-1, set a=sqrt((1+x)/2) and take
A=[[a,y/(2a)],[0,z/(2a)]]. If x=-1 use A=[[0,1],[0,0]]. These matrices
have unit norm and Hopf vector n. Thus the geometric failure has a
constructive acquisition output rather than only a Boolean result.

## 6. What a finite all-background certificate must contain

1. Literal F and a completed QC proof for every model generator used.
2. At each nonzero center, an exact global-in-X point contact (1), with
   positive rational margins. A numerical Gram margin is only acquisition.
3. The radii from (5), or independently verified larger neighborhoods.
4. Symmetry hypotheses and the exact cap-cover certificate from Section 5.

These items are sufficient for the all-background QC theorem. If strict
contacts of the specified class exist at every unit background, their open
neighborhoods have a finite subcover by compactness. This does not assert
that every strictly QC energy has such contacts, or that a fixed dictionary,
SOS degree, or affordable number of patches is complete.

A 14-feature point SOS certificate can also generate a larger semialgebraic
patch. Keep its acquired model increment profile and k fixed and add a
fixed linear coefficient-to-Gram lifting of B_F(A,X)-B_F(A0,X) to its Gram.
The correction is polynomial of degree at most two in A. Positivity of
this explicitly corrected Gram defines a sufficient patch. The radius
bound above is a simple fallback that needs no additional SDP.

For the root's complete feature list (four linear and ten distinct quadratic
X monomials), an exact Gram bound R>=tau I with tau>0 gives (1) with
a=tau and b=tau/2, since the quadratic-feature square sum is at least
|X|^4/2. At the raw center A0=I, normalization gives a_unit=b_unit=tau/2.
Thus the immediately usable guaranteed radius is
min(1/2,tau/(56C)); larger exact Gram patches may be used instead.

## 7. Controls, actual acquisition state, and the earlier obstruction

`cover_caps.py` implements the exact slab-polytope operation. The three
coordinate cap pairs of radius 1/2 have kappa=17/32 and maximum squared
vertex norm 867/1024<1, so they cover. Radius 1/4 leaves a computed uncovered
direction. One pole orbit alone fails by the missing orthogonal directions.
These are exact geometry controls, conditional on the supplied contact
neighborhoods, not new target contact certificates.

`verify_contact_identities.py` independently checks recentering, homogeneous
Bregman expansion, the complex/Hopf identity, and the global norm-fourth
strict-contact control. The known QC control DM+(positive)norm-fourth also
has an analytic all-background contact selection H=DM, with the convex
norm-fourth residual. Its use of two separately certified cap signs does
not assume the DM energy has the target's J symmetry.

The initial 120-model `parent/qc_contacts/ACQUISITION.json` record gives numerical
fixed-background margins about -0.000251891 for the ordinary PC target,
+0.00814229 for the known-QC control, and -0.000248824 for the initial
target contact dictionary. They are recorded numerical acquisition values,
not exact feasibility or infeasibility certificates. In particular, this
continuation has no verified target point contact to place in a cover.

The final parent acquisition in `parent/qc_contacts/full_cone.py` uses
198 selected maps/centers and the entire isotropic ROC/QC cone for each,
including the critical whitening maps. The parent reports a positive
matched-control margin about 0.02850054 and a negative target margin about
-0.0002480912, with affine residual about 2.64e-9. No positive target
candidate was acquired. This is a bounded numerical result for that
specified contact family; it does not exclude other contacts or QC.

The ordinary QC input for the control is the established full-range DM
theorem, [Bruno--Pasqualotto, Theorem 1](https://arxiv.org/html/2608.06367v1).
The selected gamma=9/8 obeys gamma^2<4/3 exactly. The norm-fourth residual
and its strict margins are verified here; the DM QC theorem is credited
to that primary source.

The earlier transfer obstruction does not prohibit this operation. It
concerns global positive homogeneous decompositions after projection.
Here models are shifted, chosen separately for the tested background,
and combined by a supremum of touching lower contacts, rather than one
global positive sum. The argument is a valid possible escape, but actual
all-background QC still requires the completed finite certificate above.
