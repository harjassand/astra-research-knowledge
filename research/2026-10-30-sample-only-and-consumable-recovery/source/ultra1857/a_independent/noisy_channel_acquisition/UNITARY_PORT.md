# Uniform known-unitary acquisition from a rational near-unitary matrix

30 October 2026. Independent constructive port for the growing-rank common-frame
compression. C owns the finite Gaussian/polar Haar supplier. This note closes
its passage from exact rational matrix evaluation to an ACTUAL known unitary
circuit, without an unknown inverse-pivot or exact real-arithmetic oracle.
All QR, Givens and universal-gate machinery is ordinary; no generic priority or
quantum-hardware claim is made. No source instance or quantum circuit was run.

## 1. Input/output, with the matrix supplier paid elsewhere

Let U be an r-dimensional unitary and X an explicitly acquired rational complex
matrix with a warranted operator bound ||X-U||<=e<1/4. U is not a free matrix
oracle: in C_UNIFORM_TWIRL it is polar(Ghat), and the finite rational binomial
series from the known Gram floor supplies X to any declared e at polynomial
cost. For target 0<z<=1, the task here is a circuit for an actual unitary Vtilde
with inf_theta||Vtilde-exp(i theta)U||<=z. A finite universal SU gate alphabet
does not supply an arbitrary continuum GLOBAL phase. That phase is unobservable
for the unconditional twirl channel here. Trusted known gates are the same paid quantum-control
model as the Schur compiler; no unknown source inverse or adjoint is used.

It suffices to request

    e <= z^2/(64r).

This is additional precision on an acquired known matrix, not on the unknown
physical channel. Substituting this e in C's explicit series changes its degree
and bit cost by a polynomial, preserving the growing-rank claim.

## 2. An elementary quantitative QR bound

Take an exact complex QR factorization X=V R, V unitary, R upper triangular with
positive real diagonal. Such a factorization exists since s_min(X)>=1-e>0.
For the jth diagonal entry,

    R_jj=dist(X_j,span{X_1,...,X_(j-1)}) >= s_min(X)>=1-e.

Indeed every vector realizing this distance is Xv with v_j=1, v_l=0 for l>j;
its Euclidean norm is at least one. Put W=V*U. Since ||W-R||<=e,

    Re Tr W >= r(1-2e).

For unitary W this gives

    ||V-U||^2 <= ||W-I||_F^2
                =2r-2 Re Tr W <=4re.                 (1)

Thus ||V-U||<=2sqrt(re)<=z/4. This deliberately conservative square-root
continuity bound is sufficient. It makes no claim that rounded X itself is a
physical channel or unitary.

## 3. No tiny Givens denominator is supplied

Use only row permutations among the uneliminated rows and complex Givens
rotations. At column j, after its previous columns have been eliminated, the
remaining column residual has norm R_jj>=1-e. Some remaining entry has magnitude
at least (1-e)/sqrt(r). Choose an approximate maximum using warranted entry
intervals; fixed slack permits an exact chosen pivot of magnitude at least
(1-e)/(2sqrt(r)). No exact tie between unknown real magnitudes is decided.

For a pivot a and another entry b, let c=sqrt(|a|^2+|b|^2). The two-level unitary

    [[conj(a)/c, conj(b)/c],[-b/c,a/c]]

maps the column pair (a,b) to (c,0). The denominator remains at least the pivot
floor, and the pivot magnitude increases as the other entries are eliminated.
A final one-level phase fixes a remaining complex diagonal. At most O(r^2)
two-level rotations, phases and row swaps are needed. Every exact intermediate
matrix is a unitary left multiple of X and has norm at most 1+e.

The exact QR sequence is used in the proof. It need not be stored in an
exponentially large tower of square-root number fields. Known approximate matrix
entries and ordinary bounded-denominator scalar arithmetic suffice instead.

## 4. A literal finite-bit completion

Fix the pivot indices by approximate-maximum comparisons with a margin, not by
requiring exact ties to be resolved. The analytic Givens formula above has a
known local Lipschitz bound polynomial in r whenever its denominator exceeds
(1-e)/(2sqrt(r)). The exact intermediate matrices lie in a known bounded ball.
For L<=2r^2 elementary elimination steps, one may use the deliberately crude
propagation bound C_r^L with C_r=100(r+1)^2.

Evaluate square roots, divisions and updates with interval radius smaller than

    [z/(100(L+1)^2)] C_r^(-L),

also below a fixed fraction of the pivot floor. The number of required bits is

    O(L log(r+1)+log(1/z)+input_bits),

not exponential in r. Even this loose propagation bound therefore gives
polynomial BIT work. All divisions have their declared polynomial floors, and
square roots can use rational interval bisection. Approximate maxima choose
valid pivots for one exact QR sequence of the rational X. Their interval errors
and the sum of rotation approximation errors can be kept below z/4.

Compile the resulting known two-level unitaries to total additional channel-
irrelevant-global-phase error at most z/4. Barenco et al.'s ordinary controlled two-level decomposition on
ceil(log2 r) padded qubits, followed by a standard finite-universal-gate
approximation such as Solovay--Kitaev, has polynomial r and log(1/z) gate/bit
cost. The primary BCH construction uses these same known-control primitives.
No rounded nonunitary matrix is silently executed. Relative phases of controlled
two-level gates must be preserved by that complete known-gate decomposition;
only an overall phase of the final r-dimensional unitary is discarded.
Combining (1), finite evaluation and gate errors gives
inf_theta||Vtilde-exp(i theta)U||<=3z/4<z.

The finite gate compiler and controls remain substantive trusted resources.
This note establishes an algorithm under that model, not native acquisition of
arbitrary gates on an opaque physical material or an unknown encoding.

## 5. Consumption by the growing-rank compression

Set z=g/(16M) for C's M-carrier twirl budget and ask its rational polar-series
supplier for e<=z^2/(64r). Accepted Ghat has a warranted rational Gram floor and
an explicit norm cap. Its series degree is polynomial in r,M,1/g and the new
precision bits. The rational series coefficients have finite common-denominator
representations; degree times input bit height bounds their arithmetic size.
Thus this known-unitary port has uniform polynomial cost when r grows, unlike
enumerating all GT patterns in a U(r) irrep.

For the SAME circuit Vtilde used on all M carriers,

    halfdiamond(Ad(Vtilde)^tensorM,Ad(U)^tensorM)
        <=M inf_theta||Vtilde-exp(i theta)U||.

All external references are included in this bound. Independent circuits or
unitaries on different carriers would be a different channel and would destroy
the shared-frame premise. Discard the sampled classical seed from the compared
output; a theorem about the averaged compression channel is not a theorem about
each retained seed record. Fixed tomography/recovery postprocessing preserves
the channel error by contractivity.

## 6. Primary predecessors actually consumed

* Bacon--Chuang--Harrow, quant-ph/0601001v1, gives Schur circuits polynomial in
  the carrier number, local dimension and log inverse precision. Its gate
  discussion/references include ordinary known-unitary synthesis and
  Dawson--Nielsen's Solovay--Kitaev algorithm.
* Burchardt et al., 2509.22640v1, Theorem 1 and Table 1, provides corrected
  high-dimensional Schur controls with matched representation labels. This
  avoids relying on the known incorrect classical final-isometry premise of
  the older high-dimensional construction.
* Mezzadri, math-ph/0609050v2, Sections 4--5, explains Gaussian-to-Haar QR
  and its diagonal-phase convention. The present port does NOT assert that a
  generic numerical QR output has Haar law: C's target is the correctly defined
  polar unitary, and QR is only used to compile a nearby known unitary.
* Barenco et al., quant-ph/9503016v1, supplies ordinary universal one-/two-qubit
  control decomposition. Exact continuum angles are not supplied as free gates;
  finite synthesis precision is charged above.

Historical novelty of this elementary quantitative completion is not assessed.
Its consequence here is to remove a hidden known-unitary implementation oracle
from the uniform growing-rank construction, not a new random-matrix or gate
synthesis principle.
