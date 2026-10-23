# Exact duality and uniform norm bounds for the temporal operator problem

Cycle6 distinct contribution: the full operator constraint is retained.
This is an internal mathematical source, not an external priority claim.
The exact Cycle5 FIXED_BLOCK_ORDER.tex, its finite-prefix representation,
and the two representation/susceptibility scripts were read.

## 1. Objects and hypotheses

Fix a positive integer k. Let A=(C3)^tensor k, let Q count colored ports,
and let sigma=rho_c^tensor k, rho_c=diag(1/2,1/4,1/4).
Let G_1 denote the coefficient of b=beta² in the charge-pinched exact
bulk displacement, acting on A and k bath-prefix colors. Write

    T(X)=Tr_A[(X tensor I)G_1],
    H(X)=Tr(sigma^-1 X²)/(2 ln2),
    A_k=sup_X[-lambda_max(T(X))/2-H(X)],

where X is Hermitian, commutes with Q, and Tr X=Tr QX=0.
All spaces in this variational problem are finite dimensional. The
initializer used in the communication theorem is not changed.

For each prefix density tau define

    F_tau=Tr_prefix[(I tensor tau)G_1],
    H_tau=F_tau+(2Q-kI).

The partial-trace expression is the Hermitian contraction, equivalently
defined by Tr(X F_tau)=Tr(tau T(X)).
There is no use of a potentially unbounded bath entropy here.

For a fixed computational input word, move versus stay produces orthogonal
output words in the deep bulk. Its exact diagonal displacement is
(1-b)(2 charge(word)-k) I on the bath. Therefore the input diagonal
of F_tau is -(2Q-kI), independent of tau. In particular H_tau is input
off-diagonal and charge preserving. Consequently

    Tr(sigma H_tau)=Tr(sigma Q H_tau)=0.

The distinction between H_tau (an observable) and H(X) (the entropy
quadratic form) is deliberate.

## 2. Exact closest-point duality

Theorem. Let v_k=min_tau Tr(sigma H_tau²), where tau ranges over all
prefix densities. Then

    A_k=(ln2)/8 v_k.

A minimizer tau_* exists. Put H_*=H_(tau_*). Then the explicit variational
optimizer

    X_*=-(ln2)/2 sigma H_*

satisfies all constraints, and

    T(sigma H_*) >= v_k I,
    lambda_min(T(sigma H_*))=v_k.

Proof. The set C={H_tau} is compact and convex in the real Hilbert space
of charge-preserving Hermitian observables, with inner product
<F,H>_sigma=Re Tr(sigma FH). Sigma is strictly positive and commutes
with all these observables. Choose its closest point H_* to zero.
The ordinary Hilbert-space projection inequality gives

    <H_*,H_tau>_sigma >= ||H_*||_sigma²=v_k

for every prefix density tau. Because H_* has zero input diagonal,
the affine term 2Q-kI is orthogonal to H_*; hence this inequality is
equivalent to T(sigma H_*)>=v_k I. Taking tau=tau_* gives equality
in expectation, so the minimum eigenvalue equals v_k.

For any feasible X,

    -lambda_max(T(X))/2 <= -Tr(X F_(tau_*))/2
                           = -Tr(X H_*)/2.

Completing the square with norm ||X||²=Tr(sigma^-1 X²) yields

    -Tr(X H_*)/2-Tr(sigma^-1 X²)/(2 ln2)
       <= (ln2)/8 Tr(sigma H_*²).

Equality holds at X_* above. It is feasible because H_* commutes
with sigma and Q, and its two weighted diagonal moments vanish.
The projection inequality supplies the full operator sign for this X_*,
not merely a favorable averaged sign. This proves the theorem.

This is a finite-dimensional closest-point theorem application, not
a new general minimax principle. It avoids any questionable exchange
of infinite-dimensional suprema and infima. The finite prefix density
is a dual witness, not a proposed physical bath initialization.

## 3. Toggling representation and endpoint orthogonality

Let W_0=U_k...U_1. In the interaction frame,

    W_0^* W_s = exp(is C_k)...exp(is C_1),
    C_j=U_1...U_(j-1) U_j U_(j-1)...U_1.

Perform this identity on coordinates deep enough that all displayed
finite words avoid the vacuum, for example initial depth >=4k.
The exact finite-prefix identity then determines the same bulk
coefficient on every initial depth >=k; the extra depth is only an
algebraic proof device.

On this deep core C_j changes only the zero-versus-colored bit at
position j. Other port color values may move, but their charge bits
do not. This follows by conjugating each q_i through U_l:
U_l flips q_l and commutes with q_i for i!=l, away from the vacuum.
Write C_j=C_j^++C_j^- according to total-charge change +1 or -1.
Each part is a contraction, and its adjoint is the opposite part.

Put Z=W_0^* W_s and C=sum_j C_j. Since W_0^*QW_0=kI-Q
on the deep core, the physical displacement is

    G_s=Q-W_s^*QW_s=2Q-kI+(Z^*QZ-Q).

To second order in s, the charge pinching of Z^*QZ only sees

    -1/2 [C,[C,Q]] = [C_-,C_+].

The additional ordered-product commutator is of the form [B,Q]
and vanishes under charge pinching. Since b=sin²s=s²+O(s^4),

    G_1=[C_-,C_+].

The j=j terms are I-2q_j; their sum is kI-2Q. Therefore the
off-diagonal part defining H_tau is a sum over unordered endpoint
pairs {i,j}. For i<j its joint term is

    B_ij=C_i^- C_j^+ + C_j^- C_i^+
         -C_i^+ C_j^- -C_j^+ C_i^-.

It changes exactly the two endpoint charge bits, preserving every
other charge bit. After any bath contraction tau it still has this
support. Distinct unordered endpoint pairs are therefore orthogonal
in the sigma-weighted Hilbert-Schmidt inner product.

Write

    B_ij=A_ij+A_ij^*,
    A_ij=C_i^- C_j^+ - C_j^+ C_i^-.

A_ij maps the charge sector (q_i,q_j)=(1,0) to (0,1), so its
domain and range are orthogonal. Its norm is at most 2; consequently
||B_ij||<=2. A unital bath-state contraction preserves this bound.
Its square is supported on those two endpoint sectors, whose
total sigma probability is 1/2. Thus each contracted endpoint
term contributes at most 2 to Tr(sigma H_tau²). Summing gives

    0 <= v_k <= Tr(sigma H_tau²) <= k(k-1),
    ||H_tau|| <= k(k-1).

For the optimizer this also gives

    ||X_*||_1 <= (ln2)/2 sqrt(v_k) <= (ln2)/2 k,
    ||sigma^-1 X_*|| <= (ln2)/2 k(k-1).

The trace-norm estimate is weighted Cauchy--Schwarz. These are uniform
in k and are useful for the owner's positivity and nonlinear-remainder
argument. They do not alone prove growth from below or a coding rate.

The bounded-word depth buffer does not replace the real bath by a
reflecting cutoff, and no root term is removed from the later exact
coding theorem.

## 4. Global color covariance and a focused finite certificate

The device is covariant under u in U(2): apply 1 direct-sum u on
each qutrit color sector and the second quantization of u on the
Fock bath, with identity on the seed. Thus the dual objective is
invariant under simultaneous prefix conjugation u^tensor k.
Convexity permits restriction to globally twirled prefix densities.
It does NOT justify replacing every prefix density by the maximally
mixed density: the commutant contains nontrivial permutation sectors.

The exact k=4 source demonstrates this distinction. For tau=I/16,
the dual objective is 561/512. Its gradient has four different
diagonal values and nonzero off-diagonal entries, so it is not
stationary over all densities.

For tau_sym=P_sym/(k+1), the following exact k=4 certificate holds:

    Tr(sigma H_sym²)=17/16,
    T(sigma H_sym)=(17/16) I + graph Laplacian.

Every off-diagonal Laplacian entry is nonpositive, every row sum is
zero, and the matrix is real symmetric. Hence it is positive
semidefinite. This gives the matching exact upper and lower

    A_4=17 ln2 /128,
    X_*=-(ln2)/2 sigma H_sym.

The script temporal_dual_certificate.py reads the preserved Cycle5
polynomial and verifies this certificate over exact rational numbers.
No finite-check count is used as a large-k proof. The same small
calculation for k=2,3 gave v=1/8,1/2, respectively; those values were
diagnostic and are not the owner's selected target.

## 5. Failed simplification and continuation dependency

Uniform prefix averaging alone is not optimal even at k=4.
Likewise, an intervening walk with positive net height does not
guarantee that both ordered toggles leave the original bath unchanged:
the binary pattern 011 with endpoints 0 and 2 is a counterexample.
One branch transports an original bath color and the other an input
color. Net height loses the necessary path information.

The distinct constructive contribution `temporal_constructive_structure.md`
proves a guard/meander event on charge patterns that forces an input-only
transposition. Its counting gives v_k >= k^(3/2)/32 for k>=4. Combined
with this dual theorem it proves A_k/k >= (ln2)sqrt(k)/256 with an
actual full-operator optimizer. The focused independent challenge is
recorded in `temporal_guard_independent_challenge.md`.
The owner must still carry that direction through uniform positivity,
nonlinear remainders, exact negative drift and the inherited
arbitrary-reference code. No general capacity upper, feedback
conclusion, useful blocklength or historical first follows from
this note alone.

Costs: the small certificate is exact standard-library rational
algebra; its own receipt records runtime and memory. Analytic discovery,
model inference and review totals are unmeasured.
