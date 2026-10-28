# A finite physical frame for strictly entanglement-annihilating local noise

Constructed 2026-10-27. This is an abstract, exact rational simulation
interface and one acquired gate instance. It is not a physical noise
calibration, a new generic tractability class, or a demonstrated advantage.

## Model and existing inputs

For d>=2 and rational c>c0=(1+sqrt(3))/2 set

    Phi_c(X)=(c tr(X) I-X^T)/(dc-1).

This map is CP and trace preserving for c>=1: its unnormalized Choi matrix
is c I-F_swap, whose eigenvalues are c-1 and c+1. Its tensor square is
entanglement annihilating exactly when c>=c0. The latter is an established
input, obtained from Lami--Huber2016 Theorem7/Corollary8 by setting
(alpha,beta,gamma)=(-1/c,-1/c,1/c^2) after global transposition. Their
inequality gamma<=alpha+beta+2 becomes c^2-c>=1/2.

Primary source: https://arxiv.org/html/1603.02158v1 .

An n-site process starts with a supplied nonnegative mixture of product
frame states. Alternatively, each initial product preparation passes through
the unobserved local noise before entering the process. Each retained
operation acts on one or two sites and is followed immediately by fresh
unobserved Phi_c on every retained output site. A finite supplied instrument
alphabet may have classical outcomes; the operation outcome precedes that
mandatory noise. Conditional choices can depend on the classical transcript.
Final destructive local POVMs are permitted. Noise environments supply no
flags or memory; there is no noiseless interposed refresh/control, entangled
external reference, or arbitrary entangled initial register.

The finite alphabet has rational superoperator entries in a rational real
Hermitian coordinate basis. This is a condition on the maps, not necessarily
on a chosen Kraus factorization. Physical instruments are CP and their sums
are TP. Arbitrary numerical specifications without certified precision are
not exact input data. The executed exact rational algorithm also requires
rational supplied initialization weights and rational final POVM effects.
More general computable probabilities require a separately charged exact
random-bit sampling oracle/algorithm; noncomputable real data are not granted.

## Strict contraction gives a rational physical polytope

Let D_t(X)=tX+(1-t)tr(X)I/d. Direct substitution gives

    Phi_c = D_t o Phi_c0,
    t=(dc0-1)/(dc-1),       0<t<1.

If a finite pure-projector set is a fidelity-epsilon net, its convex hull P
contains D_t of the entire density-operator body whenever
epsilon<=(1-t)/d. To prove this, for Hermitian H write M=lambda_max(H),
m=lambda_min(H). A net projector near a maximum eigenvector has expectation
at least M-epsilon(M-m). Also M-tr(H)/d>=(M-m)/d. Hence the support function
of P dominates t M+(1-t)tr(H)/d in every direction. The finite-dimensional
separation theorem gives the claimed containment. Scalar H causes no issue.

This can be constructed using only rational coordinates. Choose rational
0<epsilon<(1-t)/d using directed rational bounds for sqrt(3). Choose an
integer K with K^2 epsilon>=2d. Enumerate all nonzero vectors v in Z[i]^d
whose 2d real coordinates lie in [-K,K], and use vv*/(v*v).
Rounding K times a unit vector coordinatewise makes an error of at most
sqrt(2d)/(2K). Normalizing the nonzero rounded vector at most doubles that
error; the resulting infidelity is at most 2d/K^2<=epsilon. Every projector
entry is rational. The unreduced state-count upper bound is

    M <= (2K+1)^(2d)-1.

Duplicate projectors may be removed. This upper bound is deliberately an
explicit acquisition cost, not a claim of an economical near-boundary net.

For every normalized two-site state rho, the boundary output
omega=(Phi_c0 tensor Phi_c0)(rho) is separable by the existing EA theorem.
Applying D_t to both product factors places the strictly noisier output
in conv{sigma_i tensor sigma_j}. The same argument for one-site outputs
uses only positivity of Phi_c0. Thus arbitrary normalized instrument branches
before the mandatory noise have outputs in the same respective frame hulls.

## Rational kernels and arbitrary circuit size

For each local input vertex tuple and each operation outcome, solve a finite
linear feasibility problem for nonnegative coefficients in the output
product frame. Unnormalized coefficients sum to that outcome's trace.
Across all outcomes their sum is1. All equalities are rational and feasible
by the preceding geometry; a rational basic solution exists. A single
two-site branch needs at most d^4 nonzero output products. Normalized
probabilities are rational whenever the outcome probability is nonzero.
Zero-probability branches contribute no trajectory.

A classical state stores one of M labels per physical site. Sample an
initial product tuple, then sample each outcome and replacement local tuple
from the acquired column. Linear reconstruction proves by induction on the
entire adaptive transcript that this process has the same joint Born law.
Final local readout uses tr(E sigma_i), which is nonnegative because the
vertices are physical. Width/depth can be arbitrary finite values; the
supplied fixed gate alphabet requires only finite preprocessing.

This composition principle is established: Okay2026 Definition13,
Theorem16, Lemma17, Corollary19 provide a general polyhedral instrument
framework (also allowing nonphysical vertices). Harrow--Nielsen2003
III.2--III.3 already supplies separability-based stated-error simulation.
The present narrower construction makes the strict local-noise/rational
physical-frame interface explicit; it does not establish a new complexity
class or priority for generic positive simulation.

Primary sources:
https://link.springer.com/article/10.1007/s40687-026-00626-x ;
https://arxiv.org/html/quant-ph/0301108v1 .

## An actually acquired24-state qubit instance

Take c=7/4, with Bloch factors (-2/5,+2/5,-2/5). This single-qubit channel
is not EB: its normalized Choi partial transpose has eigenvalue -1/20.
The local states are the24 permutations/sign choices of (0,3/5,4/5).
Their Bloch polytope is exactly

    |r|_infinity <=4/5,     |r|_1<=7/5.

The rational H-polytope has exactly these24 vertices, verified by all
triples of its14 facets. It contains the Euclidean ball of radius4/5,
because the other facet distance is7/(5 sqrt3)>4/5. Here
t=2 sqrt3/5<4/5. This chosen frame therefore covers every two-qubit
operation followed by the stated pair noise; the sufficient threshold for
this chosen frame is c>=(4+5 sqrt3)/8. This is not an optimal threshold.

For this instance D_t=k D_(4/5)+(1-k)D_0 with k=sqrt3/2. For a separable
boundary output the doubly erased term is I/4 with weight
(1-k)^2=7/4-sqrt3>1/64. All other terms remain in the same product hull.
Consequently every normalized pair output permits a reserved1/64 uniform
product-frame contribution. The24-state average is I/2.

The acquired gate is controlled real rotation: the upper2x2 block is I,
the lower block is [[3/5,-4/5],[4/5,3/5]]. It is rational, entangling and
non-Clifford. EXACT24_KERNEL.json has all576 input-pair columns, each with
the reserved uniform contribution plus a rational remainder of support<=16.
The largest saved probability numerator/denominator has73bits.
compile_qubit_frame.py uses ordinary HiGHS only to propose sparse supports;
all weights and equations are reconstructed with Fraction arithmetic.
verify_kernel.py independently rebuilds the gate/Pauli transfer using only
Gaussian rationals and stdlib, and checks all9,216 Hermitian equations,
nonnegativity, stochasticity and the exact24-vertex geometry. Its initial
checker mistakenly divided integer facet coefficients as floats; converting
them to Fraction corrected the checker, after which every assertion passed.
No original kernel coefficient was changed.

runtime_sampler.py implements the acquired pair update with rational
categorical sampling. It assumes an independent unbiased-bit primitive;
it does not assert an infinite IID law for a finite-state host PRNG. Rejection
from a common denominator D uses less than2 ceil(log2 D) expected bits per
categorical call, plus6bits for the reserve decision and, on reserve, less
than20 expected bits for two uniform24 draws. LCM denominators can be much
larger than an individual73bit denominator. The acquired file's maximum
is73bits, giving a conservative152.3125 expected-bit bound per pair update;
SAMPLING_RESOURCES.json records this calculation. Non-dyadic probabilities have
unbounded worst-case bit cost.
The peer's ordinary binary-interval sampler has a better support-only
expected-bit bound; no superiority is claimed for this implementation.

## Endpoint, near-endpoint and physical-acquisition limits

No fixed finite physical product list can cover ALL noisy pure two-site
outputs at c=c0. For a rank-two Bell input the partial transpose has kernel
w=(|12>-|21>)/sqrt2, since c0^2-c0-1/2=0. Under independent local rotations
the input range supplies the rotated kernels. For each fixed normalized
physical product vertex, its expectation on the rotated partial-transpose
kernel is nonnegative and is a nonzero real-analytic function: its Haar
average is1/d^2. Its zero set has measure zero. Finitely many vertices
cannot supply a zero-expectation convex combination for every rotation.
For 1<=c<c0 some outputs are entangled, so even a continuous product-state
hull is insufficient.

This is an all-pure-output universality statement. With only maximally mixed
initialization and unital gates, the singleton I/d is a trivial invariant
frame. The theorem does not rule out nonphysical vertices, entangled blocks,
continuous/adaptive decompositions, or arbitrary HMM realizations.

The independent challenge quantifies the qubit cost. With
lambda=[1-3/(2c-1)^2]/4, any physical product list covering that universal
range has at least ceil[1/(2lambda)] elements. Dyadic inputs c_B just above
c0 have O(B)-bit descriptions but require Omega(2^B) explicitly listed
product vertices. Trace-distance tolerance epsilon replaces lambda by
lambda+epsilon in that necessary bound. The challenge also gives a
slightly noisier reference construction with total output TV<=epsilon
after L local uses, preventing the exact binary gap from dictating its
frame margin. This is approximate sampling of the original process, not
an exact claim for it. See ../quantum_frame_challenge/PROOF.md.

An average single-use channel does not acquire the model's instrument or
multi-time premises. The peer supplies exact flagged-noise and repeated-
Pauli-memory processes with the same isolated Phi_c and entangled retained
branches or two-use identity behavior. A kernel identity or finite test
cannot certify arbitrary-depth fresh unobserved noise. Actual physical
acquisition and matched full-cycle advantage remain NOT_ACHIEVED.
