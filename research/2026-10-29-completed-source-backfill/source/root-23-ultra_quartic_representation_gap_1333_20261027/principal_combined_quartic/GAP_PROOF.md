# A planar homogeneous quartic that is polyconvex but not SOS polyconvex

Internally constructed and independently checked,2026-10-27. This answers
the mathematical case expressly left open in Remark2.1 of the primary v1
below, at the definitions in that paper. World priority is not established;
no full Morrey theorem or physical capability is asserted.

For A=[[a,b],[c,d]], put

    u=a²+c², v=b²+d², w=ab+cd, q=ad-bc,
    F=u²+v²+3w²+(113/10)q²+4q(u-v).                       (1)

Theorem. F is strictly polyconvex in the quantitative support sense below,
and is not SOS polyconvex, even allowing polynomial minor selectors of
arbitrary finite degree. These two properties persist for every homogeneous
quartic whose35 ordinary monomial coefficients differ from F's by at most
1/616000 in sup norm. The perturbed quartics need no rotational symmetry.

The primary comparison is Fantuzzi, Henrion, Kružík, Murali, Weis,
*Polyconvexity with Moments and Sums of Squares*,2604.11124v1,
Definition2.5 and Remark2.1:
https://arxiv.org/html/2604.11124v1 . Its SOS condition uses a polynomial map
of supporting minor coefficients and a jointly SOS residual. It differs
from requiring a convex polynomial lift; the latter gap was already known.
Our theorem concerns the former, stronger open-case distinction. The current
arXiv record and bounded targeted primary-author searches were checked;
those checks are not an exhaustive historical novelty proof.

## 1. The exact positive support

Use row-major A=(A0,...,A3),X=(X0,...,X3), and define

    kappa(A)=(14611/2500)(u-v)+(110757/5000)q,
    P(A,X)=F(A+X)-F(A)-DF(A):X-kappa(A)detX.

The peer acquired the rational matrix R in
../quartic_alternative/sector_gap/EXACT_MULTIPLIER_SUPPORT.json such that

    |X|² P(A,X)=Z60(A,X)^T R Z60(A,X),
    R-(1/200)I is positive definite.                       (2)

Z60 consists of all40 A_i X_j X_k, j<=k, followed by all20
X_i X_j X_k, i<=j<=k. All658 polynomial coefficient equations hold exactly;
all60 exact LDL pivots of the shifted matrix are strictly positive.
Root's verify_gap.py independently rebuilds the literal(1), its derivative,
the multiplier, all features and every coefficient using stdlib rational
polynomial dictionaries. It imports no producer, optimizer, numerical array
or symbolic algebra. It separately recomputes/reconstructs the full LDL.
The positive certificate SHA256 is
a7b53759b9ba5576a099ef36b9ffce96c266478a5fbc5594a8b156d5f1576e32.

The squared feature norm satisfies

    |Z60|²=|A|² sum_(j<=k)X_j²X_k²
                  +sum_(i<=j<=k)X_i²X_j²X_k²
           >= |A|²|X|⁴/2+|X|⁶/6.

For X!=0 divide(2) by |X|²; at X=0 use continuity. Consequently

    P(A,X)>=|A|²|X|²/400+|X|⁴/1200.                      (3)

This division supplies a globally positive polynomial support. It does not
make P itself SOS; the next part proves that no polynomial selector can do
so. Multiplying by the harmless positive denominator changes the certificate
class, rather than changing F or its mathematical definition.

To obtain a finite-valued convex lift, for every A define

    ell_A(B,t)=F(A)+(DF(A)-kappa(A)cofA):(B-A)
                         +kappa(A)(t-detA).

The determinant expansion and(3) give ell_A(B,detB)<=F(B), with equality
when A=B. Thus G(B,t)=sup_A ell_A(B,t) is convex and equals F on the minor
graph. It is finite everywhere: choose Y with detY=t-detB. Then (B,t) is
the average of (B+Y,det(B+Y)) and (B-Y,det(B-Y)). Every ell_A there is bounded
above by [F(B+Y)+F(B-Y)]/2, while any one ell_A gives a finite lower bound.
Therefore F is polyconvex in the usual global sense.

For every constant A and periodic W1,4 potential phi, or phi in W1,4_0 on
a bounded Lipschitz planar domain, integrating(3) cancels the gradient mean
and determinant mean. This proves the quantitative quasiconvex bound

    integral[F(A+Dphi)-F(A)]
      >= |A|²/400 integral|Dphi|² +1/1200 integral|Dphi|⁴.  (4)

The null-Lagrangian identities first hold for smooth potentials and pass
by strong W1,4 approximation. No finite bandwidth or small-amplitude premise
is used.

## 2. Every polynomial SOS selector reduces to26 features

For any homogeneous planar quartic H, suppose a polynomial minor map s(A)
makes H(B)-H(A)-s(A).(p(B)-p(A)) jointly SOS, where p lists entries and det.
At B=A this nonnegative differentiable polynomial vanishes, so its derivative
in B vanishes. If k(A) is s's determinant component, the entry components
must be DH(A)-k(A)cofA. Substituting B=A+X gives exactly

    H(A+X)-H(A)-DH(A):X-k(A)detX.                          (5)

In particular k is polynomial. Write its homogeneous components k_j and
replace(A,X) by(tA,tX), t>0. The H Bregman part has degree4, while
the k_j term scales as t^(j+2). If the largest nonzero j>2, choose A with
k_j(A)!=0 and the sign of detX so that its leading term is negative as
t tends to infinity. If the smallest j<2, make the same choice as t tends
to zero. Both contradict nonnegativity. Hence k is homogeneous quadratic
(including the zero polynomial). This proves all-degree completeness,
without restricting k to a guessed symmetry class.

Now(5) is a homogeneous quartic. In any SOS representation all squared
polynomials can be chosen homogeneous quadratic: highest-degree squares
cannot cancel, and the lowest-degree nonzero homogeneous squares cannot
cancel either. Because(5) vanishes at X=0 for every A, each quadratic square
vanishes there and contains no pure A_i A_j terms. Thus all squares use
exactly the26-feature span

    Z26=(A_i X_j : i,j=0,...,3; X_i X_j : i<=j).

This is a necessary form for every polynomial SOS minor selector of ANY
degree, not merely a fixed-degree relaxation.

## 3. An exact separating functional

EXACT_SUPPORT_SEPARATOR.json contains a rational linear functional L on
the215 monomials in the Z26 Gram products. Its independently checked facts
are

    L(A_i A_j detX)=0 for ALL ten pairs i<=j,
    L(F(A+X)-F(A)-DF(A):X)=-39/125000,
    M=[L(Z26_i Z26_j)] is positive definite.               (6)

The negative certificate SHA256 is
768f5564a0e9ed66524d3d908626ec4f52f4a24634c4eb3daf50034314d32c19.
Root acquired this dual independently of the positive60-feature construction.
The stdlib verify_dual.py and verify_gap.py rebuild its literal target,
all ten annihilators and all26 LDL pivots. The original numerical dual only
imposed two annihilators; all ten vanish EXACTLY in the reconstructed result.
No symmetry averaging is needed for the theorem.

For a hypothetical SOS(5), Section2 gives a quadratic k and a PSD Gram Q.
Equation(6) makes the left pairing -39/125000, whereas its right pairing
tr(QM)>=0. This contradiction proves F is not SOS polyconvex under the
primary Definition2.5, regardless of selector degree.

## 4. A full35-dimensional open separation

Order the35 degree-four ordinary monomials in the four entries of A in
any fixed way, and perturb every coefficient by at most epsilon. A monomial's
Bregman polynomial has coefficient l1 norm at most16-1-4=11. Multiplying
by |X|² increases that norm by at most4. Thus the weighted Bregman change
has coefficient l1 norm at most1540 epsilon.

Every monomial of bidegree(A²,X⁴),(A,X⁵), or degreeX⁶ is a product of two
Z60 features. Assign each perturbation coefficient to one such Gram entry
(half to each symmetric off-diagonal entry). This constructs a symmetric
Gram perturbation DeltaR with entry l1 norm, hence operator norm, at most
1540 epsilon. For epsilon<=1/616000, R+DeltaR>=I/400. Keep the SAME kappa.
The global support proof above still works, so all these quartics remain PC.

For the negative side, the exact sum of the absolute L pairings of the35
unweighted monomial Bregmans is69749/25000. Therefore the perturbed pairing
is at most

    -39/125000 + epsilon*(69749/25000) <0

throughout the stated closed coefficient box. All ten selector annihilators
and the positive moment matrix are fixed, so Section3 still excludes every
polynomial SOS selector. Strictness at both ends supplies an open neighborhood
containing this closed box. This makes the separation stable under arbitrary
small homogeneous perturbations, including loss of the original symmetries.

## Scope and research consequence

This is a completed internally checked mathematical representation separation,
with positive global PC/QC construction and exact all-degree SOS impossibility.
The 658/215 finite polynomial checks support the explicit certificates;
Sections1--4 supply their analytic quantifiers and consequences. The result
does not establish efficient general polyconvexity decisions, general support
hierarchy completeness, a rank-one-convex/non-QC example, or the full planar
Morrey implication. The direct matrix-pair search and combined heat attempt
are retained failures; neither is used as a proof.

The next meaningful question is how to acquire positive supports beyond the
unmultiplied class efficiently and how far that reaches into the unresolved
quasiconvex cone. Raising the degree of the polynomial selector alone cannot
repair this counterexample. A norm multiplier succeeds already at degree2.
This is scientific progress at its stated mathematical scope; a100/100
civilisation-changing capability remains NOT_ACHIEVED.
