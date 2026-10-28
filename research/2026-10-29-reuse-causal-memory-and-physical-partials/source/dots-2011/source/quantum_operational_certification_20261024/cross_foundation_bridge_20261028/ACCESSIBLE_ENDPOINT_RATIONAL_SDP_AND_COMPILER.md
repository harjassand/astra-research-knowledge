# A finite rational endpoint optimizer and physical decoder compiler

28 October 2026. **Separate construction; independent receiving pending.**
This instantiates the accessible-channel optimization obligation in
SIGNED_CORE_COMPLETE_SERVICE_PREDICTION.md. It does not receive that source's
core-acquisition theorem. The theorem here starts with an explicitly supplied
rational Hermitian signed service Choi matrix. No hidden-model feasibility,
quantifier elimination, environment access, or supplied optimization oracle is
used. The generic rounded ellipsoid algorithm is a theoretical instantiated
algorithm, not an executed solver or delivered circuit.

## 1. Endpoint contract and conclusion

Use unnormalized, input-first Choi matrices. The supplied signed map
Nhat:L(C^p)->L(C^k) is Hermiticity preserving, but need not be positive or TP.
Its pk-by-pk Choi matrix Jhat has rational real and imaginary parts. Supply
rational 0<xi,zeta,nu<=1. There is a deterministic finite algorithm returning:

* an exactly rational CPTP service Choi Jtilde with
  half ||Ntilde-Nhat||diamond <= inf_(N CPTP) half ||N-Nhat||diamond +xi;
* an exactly rational CPTP decoder Choi C_R for a map C^k->C^p with
  e_Ntilde(R)<=inf_(D CPTP)e_Ntilde(D)+zeta;
* a finite circuit for an actual CPTP decoder R_actual with
  half ||R_actual-R||diamond<=nu.

Here e_N(D)=half ||D N-id_p||diamond. If a true service satisfies
half ||Nhat-N_true||diamond<=eta, then

    e_true(R_actual) <= inf_(D CPTP)e_true(D)
                            +4eta+2xi+zeta+nu.            (1)

The comparator holds the service, time, encoder and allowed payload calls fixed.
It is over all CPTP decoders, not a menu. Only the accessible service and decoder
are optimized. In particular eta is not clipped at one for a signed map.

The classical optimization cost is polynomial in p,k, the rational input bit
length, log(1/xi), and log(1/zeta). Circuit synthesis additionally costs a
polynomial in accessible dimensions and precision bits, as made explicit below.
This is not polynomial in log(k), not a bound on the cost of constructing Jhat,
and not an efficient hidden-process acquisition claim.

## 2. One explicit spectrahedron covers both tasks

Let C be a Choi variable for an m->n physical channel. Let L(C)-J0 be the
Hermiticity-preserving channel difference whose norm is optimized, with input
dimension a, output dimension b and Choi size D=ab. Assume a known rational
Frobenius Lipschitz bound

    ||L(E)||F <= ell ||E||F

and choose a rational g>=||J0||F. All coefficients of L and J0 are known rational.
The two instantiations are:

    task          m n a b ell       L(C)             J0
    projection    p k p k 1         C                Jhat
    recovery      k p p p p         J_(R_C Ntilde)    J_id_p.       (2)

For recovery ell=p is valid: coefficientwise Cauchy--Schwarz gives
||L(E)||F<=||Jtilde||F ||E||F, and a CPTP Choi matrix has
||Jtilde||F<=Tr Jtilde=p. In components,

    L(C)_(i,u;j,v)=sum_(y,z) Jtilde_(i,y;j,z) C_(y,u;z,v).

For projection one can take g=1+sum_ij(|Re Jhat_ij|+|Im Jhat_ij|);
for recovery take g=p. These avoid an uncomputed spectral norm.

The Hermitian diamond-norm epigraph is

    C>=0, Tr_n C=I_m,
    Z>=L(C)-J0,  Z>=-(L(C)-J0),
    Tr_b Z<=t I_a,  0<=t<=T;        minimize t/2.       (3)

The exact norm identity is the standard Hermitian symmetrization of the
completely bounded norm SDP, already independently checked for
IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY.md. It is not a new identity.

### Rational affine coordinates, rather than unhandled equality constraints

Use the usual rational Hermitian basis in dimension m: diagonal matrix units
and real/imaginary off-diagonal units. For traceless Hermitian n-by-n matrices
use E_jj-E_nn (j<n) and real/imaginary off-diagonal units. Their tensor products
span exactly Tr_n X=0. Write

    C(u)=I_(mn)/n + sum_j u_j A_j.

For n=1 the u-coordinate block is empty. The Gram matrices of these bases
have least eigenvalue at least one and largest eigenvalue at most 4n. Thus

    ||u||2 <= ||sum u_j A_j||F <= 2n ||u||2.             (4)

For Z use the ordinary rational Hermitian basis, so its coordinate-to-Frobenius
norm is at most 2 and its inverse norm at most 1. Adjoin the scalar t.
The number of real coordinates is exactly

    M=m^2(n^2-1)+D^2+1.                               (5)

All TP equalities now hold identically at every rational coordinate point.
There is no irrational orthonormal basis conversion.

### Explicit known center, inner radius and outer radius

Put

    s0=ell*m+g+1,
    C0=I_(mn)/n,  Z0=s0 I_D,  t0=b*s0+1,  T=2t0,
    r=1/[8(n^2+n*ell+b+1)],
    R=2m+a*T+s0*D+T+1.                                (6)

The center x0=(0,coordinates(Z0),t0) is rational. Since
||L(C0)-J0||op<=ell*m+g, both Z constraints have margin at least one,
the partial-trace constraint has margin one, and C0 has margin 1/n.
For a coordinate displacement of Euclidean norm at most r, the respective
operator perturbations are at most

    2n r,       (2+2n ell)r,       (1+2b)r.

They are smaller than the displayed margins; the scalar caps also hold.
Consequently B(x0,r) lies in (3), in its full M-dimensional coordinate space.

For every feasible point, C>=0 has trace m and ||C||F<=m, hence ||u||<=2m.
Also Z>=0 and Tr Z<=aT, so ||Z||F<=aT. This proves that the entire feasible
body lies in B(x0,R). The t-cap does not alter the optimum: every physical C
has a feasible oversized scalar Z with t<T, and the unconstrained minimum
cannot exceed the explicitly feasible center's t0. Compactness gives an
attained optimum. These bounds work for arbitrary signed Jhat, including bad
statistical records. They contain no source rank, eigenvalue or Slater promise.

## 3. The separation routine and the actual finite solver primitive

Given rational coordinates x, form the affine matrices in (3) exactly.
Check the two scalar caps and the PSD constraints. A violated scalar inequality
already is a rational separating hyperplane.

For a Hermitian matrix Q, exact rational congruence/LDL elimination either
certifies Q>=0 or returns a rational complex vector v with v*Qv<0.
One elementary witness routine uses a negative diagonal if present. A zero
diagonal with a nonzero entry h to another coordinate of nonnegative diagonal
d has negative vector (1,-conjugate(h)/(d+1)) on those coordinates. Otherwise
eliminate a positive diagonal pivot and recurse on its Schur complement;
lift a negative Schur witness by the same rational congruence. A zero matrix
is PSD. No approximate sign of an eigenvalue is accepted.

For a violated affine PSD constraint Q(x)>=0, the scalar affine inequality
v*Q(y)v>=0 separates the query x from every feasible y. Complex coefficients
are simply pairs of rationals, or one may use realification. Fraction-free
elimination, determinant bounds and rational arithmetic give polynomial bit
cost and polynomial witness length. Thus this is an implemented mathematical
separation procedure, not an eigenvalue or optimization oracle.

Apply the **rounded rational ellipsoid weak-optimization algorithm** of
Groetschel--Lovasz--Schrijver, Sections 1--3, to this separation routine and
the explicitly known (M,x0,r,R). Its output y can be required to satisfy

    dist(y,K)<=e,        t_y/2<=opt_K(t/2)+e,            (7)

for any supplied rational e>0. Exact separation is stronger than its weak
separation contract. The algorithm includes finite precision and rounded
ellipsoid updates; exact real-arithmetic ellipsoid updates are NOT being
substituted for the cited finite algorithm.

Primary algorithm and theorem:
[GLS, The ellipsoid method and its consequences in combinatorial optimization,
Combinatorica 1 (1981), Sections 1--3, Theorems 2.4 and 3.1](https://ir.cwi.nl/pub/10046/10046D.pdf).
This is a standard algorithmic import, not a claim of a new optimizer.

Here are the precise complexity inputs to that import. Let B be the total
binary encoding length of the rational affine data, center and objective,
let h=max(mn,ab,a), and put

    alpha=1+ceil log_2[16 max(2,R)^2/(min(1,r)*min(1,e))].

The rounded ellipsoid iteration count is O(M^2 alpha), with polynomially many
bits in B,M,alpha per query; its Section 2 uses a rounding precision proportional
to its iteration cap. Each query makes at most four Hermitian PSD tests of
orders at most h (or 2h after realification), plus scalar comparisons.
Affine evaluation, rational LDL, witness lifting and construction of the
separating row are polynomial in M,h and query/data bit length. Therefore the
entire bit-operation and storage bounds are

    poly(M,h,B,alpha),                                 (8)

with the fixed polynomial supplied by that specified rounded algorithm and
schoolbook/fraction-free rational linear algebra. There is no unspecified
separation subroutine left. In particular the precision dependence is
log(1/e), not 1/e; the numerical magnitudes enter through encoding length and
log R. We do not invent a tight degree or claim an interior-point runtime.
The published rounded algorithm, not a floating solver's success flag, is
the deterministic termination contract on every rational input.

## 4. Explicit error conversion and exact rational TP repair

Choose e as specified below and run (7). Let C=C(u_y), so Tr_n C=I exactly.
The distance guarantee and (4) give lambda_min(C)>=-aC, with aC=2n e.
Return

    Cphys=(C+2aC I_(mn))/(1+2n aC).                    (9)

This is exactly rational and TP, and

    Cphys >= [aC/(1+2n aC)] I.

Its floor is generated by the learner, not assumed for an unknown source.
Since Tr C=m and the total negative eigenvalue mass is at most mn aC,
||C||1<=m+2mn aC. Directly from (9),

    ||Cphys-C||1 <=4mn aC=8mn^2 e.                    (10)

Thus half-diamond displacement of its map is at most 4mn^2 e. For recovery
the same bound applies after composition with the physical Ntilde; complete
norm contractivity supplies this without an extra payload-dimension factor.

The near-feasible epigraph has

    Z +/- [L(C)-J0] >= -aZ I,   aZ=(2+2n ell)e,
    Tr_b Z <= t_y I + aT I,     aT=(1+2b)e.

Replacing Z by Z+aZ I proves

    half ||map_(L(C)-J0)||diamond
       <=t_y/2 + [(1+4b+2bn ell)/2]e.                 (11)

This is a proof of the objective bound for the possibly nonphysical C; it
does not label C physical. Combining (7),(10),(11) gives repaired objective
gap at most

    [1+(1+4b+2bn ell)/2+4mn^2]e.

For requested slack sigma use the entirely rational choices

    W=2+4b+2bn ell+8mn^2,
    e <= min{r/4, 1/(8n^2), sigma/(4W)}.              (12)

A largest dyadic satisfying (12) suffices. The actual bound is strictly below
sigma, leaving conservative slack. Apply sigma=xi to projection, then
sigma=zeta to recovery. The first returned service is RATIONAL, so the second
SDP retains rational coefficients; no matrix-square-root algebraic field is
smuggled into the optimization input.

Exact rational PSD and TP verification of (9) is performed before returning.
A practical differently capped solver may return UNKNOWN, but it must not
claim (7); its fallback/abort probability needs a separate outer ledger.
The stated rounded-ellipsoid algorithm itself has the deterministic finite
cap (8), and hence contributes no artificial statistical failure mass.

### Optional interface for a solver that does not preserve TP coordinates

If lambda_min(C)>=-a and ||Tr_n C-I||op<=a, root's shift/normalization repair
C1=C+aI, P=Tr_n C1, C2=(P^-1/2 tensor I)C1(P^-1/2 tensor I) has
||C2-C||1<=5mn a when (n+1)a<=1. Indeed
I+(n-1)a I<=P<=I+(n+1)a I, so P^-1/2<=I and
||P^-1/2-I||op<=(n+1)a/2; expansion of the two-sided product proves the bound.
This is a valid alternative but is NOT needed by (9), which keeps the
second SDP rational without a new inverse-square-root representation.

## 5. Bit lengths after the two optimizations

For projection,

    M1=p^2(k^2-1)+(pk)^2+1,       h1=pk.

For recovery,

    M2=k^2(p^2-1)+p^4+1,          h2=max(kp,p^2).

The basis coefficients have entries in {0,+1,-1,+i,-i}; (2) adds only rational
entries of Jtilde. The explicit centers, radii, epsilons and repairs require
O(B_in+log(pk)+log(1/sigma)) precision bits apart from the rounded solver's
fixed polynomial output bound. Hence the first output length B1 is polynomial
in p,k,B_in,log(1/xi). Composition coefficients are rational products/sums
with polynomial length in B1,p,k, so the second call gives B2 polynomial in
p,k,B_in,log(1/xi),log(1/zeta). Standard rational arithmetic is charged for
both calls. No exact optimum or algebraic eigenbasis must be encoded.

If a nonrational trusted controller is approximated when producing Jhat, its
signed-map approximation error must be certified separately, e.g. a Choi
trace-norm error epsilon_J contributes epsilon_J/2 to eta in (1). A floating
matrix handed to this algorithm without rationalization/error accounting is
not the specified input contract.

## 6. Finite physical decoder synthesis, with a specified gate interface

Only the final k->p decoder is physically implemented; projecting the service
does not require building a source simulator. Import the already received
known-Choi/Kraus/Stinespring interface from
ordinary_local_mixed_gauge_cptp_erm_addendum_20261028.md, Section 1, and the
finite universal gate construction from
single_copy_pair_pauli_finite_operation_budget.md, Sections 3--4.
Here we instantiate its dimensions and precision; no acquisition statement
from either source is imported.

Let S=kp. Columns of sqrt(C_R), unvectorized, give at most S Kraus operators
and an exact-reference isometry from k dimensions into p times S dimensions.
It is not necessary to expand the exact algebraic square root into a large
algebraic-number representation. Compute it to certified accuracy by the
received gap-free finite matrix procedure. The following explicit QR
construction supplies the completion; no quantitative completion theorem is
silently imported from the earlier manuscripts. No unknown environmental
dilation is inverted.
For the exactly rational unitary Jacobi basis, use Section 2 of
ordinary_one_sided_effect_finite_positive_cost_rounding_20261028.md on
C_R/(2k)<=I/2, rescaling its requested residual afterward. Only its known
matrix diagonalization primitive is imported, not its effect-rounding or
statistical conclusions. Exact rational unitarity is important when taking
the square root of the diagonal approximation.

For explicit matrix tolerances, let

    D=2^ceil(log_2 p) * 2^ceil(log_2(kp)) <=4kp^2,
    q=log_2 D,
    eW=nu/(64D),
    delta_square=eW^2/(32S).

Certified diagonalization at operator residual delta_square, followed by
clipping its diagonal approximants at zero, changes the PSD matrix by at most
2delta_square. The square-root Holder bound therefore costs at most eW/4
in Frobenius norm. Compute each scalar square root within eW/(8S), and
allocate a TOTAL Frobenius error at most eW/8 to subsequent matrix arithmetic.
The resulting Frobenius factor error is below eW.
This uses the gap-free square-root Holder bound, not 1/lambda_min(C_R).
Reshaping preserves Frobenius norm. Call the resulting rational D-by-k
matrix A; padding by zeros is understood. If W is the exact-reference
isometry, then ||A-W||F<=eW and A has singular values in [1-eW,1+eW].

### Explicit phase-safe isometry completion and its precision

Perform row Givens QR on A, processing columns in order. In the remaining
rows of each current column, select a largest-magnitude entry by certified
interval arithmetic, swap it to the current diagonal position, and eliminate
the lower entries with the unitary

    G(a,b)=[[conjugate(a),conjugate(b)],[-b,a]]
                         /sqrt(|a|^2+|b|^2).

It maps (a,b) to (sqrt(|a|^2+|b|^2),0), fixing a positive diagonal phase.
A final single-entry phase is treated the same way if no lower row remains.
Previous columns are unaffected because their entries in the active rows
are zero. If U is the product of these row unitaries, then

    U A=E R,     Q=U^dagger E,      A=Q R,

where E embeds k coordinates into D, Q is an isometry and R is upper
triangular with positive diagonal. Thus U^dagger is an explicit completion
of Q; no continuity of an arbitrarily chosen orthogonal complement is used.

For completeness, its error bound is elementary. Set F=A^dagger A-I.
Then ||F||F<=(2+eW)eW<=3eW<1/8. For the positive Cholesky factor
R=I+H, the identity F=H+H^dagger+H^dagger H gives
||H||F<=||F||F+||H||F^2: for upper triangular H with real diagonal,
||H+H^dagger||F>=||H||F. Along the positive Cholesky homotopy
I+tF, H starts at zero and cannot cross norm 1/2, because at that crossing
1/2<=1/8+1/4 would be false. Hence ||H||F<=2||F||F<=6eW.
It follows that

    ||Q-W||F <= ||Q-A||F+eW = ||I-R||F+eW
                 <=7eW<nu/8.                          (14)

The normalization/pivot floor is known, not a new spectral assumption.
Every residual column norm in QR is at least sigma_min(A)>=1-eW>1/2:
the corresponding Schur complement of A^dagger A is bounded below by
(1-eW)^2 I. Some active entry therefore has magnitude at least
1/(2sqrt(D)). Interval comparison of squared magnitudes to error at most
1/(64D^2) selects a pivot with a certifiable magnitude at least 1/(4D).
After a pivot is installed, elimination can only increase its magnitude.
All square-root/division denominators are consequently bounded below by
1/(4D), and the unitaries and active matrix entries have bounded norm.
There is no division by a tiny Choi eigenvalue or by an uncertain zero entry.

There are O(Dk) rotations and O(Dk^2) scalar arithmetic operations for this
QR program. To make the bit claim concrete, take L=1000D^3 as a conservative
upper bound on its scalar-operation count and V=1000(D+1)^3 as a conservative
local error-amplification bound on its additions, multiplications,
normalizations and square roots on the certified domains. If B_A is the
rational input bit bound for A, a sufficient interval working precision is

    B_work >= B_A + ceil[(L+1)log_2 V]
                     +ceil log_2[1024D max(1,G_B)/nu]+10.       (15)

Here G_B is the finite elementary-target count of the chosen decomposition
below. Per-operation roundoff at that precision, propagated through at most
L operations, is smaller than both the pivot-selection tolerance and the
required final target-matrix tolerance. Comparisons need not resolve ties:
only the certified lower pivot bound matters. Scalar square roots use
rational bisection to the prescribed interval, not exact algebraic-number
field expansion. This intentionally loose precision is polynomial in D,
B_A and log(1/nu); it may be much worse than backward-stable numerical QR.
It establishes the finite bit bound without assuming an unstated stable
completion oracle.

A dense D-dimensional unitary uses O(D^2) known two-level targets.
Gray-code/two-level reduction to one-qubit rotations and CNOT has a
conservative O(q^3) elementary-target overhead per two-level target.
Let G_B be the explicit target count emitted by that fixed finite decomposition;
G_B=O(D^2 q^3). A value-independent padded count is computed from D,k and
the fixed decomposition schedule before target arithmetic, avoiding any
circular precision choice. For q=0 the decoder is trivial. Allocate operator error
nu/(4 max(1,G_B)) each to target arithmetic and fixed-gate approximation.
The gate-by-gate hybrid then costs at most nu/2 in unitary norm.
Equation (15) covers QR, not all new arithmetic in the Barenco reduction.
Its additional known 2-by-2 roots/phases/Euler formulas are evaluated to
their assigned target tolerance with the following finite guards. For a
unitary root, one of the four phases zeta in {1,i,-1,-i} has
sigma_min(I+zeta U)>1/2, with constant selection slack: two eigenvalues
cannot lie near all four possible cuts. Certify such a chart by constant-
precision 2-by-2 singular-value bounds. The Cayley matrix
T=-i(zeta U-I)(zeta U+I)^-1 is Hermitian with norm at most four, and

    sqrt(zeta U)=(I+iT)(I+T^2)^-1/2

uses a positive matrix with spectrum in [1,17]. Multiply by the known
scalar sqrt(zeta)^-1 to retain the correct root of U, INCLUDING its
controlled relative phase. These operations admit certified polynomial-bit
evaluation without identifying an eigenbasis or resolving an eigenvalue gap.
For phase/Euler coordinates use a largest-entry chart; a remaining entry
below its allocated target tolerance can be omitted with that matrix-norm
debit, while every retained phase division is bounded below by an inverse
polynomial in the target tolerance. The exact finite formula/decomposition
schedule is polynomial in q. Interval propagation therefore adds
poly(q,log(G_B/nu),B_work) bit work and precision, not an inverse-accuracy
search or an assumed exact trigonometric oracle. These additional target
errors are included in the first nu/(4G_B) allocation above.

Choose the inverse-closed finite Clifford+T gate interface, with CNOT, and
the standard constructive Solovay--Kitaev compiler (its fixed coarse net is
precomputed once and paid). The fully decomposed primitive one-qubit gates
are normalized to SU(2); their omitted scalar phases contribute only one
physically irrelevant phase to the entire circuit. Relative phases of
controlled/two-level gates are resolved by the Barenco decomposition BEFORE
this normalization. The operator-error comparison is consequently up to
that single global phase, which has no channel effect. For known targets its length overhead
is O(log^3.97(G_B/nu)). The often quoted O(log^2.71(G_B/nu)) recursion work
uses a compressed circuit representation; explicitly writing the gate list
costs at least its O(log^3.97(G_B/nu)) length. Finite arithmetic costs on
the required precision-bit operands are also paid. Thus a concrete
conservative final gate bound is

    O(D^2 q^3 log^3.97(max(2,D^2 q^3/nu))).            (13)

Routing/connectivity and trusted storage time are additional physical costs.
The output and environment use q qubits total; at most
2 ceil(log_2 p) additional initialized qubits beyond the padded k-dimensional
input suffice. Discard the environment after the actual finite unitary
circuit. If p is not a power of two, additionally apply the known CPTP output
map that keeps the first p levels and sends any padded-level leakage to a
fixed logical state; it is identity on the target output and cannot amplify
the discrepancy. Compute the predicate "basis index<p" reversibly into one
flag and measure only that flag, not the in-code basis label; reset the bad
branch to zero. A discarded environment qubit can be reset and reused for
the flag, so the peak register bound is unchanged. The known integer
comparison has polynomial-in-q exact classical reversible/Clifford+T control
cost, included in the gate ledger. If physical control inaccuracies for this
cleanup are separately modeled, assign half-diamond error at most nu/8.
The comparison can use a disjoint-prefix threshold test with a flag and
Toffoli-ladder scratch, all borrowed from reset environment qubits; at most
ceil(log_2 p) such clean qubits are needed, whereas the environment has
ceil(log_2(kp)) available. No uncharged ancilla-free multicontrol primitive
is presumed.
Every returned implementation is CPTP, not a rounded non-isometry.
The target-arithmetic and gate errors total at most nu/2; together with
(14) the isometry error is below 5nu/8. Isometry operator error gamma
implies channel diamond error at most 2gamma; including the optional
cleanup debit still gives half-diamond error below nu,
so the half-diamond debit in (1) is nu.

The standard compilation facts are credited to
[Barenco et al.](https://arxiv.org/abs/quant-ph/9503016) and
[Dawson--Nielsen](https://arxiv.org/abs/quant-ph/0505030).
These are known dense-control algorithms, not cheap arbitrary-channel
hardware or a claim to have delivered a pulse-level circuit.

### Finite-bit guard for the single-qubit compiler

Dawson--Nielsen explicitly does not analyze finite-precision arithmetic.
Consequently its quoted real-arithmetic recursion count alone is NOT our
bit-complexity argument. The following conservative guarded version supplies
that missing part; it is not claimed to have been executed.

Take eta_0=2^-64 and a fixed inverse-closed-gate coarse net with covering
radius eta_0/8. It is constructed/verified once by finite word enumeration
against a finite rational-quaternion covering mesh, and paid as a fixed
gate-set-dependent preprocessing/storage constant. Universality ensures
termination. Interval comparisons with strict covering slack select a
base word within eta_0; there is no exact nearest-word decision.
Let b_0=64, b_j=floor(3b_(j-1)/2)-12 and eta_j=2^-b_j. Then

    4096 eta_(j-1)^(3/2) <= eta_j
                           <=8192 eta_(j-1)^(3/2).

At level j first recursively approximate the target U within eta_(j-1),
giving an actual gate word S and residual Delta=U S^dagger near identity.
Evaluate that residual with interval error at most eta_j/1024.
If its certified norm distance from I is at most eta_j/2, omit correction.
Otherwise the comparison intervals certify distance at least eta_j/4.
Overlapping decision thresholds, rather than an equality test at a sharp
boundary, provide this guarded alternative.

Write the principal near-identity logarithm Delta=exp(i h.sigma).
It has ||h||<=2eta_(j-1); on the nontrivial branch ||h||>=eta_j/8 after
the allocated residual-approximation allowance. Choose a coordinate axis e
least aligned with h, using interval comparisons with fixed relative slack.
The selected cross product can be certified to have length at least ||h||/2.
Put

    a=(h cross e)/||h cross e||,
    f=sqrt(||h||/2)*a,
    g=-sqrt(||h||/2)*(h/||h|| cross a),
    V=exp(i f.sigma),    W=exp(i g.sigma).

The Pauli commutator identity gives
[i f.sigma,i g.sigma]=i h.sigma. Expansion of the four exponentials through
degree two, with exponential-series remainder, gives

    ||V W V^dagger W^dagger-Delta||
           <=100 ||h||^(3/2)

in the fixed small neighborhood used here. Both V,W are within
sqrt(||h||/2) of I. If their recursive gate approximants have error
eta_(j-1), subtraction of identity in the conjugations bounds the additional
commutator error by 4 eta_(j-1)*sqrt(||h||/2)+2 eta_(j-1)^2.
These terms total less than 512 eta_(j-1)^(3/2). Finite interval evaluation
and rational unit-quaternion rounding of the near-identity V,W are allocated
total residual error at most eta_j/64. The enlarged dyadic recurrence leaves
ample slack, proving inductively that the actual word has error at most eta_j.
Approximate balanced commutators suffice; no singular exact axis-alignment
formula is necessary.

All divisions on the nontrivial branch have denominator at least a fixed
power of eta_j. The principal logarithm is in a fixed analytic neighborhood
of identity; square roots and the sine/cosine formulas for the exponentials
are evaluated by rational interval series/bisection. Near-identity unit
quaternions can be rounded EXACTLY onto the unit sphere by the rational
stereographic chart whose denominator is bounded away from zero. Obtaining
the stated eta_j/64 error therefore requires polynomially many precision bits
in log(1/eta_j), not reciprocal-eta_j arithmetic steps. Residuals below the
guard are never normalized. Fixed-dimensional finite-chart comparisons avoid
an unresolved zero or nearly antipodal direction.

Stop when eta_j<=tau, where tau is the required per-primitive tolerance.
The depth is O(log log(1/tau)), the number of recursive nodes is at most
2*3^j and the expanded word length is O(5^j)=O(log^3.97(1/tau)).
Multiplying actual word matrices to certified residual precision, even
recomputing rather than caching them, and the guarded scalar operations
take poly(log(1/tau)) bit operations. Input-target evaluation uses the
already paid precision mechanism (15). This proves a conservative polynomial
BIT bound; it does not identify that polynomial with the ideal-arithmetic
2.71 exponent. Expanded gate-list writing and physical execution pay every
gate in (13).

## 7. Comparator transfer and records

The true channel is feasible in the first optimization, hence
half ||Ntilde-N_true||diamond<=2eta+xi. Each physical decoder's loss changes
by at most that amount between these two services. Applying that comparison
twice, then the second optimization slack and physical compiler debit, proves
(1). No spectral, unitary-noise, Pauli, or Bell-to-diamond reduction is used.

This endpoint module works on every finite rational input and does not need
an extra optimization-success probability. In the signed-core application,
statistical bad histories and core-test abstention remain separate:
beta, alpha_core and any genuinely introduced capped-solver abort mass must
be charged by the outer theorem. One complete implementation debit transfers
the actual RECORD-AVERAGED deployed channel guarantee; it does not automatically
bound the average of record-conditioned diamond norms. If nu is already
included in that whole-process debit, do not add it again.

## 8. Evidence and receiving status

Proofs and constants above are construction claims pending independent review.
The companion accessible_endpoint_exact_checks.py executes rational PSD
separation, interior-ball directions, both repairs, exact Kraus/TP certificates,
accuracy-budget inequalities and specialized Pauli endpoint optimizers.
The latter return solutions with an all-CPTP optimum certificate: measuring
any physical service's normalized Choi matrix in the Bell basis gives a
probability vector, lower-bounding its distance from the signed Pauli weights
by their l1 distance from the simplex. Renormalizing their positive part
attains the minimum. For recovery the four-Pauli entanglement-fidelity sum
rule bounds every CPTP decoder by the largest Pauli weight, attained by its
inverse. This is a genuinely executed restricted solver, not an execution
of generic GLS optimization and not a decoder-menu comparator theorem.
No source calls, hardware execution, generic ellipsoid solve or compiled
deployment is claimed by this manuscript.
The named received compiler primitives are reused only at their finite
known-matrix/known-control interface. Primary GLS finite-bit optimization
supplies the remaining algorithmic solver mechanism, not a free optimization
oracle or a hidden-model QE reduction.
