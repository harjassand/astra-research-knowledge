# A frustration-free normal form for weak Pauli clocks

29 October 2026. This is a NEW continuation; the earlier `two_body_phase/`
package is unchanged. No model, clock matrix or finite code level is rerun.

**Status.** The construction below gives a parameter-qualified route to
arbitrary bounded-range physical perturbation stability. It uses spatial
quasi-locality and a frustration-free normal form, followed by an explicit
polynomial-buffer localization argument. It does NOT assert that a spatial
spectral flow has the support-volume norm used by Yin--Lucas. The literal
previously compiled value of lambda has NOT been numerically compared with
the additional smallness constant in Section 5. A uniformly smaller positive
constant lambda is allowed; its penalty remains independent of system size.

The two new load-bearing elementary operations are the operator-valued
vacuum martingale in Section 3 and the polynomial-buffer block-diagonal
localization in Section 7. Ordinary exact spectral-flow filters, Lieb--Robinson
bounds, and the Bravyi--Hastings--Michalakis bootstrap are explicitly retained
as prior tools. No priority or physical feasibility is inferred.

## 1. Qualified input and result

Use the commuting positive Pauli checks, bounded weight w, bounded incidence r,
clock dimension L, exact prefix gauge U, and H'(lambda;S) from the frozen proof.
For formal independent signs s, the scaled clock Hamiltonian is

    H_s(v) = Naux + v V_s,   Naux=sum_i Q_i,
    Q_i=I-|0><0|_i,         0<=v<=rho.

All its clock ground states are simple and have gap at least 1/2, uniformly in
s, v and the number of clocks. No entire zero-ancilla spectral band is isolated.
The vacuum energy obeys the already acquired identity and local bound

    E(S)=b I-2lambda^L sum_c S_c+R(S),
    max_c sum_(X containing c)|R_X| <= lambda^L/2              (1)

for 0<lambda<=lambda_*=rho^L/12. Set Delta=1/(4lambda^L).

In addition, the data and clock cells have a uniform spatial metric of
polynomial growth:

    |B_R(x)| <= nu (1+R)^D.                                  (2)

All source checks and gauged clock interactions have fixed spatial range.
These are the source-qualified bounded-density geometry premises, NOT a
property inferred from the finite ell3 compiler. All constants may depend
on this fixed geometry, w,r,L, but not on N.

The source code has distance d_N and check-soundness cutoff dc_N; put
ds_N=min(d_N,dc_N). A product of checks that is a stabilizer of weight M<ds_N
has an expansion into at most f(M)<=K(1+M)^p supplied checks, with fixed K,p.
For the accepted recursive family ds_N grows as a positive power of N.

**Parameter-qualified theorem.** There is a constant lambda_FF>0, independent
of N, such that for every fixed

    0<lambda<=min(lambda_*,lambda_FF), Delta=1/(4lambda^L),    (3)

the two-body-qudit Pauli-clock endpoint is stable to sufficiently small
arbitrary physical bounded-range Hermitian perturbations. More precisely,
for each such FIXED lambda there are constants epsilon_0,gamma_0>0,
independent of N (but allowed to depend on lambda and Delta), so that a
perturbation of local strength epsilon<=epsilon_0 leaves a band of exactly
the source logical dimension, separated from the rest by gamma_0. Its
width is at most

    C N epsilon eta(c ds_N^(1/D)),                           (4)

where eta decreases faster than every inverse power; stretched-exponential
eta can be retained throughout. Thus (4) tends to zero for this source family.
All physical perturbations may break every bare check symmetry.

This is a theorem-level, finite-constant construction. No numerical
epsilon_0, lambda_FF or physical implementation is acquired here. In
particular it is not a numerical stability receipt for the frozen clock
recipe at its literal lambda_*.

## 2. A common exact unitary for all syndrome ground fibers

Work first in the abstract local algebra

    A = tensor_i [ B(C^L)_clock,i tensor C({+1,-1})_symbol,i ].

One may realize the symbols as diagonal Z operators on auxiliary two-level
systems, retaining only their diagonal algebra. This is an analytical lift;
these extra symbol systems are NOT added physical degrees of freedom.
The map S_c -> actual source check S_c is a unital *-homomorphism on this
commutative coefficient algebra. It is norm-contracting, including when the
physical checks have relations. A symbol at c has physical support on that
WHOLE supplied check. Every pullback support is the union of precisely those
check supports and clock sites present in the abstract term.

Choose the ordinary exact spectral-flow filter with Fourier cutoff strictly
below 1/2, for example 1/4. Its self-adjoint generator is

    G(v)=integral W(t) exp(itH'(v)) V exp(-itH'(v)) dt.        (5)

The filter has the usual inverse-frequency matrix elements across energy
differences of magnitude >=1/2. Each H'(v),V commutes with every symbol.
Consequently (5) restricts in EACH fixed s sector to the ordinary exact
ground-projection spectral-flow generator for H_s(v). The same one operator
therefore transports ALL the simple clock ground projections at once.
There is no matrix element between different s sectors in this calculation;
overlap of their energy ranges is irrelevant. If A(v) transports the vacuum
to those ground fibers, take W(v)=A(v)^*.

Locality of (5) does not require a global spectral gap between different
syndromes. It uses only the local interaction and filter bounds. Ordinary
Lieb--Robinson estimates in the lifted local algebra give a spatially
quasi-local W(v), commuting with every symbol. Uniformly for 0<=v<=rho,

    W(v)H'(v)W(v)^* = E_v(S)+Naux+D(v),                     (6)
    D(v)|Omega> = 0 for EVERY formal S.                     (7)

Hermiticity in (6) is retained. Starting at v=0 and integrating the
interaction derivative gives a decomposition D(v)=sum_Z D_Z(v) with

    sup_i sum_(Z containing i, diam Z>=R)||D_Z(v)||
         <= C0 v eta0(R).                                  (8)

Here eta0 has all polynomial moments; it can be chosen stretched
exponential with any fixed, sufficiently small exponent. Polynomial factors
in support size can be absorbed in a slower such eta0. C0,eta0 are uniform
finite quantities from the fixed filter and the local interaction bounds.
The estimate is an interaction estimate, not a bound on the extensive
operator norm of W-I. The same estimates apply to the vacuum expectation
E_v(S), and to conjugating a small physical interaction by W.

For clarity, the derivative giving (8) is the sum of the original V, the
commutator of the spectral-flow generator with the locally bounded H'(v),
and their vacuum expectations. Filter-integrated LR estimates and their
Duhamel versions give its uniform spatial interaction bound. Integrating
over a parameter interval of length v supplies the displayed factor v.
On-site terms do not create a new spatial transport cost. No full-band
Schrieffer--Wolff series or unitary coupled-cluster inverse is assumed.

The ordinary primary tools are [Bachmann--Michalakis--Nachtergaele--Sims,
Proposition2.4, Lemma2.3, Theorems4.5/4.8](https://arxiv.org/html/1102.0842v2)
and the quasi-local-map/weighted-integral constructions in
[Nachtergaele--Sims--Young, Sections5--6](https://arxiv.org/html/1810.02428).
Only the sectorwise projection identity above is specific to the clock lift.

## 3. Exact martingale localization, with no exponential normal-order cost

This lemma is useful independently of the clock Hamiltonian. Let a Hermitian
interaction D in the lifted algebra satisfy (7), with spatial tail (8).
For a subset A of cells let Pi_A be the unital completely positive map that
vacuum-expects clocks outside A and uniformly averages symbols outside A,
and extends the result by identities. Keep both operations INSIDE the
abstract algebra until the final pullback.

Two elementary facts are important:

* Pi_A is Hermiticity preserving and norm-contracting.
* (Pi_A D)|Omega_A>=0 fiberwise for every remaining symbol assignment.

The second fact follows by applying <Omega_(A^c)| to D(s)|Omega>=0 and then
averaging s_(A^c). It is not a conditional expectation on physical dependent
checks. After pullback, support remains only on the retained source checks;
there is no averaging oracle acting on the physical code.

Order the cells arbitrarily, let A_i be its first i cells, and put

    T_i=Pi_(A_i) D-Pi_(A_(i-1)) D.                          (9)

Since Pi_empty D=0 and Pi_all D=D, sum_i T_i=D. Every T_i is Hermitian
and annihilates the vacuum for every symbol assignment. A local D_Z makes
no contribution to T_i unless i belongs to Z, and that contribution has
norm <=2||D_Z|| and support contained in Z. Thus T_i is spatially localized
near i, even though the chosen ordering itself need not be geometric.

Localize it again by concentric balls:

    T_i,0=Pi_(B_0(i)) T_i,
    T_i,R=(Pi_(B_R(i))-Pi_(B_(R-1)(i)))T_i, R>=1.           (10)

These operators are Hermitian, supported on B_R(i), and annihilate the local
clock vacuum for ALL its symbols. Therefore, for
P_B=|Omega_B><Omega_B| tensor I_symbols and Q_B=I-P_B,

    T_i,R=Q_(B_R(i)) T_i,R Q_(B_R(i)).                      (11)

There is no exponential expansion into creation monomials. From (8)--(10),

    ||T_i,0|| <=2C0 v eta0(0),
    ||T_i,R|| <=4C0 v eta0(R-1), R>=1.                     (12)

Indeed every surviving D_Z contains i; if diam Z<R its contribution to the
second difference in (10) is zero. Now use (2) to sum (12) at a given clock j:

    sup_j sum_(i,R: j in B_R(i)) ||T_i,R|| <= Cmart v,       (13)
    Cmart=2C0 eta0(0)+4C0 sum_(R>=1)nu(1+R)^D eta0(R-1).

All constants are independent of N. The norms may be evaluated before
pullback; a physical *-homomorphism can only lower them. The declared
physical support of T_i,R is all clocks in B_R(i), together with the union
of physical supports of source checks whose symbols are in that ball.
This fixed-range inflation preserves polynomial growth and spatial tails.
Hermiticity and (11) survive the pullback.

## 4. Pay the large excited-clock terms instead of discarding them

Choose v with Cmart v<=1/2. Let t_i,R be the explicit upper bound for
||T_i,R|| in (12); using the exact norm is unnecessary. Put

    a_j=1-sum_(i,R: j in B_R(i)) t_i,R >=1/2,
    F_i,R=T_i,R+t_i,R sum_(j in B_R(i)) Q_j.                (14)

Equation (11) and Q_B<=sum_(j in B)Q_j imply F_i,R>=0. Consequently

    Naux+D(v)=sum_j a_j Q_j+sum_(i,R) F_i,R                 (15)

is EXACT, positive and frustration free. Its ground space is the clock
vacuum tensored with arbitrary data. Each F_i,R annihilates that vacuum
locally. Its norm is bounded by (1+|B_R|)t_i,R; hence (15) has a spatial
tail with all polynomial moments. The large factor Delta is retained:
Delta F_i,R can have a very large absolute local norm. It is controlled by
the allocated Delta Q_j penalties, not asserted to be a small absolute
Yin--Lucas perturbation.

This is precisely why the frozen all-ancilla-trace obstruction is not
violated. The normal form is NOT code+product-clock penalties+small error.
The syndrome-dependent excited-clock terms remain in (15).

## 5. Make the code-energy remainder frustration free as well

Use the free-symbol energy expansion (1), before quotienting check relations.
For the spatial assertion below, KEEP the independent hop-amplitude
monomials as extra labels: X in (16)--(17) is a multi-index consisting of
that label and the nonempty symbol parity set, and `c in X` refers to the
parity set. Distinct labels are not combined even if their resulting
physical Pauli is the same. The SAME 1/8 bound holds with these unmerged
labels by the coefficient argument following (18). After multiplying by
Delta and subtracting E(+), write

    Delta[E(S)-E(+)]=sum_c Q_c+sum_X r_X(S_X-I),
    Q_c=(I-S_c)/2,
    max_c sum_(X containing c)|r_X|<=1/8.                   (16)

For any X, |S_X-I|<=2 sum_(c in X)Q_c. Thus

    b_c=1-2sum_(X containing c)|r_X| >=3/4,
    G_X=r_X(S_X-I)+2|r_X|sum_(c in X)Q_c >=0.              (17)

Then (16)=sum_c b_c Q_c+sum_X G_X is another exact FF expression.
Check relations may turn S_X into I but do not invalidate positivity.

Spatial locality of this rewriting must be paid; the unweighted incidence
bound (16) alone would not pay it. The existing KT construction can retain
independent formal amplitudes for EVERY hopping term in its l1 coefficient
algebra. A monomial of total order k uses k such terms. Its declared support
is their union; it has <=qk cells and physical support <=(q+w)k before a
fixed geometric inflation. Mixed monomials on disconnected interaction
components vanish: restricting to those components makes H and its unique
KT solution factorize, C additive, and E additive. Thus an energy monomial
of order k has diameter at most k times the fixed interaction range.

Marking one hopping term e, rather than only a wrapping hop, gives the
same total-norm derivative estimate as the frozen Section4:

    ||partial_(eta_e)E||_(formal l1) <=3|v| ||V_e||.         (18)

The mark lives in the free amplitude algebra; differentiation is performed
BEFORE setting amplitudes to 1 and BEFORE imposing S_c^2=1. Summing (18)
over hops touching a cell counts every monomial whose support contains it,
with at least its multiplicity. Replacing |v| by |v|exp(kappa(q+w)) inside
the same convergence disk pays an exponential support-volume weight.
Equivalently Cauchy estimates give exponentially decaying order/diameter
tails at any fixed |v|<rho. Winding still removes all syndrome terms below
order L and the leading term at order L. Retain this cluster support while
forming (17); the extra factor 1+|X| is absorbed in a slower exponential.
This proves spatial locality of all G_X and of their allocations.

More explicitly, use the Banach algebra of absolutely summable series in
commuting amplitude variables eta_e, tensored with the free symbol group
l1 algebra; every generator has norm one. The frozen KT estimates use
only submultiplicativity and commutativity and therefore have the SAME
rho in this enlarged algebra. Each Taylor coefficient of E at total
lambda-order k is homogeneous of degree k in the eta_e. Differentiating
eta_e counts its positive multiplicity, and the induced shift on monomial
indices is injective, so its l1 norm is the actual multiplicity-weighted
sum of absolute UNMERGED coefficients. For a fixed wrapping edge c, every
coefficient whose symbol parity contains c has positive such multiplicity.
Project to those parities, discard orders <=L (whose syndrome part is
exactly the acquired leading term), and use Cauchy on |lambda|=rho in
(18). This bounds that unmerged remainder incidence by

    3rho (lambda/rho)^(L+1)/(1-lambda/rho).

It is <=lambda^L/2 for lambda<=lambda_*. Multiplication by Delta gives
exactly the unmerged 1/8 used in (16)--(17); no cancellation after
amplitude evaluation, parity quotient or spatial regrouping is needed.

One explicit additional parameter prescription is

    lambda_FF = min(rho/2, 1/(2 Cmart)),                   (19)

using Cmart from the fixed uniform bounds of Sections2--3; then also impose
lambda<=lambda_* as in (3). All entries in (19) are determined by ordinary
fixed filter/LR majorants and the supplied geometric constants. Evaluating
those majorants numerically, or checking the old literal lambda_* against
(19), is NOT done here. No dependence on N is introduced by (19).

## 6. Local ground spaces and local gaps of the new normal form

Let Hbar be the sum of the positive code terms (17) and Delta times the
positive clock terms (15). It is unitarily equivalent to the simulator,
up to the scalar Delta E(+), via the finite-depth U and the W of Section2.
Choose the declared supports as specified above, including the WHOLE check
support of every retained symbol. For any physical region B, define Hbar_B
by keeping exactly those positive summands whose declared supports lie in B.

The retained single-check terms have coefficients >=3/4, and the retained
onsite clock penalties have coefficients >=Delta/2. Every other positive
summand annihilates their common local ground space: code terms involve only
checks whose whole supports are retained; clock terms vanish when their
declared clocks are all in the vacuum. Therefore

    ker Hbar_B = ker(Hcode_B+Naux_B),                        (20)
    Hbar_B >= (3/4)Hcode_B+(Delta/2)Naux_B,
    gap(Hbar_B)>=gamma=min(3/4,Delta/2)=3/4.                (21)

The projectors in (20) are NESTED as B increases. This is a property of the
NEW positive normal form, not of a truncated original frustrated clock
Hamiltonian. Cutting incomplete original rings is not being asserted to
preserve a gap. No strict spatial TQO-2 assertion is made.

## 7. A polynomial buffer is enough for the required relative-form bound

Here is an elementary replacement for importing a stronger Local-TQO
assumption. It is stated for any positive FF interaction satisfying (2),
(20)--(21), or analogous local projectors with the following property:

For every observable O supported in B_r(x), with r<=R_N, there is a scalar
c(O) such that

    P_(B_F(r)(x)) O P_(B_F(r)(x)) = c(O) P_(B_F(r)(x)),
    F(r)<=A(1+r)^P.                                        (22)

If F(r) exceeds the finite system, use the whole-system projector. The
scalar in (22) equals the global-ground scalar because P<=P_B. Applying
(22) to O^*O yields the exact norm equality

    ||O P_(B_F(r))|| = ||O P||.                             (23)

For our source, (22) follows directly from check soundness, NOT from an
unproved spatial filling improvement. Let M(r)=nu'(1+r)^D bound the data
sites in B_r. If M(r)<ds_N, every local Pauli is either a detected error,
a stabilizer, or (excluded by distance) a logical operator. A minimal
expansion of a stabilizer has <=f(M(r)) checks. Every connected component
of its check-overlap graph touches its support; otherwise that component
multiplies to I and can be deleted. With fixed check range Rcheck, all
these checks lie in

    F(r)=r+Rcheck[1+f(M(r))].                               (24)

This is polynomial, even though its exponent can be very large. For a
general operator, linearity of the exact compression suffices; no
exponential Pauli coefficient bound is used. Clock vacuum compression
reduces any clock-data observable to a data observable. Choose R_N as the
largest integer with M(R_N)<ds_N; it is a positive constant times
ds_N^(1/D), up to harmless small-size conventions.

**Localization lemma.** Suppose X_x is Hermitian, [X_x,P]=0, and has an
anchored decomposition

    X_x=sum_(r>=0)X_x,r, supp X_x,r subset B_r(x),
    ||X_x,r||<=epsilon f0(r),
    t(r)=sum_(j>r) f0(j),                                  (25)

where f0 has all polynomial moments. For any R<=R_N there are Hermitian
Y_x,r, 0<=r<=R, and Z_x such that

    X_x=c_x I+sum_(r=0)^R Y_x,r+Z_x,
    supp Y_x,r subset B_F(r)(x), Y_x,r P_(B_F(r))=0,
    ||Y_x,0||<=2epsilon f0(0),
    ||Y_x,r||<=24epsilon t(r-1) (r>=1),
    ||Z_x||<=14epsilon t(R).                               (26)

Proof. Put X^(r)=sum_(j<=r)X_x,j and c_r=Tr(PX^(r))/TrP.
Equation (22) makes P X^(r)P=c_rP for r<=R. Set

    O=Q(X_x-c_R I)Q, Q=I-P,
    O_r=X^(r)-c_r I,
    B_r=Q_(B_F(r)) O_r Q_(B_F(r)).                          (27)

Global block diagonality gives
||X_x-c_R I-O||<=2epsilon t(R). For r<=R,
||O-O_r||<=4epsilon t(r), so ||O_r P||<=4epsilon t(r).
Use (23) to replace P by P_(B_F(r)). For Hermitian O_r,
||Q_B O_r Q_B-O_r||<=2||O_r P_B||. Consequently
||B_r-O||<=12epsilon t(r). Take Y_x,0=B_0 and
Y_x,r=B_r-B_(r-1). Their support and vacuum-annihilation assertions use
the NESTING of the local FF projectors. The norm bounds and final residual
follow by telescoping, including the <=2epsilon t(R) global-ground block.
This proves (26).

For the positive local Hamiltonians with gap >=gamma, every such Y obeys

    |<psi,Y_x,r psi>| <= ||Y_x,r||/gamma
                         <psi,Hbar_(B_F(r)(x)) psi>.

Each positive interaction of Hbar is contained in at most
nu(1+F(r))^D balls centered at x. Summing gives

    |<psi,Y psi>| <= a epsilon <psi,Hbar psi>,               (28)
    a = [2nu(1+F(0))^D f0(0)
         +24sum_(r>=1)nu(1+F(r))^D t(r-1)]/gamma <infinity,
    ||sum_x Z_x|| <=14 |Lambda| epsilon t(R).               (29)

The crucial fact is that a polynomial F only adds a polynomial summability
cost. No uniform constant-width buffer, no strict spatial TQO-2, and no
support-volume spectral-flow estimate is assumed. Equations (26)--(29)
are the actual relative-defect receiver needed below.

## 8. Arbitrary small physical perturbations: the bootstrap

Let V be any Hermitian finite-range physical perturbation, with local
strength epsilon. Conjugate it by U and W; ordinary quasi-local-map bounds
give a spatially quasi-local interaction of strength C epsilon, with
rapid tails. It may fail to commute with every check and clock penalty.
Absorb C in epsilon in what follows.

Consider Hbar+sV, 0<=s<=1, initially on the interval on which its lowest
m=dim ker Hbar eigenvalues form a band of width <gamma/4 and have gap
>gamma/2 from the rest. This interval is nonempty in finite volume.
The ordinary exact spectral flow on that band gives U_s P_s U_s^*=P.
Use the ordinary even time-averaging filter with Fourier support strictly
inside (-gamma/2,gamma/2). For an anchored summand h_x+s v_x, define

    X_x(s)=U_s F_s(h_x+s v_x)U_s^*-F_0(h_x).                (30)

F_s kills off-band matrix elements and fixes Hbar+sV when summed over x.
Every X_x is Hermitian and commutes with P. Its anchored shell bounds have
the form (25) with epsilon times a fixed rapidly decreasing f0, uniformly
in s and N on this bootstrap interval. These are the ordinary BHM
filter/Duhamel/LR estimates; they require finite interaction moments and
a band gap, not commuting or strictly finite-range h_x. Positive quasilocal
summands can be anchored and their moment bounds summed first. Our
normal-form interaction has these uniform moment bounds.

For reference, the standard filtered-Hamiltonian and bootstrap steps are
in [Michalakis--Pytel, SectionsIV and VI](https://arxiv.org/html/1109.1588v2)
and [Nachtergaele--Sims--Young, Sections4--6](https://arxiv.org/html/2010.15337v3).
Their stronger displayed Local-TQO assumption is NOT imported here: exactly
that use is replaced by the proved localization lemma (26)--(29).

Apply that lemma to (30), with R=R_N. Up to a scalar, the conjugated
Hamiltonian is

    Hbar+Y+Z,  |<psi,Y psi>|<=a epsilon <psi,Hbar psi>,
    YP=PY=0,  ||Z||<=delta_N=14 |Lambda|epsilon t(R_N).     (31)

Choose the fixed epsilon_0 so that a epsilon_0<=1/4. Form bounds and the
min--max principle imply that Hbar+Y has exactly m zero eigenvalues and
the rest is >=(3/4)gamma. Adding Z puts the m eigenvalues in
[-delta_N,delta_N] and the remaining ones above
(3/4)gamma-delta_N. Since ds_N grows as a positive power of N, delta_N
is smaller than gamma/16 for all sufficiently large N, uniformly in s,
after one fixed choice of epsilon_0. These estimates are strictly better
than the bootstrap gap/width boundaries. Continuity therefore extends the
interval to s=1. The finitely many smaller sizes can be included by lowering
epsilon_0 once, using their uniform initial gap and their finite total
interaction norm. This introduces no N-dependent parameter.

This proves (4) and a uniform positive gap. If the input filter/interactions
are bounded by stretched exponentials, t(R_N) has such a bound at a
possibly smaller fixed exponent, giving the stated stretched-exponential
logical splitting. Ordinary spectral flow also supplies a spatially
quasi-local map on the logical ground band. No assertion of its
support-volume norm or perturbed finite-temperature memory time follows.

## 9. What was acquired and what was not

The previous endpoint gap and gapped path were insufficient by themselves.
This continuation constructs a NEW exact FF normal form retaining the large
excited-clock terms, pays its complete local ground spaces and gaps, and
provides the relative-form argument under the actual polynomial-buffer
check-soundness consequence. It removes the need to pretend the original
frustrated ring restrictions were FF or to invoke an unqualified unitary
coupled-cluster inverse.

The conclusion is an existence/constant-parameter two-body-QUDIT phase
transfer on the source-qualified finite-dimensional spatial family. It is
not the analogous statement for arbitrary nonspatial k-local perturbations
on expander graphs. It is not a two-body-qubit compiler. The useful
constant can be vastly smaller and its penalty vastly larger than the
already prohibitive frozen example. The original finite recipe and this
new parameter-qualified theorem are distinct receipts. No experiment,
device model, finite-temperature stability, threshold value, practical
advantage or historical novelty is claimed.

The FF normal form is an analytical comparison interaction, defined by
convergent filters and series. No efficient algorithm for writing its full
finite-N interaction table is claimed. Its positivity allocation uses the
scalar bounds (12), not a free oracle for exact many-clock operator norms.
