# An all-order test for a genuinely reused finite-carrier controller

30 October 2026. Root analytic construction, using ordinary finite-matrix
perturbation. No controller satisfying its positive conclusion is supplied
or claimed. This is a test of an ACTUAL acquired staged controller, not
an assumption that arbitrary coefficient matrices are physically allowed.

The exact three-carrier algebra supplies a finite coefficient transfer
T(q)=T0+qT1, q=1/r, for each fixed known-memory staged source cell. Initial
encoding E(q) and a supplied finite final decoder D(q) give the logical
channel matrix

    L(q,m)=D(q) T(q)^m E(q).                              (1)

Here the finite coefficient dimension and logical input/output dimensions
are independent of r. All operations, source calls, the actual final
decoder and its complete reference action must first be acquired as in
`c_three_carrier_algebra/PROOF.md`. A free exponentially large history
decoder, a matrix inferred from finite fidelity fits, or a marginal reset
does not meet this contract. Known controls with r-dependent parameters
must be represented by their actual analytic expansion instead.

Assume E,D are analytic at zero; T0 has a semisimple eigenvalue1 and all
other eigenvalues strictly inside the unit disk. Let P be its spectral
projector at1, Q=I−P, and define on range(P)

    K=P T1 P.                                            (2)

For every fixed tau>0,

    lim_(r->infinity) L(1/r,floor(tau r))
       =D(0) exp(tau K) P E(0).                         (3)

Convergence is in every finite matrix norm. Thus, for this acquired
controller with fixed logical dimensions, it also controls the complete
channel error, not just one input fidelity. The formula tests the actual
first-order action on a retained slow subspace, rather than treating an
order1 surviving junk-permutation coefficient as a decoder.

To prove (3), split x_n=P x_n+Q x_n. The P block obeys

    p_(n+1)=(I+qK)p_n+q P T1 Q z_n,

and the Q block has a stable zero-order matrix A=Q T0 Q. In a suitable
finite-dimensional norm, ||A||<=theta<1; this follows from its strict
spectral-radius bound by an ordinary similarity/scaled-Jordan norm.
For small q its perturbation is still contracting. Iteration gives

    ||z_n||<=C theta_1^n||z_0||+C q max_(j<n)||p_j||,
    theta<theta_1<1.

For n<=tau/q, discrete Gronwall bounds p uniformly by a constant depending
on tau. The total perturbation of its Euler recurrence is
q sum||z_j||=O(q): the initial fast transient is summable, and the driven
part is O(q) at each of O(1/q) steps. Hence p_n differs by O(q) from
(I+qK)^n p_0; the latter tends to exp(tau K)p_0. For fixed positive tau,
z_floor(tau/q) tends to zero. Analytic E,D finish the proof. There is an
initial boundary layer: (3) is not asserted at tau=0 with E(0) in place
of P E(0).

If the RIGHT SIDE of (3) is itself shown to approach the logical identity
as tau->infinity, then for every fixed useful error epsilon one can choose
a finite tau(epsilon), then sufficiently large r, to obtain that complete
error using tau(epsilon)r+O(1) source cells. This would establish linear
rank scaling for that actual controller at fixed error. A joint uniform
O(r log(1/epsilon)) guarantee additionally requires explicit convergence
constants in r and tau; it is NOT inferred merely from (3).

If K=0, this test yields only D(0)P E(0), independent of positive tau.
It cannot claim a new inverse on the linear-r timescale. That is a
controller-specific statement, not a generic adaptive lower bound. If
there are other peripheral eigenvalues or nonsemisimple blocks, this
test does not apply until their actual dynamics are treated; they are
not silently discarded. A fixed full-period echo may help, but must be
part of the acquired physical cell.

This identifies the decisive missing interface in the current quantum
alternative: exhibit a physical reused-carrier cell with a useful K and
a finite final readout, or prove its K cannot transfer the logical
payload. Exact-success r² lower bounds do not settle this approximate
limit. Conversely, the exact algebra and a surviving coherence do not
by themselves supply the required cell or readout. No such positive
controller, spectrum or asymptotic advantage was executed here.

Linear query scaling is one test, not the sole value criterion. A decoder
matching the ordinary quadratic query bill could still matter if its
actual physical storage and known gate cost are smaller. Fixed-carrier
permutation cells use O(log D) gates per physical swap and a fixed known
memory, whereas the currently paid ordinary programme constructions
have their own acquisition, storage and controller costs. Those costs
must be compared with the strongest ordinary streaming implementation
before claiming an advantage; their current conservative bound is not
a lower bound on what ordinary methods can do. No storage/gate advantage
is acquired by the transfer formula alone.
