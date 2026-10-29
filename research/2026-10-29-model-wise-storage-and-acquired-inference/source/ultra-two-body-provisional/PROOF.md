# Pauli clock transfer: a uniform gap and phase path, with the norm gate separated

29 October 2026. The positive result below is a constant-overhead, constant-
penalty-in-N, two-body **bounded-dimension qudit** construction of an endpoint
with a uniform gap and a uniformly gapped local path to the code with product
ancillas. It is not a proof of stability against arbitrary physical perturbations
of that endpoint. The stronger full-Hamiltonian small Yin--Lucas-norm identity
asked for is not acquired; Section8 gives a structural obstruction for the
natural symmetry-preserving clock/SW dressing. No finite-temperature statement
is made. No physical model is run.

## 1. Inputs, ordinary methods and exact output

Let {S_c:c in C} be positive commuting nonidentity Pauli checks on N qubits,
with no minus identity in their group. Each check has weight <=w, each data
qubit occurs in <=r checks, and all check supports have bounded spatial range.
The target is Hcode=sum_c(I-S_c)/2. No independence of the check list is
assumed. The accepted RX/RZ family has w,r<=7; its bounded-density spatial
embedding remains the named primary premise.

Choose a constant L>=max(3,w), for example L=8 for this family. There is ONE
L-level clock per supplied check and no freely fixed cat sector. Its vacuum
is uniquely |0>. Each simulator term acts on one data qubit and one clock,
or on a clock alone. The construction needs O(N) clocks, bounded degree,
bounded interaction range and strengths depending on w,r but not N.

The ordered-product ring mechanism is ordinary: see
[König0901.1333v2](https://arxiv.org/html/0901.1333v2), especially the clock
construction and the many-clock convergence qualification in Section4.3.
Exact two-body topological phase constructions are also prior, notably
[Ocko--Yoshida1107.2697](https://arxiv.org/html/1107.2697v1) for toric/quantum-
double models. What is proved here rather than imported is a generic Pauli
reduction to weak product-clock sectors and a uniform local sensitivity bound
that pays their syndrome-energy remainder. The elementary contraction below
is an explicit finite-body/qudit version of ordinary Kirkwood--Thomas theory;
[BDL0707.1894v1](https://arxiv.org/html/0707.1894v1) is its controlling prior.

## 2. Simulator and exact prefix gauge

Factor S_c=P_c,1 ... P_c,wc into its single-qubit factors, and pad with
identities to L factors. Distinct nonidentity factors within a check have
disjoint support. Use clock states0,...,L-1 moduloL and put

    Hsim=Delta [ sum_c (I-|0><0|)_c
                -lambda sum_c sum_j P_c,j (|j><j-1|+|j-1><j|)_c ].       (1)

Indices j run1,...,L. An identity-labelled edge is one-body; every other edge
is literally a data-qubit/clock two-body term. Place each clock in its check's
bounded-radius neighborhood. Bounded data incidence makes the clock density
bounded as well.

Define R_c,a=prod_(j<=a) P_c,j for a=0,...,L-1, and

    U_c=sum_a |a><a|_c tensor R_c,a.

It is a product of <=w controlled-single-qubit-Pauli gates. Color intersecting
check supports and apply the U_c in that color order. At most
B+1 colors suffice, B=w(r-1), so the circuit depth is <=w(B+1), independently
of N. Let U denote the resulting finite-depth unitary.

Conjugating a hop of clock c by U_h, h!=c, only multiplies its physical Pauli
by the sign determined by the symplectic pairing with R_h,a. This is a
diagonal sign function of clock h; it introduces NO new physical Pauli.
At its own gauge U_c, a nonwrapping hop becomes physical identity, while the
wrapping hop becomes the WHOLE S_c. All other signs remain clock diagonal.
Consequently

    U Hsim U*=Delta H'(lambda; S),                            (2)

and the data dependence of H' is only through commuting whole checks. This
is an exact all-sector identity, not perturbation theory. Every physical
logical operator is inert in each syndrome sector of (2).

Each gauged term has norm1 and acts on <=q=1+B clocks. A safe interaction-
strength bound is J=Lq: no clock occurs in more than Lq such terms. We can
therefore analyze every formal sign assignment s_c in {+1,-1}, including
assignments excluded by actual check relations, as

    H_s(lambda)=sum_c (I-|0><0|)_c +lambda V_s,
    |supp(V_e)|<=q, max_c sum_(e containing c)||V_e||<=J.       (3)

The graph or geometric range of these weak clock interactions is bounded.
The estimates below do not use a global isolated ancilla-vacuum spectral band.

## 3. A uniform finite-body/qudit KT lemma

Here the single-clock dimension is L. A creation word a_M^dagger creates a
specified nonzero clock value on each site of nonempty M and acts as |a><0|
there. All creation words commute, including different labels at the same
site (both products then vanish). Set

    C=sum_M C_M a_M^dagger,   ||C||_d=max_i sum_(M containing i)||C_M||.

Coefficients may be scalars or belong to a commutative unital Banach algebra
with submultiplicative norm. Below we use the l1 algebra of the FREE group
(Z2)^C, so ||S_X||=1. This is not an assumption that actual checks are
independent.

For H0=sum_c(I-|0><0|), define

    Phi(C)_M=lambda/|M| <M|exp(ad_C)V|Omega>,
    E=lambda <Omega|exp(ad_C)V|Omega>.                        (4)

The commutator expansion stops after2q creation factors on any V_e. Every
factor must meet e's support, and more than2q leaves at least two creations
at the same site on the same side of V_e. Such a product is zero.

For k creation arguments of densities c_1,...,c_k, direct coefficient
counting gives

 max_i sum_(M containing i) |M|^-1
     ||<M|ad_C1 ... ad_Ck V|Omega>||
 <= J L^q (2q)^k (1+2k) prod_j c_j.                         (5)

To see the locality factor, each commutator gives <=2^k terms, and the
output labels on the q touched sites cost at most L^q. If i lies in that
support, each creation sum costs <=q c_j. Otherwise i must lie in some
M_j. All sites of M_j outside the support remain created in the output;
hence |M_j|<=(q+1)|M|. The bound sum_(e meeting M_j)||V_e||<=J|M_j|
cancels this denominator. Summing over the k choices gives the second
part of (5); (q+1)/q<=2 yields the displayed form.

Let a=1/(4q) and rho=1/(64 q J L^q). On ||C||_d<=a, equations (4)--(5)
give

    ||Phi(C)||_d <= |lambda| J L^q (1+4q a) exp(2q a),
    Lip(Phi) <= |lambda| J L^q (6q+8q^2 a) exp(2q a) <=1/4       (6)

for |lambda|<=rho, using exp(1/2)<2. The map sends this ball strictly inside
itself. Thus its fixed point exists uniquely and is analytic in lambda and
in any bounded local amplitudes; this assertion holds in the coefficient
Banach algebra as well. The state exp(-C)|Omega> is an eigenvector of (3)
with the E in (4).

**The uniform GAP is a separate step, not inferred from that eigenvector.**
Fix a real syndrome. Write any other vector after KT similarity as
B|Omega>, with B a creation operator plus a scalar. Creation commutes with
C. For an eigenvalue E+delta its nonempty coefficients satisfy

    (|M|-delta) B_M
       =-lambda <M|exp(ad_C)[V,B]|Omega>.                    (7)

If |delta|<1/2, then ||(|M|-delta)^-1||<=2/|M|. The differentiated estimate
in (6), with B as one argument, bounds the right side in density norm by
2*(1/4)||B||_d. Thus B's nonempty part must vanish. Its scalar part can
only produce the already known eigenvector. This also excludes a second
independent eigenvector at delta0. Since the actual scalar-sector Hamiltonian
is Hermitian, the branch beginning at the unique product vacuum remains its
unique ground state and has gap >=1/2. There is no N in this argument.

## 4. Marked-wrap sensitivity, with no invalid symbol derivative

Keep coefficients in the free stabilizer group l1 algebra. For a fixed c,
multiply JUST its gauged wrapping edge by a scalar eta, |eta|<=1. This term
has norm W<=1, and the bounds q,J remain valid. Let B=partial_eta C and use
the total weighted norm ||B||_t=sum_M |M| ||B_M||.

The same counting as (5), now summed over all i, gives

    ||D Phi(C) B||_t <= 2|lambda| J L^q exp(2q a)||B||_t,
    ||partial_eta Phi(C)||_t <= |lambda| L^q W exp(2q a).

The factor |M| cancels (4)'s denominator. A marked creation word B_M then
meets a total interaction weight <=J|M|, which is exactly the weight in
||B||_t. Hence

    ||partial_eta C||_t <=4 |lambda| L^q W.

Differentiate the finite commutator formula for E in (4). The direct term
is <=2|lambda|W, and the C-derivative term is bounded by
4|lambda|J ||partial_eta C||_t. Thus

    ||partial_eta E|| <=3 |lambda| W                         (8)

throughout the stated disk, uniformly in the number of clocks. The fixed
point has strict slack, so ordinary differentiation on the eta interval and
Cauchy estimates on |lambda|=rho are legitimate.

There is NO derivative of a generator satisfying S_c^2=1. Instead, define
the bounded sign-flip automorphism T_c on the free group algebra by
T_c(S_X)=(-1)^{1_(c in X)}S_X. In the gauged Hamiltonian the only occurrence
of S_c is that wrapping edge, so

    (E-T_c E)/2 = (E(eta1)-E(eta-1))/2.

Its l1 norm is EXACTLY the sum of absolute coefficients whose parity label
contains c. Integrating (8) gives the uniform bound3|lambda|. Even wrap
returns are included in the marked derivative and disappear only at this
final parity difference; no scalar contribution is falsely differentiated
away.

## 5. Winding pays the syndrome-energy remainder

In any vacuum-to-vacuum perturbative word, each individual clock follows a
closed walk on its L-cycle. Modulo2 the edge-use vector of such a walk is
either all0 or all1. A wrapping-edge parity1 therefore requires at least L
steps of THAT clock. Reordering Pauli factors of different gadgets produces
only scalar signs. Thus ALL coefficients of nonidentity stabilizer symbols
vanish below orderL. The possibly extensive lower-order scalar energy
shifts remain; after Delta rescaling they need not be small.

At orderL, the only nonconstant walks are the two complete orientations of
one clock ring. No proper prefix returns to the vacuum, every intermediate
energy is1, and all other clocks are in0. The L minus hopping factors and
L-1 minus denominators give the coefficient -2 S_c. Consequently

    E(lambda; S)=b(lambda) I -2lambda^L sum_c S_c+R(lambda; S).

The Cauchy estimate from (8) gives the following genuine local receiver:

    max_c sum_(X containing c) |R_X(lambda)|
       <= 3rho (|lambda|/rho)^(L+1)/(1-|lambda|/rho).          (9)

This estimate is obtained BEFORE quotienting actual check relations. Such
relations can only make a formal sign assignment inadmissible or merge
operator terms. On the allowed syndromes the conservative bound (9) still
holds. No factor N has entered it.

Choose once and for all

    lambda_*=rho^L/12,       Delta=1/(4lambda_*^L).            (10)

Since rho<=1, lambda_*<=rho/2, and (9) is at most lambda_*^L/2. For a sign
assignment with d negative checks,

    Delta[E(s)-E(+)] >= Delta(4lambda_*^L-2*lambda_*^L/2)d
                         = (3/4)d.                         (11)

The auxiliary excitation gap is at least Delta/2. Therefore (1) has the
same exact logical ground multiplicity as the code and a spectral gap
>=min(3/4,Delta/2)=3/4. The conclusion is valid for every finite N, with all
penalties and overhead constants fixed independently of N.

## 6. An explicit uniformly gapped PHASE path

Let 0<=v<=lambda_* and use the gauged H'(v;S). Define the path, up to a
scalar energy shift, by

    K(v)=Delta H'(v;S)
           -2Delta(lambda_*^L-v^L) sum_c S_c.                (12)

Every syndrome has the same fixed leading code coefficient along this
path. The remainder in (9) is bounded by its value at lambda_*, so the
proof of (11) gives the same gap3/4. Within a syndrome, adding the bare
check term is scalar and preserves the clock gap Delta/2. At v0, (12)
is exactly Hcode+Delta sum_c(I-|0><0|)_c, up to an additive constant;
at v=lambda_* it is the gauged simulator.

This is a bounded-range, bounded-strength-in-N path. It may contain
many-body terms, as the TARGET itself does. A finite-depth unitary path
then undoes U. Standard gapped spectral flow consequently maps the ground
projectors by a quasi-local unitary. Only the actual low-energy ground
doublet is transported; no entire P0 band is claimed isolated. The path
does not approach lambda0 with a closing code gap: the retained bare-check
coefficient in (12) is essential.

## 7. Actual constant resources for the accepted family

Using the uniform w=r=7 input gives B42, q43, L8, J344 and
rho=[64*43*344*8^43]^-1. Formula (10) is an explicit rational constant;
its penalty has roughly ten thousand BITS and is physically prohibitive.
This is not a useful laboratory strength estimate. The primary geometric
ell and all original code overheads are additional fixed constants.

`compile_clock.py` constructs the complete two-body description and exact
prefix/sign description on the EXISTING level2 input. It uses no producer
scientific code and performs no extra replacement, rank, trajectory or
small-matrix experiment. Its output is the actual native Hamiltonian recipe,
not a new model fixture or a test of (9) at one small instance. The all-N
claim is the algebra and uniform contraction above.

The free coefficient algebra has exponential formal dimension, but the
constructor does NOT enumerate it or compute the unknown ground energy.
The explicit local path (12) uses only the supplied Pauli list and the
uniform scalar bounds. A sparse implementation has O(N) local terms;
the executed implementation stores dense integer Pauli masks and its
3.17MB description cost is charged, without a linear-byte-cost claim.

That retained input has algebraic subdivision ell3. Its literal Euclidean
embedding is NOT acquired. The bounded-range geometric theorem applies to
the source's separately qualified large fixed ell and bounded-density
embedding; the small retained algebraic input does not replace that premise.

## 8. The stronger full-tensor local-norm criterion is still unpaid

The gapped path is NOT the claimed identity

    W Hsim W*=Hcode tensor I + product-ancilla penalties + small E          (13)

in the full Yin--Lucas local norm. In fact (13) cannot have arbitrarily
small E for a symmetry-preserving dressing of this clock construction.
Every gauged hopping term is off diagonal on its OWN clock, so the normalized
clock trace of H'_s is independent of s. Any dressing commuting with all
bare S_c preserves that trace within each actual syndrome sector, including
after averaging over the logical multiplicity. The conditional expectation
onto the physical stabilizer algebra therefore maps the dressed simulator
to a scalar. The corresponding expectation of the right side of (13) maps
E to -Hcode plus a scalar.

This conditional expectation is ancilla trace followed by Pauli twirling;
it is contractive and does not enlarge physical support. A nonidentity
check S_c of weight w_c consequently has an error Pauli coefficient of
magnitude at least1/2 (assuming the source checks are distinct; duplicates
add). In any support-weighted local decomposition,

    ||E||_kappa >= (1/2)exp(kappa w_c).                      (14)

Choose any physical site in that check: only terms containing its WHOLE
physical support can contribute to that Pauli coefficient. Triangle
inequality proves (14). Standard local SW performed on the exactly gauged
Hamiltonian preserves this stabilizer symmetry and cannot remove this
obstruction. Increasing Delta at fixed L does not make (14) small.

This is a structural obstruction for the natural clock/SW dressing, not
a no-go for every two-body simulator or every possible nonsymmetry-preserving
unitary. The large excited-clock-conditioned terms are real. They are not
small perturbations in the required full operator norm, even though they
do not obstruct the phase path or the endpoint gap.

## 9. Remaining scope and decision

The acquired positive operation is an explicit general Pauli-stabilizer to
two-body bounded-qudit **uniform-gap / gapped-phase-path** compiler with
fixed-in-N resources. It avoids a free cat sector and a global P0-band
assumption. König and Ocko--Yoshida receive mechanism/phase-prior credit;
historical novelty of this generic Pauli/marked-KT conjunction is UNKNOWN.

The original requested arbitrary-physical-perturbation transfer is NOT
established. A quasi-local phase unitary has spatial tails; this alone does
not give exponential SUPPORT-VOLUME locality of transformed perturbations
in Yin--Lucas's norm. A separate relative-defect/local-parent stability
theorem, or an all-sector small-error construction with a genuinely paid
norm, is still required. Treating the high-clock terms as small would be
incorrect. Replacing each L-level clock by binary qubits also does not
preserve two-body locality automatically. No two-body-QUBIT reduction,
perturbed thermal lifetime, preparation protocol or physical accuracy claim
is included.

There is a precise algebraic reason not to extend the KT proof for free:
a generic physical perturbation fails to commute with the dressed source
checks. Its KT coefficients then lie in a NONCOMMUTATIVE data algebra.
Creation words with those coefficients need not commute, the finite
commutator truncation used in (4)--(7) is no longer justified, and the
classical sign-sector minimization disappears. This is an actual missing
operation. The elementary global operator-norm perturbation bound would
instead require a local strength O(1/N); that is an insufficient proof
method here, not a physical lower bound or an impossibility theorem.
