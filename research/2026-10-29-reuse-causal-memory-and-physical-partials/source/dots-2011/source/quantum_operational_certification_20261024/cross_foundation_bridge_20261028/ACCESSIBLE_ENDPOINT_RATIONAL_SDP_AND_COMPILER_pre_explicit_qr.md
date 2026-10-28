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
known-Choi/Kraus/Stinespring and stable known-isometry synthesis machinery from
ordinary_local_mixed_gauge_cptp_erm_addendum_20261028.md, Section 1, and the
finite universal gate construction from
single_copy_pair_pauli_finite_operation_budget.md, Sections 3--4.
Here we instantiate its dimensions and precision; no acquisition statement
from either source is imported.

Let S=kp. Columns of sqrt(C_R), unvectorized, give at most S Kraus operators
and an exact-reference isometry from k dimensions into p times S dimensions.
It is not necessary to expand the exact algebraic square root into a large
algebraic-number representation. Compute it to certified accuracy by the
received gap-free finite matrix procedure and use stable polar/QR completion
of the known isometry. The isometry's singular values equal one, so this
normalization has a constant conditioning floor even when C_R has tiny
eigenvalues. No unknown environmental dilation is inverted.

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
Reshaping preserves Frobenius norm. The approximate isometry has singular
values in [1-eW,1+eW]; polar correction changes it by at most eW in operator
norm, so its distance from the exact-reference isometry is at most 2eW.
The imported certified completion/synthesis routine may spend the remaining
matrix budget to achieve a unitary-reference error at most nu/2.
All required matrix precision bits are polynomial in
B2,S,log D,log(1/nu); in particular delta_square costs only twice the accuracy
bit count, not an inverse-nu number of spectral iterations.

A dense D-dimensional unitary uses O(D^2) known two-level targets.
Gray-code/two-level reduction to one-qubit rotations and CNOT has a
conservative O(q^3) elementary-target overhead per two-level target.
Let G_B be the explicit target count emitted by that fixed finite decomposition;
G_B=O(D^2 q^3). For q=0 the decoder is trivial. Allocate operator error
nu/(4 max(1,G_B)) each to target arithmetic and fixed-gate approximation.
The gate-by-gate hybrid then costs at most nu/2 in unitary norm.

Choose the inverse-closed finite Clifford+T gate interface, with CNOT, and
the standard constructive Solovay--Kitaev compiler (its fixed coarse net is
precomputed once and paid). For known one-qubit targets its length overhead
is O(log^3.97(G_B/nu)) and classical compiling time is
O(log^2.71(G_B/nu)) per target, plus finite target arithmetic. Thus a concrete
conservative final gate bound is

    O(D^2 q^3 log^3.97(max(2,D^2 q^3/nu))).            (13)

Routing/connectivity and trusted storage time are additional physical costs.
The output and environment use q qubits total; at most
2 ceil(log_2 p) additional initialized qubits beyond the padded k-dimensional
input suffice. Discard the environment after the actual finite unitary
circuit. Every returned implementation is CPTP, not a rounded non-isometry.
Unitary operator error at most nu implies channel diamond error at most 2nu,
so the half-diamond debit in (1) is nu.

The standard compilation facts are credited to
[Barenco et al.](https://arxiv.org/abs/quant-ph/9503016) and
[Dawson--Nielsen](https://arxiv.org/abs/quant-ph/0505030).
These are known dense-control algorithms, not cheap arbitrary-channel
hardware or a claim to have delivered a pulse-level circuit.

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

At initial save, proofs and constants above are construction claims pending
independent review. Executable checks are being added separately. They must
distinguish exact separation/repair/fixture certificates from actually running
the generic rounded ellipsoid algorithm. No source calls, hardware execution,
generic ellipsoid solve or compiled deployment is claimed by this manuscript.
The named received compiler primitives are reused only at their finite
known-matrix/known-control interface. Primary GLS finite-bit optimization
supplies the remaining algorithmic solver mechanism, not a free optimization
oracle or a hidden-model QE reduction.
