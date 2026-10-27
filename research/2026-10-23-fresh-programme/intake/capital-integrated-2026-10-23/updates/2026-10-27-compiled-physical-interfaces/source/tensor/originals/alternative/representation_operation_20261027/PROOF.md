# Exact gauge-free recognition and modular contraction

This is a complete construction at the generic scope below. It uses known
heterogeneous parity/matchgate gauges and Fisher/FKT contraction. It does not
claim a new tractability class, historical priority, general tensor contraction,
practical speedup or a civilisation-level result. Independent parent and
ordinary-comparator contributions are credited in REPORT.md/SOURCES.md.

## Operation and admitted inputs

Input is a closed loopless planar trivalent graph, explicit cyclic PORT order
at every vertex, and8 rational coefficients T_v[i,j,k] per vertex. Parallel
edges and disconnected components are allowed. No gauge, CP factors, hidden
spin variables, global algebraic field or contraction value is supplied.
Contraction is bilinear along each edge, with no complex conjugation.

Require every local2x2x2 hyperdeterminant nonzero and every CP edge-pairing
entry nonzero, as defined below. Among these generic inputs, a local exact
predicate recognizes PRECISELY the instances admitting compatible independent
edge bases making every vertex an even/odd parity tensor (a ternary matchgate).
The compiler returns UNKNOWN outside this admitted class or upon exhausting a
declared work budget; failure does not imply hardness or absence of some other
tractable representation.

On the admitted class, unlimited prime search terminates in deterministic
polynomial BIT cost. It returns the exact rational partition/contraction Z and,
if Z!=0 and requested, the normalized weights of each ORIGINAL edge bit. For
nonnegative tensors these are probabilities. Signed tensors can yield negative
or >1 weights. At Z=0 normalized weights are undefined: individual pin
numerators need not vanish. Self-loops, higher arity/bond dimensions and noisy/
approximately tractable tensors are not covered.

## 1. Local quadratic CP recovery

Slice T on its first leg into2x2 matrices T0,T1. Nonzero hyperdeterminant means
the determinant pencil has distinct projective roots. Choose lambda from
{0,1,-1} for which A=T0+lambda*T1 is invertible, possible because a nonzero
quadratic cannot vanish at3 distinct points. Put M=T1*A^-1. Its eigenvalues
mu0,mu1 are distinct and lie in Q[sqrt(delta)], delta=(tr M)^2-4det M!=0.

Let U be an eigenvector matrix and V^T=U^-1*A. Then

    A_0=[[1-lambda*mu0,1-lambda*mu1],[mu0,mu1]], A_1=U, A_2=V,
    T[i,j,k]=sum_(s=0,1) A_0[i,s] A_1[j,s] A_2[k,s].              (1)

The tensor slices reconstruct because A=UV^T and T1=U diag(mu)V^T.
All three factor matrices are invertible. If M01!=0, eigenvectors
(M01,mu_s-M00) suffice; otherwise if M10!=0 use(mu_s-M11,M10).
If both offdiagonals vanish, use the rational coordinate eigenvectors and
rational diagonal eigenvalues. No floating eigensolver is needed.

Any rank2 CP factorization with these nonsingular legs diagonalizes the same
simple-spectrum pencil. Therefore it differs only by exchanging its two
summands and column scalings with product1 across the3legs for each summand.
This is standard CP/pencil structure, not a new tensor factorization theorem.

Use the FORMAL quadratic etale algebra Q[z]/(z²-delta), represented by two
rationals. No integer discriminant factorization or global compositum is built.
If delta is a rational square the algebra splits into two branches; the chart
is invertible in both and the conditions tested below are label invariant.
Inversion requires nonzero rational norm a²-delta*b², so split zero divisors
are detected rather than divided by.

## 2. Intrinsic local compatibility predicate

For edge e=vw, its CP pairings are W_e=A_v,e^T A_w,e, a2x2 invertible matrix.
Assume all4entries nonzero. Let

    q_w,e(x)=det(T_w contracted with x on leg e).

This is a RATIONAL binary quadratic. Directly from(1),

    q_w,e(x)=det(A_w,other1)det(A_w,other2)
                  (x^T A_w,e[:,0])(x^T A_w,e[:,1]).             (2)

Hence for incidence(v,e),

    r_v,e² = W10*W11/(W00*W01)
            = q_w,e(A_v,e[:,1])/q_w,e(A_v,e[:,0]).              (3)

The opposite endpoint has s²=W01*W11/(W00*W10). All edge-entry nonzero tests
can therefore be made by rational norms of q evaluations in ONLY v's local
quadratic algebra. No neighboring/global algebraic roots are needed.

Define beta_v=product_(e incident v) r_v,e². Column rescaling at v changes
these ratios by squares whose product is1; neighbor column scales cancel in
(2). Exchanging v's CP summands inverts beta_v. Thus beta_v=1 is intrinsic.
Test it by equality of the products of the3q numerators and denominators,
coefficientwise in v's two-dimensional etale algebra. This uses a constant
number of bounded-degree operations per vertex and needs no nonlinear linked
system with a growing number of gauge variables.

## 3. Sufficiency, necessity and odd zero

Choose r² as in(3), and s=W11/(W00*r). Then

    r*s=W11/W00, r/s=W10/W01.

Multiplying CP column0 by r at v and by s at w changes this edge to

    diag(r,1) W diag(s,1)=[[a,b],[b,a]], a=W11,b=r*W01.           (4)

The compensating COPY coefficient at vertex v is [1/g_v,1], where
g_v=product_(e incident v) r_v,e. If beta_v=1, g_v=+1 or-1. Flipping BOTH
edge-root signs changes g at its two endpoints. A spanning-tree solve sets
all g=1 precisely when their product on the component is+1. If it is-1, a
residual signed vertex remains; global spin complement leaves all symmetric
edges invariant and changes the vertex-weight product's sign. The entire
component contraction is EXACTLY ZERO. This branch is not an unknown sign.

Necessity at the stated generic scope: pull the parity involution diag(1,-1)
through any hypothetical compatible edge bases and then into the CP factors.
CP uniqueness implies that its three leg actions either preserve the two
summands or exchange them all. Preservation would give opposite eigenvalues
on the two summands because there are3 traceless legs, so the tensor cannot
be a parity eigenvector. Thus each CP leg action has the form

    S=[[0,r],[1/r,0]].

Compatibility across the bilinear edge requires S_v^T W S_w=W. Its entries
give the displayed product/ratio equations, whose squares are(3). Each vertex's
parity eigenvalue is±1, giving beta_v=1. Conversely(4), sign neutralization and
Hadamard transform yield even/odd parity vertices; nonsingular diagonal edge
weights can be absorbed into endpoints without changing parity. Thus the
local predicate is complete for compatible independent-edge parity gauges
within the admitted nondegenerate/nonzero-pairing class. It does not classify
gadgets, graph changes, all tractable networks or degenerate tensors.

## 4. One common finite field of degree TWO

At any odd good prime p, every rational quadratic pencil splits in F=Fp²,
so all local factors can be recovered in this SAME field. No prime at which
all characteristic-zero discriminants split in Fp is sought.

Every edge radicand(3) is also a square in F. One proof that allows CP column
normalizations: q has Fp coefficients. When local CP directions split in Fp,
choose them there; r² belongs to Fp and is square in Fp². Otherwise Frobenius
exchanges directions, u0^p=c*u1 and u1^p=d*u0. Applying Frobenius again gives
c^p*d=1, so d/c=1/Norm(c) belongs to Fp. Homogeneity of q gives

    (r²)^p=(d/c)²/(r²),  Norm_(F/Fp)(r²)=(d/c)².

For x in F*, x is square exactly when its norm is square in Fp, by
x^((p²-1)/2)=Norm(x)^((p-1)/2). This proves the claim. The canonical pencil
chart even has pure component swaps without scales. The lemma does NOT need
beta=1. Then r,s, all signs/symmetric weights and FKT calculations remain
in Fp². Root/label choices can be made independently per vertex; they simply
relabel hidden spins and cannot require one characteristic-zero embedding.

fields.py uses exact finite arithmetic and Tonelli-Shanks. A retained Quartic
prototype is not the compiler field: QuadraticFinite has TWO coordinates and
is the actual evaluator. Every CP tensor identity, edge symmetry, COPY balance
and final base-field cancellation is checked. Output outside Fp is rejected.

## 5. Established Fisher/FKT evaluation with explicit signs

After sign neutralization each edge is M_e=[[a,b],[b,a]]. Under orthogonal
Hadamard its eigenweights are w0=a+b,w1=a-b. The COPY vertex transforms to
1/sqrt(2) times even parity. A closed trivalent graph has EVEN vertex count n,
so the scalar over vertices is2^(-n/2), rational. Invertible CP legs imply
invertible M_e, hence w0,w1!=0.

Replace each vertex by a triangle with internal weights1. Selecting an external
dimer edge means original state0; not selecting means state1. An even active
configuration leaves0or2 vertices to match internally in each triangle, in
exactly one way. Therefore

    Z=2^(-n/2)*product_e(w1_e)*Z_PM(external weights x_e=w0_e/w1_e). (5)

This is standard Fisher/FKT, not a new contraction algorithm. The supplied
rotation is expanded into an explicit Fisher rotation; Euler characteristic2
is checked per component. Clockwise-odd face equations, omitting one face per
component, are solved over F2 and checked. The known all-external perfect
matching fixes the Pfaffian's common sign combinatorially: its arc-crossing
permutation sign times its orientation signs. Thus no floating determinant
square root, sign guess or reference partition value is supplied.

The exact Pfaffian elimination pivots on a nonzero entry, accounts for row/
column swaps and uses the skew Schur complement. It gives0if no pivot exists.
The actual evaluator/orientation design is reused with credit from the ordinary
comparator backend; port-ID/multicomponent and insertion integration are
explicit additions. Sign/matrix/prefactor obligations were independently checked.

## 6. ORIGINAL edge-bit weights, not hidden spin occupancy

Let P_b project the shared original edge coordinate onto bit b. Its CP insertion
is E_raw=A_v,e^T P_b A_w,e. Apply the SAME incidence factors and tree-root sign
choices as used in(4): E=diag(r,1)E_raw diag(s,1).

When the neutral component is even, simultaneous hidden spin complement leaves
the surrounding model invariant. Its contraction therefore depends only on
(E+XEX)/2=[[alpha,beta],[beta,alpha]], with alpha=(E00+E11)/2 and
beta=(E01+E10)/2. This is a directional derivative of Z with respect to that
edge's a,b. The odd insertion part cancels; equating an original bit pin with
a Fisher occupancy would be wrong.

Write K for the oriented Fisher matrix and sigma for its fixed matching sign.
For Z mod p!=0, K is invertible. Define

    h=x_e*arrow_e*(K^-1)[external_end,external_start].

The derivative identity dPf(K)/dK_ij=Pf(K)*(K^-1)_ji gives the original pin
numerator divided by Z as

    ((alpha+beta)/w0)*h + ((alpha-beta)/w1)*(1-h).                 (6)

The second term includes the derivative of product(w1) in(5); dropping that
prefactor is incorrect. This is a field quantity, not automatically a positive
hidden probability. Multiplying(6) by Z yields a pin numerator for CRT. Both
original pins sum to Z, checked exactly per prime and after reconstruction.
A dense inverse gives all original edge quantities in O(n³) field operations,
not a separate inverse for each bit.

If an odd-parity component forces Z mod p=0, or an even model has a modular
cancellation, preserve the partition residue but do not invert K for normalized
weights. Individual original pin numerators can be nonzero even at exact Z=0.
The compiler returns normalized outputs UNDEFINED there, never asserts all
unnormalized pins are0. At a nonzero rational Z, primes dividing its cleared
integer numerator are skipped only for marginal reconstruction and charged
below. Signed inputs yield algebraic marginal ratios/weights; the probability
interpretation additionally requires nonnegative original tensors.

## 7. Original-input height and sound CRT

Clear denominators separately at each vertex: T_v=t_v/D_v, all entries of t_v
integer, D_v>0. Let B_v=max_x|t_v[x]| and m=|E|. The ORIGINAL cleared contraction
and each ORIGINAL edge-pin numerator satisfy

    |Z_int|, |N_(e,b),int| <= H=2^m*product_v B_v.                 (7)

There are2^m assignments, and each term has absolute value at most product B_v.
Pins restrict the sum, so the same bound applies. If a vertex is identically0,
partition0is known directly; normalized outputs are undefined. The original
answer is Z_int/product D_v, and normalized weights are N_int/Z_int.

Accumulate distinct verified prime residues by integer CRT. A modulus M>2H
uniquely determines each signed integer in[-H,H]. Center the representative,
check its height and original pin-sum identities, then divide. This bypasses
ALL characteristic-zero gauge intermediate heights/degrees.

Output soundness does not require inferring a characteristic-zero class from
finite modular tests. Every selected prime executes locally checked tensor,
edge and COPY identities, then an exact planar Pfaffian algorithm. Thus even
an accidentally tractable prime supplies the true ORIGINAL contraction residue.
The final residue is checked to lie in the base Fp subfield. Wrong extension
coefficients are not discarded or guessed. Exact local admission is used for
completeness/search guarantees; finite modular success alone is not claimed as
characteristic-zero recognition.

Partition CRT and pin CRT have separate moduli. Valid Zp=0residues enter the
partition CRT. Pin CRT receives only computed nonzero-Zp values. Once partition
M>2H, exact Z_int=0ends with normalized weights undefined. If Z_int!=0, continue
until pin modulus also exceeds2H. In particular a true zero is not followed by
an infinite hunt for nonzero residues.

## 8. Complete deterministic bit/resource accounting

Let L be the total original rational-entry and graph/embedding bit encoding.
Each local decomposition, norm and determinant-quadratic test uses bounded
algebraic degree, constant-size matrices and one local quadratic algebra.
Its rational coefficient bit sizes are polynomial in local input sizes;
summing over the bounded-degree graph is polynomial in L. No factorization of
a discriminant, global compositum or exponentially precise numerical gauge is
hidden. The code constructs a nonzero integer B_bad from nonzero chart/
coefficient numerators/denominators, discriminants and q-evaluation norms.
Its bit length is polynomial in L (indeed linear up to fixed-formula constants).

Outside primes dividing B_bad, the selected characteristic-zero chart reduces
legally, discriminants and all CP edge entries remain nonzero, and beta=1
survives. Independently chosen finite-field CP labels cannot invalidate it.
Every such odd prime>3therefore yields a verified residue. There are at most
floor(log2 B_bad) distinct excluded prime divisors.

log2 H and log2 product D_v are polynomial in L. At most log2 H+O(1) good
primes suffice for a CRT modulus>2H. For nonzero Z_int, at most log2|Z_int|
<=log2 H additional distinct primes divide it and are unavailable to the
marginal inverse. Thus

    bit_length(B_bad)+2*bit_length(H)+4

is a conservative bound on the number of prime candidates required on the
admitted class. For exact zero fewer suffice. A standard bound on the Kth
prime, p_K=O(K log K), makes the numeric sizes of all enumerated primes
polynomial in L. This uses no simultaneous-splitting density assumption, GRH
or unproved deterministic prime finder in a huge interval.

For a simple exact implementation, primes are verified by trial division.
Base-field nonresidues and Fp² Tonelli nonresidues are found by deterministic
scans; worst scan counts are O(p), not free polynomial-in-log(p) oracles.
Because p itself is polynomial in L, those costs are still polynomial in L.
Tonelli-Shanks uses exact finite-field operations. Each evaluation uses
O(n³) operations on O(log p)-bit field elements for the dense Pfaffian and,
when requested/valid, inverse. Orientation/reference sign is acquired once
from the explicit embedding. Dense evaluator memory is O(n²) field elements;
CRT stores O(m) integers of polynomial encoding size. Root setup, bad-prime
search, local recognition, denominator clearing, output reconstruction and
normalization all belong in the cost. No timing advantage follows from an
O(n³) field-operation statement alone.

The shipped default200-prime cap is a practical declared work cap, not the
mathematical completion bound for all encodings. UNKNOWN at that cap is honest.
--unbounded-prime-search implements the terminating algorithm on the admitted
class. Runtime resource/encoding limits still exist. All proofs concern exact
rational inputs; approximating a real/noisy model can destroy beta=1 and is not
covered by an unearned robust error theorem.

## What this establishes and what it does not

The completed operation acquires the representation from raw local tensors;
it does not retrieve a supplied hidden gauge. This can normalize and compute
original edge weights for admitted planar graphical models without constructing
the global algebraic object. Uniform basis recognition, full heterogeneous
linked-ideal discovery, ordinary exact tensor methods and Wick/FKT arithmetic
remain strong comparators with the same inputs and all retained work.

The underlying heterogeneous free-fermion orbit and its Pfaffian evaluation
are established prior. No checked primary source in the bounded search supplied
the identical complete uniform raw-input/bit pipeline, but absence in this
search is NOT novelty proof. A new tractability class, historical priority,
useful non-generated workload, practical comparison win and civilisation-level
advantage remain UNKNOWN / NOT_ACHIEVED. Generated hidden-gauge cases verify
implementation only; their generator/gauges/work are equally available to the
ordinary comparator. The original mission is not declared achieved.
