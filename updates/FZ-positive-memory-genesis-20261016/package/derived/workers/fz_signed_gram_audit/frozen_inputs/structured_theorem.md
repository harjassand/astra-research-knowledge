# Structured signed-GKSL regularization without full-patch depolarization

16 October 2026. Independent construction worker FZ. Producer files were read
only. No nested agents, producer edits, worktree edits, Git operations, or
physical experiments were performed.

## Finding and scope

There is an exact regularization theorem for a *specified finite local error
catalog*. Its cost is controlled by a Pauli Gram matrix on that catalog and
the products needed for its anticommutators, rather than by the Hilbert
dimension of the surrounding patch. It treats signed changes of dissipators,
Hamiltonian drift, and coherent cross terms in jump operators. A positive
lower Gram block and a range condition are indispensable; negative rates are
not presumed positive.

For a catalog of N nonidentity Pauli modes, a fixed deliberate floor of
N Pauli jumps gives a structured signed-error neighborhood of order
nu/N and a coherent Hamiltonian neighborhood of order nu/sqrt(N), where nu
is the allowed local fault-proposal budget. These are not arbitrary
full-patch diamond-norm neighborhoods. When N is polynomial in the number
of patch qubits because the error model has fixed Pauli weight or few known
shapes, there is no factor 2^(-2m) from m spectator/patch qubits. If the
catalog is unrestricted, N=4^m-1 and exponential cost returns.

The exact Pauli Hamiltonian special case was derived independently here,
but the displaced-jump identity is prior art: Shang and Franca,
[arXiv:2604.18533v1, Eq. (4) and the gauge section](https://arxiv.org/html/2604.18533v1).
The general theorem below is a constructive Gram-factorization and Schur
complement calculation. Neither that algebra nor this note establishes
historical originality. Its useful output is a sharply specified candidate
transfer interface, explicit proposal rates, and falsifiers for overstating
the interface.

The memory conclusion is **conditional** on the inherited universal
good-schedule support-recovery interface. This worker did not verify that
interface or any classical lifetime proof. Physical fabrication, calibration,
reservoir/reset costs, 4D geometry, noisy readout, and useful finite-device
advantage remain unestablished.

## 1. Exact local input and deliberate floor

Work on one m-qubit patch, with d=2^m. Let P_1,...,P_N be distinct Hermitian
nonidentity Pauli strings, with phases fixed, and use normalized
Hilbert-Schmidt inner product tr(A^dagger B)/d. Thus I,P_1,...,P_N are
orthonormal. Let gamma_i>=0 and install the actual physical noise

    F_gamma(rho) = sum_i gamma_i (P_i rho P_i-rho),
    Gamma = sum_i gamma_i.                                      (1)

The nominal floor needs only correlated Pauli kicks on the supports of the
listed P_i. It has N listed jump types with total rate Gamma, not d^2
uniformly weighted jump types. Zero gamma_i is permitted in the exact
criterion below.

Specify a local Hermiticity-preserving trace-annihilating error by

    E(rho) = -i[H,rho]
       + sum_ij C_ij (P_i rho P_j - {P_j P_i,rho}/2),
    H = sum_i h_i P_i,       h_i real,       C=C^dagger.        (2)

C need not be positive. For example, a jump replacement J -> J+Delta J
gives a difference of two positive Gram matrices. Add unused catalog modes
as zero rows/columns of C.

Compute the Hermitian rate operator

    K = sum_ij C_ij P_j P_i
      = k_0 I + sum_i k_i P_i,       k_i real,
    k_0 = tr C.                                                (3)

**Catalog obligation:** all nonzero Pauli components of H, of the jumps,
and of K must lie in the stated catalog. Add any missing product modes
before applying the theorem. It is sufficient to include every nonidentity
Pauli product of two jump modes. It is not necessary to close the catalog
under every longer product: the fault envelope later certifies arbitrary
Pauli histories on the whole bounded patch.

Define the N-dimensional objects

    D = diag(gamma_i)+C,       a = -k/2-i h.                    (4)

Only these catalog matrices and Pauli word products enter the test. There
is no d^2 by d^2 Choi matrix to acquire or diagonalize.

## 2. Exact necessary and sufficient proposal criterion

For r>0, the generator G=F_gamma+E is exactly r(Psi-Id) for a CPTP map Psi
if and only if

    D >= 0,
    a belongs to range(D),
    r >= r_min := Gamma + tr C + a^dagger D^+ a.               (5)

D^+ is the Moore-Penrose inverse. If D>0, it is the ordinary inverse.
The conditions include modes outside the original jump span which were
added for (3). If D has a zero mode carrying a component of a, no finite
proposal rate works. Increasing the scalar rate r cannot repair a negative
eigenvalue of D.

The criterion is exact for the fixed G: because Psi=Id+G/r is forced,
allowing a different Kraus representation or additional unlisted Kraus
directions does not evade it. It is a criterion for finite CPTP Poisson
uniformization, not a necessary condition for G to be a Lindbladian or
for the memory to tolerate G by a different proof.

### Direct construction of jumps with a scalar rate operator

Factor D=V V^dagger on its support and solve

    V conjugate(c) = a

with the minimum-norm solution, so sum_j |c_j|^2=a^dagger D^+a. If v_j is
column j of V, define actual algebraic jump operators

    B_j = c_j I + sum_i (v_j)_i P_i.                          (6)

Their Gram matrix on the basis (I,P_1,...,P_N) is

           [ a^dagger D^+a    a^dagger ]
    M_0 =  [       a             D    ].                     (7)

Their total rate operator is scalar, by (3)-(4):

    sum_j B_j^dagger B_j
      = (a^dagger D^+a)I + Gamma I + K + sum_i 2Re(a_i)P_i
      = r_min I.                                             (8)

Their dissipators give G exactly. Indeed, the completely positive part
contains the desired diag(gamma)+C block, its cross terms are

    sum_i [a_i P_i rho + conjugate(a_i) rho P_i]
       = -{sum_i k_i P_i,rho}/2 - i[H,rho],                   (9)

and its scalar part cancels the difference between r_min and
Gamma+tr C. Thus sum_j D[B_j]=F_gamma+E. For r>r_min add the identity jump
sqrt(r-r_min) I, whose dissipator is zero. Dividing these jumps by sqrt(r)
gives explicit CPTP Kraus operators for Psi. At the minimum rate the Kraus
rank is at most rank(D), and at a larger rate it is at most rank(D)+1.
If r_min=0 then D=a=0 and G=0; omit that stream or take any positive
identity-only proposal rate.

This construction retains complex coefficients. It does not twirl E,
throw away no-jump evolution, or implement negative jump rates.

### Why the conditions are necessary

Use the normalized maximally entangled vector and the orthonormal Pauli
vectors |P_i>=(P_i tensor I)|Omega_d>. The Choi matrix of r Id+G is zero
outside their span and is represented within that span by

        [ r-Gamma-tr C    a^dagger ]
    M = [      a             D    ].                         (10)

Positivity forces D>=0. If z is in ker D, the quadratic form on (t,z)
cannot be positive for all complex t unless z^dagger a=0. This gives the
range condition. Completing the square on range D gives

    (t,z)^dagger M(t,z)
       = (z+D^+a t)^dagger D(z+D^+a t)
         + [r-Gamma-tr C-a^dagger D^+a]|t|^2,                (11)

which proves the last condition and sufficiency. Choi positivity and its
Kraus equivalence are established mathematics; see
[Watrous, chapter 2, Theorems 2.22 and 2.26](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf).
Equations (6)-(9) additionally exhibit the scalar-rate jump realization,
which is the property required by the memory proposal argument.

## 3. A fixed structured neighborhood with all costs counted

Let nu>0 be the entire allowed proposal budget for this patch/owner cell.
Fix the nominal floor gamma_i=nu/(2N), so its physical rate is Gamma=nu/2.
Define computable error quantities

    b >= max(||C||_op, |tr C|, ||k||_2),
    u >= ||h||_2.                                             (12)

If

    b <= nu/(8N),        u <= nu/(4 sqrt(N)),                 (13)

then D>0 and

    D >= 3nu/(8N) I,
    r_min <= nu/2 + b + (b^2/4+u^2)/(nu/(2N)-b)
          <= (2/3+13/(96N))nu < nu.                          (14)

For the first inequality, ||a||_2^2=||k||_2^2/4+||h||_2^2; the cross
term vanishes because k and h are real. This is a genuine open neighborhood
inside the fixed finite-dimensional error model (2), including C with
negative eigenvalues. It is not an open neighborhood of all local maps on
the patch.

An alternative norm-based statement is available. If E is HP and trace
annihilating and its normalized Choi support is contained in
span{|I>,|P_1>,...,|P_N>}, then the same fixed floor suffices under

    ||E||_diamond <= nu/(8N).                                 (15)

Indeed, each block in (10) for E alone has norm at most
||J(E)||_op<=||E||_diamond. In particular ||C||<=delta,
|tr C|<=delta and ||a||<=delta. Hence

    r_min <= nu/2+delta+delta^2/(nu/(2N)-delta)
          <= nu/2+nu/(6N) < nu.                              (16)

The support promise in (15) is essential. It must follow from the actual
specified local Hamiltonian/jump structure; it is not inferred from a small
norm or from a finite set of calibration samples.

### Jump replacements and a local acquisition interface

For traceless nominal/error jumps in the fixed Pauli span, write
J_j=sum_i l_ji P_i and Delta J_j=sum_i delta_ji P_i. Their replacement gives

    C = sum_j [(l_j+delta_j)(l_j+delta_j)^dagger-l_j l_j^dagger]. (17)

Identity components can first be put into the standard Hamiltonian gauge;
that induced Hamiltonian must be charged in h. The following sufficient
quantity bounds all three entries in b:

    B = sum_j [2||J_j||_op ||Delta J_j||_op
                            + ||Delta J_j||_op^2].          (18)

For C, use ||l_j||_2=||J_j||_HS/sqrt(d)<=||J_j||_op and the rank-one
difference bound. For K=sum_j [(J_j+Delta J_j)^dagger(J_j+Delta J_j)
-J_j^dagger J_j], use ||K||_op<=B. Its normalized Hilbert-Schmidt
coefficient norm, including k_0, is at most B, proving the other entries.
Thus B<=nu/(8N) and a Hamiltonian coefficient bound as in (13) suffice.
For t nominal jumps with ||J_j||<=sqrt(kappa) and
||Delta J_j||<=eta sqrt(kappa), a sufficient relative-amplitude bound is

    eta <= sqrt(1+nu/(8Nt kappa))-1.                         (18a)

This counts all t affected jumps. It assumes the perturbations remain in
the verified finite mode catalog; it does not certify arbitrary changes
on the correction's entire local Hilbert space at this tolerance.

This interface uses a specified finite catalog of bounded-support control
and bath operators plus certified local coefficient/operator-norm errors.
For genuinely k-qubit-supported terms with fixed k, local matrix acquisition
has dimension 2^k, not 2^m for all m qubits in the radius-one box. A claim of
few-body structure is an input assumption to verify physically. Arbitrary
high-weight leakage, unmodeled bath correlations, calibration acquisition,
and the cost of validating the model are not supplied by this theorem.

## 4. The coherent special case is sharper and admits small-support streams

For C=0, the criterion is

    r_min = Gamma + sum_i h_i^2/gamma_i,                     (19)

with h_i=0 whenever gamma_i=0. It has the independent explicit realization

    r_i = gamma_i+h_i^2/gamma_i,
    U_i = (h_i I-i gamma_i P_i)/sqrt(h_i^2+gamma_i^2),
    -i[h_i P_i,.]+gamma_i(Ad_(P_i)-Id)
         = r_i(Ad_(U_i)-Id).                                (20)

Each proposal acts only on supp P_i. The P_i need not commute: (20) is an
identity of additive generators, with chronological Poisson compositions.
At h_i=0 choose U_i=-iP_i and r_i=gamma_i. At gamma_i=h_i=0 omit the term.

For a fixed floor budget Gamma and known h, Cauchy-Schwarz gives

    sum_i h_i^2/gamma_i >= (sum_i |h_i|)^2/Gamma,             (21)

with equality for gamma_i proportional to |h_i| on nonzero coefficients.
Optimizing Gamma as well gives total proposal cost 2 sum_i |h_i|. Unknown
errors instead require a floor fixed before h is realized; the uncertainty
ellipsoid sum_i h_i^2/gamma_i <= nu-Gamma is the exact robust condition.

For the uniform fixed floor Gamma=nu/2,

    ||h||_2 <= nu/(2 sqrt(N))                               (22)

is sufficient and sharp for that coefficient ellipsoid. Since
||h||_2=||H||_HS/sqrt(d)<=||H||_op after subtracting a scalar from H,
||H||_op<=nu/(2 sqrt(N)) is also sufficient. Neither bound is an arbitrary
ambient Hamiltonian promise unless the fixed Pauli-span promise holds.

For example, a one-body Hamiltonian on m=486 qubits has N=3m=1458 possible
Pauli modes, and (22) is nu/(2 sqrt(1458)), approximately nu/76.37.
The inherited arbitrary-map full-patch floor gives the sufficient
Hamiltonian condition 2||H||<=nu*2^(-972). This comparison concerns only
the algebraic local regularization factor and different error classes. It
does not remove the unhelpful inherited classical threshold constants.
Ownership can be regrouped by actual face sites to avoid duplicate local
streams, but their resulting per-cell rate density must still be counted.

### Reusing a real Pauli bath instead of installing a new floor

If a fixed baseline already contains the positive Markovian Pauli rates
gamma_i on all permitted Hamiltonian modes, equations (19)-(20) reuse
those rates. No additional Pauli noise is then required. One only needs
Gamma+sum_i h_i^2/gamma_i to fit the proposal threshold. This still uses
the completed correction channels. It cannot be asserted uniformly over
all baths in the original exact-Pauli theorem, which permits zero rates:
if gamma_i=0 and h_i!=0, the range condition fails.

For one-body fields in the 4D toric code, each fine owner cell has six
data qubits and eighteen possible X/Y/Z Hamiltonian modes. For equal
native bath rates gamma, the exact owner-cell proposal budget is

    r_cell = 18 gamma + sum_(six faces,P) h_(face,P)^2/gamma. (22a)

Selecting a fixed positive baseline gamma=nu/36 gives
||h_cell||_2<=nu/(2 sqrt(18)). In an already specified bath use its actual
positive rates, not a fictitious selected lower bound. This is a concrete
restricted memory theorem candidate with continuous one-body Hamiltonian
errors and no extra depolarizing floor beyond that fixed native bath.
It leaves generic interacting Hamiltonians and correction-jump errors
outside the one-body model.

There is also a simple lower obstruction to a dimension-free *unstructured*
signed-map guarantee. If a Pauli-direction rate is gamma_P, the allowed
error E=-epsilon(Ad_P-Id) requires gamma_P>=epsilon for conditional
complete positivity. Covering all d^2-1 Pauli directions with the same
epsilon therefore needs Gamma>=(d^2-1)epsilon. The exponential cost for
an unrestricted signed local-map ball has not been removed by a catalog
restriction.

## 5. Locality and catalog size must be charged honestly

If H uses Pauli weight <=k_H and jump modes use Pauli weight <=k_J, a
sufficient single-patch catalog has

    N <= sum_(w=1)^max(k_H,2k_J) 3^w binomial(m,w).           (23)

For fixed weights this is polynomial in m. Each installed floor Pauli has
weight at most max(k_H,2k_J), and its diameter is at most the diameter of
the original bounded patch. An alternative sparse catalog includes only
the modes and products actually permitted in the error model, often much
smaller than (23). The N floor types and their total Gamma are real costs.
Dense Gram factorization takes O(N^3) arithmetic and O(N^2) storage; this
is an analytical conversion, not required hardware execution.

Do not confuse low Pauli weight with a genuinely k-qubit-supported jump.
A single jump L=sum_x Z_x can describe a collective bath and acts on the
union of all those sites. Its cross terms and the range of its patch must
be charged. If instead each L_j acts on one listed set of <=k qubits,
products within that same L_j stay on that set; one can use per-support
catalogs and local rate ownership. Such a catalog has at most 4^k-1
nonidentity modes. These are different locality promises.

The physical implementation can use the original Hamiltonian and local
jump errors together with the installed Pauli floors. The B_j and Psi in
(6) are an exact alternative unravelling used in the proof. They are not
new hardware or supplied free primitives. Imperfections in the added
floors must themselves obey the same structured bound or receive a
separate rigorous treatment.
For general C, a factorized B_j can contain Pauli terms spread across the
whole bounded patch. Its proposal support is then that union, even if
each installed floor kick is few-body. The good-schedule interface must
charge the union patch. Only the independent Hamiltonian representation
(20) automatically keeps each separate proposal on supp P_i.

## 6. Exact falsifiers and a non-Pauli signed example

The accompanying `check_structured_gram_exact.py` uses SymPy exact rational
and Gaussian-rational arithmetic. It constructs normalized Choi matrices
from their action on every matrix unit, compares them with the catalog
Gram matrices, and verifies trace preservation and scalar-rate Kraus
construction. Its JSON output is finite algebra evidence only.

1. **Signed non-Pauli jump correction on two qubits.** Use
   P=(XI,YZ,ZZ), gamma_i=1/5,

       C = [[1/20, -i/40, 0],
            [i/40, -1/50, 0],
            [0,      0,   0]],
       h=(1/30,0,1/40).

   C has a negative principal diagonal entry and is not PSD. Nevertheless
   D is strictly positive and the exact r_min is finite. The diagnostic
   verifies all sixteen 4x4 matrix units, the Gram/Choi identity, and the
   exact scalar-rate Kraus identity at r_min. This is not a replacement
   of signed coefficients by positive scalar rates; factorization occurs
   only after the deliberate floor has made D positive.

2. **Missing coherent direction.** Independent single-site X,Y,Z floors
   on two qubits and H=h ZZ have, on the (I,ZZ) Choi subspace, a principal
   block with bottom-right entry zero and off-diagonal +/-ih. Its
   determinant is -h^2, for every proposal rate r. No finite r works.

3. **Missing anticommutator direction for a physical positive jump.**
   L=|00><11| is an allowed two-site positive Lindblad jump. Its effect is

       L^dagger L=(I-ZI-IZ+ZZ)/4.

   Independent single-site floors have no ZZ direction, while the
   anticommutator couples I to ZZ with coefficient -1/8. The same
   principal determinant is -1/64 for every r. Thus even positive
   two-site dissipation does not generically inherit a finite proposal
   representation from independent one-site floors.

4. **Sharp Pauli boundary.** A single P with dephasing gamma and drift h
   has minimal rate gamma+h^2/gamma. Reducing that rate makes its 2x2
   Choi determinant negative. This checks the cost charged in (19), not
   merely existence of some channel.

5. **Amplitude-damping completion.** On one qubit, lambda D[|0><1|]
   plus (lambda/4)(Ad_Z-Id) equals lambda(Reset_|0>-Id). This exact
   positive, nonunital example illustrates a useful very small catalog;
   it is standard channel-completion algebra, not a novel physical effect.

## 7. Conditional memory transfer

Assume the following interface as a separate premise: for the chosen
completed sweep correction channels and fixed bounded fault patches, there
is one clock/location-only Good_T event which simultaneously corrects
every supported Pauli history with the same final decoder, and independent
CPTP proposal streams of total owner-cell rate <=nu obey

    Pr(not Good_T) <= A' L^4(1+kappa T) exp(-c' L).            (24)

That is the inherited conditional interface; it has not been established
anew here. Under it, apply (5) patch by patch. If necessary raise r_min to
the fixed budget nu by the identity Kraus term. This gives fixed-rate,
input-independent, local CPTP proposal streams. The Kraus-span argument
on the same universal Good_T event then yields

    ||Dec exp[T(G_completed+F_gamma+E)] Enc-Id||_diamond
      <= min(2,2 A' L^4(1+kappa T) exp(-c'L)).                (25)

All physical Hamiltonian/jump errors remain continuous in the left side;
the Poisson circuit is an exactly equal representation. There is no
condition ||E||T<<1. Proposal rate, support radius, catalog multiplicity,
and all owner-cell budgets must be uniform in L. This construction still
uses the deliberately completed corrector and a real added floor. It does
not prove robustness of the original unmodified sweep generator.

## 8. Primary prior art and what can be claimed

- [Shang and Franca, arXiv:2604.18533v1](https://arxiv.org/html/2604.18533v1),
  Eq. (4), gives D[I-i delta H]=-i delta[H,.]+delta^2 D[H]; its gauge
  discussion explains identity shifts of Lindblad jumps. This already
  implies (20) for a Pauli involution after checking the scalar rate.
  Current arXiv metadata records v2 on 4 October 2026. Both inspected
  arXiv HTML versions contain Eq. (4) and gauge discussion. A search
  result from an author-uploaded ResearchGate PDF displays an explicit
  weighted Pauli Appendix D, but that PDF's version was not pinned and
  is not cited as an acquired appendix of arXiv v1/v2.
- [Aniello et al., arXiv:1002.3507v1](https://arxiv.org/pdf/1002.3507),
  Proposition 5.2 and its surrounding discussion, describe random-unitary
  semigroup generators and credit Kummerer-Maassen. Continuous
  Hamiltonian/Brownian terms can belong to the closure of the random-unitary
  cone without themselves being a finite-rate pure compound-Poisson
  generator. The finite-rate/range distinction in (5) matters.
- [Watrous, Theory of Quantum Information, chapter 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf),
  Theorems 2.22 and 2.26, supplies Choi/Kraus positivity and the TP
  condition. Its Choi convention is unnormalized; this note explicitly
  normalizes the Pauli Choi vectors. No normalization factor d survives
  the orthonormal catalog calculation.
- [Havel, quant-ph/0201127v4](https://arxiv.org/abs/quant-ph/0201127v4),
  abstract/metadata inspected, already addresses conversions among
  Lindblad, Kraus and matrix representations. Its full proof was not
  acquired in this run; no specific theorem from it is used as a premise.

The defensible output is an exact, internally derived structured
regularization theorem and explicit countermodels, plus a conditional
application to the inherited memory interface. Historical novelty and
external correctness remain unestablished. The exponential full-patch
factor is avoidable for restricted catalog errors, but the required
catalog/model validation and actual floor implementation remain decisive
physical gates.
