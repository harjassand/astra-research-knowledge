# A second acoustic-contact stratum with an exact finite-distortion projection

15 October 2026. Independent internal mathematical derivation.

This report proves an equality of projected rank-one-convex and quasiconvex
cones on a contact stratum different from the supplied shear-contact face.
It includes a direct analytic completion argument, exact polynomial
identities, and explicit obstructions on both excluded equality boundaries.
The result is model-assisted and internally checked. External correctness,
formal verification, and historical priority remain UNKNOWN.

No current other-worker research artifact was read. The source report
`sources/global_compatible_positivity/RESEARCH_REPORT.md`, the inherited
`contact_face_priority_audit/STRUCTURAL_PROOF.txt`, and the inherited
`moving_kernel_genesis/REPORT.v0002.txt` were read. They establish the
notation and distinguish the old shear contact. Their heat certificates are
not premises of the new analytic completion proof. A root coordination
message identifying older literature is recorded separately in Section 11.

## 1. Exact theorem

Write

\[
A=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
u=a^2+c^2,\quad v=b^2+d^2,\quad w=ab+cd,\quad j=ad-bc,
\]
\[
\mathcal C A=(a-d,b+c),\qquad H(A)=|\mathcal C A|^4.
\]

Let V be the nine-dimensional real space of homogeneous quartics invariant
under left SO(2), and let K be its rank-one-convex cone. The acoustic
functional

\[
\ell_{11}(F)=D^2F(I)[e_{11},e_{11}]
\]

is nonnegative on K. Its zero set in K is therefore an exposed face.

**Theorem 1 (contact span).** Every F in this face has the unique form

\[
F_{\alpha,k,\ell,m}=\alpha H+k w^2+\ell vj+m v^2. \tag{1}
\]

Conversely every polynomial (1) has the indicated acoustic contact, whether
or not it is rank-one convex.

**Theorem 2 (exact projection).** For every real triple (k,ell,m), the
following are equivalent:

1. Some finite real alpha makes (1) rank-one convex.
2. Some finite real alpha makes (1) quasiconvex at every affine background.
3. Either

\[
k=0,\qquad \ell=0,\qquad m\ge0, \tag{2}
\]

or

\[
k>0,\qquad L:=\ell+2m>0,\qquad
D:=2km-k\ell-\ell^2>0. \tag{3}
\]

The quasiconvexity contract is every bounded planar Lipschitz domain Omega,
every B in R^(2x2), and every phi in W_0^(1,4)(Omega;R^2). A periodic
contract also follows, as explained below. This is an equality of the
projections obtained by deleting alpha. It does not identify the least
alpha, assert equality of the unprojected cones, or settle the full
nine-dimensional cone.

In case (2), every alpha>=0 works by ordinary convexity. In case (3), set

\[
\tau=2k+L,\qquad
\kappa=\frac{3LD}{D+3L\tau},\qquad
M=4(|k|+|\ell|+|m|).
\]

All these numbers are finite, with kappa,M>0. An explicit sufficient
coefficient is

\[
\boxed{\alpha_*=
401296\frac{M^2}{\kappa}+\frac{9391}{4}M.} \tag{4}
\]

Every alpha>=alpha_* makes (1) quasiconvex. These constants are intentionally
conservative. They come from direct Taylor and Young inequalities and a
classical nonsharp L4 Beurling estimate; no matrix optimizer, search over
gradients, or claimed sharp transform norm is used.

If alpha>=alpha_*+nu with nu>=0, then

\[
\int_\Omega [F(B+D\phi)-F(B)]
\ge \frac{4\nu}{1875}\int_\Omega |D\phi|^4. \tag{5}
\]

## 2. Why this is a different contact stratum

The inherited face uses (A,R)=(I,e12); there
tr(A^-1 R)=0. Here the contact is (I,e11), with tr(A^-1 R)=1.
Under any invertible two-sided change (A,R)->(P A Q,P R Q), the matrix
A^-1 R changes by conjugation with Q, so its trace is unchanged. Thus no
such transformation sends this contact pair to the inherited shear pair.
The distinction is geometric and not just a change of coefficients.

The present theorem covers this contact and its applicable linear
transports, not every full-rank contact of nonzero trace. In particular,
general contacts (I,e1 tensor (1,t)) with t!=0 retain an angle parameter
under orthogonal conjugation; their full coefficient projections are not
classified here.

There is also a stronger global distinction for the completed members in
case (3). Section 9 proves that their only acoustic contacts at nonzero
backgrounds are

\[
B=sQ_\theta,\qquad R=rQ_\theta e_{11},
\qquad s>0,\ r\ne0,\quad Q_\theta\in SO(2). \tag{2a}
\]

Every one has tr(B^-1 R)=r/s!=0. Consequently none of these completed
quartics can equal any invertible two-sided linear transport of a quartic
carrying an invertible trace-free acoustic contact: that contact would be
transported to a trace-free contact somewhere. In particular this excludes
all such transports of members of the inherited shear-contact face.
No exclusion of positive sums or limiting constructions is inferred.

## 3. Derivation of the contact span

Every member of V has the unique expression

\[
f_0u^2+f_1v^2+f_2uv+f_3w^2+f_4uw+f_5vw
+f_6uj+f_7vj+f_8wj. \tag{6}
\]

This basis uses uv=w^2+j^2. Its nine monomials are independent as
quartic polynomials in (a,b,c,d).

For a rank-one-convex F, the polynomial

\[
P_F(A,\eta,\xi)=\tfrac12D^2F(A)[\eta\otimes\xi,\eta\otimes\xi]
\]

is nonnegative everywhere. If it vanishes at (I,e1,e1), all of its first
derivatives in A,eta,xi vanish there. Exact linear elimination yields five
independent constraints:

\[
f_2=6f_0,\quad f_6=-4f_0,\quad f_4=f_5=f_8=0.
\]

The remaining coefficients give precisely (1), with

\[
\alpha=f_0,\quad k=f_3+4f_0,\quad
\ell=f_7+4f_0,\quad m=f_1-f_0.
\]

The verifier constructs the acoustic polynomial directly, regenerates the
linear system, proves its rank is five, and checks that the four displayed
generators span its full kernel.

## 4. Necessary weak inequalities at conformal backgrounds

H and its Hessian vanish at I. Write eta=(e,f), xi=(p,q), and
G=k w^2+ell vj+m v^2. Direct differentiation gives

\[
P_G(I,\eta,\xi)
=k f^2p^2+2ef(k+\ell)pq
 +[(k+L)e^2+3Lf^2]q^2. \tag{7}
\]

The determinant of the quadratic matrix in (p,q) is

\[
f^2[De^2+3kLf^2]. \tag{8}
\]

Thus rank-one convexity of any finite completion forces k>=0, L>=0,
D>=0. When k=0, (8) forces ell=0, and L>=0 then gives m>=0.
When k>0, these weak conditions make (7) nonnegative for all eta,xi.
Weak conformal positivity alone is nevertheless insufficient for a finite
H completion: both equality boundaries below are genuinely excluded.

Any rank-one-convex member also has alpha>=0, since F(e11)=alpha and the
restriction to the rank-one line t e11 is alpha t^4.

## 5. Excluded boundary L=0

Suppose k>0 and L=0. If ell!=0, set

\[
A_\varepsilon=\operatorname{diag}(1+\varepsilon,1-\varepsilon),
\qquad R=e_{22}.
\]

The exact acoustic value is

\[
\tfrac12D^2F(A_\varepsilon)[R,R]
=6\ell\varepsilon+(24\alpha-6\ell)\varepsilon^2. \tag{9}
\]

Choosing epsilon of the opposite sign to ell and sufficiently small gives
a negative value for every fixed finite alpha. If ell=0, then m=0 and
D=0, which is excluded by the next argument. Hence a nontrivial k>0
completion requires L>0.

This is an actual acoustic obstruction, not failure of a Gram ansatz or
heat monotonicity.

## 6. Excluded boundary D=0

Suppose k>0 and D=0, so m=ell(k+ell)/(2k). For real z put

\[
A_z=\begin{pmatrix}1&-z^2/2\\-z^2/2&1\end{pmatrix},
\qquad
R_z=\binom{1}{-z(k+\ell)}\otimes(1,zk).
\]

R_z is rank one for every z. The exact polynomial expansion is

\[
\tfrac12D^2F(A_z)[R_z,R_z]
=-2k^2z^3+O(z^4). \tag{10}
\]

The cubic coefficient is independent of alpha and ell. Since k>0, the
quantity is negative for all sufficiently small positive z, for every
fixed finite alpha. The verifier checks that the coefficients of z^0,
z^1,z^2 vanish identically and that the z^3 coefficient is exactly -2k^2.

For inspection, at A=I the same rank-one curve satisfies

\[
P_G(I,R_z)=3k\ell(k+\ell)^2(2k+\ell)z^4
\quad(D=0),
\]

while the coefficient of z in the A-gradient of its acoustic value is
(0,2k^2,2k^2,0). Moving the off-diagonal entries of A by -z^2/2 converts
this into the uncancellable negative cubic in (10). This is the missing
flatness condition that the weak conformal test does not see.

Together, Sections 4-6 prove all necessity in Theorem 2.

## 7. The controlled conformal quadratic form

Assume (3). For an arbitrary increment

\[
X=\begin{pmatrix}x&b\\c&d\end{pmatrix},\qquad
R=e_{11},\qquad Y=X-xR,
\]

the exact quadratic identity is

\[
\tfrac12D^2G(I)[X,X]-3\ell\det X
=Q(Y), \tag{11}
\]
\[
Q(Y)=(k+L)b^2+2(k+\ell)bc+kc^2+3Ld^2.
\]

The 2x2 (b,c) block has determinant D and trace tau=2k+L. It is positive
definite because k,D>0. Its smallest eigenvalue is at least D/tau:
if its eigenvalues are 0<lambda1<=lambda2, then
lambda1=D/lambda2>=D/(lambda1+lambda2).

The choice of kappa in Section 1 is positive and smaller than both
D/tau and 3L, since

\[
\kappa^{-1}=(3L)^{-1}+\tau/D.
\]

Consequently

\[
Q(Y)\ge\kappa |Y|^2. \tag{12}
\]

For compatible X=Dphi with zero trace,
integral det X=0. The determinant term in (11) therefore disappears after
integration. This is an ordinary quadratic minor identity; no determinant
square is included in the completion coefficient.

## 8. Cubic flatness forced by this contact

Let T be the symmetric four-linear polarization of G, so G(X)=T(X,X,X,X).
The coefficient sum of the expanded polynomial G is bounded in absolute
value by M=4(|k|+|ell|+|m|). Hence

\[
|T(X_1,X_2,X_3,X_4)|\le M\prod_i|X_i|. \tag{13}
\]

To justify this elementary tensor bound: the coefficient of a monomial
with exponent nu is split equally among its 4!/nu! ordered tensor
entries. The sum of the absolute values of all tensor entries is exactly
the sum of the absolute polynomial coefficients, and every coordinate is
bounded by its vector's Euclidean norm.

Put S(U,V,W)=T(I,U,V,W), and J0=sqrt(2)M. Then
|S(U,V,W)|<=J0|U||V||W|. Direct differentiation gives

\[
S(R,R,E)=0\quad\hbox{for every }E,\qquad R=e_{11}. \tag{14}
\]

This also follows from acoustic stationarity, because
D^3G(I)[R,R,E]=24 T(I,R,R,E). It is checked as an identity in every entry
of E. For X=xR+Y, (14) gives the two useful bounds

\[
|S(E,X,X)|\le3J_0|E||X||Y|,\qquad
|S(X,X,X)|\le4J_0|X||Y|^2. \tag{15}
\]

The second bound, with two factors from the controlled transverse
increment, is the feature that allows completion despite the acoustic
zero. A generic nonrank-one kernel in a polyconvex quadratic support does
not have this property; the inherited shear extremals have a different
cubic obstruction and need their separate argument.

## 9. Direct all-background completion

The proof is first for phi in C_c^infinity(R2;R2). Let X=Dphi. Decompose an
arbitrary affine B into its conformal and anticonformal parts. Left SO(2)
invariance lets us rotate its conformal part to sI, s>=0. Thus, after an
orthogonal target rotation, write

\[
B=sI+E,\qquad E\hbox{ anticonformal},\qquad
|\mathcal C B|^2=2|E|^2. \tag{16}
\]

No domain or gradient is changed except by the same orthogonal target
rotation. All norms, H, zero boundary values, and the integral contract
are preserved.

The exact quartic Taylor remainder is

\[
G(B+X)-G(B)-DG(B):X
=6T(B,B,X,X)+4T(B,X,X,X)+T(X,X,X,X).
\]

Use (11)-(15), remove the integral of 3ell s^2 det X, and apply Young's
inequality in the following explicit forms:

\[
36J_0s|E||X||Y|
\le\frac\kappa4s^2|Y|^2+
\frac{1296J_0^2}{\kappa}|E|^2|X|^2,
\]
\[
16J_0s|X||Y|^2
\le\frac\kappa4s^2|Y|^2+
\frac{256J_0^2}{\kappa}|X|^4,
\]
\[
4M|E||X|^3\le2M|E|^2|X|^2+2M|X|^4.
\]

The remaining quadratic E,E term is bounded below by
-6M|E|^2|X|^2, and the quartic term by -M|X|^4. Since J0^2=2M^2,
we obtain

\[
\int [G(B+X)-G(B)-DG(B):X]
\ge \frac\kappa2s^2\int|Y|^2
-A_0|E|^2\int|X|^2-B_0\int|X|^4, \tag{17}
\]
\[
A_0=2592M^2/\kappa+8M,\qquad
B_0=512M^2/\kappa+3M.
\]

For real vectors U,V in R2, the exact identity

\[
|U+V|^4-|U|^4-4|U|^2U\cdot V
-|U|^2|V|^2-\tfrac15|V|^4
=5(U\cdot V+\tfrac25|V|^2)^2
+(|U|^2|V|^2-(U\cdot V)^2)
\]

shows that the H Bregman gap is at least
|C B|^2|C X|^2+|C X|^4/5. For zero-trace compatible gradients,

\[
\int|\mathcal C X|^2=\int|X|^2,\qquad
\int|X|^4\le K_4\int|\mathcal C X|^4,\quad K_4=625/4. \tag{18}
\]

The L2 equality is |C X|^2=|X|^2-2det X followed by integration. For the
L4 inequality, write f=phi1+i phi2. Then
2 barpartial f=C Dphi and partial f=Beurling(barpartial f). The
complex-valued L4 bound ||Beurling||4<=sqrt(24), together with
|Dphi|^2=2(|partial f|^2+|barpartial f|^2), gives
||Dphi||4^2 <= (25/2)||C Dphi||4^2 and hence (18).

This nonsharp transform estimate was verified in the primary author PDF
of Bañuelos and Janakiraman, *Lp-bounds for the Beurling-Ahlfors transform*,
Theorem 1.1 (formula 1.4),
https://www.math.purdue.edu/~banuelos/Papers/Beur_Ahl.pdf .
Its bound at p=4 is sqrt(24). No contemporary sharp-norm claim is needed.

Combining (16)-(18), the integrated Taylor gap for G+alpha H is nonnegative
whenever

\[
2\alpha\ge A_0,\qquad \alpha/5\ge K_4 B_0.
\]

The choice alpha_*=A0/2+5K4 B0 simplifies exactly to (4). Affine linear
terms integrate to zero. This proves all-background quasiconvexity for
smooth compactly supported perturbations.

For a bounded Lipschitz Omega, extend a W_0^(1,4) perturbation by zero and
use strong C_c^infinity approximation. Quartic growth gives continuity of
the integral under this approximation. This yields the stated full
W_0^(1,4) contract, without assumptions on the size of B or Omega.

For periodic gradients, apply a smooth spatial cutoff to N-by-N copies
of the periodic perturbation. The interior contribution is N^2 times the
periodic integral; the boundary collar, of fixed width, has O(N) area and
bounded gradients. Dividing by N^2 and letting N tend to infinity proves
the same quartic elliptic estimate (18), and the determinant/linear
integrals vanish by periodicity. The same proof then establishes periodic
quasiconvexity. A torus transform norm is not silently substituted for the
whole-plane norm.

Finally the separate identity

\[
|U+V|^4-|U|^4-4|U|^2U\cdot V-\tfrac13|V|^4
=6(U\cdot V+\tfrac13|V|^2)^2
+2(|U|^2|V|^2-(U\cdot V)^2)
\]

and (18) show that adding nu H supplies the margin (5). This finishes
sufficiency and therefore Theorem 2.

### Complete acoustic contact set for the sufficient completions

The same estimate without the cubic and quartic Taylor terms also gives,
for any nonzero rank-one increment R and Y=R-R11 e11,

\[
\tfrac12D^2G(B)[R,R]
\ge\frac{3\kappa}{4}s^2|Y|^2
-[2592M^2/\kappa+6M]|E|^2|R|^2. \tag{18a}
\]

Here det R=0 removes the minor in (11), and the first Young inequality
uses only kappa/4 of the conformal quadratic lower bound. For rank-one R,
|C R|^2=|R|^2, so direct differentiation of H gives

\[
\tfrac12D^2H(B)[R,R]
=2|C B|^2|C R|^2+4(C B\cdot C R)^2
\ge2|E|^2|R|^2.
\]

(The last lower bound is deliberately weaker than the exact factor four.)
Thus the acoustic value of F is bounded below by

\[
\frac{3\kappa}{4}s^2|Y|^2+
[2\alpha-2592M^2/\kappa-6M]|E|^2|R|^2. \tag{18b}
\]

At alpha=alpha_* the bracket simplifies to
800000M^2/kappa+(9379/2)M>0. It remains positive for larger alpha.
If E!=0 there are no nonzero rank-one contacts. If E=0 and B!=0, then
s>0, and (18b) forces Y=0; conversely R proportional to e11 is indeed a
contact. Reversing the orthogonal target normalization gives exactly
(2a). This proves the global distinctness statement in Section 2.

The derivation of this stronger contact-set consequence was suggested by
the root's independent reading of the saved analytic proof and verified
here. It was not used to prove the projected equivalence.

## 10. An explicit nonpolyconvex completed quartic outside the old face

Take k=1, ell=-1, m=3/4. Then

\[
L=1/2,\quad D=3/2,\quad \kappa=3/7,\quad M=11,
\quad\alpha_*=1359900751/12.
\]

Thus the exact rational polynomial

\[
F=113325063 H+w^2-vj+\tfrac34v^2 \tag{19}
\]

is quasiconvex by the theorem and has a Jensen margin at least
(1/1125) integral |Dphi|^4, since its extra H coefficient is 5/12.
It has F(I)=-1/4, and its shear acoustic value is
D^2F(I)[e12,e12]=3>0. Hence it lies outside the inherited shear-contact
face while retaining D^2F(I)[e11,e11]=0.

Every finite-valued polyconvex homogeneous quartic on R^(2x2) is
nonnegative. Here is the proof, to make the use of F(I)<0 precise. Write
F(A)=g(A,det A) with g convex. The potential is finite everywhere: for
any (A,z), choose B with det B=z-det A; the point (A,z) is the midpoint
of (A+B,det(A+B)) and (A-B,det(A-B)), both points where g is finite.
Therefore g has a supporting affine plane at (0,0). Its pullback gives
F(A)>=p:A+lambda det A. Applying this to tA and taking both signs as
t->0 first forces p=0; then t->0 forces lambda det A<=0 for every A,
so lambda=0. Hence F(A)>=0. Equation (19), having F(I)<0, is not
polyconvex.

The large coefficient in (19) is a proof artifact, not a minimum or a
numerical performance assertion. The theorem, rather than this one
example, is the principal result.

## 11. Relation to known completion arguments and unfinished scope

A concurrent coordination message identified Iwaniec-Kristensen (2005),
and the primary publisher PDF was then independently acquired at
https://www.rivmat.unipr.it/fulltext/2005-4s/pdf/03.pdf and visually read at
printed pp.77-80. Theorem 3.1 requires globally uniform strict
Legendre-Hadamard positivity. A full-space input strictly
Legendre-Hadamard positive on the conformal plane can first be made
globally strict by adding enough H; its qualitative completion is thus
expected to follow from that theorem. No originality claim is made for
that strict-interior observation, and it is not a premise of this report.

Every completed polynomial (1) has the persistent acoustic zero
(I,e11). Adding further multiples of H leaves it zero. Thus the strict
ellipticity hypothesis does not apply to these polynomials. The new
argument uses the same classical Taylor/Young and elliptic absorption
framework, with the contact-specific cubic flatness (14). Its exact
projection excludes the two weak-positivity boundaries by (9)-(10).

The separate `GENERAL_FLAT_COMPLETION.md` records the root's subsequent
generalization of this cubic-flat argument to a sufficient full-space
compiler; this worker checked and completed that joint construction.
It is not presented as independent confirmation of a result supplied by
another worker. The present stratum classification and its precise
unfinished boundaries remain unchanged.

Remaining obligations are precise:

* Determine the least distortion coefficient in (1); this report supplies
  neither a sharp floor nor ROC=QC at that original coefficient.
* Classify contacts (I,e1 tensor (1,t)), t!=0, including any additional
  boundary kernel-flatness conditions. The exploratory script shows the
  stationarity span again has dimension four, but no theorem is asserted.
* Classify the rest of the eight-dimensional H-projection when conformal
  acoustic forms have several contacts or nonrank-one support kernels.
* Decide whether minor-square additions can repair more boundary strata;
  no such addition is required or classified here.
* Obtain independent external or formal proof review and historical
  comparison. Internal symbolic replay verifies identities, not the whole
  analytic proof or historical novelty.

## 12. Exact reproduction and cost

Run

```
R/.venv/bin/python R/workers/full_invariant_genesis/verify_theorem.py
```

with R replaced by the absolute research directory. The verifier uses
SymPy only. It regenerates the contact span, conformal acoustic identity,
both boundary obstructions, the controlled quadratic form, tensor
flatness, both Bregman identities, the C algebra, the completion constants,
and the rational example. It writes `EXACT_RECEIPT.json` in this directory.
No optimizer, pickle, source modification, network inference, or floating
eigenvalue check is involved.

For supplied rational (k,ell,m), admission and the coefficient (4) require
a fixed number of exact arithmetic operations and sign comparisons. The
scalar formulas and one 2x2 determinant suffice; no feasibility oracle is
hidden. Rational bit sizes remain O(n) for input bit size n because the
number and degrees of the arithmetic operations are fixed. This is the
cost of compiling a sufficient coefficient, not an algorithm for finding
the least coefficient or minimizing the variational energy.
