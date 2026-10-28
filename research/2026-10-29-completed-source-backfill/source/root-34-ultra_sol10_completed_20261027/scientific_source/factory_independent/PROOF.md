# Independent ordinary-chain and phase-type derivation

Scope: the supplied sequential, number-diagonal, balanced optical factory.
This is a derivation and bounded exact comparison, not a physical acquisition
or a proof of a computational separation. The independent code imports no
producer code except the explicitly named comparison and enclosure adapters.

## 1. Model and clock convention

The raw source distribution is (99/500,4/5,1/500) on photon counts 0,1,2.
All occupied photons share the same internal optical mode. A raw preparation
costs one source use and one clock, and its photons appear at the clock end.
The detector is a bucket detector with efficiency D=19/20 and no dark clicks.
Every photon already stored independently survives each clock with common
probability 0<lambda<=1.

For n=2m, prepare F_m on the left, then prepare F_m on the right while retaining
the left. Every right-child clock, including failed attempts and its final
clock, thins the retained left state. After both children return, spend one
fusion clock: thin both inputs, apply the balanced beamsplitter, retain port0,
and accept on no click at port1. A click discards both children and restarts
this F_n. Any ancestor-held modes keep losing throughout. Ancestor loss never
changes the current child's transitions or detector result.

The raw states are diagonal. For fixed total number a beamsplitter can create
two-port coherences, but tracing the herald mode against its diagonal bucket
effect leaves the retained mode number diagonal. Mixtures over total number
remain diagonal. Thus current photon counts and the program stack suffice;
one need not retain optical amplitudes or photon ages. This relies on the
supplied same-mode, independent, memoryless model.

## 2. Literal Markov construction

Let C_n be the transient controller states. C_1 contains one raw-preparation
state. If child states are s in C_m, C_n contains

* L(s): the left child is running;
* R(a,s), 0<=a<=n: the right child is running and a left photons are stored;
* F(a,b), 0<=a,b<=n: both children await the fusion clock.

The child can output up to 2m=n photons. Hence

    M_1=1,       M_n=(n+2)M_(n/2)+(n+1)^2.

In R(a,s), each clock combines the child's transition with the independent
binomial death of a. In F(a,b), independently thin both inputs before fusion;
on a click transition to L(start_m), and on no click absorb into output k.
The same rule recursively includes loss of every occupied ancestor buffer.

For i,j Fock inputs, set N=i+j and

    c_k=sum_a binom(i,a)binom(j,k-a)(-1)^(j-k+a),
    P_BS(k|i,j)=c_k^2 k!(N-k)!/[2^N i!j!].

These are obtained by expanding the two transformed creation-operator powers.
No-click weight is (1-D)^(N-k). The independent code performs input-side
binomial thinning followed by this Fock kernel; it does not assume the
producer's collapsed after-beamsplitter formula. The two formulas agree
exactly in every tested local component. Uniform independent loss commutes
with any passive beamsplitter, which also proves their equivalence generally.

The chain has transient matrix Q and absorption matrix R (column k is output
k). Each row of [Q R] sums exactly to one and is nonnegative. For the positive
fixtures all controller states are reachable. From any completed input pair,
the event of all photons surviving the fusion clock and bunching into port0
has probability at least q^(2n), q=lambda/2. Indeed the exact probability for
N<=2n photons is lambda^N binom(N,i)/2^N >=q^(2n).
The same induction at each finite level proves almost-sure absorption and
finite preparation moments. Thus I-Q is invertible and its inverse is the
nonnegative fundamental matrix.

## 3. Full costs and correlations

For any initial transient state define H_k(z)=E[1_(N=k) z^T]. One clock is
spent on every transition, including absorption, so

    H(z)=z(R+QH(z)),       H(z)=(I-zQ)^(-1)zR.

Let U=H(1), V=z H'(z)|_(z=1), and let W be the joint source-count first
moments. Let r_i be one if the current primitive action is a raw preparation,
zero if it is a fusion. The exact equations are

    (I-Q)U=R,
    (I-Q)V=U,
    (I-Q)W=diag(r)U.

The start row of U is the output law. The start rows of V and W are respectively
E[T 1_(N=k)] and E[C 1_(N=k)]. They determine the full mean cost and the actual
output/cost correlations without a waiting-time cutoff. Fusion rewards use
1-r. Since every clock is exactly one raw or fusion primitive,

    T=C+J                       on every trajectory.

The independent solver checks E[T]=E[C]+E[J] exactly. No failed prefix or final
fusion is normalized away. Costs are per eventual accepted output, whereas
the number n is the nominal leaf count of one successful protocol tree.

At n2 the attempts each last three clocks and final output is independent of
the number of previous attempts, giving Cov(N,T)=0. At n4 and lambda<1 the
retained state sees a random right-child duration. The exact main-fixture
Cov(N,T)=-0.027052820572463106 proves that factorizing state and waiting law
would change this model. The lossless n4 control has covariance exactly zero.

## 4. The equally informed structured phase-type comparator

Let L be the pure-death matrix on held counts 0,...,K. For the falling-factorial
function f_s(k)=(k)_s, independent thinning gives

    (L f_s)(k)=lambda^s f_s(k).

The matrix F_(k,s)=(k)_s is triangular with nonzero diagonal s!, so

    L F=F diag(1,lambda,...,lambda^K).

When a child with transient Q runs while that mode waits, the ordinary joint
transient matrix is Q tensor L. Absorption into child output j and held count
l at clock t uses Q^(t-1)R_j and L^t. Diagonalizing only L therefore changes
the ordinary joint resolvent into scalar blocks

    (I-z lambda^s Q)^(-1).

Equivalently, condition on a starting held count i and child output j:

    E[1_(N_child=j) z^T Pr(held=l | i,T)]
      =binom(i,l) sum_(s=0)^(i-l) (-1)^s binom(i-l,s)
                          H_child(j;z lambda^(l+s)).

This is exactly the proposed scalar shift contraction. It retains every
state/time correlation, rather than replacing child completion by its mean
or by a new geometric law. In `phase_type_waiting.py` an explicit 65-state
Q_child tensor L block is solved independently and agrees with all 125 joint
components of this formula at each of z=1 and z=lambda^2.

The equivalence is a constructive equally informed ordinary comparator. It
rules out inferring a general separation from the unreduced chain's state
count. The spectral reduction is a useful implementation of that ordinary
method on this model.

## 5. Nested finite closure and restarts

For a node of size a, its child has size a/2 and its retained sibling can hold
at most a photons. Consequently passing to that child shifts z=lambda^e by
lambda^s with 0<=s<=a. From root n to descendant size m, cumulative shift is

    e<=n+n/2+...+2m=2(n-m)<=2n-2.

This bound uses photon support, not an age or time truncation. It is valid for
unbounded waiting and arbitrarily many failures. With an external root
query z=lambda^e0 the bound is e0+2n-2. Common lambda makes these integer
spectral exponents close under nesting. Different rates or more general
memory channels need not admit the same small set.

Let A_k(z,u) be the joint output/time/source transform of one successful
attempt, and G(z,u) its total attempt transform. The failure transform is
F=G-sum_k A_k. At the current node a failure erases both inputs; independent
restarts therefore give H_k=A_k/(1-F). All source uses and clocks of a failed
attempt occur in F. This is the ordinary renewal/Schur-complement evaluation
of the literal chain. It is not an additional assumption of independence
between an attempt's duration, source cost and outcome.

## 6. Arithmetic and what is established

All literal-chain values are rational. The independent fraction-free solver
scales rows to integer form, asserts exact Bareiss divisibility, and verifies
every returned linear system over Fraction. At n4 it matches all nine output
probabilities, nine source-joint moments, nine time-joint moments and nine
additional-PGF components of the producer, at all three supplied/control
survivals. The independent n2 control matches all five of each type.

Directed dyadic arithmetic uses exact integer floor/ceiling. Corner extrema
enclose interval multiplication and division when the denominator excludes
zero. The compiler's operation graph then gives enclosures by induction.
Reading this arithmetic and independently comparing its n4 256-bit result
encloses the same 36 literal-chain components. Larger certificates have not
been replayed here.

Polynomial arithmetic count alone does not bound exact rational bit growth.
For approximate evaluation, true renewal denominators are at least q^(2n),
source expectations are at most n q^(-4n), and clocks at most twice that.
Finite-difference coefficient sums grow at most exponentially in n. A
polynomial-size arithmetic graph therefore has intermediate magnitudes and
local derivative bounds exp(poly(n,input bits)); sufficiently small outward
rounding requires poly(n,input bits)+O(log(1/error)) bits. This is a conservative
existence argument for this explicit graph, not an exact-rational complexity
claim or a measured advantage over its factored phase-type realization.
