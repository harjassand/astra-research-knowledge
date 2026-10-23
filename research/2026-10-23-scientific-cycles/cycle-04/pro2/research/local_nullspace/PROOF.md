# Local nullspaces, signed scalar recovery, and four queries on squared paths

Contributor: /root/local_nullspace. 22 October 2026 Australia/Brisbane.
This is a bounded representation/lemma contribution to the owner's degree-four
question. It does not establish a design for every partial 2-tree.

## 1. General exact reduction for maximum degree four

Let G have maximum degree at most four. Write N[i] for the closed neighborhood
and let M_i be the matrix whose rows are x_j, j in N[i]. Assume rank(M_i) is
min(|N[i]|,4), with every positive singular value at least eta>0. Let H consist
of the degree-four vertices. At i in H choose a unit vector k_i spanning
ker(M_i^T); extend it by zero outside N[i].

For a supported symmetric D, decompose its i-th supported coefficient row as

    D_i = t_i k_i + R_i       (i in H),
    D_i = R_i                 (i outside H),

where R_i is orthogonal to k_i. The row action determines R_i, and

    ||R||F <= ||DX||F/eta,
    ||D||F^2 = ||t||2^2 + ||R||F^2.                    (1)

For every unordered edge meeting H, define the scalar edge operator

    (Q t)_{ij} = k_i(j)t_i - k_j(i)t_j,               (2)

taking the missing term as zero at vertices outside H. Symmetry gives
(Qt)_{ij}=R_{ji}-R_{ij}; therefore

    ||Qt||2 <= sqrt(2)||R||F.                         (3)

If Q^TQ >= sigma^2 I, then

    ||D||F <= eta^(-1) sqrt(1+2/sigma^2) ||DX||F.     (4)

This is an exact equivalence representation, with a sufficient coercivity
condition; it does not assert that local rank alone bounds sigma.

For the operator-output contract a weaker scalar condition is enough. If
||t||infty<=gamma||Qt||2, symmetry and degree four give

    ||D||2 <= max_i sum_j |D_ij|
            <= sqrt(5) max_i ||D_i||2
            <= sqrt(5)/eta sqrt(1+2gamma^2)||DX||F.   (5)

All diagonals are included in these row decompositions. They are free, not
deleted from the model. General k_i may have nonzero diagonal coefficients.
Either inverse estimate yields a stable mathematical decoder by constrained
least squares over S_G: its fitted action is the orthogonal projection of Y
onto the action range, so the fitted action error relative to DX has norm at
most ||E||F. Applying the inverse estimate gives the same output constant.
This observation supplies existence, not a uniformly efficient solver for a
general scalar system. Section2 gives a more explicit decoder for (4).

## 2. A concrete decoder for the Frobenius criterion

Given arbitrary noisy Y, compute each minimum-norm supported row R0_i solving
the local least-squares action equation. For true D, these rows equal R_i plus
an error Delta_i orthogonal to k_i, with ||Delta||F<=||E||F/eta. Form
b_ij=R0_ji-R0_ij and solve min_t ||Qt-b||2. For the true t, the difference
b-Qt has norm at most sqrt(2)||Delta||F. Hence the fitted t differs by at most
sqrt(2)||Delta||F/sigma. Assemble R0+t_i k_i and project orthogonally to the
supported symmetric matrices. Row orthogonality and this projection show

    ||Dhat-D||F <= eta^(-1)sqrt(1+2/sigma^2)||E||F.   (6)

The action is four columns throughout. Q has O(n) nonzeros at bounded degree.
No fast solver for an arbitrary ill-conditioned Q is presumed. In the
squared-path design below Q^TQ is uniformly conditioned and pentadiagonal.

A computed scalar fit with normal-equation residual r introduces additional
coefficient error <=||r||2/sigma^2. All local arithmetic/query perturbation
errors must also be counted in an implementation; an unverified floating
success status is not substituted for these error bounds.

## 3. Useful scalar certificates, and their limitations

If all nonzero offdiagonal entries of each local k_i have one common magnitude
c_i, put a_i=c_i t_i. The edge equations become unit signed differences
s_ij a_i-s_ji a_j, or anchors +/-a_i when only one endpoint is active. The
normal matrix is the signed graph Laplacian with the missing active edges
counted as grounded boundary edges. Ordinary Cheeger estimates apply only
after this unit-gain reduction; unequal endpoint magnitudes can invalidate
an unweighted expansion argument.

More generally, suppose all active gains have magnitude at least kappa>0,
and every vertex has a walk of length <=L to an anchor, or a closed walk of
length <=L whose gain product rho satisfies |1-rho|>=zeta>0. Transferring
the scalar equations around the walk gives

    ||t||infty <= L kappa^(-L)/min(1,zeta) ||Qt||2.    (7)

Repeated edges are allowed in this deliberately conservative bound. Thus
(5) is uniform. A finite palette makes kappa and every nonzero fixed-size
holonomy gap uniformly positive, but does not establish that such local
certificates cover the graph. Long balanced scalar paths remain a real
obstruction to this criterion. Expansion can furnish other certificates.

## 4. Explicit four-query squared-path design

Let G=P_n^2, indexed 0,...,n-1, with edges at distances one and two. Set

    c_i = i mod 3,
    s_i = (-1)^floor(i/3),
    x_i = (e_(c_i), s_i)/sqrt(2).                    (8)

This is a six-row finite palette. Every query row has total norm exactly one.
Let H={2,...,n-3}; when n<=4 it is empty. At i in H, define

    b_i = -s_(i-2)s_(i-1),  with period (-1,+1,-1),
    k_i(i-2),k_i(i-1),k_i(i),k_i(i+1),k_i(i+2)
             = (1,b_i,0,-1,-b_i)/2.                (9)

Direct substitution gives M_i^T k_i=0 and ||k_i||2=1. The four offdiagonal
kernel entries have equal magnitude, and the diagonal coefficient is zero.
The diagonal remains freely unknown and is recovered from its own color.

The positive local singular values are found from matrices of order at most
four. For two/three-row neighborhoods the least squared value is >=1/2;
for the four-row boundary neighborhoods it is (5-sqrt(17))/4; for five-row
interior neighborhoods it is (3-sqrt(5))/2. A singleton has squared value1.
Thus, uniformly in n,

    eta^2 = (5-sqrt(17))/4.                         (10)

This can be checked algebraically using unscaled Z_i=(e_(c_i),s_i). The
four-row Gram characteristic polynomial is

    (lambda-2)(lambda-1)(lambda^2-5lambda+2),

and the positive interior Gram polynomial is

    (lambda-2)^2(lambda^2-6lambda+4).

## 5. Signed frustration yields an exact sum of squares

For edge ij in H let g_ij be the product of the signs k_i(j) and k_j(i).
For adjacent indices, g_(i,i+1)=-b_(i+1). For distance two,
g_(i,i+2)=-b_i. Consequently every consecutive triangle has gain product -1.

Choose a diagonal sign gauge u_i with u_(i+1)=g_(i,i+1)u_i and write t_i=u_i z_i.
All distance-one gains become +1, and all distance-two gains become -1. Every
i in H has four active incident entries of magnitude1/2; edges to vertices
outside H are genuine anchors in Q. Hence

    ||Qt||2^2
       = sum_i z_i^2 - (1/2)sum_i z_i z_(i+1)
                        + (1/2)sum_i z_i z_(i+2).  (11)

Extend z by zero to all integers. Expanding the following expression gives
exactly (11), including endpoints:

    ||Qt||2^2
       = (1/4) sum_(i in Z) (z_(i-1)+z_(i+1)-z_i/2)^2
           + (7/16)sum_i z_i^2.                   (12)

Thus sigma^2>=7/16. Also ||Q||2^2<=2 by the unit local kernel normalization,
so the scalar normal system has condition number at most32/7. This proof
includes |H|=1,2; empty H needs no scalar solve.

Substitution into (6) gives the explicit uniform guarantee

    ||Dhat-D||2 <= ||Dhat-D||F
       <= sqrt[(39/14)(5+sqrt(17))] ||E||F
       < sqrt(26)||E||F.                          (13)

It applies to every real supported symmetric D and arbitrary correlated E.
There are exactly four actions, a fixed six-row seed, O(n) preparation and
O(n) arithmetic operations in the pentadiagonal solve and decoding. Exact
rational intermediates can have growing bit length; O(n) here is arithmetic
count, not a uniform bit-cost claim. A certified floating solve needs explicit
residual and input-rounding allowances.

Together with the accepted all-design three-query lower theorem on P_(8m)^2,
this makes four the sharp uniform stable query count on squared paths. This
is an actual receiving use of an owned lower-bound family. It does not solve
the owner's whole TW<=2, Delta<=4 question, nor improve the original NIST
benchmark. Historical originality is not established by this local note.

The construction immediately covers every support with a supplied bandwidth-
two ordering: embed it in P_n^2, apply the same decoder, then set every
forbidden coefficient to zero. Since the true matrix has zero there, this
last orthogonal projection can only reduce Frobenius error. Finding such an
ordering, if it is not supplied, is a separate graph-preparation problem.
The q3 lower family belongs to this class, so its uniform stable minimum is
also exactly four. Thus the operation has a reusable support hypothesis.

## 6. A finite-palette warning

For x_i=(e_(c_i),s_i)/sqrt2 under a proper three-coloring, a degree-four row
with neighbor-color counts(2,2) and opposite signs within each pair has the
four-active-entry kernel used above. Counts(3,1) can instead give a two-entry
duplicate-row kernel. Counts(4,0) force local rank below four. Equal signs
within a two-neighbor group can also create local ambiguity at degree<=3.
Those cases cannot be discarded in a claimed universal graph construction.
The graph K_2 joined to an independent set of three vertices has TW2 and
Delta4, but every proper three-coloring has a(3,1) high-degree neighborhood;
it refutes the claim that every admitted graph has the balanced(2,2) pattern.

The main owner must separately establish a global design theorem or a valid
structural covering/expansion argument for the remaining graph class.
