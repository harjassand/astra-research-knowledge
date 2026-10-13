# ASTRA META-GENESIS: quartic rank-one geometry and gradient moment completion

Research date: 14 October 2026 (Australia/Brisbane).

## Status and scope

This note contains a constructive proof for orthogonally invariant homogeneous quartics on R^(m x 2), a planar orientation-sensitive normal form with necessary coefficient bounds, an exact 8 x 8 acoustic Gram criterion, and an explicit rational strictly rank-one-convex non-polyconvex example. It also gives an exact dual formulation of the remaining rotation-invariant quartic Morrey question.

**The general planar Morrey problem is not solved. The rotation-invariant quartic problem is not solved. The quasiconvexity of the retained interior example is not established here. Historical novelty and independent proof validation are not established.** The sum-of-squares ingredient is an application of Calderon's existing binary biquadratic theorem, not a new SOS theorem. The duality ingredient is standard finite-dimensional semidefinite duality. The substantive candidate contributions are their explicit integration with the normal-form classification and boundary bounds below.

The accompanying verifier checks exact polynomial identities and rational positive definiteness. It does not formally verify all analytic arguments, establish priority, or turn numerical searches into theorems.

Astra repository revision consulted: `ace0cfc4437fe91c20ccd24d69e0ee4bb335e871`. Repository metadata and selected routes were consulted, not the complete archive. No unpublished Astra or OpenAI theorem is used as a premise in the proofs below. No repository write was performed.

## 1. The selected obstruction

For an integrand F on real m x n matrices, rank-one convexity means convexity of t -> F(A+t a b^T) for every A,a,b. For C^2 integrands this is equivalent to

    D^2 F(A)[a b^T, a b^T] >= 0.

Quasiconvexity requires

    integral_Omega F(A0 + D phi) >= |Omega| F(A0)

for every bounded Lipschitz domain and every Lipschitz zero-boundary perturbation phi. The latter tests compatible mixtures of gradients, not just a single rank-one line.

The decisive difficulty is the passage from positivity on rank-one directions to positivity for spatially compatible, multidirectional oscillations. The work below does not assume that passage.

Recent baseline: Bruno and Pasqualotto, arXiv:2608.06367v1, prove quasiconvexity throughout the rank-one-convex range of the Dacorogna-Marcellini family and for homogeneous quartics invariant under both left and right planar rotations. Their heat-flow/differential-form proof is credited prior work. This note instead studies left invariance, right-coordinate normal forms, and finite moment completion. Its six-dimensional reflection-invariant class is not a strict superset of the three-dimensional left-and-right SO(2)-invariant class: each imposes a different symmetry restriction.

## 2. Constructive classification with reflections

### Theorem 1

Let m >= 2 and let F:R^(m x 2)->R be a homogeneous quartic polynomial with

    F(U A) = F(A) for every U in O(m).

Then the following are equivalent:

1. F is rank-one convex.
2. F is quasiconvex.
3. F is polyconvex.
4. There exist a convex homogeneous quartic G and gamma >= 0 such that

    F(A) = G(A) + gamma det(A^T A).

Here

    det(A^T A) = sum_{1 <= i < j <= m} det(A_{ij})^2,

where A_{ij} is the two-row, two-column submatrix. Thus the correction is a nonnegative sum of squared minors, not a null Lagrangian itself.

No invariance under right rotations is assumed.

### Proof

Write A=(x|y), with x,y in R^m, and set

    u=|x|^2, v=|y|^2, w=x.y, Delta=uv-w^2.

An O(m)-invariant homogeneous quartic is of the form

    F = a u^2 + b v^2 + c uv + e w^2 + g uw + h vw.       (2.1)

For m=2 this follows by imposing the infinitesimal rotation equation and a reflection on all 35 quartic coefficients; the exact kernel dimensions are checked in the verifier. For arbitrary m, rotate the span of x,y into a fixed two-dimensional subspace. Its O(2)-invariant restriction has (2.1), and the same Gram variables describe every pair x,y, proving (2.1) in general.

#### Step 1: normalize the rank-one restriction

Fix a unit output vector e and define the binary quartic

    P(s,t)=F(e (s,t)).

Rank-one convexity of F implies ordinary convexity of P: every direction in this two-dimensional subspace is rank one. The quartic is nonnegative because it is convex, even and zero at the origin.

First suppose P is positive away from zero. A positive real binary quartic factors as a positive constant times the product of two positive-definite real quadratic forms. Indeed, its nonreal roots occur in conjugate pairs; each pair supplies a definite quadratic factor. Simultaneous diagonalization of the two positive-definite quadratic forms, followed by diagonal rescaling, yields an invertible real coordinate change and a positive rescaling for which

    P(s,t) = s^4 + 2 r s^2 t^2 + t^4,   r >= 1.        (2.2)

For completeness, after whitening one factor, let the other have positive eigenvalues alpha,beta. The final mixed coefficient is

    2 r = sqrt(alpha/beta) + sqrt(beta/alpha) >= 2.

Convexity evaluated at (s,t)=(1,1) in direction (1,-1) gives

    D^2 P(1,1)[(1,-1),(1,-1)] = 8(3-r) >= 0.

Hence 1 <= r <= 3. Right multiplication by an invertible matrix and positive scaling preserve rank-one convexity. They also preserve existence of the decomposition claimed in the theorem.

#### Step 2: recover the full reflection-invariant quartic

Two expressions of the form (2.1) with the same restriction to rank-one matrices differ by a multiple of uv-w^2: compare the coefficients of s^4,t^4,s^3t,st^3,s^2t^2. Therefore, in the normalized coordinates,

    F = u^2 + v^2 + 2r w^2 + lambda Delta.             (2.3)

Use two orthogonal output vectors e1,e2, the background

    A=e2 (1,-1),

and the rank-one direction

    B=e1 (1,1).

Direct differentiation gives

    D^2 F(A)[B,B] = 8(1+lambda-r).

Consequently

    lambda >= r-1.                                  (2.4)

#### Step 3: construct the convex part

Define

    H1 = u^2+v^2+2w^2 = tr((A^T A)^2),
    H3 = (u+v)^2+4w^2
       = (|x+y|^4+|x-y|^4)/2.

Both are convex. For H3 this follows directly from its last expression. For H1, with C=A^T A and a matrix direction B,

    D^2 H1(A)[B,B]
      = 2 ||A^T B+B^T A||_F^2 + 4 tr((A^T A)(B^T B)) >= 0.

The last trace is nonnegative because both matrices are positive semidefinite.

Now the exact identity

    F = ((3-r)/2) H1 + ((r-1)/2) H3
        + (lambda-r+1) Delta                         (2.5)

has only nonnegative coefficients. This proves the desired decomposition for positive P.

#### Step 4: include degenerate P

If a nonnegative convex homogeneous quartic P has a nonzero zero direction, its fourth root is a seminorm: this follows from convexity of its balanced unit sublevel set and homogeneity. Vanishing in one direction makes this seminorm invariant under translation along that direction. Thus, in suitable coordinates, P(s,t)=a s^4 with a>=0, including a=0.

Equation (2.1) then gives

    F=a u^2+lambda Delta.

Taking A=e2 (1,0) and B=e1 (0,1) shows lambda>=0. This already has the required form.

#### Step 5: undo the coordinates and infer quasiconvexity

If A is replaced by AS, then Delta(AS)=det(S)^2 Delta(A). Convexity and nonnegativity of the correction coefficient survive undoing S and the positive scaling.

The resulting decomposition is polyconvex because it is convex jointly in A and all its 2 x 2 minors. It also proves quasiconvexity directly: Jensen's inequality handles G, while the mean of each minor of A0+D phi equals that minor of A0. Jensen applied to the square of each minor handles the correction. The standard reverse implication from quasiconvexity to rank-one convexity completes the equivalences. QED.

### Interpretation

The entire reflection-invariant quartic sector cannot furnish a Morrey counterexample. This is a constructive classification, not a lower bound for a chosen computational representation. However, it is a symmetry-restricted theorem: no argument here reduces arbitrary integrands, or all 35 planar quartic coefficients, to this sector.

## 3. The remaining planar orientation-sensitive terms

Let A=[[a,b],[c,d]]. Set

    u=a^2+c^2, v=b^2+d^2, w=ab+cd, q=ad-bc,
    uv-w^2=q^2.

A homogeneous quartic invariant under left SO(2), but not necessarily reflections, has nine coefficients:

    F = Acoef*u^2 + Bcoef*v^2 + Ccoef*uv + Ecoef*w^2
        + Gcoef*uw + Hcoef*vw
        + q*(Lcoef*u+Mcoef*v+Ncoef*w).                 (3.1)

The last three terms change sign under an output reflection. They cannot be removed by averaging without potentially erasing the obstruction.

For positive rank-one restriction, the same binary factorization gives, up to an invertible right-coordinate change and positive scaling,

    F = u^2+v^2+2r w^2+lambda q^2
        +q*(ell*u+mu*v+nu*w),   1<=r<=3.             (3.2)

The reflection average remains rank-one convex. Hence

    D = 1+lambda-r >= 0,
    epsilon = 3-r >= 0.                              (3.3)

The two parameters measure different departures from the reflection-even boundary.

### Theorem 2: necessary two-slack bounds

For a rank-one-convex F in (3.2), let S=ell+mu. Then

    (|S|+|nu|)^2 <= 16(1+r) min(epsilon,D/3),         (3.4)
    (ell-mu)^2 <= 4 epsilon D.                        (3.5)

When epsilon,D>0, the stronger joint inequalities hold:

    (|S|+|nu|)^2/(1+r) + 4(ell-mu)^2/D
        <= 16 epsilon,                              (3.6)

    3(|S|+|nu|)^2/(1+r) + 4(ell-mu)^2/epsilon
        <= 16 D.                                    (3.7)

These are necessary, not asserted sufficient or sharp, conditions.

In particular, if r=3 or lambda=r-1, all three orientation-sensitive coefficients vanish. The resulting F is polyconvex by Theorem 1.

### Proof

By output rotation, rank-one convexity is equivalent to the nonnegativity, for every background (p,z) in R^2 x R^2 and every b=(s,t), of the Hessian in direction e1 b^T. For b=(1,1), diagonalize both background row blocks in the basis

    e+=(1,1)/sqrt(2), e-=(1,-1)/sqrt(2).

The first-row block has eigenvalues 12(1+r),4epsilon. The second-row block has eigenvalues 4(1+r),4D. Among the cross-block entries are

    coupling(p-,z+) = S+nu,
    coupling(p-,z-) = 2(mu-ell),
    coupling(p+,z-) = -3(S+nu).

For b=(1,-1), the small and large eigenvectors interchange, and the corresponding entries replace S+nu by S-nu, up to signs.

Positive semidefiniteness of the two relevant 3 x 3 principal blocks, followed by a Schur complement, yields (3.6) and (3.7). Taking the maximum between the plus and minus directions uses

    max{(S+nu)^2,(S-nu)^2}=(|S|+|nu|)^2.

The 2 x 2 principal minors give (3.4) and (3.5) directly, including the boundary. A zero diagonal entry of a positive semidefinite matrix forces its whole row and column to vanish; this also gives boundary rigidity without dividing by either slack. All displayed block identities are checked exactly in the verifier. QED.

### Degenerate rank-one restriction in the SO(2) class

There is no missing degenerate orientation-sensitive case. Put P=a s^4 in suitable coordinates. Formula (3.1) becomes

    F=a u^2+lambda q^2+q*(ell*u+mu*v+nu*w).

For b=e2 the acoustic matrix has zero diagonal entries whose rows force mu=nu=0. For b=e1 another zero diagonal entry forces ell=0. Finally lambda>=0. Thus this case is also polyconvex.

Any counterexample within the nine-dimensional SO(2)-invariant quartic class must therefore have a positive rank-one restriction, 1<=r<3, lambda>r-1, and nonzero orientation-sensitive terms satisfying the bounds above.

## 4. Exact acoustic certificates, without sampling directions

Use coefficient names A,B,C,E,G,H,L,M,N in (3.1), and let x=(a,b,c,d)^T. Define

    M11 = [[12A,3G,0,3L],
           [3G,2C+2E,-L,N],
           [0,-L,4A,G],
           [3L,N,G,2C]],

    M12 = [[3G,2C+2E,-L,N],
           [2C+2E,3H,-N,M],
           [-L,-N,G,E],
           [N,M,E,H]],

    M22 = [[2C+2E,3H,-N,M],
           [3H,12B,-3M,0],
           [-N,-3M,2C,H],
           [M,0,H,4B]].

Direct differentiation gives

    D^2 F(A)[e1 (s,t),e1 (s,t)]
      = x^T (s^2 M11+2st M12+t^2 M22) x.             (4.1)

### Theorem 3: exact 8 x 8 criterion

F in (3.1) is rank-one convex if and only if there is a real skew-symmetric 4 x 4 matrix K such that

    Q(F,K) = [[M11, M12+K],
              [M12-K, M22]] >= 0.                   (4.2)

There are six auxiliary real variables in K. This is an exact equivalence, not a finite angular discretization.

### Proof and attribution

Output rotation reduces every rank-one direction to (4.1). The latter is a biquadratic form in x in R^4 and (s,t) in R^2. Calderon's binary biquadratic sum-of-squares theorem says that its global nonnegativity is equivalent to a sum of squares of bilinear forms. A Gram matrix for the bilinear monomials (s x,t x) must have the fixed diagonal blocks in (4.2); its off-diagonal block can differ from M12 precisely by a skew matrix. Conversely any positive semidefinite matrix (4.2) is such a sum-of-squares certificate. QED.

This is an application of established SOS mathematics. Its contribution here is the explicit, complete acoustic interface for all nine coefficients.

A rational certificate K can be verified by exact rational matrix arithmetic. Existence of a real K does not assert that every boundary input has a rational certificate of small bit length. No general polynomial-bit acquisition guarantee is claimed.

## 5. A retained interior example with an exact rational certificate

Consider

    Fstar(A)=u^2+v^2+4w^2+(7/2)q^2-(29/10)q(u+v).   (5.1)

Its normalized parameters are r=2,lambda=7/2,ell=mu=-29/10,nu=0. Both slacks are strictly positive.

Choose

    K = [[0,1/2,17/10,0],
         [-1/2,0,0,17/10],
         [-17/10,0,0,23/10],
         [0,-17/10,-23/10,0]].

The resulting matrix Q in (4.2) is

    [[12,0,0,-87/10,0,17/2,23/5,0],
     [0,8,29/10,0,15/2,0,0,-6/5],
     [0,29/10,4,0,6/5,0,0,14/5],
     [-87/10,0,0,7,0,-23/5,-9/5,0],
     [0,15/2,6/5,0,8,0,0,-29/10],
     [17/2,0,0,-23/5,0,12,87/10,0],
     [23/5,0,0,-9/5,0,87/10,7,0],
     [0,-6/5,14/5,0,-29/10,0,0,4]].

Its leading principal minors are

    12,
    96,
    7077/25,
    1960329/10000,
    9141/250,
    22429/250,
    536679/25000,
    445394781/100000000.

All are strictly positive. The verifier also checks every leading principal minor of Q-(1/16)I is positive. Consequently

    D^2 Fstar(A)[a b^T,a b^T]
      >= (1/16)|A|^2 |a|^2 |b|^2.                    (5.2)

Thus rank-one convexity is proved globally by exact arithmetic, not inferred from the numerical search that produced the certificate.

### Non-polyconvexity

Let I be the identity and J=diag(1,-1). Then

    Fstar(I)=-3/10,    Fstar(J)=113/10.

Define a finite probability measure assigning mass 1/100 to each of +7I,-7I and mass 49/100 to each of +J,-J. It has mean matrix zero and mean determinant zero, but

    E Fstar = -833/250 < 0 = Fstar(0).

For any polyconvex representation Fstar(A)=g(A,det A), Jensen's inequality for convex g would give the opposite inequality. Hence Fstar is not polyconvex.

**This measure is not a constructed gradient field. The calculation does not disprove quasiconvexity.** Non-polyconvex rank-one-convex quartics already exist in the literature; no priority claim is made for that phenomenon or this particular example.

### Actual search evidence

A Fourier search tested Fstar directly, after its rank-one certificate was established. It used 12 initializations for each of two frequency cutoffs, 3 and 5; 1000 Adam steps per initialization; a 32 x 32 periodic grid; and backgrounds constrained to Euclidean norm at most 3. The periodic gradient was normalized to have mean fourth power of its Frobenius norm equal to one. The reported minimum Jensen gaps were approximately

    cutoff 3: 0.3350685422,
    cutoff 5: 0.2432525665.

No negative gap was found. These are floating-point local-search observations, not lower bounds over the search space and not quasiconvexity certificates. For these bandwidths, a quartic trigonometric polynomial has no spatial quadrature aliasing on the 32-point grid; floating-point and optimization limitations remain. Logs record the final evaluated iterate, immediately before its final optimizer update; the saved coefficient state is the subsequent update and need not reproduce the displayed last digits exactly.

Earlier, a generic 35-coefficient sampled acoustic LP produced an apparent negative-energy candidate which failed held-out rank-one tests. It was rejected. That experiment establishes no counterexample.

## 6. An exact moment-completion formulation of the surviving problem

Let f1,...,f9 denote the nine basis polynomials in (3.1). Write

    Q(p,K)=sum_i p_i B_i + sum_j k_j C_j,

where the matrices B_i and C_j are read explicitly from (4.2).

For a probability law mu on matrices with finite fourth moment and a prescribed comparison matrix A0, define its nine-component Jensen moment vector

    m_i = E_mu f_i(A) - f_i(A0).

### Theorem 4: finite moment-completion equivalence

The following are equivalent:

(a) E_mu F(A) >= F(A0) for every left-SO(2)-invariant rank-one-convex homogeneous quartic F.

(b) There exists a positive semidefinite real 8 x 8 matrix Y such that

    <B_i,Y>=m_i   for i=1,...,9,
    <C_j,Y>=0     for j=1,...,6.                     (6.1)

If Y is written in 4 x 4 blocks, the second line is precisely the symmetry of its off-diagonal block Y12.

### Proof

Theorem 3 identifies the rank-one-convex coefficient cone with the projection of Q(p,K)>=0. Condition (a) says that the conic optimization problem

    minimize m.p over Q(p,K)>=0

has finite minimum zero. It has a strictly feasible point: take F(A)=|A|^4, whose coefficient vector is (1,1,2,0,0,0,0,0,0), and take K12=1 with all other independent K entries zero. The resulting Q is positive definite, as verified exactly.

Finite-dimensional semidefinite strong duality therefore supplies an attained dual matrix Y>=0 with adjoint equations (6.1). Conversely, for any such Y and any feasible Q(p,K),

    m.p = <Y,Q(p,K)> >= 0,

which is (a). The off-diagonal symmetry follows by pairing Y with every skew K. QED.

### The strongest unresolved operation

For mu equal to the distribution of A0+D phi on a bounded domain, the unresolved statement is:

    curl compatibility of D phi forces a positive completion Y in (6.1).

A proof would settle Morrey's implication for the entire nine-dimensional left-SO(2)-invariant homogeneous quartic class, not merely for the reflection-even part. A compatible field for which (6.1) is impossible would, by separation, produce a genuine planar Morrey counterexample inside this class.

This is not claimed to solve the obstruction by renaming it. The concrete change is that one side of the problem now has an exact fixed-size positivity certificate, while all spatial difficulty is isolated in a nine-moment completion theorem. It remains unproved that gradient compatibility supplies the completion. The statement is a reduction, not a new universal algorithm for quasiconvexity.

The completion formulation does not require choosing a heat flow or restricting a differential-form corrector to a particular ansatz. It is the strongest retained alternative to the earlier pointwise heat-completion direction.

## 7. A distinct Fourier-resonance attack

There is a rigorous exclusion which can guide a counterexample search.

Let

    X(x)=sum_{j=1}^N R_j cos(k_j.x+theta_j),

where k_j are nonzero integer frequencies, R_j=a_j k_j^T are rank-one matrices, and the spatial average is over a torus. Suppose no signed sum of at most four frequencies vanishes except by cancelling equal opposite occurrences (choose the frequency list without duplicates modulo sign).

Then for every polynomial F of degree at most four and every A0,

    E_x F(A0+X(x))
      = E_{independent phases} F(A0+sum_j R_j cos U_j).

Proof: expand in Fourier characters. Each monomial of degree at most four has exactly the same surviving frequency terms under the stated no-resonance condition as under independent phase integration.

If F is rank-one convex, iterated Jensen over the independent phases then gives

    E_x F(A0+X(x)) >= F(A0).

Thus a quartic Fourier counterexample must use a nontrivial additive resonance of length at most four. This exclusion is a consequence of moment matching, not a claim that resonant fields fail Jensen. The existing literature proves additional low-wave exclusions; these must not be rediscovered and claimed as new. In particular, the 2020 numerical study by Guerra and Teixeira da Costa discusses known three-wave rigidity in the planar case.

For Fstar, the retained counterexample attack is therefore certified positivity plus deliberately resonant gradient fields, not arbitrary probability measures with matching mean minors. The 24 local searches above did not close this attack.

### Exact acquisition of the nine Fourier moments

The included `exact_fourier_moments.py` evaluates the nine Jensen moments for any rational background and rational finite Fourier potential

    phi(x)=sum_j [c_j cos(k_j.x)+s_j sin(k_j.x)], k_j in Z^2.

It forms the Fourier coefficients of the four gradient entries, then of the quadratic invariants u,v,w,q. Each invariant has at most O(M^2) pair-frequency terms for M waves. The nine quartic means are zero-frequency inner products of these quadratic coefficient dictionaries. Thus all nine moments require O(M^2) exact rational arithmetic operations, up to fixed constants and dictionary costs; the bit costs of rational arithmetic and integer frequency manipulation remain charged. There is no grid whose size grows with the numerical magnitude of the frequencies.

Four exact identities were executed, including a wave of frequency 10^12 with inverse-frequency potential amplitude. This is an implemented moment-acquisition operation, not an assumed integration oracle. It does not acquire the unknown positive completion Y or prove that such a completion always exists.

For rational quartic coefficients, a rational positive acoustic Gram certificate, and a rational Fourier potential with a negative exactly computed Jensen gap, all parts of a counterexample would be directly checkable. A negative periodic gap would imply failure of the zero-boundary quasiconvexity test by tiling many periods and cutting off the bounded periodic potential near the outer boundary; the boundary error is lower order in the number of periods. No such negative compatible field was produced here.

## 8. Discovery-method conclusions supported by the mathematics

First, restriction to the rank-one cone gives a binary quartic whose factorization determines a useful coordinate system. This is a constructive representation change: it yields the interval 1<=r<=3 and the convex decomposition, not just a new notation.

Second, zero eigenvalues of the even acoustic blocks force all orientation couplings to vanish on two boundary regimes. The quantitative inequalities identify how much interior slack is needed before an orientation-sensitive obstruction can exist. Searching those excluded boundaries for a counterexample would be mathematically futile.

Third, an exact acoustic certificate distinguishes a valid interior challenge from a sampled-positivity artifact. The rejected LP candidate and the exact certificate for Fstar demonstrate this distinction in the actual computation.

Fourth, the exact moment dual exposes what is still missing: a positive completion produced by gradient compatibility. Neither a new name for this condition, a restricted heat certificate, nor failure to find a counterexample proves that completion theorem.

These observations support a bounded structural advance. They do not establish a general discovery methodology that produces exceptional breakthroughs, and the requested exceptional theorem remains unproved in this investigation.

## References and provenance

1. G. Bruno and F. Pasqualotto, *Quasiconvexity for the Dacorogna-Marcellini Energy*, arXiv:2608.06367v1 (2026). Baseline result and prior heat-form method. Not a premise of Theorem 1 or the certificate for Fstar.
2. A. P. Calderon, *A note on biquadratic forms*, Linear Algebra and its Applications 7 (1973), 175-177. Binary biquadratic SOS theorem imported in Theorem 3. The modern research manuscript *The SOS Rank of Biquadratic Forms*, arXiv:2507.16399, was consulted for its statement and attribution.
3. A. Guerra and R. Teixeira da Costa, *Numerical evidence towards a positive answer to Morrey's problem*, arXiv:2006.09063. Low-wave prior art and numerical pitfalls.
4. L. Bandeira and P. Pedregal, *Quasiconvexity: the quadratic case revisited, and some consequences for fourth-degree polynomials* (2011). The abstract was consulted; its complete quartic results were not audited. Priority relative to that work remains unresolved.
5. P. Bizeul, B. Klartag and J. Lehec, *Presenting a proof of the Kannan-Lovasz-Simonovits conjecture*, arXiv:2610.05474 (4 October 2026). Used for frontier selection, not as a theorem premise.
6. L. Guth, *The Kakeya conjecture, after Wang and Zahl*, arXiv:2604.03416 (2026). Used for frontier comparison, not as a theorem premise.

No source manuscripts are redistributed in this package.
