# Higher-rank stationary compiler: acquisition, deformation audit, and a sharp computational boundary

Let A=F_q[t]/(t^e), q=2^d, let b>=5 be odd, and put m=b-1. Thus m is even.
Write lambda_e=Tr[t^(e-1)]. Let H be an ordinary homogeneous cubic in b
ring variables. Its residue alternating third form is assumed to pass the
following acquired certificate:

    T_0=ell wedge omega,

where omega is nondegenerate on W=ker ell. No restriction is placed on
higher nilpotent cubic coefficients. A binary quadratic weight Q may use
the quotient A/t^h, with 3h<=e+1. The root compiler handles raw coefficient
acquisition; this note independently audits the geometry and counting step.

## 1. The linear factor is acquired by a polynomial-size linear system

Compute the kernel of the map

    V* -> exterior^4 V*,     alpha -> alpha wedge T_0.

If T_0=ell wedge omega as above, its kernel is exactly the line F_q ell.
Indeed write alpha=a ell+beta with beta in W*. Then alpha wedge T_0=0
if and only if beta wedge omega=0. For a symplectic space W of dimension
at least four, beta->beta wedge omega is injective. A symplectic basis
sends a nonzero beta to its first basis covector, whose product with the
second symplectic pair is nonzero. This argument is valid in
characteristic two and does not divide by factorials.

The system has b unknown field coordinates and binomial(b,4) equations.
After acquiring ell, select v with ell(v)=1, construct a basis of W, and
recover omega(u,w)=T_0(v,u,w). Verify its rank m. In this basis,
ell wedge T_0=0 already implies T_0=ell wedge omega; a coefficient check
is also cheap. A Darboux basis follows by ordinary alternating elimination.
All operations are polynomial in b and d, so fixed b is unnecessary for
this geometry acquisition.

## 2. Higher nilpotent deformations retain the full chain centroid

First consider T_0 over its residue field. Its radical is zero: contraction
by a vector a v+w has components a omega and ell wedge contraction_w omega,
which vanish only when a=w=0. Its centroid is the scalar field. Writing a
centroid map as E(v)=a v+u and E(w)=l(w)v+B w, balancing repeated v slots
forces u=0. Balancing three W slots forces l=0. Balancing (v,w,w') then
gives omega(Bw,w')=a omega(w,w'), hence B=aI.

Now let T_A be any A-valued alternating lift of T_0, including arbitrary
nilpotent perturbations. The binary scalar form lambda_e(T_A) is
radical-free. For a nonzero input of lowest t-valuation j, choose two
residue inputs detecting its nonzero residue contraction, and multiply one
by t^(e-1-j) and a suitable field scalar. The top trace is nonzero.

The centroid of any radical-free trilinear form is commutative: for two
balanced maps E,F, moving them through all three slots gives

    T(EF x,y,z)=T(Fx,Ey,z)=T(x,Ey,Fz)
              =T(Ex,y,Fz)=T(FE x,y,z).

Multiplication by A lies in this centroid, so every binary centroid map
commutes with A and is A-linear. Scalar balancing then implies A-valued
balancing: multiply the third slot by every a in A and use the
nondegeneracy of lambda_e(ab). Reduction modulo t is scalar by the
preceding residue argument. Subtract that scalar and write E=tE_1.
Balancing E implies that E_1 is a centroid map for the form truncated at
depth e-1. Induction shows E_1 is scalar modulo t^(e-1). Hence E is
multiplication by a single ring element. The full binary centroid is
exactly A, even after arbitrary nilpotent cubic deformations.

## 3. Infinity certification, including a small strengthening

In coordinates (x,z) with z=ell, write

    H_0(x,z)=G_3(x)+z Q_2(x)+z^2 L_1(x)+c z^3.

The third form of G_3 vanishes, so G_3 is a sum of x_i^2 x_j monomials.
Its gradient is M x^[2]. The polar matrix of Q_2 is the symplectic matrix
Omega. Thus

    grad_x H_0(x,1)=M x^[2]+Omega x+c_0,
    grad_x H_0(x,0)=M x^[2],
    partial_z H_0(x,0)=Q_2(x).

An invertible M certifies that there are no projective critical points at
z=0. This sufficient certificate has a complete inexpensive refinement:
let K be the field subspace obtained by taking coordinatewise square roots
of ker M. There are no geometric critical points at infinity exactly when
either dim K=0, or dim K=1 and Q_2 is nonzero on a generator of K. If
dim K>=2, every homogeneous quadratic on K has a nonzero zero over the
algebraic closure. The strengthened test avoids rejecting the corank-one
case unnecessarily.

The infinity gate cannot be omitted. For b=5 over F_2, take

    H=Z^3+Z(X_1Y_1+X_2Y_2).

Its residue third form has the required radical-free factorization, but
M=0. At depth e=2 its exact signed count is320, while an origin-only
calculation gives32. The ten residue critical vectors are Z=0 and
X_1Y_1+X_2Y_2=0. The complete ten-bit counterexample is saved in
`higher_rank_boundary_results.json`.

## 4. Residue roots and higher deformations

The chart gradient is an affine binary-linear system on md bits. Its
ordinary Jacobian is the constant matrix Omega, so its geometric fibers
are zero-dimensional and simple. Bezout bounds a fiber by2^m points.
If its computed binary kernel has dimension k, then k<=m and there are
exactly2^k candidate affine solutions when the system is consistent.
Enumerate these candidates, filter H_0(x,1)=0, and charge2^k explicitly.
No scan through q^m points is needed.

Each surviving residue point has a unique full critical lift for the
dehomogenized H. At stage j>=1, changing the approximation by t^j delta
changes its gradient at coefficient j by Omega delta. Thus invert Omega
once and correct one field layer at a time, verifying the final gradient.

Higher nilpotent terms generally make the full ring gradient nonlinear
over F_2. For example, t X_1Y_1X_2 contributes t Y_1X_2 to one derivative.
Its additivity discrepancy at Y_1=1 and X_2=1 is t. A binary linear solve
on the full ring gradient would therefore be invalid. Only the residue
solve is binary-linear; the later Hensel corrections use its invertible
Jacobian. This failure is explicitly executed in the saved check program.

## 5. Exact Gaussian factor in any even transverse dimension

Fix one critical ray with lifted chart point a, critical value C=H(a,1),
and a unit radial parameter r. Let B_a(u) be the ordinary homogeneous
quadratic Taylor term of the residue chart polynomial at a_0. Its polar
matrix is Omega, so

    sum_(u in F_q^m) (-1)^Tr(B_a(u)) = kappa q^(m/2),

where kappa is +1 or -1, obtained by exact binary Gaussian elimination.
For every nonzero gamma in F_q, multiplication of u by sqrt(gamma) gives

    sum_u (-1)^Tr(gamma B_a(u)) = sum_u (-1)^Tr(B_a(u)).

This supplies the needed scale invariance in characteristic two without
using an odd-characteristic diagonal-square Morse lemma.

For e=2s, sum the last s digits of every transverse coordinate. They force
the first s digits to the unique critical lift and give factor q^(ms).
For e=2s+1>=3, sum the last s digits first, then the middle field digit.
The latter contributes kappa q^(m/2), so the factor is

    q^(me/2) kappa^(e mod2).

All cubic Taylor terms vanish in the odd case because3s>=2s+1. Therefore
arbitrary higher nilpotent cubic deformations do not invalidate the
formula. If the quotient weight uses h<=floor(e/2) digits, it is constant
on the eliminated transverse directions. The ray contribution is exactly

    q^(me/2) kappa^(e mod2)
       * sum_(r in A*) (-1)^(lambda_e(C r^3)+Q(r(a,1))).

The radial phase is binary quadratic. Subtract the Gaussian over tA from
the Gaussian over A to evaluate it. The origin contributes one smaller
state with factor q^(2b), depth e-3, and quotient height h-1. At e=2 or3,
its contribution is (-1)^Q(0) q^(b(e-1)). The condition3h<=e+1 remains
sufficient throughout this descent.

## 6. What unbounded b costs

Geometry, coefficient operations, Hensel lifting, and each Gaussian are
polynomial in the original n=bde and explicit description length. Streaming
the2^k residue candidates and processing each candidate across all depths
gives2^k poly(n,L) time with polynomial working storage, before any
depth-one terminal. The2^k factor is manufactured and charged.

For e=0 or2 modulo3 there is no field terminal. For e=1 modulo3, a
fixed-variable point-counting bound must not be called polynomial while b
grows. One transparent alternative is to fix z in F_q, note that
Tr H_0(x,z) is binary quadratic in x, and sum its exact Gaussian over all
q values of z. This costs2^d poly(bd). It is not polynomial in growing d.
For fixed b, the established fixed-variable Lauder--Wan terminal is
polynomial in d. These costs must remain explicit.

## 7. An acquired one-ray family with unbounded module rank

For any number of pairs, let

    H_0=sum_i (X_i^3+X_iY_i^2+Y_i^3+Z X_iY_i).

Assume3 does not divide d. In the chart Z=1 the critical equations for
each pair are

    X_i^2+Y_i^2+Y_i=0,     Y_i^2+X_i=0.

They imply Y_i(Y_i^3+Y_i+1)=0. The cubic Y^3+Y+1 is irreducible over F_2,
and its three roots lie in F_8. None lies in F_(2^d) when3 does not divide
d, so X_i=Y_i=0 is the only residue solution. The binary kernel dimension
is zero for every b. The infinity matrix is block diagonal with blocks
[[1,1],[0,1]], hence invertible. The single ray is the Z-axis, has residue
critical value zero, and has positive quadratic sign.

Arbitrary higher nilpotent cubic coefficients and allowed quotient
quadratics preserve the verified geometry and unique-lift argument. Thus
the coefficient-level algorithm is polynomial uniformly in unbounded b,d,e
for depths0 or2 modulo3. The raw version additionally needs the root
compiler's representation acquisition and exact-fit proof. If3 divides d,
each pair instead contributes a two-dimensional binary kernel; this is a
real field-degree qualification, not an incidental implementation choice.

`higher_rank_fixed_field_checks.py` independently checks the two-coordinate
binary linear kernel over every extension degree from1 through12. It also
enumerates the roots of Y^4+Y^2+Y only as a small-field validation oracle.
The measured kernel dimension is zero exactly when3 does not divide d,
and is two otherwise. Production acquisition uses the binary linear system
and does not enumerate field elements.

## 8. Why arbitrary nilpotent deformations prevent removing the2^k factor

There is a direct reduction from arbitrary Boolean cubic signed counting
to this unbounded-rank geometric family at d=1,e=2, even with M invertible
and no quotient noise. Let F(u_1,...,u_N) be a Boolean cubic, with even N
(add an unused bit if necessary). Put m=N+2 and b=m+1. Introduce two
auxiliary coordinates a,beta and write W=(u,a,beta), grouped in symplectic
pairs. Let

    q(W)=q_u(u)+a beta,
    H_0=Z q(W)+sum_pairs(X^2Y+XY^2).

Its third form is Z wedge Omega, and its infinity matrix M=Omega is
invertible. In the chart Z=1 its gradient is Omega(W^[2]+W), which
vanishes on every binary W. Thus its binary kernel dimension is m.

Homogenize F(u)+q_u(u)+a to ordinary degree three using Z; call the result
G. Over A=F_2[t]/t^2, set H=H_0+tG. At every chart critical vector
v=(W,1) with q(W)=0, the uniquely lifted critical value is tG(W,1): the
change in H_0 from lifting is zero modulo t^2 because its gradient
vanishes. The even-depth transverse factor is2^m, and its two unit radial
values give another factor2. The origin contributes2^b. Consequently

    Z_A(H)=2^b [1+sum_(q(W)=0) (-1)^(F(u)+q_u(u)+a)].

For each fixed u, the auxiliary sum is

    sum_(a beta=q_u(u)) (-1)^(q_u(u)+a) =1.

For q_u=0 the three pairs contribute1+1-1; for q_u=1 the unique pair
(1,1) contributes1. Therefore

    Z_A(H)=2^b(1+Z_F).

Recover Z_F by division and subtraction. This is a polynomial-size,
one-query exact reduction. The original binary input count is2b=2N+6.
The full binary centroid remains A by Section2. Thus even this acquired
geometry, with an invertible infinity matrix, does not make arbitrary
unbounded-rank nilpotent deformations polynomially countable unless
FP=#P. The kernel-dependent exponential
factor is substantive. The one-ray family in Section7 avoids this
obstruction through a verified zero-dimensional binary kernel.

For completeness, Boolean cubic signed counting is #P-hard by gate
arithmetization. Given a Boolean circuit, use its input and internal wire
variables and one binary multiplier per gate constraint, plus one for the
accepting-output constraint. Each gate equation has degree at most two,
and the sum of multiplier times constraint has degree at most three.
Summing its sign over the multipliers selects exactly the valid accepting
computations, with the known factor2^(number of constraints). Internal
wires are uniquely determined by the original circuit inputs. This proves
the required hardness without a conjectural inequality.

`higher_rank_boundary_checks.py` executed12 independently disguised
reductions through18 original bits and verified the full centroid dimension
two in every case. Together with the missing-infinity counterexample,
these cover1,119,232 complete truth assignments. Five additional field
cases verify acquisition of the unique exterior factor line through b=9
over F_8. Results and exact input polynomials are preserved in the matching
JSON file.

### The same obstruction over the raw compiler's F_8 field

The reduction above is not confined to d=1. Keep exactly the same
F_2-coefficient polynomials H_0 and G and use any odd d. The chart critical
equations still force every coordinate of W into F_2. The number of
accepted binary critical rays is

    N_crit=(2^m+2^(m/2))/2.

The unique critical value at each lifted ray is tG(W,1), with G(W,1) in
F_2. Cubing permutes F_(2^d) because d is odd. Therefore the depth-two
unit radial character sum is q(q-1) if G=0 and -q if G=1. Equivalently,
it is q[(q/2)(-1)^G+(q/2-1)]. Each ray's transverse factor is q^m, while
the origin contributes q^b. The same auxiliary cancellation now gives

    Z_A(H)=q^b[1+(q/2)Z_F+(q/2-1)N_crit].

In particular, for q=8,

    Z_A(H)=8^b[1+4Z_F+3N_crit],    n=6N+18.

Thus the #P-hardness remains at fixed d=3, fixed e=2, with no missing
critical points at infinity, no quotient perturbation, and full acquired
binary centroid of dimension de=6. The zero-kernel tractable family and
the arbitrary-kernel hardness family meet the same infinity certificate;
the charged kernel dimension separates their counting difficulty.

The independent F_8 test sums over every residue assignment, eliminates
the higher digits by exact character orthogonality, and compares against
this closed formula. Cases with N=2 and N=4 have respectively30 and42
original binary inputs. They cover2,129,920 residue assignments. Both
random binary-affine disguises have full acquired centroid dimension six.
The saved JSON contains the source cubic, the ordinary ring polynomial,
the disguise, the extracted Boolean ANF, and the exact counts. It does not
claim enumeration of all2^30 or2^42 original bit assignments.

## 9. A separate obstruction when the infinity matrix is omitted

The preceding obstruction is stronger, but the degenerate example also
has a useful exact formula. Let q=8, e=2, and use k pairs, with

    H_0=Z sum_(i=1)^k X_iY_i,       b=2k+1,
    H=H_0+tG(X),

and let Q(X) be any binary quadratic on the residue X coordinates. Put
f(X)=Tr G(X)+Q(X) and S_f=sum_X(-1)^f(X). Expanding a ring vector as
v+t w makes the phase linear in w. Orthogonality gives q^b exactly when
grad H_0(v)=0 and zero otherwise. At Z=0 the critical condition is
X dot Y=0. For X nonzero there are q^(k-1) choices of Y; for X=0 there
are q^k. At each nonzero Z the only critical point is X=Y=0. Consequently

    Z_total=q^b[q^(k-1)S_f+
                 (q^k-q^(k-1)+q-1)(-1)^f(0)].

For a Boolean cubic p on m bits, take k=2m and write X=(x,a), with
x,a in F_8^m. Split p=p_3+p_(<=2), and set

    G(X)=p_3(x)+sum_i a_i x_i^2,
    Q(X)=Tr[p_(<=2)(x)+sum_i a_i x_i].

Here G is ordinary homogeneous cubic; Q is binary quadratic, since the
field multiplication is bilinear and squaring is binary-linear. Summing
over a imposes x_i^2+x_i=0 for every i, so all x_i belong to F_2 and

    S_f=q^m Z_p.

The equality Tr_(F_8/F_2)(1)=1 preserves the source Boolean phase. Thus
the source signed count is recovered by one exact affine arithmetic
expression. The original input count is n=6(4m+1)=24m+6; all coefficients
and masks are constructed in polynomial time. The centroid remains the
entire chain ring by Section2. This family has M=0 and correctly fails
the infinity gate. Its formula pinpoints the positive-dimensional
critical locus as a carrier of an unrestricted cubic phase; no unproved
compression or free decomposition is used in the obstruction.

## Primary-literature qualification

Local stationary phase and reduction to quadratic contributions have
established ancestry. Adamski, *Non-Archimedean and motivic stationary
phase formulas*, https://arxiv.org/pdf/2502.04881, version2, Section1.2,
explicitly excludes residue characteristic two before using the
Cluckers--Herremans Morse lemma; its stationary formula continues under
that hypothesis. It therefore does not directly justify the formulas
above. The finite half-depth argument given here establishes the required
characteristic-two statement directly. This distinction does not amount
to a claim of historical priority for the quadratic stationary-phase
identity or for the full representation-compiler pipeline.
